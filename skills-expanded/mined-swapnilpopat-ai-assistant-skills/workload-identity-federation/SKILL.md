---
name: workload-identity-federation
description: Design keyless, federated, short-lived credentials for CI/CD jobs and workloads — GitHub Actions OIDC, GitLab JWT, Buildkite, CircleCI, Bitbucket Pipelines, Terraform Cloud, SPIFFE/SPIRE — federated to AWS STS AssumeRoleWithWebIdentity, GCP Workload Identity Federation, Azure Workload Identity, and HashiCorp Vault. Use when eliminating long-lived cloud access keys from CI, hardening trust policies against subject-claim spoofing, or enabling service-to-service identity in multi-cloud / Kubernetes environments.
allowed-tools: Read, Grep, Glob, Write, Edit
---

# Workload Identity Federation

Eliminate every long-lived cloud access key, service-account key, and PAT from CI/CD systems and workloads — replace them with short-lived, identity-bound, audience-pinned, claim-restricted OIDC-federated credentials so a leaked secret is no longer a breach.

## Context

You are a senior cloud-security engineer hardening $ARGUMENTS. Long-lived credentials (`AWS_SECRET_ACCESS_KEY`, GCP service-account JSON, Azure app-registration secrets, ssh deploy keys, npm/PyPI tokens) are the most common root cause of cloud breaches reported in DBIR / Mandiant / Wiz incident reports. They live in CI variables, `.env` files, hard-coded constants, S3 buckets, and abandoned forks. The fix is structural: stop issuing long-lived credentials at all. Modern CI systems mint a signed, ephemeral OIDC token for every job; cloud providers and Vault accept that token and exchange it for a short-lived (15-min – 1-hr) credential bound to the job's identity. Combined with **strict trust-policy claim conditions**, the resulting credential cannot be replayed, cannot be exfiltrated to use elsewhere, and cannot be granted scope beyond what the specific job legitimately needs.

## Domain Context

- **OIDC (OpenID Connect)**: an OAuth2 extension that issues a signed JWT (`id_token`) describing the bearer's identity (`iss`, `sub`, `aud`, plus issuer-specific claims). Verifiable via the issuer's published JWKS endpoint.
- **Workload Identity Federation**: a cloud trust policy that says "I trust JWTs from issuer X, with audience Y, and subject matching pattern Z, and will exchange them for short-lived cloud credentials with role R."
- **Confused-deputy / claim-spoofing risk**: the most common misconfiguration is a trust policy that pins only `iss` and `aud` but not `sub` — any GitHub repo / GitLab project / Azure DevOps org sharing the issuer can mint a token with an arbitrary `sub` and assume your role. Pin **multiple claims**, especially the repository / project / branch / environment.
- **SPIFFE/SPIRE**: workload-identity standard for service-to-service inside a cluster or across heterogeneous platforms. Issues SVIDs (X.509 or JWT) bound to selectors (Kubernetes namespace+SA, Unix UID, AWS instance role, etc.).
- **AWS STS AssumeRoleWithWebIdentity**: exchanges OIDC token → temporary AWS creds (1 hr default, max 12 hr). Trust policy uses `Condition: StringEquals/StringLike` on `iss:sub` / `iss:aud`.
- **GCP Workload Identity Federation**: a Workload Identity Pool + Provider maps OIDC tokens to a service-account impersonation; tokens last ≤ 1 hr.
- **Azure Workload Identity / Federated Credentials**: app registration declares federated identity credentials referencing OIDC issuer + subject; STS-equivalent grants tokens for Microsoft Graph / Azure ARM.
- **HashiCorp Vault JWT/OIDC auth**: same pattern, applied to any secret Vault manages.
- **Common OIDC issuers (2026)**:
  - GitHub Actions — `https://token.actions.githubusercontent.com`
  - GitLab CI — `https://gitlab.com` (or self-hosted)
  - Buildkite — `https://agent.buildkite.com`
  - CircleCI — `https://oidc.circleci.com/org/<org-id>`
  - Bitbucket Pipelines — `https://api.bitbucket.org/2.0/workspaces/<ws>/pipelines-config/identity/oidc`
  - Terraform Cloud / HCP — `https://app.terraform.io`
  - JFrog, Spacelift, env0, Atlantis, Render, Vercel, Cloudflare Workers — all expose OIDC in 2026

