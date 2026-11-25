---
name: azure-managed-identity-basics
description: >
  Azure managed identities for owned resources: system-assigned vs user-assigned,
  enabling identity on compute, granting Azure RBAC, DefaultAzureCredential usage,
  and eliminating connection strings/secrets. Use when wiring apps to Key Vault,
  Storage, SQL, Service Bus without secrets — not for forging tokens or cross-tenant
  abuse.
---

# Azure Managed Identity Basics

## Scope And Authorization

- **In scope:** Azure resources and role assignments in subscriptions you own or operate.
- **Out of scope:** Assigning privileged roles without approval; using identities to access data outside scope.
- Over-privileged managed identities are standing cloud credentials — least privilege required.
- Pair AKS federation with `azure-aks-workload-identity`; federated app creds with `azure-managed-identity-federated`.

## When To Use

- Replacing storage keys, SQL passwords, or Service Bus connection strings with MI.
- Choosing system-assigned vs user-assigned for App Service, Functions, VMs, Container Apps, ACR tasks.
- Debugging `DefaultAzureCredential` / IMDS failures on Azure compute.
- Inventorying identities and their role assignments for access reviews.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| K8s workload identity federation | `azure-aks-workload-identity` |
| Federated credentials on apps (GitHub/OIDC) | `azure-managed-identity-federated` |
| Key Vault hardening | `azure-keyvault-basics` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Type | Lifecycle | Use when |
| --- | --- | --- |
| System-assigned | Tied to resource; deleted with resource | Single resource, simple ops |
| User-assigned | Independent Azure resource; reusable | Shared identity, pre-provision RBAC, blue/green |
| Local dev | Not IMDS — use CLI/VS auth or federated | Never commit SP secrets for prod path |
| Tooling | `az identity`, resource `identity assign`, RBAC, Azure SDKs |

## Workflow

### 1. Confirm scope and success criteria

1. Resource, target Azure services, required data actions, authorization.
2. Success: app accesses target without secrets in config; unauthorized resources denied.
3. Plan removal of old keys after cutover.

### 2. Inventory identities

```bash
az account show
az webapp identity show -g "$RG" -n "$APP" 2>/dev/null
az functionapp identity show -g "$RG" -n "$FN" 2>/dev/null
az identity list -g "$RG" -o table
az role assignment list --assignee "$PRINCIPAL_ID" -o table
```

1. List system vs user-assigned on each compute resource.
2. Flag identities with Owner/Contributor at subscription scope.
3. Find connection strings still present in app settings.

### 3. Baseline

1. Map current secret-based auth per dependency.
2. Note regional IMDS dependency (compute must be on Azure or Arc patterns).
3. SDK versions supporting MI credential chain.

### 4. Enable identity and grant RBAC

```bash
# System-assigned on App Service
az webapp identity assign -g "$RG" -n "$APP"
PRINCIPAL=$(az webapp identity show -g "$RG" -n "$APP" --query principalId -o tsv)

# Or user-assigned
az identity create -g "$RG" -n "id-app-api"
UAMI_ID=$(az identity show -g "$RG" -n "id-app-api" --query id -o tsv)
PRINCIPAL=$(az identity show -g "$RG" -n "id-app-api" --query principalId -o tsv)
az webapp identity assign -g "$RG" -n "$APP" --identities "$UAMI_ID"

# Least privilege examples
az role assignment create --assignee-object-id "$PRINCIPAL" --assignee-principal-type ServicePrincipal \
  --role "Key Vault Secrets User" --scope "$VAULT_ID"
az role assignment create --assignee-object-id "$PRINCIPAL" --assignee-principal-type ServicePrincipal \
  --role "Storage Blob Data Contributor" --scope "$STORAGE_ID"
```

**App code:** use `DefaultAzureCredential` or explicit `ManagedIdentityCredential` with client ID for user-assigned.

1. Prefer data-plane roles over control-plane Contributor.
2. Scope to resource or RG — not subscription — unless platform identity.
3. For Azure SQL: create user from external provider / MI and grant DB roles (T-SQL), not only ARM RBAC.
4. Remove secrets from app settings after dual-run.

### 5. Verify with evidence

```bash
az role assignment list --assignee "$PRINCIPAL" -o table
# App logs: successful token acquire; dependency call 200
# IMDS from VM (authorized): curl token endpoint metadata header required
```

1. Negative: revoke role → app fails closed with clear auth error.
2. Confirm no key fallback still used silently.
3. Local dev path documented without prod secrets.

### 6. Observe and harden

1. Alert on new role assignments to MIs at high scope.
2. Access review of user-assigned identities quarterly.
3. Disable local auth on targets (Storage shared key, KV access policies) when ready.

### 7. Hand off

1. Identity catalog: name, type, resources using it, roles, owner.
2. Standard: user-assigned for shared; system for simple singles.
3. Runbook for rotating away compromised secret-based clients.

## Credential Chain Notes

| Environment | Typical credential |
| --- | --- |
| Azure App Service/Functions/VM | Managed identity via IMDS |
| AKS | Workload identity (federated) — not classic pod MSI alone |
| Local | Azure CLI / VS / env federated |
| GitHub Actions | OIDC federated credential to app/MI |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Roles | Data plane least privilege | Contributor on subscription for app MI |
| Type | User-assigned for stable shared | Recreate system MI lose role mappings carelessly |
| Secrets | Deleted after MI cutover | Keep keys “just in case” in config |
| Code | Azure SDK credential types | Hand-rolled IMDS without error handling |
| Review | Inventory + quarterly | Unknown identities with Owner |

## Output Checklist

- [ ] System vs user-assigned choice documented
- [ ] Identity enabled on compute
- [ ] RBAC (and data plane DB users if needed) granted least privilege
- [ ] App uses MI credential path
- [ ] Old secrets removed or ticketed
- [ ] Positive/negative access tests passed
- [ ] Identity catalog updated
- [ ] High-scope role alerts considered
- [ ] `code-quality-standards` applied

## Rules

- Authorized role assignment only.
- Least privilege always; no standing Owner for apps.
- Prefer MI over keys and client secrets.
- Do not log access tokens.
- Route K8s and GitHub OIDC federation to specialized skills.
