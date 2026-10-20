# GCP Secret Manager + WIF Integration

## Role
You are an infrastructure agent provisioning GCP Secret Manager + Workload Identity Federation
for a GitHub repository. You operate entirely through GitHub Actions — never run `gcloud` or
`terraform` locally. Every secret is fetched at runtime by CI runners; no values ever appear
in committed files.

## Context — Read First
- `CLAUDE.md` — Token Inventory table, Agent Autonomy Policy (Level 1–3)
- `[your-journey-file]` — most recent entries for current secret/WIF status
- `terraform/` — existing Terraform files (if any — use as baseline)
- `docs/adr/0004-zero-trust-secrets.md` — policy ADR
- `docs/adr/0006-gcp-wif-bootstrap-terraform.md` — implementation ADR

## Prerequisites

| Prerequisite | How to verify |
|---|---|
| GCP Seed Project WIF operational (`tf-seed-1776532715`) | `gcp-bootstrap.yml` hardcodes Seed WIF provider — confirm with operator |
| Terraform SA (`terraform-sa@tf-seed-1776532715`) exists | GCP Console > IAM > Service Accounts |
| GCS state bucket (`tf-state-905978345393`) exists | GCP Console > Cloud Storage |
| `TF_VAR_BILLING_ACCOUNT` GitHub repo secret set | GitHub → Settings → Secrets and variables → Actions |
| `PAT_SECRETS_WRITE` GitHub repo secret set (value = PAT with `secrets:write`) | GitHub → Settings → Secrets → Actions |
| Branch protection on `main` requires PR | GitHub → Settings → Branches |

## Instructions

### Phase 1 — Write Terraform Infrastructure

Write 6 files under `terraform/`. Run `git ls-files terraform/` to check which already exist.

**`terraform/versions.tf`** — pin provider versions + GCS backend (`tf-state-<ORG_BUCKET_ID>`).

**`terraform/variables.tf`** — declare: `org_id`, `billing_account`, `project_id`, `github_repo`,
`github_org`. Use **multiline blocks** for ALL variables with a `default`:
```hcl
variable "github_org" {
  default = "bben15600-sys"
}
```
⚠️ Inline form `variable "x" { default = "y" }` causes HCL parse errors. Always use multiline.

**`terraform/main.tf`** — GCP project + 5 API enablements + mandatory 90s propagation sleep:
```hcl
resource "time_sleep" "api_propagation" {
  depends_on      = [google_project_service.apis]
  create_duration = "90s"
}
```
⚠️ WIF pool creation immediately after `google_project_service` returns 403. The `time_sleep`
with `depends_on` on ALL WIF + Secret Manager resources is mandatory.

**`terraform/wif.tf`** — WIF pool + provider + SA + IAM binding:
```hcl
attribute_condition = "attribute.repository.startsWith(\"${var.github_org}/\")"
...
member = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github.name}/*"
```
⚠️ `member = "principalSet://...attribute.repository/${org}/*"` is a literal string — GCP IAM
does NOT support `/*` as a wildcard in attribute values. Pool-level `/*` is the only correct
form. Org restriction is enforced by `attribute_condition` alone. See ADR 0011.

**`terraform/secrets.tf`** — one secret per name via `for_each` + resource-level IAM bindings:
```hcl
resource "google_secret_manager_secret_iam_member" "version_adder" {
  for_each  = google_secret_manager_secret.secrets
  role      = "roles/secretmanager.secretVersionAdder"
  member    = "serviceAccount:${google_service_account.github_actions.email}"
}
```
⚠️ DO NOT add `google_project_iam_member` for `roles/secretmanager.secretCreator` or
`secretVersionAdder` — these roles don't exist at project scope → Error 400. See ADR 0008.

⚠️ If a secret was created out-of-band before Terraform managed it, `terraform apply` fails
with Error 409. Fix: add an `import {}` block per pre-existing secret (Terraform 1.5+,
idempotent on subsequent applies):
```hcl
import {
  to = google_secret_manager_secret.secrets["SECRET_NAME"]
  id = "projects/<project-id>/secrets/SECRET_NAME"
}
```

**`terraform/outputs.tf`** — export `workload_identity_provider`, `service_account_email`,
`project_id`.

---

### Phase 2 — Write and Trigger `gcp-bootstrap.yml`

