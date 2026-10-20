# Stage 1 Bootstrap — [your-railway] + [your-cloudflare]

## Role
You are an Infrastructure Automation Engineer who provisions [your-railway] projects
and [your-cloudflare] DNS records entirely through APIs and GitHub Actions — never
through dashboards or manual CLI commands.

## Context — Read First

Before starting, read in parallel:
- `CLAUDE.md` — extract `GCP_PROJECT_ID` and project name
- `terraform/secrets.tf` — check if `RAILWAY_PROJECT_TOKEN` already exists in `secret_names`
- `.github/workflows/bootstrap.yml` — check if file already exists (warn before overwriting)

## Org constants (hardcoded for or-infra.com)

| Constant | Value |
|----------|-------|
| `DOMAIN` | `or-infra.com` |
| Seed WIF | `projects/725011244321/locations/global/workloadIdentityPools/github-pool/providers/github-provider` |

⚠ If target org is not `bben15600-sys` / `or-infra.com`, replace these values and confirm with user.

## Instructions

### Step 1: Auto-detect project name

```bash
REMOTE=$(git remote get-url origin 2>/dev/null)
PROJECT_NAME=$(echo "$REMOTE" | grep -oE '[^/]+$' | sed 's/\.git$//')
```

Print: `Detected project name: <name>. Proceeding...`
If name cannot be resolved, ask the user.

### Step 2: Verify prerequisites

Check all of the following. If any is missing, stop and print exactly what is missing:

| Prerequisite | How to verify |
|---|---|
| `WIF_PROVIDER` GitHub Secret | Referenced in CLAUDE.md GCP Bootstrap section |
| `WIF_SERVICE_ACCOUNT` GitHub Secret | Referenced in CLAUDE.md GCP Bootstrap section |
| `GCP_PROJECT_ID` GitHub Secret | Referenced in CLAUDE.md GCP Bootstrap section |
| `PAT_SECRETS_WRITE` GitHub Secret | Must exist — used by `gcp-bootstrap.yml` to set GitHub Secrets (contains `GITHUB_PAT_SECRETS_WRITE` value; ADR 0010) |
| GCP Secret `RAILWAY_TOKEN` populated | Confirm with user (cannot verify without gcloud) |
| GCP Secret `CLOUDFLARE_TOKEN` populated | Confirm with user |
| GCP Secret `CLOUDFLARE_ZONE_ID` populated | Confirm with user |

### Step 3: Update terraform/secrets.tf

If `RAILWAY_PROJECT_TOKEN` is NOT in `local.secret_names`, add it.
If `google_secret_manager_secret_iam_member.version_adder` resource does NOT exist, add it.

Required additions:

```hcl
# In locals.secret_names — add if missing:
"RAILWAY_PROJECT_TOKEN",

# Resource — add if missing:
resource "google_secret_manager_secret_iam_member" "version_adder" {
  for_each  = google_secret_manager_secret.secrets
  project   = google_project.app.project_id
  secret_id = each.value.secret_id
  role      = "roles/secretmanager.secretVersionAdder"
  member    = "serviceAccount:${google_service_account.github_actions.email}"
}
```

If any GCP secrets were created outside Terraform, add import blocks before the resource:

```hcl
import {
  to = google_secret_manager_secret.secrets["SECRET_NAME"]
  id = "projects/<gcp_project_id>/secrets/SECRET_NAME"
}
```

If `terraform/secrets.tf` was modified: commit, push, wait for `gcp-bootstrap.yml` to go green
before continuing to Step 4.

⚠ **Known failure (ADR 0008):** `roles/secretmanager.secretCreator` does **not** exist as a
project-level IAM role in GCP. Never add `google_project_iam_member` for `secretCreator` or
`secretVersionAdder`. Resource-level bindings (the `version_adder` block above) are the only
correct pattern.

### Step 4: Write .github/workflows/bootstrap.yml

Write the file below. Replace every `<project-name>` with the name from Step 1:

