---
name: swe-router
description: Technical concern router for software engineering work. Identifies which domain-specific skills to load based on task signals — covering modularity, anti-patterns, reuse, testability, security, performance, concurrency, architecture, data/API design, resilience, observability, deployment, scoping, debugging methodology, incident response, frontend engineering, and AI collaboration. Use when designing systems, reviewing code, debugging, making architecture decisions, handling production issues, or any substantive engineering work. Does not cover process steps (use /understand, /plan, /implement, /debug, /review for those) or issue/branch flow (use issue-branch-orchestrator).
---

# SWE Technical Concern Router

Loads first on substantive engineering work. Identifies which domain skills are relevant and in what order. Does not replace process commands — it routes to technical knowledge those commands don't carry.

## Hard rules (always apply, regardless of domain)

These are non-negotiable. They are the anti-hallucination layer.

**Verify before asserting.** Never claim a function, method, CLI flag, file path, environment variable, schema field, or package version exists without confirming it. If you cannot verify, state the assumption explicitly:
> "Assumption: I have not confirmed that `X` exists. Verify before using."

**Separate facts from assumptions.** In any non-trivial output, distinguish:
- Observed — directly read from code, config, logs, or output
- Assumed — inferred without direct evidence
- Unknown — cannot be determined without further inspection

**State the unknown rather than guess.** When the correct value is unclear: name it as unknown, suggest how to verify, do not fill the gap with a plausible-sounding value.

**Stop before destructive or irreversible actions.** Do not proceed with deleting files, dropping tables, force-pushing, resetting state, or adding new external dependencies without surfacing the action and its consequences first.

**The 70% problem.** Agents complete the happy path. What is consistently missing: error handling, timeouts, idempotency, observability, edge cases, and failure modes. Before declaring any implementation complete, ask: what happens when this fails? Is there a timeout? Is the error observable? Is a retry safe?

**Hypothesise before changing code in debugging.** When investigating a bug, every change must test a specific hypothesis. Multiple changes without verifying each is the most common debugging anti-pattern.

## Domain routing

Load the relevant skill(s) based on task signals. Multiple skills may apply.

### Scope and design

**scoping-discipline** — PoC vs MVP vs production decisions, technical debt management, requirements ambiguity resolution, estimation. Load when: asked to "just make it work", scoping a first version, deciding what to cut, evaluating whether a prototype is ready to promote, given a vague requirement.

**architecture-selection** — Architecture style trade-offs, decision rubric, ADRs and RFCs, cost as architectural constraint. Load when: starting a new system, deciding monolith vs. microservices, choosing between styles, writing a design doc, evaluating cost implications of an architectural choice.

**modularity** — Coupling, cohesion, structural dependency signals, naming, abstraction depth (deep vs. shallow modules), information hiding. Load when: designing or reviewing module/class boundaries, naming things, evaluating whether an abstraction is shallow or deep, investigating why changes ripple.

**reuse-and-patterns** — GoF pattern signals (signal + overkill-when), reuse strategy trade-offs. Load when: deciding between library and build, evaluating whether a design pattern applies, designing for variation.

**data-and-api-design** — Schema design, expand/contract migrations, backward compatibility, API versioning, idempotency. Load when: designing a schema or migration, designing an API endpoint, adding a field to an existing API, evaluating backward compatibility.

### Quality

**anti-patterns** — Code-level and architectural smells, refactoring discipline (refactor under test, small steps, Mikado method). Load when: reviewing code for structural problems, planning or executing a refactor, noticing a class or module is doing too much.

**testability** — Controllability/Observability/Isolation as design properties, test smells, design-for-testability moves. Load when: code is difficult to test, designing new code that needs a test suite, reviewing why tests are slow or brittle.

**performance-engineering** — Measure-before-optimise, complexity signals, caching, capacity planning, load/stress/soak testing. Load when: investigating slow code, choosing data structures for a hot path, designing caching, sizing infrastructure for expected load.

**concurrency** — Race condition signals, async/await correctness, the concurrency testing gap. Load when: writing multi-threaded or async code, debugging non-deterministic failures, when behaviour differs under load vs. sequential tests.

### Safety

**security-engineering** — STRIDE, secure design principles, common vulnerabilities, compliance engineering (PII in logs, audit trails, data retention, encryption at rest). Load when: designing auth flows, handling user input, identifying trust boundaries, designing audit trails, implementing data retention or right-to-erasure.

**resilience-engineering** — Timeout, retry+backoff+jitter, circuit breaker, bulkhead, graceful degradation, partial failure. Load when: writing code that calls external services, designing retry logic, debugging cascading failures.

### Production

