---
name: azure-purview-basics
description: >
  Microsoft Purview (data governance / data map) basics for owned tenants: account
  setup, data source registration, scans, classifications, collections, and access
  control for catalog consumers. Use when standing up data discovery/governance or
  classifying sensitive data estates — not for unauthorized scanning of third-party
  data sources.
---

# Microsoft Purview Basics

## Scope And Authorization

- **In scope:** Purview accounts and data sources you own or are authorized to scan/govern.
- **Out of scope:** Registering/scanning data systems without owner approval; exporting catalogs with sensitive classifications publicly.
- Scans can read metadata (and sometimes content samples depending on config) — treat as privileged.
- Pair storage/SQL hardening with service skills; `code-quality-standards` for automation.

## When To Use

- First Purview account for data map / catalog.
- Registering Azure Storage, SQL, Snowflake (supported sources), etc., and running scans.
- Configuring collections hierarchy and role assignments (Data Source Admin, Data Reader…).
- Reviewing classifications/sensitivity labels integration patterns.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Blob public access fix | `azure-blob-misconfig` |
| Key Vault secrets | `azure-keyvault-basics` |
| Defender plans | `azure-defender-cloud` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Detail |
| --- | --- |
| Account | Purview account resource; region considerations |
| Collections | Hierarchy for ownership and RBAC scoping |
| Data source | Registered system with scan credentials/MI |
| Scan | Schema/classification discovery schedule |
| Atlas/catalog | Assets, lineage (where configured), glossary |
| Tooling | Azure Portal Purview governance portal, `az purview`, REST |

## Workflow

### 1. Confirm scope and success criteria

1. Data domains, sources in scope, legal basis for scanning, authorization, region.
2. Success: sources registered; scans succeed; classifications visible to authorized catalog users only.
3. Exclude out-of-scope personal datasets.

### 2. Inventory Purview and sources

```bash
az account show
az purview account list -o table 2>/dev/null || true
az purview account show -n "$PURVIEW" -g "$RG" -o jsonc
# List managed identity of Purview account for RBAC grants
```

1. Map collections to business domains.
2. List who has Purview Data Curator vs Reader.
3. Identify sources already in Defender/SQL audits.

### 3. Baseline governance model

1. Collection tree (root → domain → system).
2. Classification rules and custom rules needs.
3. Integration with Entra groups for catalog access.

### 4. Register, authorize, scan

```bash
# Grant Purview MI data read on a storage account (example)
PU_MI=$(az purview account show -n "$PURVIEW" -g "$RG" --query identity.principalId -o tsv)
az role assignment create --assignee-object-id "$PU_MI" --assignee-principal-type ServicePrincipal \
  --role "Storage Blob Data Reader" --scope "$STORAGE_ID"

# Prefer portal/API for data source registration + scan rule sets when CLI coverage is limited
# Configure scan: full vs incremental, classification on, schedule off-peak
```

1. Use **managed identity** or scoped SP — not personal user creds — for scans.
2. Limit scan rule sets to needed classifiers; sampling settings per privacy review.
3. Collections: put each source under the owning domain collection.
4. Glossary terms assigned by stewards, not only auto-classifiers.
5. Network: private endpoints for Purview and sources when required; self-hosted IR for private/on-prem sources.

### 5. Verify with evidence

1. Scan history shows succeeded; asset count non-zero for known schemas.
2. Sample asset shows schema and classification (e.g. suspected UPI patterns) — handle carefully.
3. User without Reader role cannot search catalog.
4. Lineage appears only where integration configured (ADF/Synapse/etc.).

### 6. Observe and harden

1. Monitor failed scans (cred expiry, network).
2. Access reviews on Purview roles; alert on broad Reader grants.
3. Export controls: who can download catalogs.

### 7. Hand off

1. Operating model: stewards, scan owners, classification dispute process.
2. Onboarding checklist for new data sources.
3. Runbook for IR and private network failures.

## Role Snapshot

| Role | Intent |
| --- | --- |
| Purview Data Source Admin | Register/scan sources |
| Purview Data Curator | Edit annotations/glossary links |
| Purview Data Reader | Discover/search catalog |
| Collection Admin | Scope governance within collection |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Auth for scans | MI least privilege | Shared SQL sa password in scan config |
| Scope | Owner-approved sources | Scan entire tenant “to see what happens” |
| Access | Group-based Readers | Entire company Curator |
| Privacy | Classification governance | Publishing raw samples externally |
| Ops | Scheduled scans + alerts | One-off scan never refreshed |

## Output Checklist

- [ ] Authorization and legal scope recorded
- [ ] Purview account and collections designed
- [ ] Data sources registered under correct collections
- [ ] Scan identity least privilege granted
- [ ] Successful scans evidenced
- [ ] Catalog RBAC verified (positive/negative)
- [ ] Classification/steward process defined
- [ ] Network/IR requirements met
- [ ] `code-quality-standards` applied to automation

## Rules

- Only scan authorized data sources.
- Treat catalog metadata as sensitive.
- Least privilege for Purview MI and users.
- Keep self-hosted IR patched and private.
- Do not paste discovered secret-like strings into tickets.
