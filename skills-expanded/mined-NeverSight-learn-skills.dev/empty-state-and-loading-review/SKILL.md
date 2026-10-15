---
name: empty-state-and-loading-review
description: Review and design empty states, loading states, skeletons, progress indicators, offline states, first-use states, zero-result states, and error recovery for apps, SaaS, games, utilities, and web products. Use when a product surface feels blank, confusing, slow, dead, or when designing resilient UI states beyond the happy path.
---

# Empty State And Loading Review

Use this skill to make non-happy-path UI feel intentional, useful, and fast.

## Workflow

1. Identify the state type: first-use empty, zero-result, permission-blocked, loading, partial loading, offline, error, or completed.
2. Read `references/empty-loading-patterns.md`.
3. Check whether the state explains what happened, why it matters, and what the user can do next.
4. Separate product-state fixes from visual polish.
5. Produce copy, layout, instrumentation, and acceptance checks.

## Guardrails

- Do not use cute empty-state copy when the user has lost work, money, or access.
- Do not hide loading uncertainty behind fake precision.
- Preserve accessibility, reduced motion, and layout stability.

## Output format

```text
Surface:
State type:

Findings/spec:
- <rule id> <issue or decision> -> <fix>

Copy and action:
- Message:
- Primary action:
- Secondary action:

Acceptance checks:
- <check>
```
