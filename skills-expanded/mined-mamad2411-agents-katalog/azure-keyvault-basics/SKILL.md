---
name: azure-keyvault-basics
description: >
  Authorized assessment and hardening of Azure Key Vault: access policies vs Azure
  RBAC, network firewall and private endpoints, soft-delete and purge protection,
  managed identity data-plane access, diagnostics, and secret hygiene. Use when
  reviewing org-owned Key Vaults, ARM/Bicep/Terraform, or written Azure engagements —
  not unauthorized third-party vault enumeration.
---

# Azure Key Vault Basics

## Scope And Authorization

- **In scope:** Key Vaults in subscriptions you own or are authorized to assess/harden.
- **Out of scope:** Enumerating or reading secrets from vaults outside authorization.
- Changes to access policies/RBAC can lock out apps — use change windows and break-glass.
- Never dump secret values into tickets; prefer IDs and metadata.
- Pair RBAC migration details with `azure-keyvault-rbac-migration`; HSM keys with `azure-keyvault-hsm`.

## When To Use

- Baseline hardening of a vault (network, protection, access model).
- Apps need managed identity to read secrets/keys/certs.
- Findings: public network, missing purge protection, broad access policies.
- Choosing access policy model vs Azure RBAC permission model.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Access policy → RBAC migration deep dive | `azure-keyvault-rbac-migration` |
| HSM / key types / key ops | `azure-keyvault-hsm` |
| App Config vs KV split | `azure-keyvault-appconfig-split` |
| Managed identity federation (non-KV) | `azure-managed-identity-federated` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Control | Target posture |
| --- | --- |
| Permission model | Prefer Azure RBAC (data plane roles) for new vaults |
| Network | Default deny public + private endpoint; or strict IP/VNet rules |
| Soft delete | Enabled (default on modern vaults) |
| Purge protection | On for production/secrets of record |
| Auth | Azure AD only; disable local access where applicable |
| Diagnostics | Audit events to Log Analytics |
| Tooling | `az keyvault`, Azure Policy, Defender for Key Vault |

## Workflow

### 1. Confirm scope and success criteria

1. Vault names, RG, env, data classification, app identities, authorization.
2. Success: least-privilege RBAC/policies; purge protection on; diagnostics on; apps still read secrets.
3. Break-glass: admin group via PIM for vault administration.

### 2. Inventory vaults and access

```bash
az account show
az keyvault list -o table
az keyvault show -n "$VAULT" -g "$RG" -o jsonc
az keyvault show -n "$VAULT" -g "$RG" --query "{rbac:properties.enableRbacAuthorization,public:properties.publicNetworkAccess,soft:properties.enableSoftDelete,purge:properties.enablePurgeProtection,net:properties.networkAcls}"
az keyvault secret list --vault-name "$VAULT" -o table  # names only
az role assignment list --scope "$VAULT_ID" -o table
```

1. List access policies if not RBAC mode.
2. Note private endpoints and diagnostic settings.
3. Find human users with secret get on prod vaults (should be rare).

### 3. Baseline

1. Export access policies / role assignments.
2. Map each secret to consumer identity.
3. Confirm backup/disaster expectations for keys vs secrets.

### 4. Harden vault

```bash
# Purge protection + soft delete (purge protection irreversible)
az keyvault update -n "$VAULT" -g "$RG" --enable-purge-protection true

# Prefer RBAC authorization
az keyvault update -n "$VAULT" -g "$RG" --enable-rbac-authorization true

# Grant app MI secrets user (data plane)
az role assignment create \
  --role "Key Vault Secrets User" \
  --assignee-object-id "$APP_MI_PRINCIPAL" \
  --assignee-principal-type ServicePrincipal \
  --scope "$VAULT_ID"

# Network: deny public (then ensure PE / jump path for ops)
az keyvault update -n "$VAULT" -g "$RG" --default-action Deny --public-network-access Disabled

# Diagnostics
az monitor diagnostic-settings create --name kv-diag \
  --resource "$VAULT_ID" \
  --workspace "$LAW_ID" \
  --logs '[{"category":"AuditEvent","enabled":true}]' \
  --metrics '[{"category":"AllMetrics","enabled":true}]'
```

1. Separate **admin** roles (`Key Vault Administrator`) from **app** roles (`Secrets User`, `Crypto User`).
2. Avoid giving humans standing `Secrets Officer` on prod; use PIM.
3. Template secrets with content type and rotation tags; do not store non-secrets (use App Config).
4. Private endpoint DNS (`privatelink.vaultcore.azure.net`) must resolve from app VNet.

### 5. Verify with evidence

```bash
az keyvault show -n "$VAULT" -g "$RG" --query "properties.{rbac:enableRbacAuthorization,purge:enablePurgeProtection,public:publicNetworkAccess}"
# From app identity context: secret show succeeds
# From unauthorized identity: 403
az keyvault secret show --vault-name "$VAULT" --name "app-secret" --query id -o tsv
```

1. Portal/CLI from blocked network should fail when public disabled.
2. Defender for Cloud Key Vault recommendations reviewed.
3. App smoke test post-change.

### 6. Observe and harden

1. Alert on `SecretGet` from unexpected principals; on vault policy changes.
2. Azure Policy: require purge protection, RBAC, deny public network.
3. Periodic access review of role assignments.

### 7. Hand off

1. Vault catalog: purpose, owners, apps, model (RBAC/policy).
2. Break-glass and rotation contacts.
3. IaC module enforcing baseline.

## Access Model Snapshot

| Role (RBAC) | Typical use |
| --- | --- |
| Key Vault Secrets User | App read secrets |
| Key Vault Secrets Officer | Managed rotation jobs |
| Key Vault Crypto User | App encrypt/decrypt/sign |
| Key Vault Administrator | Platform admin (PIM) |
| Reader (control plane) | See vault resource, not secret values |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| App access | MI + Secrets User | Connection string to vault with wide policy |
| Network | PE + deny public | Open vault + “secret names are random” |
| Humans | PIM eligible admin | Standing list of users in access policies |
| Protection | Purge protection on prod | Soft delete off, purgeable by attacker |
| Config split | Secrets only in KV | Feature flags as secrets |

## Output Checklist

- [ ] Vault inventory and authorization recorded
- [ ] Permission model documented (RBAC preferred)
- [ ] Soft delete + purge protection verified for prod
- [ ] Network posture applied (firewall/PE)
- [ ] App MI least privilege verified
- [ ] Diagnostics enabled
- [ ] Negative access tests evidenced
- [ ] Policy/monitoring considered
- [ ] `code-quality-standards` applied if IaC shipped

## Rules

- Authorized vaults only; no secret value dumps.
- Prefer RBAC + managed identity.
- Purge protection is a one-way door — confirm before enable.
- Separate human admin from app data plane access.
- Route deep RBAC migration and HSM topics to specialized skills.
