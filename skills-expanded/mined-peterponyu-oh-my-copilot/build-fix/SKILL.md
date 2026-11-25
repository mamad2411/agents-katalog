---
name: build-fix
description: "[OMCP] Fix build, typecheck, or compile errors with minimal changes until the build is green"
orchestrates-agents: "debugger, verifier"
---

# [OMCP] Build Fix

Use this skill when a build, typecheck, or compile step is red and the goal is
to get it green with the smallest possible diff. Not for refactors,
architectural changes, or feature work — those go through the regular
implementation skills.

## Agent orchestration

This skill coordinates `debugger` for error categorization and minimal-fix
proposals, and `verifier` for confirming each fix actually clears the error
without introducing new ones.

## When to use

- "fix the build", "build is broken", "tests won't compile"
- TypeScript / Rust / Go / Python typecheck fails
- Linter errors blocking the build
- Module resolution or import errors after a refactor

## When not to use

- The failure is a *runtime* bug (use `/omcp:debug` instead).
- The diff would need to be large or cross-cutting (use `/omcp:plan` first).
- A test is *logically* failing rather than failing to compile (use
  `/omcp:verify` or `/omcp:debug`).

## Run

1. Identify the actual build command(s) from the repo (look for `package.json`
   scripts, `Makefile`, `cargo`, `go build`, `tsc`, `pytest --collect-only`,
   etc.). Do not invent commands.
2. Run the build and capture the full error output. Read the actual output;
   do not infer.
3. Categorize each error by location, kind, and likely cause. Group fixes
   that share a root cause.
4. Apply the smallest fix that clears each error class:
   - Add missing type annotations or imports.
   - Fix obvious typos and renames.
   - Add the smallest null/guard checks the type system requires.
   - Restore deleted re-exports only if other code already depends on them.
5. Re-run the build after each fix or fix-cluster. Stop when the build exits
   green.
6. If a fix would require non-trivial design changes, **stop and surface the
   decision** rather than guessing.

## Hard constraints

- No refactoring of unrelated code.
- No architectural changes.
- No performance "while I'm here" improvements.
- No silent `// @ts-ignore`, `# type: ignore`, or `eslint-disable` without an
  explicit reason and the user's acknowledgement.
- Do not weaken types or delete tests to silence errors.

## Output format

```
Build command: <exact command>
Errors before: <N>
Fix clusters:
  1. <error class> — files: ..., fix: <one sentence>
  2. ...
Errors after each cluster: <N> -> <N-k> -> ... -> 0
Final build status: PASS | still failing (reason)
Lines changed: <N>
Open decisions surfaced: <list or "none">
```

## Goal

- get the build green with the smallest diff possible;
- never trade short-term green for long-term fragility;
- when in doubt, stop and ask rather than mask.