**observability** — Structured logging, logs vs. metrics vs. traces, cardinality, four golden signals, SLO design and error budget management. Load when: writing code that will run in production, adding error handling, diagnosing why a production failure is hard to debug, designing alerts.

**source-to-deployment** — CI/CD pipeline patterns, container signals, deployment strategies, IaC, dependency and supply chain management. Load when: setting up CI/CD, containerising an application, designing a deployment strategy, evaluating a new dependency.

**incident-response** — Severity triage, mitigation vs. fix decisions, blameless postmortems, runbook design. Load when: a production system is broken right now, triaging a page, deciding rollback vs. fix-forward, writing or reviewing a postmortem, designing a runbook.

**debugging-methodology** — Hypothesis formation, bisection (git/code/data/config), reproduction discipline, production debugging. Load when: investigating any bug, when a fix is not converging after multiple attempts, when production behaves differently from local, when an agent has been editing the same file repeatedly without progress.

### Specialised

**frontend-engineering** — Render performance and Core Web Vitals, bundles and assets, CSS architecture, client-side state, accessibility. Load when: building or reviewing UI code, investigating Core Web Vitals, when bundle size is growing, when hydration mismatches appear, when CSS is bleeding across components.

**ai-collaboration** — Generation guardrails, AI for testing and requirements, ML system signals (training/serving skew, model rot, feedback loops). Load when: generating code with AI assistance, reviewing AI-generated code, building features where an ML model is the core product.

## Routing by task signal

| Task signal | Primary skill(s) | Also consider |
|---|---|---|
| "Review this code / PR" | `anti-patterns` | `modularity`, `testability`, `security-engineering` |
| "Refactor this class / module" | `anti-patterns`, `modularity` | `testability`, `reuse-and-patterns` |
| "Design auth / permissions" | `security-engineering` | `architecture-selection` |
| "Why is this slow?" | `performance-engineering` | `architecture-selection` (if systemic), `observability` |
| "Should we use microservices?" | `architecture-selection` | `source-to-deployment` |
| "Set up CI/CD" | `source-to-deployment` | `testability`, `observability` |
| "This is hard to test" | `testability` | `modularity`, `anti-patterns` |
| "Use a library or build it?" | `reuse-and-patterns` | `architecture-selection`, `source-to-deployment` (deps) |
| "Add an ML feature" | `ai-collaboration` | `security-engineering`, `data-and-api-design` |
| "Review AI-generated code" | `ai-collaboration` | `anti-patterns`, `testability`, `observability` |
| "Design a new system from scratch" | `architecture-selection` | `scoping-discipline`, `security-engineering`, `modularity`, `observability` |
| "Write a migration" | `data-and-api-design` | `source-to-deployment` |
| "Add a new API endpoint" | `data-and-api-design` | `security-engineering`, `observability`, `resilience-engineering` |
| "Is this PoC ready for production?" | `scoping-discipline` | `observability`, `resilience-engineering`, `incident-response` (runbook) |
| "Nothing in the logs / can't debug this" | `observability` | `debugging-methodology` |
| "Service goes down when dependency is slow" | `resilience-engineering` | `observability` |
| "Tests pass but prod fails sometimes" | `concurrency`, `debugging-methodology` | `testability` |
| "Production is broken right now" | `incident-response` | `observability`, `debugging-methodology` |
| "Write a postmortem" | `incident-response` | — |
| "Investigate this bug" | `debugging-methodology` | (domain-specific by symptom) |
| "Why is the page slow / large bundle / layout shift" | `frontend-engineering` | `performance-engineering` |
| "Add accessibility / keyboard support" | `frontend-engineering` | — |
| "Estimate this work / what's a good MVP" | `scoping-discipline` | — |
| "Make the case to pay down tech debt" | `scoping-discipline` (technical-debt) | `anti-patterns` |
| "Naming this feels off / abstraction is wrong" | `modularity` (naming-and-abstraction) | `reuse-and-patterns` |
| "Define SLOs / set up alerting" | `observability` (slo-design) | `incident-response` |
| "Add a new dependency" | `source-to-deployment` (dependency-management) | `security-engineering` |
| "Compliance / GDPR / audit logs" | `security-engineering` (compliance-engineering) | `observability` |
| "Write a design doc / RFC" | `architecture-selection` (design-docs) | — |
| "Capacity / load testing" | `performance-engineering` (capacity-and-load-testing) | `observability` |

## Process command cross-reference

- `/understand` — inspect context before any change
- `/plan` — produce a short implementation plan
- `/implement` — make the smallest useful change
- `/test` — write and run tests
- `/review` — critical review of a plan or diff
- `/debug` — root cause before fixing (for the *judgment* of debugging, load `debugging-methodology`)

Load domain skills to ground the *technical judgment* those phases require. The commands handle the *process*.
