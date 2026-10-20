---
name: keyvault-analyze-github-actions
description: Analyze GitHub Actions integration with Azure Key Vault using OIDC/federated identity, Azure login, managed access, secret retrieval, workflow permissions, and least privilege. Use for CI/CD access failures or hardcoded-secret reduction.
---

# Analyze GitHub Actions Integration

1. Identify workflow, Azure identity/service principal, federated credential, repository/environment, and required Key Vault operations.
2. Prefer OIDC/federated login over long-lived client secrets.
3. Inspect workflow `permissions`, environment protection, Azure role assignments, and Key Vault RBAC.
4. Check network reachability if the vault is private.
5. Ensure retrieved secrets are masked and never echoed.
6. Distinguish GitHub OIDC, Azure authentication, RBAC, and network failures.

## Output
- Workflow Identity Model
- OIDC/Federation Findings
- RBAC/Network Findings
- Secret Handling Risks
- Recommended Action
