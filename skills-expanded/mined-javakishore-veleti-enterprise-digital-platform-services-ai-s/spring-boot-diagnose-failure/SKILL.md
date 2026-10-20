---
name: spring-boot-diagnose-failure
description: Diagnose Spring Boot service failures by inspecting the current service repository, .digital-platform-ai metadata, application code, configuration, logs, traces, runtime signals, dependent services, and operations context. Use for HTTP 4xx/5xx errors, exceptions, startup failures, dependency failures, latency regressions, deployment-related application failures, or production incident investigation.
---

# Diagnose Spring Boot Failure

1. Read `.digital-platform-ai/service.yaml`, dependencies, environments, observability metadata, and relevant `ServiceInstructions-*.md`.
2. Identify the target environment, application version, corresponding `-ops` repository, and affected request or workflow.
3. Inspect the relevant Spring Boot code and configuration before making code-level claims.
4. Gather independent evidence in parallel when useful from logs, traces, metrics, runtime platform state, databases, caches, and dependent services.
5. Correlate by request ID, trace ID, deployment version, timestamp, endpoint, pod/container, and downstream dependency.
6. Identify the first confirmed divergence from expected behavior rather than the loudest downstream symptom.
7. Route specialized findings to capability or platform skills such as `spring-boot-security-*`, `spring-boot-data-*`, `spring-boot-observability-*`, `aks-*`, `datadog-*`, `redis-*`, `postgres-*`, `mongodb-*`, `kafka-*`, or `eventhub-*`.
8. Separate observed evidence, inference, and unknowns.
9. Do not modify production resources unless explicitly authorized.

## Output
- Incident Scope
- First Confirmed Failure
- Supporting Evidence
- Affected Components
- Root Cause Status
- Recommended Action
- Remaining Unknowns
