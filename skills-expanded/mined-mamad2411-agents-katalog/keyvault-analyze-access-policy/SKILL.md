---
name: keyvault-analyze-access-policy
description: Analyze legacy Azure Key Vault access policies, object IDs, secret/key/certificate permissions, migration considerations, and authorization failures. Use only when a vault still uses access policies rather than Azure RBAC.
---

# Analyze Access Policy

1. Confirm the vault uses access policies rather than Azure RBAC.
2. Identify principal object ID and required secret/key/certificate operations.
3. Inspect configured permissions and tenant alignment.
4. Check for stale or incorrect principal references.
5. Distinguish access-policy issues from network or authentication failures.
6. When appropriate, note migration considerations to Azure RBAC without forcing a migration.

## Output
- Access Model
- Principal/Permissions
- Missing or Excess Access
- Failure Layer
- Recommended Action
