---
name: cosmosdb-analyze-security
description: Analyze Azure Cosmos DB security configuration, including Entra ID/RBAC, managed identity, keys/connection strings, network access, private endpoints, Key Vault references, and least-privilege application access. Use for authentication, authorization, connectivity, or secret-management investigations.
---

# Analyze Security

1. Read service authentication metadata and Cosmos DB account references.
2. Identify the application's intended authentication mechanism.
3. Inspect identity/RBAC assignments, network restrictions, private endpoints, and Key Vault references as applicable.
4. Prefer identity-based access over embedded secrets when supported by the application design.
5. Distinguish authentication, authorization, DNS/network, and database-level failures.
6. Never print or persist secrets, account keys, connection strings, or tokens.

## Output
- Authentication Model
- Access/Network Findings
- Least-Privilege Assessment
- Failure Layer
- Recommended Action
