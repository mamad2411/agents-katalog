---
name: keyvault-analyze-terraform
description: Analyze Terraform configuration for Azure Key Vault and Managed HSM, including vault creation, RBAC, private endpoints, purge protection, keys, diagnostics, and application identity wiring. Use for infrastructure-as-code review, drift, or deployment failures.
---

# Analyze Terraform

1. Locate Key Vault/HSM modules, environment variables, role assignments, private endpoint resources, and diagnostics.
2. Inspect authorization model, network access, soft delete/purge protection, SKU, and object definitions.
3. Compare intended Terraform state with observed Azure configuration.
4. Identify drift, lifecycle risks, circular dependencies, or secret material accidentally represented in Terraform.
5. Treat plan/apply as mutating; never execute without explicit authorization.
6. Never expose sensitive Terraform state values.

## Output
- Terraform Scope
- Intended Configuration
- Drift/Security Findings
- Runtime Correlation
- Recommended Action
