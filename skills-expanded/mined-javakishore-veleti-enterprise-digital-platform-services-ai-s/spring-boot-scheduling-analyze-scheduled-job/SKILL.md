---
name: spring-boot-scheduling-analyze-scheduled-job
description: Analyze Spring scheduled jobs, cron/fixed delay/rate semantics, execution overlap, time zones, exceptions, and lifecycle. Use for Spring Boot scheduling engineering, architecture, or runtime diagnosis.
---

# Analyze Scheduled Job

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
