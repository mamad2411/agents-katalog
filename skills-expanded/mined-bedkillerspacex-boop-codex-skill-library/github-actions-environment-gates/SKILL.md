---
name: github-actions-environment-gates
description: >
  GitHub Environments as deploy gates: protection rules, required reviewers,
  wait timers, deployment branches, environment secrets/variables, and concurrency.
  Use to control promotions on owned repos — not to circumvent org deployment policies.
---

# GitHub Actions Environment Gates

## Scope And Authorization

- **In scope:** Repositories/orgs you administer; configuring deploy approvals.
- **Out of scope:** Bypassing required reviewers on systems you do not own; abusing
  admin rights to skip production gates without change control.
- Environment secrets are sensitive — limit admin access; audit changes.
- Pair with OIDC deploy (`github-actions-oidc-aws`) and `git-workflow-conventions`.

## When To Use

- Requiring human approval before production deploy jobs.
- Separating `dev` / `staging` / `prod` secrets and URLs.
- Restricting which branches can deploy to prod.
- Adding wait timers for bake time after staging.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| OIDC role assumption | `github-actions-oidc-aws` / WIF skills |
| Reusable deploy workflows | `github-actions-reusable-workflows` |
| Attestation verify gates | `github-actions-artifact-attestations` |
| CODEOWNERS for code review | `github-codeowners-enforcement` |
| Implementation quality | `code-quality-standards` |

## Concepts

| Feature | Purpose |
| --- | --- |
| Environment | Named target (`production`) with rules + secrets |
| Required reviewers | Manual approval gate |
| Wait timer | Delay before job proceeds |
| Deployment branches/tags | Only `main` or `v*` may deploy |
| Environment secrets | Scoped credentials not available to other jobs |
| Concurrency | Avoid overlapping prod deploys |
| Protection rules | Combine above |

## Workflow

### 1. Define environments

| Name | Reviewers | Branches | Secrets |
| --- | --- | --- | --- |
| development | none | any | dev cloud role |
| staging | optional | `main` | staging role |
| production | 2 people / team | `main` + tags | prod role |

Create via repo Settings → Environments (or API/Terraform/`gh`).

### 2. Wire jobs to environments

```yaml
jobs:
  deploy-prod:
    needs: [build, test]
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.example.com
    concurrency:
      group: prod-deploy
      cancel-in-progress: false
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        run: ./scripts/deploy.sh
        env:
          # Environment secrets injected automatically by name
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
```

Job remains **pending** until protection rules pass.

### 3. Configure protection rules

1. Required reviewers: assign team, not shared personal accounts only.
2. Wait timer: e.g. 5–30 minutes for prod if desired.
3. Deployment branches: selected branches — `main` only or release tags.
4. Optionally prevent self-review if org supports policy.
5. Document break-glass admin bypass with ticket requirement.

### 4. Secrets and variables split

| Store | Examples |
| --- | --- |
| Environment secrets | Prod API tokens, webhook secrets (prefer OIDC over static) |
| Environment variables | `LOG_LEVEL`, non-secret URLs |
| Repository secrets | Shared non-prod only when necessary |

Prefer OIDC federated roles **scoped per environment** over one static cloud key.

### 5. Promotion pipeline pattern

```yaml
jobs:
  deploy-staging:
    environment: staging
    # ...
  deploy-prod:
    needs: deploy-staging
    environment: production
    # approval happens here
```

Optional: attestation verify step inside prod job before mutate.

### 6. Verify gates

| Test | Expect |
| --- | --- |
| PR branch deploy to prod | Blocked by deployment branch rule |
| Push to main without approval | Job waits / fails if timed out policy |
| Approval by reviewer | Job runs; secrets available |
| Non-prod job | Cannot read prod environment secrets |

### 7. Operate

- Audit log: who approved deployments.
- Rotate environment secrets; prefer keyless.
- Review reviewer list quarterly (ex-employees).
- Alert on admin overrides of protection rules.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Prod access | 2-person rule + branch limit | Auto-deploy prod from any branch |
| Secrets | Per-environment + OIDC | One repo secret used everywhere |
| Concurrency | Single prod group | Parallel prod deploys clobber |
| Reviewers | Team-based | Only one personal account forever |
| Break-glass | Ticketed time-limit | Silent disable protections |

## Output Checklist

- [ ] Environments named and documented
- [ ] Protection rules set for prod
- [ ] Workflows reference `environment:`
- [ ] Secrets scoped correctly (verified isolation)
- [ ] Branch/tag rules tested
- [ ] Concurrency configured
- [ ] Approval audit path known
- [ ] OIDC/roles aligned per env
- [ ] `code-quality-standards` applied to deploy scripts

## Rules

- Do not weaken prod gates without change control.
- Least-privilege secrets per environment.
- Prefer keyless cloud auth.
- Human approval is not a substitute for automated tests/attestations.
- Focus on GitHub Environments; cloud IAM is sibling work.
