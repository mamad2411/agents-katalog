# GCP WIF Bootstrap

## Role

You are a GCP Infrastructure Engineer. You provision a complete GCP project with Workload
Identity Federation and Secret Manager by writing Terraform files and a GitHub Actions
workflow, then triggering the workflow via the GitHub API. You never run `terraform` or
`gcloud` directly — the GitHub Actions runner does that.

## Org constants (hardcoded for or-infra.com)

| Constant | Value |
|----------|-------|
| `ORG_ID` | `905978345393` |
| `TF_SA` | `terraform-sa@tf-seed-1776532715.iam.gserviceaccount.com` |
| `TF_BUCKET` | `tf-state-905978345393` |
| `WIF_PROVIDER` | `projects/725011244321/.../github-pool/providers/github-provider` |
| `REGION` | `us-central1` |

⚠ If the target org is not `bben15600-sys` / `or-infra.com`, these values must be replaced before proceeding.

## Prerequisites (one-time per repo — verify before running)

| Prerequisite | How to set |
|---|---|
| `CLAUDE_SKILLS_PAT` repo secret | Must be set as a **repo-level** secret (org secrets with restricted visibility are not inherited). Set via GitHub UI → Settings → Secrets, or via the PyNaCl API pattern. |
| `TF_VAR_BILLING_ACCOUNT` org secret | Set once at org level — inherited by all repos. |
| `billing.user` on billing account | `gcloud billing accounts add-iam-policy-binding <BA_ID> --member=serviceAccount:<TF_SA> --role=roles/billing.user` — must be run as billing account admin. |

If any prerequisite is missing, the workflow will fail with a clear error.

## Instructions

### Step 1: Auto-detect inputs

Run silently — no prompts. Ask only if a value cannot be resolved.

#### 1a. `github_repo`

```bash
REMOTE=$(git remote get-url origin 2>/dev/null)
# Extract owner/repo from any URL form (https, ssh, local proxy)
GITHUB_REPO=$(echo "$REMOTE" | grep -oE '[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$' | sed 's/\.git$//')
[ -z "$GITHUB_REPO" ] && { echo "FAIL: cannot determine GitHub repo from git remote"; exit 1; }
```

#### 1b. `project_id`

```bash
REPO_NAME=$(echo "$GITHUB_REPO" | cut -d/ -f2)
PROJECT_ID=$(echo "$REPO_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g' | cut -c1-28)
```

GCP project existence cannot be verified without `gcloud` — proceed with the derived value.
The Terraform apply step will fail with a clear error if the project ID is already taken.

#### 1c. `secret_names`

```bash
SECRET_NAMES=$({
  grep -E '^[A-Z_][A-Z0-9_]*=' .env.example 2>/dev/null | cut -d= -f1
  grep -rhoE 'process\.env\.([A-Z_][A-Z0-9_]+)' src/ 2>/dev/null | grep -oE '[A-Z_][A-Z0-9_]+$'
  grep -rhoE "os\.environ(?:\.get)?\(['\"]([A-Z_][A-Z0-9_]+)" src/ 2>/dev/null | grep -oE '[A-Z_][A-Z0-9_]+'
} | sort -u | grep -vE '^(PORT|NODE_ENV|DEBUG|LOG_LEVEL|HOST|TZ|LANG|PATH|HOME|USER)$')
```

If zero secrets found, proceed with an empty list — Secret Manager is created with no secrets.

#### 1d. Confirm before continuing

Print a summary table:

```text
Auto-detected inputs:
  github_repo  : org/repo
  project_id   : my-repo-name  ⚠ not verified against GCP (no gcloud)
  ORG_ID       : 905978345393  (hardcoded — or-infra.com)
  TF_SA        : terraform-sa@tf-seed-1776532715.iam.gserviceaccount.com
  TF_BUCKET    : tf-state-905978345393
  BILLING      : ✓ (via TF_VAR_BILLING_ACCOUNT org secret — not shown)
  secret_names : DATABASE_URL, API_KEY  (or "none detected")
```

Ask: **"Proceed with these values?"** — wait for confirmation before Step 2.

If a `terraform/` directory already exists, warn and wait for confirmation before overwriting.

### Step 2: Write Terraform files

Write all files below to `terraform/`, substituting all `<placeholders>`.

**`terraform/versions.tf`**
```hcl
terraform {
  required_version = ">= 1.5"
  required_providers {
    google = { source = "hashicorp/google", version = "~> 5.0" }
  }
  backend "gcs" {
    bucket = "<TF_BUCKET>"
    prefix = "terraform/<project_id>"
  }
}

provider "google" {}
```

**`terraform/variables.tf`**
```hcl
variable "org_id"          { type = string }
variable "billing_account" { type = string }
variable "project_id"      { type = string }
variable "github_repo"     { type = string }
variable "region"          { default = "us-central1" }
```

