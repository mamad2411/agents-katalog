---
name: azure-blob-misconfig
description: >
  Authorized assessment and hardening of Azure Blob Storage public access
  misconfigurations: container public access, anonymous read, SAS/shared keys,
  account firewalls, soft-delete, and logging. Use when assessing org-owned storage
  accounts or written engagements — not unauthorized enumeration of third-party blobs.
---

# Azure Blob Storage Misconfiguration

## Scope And Authorization

- **In scope:** Storage accounts and containers in Azure subscriptions you own or are authorized to assess.
- **Out of scope:** Hunting or downloading third-party public blobs; abusing SAS tokens found on the Internet.
- Prefer read-only discovery first; disabling public access can break CDN/static sites — coordinate owners.
- Redact account keys and SAS from tickets; rotate if exposed in chat/logs.
- Pair IaC with `code-quality-standards`.

## When To Use

- Defender for Cloud / CSPM findings: anonymous blob access, public containers.
- Hardening app uploads, logs, backups, static website accounts.
- Reviewing overly broad SAS, account keys in apps, missing firewalls/private endpoints.
- Enabling soft delete, versioning, immutable storage where required.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| AWS S3 public access hardening | `aws-s3-bucket-hardening` |
| Key Vault secrets | `azure-keyvault-basics` |
| Front Door / WAF edge | `azure-frontdoor-waf` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Control | Target |
| --- | --- |
| AllowBlobPublicAccess | Prefer `false` at account |
| Container publicAccess | `Off` unless deliberate static content with owner |
| Shared key | Prefer Azure AD / MI; disable shared key when possible |
| SAS | Short TTL, least permissions, stored access policies, HTTPS only |
| Network | Firewall + private endpoint; trusted Azure services as needed |
| Data protection | Soft delete, versioning, optional immutability |
| Tooling | `az storage`, Azure Policy, Defender for Storage, Activity Log |

## Workflow

### 1. Confirm scope and success criteria

1. Subscriptions, resource groups, storage accounts, data classification, authorization.
2. Success: no unexpected anonymous access; public exceptions ticketed; keys not in code.
3. List intentional public containers (static websites) with owners.

### 2. Inventory accounts and public exposure

```bash
az account show
az storage account list --query "[].{name:name,rg:resourceGroup,allowBlobPublicAccess:allowBlobPublicAccess,https:enableHttpsTrafficOnly,minTls:minimumTlsVersion}" -o table

ACCT=stappprod
RG=rg-app-prod
az storage account show -n "$ACCT" -g "$RG" -o jsonc
az storage container list --account-name "$ACCT" --auth-mode login -o table
az storage container show --account-name "$ACCT" --name "$CONTAINER" --auth-mode login \
  --query "properties.publicAccess"
```

1. Check blob anonymous read with authorized test only on owned URLs.
2. Inventory diagnostic settings and Defender for Storage plan.
3. Search pipelines for `AccountKey=` and long-lived SAS (secrets hygiene).

### 3. Baseline

1. Export current network rules, public access flags, container ACLs.
2. Note clients using shared key vs AAD OAuth.
3. Soft-delete retention days.

### 4. Remediate misconfigurations

```bash
# Deny new public blob access at account
az storage account update -n "$ACCT" -g "$RG" --allow-blob-public-access false

# Set container private
az storage container set-permission --account-name "$ACCT" --name "$CONTAINER" \
  --public-access off --auth-mode login

# HTTPS + TLS
az storage account update -n "$ACCT" -g "$RG" --https-only true --min-tls-version TLS1_2

# Network: default deny + selected nets / private endpoint (illustrative)
az storage account update -n "$ACCT" -g "$RG" --default-action Deny
# Then add VNet rules / create private endpoint as designed

# Soft delete for blobs
az storage blob service-properties delete-policy update --account-name "$ACCT" \
  --enable true --days-retained 14 --auth-mode login
```

1. Prefer managed identity + RBAC roles (`Storage Blob Data Reader/Contributor`) over keys.
2. Disable shared key access only after all clients migrate to AAD:
   `az storage account update ... --allow-shared-key-access false`
3. SAS: use user delegation SAS where possible; revoke via stored access policy rotation.
4. Static websites: prefer Front Door/CDN with private origin instead of public container when feasible.

### 5. Verify with evidence

```bash
az storage account show -n "$ACCT" -g "$RG" --query "{public:allowBlobPublicAccess,key:allowSharedKeyAccess,https:enableHttpsTrafficOnly,net:networkRuleSet}"
# Anonymous GET to a private blob URL should fail
curl -sI "https://${ACCT}.blob.core.windows.net/${CONTAINER}/probe.txt" | head -n1
# Authorized path
az storage blob download --account-name "$ACCT" -c "$CONTAINER" -n probe.txt --auth-mode login -f /tmp/probe.txt
```

1. Defender recommendations resolve or are exception-ticketed.
2. App smoke tests with MI succeed; key-based clients identified if broken.
3. Attach redacted before/after JSON to change ticket.

### 6. Observe and harden

1. Azure Policy: deny public blob access, require HTTPS, require soft delete.
2. Alert on `Microsoft.Storage/storageAccounts/write` changing public flags.
3. Periodic SAS inventory and key regeneration schedule if keys still enabled.

### 7. Hand off

1. Exception register for public containers with expiry.
2. IaC modules defaulting to private + AAD data plane.
3. Incident path if keys/SAS leaked: rotate keys, revoke policies, purge tokens from git history process.

## Common Findings

| Finding | Severity | Fix direction |
| --- | --- | --- |
| Container `blob`/`container` public | High | Set Off + account deny public |
| Account keys in appsettings | High | MI + Key Vault reference |
| SAS years-long, `sc=rwdl` | High | Short TTL least privilege |
| No firewall, public endpoint | Medium | PE + deny default |
| Soft delete off on backups | Medium | Enable retention |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Public access | Account-level false | Per-container hope |
| Auth | MI + RBAC data plane | Account key in mobile app |
| SAS | User delegation, minutes-hours | `?sv=...&sig=` in git forever |
| Network | Private endpoint | Open + “security by name” |
| Verification | curl anonymous + az login path | Portal glance only |

## Output Checklist

- [ ] Scope and authorization recorded
- [ ] Accounts/containers inventoried for public access
- [ ] Public access disabled or exceptions ticketed
- [ ] HTTPS/TLS and network baseline applied
- [ ] Shared key / SAS strategy decided
- [ ] Soft delete / versioning considered
- [ ] Evidence of anonymous deny + authorized allow
- [ ] Policy/monitoring planned
- [ ] `code-quality-standards` applied if IaC shipped

## Rules

- Authorized storage only; no third-party blob abuse.
- Prefer AAD/MI over shared keys and broad SAS.
- Never paste account keys or live SAS into chat.
- Document public exceptions with owners and expiry.
- Fix root app design, not only the CSPM checkbox.
