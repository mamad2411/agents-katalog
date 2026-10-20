---
name: drools-analyze-session
description: Analyze Drools KieSession and StatelessKieSession lifecycle, fact retention, disposal, concurrency boundaries, memory behavior, and execution patterns. Use for session leaks, stale facts, concurrency concerns, or stateful-versus-stateless design review.
---

# Analyze Session

1. Identify session type, creation point, scope, reuse pattern, and disposal behavior.
2. Inspect fact lifetime and whether state intentionally survives requests/events.
3. Check concurrency boundaries and application lifecycle integration.
4. Identify stale-fact, memory-retention, unsafe-sharing, or excessive-session-creation risks.
5. Correlate session behavior with runtime memory and latency evidence.
6. Do not recommend stateful sessions without a clear stateful requirement.

## Output
- Session Lifecycle
- Fact Retention
- Concurrency Findings
- Memory/Correctness Risks
- Recommended Pattern
