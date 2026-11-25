---
name: postgres-analyze-azure-ai
description: Analyze Azure AI integration extensions for Azure Database for PostgreSQL Flexible Server when supported, including Azure OpenAI/AI service connectivity, embedding generation, SQL workflows, authentication, networking, quotas, and operational risk. Use for database-integrated AI workflows.
---

# Analyze Azure AI Integration

1. Verify the exact Azure AI extension/capability is supported for the deployed PostgreSQL version and region.
2. Identify AI endpoint/model, database workflow, authentication method, network path, and expected throughput.
3. Inspect SQL-side calls, latency, retry/error behavior, and quota dependencies.
4. Prefer managed identity or secure secret references where supported.
5. Separate model-service failures from PostgreSQL query/extension failures.
6. Never expose AI service keys or tokens.

## Output
- Capability Support
- Database/AI Flow
- Identity/Network Findings
- Latency/Quota Findings
- Recommended Action
