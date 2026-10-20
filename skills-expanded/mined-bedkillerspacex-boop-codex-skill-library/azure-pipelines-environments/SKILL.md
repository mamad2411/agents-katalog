---
name: azure-pipelines-environments
description: >
  Azure DevOps Pipelines Environments for owned projects: environment resources,
  checks (approvals, branch control, business hours), service connections isolation,
  YAML deployment jobs, and least-privilege service principals. Use when locking down
  prod deployments or configuring multi-stage pipelines — not for attacking ADO orgs
  without authorization.
---

# Azure Pipelines Environments

## Scope And Authorization

- **In scope:** Azure DevOps organizations/projects you administer; target Azure subscriptions for deploy.
- **Out of scope:** Changing checks to bypass change control; deploying to subscriptions without authority.
- Weak environment checks enable silent prod deploys — treat as production security control.
- Pair federated Azure login with `azure-managed-identity-federated`; use `code-quality-standards` for YAML.

## When To Use

- Creating `dev`/`test`/`prod` Environments with approval gates.
- Binding Kubernetes/VM resources to Environments for deployment history.
- Restricting which branches can deploy to prod.
- Separating Azure service connections per environment.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Entra PIM for humans | `azure-pim-eligible-roles` |
| OIDC federation to Azure | `azure-managed-identity-federated` |
| Bamboo Specs security | `bamboo-specs-security` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Detail |
| --- | --- |
| Environment | Named deployment target grouping with checks |
| Checks | Approvals, invoke REST, branch control, required template, etc. |
| Deployment job | YAML `deployment:` with `environment:` |
| Service connection | Auth to Azure/K8s — scope per env |
| Permissions | Who can administer environment vs deploy |
| Tooling | Azure DevOps UI, REST API, YAML pipelines |

## Workflow

### 1. Confirm scope and success criteria

1. ADO project, repos, stages, Azure targets, approvers, authorization.
2. Success: prod deploy blocked without approval and from non-main branches; audit shows who approved.
3. Emergency hotfix path documented (still audited).

### 2. Inventory environments and connections

```bash
# Azure CLI won't cover ADO fully — use az devops if extension installed
az devops configure --defaults organization=https://dev.azure.com/ORG project=PROJ
az pipelines environment list -o table 2>/dev/null || true
az devops service-endpoint list -o table
```

1. List Environments, checks, and pipeline permissions.
2. Inventory service connections and their Azure RBAC.
3. Find classic releases vs YAML multi-stage.

### 3. Baseline risk

1. Prod connection usable from PR pipelines?
2. Approvals optional or single self-approve?
3. Same SP for dev and prod with Owner?

### 4. Configure Environments and YAML

**YAML sketch:**

```yaml
stages:
- stage: Build
  jobs:
  - job: build
    steps:
    - task: ...

- stage: DeployProd
  dependsOn: Build
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
  jobs:
  - deployment: deploy
    environment: prod
    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureCLI@2
            inputs:
              azureSubscription: sc-azure-prod
              ...
```

1. Create Environment `prod` with **Approvals and checks**: required approvers (group), timeout, branch control `refs/heads/main`.
2. Deny contribute on environment to broad project contributors; limit “User” deploy permission.
3. Separate service connections: `sc-azure-dev`, `sc-azure-prod` with RG-scoped RBAC.
4. Prefer OIDC Azure service connections over stored secrets.
5. Optional: required YAML template check for security baseline tasks.

### 5. Verify with evidence

1. Pipeline from feature branch cannot deploy to `prod` environment.
2. Main branch deploy waits for approval; unauthorized user cannot approve.
3. Dev connection cannot touch prod RG.
4. Deployment history on Environment shows run IDs.

### 6. Observe and harden

1. Audit stream for check modifications and service connection changes.
2. Periodic review of approver groups (no nested everyone).
3. Block self-approval if org policy requires separation of duties.

### 7. Hand off

1. Environment matrix: name, checks, connection, Azure scope, owners.
2. Hotfix runbook still through Environment checks.
3. Pipeline template library for standard deploy jobs.

## Checks Catalog

| Check | Use for |
| --- | --- |
| Approvals | Human gate for prod |
| Branch control | Only release branches |
| Business hours | Optional change windows |
| Invoke Azure Function/REST | Change ticket validation |
| Required template | Enforce org steps |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Connections | Per-env least privilege | One Owner SP everywhere |
| Approvals | Group of platform owners | Single dev self-approves prod |
| Branches | Main/release only to prod | Any branch deploy prod |
| Auth | OIDC federation | PAT with full access in variable |
| Audit | Environment deployment history | FTP from laptop to prod |

## Output Checklist

- [ ] Environments created per stage
- [ ] Checks configured and tested
- [ ] Service connections split and scoped
- [ ] YAML deployment jobs reference environments
- [ ] Negative tests (wrong branch/user) evidenced
- [ ] Approver groups reviewed
- [ ] Audit/monitoring for config changes
- [ ] Hotfix path documented
- [ ] `code-quality-standards` applied to pipelines

## Rules

- Authorized ADO and cloud scopes only.
- Prod deploys always gated and audited.
- Never share prod credentials with sandbox pipelines.
- Prefer OIDC over long-lived secrets.
- Separation of duties for approvals where required.
