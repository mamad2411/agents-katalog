---
name: github-actions-oidc-aws
description: >
  GitHub Actions OIDC to AWS IAM Roles Anywhere/web identity: configure IAM IdP
  for token.actions.githubusercontent.com, trust policies with sub/claims, role
  assumption in workflows, and keyless deploys. Use for owned AWS accounts —
  not to access third-party accounts. Pair with GCP WIF skill for multi-cloud.
---

# GitHub Actions OIDC → AWS

## Scope And Authorization

- **In scope:** AWS accounts and GitHub repos you administer.
- **Out of scope:** Assuming roles in accounts without permission; widening trust to all repos.
- Over-broad `sub` conditions (`repo:ORG/*`) are a common critical misconfig.
- Prefer one role per environment/repo; delete long-lived AKIA keys after cutover.
- Pair with `github-actions-environment-gates` and `gcp-workload-identity-federation` as needed.

## When To Use

- Deploying from GitHub Actions to AWS without static keys.
- Replacing `AWS_ACCESS_KEY_ID` secrets in workflows.
- Auditing existing OIDC trust policies for claim conditions.
- Multi-env roles (`dev`/`prod`) with environment gates.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| GCP WIF | `gcp-workload-identity-federation` |
| GitLab OIDC | `gitlab-ci-oidc-cloud` |
| GH environment approvals | `github-actions-environment-gates` |
| Attestations | `github-actions-artifact-attestations` |
| Implementation quality | `code-quality-standards` |

## Concepts

| Piece | Role |
| --- | --- |
| OIDC token | JWT from GitHub with `sub`, `repository`, `ref`, `aud` |
| IAM OIDC provider | Trusts `https://token.actions.githubusercontent.com` |
| IAM role trust policy | `sts:AssumeRoleWithWebIdentity` + claim conditions |
| `aws-actions/configure-aws-credentials` | Exchanges token for temp creds |
| `sub` claim | Often `repo:ORG/REPO:ref:refs/heads/main` or environment form |

## Workflow

### 1. Confirm design

1. Record AWS account, role names, repos/branches/environments allowed.
2. Success: workflow on allowed ref assumes role; other repos denied; no static keys.

### 2. Create OIDC provider (once per account)

```bash
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list <CURRENT_THUMBPRINT>
# Thumbprint guidance evolves — follow current AWS/GitHub docs
```

Terraform `aws_iam_openid_connect_provider` preferred for drift control.

### 3. Trust policy (tight)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:ORG/REPO:ref:refs/heads/main"
        }
      }
    }
  ]
}
```

Better for GitHub Environments:

```text
repo:ORG/REPO:environment:production
```

Avoid:

```text
repo:ORG/*:*
```

unless every repo is equally trusted (rare).

### 4. Permission policy on role

Grant least privilege (e.g. `s3:PutObject` on one bucket, `eks:DescribeCluster`, …).
Never attach `AdministratorAccess` for CI “to unblock.”

### 5. Workflow

```yaml
permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::ACCOUNT_ID:role/gha-prod-deploy
          aws-region: us-east-1
      - run: aws sts get-caller-identity
      - run: ./deploy.sh
```

### 6. Verify

| Case | Expect |
| --- | --- |
| `main` / prod environment | Assume succeeds; caller identity = role |
| Feature branch | Denied if not in trust policy |
| Different repo | Denied |
| Missing `id-token: write` | Token fetch fails |

```bash
# After deploy, confirm no residual user keys in repo secrets for that path
```

### 7. Audit existing trusts

```bash
aws iam list-open-id-connect-providers
aws iam get-role --role-name gha-prod-deploy
# Inspect AssumeRolePolicyDocument conditions
```

Checklist:

- [ ] Audience restricted
- [ ] `sub` least privilege
- [ ] Role permissions least privilege
- [ ] Static keys removed
- [ ] CloudTrail on `AssumeRoleWithWebIdentity`

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Trust | Single repo + env | `repo:ORG/*` |
| Role | Deploy-only actions | AdminAccess |
| Secrets | Keyless | AKIA in GitHub secrets forever |
| Envs | Separate roles | One role for dev and prod |
| Perms | `id-token: write` only | `permissions: write-all` |

## Output Checklist

- [ ] Account/repo/role design documented
- [ ] OIDC provider present
- [ ] Trust policy claim conditions reviewed
- [ ] Workflow assumes role successfully
- [ ] Negative tests (wrong ref/repo) fail
- [ ] Static keys retired
- [ ] CloudTrail/monitoring considered
- [ ] Environment gates linked for prod
- [ ] `code-quality-standards` applied to deploy scripts

## Rules

- Authorized AWS accounts only.
- Treat trust policy as critical as root keys.
- Prefer environment subject claims for prod.
- Delete long-lived keys after OIDC works.
- Multi-cloud GCP → use WIF skill, not this one alone.