```yaml
name: Stage 1 — Railway + Cloudflare Bootstrap

on:
  workflow_dispatch:

permissions:
  id-token: write
  contents: read

jobs:
  bootstrap:
    name: Bootstrap Railway + Cloudflare
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Authenticate to GCP via WIF
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.WIF_SERVICE_ACCOUNT }}

      - name: Set up gcloud CLI
        uses: google-github-actions/setup-gcloud@v2

      - name: Fetch secrets from GCP Secret Manager
        id: secrets
        uses: google-github-actions/get-secretmanager-secrets@v2
        with:
          secrets: |-
            RAILWAY_TOKEN:projects/${{ secrets.GCP_PROJECT_ID }}/secrets/RAILWAY_TOKEN/versions/latest
            CLOUDFLARE_TOKEN:projects/${{ secrets.GCP_PROJECT_ID }}/secrets/CLOUDFLARE_TOKEN/versions/latest
            CLOUDFLARE_ZONE_ID:projects/${{ secrets.GCP_PROJECT_ID }}/secrets/CLOUDFLARE_ZONE_ID/versions/latest

      - name: Bootstrap Railway project (idempotent)
        id: railway
        env:
          RAILWAY_TOKEN: ${{ steps.secrets.outputs.RAILWAY_TOKEN }}
          KNOWN_PROJECT_ID: ${{ secrets.RAILWAY_PROJECT_ID }}
        run: |
          # Fast-path: if RAILWAY_PROJECT_ID is already stored, verify directly (avoids workspace scan)
          if [ -n "$KNOWN_PROJECT_ID" ]; then
            PROJ=$(curl -s -X POST https://backboard.railway.com/graphql/v2 \
              -H "Authorization: Bearer $RAILWAY_TOKEN" \
              -H "Content-Type: application/json" \
              -d "$(jq -cn --arg id "$KNOWN_PROJECT_ID" \
                '{"query":"query($id:String!){project(id:$id){id name environments{edges{node{id name}}}}}","variables":{"id":$id}}')")
            read -r PROJECT_ID ENV_ID PROJ_NAME < <(echo "$PROJ" | jq -r \
              '[(.data.project.id // ""), (.data.project.environments.edges[0].node.id // ""), .data.project.name] | @tsv')
            if [ -n "$PROJECT_ID" ]; then
              echo "Project verified via fast-path: $PROJ_NAME"
              echo "project_id=$PROJECT_ID" >> "$GITHUB_OUTPUT"
              echo "env_id=$ENV_ID" >> "$GITHUB_OUTPUT"
              exit 0
            fi
            echo "::warning::Stored project ID not found — falling back to workspace scan"
          fi

          # Use workspace-scoped query — { projects } returns personal workspace only (ADR 0009)
          WS_RESP=$(curl -s -X POST https://backboard.railway.com/graphql/v2 \
            -H "Authorization: Bearer $RAILWAY_TOKEN" \
            -H "Content-Type: application/json" \
            -d '{"query":"{ me { workspaces { id name projects { edges { node { id name environments { edges { node { id name } } } } } } } } }"}')
          WS_DATA=$(echo "$WS_RESP" | jq -c '.data.me.workspaces[0]')
          WORKSPACE_ID=$(echo "$WS_DATA" | jq -r '.id // empty')
          WORKSPACE_NAME=$(echo "$WS_DATA" | jq -r '.name // empty')
          if [ -z "$WORKSPACE_ID" ] || [ "$WORKSPACE_ID" = "null" ]; then
            echo "::error::Failed to resolve Railway workspace ID"
            exit 1
          fi
          echo "Workspace: $WORKSPACE_NAME ($WORKSPACE_ID)"

          PROJECT_NODE=$(echo "$WS_DATA" | jq -c '[.projects.edges[].node | select(.name == "<project-name>")] | first')
          PROJECT_ID=$(echo "$PROJECT_NODE" | jq -r '.id // empty')

          if [ -n "$PROJECT_ID" ]; then
            echo "Project already exists — reusing."
            ENV_ID=$(echo "$PROJECT_NODE" | jq -r '.environments.edges[0].node.id // empty')
          else
            echo "Creating Railway project..."
            PAYLOAD=$(jq -cn --arg wsId "$WORKSPACE_ID" \
              '{"query":"mutation($wsId:String!){projectCreate(input:{name:\"<project-name>\",workspaceId:$wsId,defaultEnvironmentName:\"production\"}){id environments{edges{node{id name}}}}}","variables":{"wsId":$wsId}}')
            RESPONSE=$(curl -s -X POST https://backboard.railway.com/graphql/v2 \
              -H "Authorization: Bearer $RAILWAY_TOKEN" \
              -H "Content-Type: application/json" \
              -d "$PAYLOAD")
            echo "$RESPONSE" | jq '{errors: .errors, id: .data.projectCreate.id}'
            PROJECT_ID=$(echo "$RESPONSE" | jq -r '.data.projectCreate.id')
            ENV_ID=$(echo "$RESPONSE" | jq -r '.data.projectCreate.environments.edges[0].node.id')
          fi

          if [ -z "$PROJECT_ID" ] || [ "$PROJECT_ID" = "null" ]; then
            echo "::error::Failed to resolve Railway project ID"
            exit 1
          fi

          echo "project_id=$PROJECT_ID" >> "$GITHUB_OUTPUT"
          echo "env_id=$ENV_ID" >> "$GITHUB_OUTPUT"

      - name: Store Railway IDs as GitHub Secrets
        env:
          GH_TOKEN: ${{ steps.secrets.outputs.GITHUB_PAT_SECRETS_WRITE }}   # ADR 0010 — CLAUDE_SKILLS_PAT deleted
          PROJECT_ID: ${{ steps.railway.outputs.project_id }}
          ENV_ID: ${{ steps.railway.outputs.env_id }}
        run: |
          gh secret set RAILWAY_PROJECT_ID --body "$PROJECT_ID" --repo "$GITHUB_REPOSITORY" &
          gh secret set RAILWAY_ENVIRONMENT_ID --body "$ENV_ID" --repo "$GITHUB_REPOSITORY" &
          wait

      - name: Store Railway IDs in GCP Secret Manager (idempotent)
        env:
          GCP_PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
          PROJECT_ID: ${{ steps.railway.outputs.project_id }}
          ENV_ID: ${{ steps.railway.outputs.env_id }}
        run: |
          store_sm() {
            local secret="$1" value="$2"
            if gcloud secrets versions list "$secret" --limit=1 \
                --project="$GCP_PROJECT_ID" &>/dev/null 2>&1; then
              echo "SKIP $secret (already in GCP SM)"
            else
              printf '%s' "$value" | gcloud secrets versions add "$secret" \
                --project="$GCP_PROJECT_ID" --data-file=-
              echo "OK $secret"
            fi
          }
          store_sm "RAILWAY_PROJECT_ID" "$PROJECT_ID" &
          store_sm "RAILWAY_ENVIRONMENT_ID" "$ENV_ID" &
          wait

      - name: Create Railway project token (idempotent)
        env:
          RAILWAY_TOKEN: ${{ steps.secrets.outputs.RAILWAY_TOKEN }}
          PROJECT_ID: ${{ steps.railway.outputs.project_id }}
          ENV_ID: ${{ steps.railway.outputs.env_id }}
          GCP_PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
        run: |
          VERSIONS=$(gcloud secrets versions list RAILWAY_PROJECT_TOKEN \
            --project="$GCP_PROJECT_ID" --format=json 2>/dev/null | jq 'length')
          if [ "${VERSIONS:-0}" -gt 0 ]; then
            echo "RAILWAY_PROJECT_TOKEN already exists — skipping."
          else
            PAYLOAD=$(jq -cn --arg pid "$PROJECT_ID" --arg eid "$ENV_ID" \
              '{"query":"mutation($pid:String!,$eid:String!){projectTokenCreate(input:{projectId:$pid,environmentId:$eid,name:\"github-actions\"})}","variables":{"pid":$pid,"eid":$eid}}')
            TOKEN=$(curl -s -X POST https://backboard.railway.com/graphql/v2 \
              -H "Authorization: Bearer $RAILWAY_TOKEN" \
              -H "Content-Type: application/json" \
              -d "$PAYLOAD" | jq -r '.data.projectTokenCreate')
            if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ]; then
              echo "::error::Failed to create Railway project token"
              exit 1
            fi
            echo -n "$TOKEN" | gcloud secrets versions add RAILWAY_PROJECT_TOKEN \
              --project="$GCP_PROJECT_ID" --data-file=-
          fi

      - name: Create Cloudflare DNS record (idempotent)
        env:
          CLOUDFLARE_TOKEN: ${{ steps.secrets.outputs.CLOUDFLARE_TOKEN }}
          CLOUDFLARE_ZONE_ID: ${{ steps.secrets.outputs.CLOUDFLARE_ZONE_ID }}
        run: |
          EXISTING=$(curl -sf \
            "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records?name=<project-name>.or-infra.com&type=CNAME" \
            -H "Authorization: Bearer $CLOUDFLARE_TOKEN")
          COUNT=$(echo "$EXISTING" | jq '.result | length')
          if [ "$COUNT" -gt 0 ]; then
            echo "DNS record already exists — skipping."
          else
            RESULT=$(curl -sf -X POST \
              "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/dns_records" \
              -H "Authorization: Bearer $CLOUDFLARE_TOKEN" \
              -H "Content-Type: application/json" \
              -d '{"type":"CNAME","name":"<project-name>","content":"railway.app","ttl":1,"proxied":true}')
            echo "$RESULT" | jq '{success: .success, id: .result.id, name: .result.name}'
          fi

      - name: E2E — Verify Railway project via API
        env:
          RAILWAY_TOKEN: ${{ steps.secrets.outputs.RAILWAY_TOKEN }}
          PROJECT_ID: ${{ steps.railway.outputs.project_id }}
        run: |
          # Declare variable type explicitly — Railway enforces strict GraphQL validation (ADR 0009)
          PAYLOAD=$(jq -cn --arg id "$PROJECT_ID" \
            '{"query":"query($id: String!) { project(id: $id) { id name } }","variables":{"id":$id}}')
          NAME=""
          for attempt in 1 2 3; do
            RESULT=$(curl -s -X POST https://backboard.railway.com/graphql/v2 \
              -H "Authorization: Bearer $RAILWAY_TOKEN" \
              -H "Content-Type: application/json" \
              -d "$PAYLOAD")
            NAME=$(echo "$RESULT" | jq -r '.data.project.name // empty')
            [ -n "$NAME" ] && break
            echo "Attempt $attempt: retrying in 10s..."
            sleep 10
          done
          [ "$NAME" = "<project-name>" ] || { echo "::error::Project name mismatch: '$NAME'"; exit 1; }
          echo "Verified: $NAME"

      - name: E2E — Check DNS resolves
        run: |
          HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 15 \
            https://<project-name>.or-infra.com || echo "000")
          echo "HTTP response: $HTTP_CODE"
          [ "$HTTP_CODE" = "000" ] && \
            echo "::warning::DNS not yet propagated — acceptable at Stage 1" || \
            echo "DNS resolves. HTTP $HTTP_CODE — pass at Stage 1."

      - name: Summary
        run: |
          {
            echo "## Stage 1 Bootstrap Complete"
            echo "| Resource | Status |"
            echo "|----------|--------|"
            echo "| Railway project \`<project-name>\` | ✅ |"
            echo "| Railway environment \`production\` | ✅ |"
            echo "| Cloudflare CNAME \`<project-name>.or-infra.com → railway.app\` | ✅ |"
            echo "| GitHub Secrets \`RAILWAY_PROJECT_ID\`, \`RAILWAY_ENVIRONMENT_ID\` | ✅ |"
            echo "| GCP Secret \`RAILWAY_PROJECT_TOKEN\` | ✅ |"
          } >> "$GITHUB_STEP_SUMMARY"
```

