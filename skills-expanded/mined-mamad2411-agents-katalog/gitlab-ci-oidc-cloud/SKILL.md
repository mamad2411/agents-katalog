---
name: gitlab-ci-oidc-cloud
description: >
  GitLab CI OIDC / JWT federation to cloud providers (AWS, GCP, Azure): id_tokens
  in .gitlab-ci.yml, audience configuration, cloud trust policies bound to project
  path and ref, and keyless deploys. Use for owned GitLab projects and cloud
  accounts — not third-party access.
---

# GitLab CI OIDC → Cloud

## Scope And Authorization

- **In scope:** GitLab projects you administer and cloud accounts you own.
- **Out of scope:** Broad trust policies enabling any project in a shared GitLab to assume prod roles.
- Bind cloud trust to `project_path`, `ref_protected`, `environment` claims as applicable.
- Remove long-lived cloud keys from GitLab CI variables after cutover.
- Pair with `gitlab-ci-security-basics` and provider-specific IAM skills.

## When To Use

- GitLab pipelines deploying to AWS/GCP/Azure without static keys.
- Migrating from masked CI variables containing AKIA/JSON keys.
- Auditing JWT `aud` and cloud conditions.
- Environment-scoped deploys (`production` protected).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| GitHub Actions OIDC AWS | `github-actions-oidc-aws` |
| GCP WIF deep dive | `gcp-workload-identity-federation` |
| GitLab security baseline | `gitlab-ci-security-basics` |
| Pipeline execution policies | `gitlab-ci-pipeline-execution-policies` |
| Implementation quality | `code-quality-standards` |

## Concepts

| Piece | Meaning |
| --- | --- |
| `id_tokens` | CI JWT minted for job with custom `aud` |
| Claims | `project_path`, `namespace_path`, `ref`, `ref_protected`, `environment`, `user_email`, … |
| Cloud IdP | AWS OIDC provider / GCP WIF / Azure federated credentials |
| Protected refs | Limit prod roles to protected branches/tags |
| CI variables | Prefer OIDC over `AWS_SECRET_ACCESS_KEY` |

Exact claim names can vary by GitLab version — verify in job `jwt` debug carefully (never log full token in shared logs long-term).

## Workflow

### 1. Design trust

| Deploy target | Allowed GitLab | Allowed ref |
| --- | --- | --- |
| AWS prod role | `group/app` | protected `main` or tag |
| GCP SA | same | `environment=production` if used |

Success: only intended project+ref assumes role.

### 2. GitLab job with id_token

```yaml
# .gitlab-ci.yml
deploy_prod:
  stage: deploy
  environment:
    name: production
  id_tokens:
    GITLAB_OIDC_TOKEN:
      aud: https://gitlab.com  # or cloud-specific audience you configure
  rules:
    - if: $CI_COMMIT_BRANCH == "main" && $CI_PROJECT_PATH == "group/app"
  script:
    - echo "Exchange token with cloud CLI/SDK"
```

For AWS, audience often `sts.amazonaws.com` or custom — match IAM OIDC client IDs.
For GCP WIF, follow provider attribute mapping docs for GitLab issuer.

### 3. AWS trust sketch

```json
{
  "Effect": "Allow",
  "Principal": {
    "Federated": "arn:aws:iam::ACCOUNT:oidc-provider/gitlab.com"
  },
  "Action": "sts:AssumeRoleWithWebIdentity",
  "Condition": {
    "StringEquals": {
      "gitlab.com:aud": "https://gitlab.com"
    },
    "StringLike": {
      "gitlab.com:sub": "project_path:group/app:ref_type:branch:ref:main"
    }
  }
}
```

Claim key prefixes depend on how the OIDC provider is configured — validate with a decoded JWT in a secure lab job.

### 4. GCP WIF sketch

1. Create pool + OIDC provider with issuer `https://gitlab.com` (or self-managed URL).
2. Map attributes: `google.subject=assertion.sub`, `attribute.project_path=assertion.project_path`, …
3. Condition: `assertion.project_path=='group/app' && assertion.ref=='refs/heads/main'`.
4. Bind `roles/iam.workloadIdentityUser` on deploy SA to principalSet for that project path.
5. Use credential config + `GOOGLE_APPLICATION_CREDENTIALS` in job after exchange.

See `gcp-workload-identity-federation` for pool mechanics.

### 5. Azure federated credentials

- App registration federated credential with issuer GitLab and subject matching job identity.
- Use Azure login actions/OIDC in pipeline without client secret.

### 6. Verify

| Test | Expect |
| --- | --- |
| main pipeline | Assume OK |
| feature branch | Deny for prod role |
| forked/mirrored path | Deny |
| Static key removed | Deploy still works |

### 7. Harden GitLab side

- Protected branches/tags for production.
- Protected environments with required approvals.
- Disable export of OIDC tokens to untrusted child pipelines without review.
- Least-privilege cloud roles.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Trust | Exact project_path + protected ref | Entire GitLab instance wildcard |
| Tokens | Short-lived OIDC | Long-lived keys in CI variables |
| Envs | Protected production | Any branch deploys prod |
| Logging | Caller identity only | Full JWT in public job log |
| Audience | Explicit match | Accept any `aud` |

## Output Checklist

- [ ] Cloud account + GitLab project mapping documented
- [ ] `id_tokens` configured with correct `aud`
- [ ] Cloud trust conditions least privilege
- [ ] Prod limited to protected refs/environments
- [ ] Positive/negative assume tests done
- [ ] Static cloud keys removed from CI variables
- [ ] Approvals enabled for production environment
- [ ] `code-quality-standards` applied to deploy scripts

## Rules

- Owned GitLab + cloud only.
- Never wildcard-trust all projects for prod.
- Prefer protected environments + OIDC together.
- Do not paste live JWTs into tickets.
- Provider-specific deep dives may require sibling IAM skills.
