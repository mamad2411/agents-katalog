---
name: keyvault-analyze-bicep-arm
description: Analyze Bicep or ARM templates for Azure Key Vault, Managed HSM, RBAC, networking, diagnostics, keys, and dependent-service integration. Use for template review, deployment failures, or configuration drift.
---

# Analyze Bicep/ARM

1. Identify Key Vault/HSM resources, parameters, role assignments, networking, diagnostics, and outputs.
2. Check secure parameter usage and ensure secrets are not emitted through outputs/logging.
3. Inspect dependencies and deployment ordering for identities, private endpoints, and role assignments.
4. Compare template intent with live Azure configuration.
5. Identify risky defaults such as public exposure or missing protection settings.
6. Do not deploy changes unless explicitly authorized.

## Output
- Template Scope
- Security/Dependency Findings
- Drift
- Deployment Risk
- Recommended Changes
