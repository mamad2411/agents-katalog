---
name: spring-boot-diagnostics-analyze-dependency-failure
description: Analyze downstream dependency failures from Spring Boot using code paths, clients, retries, traces, logs, and dependency-specific evidence. Use for Spring Boot diagnostics engineering, architecture, or runtime diagnosis.
---

# Analyze Dependency Failure

1. Read the current service repository, `.digital-platform-ai/` metadata, environment context, deployment version, and relevant service instructions.
2. Inspect code, configuration, JVM/runtime behavior, dependencies, tests, and deployment wiring relevant to the task.
3. Gather evidence from logs, traces, metrics, actuator, JVM diagnostics, Kubernetes/platform state, and dependent systems when diagnostic.
4. Build a timeline and identify the first confirmed divergence rather than treating the loudest symptom as root cause.
5. Separate Spring Boot/JVM findings from platform-specific findings and route those to the owning technology family.
6. Preserve application contracts and production safety boundaries.
7. Do not mutate production resources, kill processes, or change runtime configuration unless explicitly authorized.

## Output
- Scope
- Code/Runtime Findings
- Supporting Evidence
- Root Cause or Design Assessment
- Recommended Action
- Remaining Unknowns