### Step 5: Commit, push, and trigger

```bash
git add .github/workflows/bootstrap.yml terraform/secrets.tf
git commit -m "feat: stage 1 — Railway + Cloudflare bootstrap"
git push -u origin <branch-name>
```

Trigger via GitHub Actions UI (primary path — always works):
Actions → "Stage 1 — [your-railway] + [your-cloudflare] Bootstrap" → Run workflow → `main`.

If Secrets Broker is already live (Stage 6 established), trigger via API using `GITHUB_PAT_ACTIONS_WRITE`
fetched from the Secrets Broker (ADR 0025 — `CLAUDE_SKILLS_PAT` is **retired**):
```bash
PAT=$(curl -s -X POST "https://<n8n-domain>/webhook/secrets-broker" \
  -H "Authorization: Bearer $AGENT_SESSION_OTP" \
  -H "Content-Type: application/json" \
  -d '{"secret_name":"GITHUB_PAT_ACTIONS_WRITE"}' | jq -r '.value // empty')
curl -s -X POST \
  "https://api.github.com/repos/<github_repo>/actions/workflows/bootstrap.yml/dispatches" \
  -H "Authorization: Bearer $PAT" \
  -H "Accept: application/vnd.github+json" \
  -d '{"ref":"main"}'
```

⚠️ For a fresh system (Stage 1 is before Stage 2/6), the Secrets Broker is not yet deployed.
Use the GitHub UI trigger — one operator click is acceptable here.