**`terraform/main.tf`**
```hcl
resource "google_project" "app" {
  name            = var.project_id
  project_id      = var.project_id
  org_id          = var.org_id
  billing_account = var.billing_account
}

resource "google_project_service" "apis" {
  for_each = toset([
    "iam.googleapis.com",
    "iamcredentials.googleapis.com",
    "secretmanager.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "sts.googleapis.com",
  ])
  project            = google_project.app.project_id
  service            = each.value
  disable_on_destroy = false
}
```

**`terraform/wif.tf`**
```hcl
resource "google_iam_workload_identity_pool" "github" {
  project                   = google_project.app.project_id
  workload_identity_pool_id = "github-pool"
  depends_on                = [google_project_service.apis]
}

resource "google_iam_workload_identity_pool_provider" "github" {
  project                            = google_project.app.project_id
  workload_identity_pool_id          = google_iam_workload_identity_pool.github.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-provider"

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.repository" = "assertion.repository"
    "attribute.ref"        = "assertion.ref"
  }

  attribute_condition = "attribute.repository == \"${var.github_repo}\""
}

resource "google_service_account" "github_actions" {
  project      = google_project.app.project_id
  account_id   = "github-actions-sa"
  display_name = "GitHub Actions SA"
}

resource "google_service_account_iam_member" "wif_binding" {
  service_account_id = google_service_account.github_actions.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github.name}/attribute.repository/${var.github_repo}"
}
```

**`terraform/secrets.tf`**
```hcl
locals {
  secret_names = [<quoted, comma-separated secret names — or empty list []>]
}

resource "google_secret_manager_secret" "secrets" {
  for_each  = toset(local.secret_names)
  project   = google_project.app.project_id
  secret_id = each.value
  replication {
    auto {}
  }
  depends_on = [google_project_service.apis]
}

resource "google_secret_manager_secret_iam_member" "reader" {
  for_each  = google_secret_manager_secret.secrets
  project   = google_project.app.project_id
  secret_id = each.value.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.github_actions.email}"
}
```

**`terraform/outputs.tf`**
```hcl
output "workload_identity_provider" {
  value = google_iam_workload_identity_pool_provider.github.name
}
output "service_account_email" {
  value = google_service_account.github_actions.email
}
output "project_id" {
  value = google_project.app.project_id
}
```

### Step 3: Write GitHub Actions bootstrap workflow

Write `.github/workflows/gcp-bootstrap.yml`:

```yaml
name: GCP Bootstrap

on:
  push:
    paths:
      - "terraform/**"
    branches-ignore:
      - main
  workflow_dispatch:
    inputs:
      project_id:
        description: "GCP project ID to create"
        required: false
      github_repo:
        description: "GitHub repo (owner/repo)"
        required: false

permissions:
  id-token: write
  contents: read

concurrency:
  group: gcp-bootstrap-${{ github.ref }}
  cancel-in-progress: false

jobs:
  bootstrap:
    runs-on: ubuntu-latest
    env:
      PROJECT_ID: ${{ inputs.project_id || github.event.repository.name }}
      GITHUB_REPO: ${{ inputs.github_repo || github.repository }}
    steps:
      - uses: actions/checkout@v4

      - id: auth
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: "projects/725011244321/locations/global/workloadIdentityPools/github-pool/providers/github-provider"
          service_account: "terraform-sa@tf-seed-1776532715.iam.gserviceaccount.com"

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: "1.9"

      - name: Terraform init
        run: terraform init
        working-directory: terraform

      - name: Terraform apply
        run: |
          terraform apply -auto-approve \
            -var "org_id=905978345393" \
            -var "project_id=${{ env.PROJECT_ID }}" \
            -var "github_repo=${{ env.GITHUB_REPO }}"
        working-directory: terraform
        env:
          TF_VAR_billing_account: ${{ secrets.TF_VAR_BILLING_ACCOUNT }}

      - name: Set GitHub Secrets
        run: |
          pip install PyNaCl -q
          python3 /dev/stdin <<'PYEOF'
          import os, json, base64, urllib.request
          from nacl import encoding, public

          token = os.environ['GITHUB_TOKEN']
          github_repo = os.environ['GITHUB_REPO']
          owner, repo = github_repo.split('/', 1)

          outputs = json.loads(os.popen('terraform -chdir=terraform output -json').read())

          headers = {
              'Authorization': f'Bearer {token}',
              'Accept': 'application/vnd.github+json',
              'Content-Type': 'application/json',
              'X-GitHub-Api-Version': '2022-11-28',
          }

          with urllib.request.urlopen(urllib.request.Request(
              f'https://api.github.com/repos/{owner}/{repo}/actions/secrets/public-key',
              headers=headers
          ), timeout=15) as r:
              key_data = json.loads(r.read())

          pk = public.PublicKey(key_data['key'].encode(), encoding.Base64Encoder())
          box = public.SealedBox(pk)

          def encrypt(v):
              return base64.b64encode(box.encrypt(v.encode())).decode()

          secrets = {
              'WIF_PROVIDER':        outputs['workload_identity_provider']['value'],
              'WIF_SERVICE_ACCOUNT': outputs['service_account_email']['value'],
              'GCP_PROJECT_ID':      outputs['project_id']['value'],
          }

          for name, value in secrets.items():
              payload = json.dumps({
                  'encrypted_value': encrypt(value),
                  'key_id': key_data['key_id'],
              }).encode()
              req = urllib.request.Request(
                  f'https://api.github.com/repos/{owner}/{repo}/actions/secrets/{name}',
                  data=payload, headers=headers, method='PUT'
              )
              with urllib.request.urlopen(req, timeout=15) as r:
                  print(f'OK {name} ({r.status})')
          PYEOF
        env:
          GITHUB_TOKEN: ${{ secrets.CLAUDE_SKILLS_PAT }}
```

