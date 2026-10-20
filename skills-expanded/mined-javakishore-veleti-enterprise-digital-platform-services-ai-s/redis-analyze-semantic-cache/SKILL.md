---
name: redis-analyze-semantic-cache
description: Analyze semantic caching on Azure Managed Redis for AI workloads including embedding strategy, similarity thresholds, TTLs, invalidation, privacy, quality, latency, and token-cost tradeoffs. Use for Azure Redis engineering, architecture, operations, or incident analysis when Azure Managed Redis or Azure Cache for Redis is material to the task.
---

# Analyze Semantic Cache

1. Read `.digital-platform-ai/redis.yaml`, service metadata, dependencies, environments, observability metadata, and relevant service instructions.
2. Resolve whether the target is Azure Managed Redis or legacy Azure Cache for Redis before applying service-specific guidance.
3. Resolve environment, instance, region, tier, clustering policy, network path, authentication mode, consuming application, and workload pattern.
4. Gather configuration and runtime evidence relevant to the investigation. Separate observed evidence from inference.
5. Check client-side behavior as well as Redis-side state; a Redis timeout is evidence of a timeout, not proof that Redis is the root cause.
6. Verify feature availability against the actual Azure Redis service, tier, region, clustering policy, and enabled modules before recommending a capability.
7. Route cross-layer evidence to `aks-*`, `datadog-*`, `spring-boot-*`, database, or messaging skills when appropriate.
8. Prefer Azure Managed Redis for new architecture decisions; treat Azure Cache for Redis as a migration/legacy context.
9. Do not mutate production resources unless explicitly authorized. Never expose credentials, access keys, tokens, connection strings, or sensitive cached values.

## Output
- Redis Context
- Observed Evidence
- Findings
- Root Cause Status or Architecture Assessment
- Recommended Action
- Remaining Unknowns
