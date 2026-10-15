---
name: eng-multidimensional-audit
description: Execute comprehensive multi-dimensional code reviews and deep architectural repairs using spatial thinking (architecture topology), solid thinking (end-to-end data flow), and reverse thinking (scenario/threat deduction).
---

# Multi-Dimensional Code Review & Remediation

Perform rigorous, holistic code inspection and deep remediation across spatial architecture, end-to-end data flows, and reverse failure scenarios before production deployment.

## Three-Dimensional Review Framework

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     3D Architectural Audit Triad                         │
├─────────────────────────────────────────────────────────────────────────┤
│ 1. Spatial Thinking (空间思维) : Topology, imports, layer isolation, configs │
│ 2. Solid Thinking   (立体思维) : End-to-end request lifecycle, DB, cache, MQ │
│ 3. Reverse Thinking (逆向思维) : Threat modeling, exception paths, bottlenecks│
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Dimension 1: Spatial Architecture Review (空间思维)

1. **Directory Topology & Module Organization**: Verify clean separation of concerns across API, Business Logic, and Data Access layers.
2. **Import Integrity**: Validate all import/require paths, ensuring target modules are resolvable and free of circular dependencies.
3. **Path & Environment Resolution**: Verify configurations, static assets, and log paths against target runtime environments.

---

## Dimension 2: Solid Data-Flow Tracing (立体思维)

1. **Full Request-Response Lifecycle**: Trace data from ingress controllers/handlers down through services, repositories, and persistence engines.
2. **Contract Alignment**: Verify API schema parameters, return payloads, and HTTP status codes match client contracts.
3. **Persistence & Transactions**: Check database connection pool sizing, transactional boundaries (`@Transactional` or `BEGIN/COMMIT`), and safe resource release (`try-with-resources` / `defer` / `finally`).
4. **Caching & Asynchronous Processing**: Audit cache invalidation consistency (cache-aside / write-through) and message queue delivery guarantees (idempotency, dead-letter queues).

---

## Dimension 3: Reverse Scenario & Threat Deduction (逆向思维)

1. **Scenario Backtracking**: Deduce omitted business logic from end-user failure modes and edge cases.
2. **Exception Path Tracing**: Trace unhandled error states, incomplete try/catch blocks, and missing error code propagation.
3. **Threat & Security Modeling**: Verify input sanitization, authentication/authorization guardrails, and sensitive data encryption from an attacker's perspective.
4. **Performance & Resource Bottlenecks**: Inspect hot paths for memory leaks, unindexed queries, blocking I/O, and race conditions.

---

## Remediation & Production Adaptation Standards

When generating or applying fixes:
- **Eliminate Hardcoded Stubs**: Replace simulated mocks with real system calls, environment variables, or verified data sources.
- **Defensive Parameter Validation**: Implement strict boundary checks, nullability guards, and schema validators.
- **Resource Leak Elimination**: Ensure file descriptors, database connections, and network sockets close deterministically.
- **Unified Error Handling**: Establish structured error codes and contextual error logging.
- **Data Consistency & Concurrency**: Apply optimistic/pessimistic locking, atomic operations, and idempotency keys.

---

## Structured Output Template

```markdown
# Multi-Dimensional Audit & Remediation Report

## 1. Spatial Architecture Findings (空间维度)
- **Topology & Layer Boundaries**: [Pass | Finding]
- **Import & Module Graph**: [Pass | Finding]
- **Environment & Config Match**: [Pass | Finding]

## 2. Solid Data-Flow Findings (立体维度)
- **End-to-End Tracing**: [Pass | Finding]
- **Database & Transactional Integrity**: [Pass | Finding]
- **Cache & Async Processing**: [Pass | Finding]

## 3. Reverse Threat & Edge Case Findings (逆向维度)
- **Omitted Business Edge Cases**: [Pass | Finding]
- **Exception Chains & Error Handling**: [Pass | Finding]
- **Security & Vulnerability Exposure**: [Pass | Finding]
- **Performance & Concurrency Hazards**: [Pass | Finding]

## 4. Prioritized Remediation Plan
| ID | Dimension | Severity | Location | Issue Summary | Recommended Surgical Fix |
|---|---|---|---|---|---|
| FIX-1 | Spatial | High | `path/file.ext:line` | Circular dependency | Extract shared interface |

## 5. Verification Commands
- `<executable validation command>`
```

## Checkable Completion Criteria

- [ ] Spatial, solid, and reverse dimensions fully audited.
- [ ] All findings backed by real codebase evidence and file line references.
- [ ] Remediation plan replaces mock data with verified production patterns.
- [ ] Verification command confirmed against real test tooling.