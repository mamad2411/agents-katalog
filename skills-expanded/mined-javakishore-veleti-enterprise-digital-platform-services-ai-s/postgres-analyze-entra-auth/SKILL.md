---
name: postgres-analyze-entra-auth
description: Analyze Microsoft Entra authentication for Azure Database for PostgreSQL Flexible Server, including administrators, users/roles, managed identities, token-based authentication, group access, and application failures. Use for passwordless PostgreSQL access or Entra authorization issues.
---

# Analyze Entra Authentication

1. Identify application/user identity, tenant, server, database role, and required operation.
2. Inspect configured Entra administrator and database role mapping.
3. Verify managed identity or workload identity token acquisition when applicable.
4. Correlate token/authentication failures with network and PostgreSQL authorization.
5. Distinguish Azure identity authentication from PostgreSQL object privileges.
6. Never print access tokens or credentials.

## Output
- Identity Mapping
- Entra Configuration
- PostgreSQL Role Findings
- Failure Layer
- Recommended Action