## Stack Baseline (2026)

| Need | Recommended |
| --- | --- |
| CI → AWS | GitHub `aws-actions/configure-aws-credentials@v4` with `role-to-assume`; GitLab `id_tokens:` with `aws-cli sts assume-role-with-web-identity` |
| CI → GCP | `google-github-actions/auth@v2` with `workload_identity_provider` |
| CI → Azure | `azure/login@v2` with `client-id`/`tenant-id`/`subscription-id`, no client secret |
| CI → Vault | `hashicorp/vault-action@v3` with `method: jwt` |
| K8s → AWS | IAM Roles for Service Accounts (IRSA) or **EKS Pod Identity** (preferred 2026) |
| K8s → GCP | GKE Workload Identity (KSA → GSA) |
| K8s → Azure | Microsoft Entra Workload ID for Kubernetes |
| Cross-cluster / multi-cloud workload | SPIFFE/SPIRE 1.10+ with JWT-SVIDs + cloud federation |
| Service mesh identity | Istio + SPIFFE, Linkerd identity, Cilium ServiceMesh + SPIRE |

## When to Use This Skill

- Standing up a new CI/CD pipeline that needs cloud access
- Auditing existing CI for long-lived `AWS_*`, `GCP_*`, `AZURE_*` secrets and replacing them
- Designing service-to-service auth in Kubernetes or across clouds
- Responding to a leaked-credential incident (rotate first, then move to OIDC so it can't recur)
- Reviewing a third-party trust-policy contribution / pull-request before merge
- Writing org-wide Terraform / CrossPlane / Pulumi modules for federated identity

## Prerequisites

1. **Inventory** of every long-lived credential in CI variables, secret managers, repo secrets, Helm values, `.env` files, and OS keychains
2. **OIDC support confirmed** in the CI / runtime issuing the token (every major CI in 2026 supports it)
3. **Cloud admin access** to create IAM roles / Workload Identity Pools / Federated Credentials
4. **Naming convention** for roles: encode environment + repo + workflow in the role name (e.g., `gha-acme-payments-deploy-prod`)
5. **Branch / environment protection** in the source CI — the OIDC token's value is only as good as the gating around who can run a workflow at that path/ref/environment

## Instructions

### 1. Pin every claim that gives you defense-in-depth

A trust policy that matches only `iss` + `aud` is **broken** the moment another tenant of the same issuer points a workflow at it. Always pin the most specific subject pattern your CI exposes.

GitHub Actions `sub` claim format:

```
repo:<org>/<repo>:environment:<env>            ← prefer this (env-protected)
repo:<org>/<repo>:ref:refs/heads/<branch>
repo:<org>/<repo>:ref:refs/tags/<tag-pattern>
repo:<org>/<repo>:pull_request                 ← high-risk; rarely allow
```

GitLab CI `sub` format:

```
project_path:<group>/<project>:ref_type:branch:ref:<branch>
project_path:<group>/<project>:ref_type:tag:ref:<tag>
project_path:<group>/<project>:environment:<env>
```

### 2. AWS — STS AssumeRoleWithWebIdentity

OIDC provider (one per issuer per account):

```hcl
resource "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com"]
  thumbprint_list = ["ffffffffffffffffffffffffffffffffffffffff"] # AWS now ignores; safe default
}
```

(Note: since 2023 AWS validates GitHub's certificate via the trust store and the thumbprint check is no longer enforced, but the field is still required.)

Strict role trust policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com" },
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": {
        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
        "token.actions.githubusercontent.com:sub": "repo:acme/payments:environment:production"
      }
    }
  }]
}
```

`StringLike` is acceptable for tag/branch glob patterns:

```json
"StringLike": {
  "token.actions.githubusercontent.com:sub": "repo:acme/payments:ref:refs/tags/v*"
}
```

Workflow:

```yaml
permissions:
  id-token: write   # required to mint the OIDC token
  contents: read
