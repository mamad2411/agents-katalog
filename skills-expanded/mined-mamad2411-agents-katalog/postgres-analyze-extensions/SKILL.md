---
name: postgres-analyze-extensions
description: Analyze PostgreSQL extensions available on Azure Flexible Server, including allowlisting/support, version compatibility, dependencies, upgrades, security, and application usage. Use when a workload depends on pgvector, PostGIS, AGE, RDKit, or other extensions.
---

# Analyze Extensions

1. Identify required extension, version, database, and application use case.
2. Verify that the extension is supported/allowlisted for the target Azure PostgreSQL region/version.
3. Inspect dependencies, upgrade compatibility, privileges, and configuration requirements.
4. Evaluate operational/security impact before enabling extensions.
5. Route specialized vector/AI extension behavior to focused skills.
6. Do not enable production extensions without explicit authorization.

## Output
- Extension Requirement
- Azure Support Status
- Version/Dependency Findings
- Operational Impact
- Recommended Action
