---
name: postgres-analyze-bicep-arm
description: Analyze Bicep or ARM templates for Azure Database for PostgreSQL Flexible Server, including server, databases, networking, identity, HA, backup, CMK, parameters, and monitoring. Use for template review, deployment failures, or drift.
---

# Analyze Bicep and ARM

1. Identify PostgreSQL and dependent resources, parameters, identities, networking, CMK, diagnostics, and outputs.
2. Inspect secure parameter usage and deployment ordering.
3. Review compute/storage/HA/backup/network settings.
4. Compare template intent with live Azure configuration.
5. Identify risky outputs, public exposure, or replacement behavior.
6. Do not deploy production changes without explicit authorization.

## Output
- Template Scope
- Configuration/Security Findings
- Dependency/Replacement Risk
- Drift
- Recommended Changes