jobs:
  deploy:
    environment: production    # enforces approval + restricts sub claim
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@a5ac7e51b41094c92402da3b24376905380afc29  # v4.1.1
      - uses: aws-actions/configure-aws-credentials@e3dd6a429d7300a6a4c196c26e071d42e0343502  # v4.0.2
        with:
          role-to-assume: arn:aws:iam::123456789012:role/gha-acme-payments-deploy-prod
          aws-region: eu-west-1
          role-session-name: gha-${{ github.run_id }}
          role-duration-seconds: 1800
      - run: aws s3 sync ./build s3://acme-payments-prod/
```

### 3. GCP — Workload Identity Federation

```hcl
resource "google_iam_workload_identity_pool" "gha" {
  workload_identity_pool_id = "github"
  display_name              = "GitHub Actions"
}

resource "google_iam_workload_identity_pool_provider" "gha" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.gha.workload_identity_pool_id
  workload_identity_pool_provider_id = "github"
  oidc { issuer_uri = "https://token.actions.githubusercontent.com" }
  attribute_mapping = {
    "google.subject"             = "assertion.sub"
    "attribute.repository"       = "assertion.repository"
    "attribute.repository_owner" = "assertion.repository_owner"
    "attribute.environment"      = "assertion.environment"
  }
  attribute_condition = "assertion.repository_owner == 'acme' && assertion.environment == 'production'"
}

resource "google_service_account_iam_binding" "impersonate" {
  service_account_id = google_service_account.deploy.name
  role               = "roles/iam.workloadIdentityUser"
  members = [
    "principalSet://iam.googleapis.com/projects/${var.project_number}/locations/global/workloadIdentityPools/github/attribute.repository/acme/payments"
  ]
}
```

Workflow:

```yaml
permissions:
  id-token: write
  contents: read
jobs:
  deploy:
    environment: production
    steps:
      - uses: actions/checkout@a5ac7e51b41094c92402da3b24376905380afc29  # v4.1.1
      - uses: google-github-actions/auth@b7593ed2efd1c1617e1b0254da33b86225adb2a5  # v2.1.5
        with:
          workload_identity_provider: projects/123456/locations/global/workloadIdentityPools/github/providers/github
          service_account: deploy@acme-prod.iam.gserviceaccount.com
      - run: gcloud run deploy payments --image=...
```

Note: GCP requires either an `attribute_condition` **or** principalSet binding pinned to specific attributes (repo + environment). Bare `principalSet://.../*` over a pool with multiple repos is a confused-deputy bug.

### 4. Azure — Federated Identity Credentials

```bash
az ad app federated-credential create --id "$APP_ID" --parameters '{
  "name": "gha-acme-payments-prod",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "repo:acme/payments:environment:production",
  "audiences": ["api://AzureADTokenExchange"]
}'
```

Workflow:

```yaml
permissions: { id-token: write, contents: read }
jobs:
  deploy:
    environment: production
    steps:
      - uses: actions/checkout@a5ac7e51b41094c92402da3b24376905380afc29
      - uses: azure/login@a457da9ea143d694b1b9c7c869ebb04ebe844ef5  # v2.1.0
        with:
          client-id:       ${{ vars.AZURE_CLIENT_ID }}
          tenant-id:       ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
      - run: az webapp deploy ...
```

### 5. Kubernetes workload identity

- **AWS**: prefer **EKS Pod Identity** (2024+) over IRSA — simpler, no IAM OIDC provider per cluster, role-attachment is a single API call
- **GCP**: GKE Workload Identity binds `KSA` → `GSA` via annotation `iam.gke.io/gcp-service-account=...`
- **Azure**: AKS Workload ID — namespace label + service-account annotation + federated credential on the app registration; OIDC token mounted by the projected volume
- **Cross-cloud / on-prem**: SPIFFE/SPIRE issues JWT-SVIDs that AWS/GCP/Azure can federate with — same trust policy pattern, SPIRE issuer instead of GitHub

