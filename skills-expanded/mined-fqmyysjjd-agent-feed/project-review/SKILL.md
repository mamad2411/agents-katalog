---
name: project-review
description: Use when reviewing modified code, git diffs, commits, merges, PR-like changes, or implementation output.
source: agent-feed
trust: core
---

# Project Review Skill

## Required Use

Use this skill for code, diff, commit, merge, or AI-generated implementation review.

Do not modify code during a review unless the user explicitly asks for fixes in the same task.

## Review Mode

Classify the review before acting:

1. `Pure review`: the user asked for review, diff review, commit review, or findings. Do not edit files. Return findings and residual risk only.
2. `Implementation gate`: the review is part of a task that already includes coding, refactor, fix, or tests. Findings may become follow-up fixes inside the same Task Brief.

For implementation gates, route P0/P1 findings and default-fix P2 findings through `.agents/skills/project-fix/SKILL.md`, then rerun relevant verification before final handoff.

If a finding requires an unconfirmed decision outside the current Task Brief, stop and apply `.agents/rules/decision-gates.md`.

## Fix-Loop Budget Tracking

This section applies **only to Implementation gate reviews and Fix tasks** (see Review Mode above). Pure Review tasks do not write `review_round` — return findings and stop.

`current_task.review_round` records the **number of completed review rounds** on the current task. Treat an absent field as `0`.

1. Before starting a round, read `current_task.review_round` (or treat absent as `0`). If it is already `>= 2`, stop and apply `.agents/rules/review-gates.md` Fix-Loop Budget — do not start another round unless the user asked or a P0/P1 was newly introduced by the last fix; if you proceed, state the reason.
2. After the round finishes (findings reported, in-task fixes applied, verification rerun), increment `current_task.review_round` (set it to `1` if absent). Do not increment at the start of a round.
3. The counter is per-task. Drop it from session-state when the task boundary is satisfied.

## Required Reading

1. `.agents/rules/outcome-boundary.md`
2. `.agents/rules/engineering-architecture.md`
3. `.agents/project/architecture-boundaries.md`
4. `.agents/rules/development-workflow.md`
5. `.agents/project/project-structure.md`
6. `.agents/rules/testing-gates.md`
7. `.agents/rules/review-gates.md`
8. `.agents/domain/contracts.md`
9. `.agents/skills/README.md`
10. `.agents/skills/specialist-router/SKILL.md` when an optional, imported, custom, or specialized skill may match the diff or risk.

## Review Scope

Findings should prioritize correctness, contract drift, repository-evidence
ownership, dependency direction, tests, error handling, security/secret
handling, and maintainability.

Before finalizing findings, check `.agents/skills/README.md` for specialized review or fix skills that match the changed language, architecture, framework, persistence layer, or risk category. Use `.agents/skills/specialist-router/SKILL.md` when the match is not obvious, when a custom skill is involved, or when multiple skills could apply. Use only the skills that directly serve the current review boundary.

Use `.agents/skills/concept-review/SKILL.md` when the diff introduces or changes names, concepts, abstractions, protocol terms, user-facing language, or skill vocabulary.

## Module Understanding Review

For every affected module, command, adapter, protocol asset, or public surface, review whether the change proves the AI understood the path it modified.

Check for evidence of:

1. Affected entrypoints, owners, and outputs: the changed files cover the actual requirement path and do not miss a relevant caller, boundary converter, generated template, or user-visible surface.
2. Flow closure: input or trigger -> orchestration/state -> output, write, generated asset, or side effect is complete.
3. Contract consistency: function signatures, CLI arguments, config keys, schemas, generated file paths, adapter expectations, and documented behavior stay aligned.
4. Architecture evidence: ownership and placement are inferred from this repository's files, calls, tests, docs, config, or generated assets, not from generic template categories.
5. Dependency direction: low-level reusable logic, entrypoints, boundary conversion, generated outputs, tests, and external effects keep their existing dependency direction unless an architecture decision was confirmed.
6. Boundary and failure handling: validation, permissions, error messages, cleanup, rollback expectations, and logging/audit anchors are handled at the owning layer.
7. State and data safety: defaults, empty/null cases, async or repeated execution, durable state, secrets, and trust/config boundaries remain safe.
8. Reuse and duplication: existing helpers, patterns, tests, boundary converters, generated sources, or template owners were reused before adding parallel behavior.
9. Maintainability cost: new concepts, abstractions, branches, or files add only necessary complexity.
10. Minimal implementation: the diff does not introduce future-facing machinery, broad rewrites, or unrelated formatting/noise to satisfy a narrow task.
11. Style consistency: similar existing behavior uses compatible naming, layering, errors, output style, comments, and verification patterns.
12. Shared or deletion risk: global files, shared helpers, generated assets, removed paths, and adapter mirrors were checked for other consumers.

If a relevant item has no evidence, report it as a finding or residual risk. Do not replace missing evidence with a general "looks fine" statement.

## Severity Model

1. `P0`: Data loss, secret leak, source-of-truth break, or irreversible corruption.
2. `P1`: Public API, contract, lifecycle, persistence, security, or recovery break.
3. `P2`: Module boundary, test coverage, traceability, or maintainability risk.
4. `P3`: Naming, local readability, or small cleanup issue.

## Output

Return findings first, ordered by severity. If no findings are found, say so explicitly and list residual risks or tests not run.