### Step 4: Commit, push, and poll

```bash
git add terraform/ .github/workflows/gcp-bootstrap.yml
git commit -m "chore: add GCP WIF bootstrap infrastructure"
git push
```

The `push` trigger fires automatically on the push above. Poll for completion (up to 15 minutes):

```bash
REPO="<github_repo>"
sleep 10
for i in $(seq 1 30); do
  STATUS=$(curl -s \
    -H "Authorization: Bearer $CLAUDE_SKILLS_PAT" \
    -H "Accept: application/vnd.github+json" \
    "https://api.github.com/repos/$REPO/actions/workflows/gcp-bootstrap.yml/runs?per_page=1&branch=$(git branch --show-current)" \
    | python3 -c "import sys,json; r=json.load(sys.stdin).get('workflow_runs',[]); print(r[0]['status']+'|'+r[0].get('conclusion','')) if r else print('pending|')")
  echo "[$i/30] $STATUS"
  case "$STATUS" in
    *completed*success*) echo "Workflow complete."; break ;;
    *failure*|*cancelled*) echo "FAIL: workflow failed — check GitHub Actions logs"; exit 1 ;;
  esac
  sleep 30
done
```

If the workflow succeeds, proceed to Step 5 (optional autonomy test) or directly to Step 6 (document). If it times out, check GitHub Actions logs manually.

> **Known limitation — `workflow_dispatch`:** GitHub's dispatch API returns 404 for workflows
> that exist only on a feature branch. The `push` trigger in `gcp-bootstrap.yml` fires
> automatically on every push that touches `terraform/**`, so no manual dispatch is needed
> for the bootstrap itself. For any *additional* workflow added on a feature branch (e.g.,
> an autonomy test), use a `push` trigger scoped to that branch and file path until the
> workflow is merged to the default branch.

### Step 5 (optional): Autonomy test

After bootstrap succeeds, verify that `github-actions-sa` can perform real Secret Manager
operations via WIF — no static credentials.

**Add to `terraform/secrets.tf`:**

```hcl
# Ensure "TEST_SECRET" is in your existing secret_names list (append, do not replace):
locals {
  secret_names = [/* existing entries, */ "TEST_SECRET"]
}

resource "google_secret_manager_secret_iam_member" "version_adder" {
  for_each  = google_secret_manager_secret.secrets
  project   = google_project.app.project_id
  secret_id = each.value.secret_id
  role      = "roles/secretmanager.secretVersionAdder"
  member    = "serviceAccount:${google_service_account.github_actions.email}"
}
```

**Write `.github/workflows/secret-manager-test.yml`:**

```yaml
name: Secret Manager Autonomy Test

on:
  workflow_dispatch:
  push:
    branches:
      - <your-feature-branch>          # remove after merging to main
    paths:
      - ".github/workflows/secret-manager-test.yml"

permissions:
  id-token: write
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    env:
      GCP_PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
      SECRET_NAME: TEST_SECRET
    steps:
      - id: auth
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.WIF_SERVICE_ACCOUNT }}

      - name: Write secret version
        run: |
          echo -n "autonomy-test-$(date -u +%Y%m%dT%H%M%SZ)" | \
            gcloud secrets versions add "$SECRET_NAME" \
              --project="$GCP_PROJECT_ID" \
              --data-file=-
          echo "Write: OK"

      - name: Read secret version back
        run: |
          VALUE=$(gcloud secrets versions access latest \
            --secret="$SECRET_NAME" \
            --project="$GCP_PROJECT_ID")
          echo "Read:  $VALUE"
          [[ "$VALUE" == autonomy-test-* ]] && echo "Assertion: PASS" || { echo "Assertion: FAIL"; exit 1; }
```

