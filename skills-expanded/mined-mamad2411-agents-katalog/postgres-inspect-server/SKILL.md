---
name: postgres-inspect-server
description: Inspect Azure Database for PostgreSQL Flexible Server configuration, compute/storage, PostgreSQL version, HA, replicas, networking, identity, backup, extensions, parameters, monitoring, and environment context. Use as the primary Azure PostgreSQL entry point when the failure domain is unknown.
---

# Inspect Flexible Server

1. Read `.digital-platform-ai/postgres.yaml`, service metadata, environments, and relevant instructions.
2. Resolve subscription, resource group, server, database, region, environment, and consuming applications.
3. Inspect PostgreSQL version, compute tier, storage, HA, replicas, networking, authentication, backup, extensions, server parameters, and monitoring.
4. Identify whether the issue is availability, query, connection, storage, identity, network, migration, extension, AI/vector, or application related.
5. Route to focused `postgres-*` skills.
6. Do not mutate production resources unless explicitly authorized.

## Output
- Server Context
- Managed Configuration
- Runtime State
- Scope Assessment
- Recommended Next Skill
