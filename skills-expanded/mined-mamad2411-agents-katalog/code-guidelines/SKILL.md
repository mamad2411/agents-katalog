---
name: code-guidelines
description: Use this skill for any substantive software-engineering task involving design, implementation, debugging, review, refactoring, testing, build or configuration changes, HTTP APIs, persistence, security boundaries, concurrency or parallelism, Java, Kotlin, or JVM systems. Load it even when the user asks for a small fix, root-cause analysis, performance change, async or background work, thread-safety review, coroutine change, database migration, or repository convention decision; use the relevant reference guides and base conclusions on verified repository evidence.
---

# Code Guidelines

Use this skill for code analysis, feature implementation, bug investigation, code review, refactoring, testing, API and persistence design, security-sensitive engineering, concurrency, observability, and Java/Kotlin/JVM work.

The goal is to produce the smallest correct change supported by evidence and consistent with the repository's verified contracts, architecture, and engineering requirements.

## 1. Normative Model

The keywords **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** in this skill and its reference guidelines are to be interpreted as described in BCP 14, RFC 2119 and RFC 8174, when and only when they appear in all capitals.

| Term | Meaning |
|---|---|
| **MUST** / **REQUIRED** | Mandatory whenever the rule applies. |
| **MUST NOT** | Prohibited whenever the rule applies. |
| **SHOULD** / **RECOMMENDED** | Default engineering decision. Deviation requires a concrete, evidence-supported reason. |
| **SHOULD NOT** | Avoid by default. Deviation requires a concrete, evidence-supported reason. |
| **MAY** / **OPTIONAL** | Permitted but not required. |
| **TRIGGER** | Observable condition that makes a conditional rule applicable. |
| **EXCEPTION** | Explicit, narrowly scoped condition that relaxes or disables an otherwise applicable rule. |

A **SHOULD** or **SHOULD NOT** MUST NOT be treated as an unconditional requirement. Deviation MAY occur only when supported by repository evidence, an explicit requirement, a verified technical constraint, or a clearly identified tradeoff. Convenience, speculation, preference, and hypothetical future requirements are not sufficient justification.

For a conditional rule:

1. Establish whether its **TRIGGER** is satisfied by evidence.
2. If the trigger is not established, the rule MUST NOT be activated automatically.
3. If the trigger is established, its normative requirements MUST be enforced.
4. An **EXCEPTION** MAY be applied only when every condition stated by that exception is satisfied.

Missing information establishes neither a trigger nor an exception.

An **EXCEPTION** MUST be explicit, address a concrete requirement or constraint, be scoped to the smallest affected behavior, preserve unrelated requirements, and remain distinguishable from normal behavior. A generic environment or mode MUST NOT automatically disable unrelated engineering or security requirements.

## 2. Rule Application

`references/engineering-guidelines.md` MUST be applied to every coding task.

`references/testing-guidelines.md` MUST be applied when a task introduces, changes, reviews, or diagnoses tests, test fixtures, test configuration, verification strategy, flaky test behavior, or a material behavior change requires nontrivial verification.

`references/security-guidelines.md` MUST be applied when a task changes or introduces a trust boundary or security-sensitive behavior, including authentication, authorization, credentials, externally controlled input, externally reachable APIs, server-side network access, files, serialization, dynamic execution, cryptography, sensitive data, privileged operations, dependencies, build security, artifact integrity, or deployment security.

`references/rest-api-guidelines.md` MUST be applied when a task introduces, changes, reviews, or diagnoses an HTTP API contract, including resource design, URI structure, HTTP methods, request or response models, status codes, errors, collections, filtering, pagination, idempotency, compatibility, or API evolution.

`references/database-guidelines.md` MUST be applied when a task introduces, changes, reviews, or diagnoses persistence behavior, including data modeling, schema design, persistence models, migrations, queries, indexes, transactions, concurrency, or data lifecycle.

`references/concurrency-guidelines.md` MUST be applied when a task introduces, changes, reviews, or diagnoses concurrent or asynchronous execution, including threads, executors, pools, futures, promises, locks, atomics, concurrent collections, coroutines, reactive pipelines, parallel processing, scheduled work, background jobs, message redelivery, cancellation, races, deadlocks, starvation, or shared mutable state.

