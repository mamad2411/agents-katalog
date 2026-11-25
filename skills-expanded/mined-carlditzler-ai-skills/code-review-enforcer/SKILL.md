---
name: code-review-enforcer
description: Use for rigorous code review of diffs, pull requests, or generated changes. Focus on bugs, regressions, unsafe behavior, missing tests, performance risk, accessibility issues, and platform-fit problems across Swift, Kotlin, Flutter, Tauri, Rust, and frontend code.
---

# Code Review Enforcer

## Use when
- the user asks for a review, PR review, diff review, or a second pass before merge
- generated code needs a serious correctness and release-quality check
- the main task is finding problems, not implementing a feature

## Do not use when
- the user mainly wants code written from scratch
- the task is architecture planning without a concrete diff or proposed change

## Review rules
- Findings come first. Keep summaries brief and secondary.
- Order findings by severity and user impact.
- Prefer concrete issues with file and function references over broad opinions.
- Distinguish merge blockers from release blockers.
- Do not pad the review with praise, filler, or style-only comments unless they hide a real risk.

## Review order
1. Correctness, crashes, broken invariants, and data loss.
2. Security, privacy, permissions, and destructive behavior.
3. State ownership, async ordering, lifecycle, and contract mismatches.
4. UX, accessibility, focus, keyboard, and error-state regressions.
5. Tests, observability, rollout, and rollback gaps.
6. Maintainability, naming, complexity, and dead code.

## Quality bar
- Every finding should explain why the current behavior is risky.
- Suggest the smallest credible correction.
- Flag missing negative-path coverage when the diff changes error handling, permissions, serialization, migration, or UI state.
- If no findings exist, say so explicitly and note any residual test or validation gaps.

## Reference routing
- Read `references/review-checklist.md` for the review checklist.
- Read `references/release-quality-gates.md` for release-blocker criteria.
- Read `references/official-docs.md` only when platform rules or primary docs are needed to validate a finding.

## Output contract
Provide:
- findings first, ordered by severity
- a short closeout: `Release ready`, `Merge ready, not release ready`, or `Not ready`
- the smallest set of actions needed to reach the next bar