Triggers on `push: paths: terraform/**` (non-main branches) + `workflow_dispatch`.
Authenticates via **Seed Project WIF** (not the app WIF — that doesn't exist yet).

⚠️ **Bootstrap paradox**: `gcp-bootstrap.yml` creates GCP SM. It cannot fetch
`GITHUB_PAT_SECRETS_WRITE` from SM before SM exists. Keep the token as GitHub repo secret
`PAT_SECRETS_WRITE`. All other workflows fetch from GCP SM at runtime. See ADR 0010.

⚠️ **GitHub naming constraint**: GitHub rejects secret names starting with `GITHUB_`
(HTTP 422). Name the GitHub repo secret `PAT_SECRETS_WRITE`; GCP SM can use the full name.

```yaml
- id: auth
  uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: "projects/725011244321/.../github-provider"
    service_account: "terraform-sa@tf-seed-1776532715.iam.gserviceaccount.com"

- name: Set GitHub Secrets
  env:
    GH_TOKEN: ${{ secrets.PAT_SECRETS_WRITE }}   # NOT secrets.GITHUB_PAT_SECRETS_WRITE
  run: |
    gh secret set WIF_PROVIDER        --body "$WIF"
    gh secret set WIF_SERVICE_ACCOUNT --body "$SA"
    gh secret set GCP_PROJECT_ID      --body "$PID"
```

Push Terraform files + `gcp-bootstrap.yml` to a feature branch. The `terraform/**` push
auto-triggers the workflow. Wait for all steps green before Phase 3.

---

### Phase 3 — Write and Run `populate-secrets.yml` (SEED_ Pattern)

One-time `workflow_dispatch`. Uses **app project WIF** (available after Phase 2 completes).

Stage secret VALUES as temporary `SEED_<NAME>` GitHub repo secrets. The workflow reads them
as masked env vars → writes to GCP SM → deletes `SEED_*` on success:

```yaml
env:
  SEED_RAILWAY_TOKEN: ${{ secrets.SEED_RAILWAY_TOKEN }}
run: |
  printf '%s' "$SEED_RAILWAY_TOKEN" | gcloud secrets versions add "RAILWAY_TOKEN" \
    --project="$GCP_PROJECT_ID" --data-file=-
```

⚠️ `gcloud secrets versions add` fails silently if the secret shell doesn't exist in GCP SM
or if the SA lacks `secretVersionAdder` on it. Every secret written here MUST be declared in
`terraform/secrets.tf` AND `gcp-bootstrap.yml` must have run first.

For auto-generated secrets (keys, passwords), generate inline — never stage as `SEED_*`:
```bash
openssl rand -hex 32 | tr -d '\n' | gcloud secrets versions add "N8N_ENCRYPTION_KEY" \
  --project="$GCP_PROJECT_ID" --data-file=-
```

**Alternative: GCP Console direct insertion** — The operator can add secret values directly
via GCP Console → Secret Manager → select secret → "Add version". This is functionally
identical to the SEED_ workflow and is faster for one-time manual population. The SEED_
pattern is preferable for secrets that need to be rotated or automated; Console insertion
is acceptable for the initial PAT population where the operator is already present.

---

### Phase 4 — GitHub PAT Centralization (Human + Agent)

Fine-grained PAT creation is **human-only** — GitHub API cannot create fine-grained PATs
programmatically.

**Operator creates in GitHub UI (Settings → Developer settings → Fine-grained tokens):**

| Secret name in GCP SM | Scopes | Target repo | Purpose |
|---|---|---|---|
| `GITHUB_PAT_SKILL_SYNC` | `contents: read` | skills source repo | skill-sync.yml |
| `GITHUB_PAT_SKILL_WRITE` | `contents: write`, `pull-requests: write` | skills source repo | skill-contribute.yml |
| `GITHUB_PAT_SECRETS_WRITE` | `secrets: write` | this repo | bootstrap.yml, populate-secrets.yml |
| `GITHUB_PAT_ACTIONS_WRITE` | `actions: write` | this repo | agent autonomous `workflow_dispatch` (see ADR 0016) |

⚠️ **`GITHUB_PAT_ACTIONS_WRITE` is required for full agent autonomy.** Without it, every `workflow_dispatch` requires a human in the GitHub UI — violating the zero-operator-dashboard principle. Create this PAT at the same time as the other three.

**Write `rotate-github-pats.yml`** — `workflow_dispatch` with `secret_name` (choice enum) +
`new_token` (masked). WIF auth → writes new version to GCP SM → [your-telegram] confirmation.

⚠️ **[your-telegram] confirmation dependency**: `rotate-github-pats.yml` sends a [your-telegram] confirmation.
If [your-telegram] is not yet live (Stage 5 not complete), the confirmation step will fail (no `continue-on-error`).
The GCP SM write still succeeds — the [your-telegram] step is informational only. Do not block PAT
storage waiting for [your-telegram]; it can be wired in after Stage 5.

**Update all workflows** that used `secrets.CLAUDE_SKILLS_PAT`:
1. Add `permissions: id-token: write, contents: read`
2. Add WIF auth step (`google-github-actions/auth@v2`)
3. Add `google-github-actions/get-secretmanager-secrets` step
4. Replace `secrets.CLAUDE_SKILLS_PAT` → `steps.secrets.outputs.<PAT_NAME>`

After operator confirms PATs stored in GCP SM, delete the classic PAT from GitHub secrets.

⚠️ **`PAT_SECRETS_WRITE` check**: Verify `PAT_SECRETS_WRITE` contains the fine-grained `GITHUB_PAT_SECRETS_WRITE` value before treating Stage 3 complete. If it was set to a classic PAT as a bootstrap placeholder, update it now.

**Additional secrets stored during this stage** (not PATs — but stored in GCP SM as part of
the broader secret inventory):

| Secret name in GCP SM | Set by | Notes |
|---|---|---|
| `RAILWAY_PROJECT_ID` | `bootstrap.yml` (Stage 1 re-run) | UUID of the [your-railway] project; also stored as GitHub Secret for fast-path idempotency (ADR 0017) |
| `RAILWAY_ENVIRONMENT_ID` | `bootstrap.yml` (Stage 1 re-run) | UUID of the [your-railway] `production` environment (ADR 0017) |
| `N8N_ENCRYPTION_KEY` | `populate-secrets.yml` (auto-generated) | Required before first N8N boot; `openssl rand -hex 32` |
| `N8N_OWNER_PASSWORD` | `populate-secrets.yml` (auto-generated) | base64 format required — N8N rejects all-lowercase hex |
| `GITHUB_APP_PRIVATE_KEY` | operator (GCP Console) | Placeholder for future GitHub App credential (long-term PAT replacement) |
| `GITHUB_APP_ID` | operator (GCP Console) | Placeholder for future GitHub App credential |

Declare all of these in `terraform/secrets.tf` so `gcp-bootstrap.yml` creates the shells before
`populate-secrets.yml` writes the values.

---

### Phase 5 — End-to-End Verification

Trigger a WIF-authenticated workflow via GitHub Actions UI `workflow_dispatch`. Confirm:
1. `google-github-actions/auth` step ✅
2. `get-secretmanager-secrets` step ✅ (verifies IAM binding)
3. Functional step ✅

If WIF auth fails with `permission 'iam.serviceAccounts.getAccessToken' denied`:
- Check `terraform/wif.tf` IAM member — must be pool-level `/*`, not attribute-level
- Fix, commit, push → `gcp-bootstrap.yml` auto-triggers → re-test

Document E2E run ID in `[your-journey-file]`.

---

## Known Failures

| Failure | Symptom | Root Cause | Fix | ADR |
|---------|---------|-----------|-----|-----|
| API propagation race | Terraform fails at WIF pool creation with `403 API not enabled` | `iam.googleapis.com` not ready immediately after `google_project_service` | Add `time_sleep` (90s) in `main.tf` with `depends_on` on all WIF resources | 0006 |
| Invalid project-level IAM roles | `Error 400: roles/secretmanager.secretCreator is not supported` | Role doesn't exist at project scope — only at resource level | Remove `google_project_iam_member` for SM roles; use `for_each` in `secrets.tf` | 0008 |
| Pre-existing secret conflict | `Error 409: Secret X already exists` in `terraform apply` | Secret created out-of-band before Terraform managed it | Add `import {}` block in `secrets.tf` for each pre-existing secret | 0008 |
| WIF wildcard silent failure | `permission 'iam.serviceAccounts.getAccessToken' denied` everywhere | `attribute.repository/org/*` is a literal string — no real repo matches | Change member to pool-level `principalSet://.../${pool.name}/*` | 0011 |
| GitHub `GITHUB_*` naming | `gh secret set` returns HTTP 422 | GitHub forbids repo secrets starting with `GITHUB_` | Use `PAT_SECRETS_WRITE` as GitHub secret name; full name only in GCP SM | — |
| `gcloud secrets versions add` fails | Silent failure or `PERMISSION_DENIED` | Secret shell not pre-created in `secrets.tf` / `gcp-bootstrap.yml` not run yet | Pre-declare every secret in `secrets.tf`; run `gcp-bootstrap.yml` first | 0008 |
| Bootstrap paradox | "Set GitHub Secrets" step fails, `GH_TOKEN` empty | `gcp-bootstrap.yml` can't fetch from GCP SM before SM exists | Keep `PAT_SECRETS_WRITE` as GitHub secret for `gcp-bootstrap.yml` only | 0010 |
| HCL inline variable syntax | `terraform init` fails: HCL parse error or `unexpected token ";"` | Single-line or semicolon-terminated variable blocks rejected by HCL parser | Use fully multiline blocks for all variables | — |

---

## E2E Gate

```bash
# 1. gcp-bootstrap.yml fully green — all steps including "Set GitHub Secrets"
# 2. Trigger skill-sync.yml (or any WIF workflow) via workflow_dispatch
#    Confirm: WIF auth ✅, GCP SM fetch ✅, functional step ✅
# 3. Zero hardcoded values in any committed file:
grep -rn "TOKEN\|PASSWORD\|KEY\|SECRET" terraform/ .github/workflows/ \
  | grep -v "secret_name\|secret_id\|secretmanager\|#\|var\.\|\.name\|\.id\|GCP_PROJECT"
# Expected: zero matching lines
```

**Note on `secrets-sync.yml`**: Early BUILD-STAGES.md plans described a centralised
`secrets-sync.yml` workflow that would pull all secrets from GCP SM and inject them into
[your-railway] on a weekly schedule. This was **never built**. The pattern that was actually
adopted: each deployment workflow (deploy-n8n.yml, bootstrap.yml, configure-*.yml) fetches
its own required secrets inline via WIF + `get-secretmanager-secrets`. This is simpler
and more robust — each workflow is self-contained. There is no centralised sync job.
Do not attempt to build `secrets-sync.yml`; the per-workflow fetch pattern is the
correct approach for this system.

## Safety Rules

1. **NEVER add `google_project_iam_member` for Secret Manager roles** — these role names do not exist at project scope; use resource-level `for_each` bindings in `secrets.tf` only.
2. **NEVER name a GitHub repo secret with the `GITHUB_` prefix** — GitHub rejects it (HTTP 422); use `PAT_*` naming for GitHub secrets, full names inside GCP SM.
3. **NEVER call `gcloud secrets versions add` before `gcp-bootstrap.yml` has run** — secret shell and SA binding must pre-exist; there is no `secretCreator` fallback.
4. **NEVER use `attribute.repository/org/*` in the WIF IAM binding member** — literal string, not a wildcard; use pool-level `/*` with `attribute_condition` for org restriction.
5. **NEVER commit or log a secret value** — reference by name only; SEED_ pattern stages values as masked GitHub secrets and deletes them after population.
6. **NEVER run `terraform apply` locally** — no local GCP credentials; all Terraform runs are CI-only via `gcp-bootstrap.yml`.

## Examples

**User:** `/gcp-wif-secret-manager-integration`

**Agent behaviour:**
Reads CLAUDE.md + [your-journey-file] to confirm current GCP state. Verifies 6 prerequisites. Writes
6 Terraform files (multiline variable syntax, pool-level `/*` WIF binding, resource-level IAM
only, `import {}` blocks for any pre-existing secrets). Declares ALL secrets in `secrets.tf`
including non-PAT secrets (RAILWAY_PROJECT_ID, N8N_ENCRYPTION_KEY, GITHUB_APP_PRIVATE_KEY, etc.).
Writes `gcp-bootstrap.yml` referencing `secrets.PAT_SECRETS_WRITE` (not `GITHUB_PAT_SECRETS_WRITE`
— GitHub would reject that name). Commits and pushes to feature branch — `terraform/**` push
auto-triggers `gcp-bootstrap.yml`. Expects 2–3 runs before fully green (HCL syntax, IAM
roles, pre-existing secrets are common first-run failures). Waits for all steps including
"Set GitHub Secrets" to be green. Writes `populate-secrets.yml` — uses SEED_ pattern or
prompts operator to use GCP Console directly (both are equivalent). Writes
`rotate-github-pats.yml`. Asks operator to create **4 fine-grained PATs** (not 3 — include
`GITHUB_PAT_ACTIONS_WRITE` with `actions:write`). After operator confirms
GCP SM populated, triggers a WIF-authenticated workflow to verify E2E. If auth fails, checks
`wif.tf` for attribute wildcard trap and fixes to pool-level `/*`. Documents run ID in [your-journey-file].
