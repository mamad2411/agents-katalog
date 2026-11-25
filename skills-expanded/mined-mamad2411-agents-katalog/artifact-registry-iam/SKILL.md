---
name: artifact-registry-iam
description: >
  Authorized assessment and hardening of Google Cloud Artifact Registry IAM: repository-
  vs project-level bindings, reader/writer/repoAdmin least privilege, public allUsers
  exposure, CI push identities, and cross-project consumers. Use when reviewing org-owned
  Artifact Registry repos, package/container pull and push roles, Terraform
  google_artifact_registry_*_iam_*, or accidental public packages — not unauthorized
  enumeration of third-party registries.
---

# Artifact Registry IAM

## Scope And Authorization

- **In scope:** GCP projects and Artifact Registry repositories you own or assess with written authorization.
- **Out of scope:** Enumerating or pulling private third-party registries without permission.
- Public (`allUsers` / `allAuthenticatedUsers`) readers can expose proprietary packages — treat as release decisions.
- Redact SA keys and temporary tokens; prefer workload identity over downloaded keys.
- Pair Terraform IAM with `code-quality-standards` and `secrets-management-hygiene`.

## When To Use

- Reviewing who can download (`reader`) vs upload (`writer`) vs admin repos.
- Finding accidental public Docker/npm/python/maven repositories.
- Granting CI/CD push and runtime pull (GKE/Cloud Run) with least privilege.
- Cross-project artifact sharing via IAM (not by making repos public).
- Cleaning project-level broad bindings that apply to every repository.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| AWS ECR IAM | ECR-specific skill if present |
| Generic GCP org IAM strategy | broader GCP IAM skill |
| Container image CVE scanning | image scanning skill |
| Supply chain SLSA broadly | supply-chain skill |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Role (common) | Capabilities (summary) |
| --- | --- |
| `roles/artifactregistry.reader` | pull/download artifacts; list |
| `roles/artifactregistry.writer` | push + reader |
| `roles/artifactregistry.repoAdmin` | manage repo IAM + content |
| `roles/artifactregistry.admin` | create/delete repositories (broader) |
| `roles/artifactregistry.createOnPushWriter` | create repo on push patterns (use carefully) |

| Scope | Use |
| --- | --- |
| Repository IAM | Preferred least privilege per repo |
| Project IAM | Convenience but wide blast radius |
| Public principals | `allUsers`, `allAuthenticatedUsers` — explicit product decision |

## Workflow

### 1. Confirm scope and success criteria

1. Record org/folder/project IDs, locations, repository names/formats, owners.
2. Success: no unintended public principals; CI SA can push only needed repos; runtime SAs pull-only; admins enumerated.
3. Note break-glass project admins separately from registry roles.

### 2. Inventory repositories and IAM

```bash
gcloud config get-value project
gcloud artifacts repositories list --location=us
# Per repository policy
REPO=app-images
LOC=us
gcloud artifacts repositories get-iam-policy "$REPO" --location="$LOC"
# Project-level bindings that include artifactregistry roles
gcloud projects get-iam-policy "$(gcloud config get-value project)" \
  --flatten="bindings[].members" \
  --filter="bindings.role:artifactregistry" \
  --format="table(bindings.role, bindings.members)"
```

1. Flag `allUsers` / `allAuthenticatedUsers` on any repo.
2. List human users with `repoAdmin` / `admin`.
3. Identify CI SAs (`@cloudbuild`, GitHub WIF SAs) and runtime GKE node/workload SAs.

### 3. Baseline

1. Export IAM policies JSON for each production repo.
2. Capture recent push accounts from Cloud Audit Logs (if enabled).
3. Document intended consumers (projects, GKE clusters, Cloud Run services).

### 4. Apply least-privilege bindings

**Pull-only for runtime SA:**

```bash
gcloud artifacts repositories add-iam-policy-binding "$REPO" \
  --location="$LOC" \
  --member="serviceAccount:runtime@PROJECT.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.reader"
```

**Push for CI SA (not admin):**

```bash
gcloud artifacts repositories add-iam-policy-binding "$REPO" \
  --location="$LOC" \
  --member="serviceAccount:ci-push@PROJECT.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"
```

**Remove public access:**

```bash
gcloud artifacts repositories remove-iam-policy-binding "$REPO" \
  --location="$LOC" \
  --member="allUsers" \
  --role="roles/artifactregistry.reader"
```

**Terraform sketch:**

```hcl
resource "google_artifact_registry_repository_iam_member" "ci_writer" {
  project    = var.project_id
  location   = var.location
  repository = google_artifact_registry_repository.app.repository_id
  role       = "roles/artifactregistry.writer"
  member     = "serviceAccount:${var.ci_sa_email}"
}
```

1. Prefer repository-level IAM over project-level `roles/artifactregistry.writer`.
2. Use Workload Identity Federation for GitHub/GitLab — avoid long-lived JSON keys.
3. Separate prod and non-prod repositories; do not share writer across env if avoidable.
4. For cross-project pull: grant reader on repo to the other project’s runtime SA (or use VPC-SC as org requires).

### 5. Verify with evidence

```bash
gcloud artifacts repositories get-iam-policy "$REPO" --location="$LOC"
# As CI SA (impersonation example)
gcloud artifacts docker images list "${LOC}-docker.pkg.dev/PROJECT/${REPO}" \
  --impersonate-service-account=ci-push@PROJECT.iam.gserviceaccount.com
# Expect deny for reader SA on push (use a docker push test in CI sandbox)
```

1. Confirm public principals gone (unless approved public packages with ticket).
2. Audit log: unauthorized `PermissionDenied` on push attempts from wrong SA.
3. Attach before/after policy JSON (redact if needed) to change ticket.

### 6. Observe and harden

1. Cloud Asset Inventory / Policy Analyzer for `allUsers` on Artifact Registry.
2. Alerts when IAM policy changes on prod repos.
3. Periodic review of `repoAdmin` and project-level artifact roles.
4. Enable vulnerability scanning features as org standard (separate from IAM but related).

### 7. Hand off

1. Document repo catalog, formats, and intended IAM matrix.
2. CODEOWNERS for Terraform IAM; require security review on public bindings.
3. Onboarding snippet for new CI SA grants.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Scope | per-repo reader/writer | project-wide writer for all humans |
| Public | none unless productized | `allUsers` “for testing” left on |
| CI | WIF + writer on one repo | JSON key with admin role |
| Runtime | reader only | writer on node SA |
| Humans | group + limited admin | personal owner on every repo |
| Verify | get-iam-policy + deny tests | “we use private Google access” alone |

## Output Checklist

- [ ] Projects, locations, repos, authorization recorded
- [ ] IAM inventory includes public principals check
- [ ] Repository-level least privilege applied
- [ ] CI push and runtime pull identities separated
- [ ] Cross-project consumers documented
- [ ] Public access removed or ticketed
- [ ] Verification evidence attached
- [ ] Monitoring for policy changes considered
- [ ] Terraform/IaC updated; `code-quality-standards` applied

## Rules

- Authorized GCP resources only.
- Treat public artifact repos as intentional product releases with owners.
- Prefer WIF over SA user keys.
- Do not grant `repoAdmin` for routine push.
- Focus on Artifact Registry IAM; route image CVE scanning and org-wide IAM elsewhere.
