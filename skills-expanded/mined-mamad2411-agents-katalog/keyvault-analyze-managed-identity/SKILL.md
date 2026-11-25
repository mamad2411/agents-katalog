---
name: keyvault-analyze-managed-identity
description: Analyze system-assigned and user-assigned managed identity access to Azure Key Vault, including principal mapping, RBAC, workload identity, token acquisition, and application/runtime failures. Use when Azure workloads access Key Vault without embedded credentials.
---

# Analyze Managed Identity

1. Identify workload type, identity type, principal/client ID, tenant, vault, and required operation.
2. Verify the intended managed identity is actually attached to the workload.
3. Inspect Key Vault role assignments or access-policy permissions.
4. Check token acquisition and identity selection behavior in the application/runtime.
5. For AKS, distinguish managed identity from Workload Identity and CSI-provider identity.
6. Correlate authorization failures with network/private endpoint state.
7. Never introduce client secrets as a shortcut when managed identity is the intended model.

## Output
- Identity Mapping
- Authorization Findings
- Runtime Token Acquisition
- Failure Layer
- Recommended Action
