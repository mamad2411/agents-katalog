---
name: gcp-workload-identity-federation
description: >
  Configure and review Google Cloud Workload Identity Federation (WIF) so CI and
  external IdPs (GitHub Actions OIDC, GitLab, AWS, Azure AD) obtain short-lived
  tokens for a GCP service account without user-managed SA keys. Covers pools,
  providers, attribute mapping/conditions, principalSet IAM, and key retirement
  on owned or authorized GCP projects.
---

# GCP Workload Identity Federation

## Scope And Authorization

- **In scope:** Owned/authorized GCP projects replacing SA JSON keys with WIF.
- **Out of scope:** Using federation to access projects without permission; forging
  OIDC claims against third parties.
- Misconfigured attribute conditions can allow any repo or any branch to mint tokens —
  treat pool/provider config as security-critical code.
- Prefer non-prod pool first; delete keys only after green deploys.
- Pair with `github-actions-oidc-aws` patterns for dual-cloud CI and `gcp-iam-basics`.

## When To Use

- GitHub Actions / GitLab CI deploying to GCP without JSON keys.
- Federating AWS/Azure workloads to GCP SAs.
- Auditing existing WIF pools for overly broad `attribute_condition`.
- Completing org policy “no SA key creation” migrations.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Baseline IAM / key inventory | `gcp-iam-basics` |
| Org policy disable key creation | `gcp-org-policies` |
| GKE Workload Identity (GSA↔KSA) | GKE WI skills (in-cluster) |
| GitHub OIDC to AWS only | `github-actions-oidc-aws` |
| GitLab OIDC cloud | `gitlab-ci-oidc-cloud` |
| Secret Manager consumption | `gcp-secret-manager-versions` |
| Implementation quality | `code-quality-standards` |

## Concepts

| Term | Meaning |
| --- | --- |
| Workload identity pool | Namespace for external identities |
| Provider | OIDC/SAML IdP config (issuer, audiences, mapping) |
| Attribute mapping | Maps token claims → Google principal attributes |
| Attribute condition | CEL gate on which tokens are accepted |
| principalSet / principal | IAM member forms for federated identities |
| SA impersonation | External identity needs `roles/iam.workloadIdentityUser` on target SA |
| Credential configuration | JSON file for client libraries (`gcloud` ADC) without private keys |

### Trust boundary (critical)

```text
IdP token (e.g. GitHub OIDC)
  → WIF provider validates issuer/signature/audience
  → attribute_condition must pass (repo, ref, environment)
  → STS exchange → federated principal
  → allowed to impersonate specific SA
  → SA performs GCP API calls
```

If `attribute_condition` is missing or only checks `assertion.repository_owner`,
**every repo in the org** may deploy with that SA.

## Workflow

### 2. Inventory keys and existing pools

```bash
# User-managed keys still present?
gcloud iam service-accounts list --project=PROJECT_ID
gcloud iam service-accounts keys list --iam-account=SA_EMAIL --project=PROJECT_ID

# Existing pools
gcloud iam workload-identity-pools list --location=global --project=PROJECT_ID
gcloud iam workload-identity-pools providers list \
  --workload-identity-pool=POOL_ID --location=global --project=PROJECT_ID
```

### 1. Confirm scope

1. Record project, target SA roles, CI system, repos/branches allowed, authorization.
2. Success: deploy works via OIDC; SA keys deleted; condition limited to exact repo + env.

### 3. Create pool and OIDC provider (GitHub example)

```bash
gcloud iam workload-identity-pools create github-pool \
  --project=PROJECT_ID \
  --location=global \
  --display-name="GitHub Actions pool"

gcloud iam workload-identity-pools providers create-oidc github-provider \
  --project=PROJECT_ID \
  --location=global \
  --workload-identity-pool=github-pool \
  --display-name="GitHub provider" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository,attribute.ref=assertion.ref" \
  --attribute-condition="assertion.repository=='ORG/REPO' && assertion.ref=='refs/heads/main'"
```

Tighten further with `environment` claim for GitHub Environments when used.

### 4. Bind external identity to SA

```bash
# Project number needed for principalSet
PROJECT_NUMBER=$(gcloud projects describe PROJECT_ID --format='value(projectNumber)')

gcloud iam service-accounts add-iam-policy-binding SA_EMAIL \
  --project=PROJECT_ID \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/github-pool/attribute.repository/ORG/REPO"
```

Prefer narrow principalSet (repository or `subject`) over entire pool.

### 5. Download credential config (no private key)

```bash
gcloud iam workload-identity-pools create-cred-config \
  projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/github-pool/providers/github-provider \
  --service-account=SA_EMAIL \
  --output-file=gcp-wif.json \
  --google-service-account-impersonation
# Commit only non-secret config if required; contains no private key but still scopes trust
```

### 6. CI configuration (GitHub Actions sketch)

```yaml
permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/providers/github-provider
          service_account: SA_EMAIL
      - uses: google-github-actions/setup-gcloud@v2
      - run: gcloud storage ls gs://BUCKET
```

GitLab: use GitLab OIDC issuer and `gitlab-ci-oidc-cloud` patterns with analogous
attribute conditions (`project_path`, `ref_protected`).

### 7. Verify and retire keys

| Test | Expect |
| --- | --- |
| Workflow on allowed branch | Auth succeeds; API works |
| Workflow on fork / other repo | Auth fails |
| Direct SA key | Removed after soak |
| Audit logs | `GenerateAccessToken` / STS from expected subjects |

```bash
# After successful CI, delete user-managed keys
gcloud iam service-accounts keys delete KEY_ID \
  --iam-account=SA_EMAIL --project=PROJECT_ID
```

Enable org policy to block new keys (`gcp-org-policies`).

### 8. Audit checklist for existing WIF

- [ ] Issuer URI correct and HTTPS
- [ ] Attribute condition present and least privilege
- [ ] principalSet not pool-wide without condition
- [ ] SA roles least privilege (not Editor)
- [ ] No residual JSON keys
- [ ] Environments/branches restricted for prod SA

## Attribute condition examples

```cel
// GitHub: one repo, main only
assertion.repository == "acme/api" && assertion.ref == "refs/heads/main"

// GitHub: environment-based
assertion.repository == "acme/api" && assertion.environment == "production"

// Too broad — avoid
assertion.repository_owner == "acme"
```

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Trust | Repo + ref + environment CEL | Entire org owner claim only |
| SA | Deploy-only predefined roles | Owner SA for all CI |
| Keys | Zero user-managed keys | WIF plus keys “for backup” forever |
| Pools | Separate prod/nonprod providers | One condition-less provider for all |
| Review | Treat provider YAML as code review | Console click without PR |

## Output Checklist

- [ ] Project, SA, CI system, allowed identities recorded
- [ ] Pool + provider created with attribute mapping
- [ ] Attribute condition least-privilege reviewed
- [ ] workloadIdentityUser bound via principalSet
- [ ] CI workflow uses OIDC auth successfully
- [ ] Negative test (wrong repo/branch) fails
- [ ] User-managed keys deleted
- [ ] Org policy / monitoring for key creation considered
- [ ] Runbook for rotating provider / adding repos
- [ ] `code-quality-standards` applied to workflow YAML

## Rules

- Authorized projects only.
- Never ship a provider without a strict attribute condition in production.
- WIF config contains trust policy — review like IAM.
- Prefer short-lived tokens; do not reintroduce long-lived keys.
- Focus on GCP WIF; GHA→AWS and GitLab specifics hand off to sibling skills.
