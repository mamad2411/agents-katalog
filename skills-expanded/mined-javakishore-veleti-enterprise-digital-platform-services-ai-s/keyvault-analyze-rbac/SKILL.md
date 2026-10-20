---
name: keyvault-analyze-rbac
description: Analyze Azure Key Vault Azure RBAC configuration, role assignments, scopes, principals, data-plane access, least privilege, and authorization failures. Use for access denied errors, RBAC migration, or permission reviews on standard Key Vault vaults.
---

# Analyze RBAC

1. Identify caller principal, operation, vault, object type, and target scope.
2. Confirm whether the vault uses Azure RBAC authorization.
3. Inspect role assignments and scopes relevant to secret, key, or certificate operations.
4. Distinguish control-plane permissions from data-plane permissions.
5. Check propagation timing and role scope before concluding the assignment is ineffective.
6. Prefer least-privilege built-in roles or narrowly scoped custom roles.
7. Do not broaden access merely to make an error disappear.

## Output
- Caller Identity
- Required Operation
- Current Role Assignments
- Authorization Gap
- Recommended Role/Scope
