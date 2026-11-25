---
name: azure-managed-identity-federated
description: >
  Federated identity credentials for owned Entra ID apps and user-assigned managed
  identities: GitHub Actions OIDC, Kubernetes issuer subjects, other OIDC providers,
  eliminating client secrets for CI/CD and workloads. Use when configuring
  federated credentials or fixing token exchange failures — not for forging issuers
  or accessing tenants without authorization.
---

# Azure Federated Identity Credentials

## Scope And Authorization

- **In scope:** App registrations and user-assigned managed identities in tenants you administer; CI/CD orgs you control.
- **Out of scope:** Adding federated trust to apps you do not own; broad federation from untrusted issuers.
- A mis-scoped subject (`repo:*`) can allow any repo to mint cloud admin tokens — treat as high risk.
- Pair AKS-specific wiring with `azure-aks-workload-identity`; MI basics with `azure-managed-identity-basics`.

## When To Use

- GitHub Actions / Azure DevOps OIDC to deploy without secrets.
- Federating external OIDC IdPs to an Entra application.
- User-assigned MI federated credentials for K8s or other issuers.
- Replacing expiring client secrets on automation apps.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| AKS pod labels / OIDC issuer enablement | `azure-aks-workload-identity` |
| General MI on App Service/VM | `azure-managed-identity-basics` |
| PIM eligible human roles | `azure-pim-eligible-roles` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Piece | Role |
| --- | --- |
| Issuer | OIDC provider URL (GitHub, AKS, etc.) |
| Subject | Specific identity (repo+env, SA, etc.) |
| Audience | Usually `api://AzureADTokenExchange` |
| Trust | Federated credential on app or UAMI |
| Exchange | External token → Entra access token |
| Tooling | `az ad app federated-credential`, `az identity federated-credential`, GitHub `azure/login` |

## Workflow

### 1. Confirm scope and success criteria

1. Target app/MI, issuer, exact subject, Azure roles needed, authorization.
2. Success: pipeline/workload obtains Entra token; wrong subject denied; no client secret stored.
3. Break-glass SP secret only if required and vaulted with expiry.

### 2. Inventory existing credentials

```bash
az ad app list --display-name "$APP_NAME" --query "[].{appId:appId,id:id}" -o table
APP_OBJ=$(az ad app show --id "$APP_ID" --query id -o tsv)
az ad app federated-credential list --id "$APP_OBJ" -o jsonc
az identity federated-credential list --identity-name "$UAMI" -g "$RG" -o jsonc
az ad app credential list --id "$APP_ID" -o table  # plan to remove secrets
```

1. Flag federated credentials with overly broad subjects.
2. List role assignments on the SP / MI.
3. Note GitHub environment protection rules.

### 3. Baseline least privilege

1. Map jobs to minimum Azure RBAC (e.g. scoped deploy to one RG).
2. Prefer **environment-scoped** GitHub subjects over branch-only when secrets deploy to prod.
3. Separate apps for prod vs nonprod CI.

### 4. Create federated credentials

**GitHub Actions → Entra app (illustrative subject formats):**

```bash
az ad app federated-credential create --id "$APP_OBJ" --parameters '{
  "name": "gh-prod-deploy",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "repo:myorg/myrepo:environment:production",
  "audiences": ["api://AzureADTokenExchange"],
  "description": "GitHub env production"
}'
```

**User-assigned MI (e.g. K8s):**

```bash
az identity federated-credential create \
  --name "fc-api-sa" \
  --identity-name "$UAMI" \
  --resource-group "$RG" \
  --issuer "$AKS_OIDC_ISSUER" \
  --subject "system:serviceaccount:app:api-sa" \
  --audiences "api://AzureADTokenExchange"
```

**GitHub workflow sketch:**

```yaml
permissions:
  id-token: write
  contents: read
jobs:
  deploy:
    environment: production
    steps:
      - uses: azure/login@v2
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
```

1. Grant RBAC to the app’s service principal / MI at least scope.
2. Delete client secrets after OIDC proven.
3. Never use `repo:org/name:*` wildcards unless risk-accepted.

### 5. Verify with evidence

```bash
# CI run: azure/login succeeds; az account show shows correct SP
# Wrong branch/env workflow must fail token exchange
az role assignment list --assignee "$SP_OBJECT_ID" -o table
```

1. Capture failed login from unauthorized subject as evidence of correct scoping.
2. Confirm no `AZURE_CLIENT_SECRET` remains in GitHub secrets for that path.
3. Token lifetime and audience errors → fix federated credential fields, not add secrets blindly.

### 6. Observe and harden

1. Sign-in logs for the application in Entra; alert on new federated credential creation.
2. Review subjects quarterly; remove stale repos/envs.
3. Require GitHub environment reviewers for prod subjects.

### 7. Hand off

1. Document issuer/subject/app/role matrix.
2. Template for new repo onboarding.
3. Revocation steps: delete federated credential + disable SP.

## Subject Design

| Scenario | Subject style |
| --- | --- |
| GitHub env-protected prod | `repo:org/repo:environment:production` |
| GitHub branch | `repo:org/repo:ref:refs/heads/main` |
| AKS SA | `system:serviceaccount:ns:name` |
| Pull request | Avoid privileged deploy subjects from forks |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Subject | Narrow env/SA | `repo:org/*:ref:refs/heads/*` style overbreadth |
| Secrets | Removed after OIDC | Keep long-lived client secret forever |
| Roles | RG-scoped deploy | Subscription Owner for CI app |
| Forks | No prod OIDC from fork PRs | PR from fork deploys prod |
| Review | Entra audit on federated cred changes | Untracked portal edits |

## Output Checklist

- [ ] App/MI and issuer documented
- [ ] Subject least privilege designed
- [ ] Federated credential created
- [ ] Azure RBAC scoped and assigned
- [ ] CI/workload login succeeds
- [ ] Unauthorized subject fails
- [ ] Client secrets removed or ticketed
- [ ] Audit/alert on trust changes
- [ ] `code-quality-standards` applied to workflows

## Rules

- Authorized identity administration only.
- Narrow subjects; no casual wildcards.
- Prefer OIDC over client secrets for CI.
- Do not log id-tokens or access tokens.
- Pair with environment protection and least RBAC.
