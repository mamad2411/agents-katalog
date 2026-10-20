---
name: cosmosdb-inspect-account
description: Inspect Azure Cosmos DB account configuration, API mode, regions, consistency, networking, identities, throughput mode, databases, and containers. Use as the general Cosmos DB entry point when account-level context or configuration must be resolved before deeper analysis.
---

# Inspect Account

1. Read `.digital-platform-ai/cosmosdb.yaml`, environment metadata, and relevant service instructions.
2. Resolve the target environment, Cosmos DB account, database, and containers.
3. Inspect account-level settings:
   - API mode
   - regions and write regions
   - consistency configuration
   - networking/private endpoints
   - identity/authentication references
   - backup mode
   - throughput mode
4. Identify whether the issue is account-, database-, container-, or application-scoped.
5. Route to focused Cosmos DB skills based on evidence.
6. Do not modify account configuration unless explicitly authorized.

## Output
- Account Context
- Relevant Configuration
- Scope Assessment
- Evidence
- Recommended Next Skill
