---
name: secrets-management-audit
description: >-
  Secrets management audit checklist for Azure workloads. Covers the
  authentication hierarchy, Key Vault configuration, access patterns,
  secret rotation, detection of leaked credentials, and common anti-patterns.
when-to-use: >-
  Invoke when auditing secrets management practices, configuring Azure Key
  Vault, reviewing authentication methods, implementing secret rotation,
  or remediating exposed credentials.
categories:
  - security
  - secrets
  - azure
  - audit
---

# Secrets Management Audit

The best secret is one that doesn't exist. Prefer managed identity over every other option.

## Authentication Hierarchy

| Rank | Method | Security | Notes |
|---|---|---|---|
| **1. Best** | Managed identity | No secrets exist | Nothing to leak, rotate, or manage. Always prefer. |
| **2. Good** | Certificate credential | Rotatable, harder to exfiltrate | Stored in Key Vault, automatable |
| **3. Acceptable** | Key Vault secret | Centralized, audited, access-controlled | Requires rotation policy |
| **4. Bad** | App setting / env variable | Not audited, visible in portal | Exposed in logs, portal, config |
| **5. Unacceptable** | Source code | In git history forever | Immediate Critical finding. Rotate immediately. |

**Rule:** Start at rank 1 for every integration. Only drop to lower ranks when managed identity is technically impossible.

---

## Azure Key Vault Configuration

### Required Settings

- [ ] **RBAC access model** — not legacy access policies. Finer-grained, consistent with Azure RBAC.
- [ ] **Soft delete enabled** — mandatory since February 2025. 90-day retention.
- [ ] **Purge protection for production** — prevents permanent deletion during soft-delete period.
- [ ] **Private endpoint** — no public access on production Key Vaults.
- [ ] **Diagnostics enabled** — all access logged to Log Analytics. Alert on unusual patterns.

### RBAC Roles

| Role | Purpose |
|---|---|
| Key Vault Secrets Officer | Manage secrets (create, update, delete) |
| Key Vault Secrets User | Read secrets only |
| Key Vault Crypto Officer | Manage keys |
| Key Vault Certificates Officer | Manage certificates |

### Environment Separation

- [ ] Separate Key Vault per environment (dev, staging, prod)
- [ ] No cross-environment access — prod vault is not accessible from dev
- [ ] Different access policies per environment

---

## Access Patterns by Service

| Service | How to Access Key Vault |
|---|---|
| App Service / Functions | Key Vault references in app settings: `@Microsoft.KeyVault(SecretUri=...)`. Managed identity. |
| AKS | Secrets Store CSI Driver. Workload identity for auth. |
| VMs | Azure SDK with managed identity. `DefaultAzureCredential`. |
| Azure Pipelines | Azure Key Vault task at runtime. Not stored in pipeline variables. |
| Terraform | `azurerm_key_vault_secret` data source |
| Bicep | `getSecret()` function |

---

## Secret Rotation

### Automated Rotation (Preferred)

- Storage account keys — Event Grid trigger + Azure Function
- SQL passwords — Key Vault rotation policy
- Cosmos DB keys — Key Vault rotation policy

### Manual Rotation Pattern (Near-Zero Downtime)

1. Add new secret version to Key Vault
2. Update all consumers to use new version (or use latest version URI)
3. Verify all consumers working with new secret
4. Disable old secret version
5. After grace period, delete old version

### Rotation Frequency

| Sensitivity | Frequency |
|---|---|
| High (database credentials, API keys) | 90 days |
| Standard (service connections) | 180 days |
| Certificates | Before expiry, auto-renew preferred |

- [ ] Configure Key Vault expiry notifications via Event Grid
- [ ] Alert on secrets approaching expiration

---

## Detection — Finding Secrets Where They Shouldn't Be

| Tool | What It Catches |
|---|---|
| GitHub Advanced Security | Secrets in repos, push protection blocks commits |
| Azure DevOps Advanced Security | Credential scanning in Azure Repos |
| Pre-commit hooks (`detect-secrets`) | Secrets before they're committed |
| Key Vault audit logs | Who accesses secrets, when, from where |
| Defender for Key Vault | Unusual access patterns, bulk retrieval, suspicious IPs |

---

## Anti-Patterns (Always a Finding)

| Anti-Pattern | Severity | Remediation |
|---|---|---|
| Secrets in `appsettings.json` committed to source | Critical | Remove from repo, rotate secret, use Key Vault |
| Connection strings as pipeline variables | High | Link to Key Vault via Key Vault task |
| Shared Key Vault across environments | High | Separate vault per environment |
| No rotation policy — secrets never expire | High | Configure rotation policy and expiry |
| Legacy access policies instead of RBAC | Medium | Migrate to RBAC model |
| Building connection strings from individual secrets | Medium | Use managed identity instead |
| Secrets in command-line arguments | High | Visible in process listings — use env vars or files |
| Logging secret values | Critical | Sanitize all log output |

---

## Audit Checklist

- [ ] All production services use managed identity (rank 1) where supported
- [ ] No secrets in source code repositories
- [ ] Key Vault uses RBAC (not access policies)
- [ ] Soft delete and purge protection enabled
- [ ] Private endpoint configured, public access disabled
- [ ] Diagnostics logging to Log Analytics
- [ ] Secret rotation policy defined and automated where possible
- [ ] Expiry notifications configured
- [ ] Separate Key Vault per environment
- [ ] No secrets stored in pipeline variables (linked to Key Vault)
- [ ] Pre-commit hooks or push protection enabled
- [ ] Defender for Key Vault enabled

## Related Skills

- `security-review-framework` — Full security review checklist
- `network-security-design` — Private endpoint and network security
