---
name: forge-prove
description: >-
  Evidence-first verification during implementation: failing test, minimal fix,
  green gate. Use when adding or changing behavior.
---
# Forge Prove

**Activates:** during `forge-execute` when behavior changes.

## Cycle

1. **Red** â€” write or extend a test that fails for the right reason
2. **Witness** â€” run test; confirm failure message matches intent
3. **Green** â€” minimal production code to pass
4. **Witness** â€” full relevant suite passes
5. **Refactor** â€” only with green tests; no scope expansion

## Anti-patterns (reject)

- Production code before any failing test (unless pure refactor with full coverage)
- Tests that always pass regardless of implementation
- Deleting tests to go green
- `skip` / `@ts-ignore` to bypass without owner OK

## Commands

```bash
npm test -- path/to/focused.test.ts
npm test   # before task complete
```

## Prompt cross-ref

`docs-ai/cross-cutting/agent-forge/workflow/prompts/testing/unit-test-design.md`

## When to skip

Docs-only or comment-only â€” run lint/typecheck instead.
