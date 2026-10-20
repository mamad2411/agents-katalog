---
name: eventhub-analyze-security
description: Analyze Azure Event Hubs authentication, authorization, managed identity, Entra ID/RBAC, SAS policies, network access, private endpoints, and least-privilege producer/consumer access. Use for authentication, authorization, connectivity, or secret-management investigations.
---

# Analyze Security

1. Read service authentication metadata and Event Hubs references.
2. Identify intended producer/consumer authentication method.
3. Inspect RBAC assignments, managed identities, SAS policy usage, and network/private endpoint constraints.
4. Prefer identity-based access where consistent with enterprise architecture.
5. Distinguish authentication, authorization, DNS/network, and broker-level failures.
6. Never print or persist keys, connection strings, SAS tokens, or credentials.

## Output
- Authentication Model
- Authorization Findings
- Network Access
- Failure Layer
- Recommended Action