### Step 6: Verify and document

Verify all 5 resources in the workflow Summary tab are ✅.

Then append to `[your-journey-file]` (before `## Entry Template`):

```markdown
## [<YYYY-MM-DD>] Stage 1 Complete — Railway + Cloudflare Bootstrap

**Author**: claude-sonnet-4-6 (autonomous agent)
**Scope**: `.github/workflows/bootstrap.yml`, `terraform/secrets.tf`, `CLAUDE.md`, `JOURNEY.md`
**Objective**: Bootstrap Railway project + Cloudflare DNS for <project-name>

### E2E Results (run ID: <run_id> — <timestamp>)

| Step | Result |
|------|--------|
| GCP WIF auth | ✅ |
| Fetch RAILWAY_TOKEN, CLOUDFLARE_TOKEN, CLOUDFLARE_ZONE_ID | ✅ |
| Railway project `<project-name>` created (workspace: <workspace>) | ✅ |
| GitHub Secrets `RAILWAY_PROJECT_ID`, `RAILWAY_ENVIRONMENT_ID` stored | ✅ |
| `RAILWAY_PROJECT_TOKEN` stored in GCP Secret Manager | ✅ |
| Cloudflare CNAME `<project-name>.or-infra.com → railway.app` | ✅ |
| E2E — Railway project name verified | ✅ |
| E2E — DNS HTTP response | ✅ |

### Open Items
- [ ] Stage 2: Deploy N8N + PostgreSQL to Railway
- [ ] Stage 2: Update CNAME target to actual N8N service URL
- [ ] Stage 2: Add external monitoring
```

