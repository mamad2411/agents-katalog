---
name: keyvault-analyze-azure-devops
description: Analyze Azure DevOps pipelines and variable-group integration with Azure Key Vault, service connections, RBAC, secret retrieval, masking, network access, and pipeline failures. Use for Azure DevOps CI/CD secret integration.
---

# Analyze Azure DevOps Integration

1. Identify pipeline, service connection, variable group or task integration, vault, and required objects.
2. Inspect service-principal/workload identity permissions and Key Vault authorization.
3. Check whether secret values are masked and avoided in logs/artifacts.
4. Inspect private-network reachability from build agents when applicable.
5. Distinguish service-connection, Key Vault RBAC, pipeline, and network failures.
6. Prefer short-lived/federated credentials when supported by the enterprise setup.

## Output
- Pipeline Identity
- Variable Group/Task Findings
- RBAC/Network Findings
- Secret Exposure Risks
- Recommended Action
