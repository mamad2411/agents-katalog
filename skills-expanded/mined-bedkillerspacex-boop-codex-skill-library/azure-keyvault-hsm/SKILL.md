---
name: azure-keyvault-hsm
description: >
  Azure Key Vault HSM-backed keys for owned vaults: key types (RSA-HSM, EC-HSM),
  Premium vault vs Managed HSM, key operations, import/BYOK/export policies, rotation,
  and crypto-user RBAC. Use when generating or managing HSM-protected keys for apps,
  encryption, or signing — not for extracting HSM key material or unauthorized vaults.
---

# Azure Key Vault HSM Keys

## Scope And Authorization

- **In scope:** Premium Key Vaults or Managed HSM pools you own or are authorized to administer.
- **Out of scope:** Attempts to export non-exportable HSM keys; crypto operations on foreign tenants.
- Key deletion with purge protection has long recovery implications — double-confirm.
- Pair baseline vault controls with `azure-keyvault-basics`; RBAC migration with `azure-keyvault-rbac-migration`.

## When To Use

- Creating RSA-HSM / EC-HSM keys for application encryption, token signing, or CMK.
- Choosing **Key Vault Premium** software+HSM keys vs **Managed HSM** dedicated pool.
- BYOK import of keys into HSM; defining key ops (`encrypt`, `decrypt`, `sign`, `wrapKey`, …).
- Rotation and versioning strategies for HSM keys used as CMK for Storage/Cosmos/SQL.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Vault network/RBAC baseline | `azure-keyvault-basics` |
| Secrets vs App Config | `azure-keyvault-appconfig-split` |
| Generic secrets hygiene | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Offering | Notes |
| --- | --- |
| KV Standard | Software-protected keys/secrets; not HSM |
| KV Premium | HSM-backed keys (FIPS 140-2 Level 2 boundary per Microsoft docs) |
| Managed HSM | Single-tenant HSM pool; higher assurance / control |
| Key ops | Least privilege operations on key items |
| Export | Non-exportable by default for HSM keys |
| Tooling | `az keyvault key`, Managed HSM CLI, Azure Policy, crypto SDK |

## Workflow

### 1. Confirm scope and success criteria

1. Compliance need (HSM required?), regions, apps, CMK targets, authorization, cost.
2. Success: HSM key created; apps perform allowed ops only; unauthorized ops fail; rotation plan exists.
3. Decide Premium vault vs Managed HSM with security architecture.

### 2. Inventory keys and SKU

```bash
az account show
az keyvault show -n "$VAULT" -g "$RG" --query "{sku:properties.sku,rbac:properties.enableRbacAuthorization}"
az keyvault key list --vault-name "$VAULT" -o table
az keyvault key show --vault-name "$VAULT" --name "$KEY" --query "{kty:key.kty,ops:key.keyOps,exp:attributes.expires}"
# Managed HSM:
# az keyvault show --hsm-name "$HSM" ...
```

1. Flag software `RSA` keys that should be `RSA-HSM` under policy.
2. List which Azure services use the key as CMK.
3. Check release policies for secure key release (if used with confidential compute).

### 3. Baseline

1. Document key sizes (RSA 2048/3072/4096, EC P-256/P-384), lifetimes, rotation cadence.
2. Map identities with `Key Vault Crypto User` / `Crypto Officer`.
3. Backup/restore procedures for Managed HSM security domain (break-glass).

### 4. Create and govern HSM keys

```bash
# Premium vault HSM key
az keyvault key create --vault-name "$VAULT" --name "cmk-storage-prod" \
  --kty RSA-HSM --size 3072 \
  --ops wrapKey unwrapKey encrypt decrypt \
  --protection hsm

# EC example for signing
az keyvault key create --vault-name "$VAULT" --name "jwt-sign" \
  --kty EC-HSM --curve P-256 \
  --ops sign verify \
  --protection hsm

# RBAC for app
az role assignment create \
  --role "Key Vault Crypto User" \
  --assignee-object-id "$APP_MI" \
  --assignee-principal-type ServicePrincipal \
  --scope "$VAULT_ID/keys/cmk-storage-prod"
```

1. Restrict `keyOps` to what the app needs (no `sign` if only wrap/unwrap).
2. BYOK: follow Microsoft BYOK tooling; never paste key material into chat.
3. Rotation: create new version; rewrap data keys; keep old version until rewrap completes.
4. Managed HSM: configure local RBAC, security domain download with quorum, private networking.
5. Soft delete + purge protection on vault/HSM resources.

### 5. Verify with evidence

```bash
az keyvault key show --vault-name "$VAULT" --name "cmk-storage-prod" --query "key.kty"
# Expect RSA-HSM / EC-HSM
# Crypto op test from app (encrypt/wrap) succeeds; forbidden op returns error
# Export attempt should fail for non-exportable HSM keys
```

1. CMK resource shows key URI version and is not “key unavailable”.
2. Unauthorized principal cannot crypto-use the key.
3. Disaster drill: key version recovery / Managed HSM security domain process (tabletop).

### 6. Observe and harden

1. Diagnostics on key ops; alert on delete/purge attempts and unusual decrypt volumes.
2. Policy: deny creation of non-HSM keys in prod vaults if compliance requires.
3. Dual control for Crypto Officer assignments via PIM.

### 7. Hand off

1. Key inventory: name, kty, ops, consumers, rotation date.
2. Runbook for version rotation and CMK rewrap.
3. Managed HSM security domain custody procedure (split knowledge).

## Premium KV vs Managed HSM

| Factor | Premium Key Vault | Managed HSM |
| --- | --- | --- |
| Tenancy | Multi-tenant service | Single-tenant pool |
| Ops model | Familiar vault APIs | HSM pool + security domain |
| Scale/compliance | Many HSM key scenarios | Higher control / specialized |
| Cost | Per vault + ops | Pool capacity pricing |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| kty | RSA-HSM/EC-HSM for required keys | Software RSA for regulated CMK |
| keyOps | Minimal ops set | All ops enabled “for later” |
| Access | Crypto User for apps | Admin on every developer |
| Rotation | Version + rewrap plan | Delete old version immediately |
| BYOK | Official tooling + dual control | Private key in Slack |

## Output Checklist

- [ ] SKU/offering choice documented (Premium vs Managed HSM)
- [ ] HSM keys created with correct kty/size/curve
- [ ] keyOps least privilege applied
- [ ] App crypto roles scoped and tested
- [ ] CMK consumers validated
- [ ] Rotation/rewrap runbook written
- [ ] Diagnostics and delete alerts configured
- [ ] Security domain / break-glass (Managed HSM) documented if applicable
- [ ] `code-quality-standards` applied to automation

## Rules

- Authorized crypto administration only.
- Never attempt to exfiltrate HSM private key material.
- Least privilege on key operations and RBAC.
- Treat security domain materials as crown jewels.
- Confirm compliance mapping with security architecture, not marketing labels alone.