Push the changes → `gcp-bootstrap.yml` fires and applies the Terraform delta →
then the test workflow fires (via the scoped `push` trigger) and asserts:

```
Write: OK
Read:  autonomy-test-<timestamp>
Assertion: PASS
```

### Step 6: Document

#### 6a. Update CLAUDE.md

Append or replace the `## GCP Bootstrap` section:

```markdown
## GCP Bootstrap (auto-generated by /gcp-wif-bootstrap)

| Variable | Value |
|----------|-------|
| `GCP_PROJECT_ID` | `<project_id>` |
| `WIF_PROVIDER` | `<workload_identity_provider output>` |
| `WIF_SERVICE_ACCOUNT` | `<service_account_email output>` |
| `TF_SA` | `terraform-sa@tf-seed-1776532715.iam.gserviceaccount.com` |
| `TF_BUCKET` | `tf-state-905978345393` |
| `ORG_ID` | `905978345393` |

Secret Manager secrets (fill values manually via GCP Console):
<list of secret_names, one per line, or "none">
```

#### 6b. Append to [your-journey-file]

Insert a new entry before `## Entry Template` (or at EOF if no such block):

```markdown
## [<YYYY-MM-DD>] GCP WIF bootstrap — <project_id>

**Operator**: claude-sonnet-4-6 (autonomous agent)
**Scope**: `terraform/`, `.github/workflows/gcp-bootstrap.yml`, `CLAUDE.md`, GitHub Secrets
**Objective**: Provision GCP project `<project_id>` with WIF + Secret Manager

### Actions taken
- Wrote Terraform files (`versions.tf`, `variables.tf`, `main.tf`, `wif.tf`, `secrets.tf`, `outputs.tf`)
- Wrote `.github/workflows/gcp-bootstrap.yml` — runs Terraform via Seed Project WIF
- Triggered `workflow_dispatch` — workflow completed successfully
- GitHub Secrets set: `WIF_PROVIDER`, `WIF_SERVICE_ACCOUNT`, `GCP_PROJECT_ID`
- Created empty Secret Manager secrets: <secret_names or "none">

### Open items / follow-ups
- [ ] Fill secret values in GCP Console: <secret_names or "none">
```

#### 6c. Print summary

```text
✓ Terraform files written    : terraform/ (6 files)
✓ Workflow written           : .github/workflows/gcp-bootstrap.yml
✓ Workflow triggered         : gcp-bootstrap.yml
✓ Workflow completed         : success
✓ GitHub Secrets set         : WIF_PROVIDER, WIF_SERVICE_ACCOUNT, GCP_PROJECT_ID
✓ CLAUDE.md updated
✓ JOURNEY.md updated

Secret Manager secrets created (values are EMPTY — fill via GCP Console):
  <list or "none">
```

## Safety rules

1. **NEVER write `billing_account` to any file** — it flows only via `TF_VAR_BILLING_ACCOUNT` org secret.
2. **NEVER run `terraform` or `gcloud` directly** — the GitHub Actions runner does this.
3. **NEVER create secret versions with production values** — create the secret resource (name) only. The optional autonomy test (Step 5) may write a timestamped test value to `TEST_SECRET`; that is the only permitted exception.
4. **NEVER overwrite an existing `terraform/` directory** without warning the user first.
5. **NEVER pass secret values via CLI args** — use env vars and stdin only.
6. **NEVER print token values** anywhere in output or logs.
7. **If the workflow fails**, print the error and stop — do not retry automatically.

## Examples

**User:** `/gcp-wif-bootstrap` (standard case)

**Agent behaviour:**
Derives `github_repo` from git remote (handles proxy URLs), derives `project_id` from repo name.
Prints summary table, waits for "Proceed?". Writes 6 Terraform files + workflow YAML. Commits,
pushes, triggers `workflow_dispatch`. Polls every 30s. When workflow succeeds: updates
`CLAUDE.md` and `[your-journey-file]`, prints summary.

**User:** `/gcp-wif-bootstrap` (org is NOT bben15600-sys)

**Agent behaviour:**
Prints summary table with ⚠ on all hardcoded org constants. Prints warning:
"These values are hardcoded for or-infra.com — confirm they are correct before proceeding."
Waits for explicit confirmation.

**User:** `/gcp-wif-bootstrap` (no `.env.example`, no `src/`)

**Agent behaviour:**
`secret_names` scan returns zero results. Proceeds with empty secret list.
`terraform/secrets.tf` contains `local.secret_names = []`. CLAUDE.md notes: "No secrets detected."

**User:** `/gcp-wif-bootstrap` (workflow fails)

**Agent behaviour:**
Prints: "FAIL: workflow failed — check GitHub Actions logs at
https://github.com/<github_repo>/actions/workflows/gcp-bootstrap.yml"
Stops. Does not update CLAUDE.md or [your-journey-file] (no successful bootstrap to document).
