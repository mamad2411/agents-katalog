---
name: tdd
description: Test-driven development — vertical red-green-refactor slices through public interfaces.
---

# TDD

Tests verify **behavior through public interfaces**, not implementation. Good tests survive refactors; bad tests break on rename.

See [tests.md](tests.md) and [mocking.md](mocking.md) for examples.

## Anti-pattern: horizontal slices

Don't write all tests then all code. One behavior: RED → GREEN → repeat.

## Workflow

1. **Plan** — read `CONTEXT.md`/ADRs. Confirm interface changes and behaviors to test with user.
2. **Tracer bullet** — one test, one minimal implementation, passes.
3. **Loop** — one test at a time; only code to pass current test; no speculation.
4. **Refactor** — only when GREEN; see [refactoring.md](refactoring.md).

## Per-cycle checklist

- [ ] Describes behavior, not implementation
- [ ] Uses public interface only
- [ ] Minimal code for this test
