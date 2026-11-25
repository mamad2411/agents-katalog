---
name: multi-perspective-review
description: Review an already implemented repository diff from budgeted expert perspectives after code changes are complete. Use when Codex needs post-implementation review before final verification, commit, PR, or handoff, especially when the user asks for senior engineer, senior architect, QA, performance, security, accessibility, migration, or multi-perspective review of a diff.
---

# Multi Perspective Review

## Goal

Review an implemented diff with the smallest set of expert perspectives that still covers the real risk. Use this skill after changes exist, not for planning or design approval before implementation.

The main agent owns final judgment, integration of reviewer feedback, and the user-facing report. Subagents provide independent review passes only when their perspective can materially reduce risk.

## Entry Gate

Use this skill only when there is an implemented change to review.

Before assigning reviewers, the main agent must inspect:

- the user request or approved plan that explains the intended behavior
- the current diff and touched files
- relevant tests, stories, fixtures, schemas, configs, or docs changed by the diff
- verification already run, if any
- dirty worktree state that may be unrelated to the review target

Do not edit files during the review unless the user also asked to fix findings. If the user only asked for review, report findings and stop.

## Classify Review Size

Classify by risk and behavioral concerns, not by raw file count.

- **Small / Low risk:** one primary concern, localized diff, established pattern, no high-risk domain.
- **Small / Normal risk:** localized diff with a meaningful edge case, stale assumption risk, or test gap risk.
- **Medium:** two or three concerns that can drift from each other, or one moderately complex behavior change.
- **Large / High risk:** four or more concerns, cross-system contracts, auth, permissions, security, payments, data migrations, irreversible data changes, scale-sensitive paths, or broad user-visible flows.

Record the classification and the reason before deciding the reviewer mix.

## Reviewer Budget

Review is mandatory. Subagent review is budgeted.

- **Small / Low risk:** main agent checklist review only. Do not call this skipped review.
- **Small / Normal risk:** at most 1 reviewer subagent for the one independent risk.
- **Medium:** 1-2 reviewer subagents. Avoid overlapping assignments.
- **Large / High risk:** 2 or more reviewer subagents with explicit ownership boundaries.

Use fewer subagents when the concerns are tightly coupled and the main agent can review them directly. Use more only when each reviewer has a distinct perspective that can find different failures.

## Standard Perspectives

Assign only the perspectives that match the diff.

- **Senior Engineer:** changeability, maintainability, module boundaries, naming, coupling, existing pattern drift, error handling, and whether the diff is simpler than the problem requires.
- **Senior Architect:** system structure, responsibility split, extensibility, integration boundaries, cross-module consistency, API or schema shape, and long-term ownership.
- **QA Engineer:** testability, missing test cases, regression scenarios, fixtures, mocks, acceptance criteria, and whether verification proves the intended behavior.
- **Performance Reviewer:** unnecessary recomputation, rendering churn, I/O, queries, network behavior, concurrency, memory, bundle size, and scale risks.

Add these only when the diff justifies them:

- **Security / Privacy Reviewer:** authorization, authentication, input validation, secrets, logs, sensitive data exposure, dependency risk, and abuse cases.
- **Accessibility / UX Reviewer:** keyboard interaction, focus, screen reader semantics, loading/error/empty states, visual state clarity, and user-flow regressions.
- **Data / Migration Reviewer:** migration safety, rollback, compatibility, backfill, data integrity, generated types, and deployment ordering.

If the diff has a domain-specific risk not listed above, name that reviewer explicitly and define the concern in one sentence.

## Delegating Review

Before spawning any reviewer, decide what the main agent will review locally and what can run in parallel.

Each reviewer prompt must include:

- the exact review target, such as diff, files, issue, or plan excerpt
- the assigned perspective and concerns
- the expected output format: findings first, with severity, file/line when available, evidence, and suggested fix
- the instruction to avoid editing files
- the instruction to ignore unrelated dirty changes unless they affect the reviewed diff

Keep reviewer prompts narrow. Do not ask every reviewer to perform a general review.

Example reviewer prompt:

```text
Review the implemented diff only from the QA Engineer perspective. Focus on missing test cases, regression scenarios, fixtures, mocks, and whether existing verification proves the intended behavior. Do not edit files. Return findings first, ordered by severity, with file/line references when available, then residual test gaps.
```

## Main Agent Checklist

The main agent must always perform a local checklist review, even when subagents are used:

- intended behavior is actually implemented
- old behavior or stale assumptions do not remain elsewhere
- tests and fixtures match the changed behavior
- public interfaces, types, schema, mocks, docs, and stories are synchronized when relevant
- implementation follows nearby repository patterns
- edge cases and error states are handled
- performance, security, accessibility, and migration risks are either covered or explicitly not applicable

Prefer contradiction search: look for evidence that the old behavior still exists or that another representation was missed.

## Handling Reviewer Results

Merge reviewer feedback into one judgment.

- Treat concrete correctness, regression, data loss, security, or missing-test findings as actionable unless evidence proves otherwise.
- Deduplicate overlapping findings and keep the clearest evidence.
- If a reviewer suggestion is not adopted, record the reason briefly.
- If the user asked to fix findings, fix only the in-scope issues, then rerun the relevant review or checklist for the changed area.
- If review exposes a material scope or behavior change, stop and ask for approval before fixing it.

## Final Report

Report findings first, ordered by severity.

For each finding, include:

- severity or priority
- file and line when available
- what is wrong
- why it matters
- suggested fix

After findings, include:

- reviewer budget used and why it fit the classification
- perspectives covered by subagents and by the main agent
- verification already considered or still missing
- residual risks or test gaps

If there are no findings, say that clearly and list the perspectives checked plus any remaining verification gaps. Do not produce a long process transcript.