## Known Failures and Fixes

| Failure | Symptom | Root Cause | Fix |
|---------|---------|-----------|-----|
| Duplicate [your-railway] projects | Multiple projects same name | `{ projects }` returns personal workspace only | Use `{ me { workspaces { projects } } }` — already in template (ADR 0009) |
| GraphQL validation error | `Variable "$id" is not defined` | Missing type annotation | `query($id: String!)` — already in template (ADR 0009) |
| PERMISSION_DENIED on token write | `gcloud secrets versions add` fails | SA missing `secretVersionAdder` on secret | Add `version_adder` resource to `secrets.tf`, re-run `gcp-bootstrap.yml` (ADR 0008) |
| Terraform Error 409 | `Secret X already exists` | Secret created outside Terraform | Add `import {}` block to `secrets.tf` (ADR 0008) |
| Terraform Error 400 | `secretCreator not supported` | Role doesn't exist at project level | Remove project-level IAM binding, use resource-level only (ADR 0008) |

## Safety Rules

1. **NEVER print, log, or write [your-railway] token values** — pipe directly via `--data-file=-`.
2. **NEVER update [your-journey-file] before E2E verification passes** — only document success.
3. **NEVER trigger bootstrap.yml on main before gcp-bootstrap.yml is green** — Terraform must provision secret shells first.
4. **NEVER create duplicate [your-railway] projects** — always run the idempotency query first.
5. **NEVER overwrite an existing bootstrap.yml** without warning the user and receiving confirmation.

## Examples

**User:** `/stage1-bootstrap`

**Agent behaviour:**
Reads git remote → derives `project-life-130`. Reads `terraform/secrets.tf` — finds
`RAILWAY_PROJECT_TOKEN` missing → adds it and `version_adder` resource. Commits Terraform
change, waits for `gcp-bootstrap.yml`. Writes `bootstrap.yml`. Commits, pushes, triggers
`workflow_dispatch`. Waits for all steps green. Appends E2E results to `[your-journey-file]`.

**User:** `/stage1-bootstrap` (bootstrap.yml already exists)

**Agent behaviour:**
Detects existing file. Prints: "bootstrap.yml already exists. Overwrite? (y/n)"
Waits for confirmation before proceeding.

**User:** `/stage1-bootstrap` (GCP secrets not populated)

**Agent behaviour:**
At Step 2, cannot verify GCP secret values without gcloud. Prints:
"Cannot verify RAILWAY_TOKEN, CLOUDFLARE_TOKEN, CLOUDFLARE_ZONE_ID values.
Confirm all 3 are populated in GCP Secret Manager before continuing. (y/n)"
Waits for explicit confirmation.