### 6. Service-to-service: SPIFFE/SPIRE

For workloads inside one or more clusters that need a portable identity not tied to a specific cloud:

- Deploy SPIRE server (one per trust domain) + agent on every node
- Identify workloads by selector (`k8s:ns:payments,k8s:sa:checkout`, `unix:uid:1001`, `aws:iid:i-0123`)
- Issue JWT-SVID with audience `aws-sts` or `gcp-token` and federate with the cloud's workload identity pool
- Service mesh (Istio, Linkerd, Cilium) consumes the X.509-SVID for mTLS

### 7. Detect long-lived credentials still in use

- Search source: `AKIA[0-9A-Z]{16}` (AWS access key id pattern), `"type": "service_account"` (GCP JSON keys), Azure client secret patterns
- Cloud-side: AWS IAM credential report (rotate / disable any user-key > 90 days), GCP `disable-service-account-key-creation` org policy, Azure secret expiration policy
- CI-side: list repo / org secrets and tag every static cloud secret as a remediation item

### 8. Token-replay and abuse defenses

Even short-lived tokens can be replayed if exfiltrated mid-job. Reduce blast radius:

- Use **environment protections** (required reviewers, deployment branches) — only protected environments can mint tokens to assume sensitive roles
- Set the shortest viable `role-duration-seconds` (often 15 min is enough for the actions that follow)
- Pin `role-session-name` to include the run id so CloudTrail / audit logs are job-attributable
- Enable AWS CloudTrail / GCP Audit Logs / Azure Sign-in Logs for every federated assume — alert on subject claims you didn't expect
- For very-high-blast-radius roles (account-admin, prod-deploy), require **manual approval** + **signed commits** + **branch protection** + the trust-policy pin in concert

## Common Pitfalls

| Pitfall | Why it fails | Fix |
| --- | --- | --- |
| Trust policy pins only `aud`, not `sub` | Any other repo / project on the same issuer can assume the role | Pin `sub` to specific repo + branch / environment / tag pattern |
| `StringLike` on `sub` with `*` at end | Matches forks / PRs from anyone | Anchor patterns end-to-end; whitelist refs explicitly |
| Allow `pull_request` event to mint OIDC tokens with deploy roles | Forks of public repos can run workflows | Restrict via environment protections; never let PRs from forks reach prod roles |
| Leaving the OIDC provider thumbprint stale | Rare for GitHub (AWS validates via trust store) but matters for self-hosted issuers | Document rotation; for self-hosted, automate `aws iam update-open-id-connect-provider-thumbprint` |
| Granting the federated role overly broad IAM | Compromise of the workflow ⇒ broad cloud access | Per-workflow least-privilege role; one role ≠ one repo, ideally one role per (repo, environment) |
| Not enforcing GitHub Environments / GitLab Environments | The protection layer (reviewers, branch limits) is what makes the `sub` claim meaningful | Use Environments + protection rules + branch-allow-list |
| OIDC enabled but `permissions: id-token: write` missing or default-allowed everywhere | Either token is not minted, or every job mints one (extra blast radius) | Set at job level only where needed; keep workflow-level `permissions: read-all` |
| GCP attribute_condition omitted | Pool maps any GitHub identity to your SA | Always include both `attribute_condition` and tightly-scoped `principalSet` |

## Output Format

Produce a **Workload Identity Federation Plan**:

