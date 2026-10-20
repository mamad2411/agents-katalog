---
name: aws-elasticache-redis-analyze-connections
description: Analyze ElastiCache client connections, pooling or multiplexing, TLS, DNS, retry storms, reconnect behavior, connection limits, and long-lived IAM-authenticated sessions. Use for AWS ElastiCache engineering, architecture, operations, or incident analysis when Redis OSS or Valkey compatibility is material to the task.
---

# Analyze Connections

1. Read `.digital-platform-ai/redis-aws.yaml`, service metadata, dependencies, environments, observability metadata, and relevant service instructions.
2. Resolve whether the target is node-based ElastiCache or ElastiCache Serverless and whether the engine is Redis OSS or Valkey before applying service-specific guidance.
3. Resolve AWS account, region, cache/replication group, engine version, shard/replica topology, VPC path, authentication model, encryption, consuming application, and workload pattern.
4. Gather configuration and runtime evidence before drawing conclusions. Separate observed evidence from inference.
5. Check client-side behavior as well as ElastiCache-side state; a Redis timeout is evidence of a timeout, not proof that ElastiCache is the root cause.
6. Treat node-based replica propagation and Global Datastore replication as asynchronous unless the deployed feature explicitly documents stronger durability semantics.
7. Verify feature availability against the actual engine, version, cache type, region, and topology before recommending a capability.
8. Route generic Redis semantics to portable Redis reasoning only when AWS-managed behavior is not material. Route KMS details to `kms-*`, Datadog to `datadog-*`, and application issues to framework skills.
9. Do not mutate production resources unless explicitly authorized. Never expose credentials, auth tokens, connection strings, cached sensitive values, or key material.

## Output
- ElastiCache Context
- Observed Evidence
- Findings
- AWS Platform vs Client/Application Assessment
- Recommended Action
- Remaining Unknowns
