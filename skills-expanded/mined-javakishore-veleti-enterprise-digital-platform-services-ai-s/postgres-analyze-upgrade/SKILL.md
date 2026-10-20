---
name: postgres-analyze-upgrade
description: Analyze Azure PostgreSQL Flexible Server major-version upgrade readiness, prechecks, extensions, parameters, application/driver compatibility, downtime, validation, and rollback constraints. Use for PostgreSQL version upgrade planning or upgrade incidents.
---

# Analyze Major Version Upgrade

1. Identify current/target PostgreSQL versions, extensions, parameters, schemas, and application drivers.
2. Run or review currently supported Azure prechecks/validation mechanisms.
3. Inspect extension and feature compatibility.
4. Define application/database health gates before and after upgrade.
5. Understand rollback constraints before scheduling production work.
6. Do not initiate a production major upgrade without explicit authorization.

## Output
- Current/Target Versions
- Precheck Findings
- Compatibility Risks
- Validation/Rollback Constraints
- Recommended Plan
