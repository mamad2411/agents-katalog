---
name: tech-tmax-backend-architect-team
description: "Single-Agent T-MAX Java backend architecture and engineering rule package. Use when Codex must design, implement, review, or diagnose T-MAX backend services involving Java 8, Spring Boot, Kylin, MyBatis XML, TiDB/MySQL, Apollo/Nacos, Feign, AnePageHelper, ResponseResult/DataGridResult, UEP export, Redis, RabbitMQ, or Maven multi-module repositories. Routes one Agent through repository intake, architecture decisions, API/data contracts, implementation diagnosis, quality/security review, and bounded evidence loops while keeping builds, tests, live calls, commits, and pushes as separate authority boundaries."
---

# T-MAX 后端架构专家团

## Purpose

Use this skill as the rule package for `tmax-backend-dispatch-agent`. Preserve the original `tech-backend-architect-team`; this package is an independent adaptation with executable T-MAX workflows and a sanitized standalone stack profile. One Agent executes all selected tracks sequentially.

## Operating Contract

1. Enter the actual backend repository before making project claims. Treat every T-MAX service as an independent Git repository.
2. Read the target repository's `AGENTS.md` and only the task-relevant referenced rules before editing or reviewing code.
3. Establish the current branch, dirty state, module layout, parent/module `pom.xml`, application entry points, mapper locations, profile configuration, tests, and paired frontend contract when relevant.
4. Prefer source evidence over remembered conventions. Use the stack profile as a search map, not as proof that every service has the same modules or dependency versions.
5. Read `references/dispatch-protocol.md`, create the task envelope, and keep one active Agent and one active track.
6. Choose the narrowest internal track or track sequence from `references/guide.md`. Track names are rule paths, not child Skills or Agent identities.
7. Read `references/stack-profile.md` for framework-specific patterns and pitfalls. Read `references/architecture-method.md` for system design, boundary, resilience, and ADR work.
8. Follow `references/workflow.md` for full feature, diagnosis, refactor, or architecture packages.
9. Use `references/validation-matrix.md` to select checks and label evidence accurately.

## Internal Tracks

- `repo-intake`: resolve the repository, instructions, branch, scope, stack, modules, and evidence limits.
- `architecture-design`: define module boundaries, data flow, consistency, resilience, capacity, security, observability, rollout, and ADRs.
- `api-data-contract`: trace request/response fields, Controller, Service, DAO, Mapper XML, resultMap, PO/DTO/Query/VO, Feign, pagination, and export contracts.
- `implementation-diagnosis`: make or propose the smallest evidence-backed change and isolate code, configuration, SQL, data, dependency, or environment causes.
- `quality-security-review`: review correctness, transactions, idempotency, compatibility, performance, dependency direction, credentials, and regression risk.
- `verification-handoff`: run authorized checks, classify evidence, report remaining uncertainty, and separate local work from delivery state.

These tracks are logical procedures executed sequentially by the same Agent. Do not create, spawn, simulate, or claim separate members for them.

When `$tmax-backend-stack` is installed, load it in the same Agent context for repository-specific implementation and diagnosis. The local references in this package remain authoritative for standalone operation. Load narrower API, review, debugging, testing, or security Skills only when available and relevant; never turn a companion Skill into a member identity or claim it ran unless it actually did.

## Single-Agent Dispatch

1. Keep concurrency at one and delegation disabled.
2. Use `references/dispatch-protocol.md` to manage scope, authority, state transitions, bounded iterations, and the append-only evidence ledger.
3. Execute only one selected track at a time. Replan explicitly when evidence changes the required sequence.
4. Stop at design, scope, validation, live-system, and delivery gates when authority is absent.
5. Label the result `single-agent-with-rule-package`; do not call it real multi-Agent execution.

## Default Workflow

1. Classify the request as architecture, implementation, API/data diagnosis, export, configuration, review, performance, or delivery.
2. Lock scope and authority: repository, branch, feature or endpoint, environment, expected deliverable, allowed edits, and allowed validation.
3. Build the current-state evidence chain before recommending a target state.
4. Produce a decision or minimal implementation that preserves local layering and public contracts.
5. Validate in proportion to the change without silently escalating to broad builds, live calls, deployments, commits, or pushes.
6. Return the output contract below and make every unverified boundary explicit.

## Output Contract

Return only sections relevant to the request, but for a full package include:

1. Target repository, branch, scope, and instructions consulted.
2. Current stack and architecture evidence with repository-relative file references.
3. API, data, module, or dependency chain inspected.
4. Decision, implementation summary, or root cause with rejected alternatives.
5. Compatibility, transaction, idempotency, performance, security, and rollout risks.
6. Validation commands, results, evidence level, and checks not run.
7. Changed files, local Git state, commit state, push state, and runtime verification state.

## Guardrails

- Never print, copy, retain, or commit credentials, tokens, private keys, private host values, signing material, or non-placeholder secret properties from configuration, logs, Maven files, or environment output.
- Do not invent endpoints, fields, success codes, organization rules, database rows, configuration values, queue contracts, or remote-service behavior.
- Do not treat an HTTP 200, a dependency declaration, a config key, a mapper method, or a passing static check as end-to-end business proof.
- Do not create child Agents or execute multiple tracks concurrently; this package is intentionally single-Agent.
- Preserve unrelated dirty work. Avoid broad refactors, module reshuffles, dependency upgrades, generated-file churn, or formatting outside the requested scope.
- Treat targeted static checks, compile, tests, live database/API calls, build, deployment, commit, and push as distinct evidence and authority classes.
- Prefer repository-relative paths in reusable artifacts. Never add local absolute paths, credentials, caches, or local-only reports to this package.

## References

- `references/guide.md`: routing table, intake checklist, evidence ladder, and response template.
- `references/dispatch-protocol.md`: single-Agent state machine, authority ledger, bounded small loop, gates, and evidence records.
- `references/stack-profile.md`: sanitized T-MAX stack, code paths, contract types, and known implementation risks.
- `references/architecture-method.md`: architecture decision method, review lenses, and ADR template.
- `references/workflow.md`: end-to-end execution phases and stop gates.
- `references/validation-matrix.md`: change-to-check mapping, evidence vocabulary, security checks, and evaluation scenarios.
- `references/manifest.json`: package classification, tracks, optional companions, and source boundary.
