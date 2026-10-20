---
name: archproof-audit
description: Audit architecture claims against repository and runtime evidence for backend, distributed, event-driven, real-time, and AI-enabled systems. Use when reviewing a course project, architecture report, production-readiness plan, microservice migration, incident repair, or performance claim that must prove trust boundaries, data consistency, cache and MQ behavior, idempotency, failure recovery, LLM governance, deployment reproducibility, high availability, or scaling. Produces traceability, defect findings, evidence passports, test plans, and qualified conclusions without inventing results.
---

# ArchProof Architecture Evidence Audit

Use requirements, repository evidence, runtime state, and failure experiments to check whether architecture claims survive concurrency, duplication, partial failure, and recovery. Treat framework presence and successful happy-path requests as candidate evidence only. Spend most effort on ownership and state transitions across trust boundaries, caches, messages, databases, real-time delivery, and external AI calls.

## Select the audit mode

1. For a course or acceptance audit, read the assignment, scoring rules, selected scope, submission checklist, and report. Read [references/course-project-profile.md](references/course-project-profile.md) only when the rubric resembles a Web backend course project.
2. For a product architecture audit, read requirements, ADRs, API contracts, data ownership, SLOs, deployment manifests, and incident history.
3. For production readiness, add capacity assumptions, fault domains, observability, recovery objectives, secret handling, and rollback procedures.
4. For a defect investigation, begin with the failing request, violated invariant, state transition, and regression test.

## Start from requirements

1. Read the authoritative requirements, README, architecture decisions, deployment files, API collections, migrations, tests, and raw outputs.
2. Separate functional requirements, architectural invariants, operational evidence, and future design.
3. Mark the agreed scope and any optional prototypes. Keep local measurements separate from planned production behavior.
4. Record unknown information and placeholders. Never infer a test result, deployment state, team member, credential, capacity number, or performance result.

Read [references/architecture-checklist.md](references/architecture-checklist.md) when the task covers concurrency, messaging, real-time communication, AI, or production evolution. Keep assignment-specific component counts and deliverables in a profile rather than treating them as universal architecture rules.

## Build an evidence map before judging

Run the repository scanner when the project is unfamiliar:

```bash
python <skill-dir>/scripts/collect_architecture_evidence.py --root . --format markdown
```

The scanner returns candidate files, source kinds, and matching lines. A match proves only that a term exists. Open the implementation, configuration, migration, and test before marking a requirement complete. Use repeated `--exclude` arguments for generated or project-specific directories.

For every important claim, record:

1. Requirement and business consequence.
2. Service, API, and key class or function.
3. Database table, index, or transaction boundary.
4. Redis key and atomic operation.
5. MQ exchange, queue, routing, confirm, ACK, retry, and DLQ behavior.
6. Automated test, API collection step, log, database query, or raw performance file.
7. Status: implemented and tested, implemented but not tested, design only, contradicted, or missing.

Use the schema in [references/evidence-passport.md](references/evidence-passport.md) for reports and traceability files.

## Audit the running architecture

### Gateway and identity

Verify that client traffic uses the Gateway, public routes do not expose internal endpoints, external identity headers are removed, JWT verification happens at a trusted boundary, logout invalidates the old token, and role assignment cannot be chosen during public registration. Test horizontal access to another user's resource.

### Redis and concurrency

Write the business invariants before reading the code. For inventory reservations such as flash sales, include non-negative stock, per-user limits, one accepted qualification per permitted unit, and stock conservation. Confirm that one Lua execution performs every decision that must be atomic. Check Cluster hash tags when a script accesses multiple keys. Inspect cold-start and data-loss recovery; rebuilding stock from a stale initial value can resell completed orders.

For rankings and rate limits, verify the actual ZSET score formula, duplicate-view policy, concurrent-like behavior, rule refresh mechanism, TTL, and 429 evidence. Do not mark a dependency as implemented merely because its library is present.

### MQ and database consistency

Trace one message from the local transaction to final acknowledgement. Locate Outbox creation, publisher confirm, retry state, consumer transaction, unique constraint, ACK timing, and DLQ behavior. Simulate or test at least publisher unavailability, duplicate delivery, database failure, consumer restart, and poison messages.

Reject compensation triggered by a notification failure after the business transaction has committed. A failed WebSocket or SSE connection changes delivery state, not the database fact.

### LLM and real-time communication

Check model configuration through environment variables or secret management. Verify timeouts, concurrency limits, rate-limit handling, queueing, cache versioning, prompt-injection boundaries, read-only tool allowlists, source attribution, and explicit fallback behavior. Distinguish mock output from a real provider response.

For WebSocket and SSE, identify the durable fact source, authentication, connection loss behavior, completion event, reconnect or query fallback, and multi-instance delivery mechanism. Do not promise exactly-once push delivery.

## Diagnose structural defects

Use this order:

1. Reproduce the behavior with a minimal request or test.
2. State the violated invariant.
3. Trace ownership across service, cache, queue, and database boundaries.
4. Find the first state transition that becomes ambiguous or irreversible.
5. Fix the ownership or transaction boundary before adding retries or catches.
6. Add a regression test for the original failure and the compensation path.
7. Re-run the complete core flow and reconcile final state.

Avoid broad exception handling, silent mock fallback, parallel implementations, and duplicated security checks. Prefer database uniqueness, explicit state machines, idempotent consumers, and visible failure states.

## Verify performance claims

Preserve the load tool script, environment, concurrency, request count, data distribution, raw JSON or CSV, and database reconciliation query. Report throughput, success classes, transport errors, P50, P95, P99, and resource conditions. Explain whether business rejections such as sold-out or duplicate purchase are expected results.

For stock, calculate and verify a conservation relation such as:

```text
initial stock = remaining Redis stock + accepted qualifications
accepted qualifications = durable orders + pending Outbox + known compensations in progress
```

Adjust the equation to the implementation. Do not claim zero oversell from HTTP success counts alone.

## Review the report

Organize the main report around architecture evidence. Keep ordinary CRUD in a compact matrix. For each important choice, explain the business problem, chosen boundary, implementation, measured evidence, failure consequence, and tradeoff in normal prose.

Separate local measurements from production design. Production evolution should cover stateless service replicas, Gateway clustering, MySQL replication and failover, Redis Sentinel or Cluster, durable MQ clustering, autoscaling signals, overload protection, observability, secret management, and LLM queueing and cache governance. Label Kubernetes, KEDA, and multi-zone deployment as design when they were not run locally.

Before delivery, compile the report, render every page, search for placeholders and unsupported claims, and check the contents, ER diagrams, sequence diagrams, page references, tables, and figures.

## Required output

Return these sections when auditing a project:

1. Overall assessment with separate scores for basic functions, core architecture, evidence, and production design.
2. Requirement matrix with implementation and evidence status.
3. Defects ordered by severity and business consequence.
4. Evidence passports for the main highlights.
5. Repair plan with exact files, tests, and expected state changes.
6. Claims that must remain qualified or marked as design only.

Stop when the evidence is sufficient for the requested decision. Do not expand the project with unrelated features.