```markdown
# Workload Identity Federation Plan: <org / system>

## 1. Long-lived credential inventory
| Secret | Location | Owner | Replacement plan | Removal date |

## 2. Trust topology
- CI / runtime issuers in scope
- Cloud accounts / GCP projects / Azure tenants in scope
- Pool / provider naming convention

## 3. Trust policies (per role / SA)
| Role / SA | Issuer | sub pattern | aud | Extra conditions | Owner |

## 4. Workflow / pod changes
- Per-repo PR list

## 5. Detection & monitoring
- CloudTrail / Audit Log alerts on unexpected `sub` claims
- Periodic cred-report scan for resurrection of long-lived keys

## 6. Rollback plan
- Per-cutover rollback steps
```

## Worked Example

**Subject**: 47 GitHub repos in `acme-org`, deploying to AWS (12 accounts), GCP (3 projects), Azure (1 tenant). Today: 71 long-lived `AWS_ACCESS_KEY_ID` repo secrets + 14 GCP service-account JSONs + 8 Azure client secrets.

Plan:

1. Provision `aws_iam_openid_connect_provider` per AWS account (Terraform module rolled out via `org-foundations` repo)
2. Roles named `gha-<repo>-<env>`; trust policy template enforces `sub: repo:acme-org/<repo>:environment:<env>`; default `role-duration-seconds: 1800`
3. GitHub Environments created per repo: `staging` (no reviewers, branch allow-list `main`), `production` (2 reviewers, tag pattern `v*`)
4. Replace per-repo `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` with `aws-actions/configure-aws-credentials@v4` referring to the role
5. GCP Workload Identity Pool `github` per project; one provider per CI; `principalSet` keyed by `attribute.repository` + `attribute.environment`
6. Azure: federated credentials added to existing app registrations; client secrets removed after 1-week overlap
7. After all 71 repos cut over: AWS IAM credential report shows zero `gha-*` user keys; rotate / delete the legacy IAM users

Outcome: 93 long-lived secrets eliminated; zero credential-leak incidents in following 12 months; CloudTrail alert successfully fired on a misconfigured fork attempting to assume a prod role (attempt failed at trust-policy evaluation).

## Decision Framework

- **OIDC vs. signed assertions vs. mTLS for service-to-service?** OIDC is the default 2026 pattern across CIs and clouds. SPIFFE for portable workload identity. mTLS for in-mesh service auth (and SPIRE issues the cert).
- **One role per repo or per (repo, env)?** Per (repo, env) — you almost never want a single role usable from both staging and production.
- **EKS Pod Identity vs. IRSA?** Pod Identity for new clusters (simpler, no per-cluster OIDC provider). IRSA still fine for existing.
- **Should we still keep one break-glass static key?** Yes, in a sealed envelope: an account-root with MFA + a single break-glass IAM user, both monitored — for the day federated identity is broken. Store offline.
- **GitHub `sub` pinned to branch or environment?** Environment is preferable — it composes with required reviewers and protection rules. Branch-only pinning misses the human-approval gate.
- **`StringLike` is acceptable when?** Tag patterns (`refs/tags/v*`) and only when the protection layer (env reviewers, branch protection on tag creation) prevents arbitrary tag pushes.

## Authoritative References

- GitHub Actions OIDC: https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect
- AWS — Configuring a role for GitHub OIDC: https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services
- GCP Workload Identity Federation: https://cloud.google.com/iam/docs/workload-identity-federation
- Azure Workload Identity Federation: https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation
- HashiCorp Vault JWT/OIDC auth: https://developer.hashicorp.com/vault/docs/auth/jwt
- SPIFFE / SPIRE: https://spiffe.io/docs/
- EKS Pod Identity: https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html
- GitLab CI OIDC ID tokens: https://docs.gitlab.com/ee/ci/cloud_services/
- CircleCI OIDC: https://circleci.com/docs/openid-connect-tokens/
- Buildkite OIDC: https://buildkite.com/docs/agent/v3/cli-oidc
- Terraform Cloud OIDC dynamic credentials: https://developer.hashicorp.com/terraform/cloud-docs/workspaces/dynamic-provider-credentials
- AWS IAM Roles for Service Accounts (IRSA): https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html
- GitHub OIDC `sub` claim format: https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect#example-subject-claims
