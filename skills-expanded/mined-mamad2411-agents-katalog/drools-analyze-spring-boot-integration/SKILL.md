---
name: drools-analyze-spring-boot-integration
description: Analyze Drools integration in Spring Boot services including KieContainer/KieBase/KieSession configuration, bean lifecycle, rule loading, request flow, concurrency, observability, and error handling. Use for enterprise Java microservice integration or runtime failures.
---

# Analyze Spring Boot Integration

1. Trace the application path from controller/message consumer to rule execution and result handling.
2. Inspect KIE configuration, bean scopes, artifact loading, session creation/disposal, and exception handling.
3. Verify concurrency and lifecycle assumptions.
4. Correlate rule failures with Spring Boot logs, traces, deployment version, and configuration.
5. Route framework-specific issues to relevant `spring-boot-*` skills.
6. Avoid embedding business-rule semantics in integration glue.

## Output
- Integration Flow
- KIE Configuration
- Lifecycle/Concurrency Findings
- Runtime Evidence
- Recommended Action
