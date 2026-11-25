---
name: spring-boot-batch-diagnose-failure
description: Diagnose failed or stuck Spring Batch executions using job repository state, logs, step metrics, retries, and dependent systems. Use for Spring Boot batch engineering, architecture, or runtime diagnosis.
---

# Diagnose Batch Failure

1. Read the current service repository, `.digital-platform-ai/` metadata, environment context, and relevant service instructions.
2. Inspect the exact Spring Boot code, configuration, framework annotations, dependencies, and tests involved.
3. Gather logs, traces, metrics, actuator evidence, message/job state, and downstream evidence when diagnostic.
4. Separate framework behavior from broker, cloud, database, cache, or infrastructure behavior and route those concerns to the owning technology skill.
5. Identify the first confirmed divergence from expected behavior.
6. Preserve contracts, idempotency, transaction boundaries, and business semantics unless redesign is explicitly requested.
7. Do not mutate production resources unless explicitly authorized.

## Output
- Scope
- Code/Configuration Findings
- Runtime Evidence
- Root Cause or Design Assessment
- Recommended Action
- Remaining Unknowns
