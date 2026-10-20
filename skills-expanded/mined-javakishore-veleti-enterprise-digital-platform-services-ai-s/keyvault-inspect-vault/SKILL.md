---
name: keyvault-inspect-vault
description: Inspect Azure Key Vault configuration, SKU, RBAC/access model, networking, private endpoints, soft delete, purge protection, diagnostics, keys, secrets, certificates, and environment context. Use as the general Azure Key Vault entry point when the issue domain is not yet known.
---

# Inspect Vault

1. Read `.digital-platform-ai/keyvault.yaml`, service metadata, environments, and relevant instructions.
2. Resolve subscription, resource group, vault name, environment, and consuming applications.
3. Inspect:
   - vault SKU
   - RBAC vs access-policy authorization model
   - public/private network access
   - private endpoints and DNS
   - soft delete and purge protection
   - diagnostics and monitoring
   - keys, secrets, and certificates inventory metadata
4. Identify whether the issue is identity, authorization, networking, secret/key/certificate lifecycle, application integration, or governance.
5. Route to focused `keyvault-*` skills based on evidence.
6. Never expose secret values, keys, certificates, or tokens.

## Output
- Vault Context
- Security/Network Configuration
- Protection/Diagnostics State
- Scope Assessment
- Recommended Next Skill
