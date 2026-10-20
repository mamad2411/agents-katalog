---
name: azure-keyvault-rbac-migration
description: >
  Migrate Azure Key Vault from access policies to Azure RBAC permission model for
  owned vaults: inventory policies, map to data-plane roles, dual-run cutover,
  enableRbacAuthorization, and break-glass validation. Use when converting vaults
  or fixing apps broken after RBAC enablement — not for general vault creation alone.
---

# Azure Key Vault Access Policy → RBAC Migration

## Scope And Authorization

- **In scope:** Key Vaults you own where you may change permission model and role assignments.
- **Out of scope:** Changing vaults outside authorization; bulk-reading secrets during migration.
- Enabling RBAC **disables classic access policies** for data plane — apps can break immediately.
- Pair baseline controls with `azure-keyvault-basics`; use `code-quality-standards` for IaC.

## When To Use

- Vault still uses access policies; org standard is Azure RBAC.
- Preparing for per-key/secret scope assignments or Privileged Identity Management patterns.
- Incident: vault switched to RBAC without mapping policies → widespread 403.
- Aligning Terraform/Bicep modules to `enableRbacAuthorization = true`.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General KV hardening | `azure-keyvault-basics` |
| HSM key management | `azure-keyvault-hsm` |
| Secrets vs App Config | `azure-keyvault-appconfig-split` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Access policies | Azure RBAC data plane |
| --- | --- |
| Per-vault identity entries | Role assignments on vault or item scope |
| Built-in permission checkboxes | Roles: Secrets User/Officer, Crypto User/Officer, Certificates… |
| Coexists poorly once RBAC on | Classic policies ignored when RBAC enabled |
| Tooling | `az keyvault show`, `az role assignment`, Policy, Portal access control |

## Workflow

### 1. Confirm scope and success criteria

1. Vault list, cutover window, app owners, break-glass admins, authorization.
2. Success: every former policy principal has equivalent RBAC; smoke tests pass; policies documented as retired.
3. Rollback: only possible if you re-disable RBAC quickly **and** policies still exist — snapshot first.

### 2. Inventory access policies and current model

```bash
az keyvault show -n "$VAULT" -g "$RG" --query "properties.enableRbacAuthorization"
az keyvault show -n "$VAULT" -g "$RG" --query "properties.accessPolicies" -o jsonc > policies-$VAULT.json
az role assignment list --scope "$VAULT_ID" -o table
```

1. For each policy object id, resolve display name (app registration, MI, group, user).
2. Record permissions: secrets/keys/certs get/list/set/delete/backup/restore/purge…
3. Note deployment SPs and human admins separately.

### 3. Map policies → roles

| Policy intent | Typical RBAC role |
| --- | --- |
| get/list secrets only | Key Vault Secrets User |
| set/delete secrets | Key Vault Secrets Officer |
| sign/encrypt/decrypt | Key Vault Crypto User |
| full key admin | Key Vault Crypto Officer |
| cert get | Key Vault Certificate User (or Officer for manage) |
| full vault data admin | Key Vault Administrator (minimize; PIM) |
| control plane only | Reader / Key Vault Contributor (does **not** grant secret values) |

1. Prefer **group** assignments over individual users.
2. Scope to individual secret/key paths when one app must not read all secrets.
3. Create missing role assignments **before** flipping the vault flag.

### 4. Dual-run then cut over

```bash
# Pre-create RBAC (example)
az role assignment create --role "Key Vault Secrets User" \
  --assignee-object-id "$APP_MI" --assignee-principal-type ServicePrincipal \
  --scope "$VAULT_ID"

az role assignment create --role "Key Vault Administrator" \
  --assignee-object-id "$ADMIN_GROUP" --assignee-principal-type Group \
  --scope "$VAULT_ID"

# Verify assignments
az role assignment list --scope "$VAULT_ID" -o table

# Cut over — access policies stop authorizing data plane
az keyvault update -n "$VAULT" -g "$RG" --enable-rbac-authorization true
```

1. Test critical apps immediately after flip.
2. Watch for ARM templates still using `accessPolicies` array — update IaC.
3. Remove stale access policy entries from templates to avoid confusion (they won’t apply under RBAC).

### 5. Verify with evidence

```bash
az keyvault show -n "$VAULT" -g "$RG" --query "properties.enableRbacAuthorization"
# App identity: secret show OK
# Removed principal: 403 Forbidden
# Portal: Access configuration shows Azure role-based access control
```

1. Regression list: every app/job signed off.
2. Human break-glass via PIM elevation works.
3. CI deployment SP can set secrets only if intended (Officer), not by accident.

### 6. Observe and harden

1. Alert on `Microsoft.KeyVault/vaults/write` changing `enableRbacAuthorization`.
2. Access reviews quarterly for Officer/Admin roles.
3. Policy: audit vaults still on access policies.

### 7. Hand off

1. Mapping spreadsheet: old policy → role → scope → owner.
2. Updated Bicep/Terraform modules.
3. Incident tip: 403 after migration → check role assignment + scope, not network first.

## Common Breakage

| Symptom | Cause | Fix |
| --- | --- | --- |
| All apps 403 | RBAC on, no roles | Assign roles; temporary disable only if break-glass plan allows |
| Portal can see vault, not secrets | Control plane Reader only | Add data plane role |
| One secret denied | Scoped assignment missing | Assign at secret scope or broaden carefully |
| Terraform drift | Still manages accessPolicies | Switch to `azurerm_role_assignment` |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Order | Roles first, then enable flag | Flip flag then invent roles under outage |
| Humans | PIM eligible Admin | Standing Admin for all engineers |
| Scope | Per-app least privilege | Everyone Secrets Officer on vault |
| IaC | RBAC resources in git | Portal-only assignments |
| Evidence | Per-app smoke checklist | “Looks enabled in portal” |

## Output Checklist

- [ ] Access policies exported and principals resolved
- [ ] Mapping to RBAC roles completed and reviewed
- [ ] Role assignments created pre-cutover
- [ ] `enableRbacAuthorization=true` applied in window
- [ ] All consumers smoke-tested
- [ ] IaC updated; accessPolicies retired from modules
- [ ] Break-glass PIM path verified
- [ ] Monitoring for model changes
- [ ] `code-quality-standards` applied

## Rules

- Never flip RBAC without a complete principal map.
- Do not paste secret values while testing — use metadata and app health.
- Prefer groups and PIM for privileged roles.
- Authorized vaults only.
- Keep dual-control for production Officer assignments.