`references/java-guidelines.md` MUST be applied when Java, Kotlin, or related JVM technologies are involved.

`references/observability-guidelines.md` MUST be applied when a task introduces, changes, reviews, or diagnoses logging, metrics, tracing, health checks, readiness, startup, shutdown, runtime configuration, feature flags, alerts, or other operational behavior.

`references/project-guidelines.md` MUST be applied when discovering, establishing, evaluating, or modifying repository-specific engineering rules.

Multiple applicable references MUST be applied together. The more specific applicable rule refines the general rule; it does not silently disable other applicable references. Repository-specific rules MUST be established from project evidence rather than inferred from a single implementation. Existing insecure or incorrect behavior MUST NOT be treated as sufficient justification to weaken a general correctness or security requirement.

Each substantive requirement SHOULD have one owning reference. A specialized reference MAY restate a general requirement only to express a boundary-specific consequence, trigger, or language/runtime mapping; otherwise it SHOULD link to the owning reference. Overlapping rules MUST be reconciled so that specialization refines the general requirement rather than creating a second, potentially divergent definition.

Language and runtime API rules MUST live in the applicable language/runtime reference. Generic references MUST use language-neutral concepts or examples and MUST NOT prescribe a language's syntax, standard-library API, or framework mechanism. Project-specific language conventions belong in `project-guidelines.md`; the current Java, Kotlin, and JVM language/runtime layer is `references/java-guidelines.md`.

Reference files SHOULD be loaded only when their trigger applies. An untriggered reference MUST NOT be used to manufacture requirements or expand a focused task's scope.

### Evidence

Engineering conclusions MUST be supported by available evidence. Relevant evidence includes source code and actual definitions, callers and callees, tests and runtime behavior, build and analysis configuration, framework configuration, schemas and public contracts, logs and reproducible failures, repository documentation, and multiple consistent current implementations.

Verified facts MUST be distinguished from assumptions. An unverified assumption MUST NOT be presented as a confirmed root cause, contract, security property, performance characteristic, or project convention.

**TRIGGER:** A material engineering decision depends on information that is not yet established.

- Available code, configuration, tests, definitions, documentation, and runtime evidence MUST be inspected before the missing fact is assumed.
- If the fact can be established from available evidence, it MUST be established before the material decision is made.
- If the fact cannot be established, it MUST remain explicitly unverified rather than being invented.

### Change Decision Gate

Before introducing any of the following, the stated present-day justification MUST be established:

| Change | Required justification |
|---|---|
| New abstraction or interface | Real variation point, architectural boundary, meaningful decoupling, or duplicated knowledge |
| New dependency | Existing stack cannot adequately satisfy the requirement |
| Compatibility behavior | Verified consumer, persisted data, protocol, or explicit compatibility requirement |
| Fallback or degradation | Verified failure mode and defined fallback semantics |
| Retry | Verified retryable failure and safe or idempotent execution |
| Public API | Actual consumer or explicit contract |
| Security exception | Applicable explicit **EXCEPTION** with all conditions satisfied |
| Performance optimization | Requirement, expected scale, profiling, benchmark, or runtime evidence |

Hypothetical future requirements MUST NOT justify additional architecture.

## 3. Engineering Workflow

Before making a material behavior-changing decision, the following MUST be established or inspected as applicable:

1. The requested behavior and affected scope.
2. The affected language, framework, module, boundary, and contract.
3. The applicable reference guidelines.
4. Relevant repository-specific engineering rules and configuration.
5. The affected implementation and actual API or type definitions.
6. Relevant callers, callees, tests, and analogous implementations.
7. Verified facts and remaining assumptions.
8. The smallest change that satisfies the verified requirement.

If an unresolved interpretation could affect destructive operations, money, permissions, security, persistent data, a public contract, or concurrency semantics, the ambiguity MUST be resolved before implementation. For lower-impact ambiguity, state the assumption and choose the smallest reversible path.

Unfamiliar external APIs MUST be verified from authoritative documentation, dependency source, or established project usage before introduction. Internal methods MUST be inspected at their actual definition before their behavior or signature is assumed.

