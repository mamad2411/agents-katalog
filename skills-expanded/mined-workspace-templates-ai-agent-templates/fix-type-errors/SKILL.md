---
name: fix-type-errors
description: Runs your type checker and fixes each reported error at its root cause, never with casts, any or suppression comments.
disable-model-invocation: true
---

Fix the type errors in this project. Scope: $ARGUMENTS (everything if empty).

1. Find the checker command in package.json scripts, pyproject, tox or CI config (`tsc --noEmit`, `mypy .`, `pyright`, `go vet`, `cargo check`). Run it and save the full error list with the count.
2. Group errors by root cause: a changed library type, a wrong interface, a missing null check, an outdated mock. Fix the root first and re-run, since many errors usually vanish together.
3. Fix each one with a correct type or a real guard. Never add `as any`, `as unknown as`, `!` non-null assertions, `@ts-ignore`, `@ts-expect-error` or `# type: ignore`, and never loosen the compiler options.
4. If the fix would require changing behavior, or the error reveals a genuine bug, stop on that item and describe it with the file and line.
5. Re-run the checker until clean or until only the stopped items remain. Then run the tests.

Report the count before and after, the root causes found, any bugs, and the files changed. Ask before changing any public type that other packages consume.
