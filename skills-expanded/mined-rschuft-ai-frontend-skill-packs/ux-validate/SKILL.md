---
name: ux-validate
description: "Validate a designed or implemented UI/UX change with task-based usability checks, accessibility checks, keyboard/mobile flows, failure recovery, and explicit evidence. Use for verifying fixes and UI acceptance tests."
---

# Validate UI/UX changes

## Scope

Assess the actual user outcome; snapshots and lint alone are insufficient.

Use `references/acceptance-matrix.md` to select relevant executable/user-test cases; do not mechanically run the entire matrix for a tiny change.

## Procedure

1. Start from explicit user goals and expected outcomes. Read prior issue IDs if available and translate each recommendation into an observable pass/fail case.
2. Inspect runtime behavior when access exists: first use, common expert path, loading, empty/error, cancellation, back/forward, interrupted draft and final confirmation. Distinguish simulated tests from live evidence.
3. Inspect accessibility systematically: keyboard-only, focus order and visibility, form labels/errors, correct name/role/state, screen reader when available, zoom and reflow, pointer targets, contrast and reduced motion. Use applicable WCAG 2.2 criteria, not psychology laws as legal standards.
4. For a chosen UX law, design a disconfirming scenario: e.g. does reduced choice hide expert features? Does novelty impede expected interactions? Does optimistic feedback claim success before durable state?
5. Record outcomes and the environment; identify regressions, risks and explicit remaining unknowns. Mark `verified` only for actual observed/tested success.

Useful measures: task completion, first correct action, error/recovery, mis-tap, decision time, findability, resume rate, comprehensibility and user trust. Measure before/after when feasible. Report `tested | passed | failed | untested`; never invent metrics.
