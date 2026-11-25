---
name: production-ai-saas-builder
description: Build a production-ready AI tool or multi-tenant SaaS end to end, from problem definition through architecture, implementation, verification, deployment, and launch operations. Use for AI products, copilots, RAG applications, agentic workflows, paid web apps, MVPs that must be safely productionized, and SaaS modernization; require authorization before accessing services or deploying.
---

# Production AI SaaS Builder

Turn a business problem into a working, secure, observable, cost-controlled product. Produce code and artifacts only after the acceptance criteria and delivery constraints are clear. Apply the shared [OutcomeLab skill standard](../../docs/SKILL-STANDARD.md).

## Required intake

Collect or explicitly assume: target user and job, business outcome, acceptance criteria, budget/runway, timeline, legal geography, data classes, existing code/designs, team skills, cloud and model constraints, integrations, expected volume, SLOs, deployment authority, and launch owner. Ask only questions that change architecture, safety, scope, or cost. If details are missing, write a short assumption register and build the smallest reversible slice.

## Delivery contract

Do not stop at a plan. Deliver the artifacts appropriate to the authorized scope:

1. Product brief: ICP, job, user journey, non-goals, pricing hypothesis, success metric, and acceptance criteria.
2. Technical design: architecture, data flow, trust boundaries, ADRs, API/schema contracts, tenancy model, and failure behavior.
3. Working implementation: repo structure, frontend, backend, auth, persistence, background work, model integration, tests, environment examples, and local run instructions.
4. Production operations: CI, migrations, secrets handling, logging/metrics/tracing, alerts, dashboards, rate limits, backups, retention/deletion, incident and rollback runbooks.
5. Launch packet: threat model, cost model, evaluation results, release checklist, analytics events, support/feedback route, and post-launch review date.

When a requested artifact is unsafe or requires unavailable credentials, create a reviewed interface, mock, migration, or deployment plan instead of pretending it was executed.

## Operating framework

### 1. Frame the product

Write a one-page product brief. Convert vague ambition into user-visible outcomes and testable acceptance criteria. Choose an MVP that validates the riskiest assumption; defer features that do not affect the first paid or retained user.

### 2. Choose a boring-enough architecture

Start with a modular monolith unless independent scaling, isolation, or ownership evidence justifies distributed services. Select stack, database, queue, storage, model provider, and hosting by constraints—not popularity. Define boundaries for UI, API, domain logic, worker, integrations, and AI gateway. Record why each irreversible choice is safe enough now.

### 3. Design the AI subsystem

Define the task, model contract, prompt/version ownership, tool permissions, context assembly, output schema, fallback, latency and token budget. For RAG, define corpus authority, ingestion, chunking, metadata/tenant filters, retrieval evaluation, citations, refresh, and deletion. For agents, constrain tools with least privilege, confirmations for consequential actions, timeouts, idempotency, loop/cost caps, and auditable traces. Treat model output as untrusted input.

### 4. Build the SaaS foundation

Implement identity and organization membership before user data; enforce authorization on every data access. Put tenant ID in the authoritative query boundary, not only the UI. Define billing entitlement separately from payment callbacks. Use transactions, idempotency keys, dead-letter/retry policy, and schema validation around external events. Keep secrets server-side and configuration typed and validated at boot.

### 5. Make it operable

Add structured logs without sensitive content, request/trace IDs, product and reliability metrics, health checks, alerts, runbooks, and ownership. Model cost per successful task, customer, and model call. Add hard usage caps and graceful degradation before usage scales. Practice restore, failed deployment, and provider-outage paths.

### 6. Verify before release

Run type/lint/build checks; unit, integration, authorization, migration, and end-to-end tests; dependency/secret scanning; load tests for known critical paths; and AI task evaluations covering ordinary, adversarial, refusal, and degraded-provider cases. Verify accessibility, mobile behavior, privacy controls, legal copy, analytics consent, and support flow. Do not mark production-ready solely because the happy path works locally.

### 7. Release safely

Use preview environments, reviewed migrations, feature flags, staged rollout, telemetry gates, and an owner on call. Define explicit abort/rollback conditions. After launch, compare real behavior, cost, latency, reliability, and user outcome with pre-launch assumptions; create the next smallest improvement.

## Quality gates

- Every feature has an acceptance test and an observable product or operational signal.
- Every external input, model response, webhook, and tool call is authenticated/validated/authorized at its boundary.
- Every tenant-scoped query and object-store key is isolation-tested.
- Every stateful release has backup, migration, rollback, and owner evidence.
- Every AI capability has a task-specific evaluation set, prompt/model version, cost ceiling, timeout, and fallback behavior.
- Every production secret is absent from source, logs, client bundles, fixtures, and public examples.
- Every release has a measurable release criterion, monitoring window, and reversal path.

## Failure detection and risk controls

Flag and halt for missing authorization, unclassified sensitive data, undefined tenant model, unbounded model/tool loops, no rollback for destructive change, no evaluation for a user-facing AI claim, or a launch without operational ownership. Do not claim compliance certification, security approval, availability, model accuracy, or deployment completion without corresponding evidence. Escalate payment, healthcare, legal, safety-critical, biometric, or regulated-data decisions to qualified humans.

## Output format

Return: (1) status and assumptions, (2) prioritized delivery plan, (3) architecture/ADR, (4) implementation changes and commands actually run, (5) test/evaluation evidence, (6) risk register and unresolved decisions, (7) release checklist/rollback plan, and (8) next owner/action. Keep confirmed facts, estimates, and recommendations separate.

## Benchmark and improvement

Compare against a generic “build me a SaaS” result on requirement traceability, tenant/security coverage, AI evaluation, test coverage, deployability, operational readiness, cost controls, and calibration. Success is a user-validated workflow released with passed gates and no unaccepted critical risk. Feed incidents, support tickets, failed evaluations, and cost surprises back into the requirements, tests, and architecture.

## Reference

Read [production-checklist.md](references/production-checklist.md) before declaring a project launch-ready.