Changes MUST remain focused on the requested engineering scope. Unrelated cleanup, formatting, modernization, or refactoring MUST NOT be included merely because an issue was discovered nearby.

## 4. Task Workflows

### Bug Investigation

A bug investigation MUST:

1. Establish the observed incorrect behavior.
2. Reproduce it when a practical reproduction path exists.
3. Trace the actual execution path.
4. Gather evidence.
5. Form a falsifiable root-cause hypothesis.
6. Verify the hypothesis before declaring the root cause.
7. Establish the violated contract.
8. Fix the verified cause with the smallest scoped change.
9. Re-run the reported scenario and relevant tests.

Suspicious-looking code, correlation, or an untested hypothesis MUST NOT be reported as a confirmed root cause. A callee contract MUST NOT be broadened, validation weakened, or fallback behavior introduced merely because one caller violates an established contract.

### Feature Implementation

Feature design MUST establish the owning domain concept, responsible component, affected contract, closest existing implementation, and existing extension point when one exists.

Existing abstractions SHOULD be reused when they correctly represent the required behavior. A new abstraction MUST have a concrete present-day responsibility, boundary, variation point, decoupling benefit, or duplicated knowledge to justify it. Public API surface MUST be limited to actual consumers and verified contracts.

### Refactoring

Refactoring MUST have a concrete motivation such as duplicated business knowledge, misplaced responsibility, excessive coupling, a violated dependency boundary, or demonstrated cognitive complexity.

Externally observable behavior MUST remain unchanged unless behavior change is part of the verified requirement. Refactoring MUST NOT introduce parallel replacement variants such as `XxxV2`, `newXxx()`, or `XxxImpl2` instead of replacing obsolete behavior.

Patterns, stylistic preference, arbitrary metrics, or hypothetical extensibility MUST NOT be sufficient reasons for refactoring.

### Code Review

Review findings MUST be evidence based and prioritized by impact:

1. Correctness and data integrity.
2. Security, authentication, authorization, and trust-boundary violations.
3. Concurrency and resource safety.
4. Contract and compatibility correctness.
5. Missing or insufficient tests and verification.
6. Responsibility and dependency boundaries.
7. Maintainability.
8. Performance problems supported by evidence.

Code smells are investigation signals, not automatic defects. A substantive finding MUST identify concrete evidence and explain the actual or likely impact.

### Security-Sensitive Changes

**TRIGGER:** `references/security-guidelines.md` applies to the affected behavior.

- The relevant trust boundary, protected asset or operation, untrusted actor or input, and security property MUST be identified.
- Existing framework or infrastructure controls MUST be verified before they are relied upon or duplicated.
- Applicable security **TRIGGER**, requirement, and **EXCEPTION** rules MUST be evaluated from evidence.
- Relevant allowed behavior and denied or failure behavior MUST be verified.

Following a guideline or passing tests MUST NOT be presented as proof that an implementation is comprehensively secure.

## 5. Completion Report

For implementation, debugging, review, refactoring, or design work, the final report SHOULD state:

- what changed or was concluded;
- why the change or conclusion follows from the evidence;
- the affected scope and applicable references;
- what verification ran and its result;
- relevant limitations, remaining assumptions, or unverified behavior.

Do not claim runtime, performance, security, compatibility, or concurrency properties that were not established by the available evidence.

## 6. Verification

Code changes MUST be verified before they are considered complete.

Verification MUST include the most focused relevant tests. Broader regression, build, compiler, static-analysis, or runtime checks SHOULD be included when required by the affected boundary. Failures MUST be investigated before being classified as unrelated.

**TRIGGER:** An existing test fails after a production change.

- The failure MUST first be classified as incorrect production behavior, an incorrect test, an intentionally changed contract, or explicitly unresolved.
- The test MUST NOT be changed merely to make the implementation pass.

The final change set MUST be inspected for accidental or unrelated modifications. Temporary debugging output, placeholders, incomplete TODOs, and other intermediate implementation artifacts MUST NOT remain in completed code.

Security-sensitive changes MUST verify relevant failure paths in addition to successful behavior.

Verification that cannot be performed MUST remain explicitly unverified rather than being inferred from inspection alone.
