---
name: validate-quick
description: Quick pass/fail run of the project's own gate (typecheck, lint, unit tests from package.json). Use before a commit or push, or when the user asks "is it ready?", "can we commit?", "c'est prêt ?", "on peut commit ?".
allowed-tools: Bash(pnpm:*), Bash(corepack:*), Bash(npx:*), Read
context: fork
agent: general-purpose
user-invocable: true
---

# Quick Validation Check

Run the project's gate and return a short pass/fail summary.

## Process

1. Read the project instructions (AGENTS.md, CLAUDE.md). If they define a pre-commit gate, run exactly that gate.
2. Otherwise read the `package.json` scripts and run, in order, whichever exist:
   - `typecheck`, or `tsc --noEmit` when there is no such script but a `tsconfig.json` exists;
   - `lint`;
   - `test` (unit tests).
   Run `build` only when the project has no typecheck at all (for example a web app whose build is its type check). Never run E2E or device suites here.
3. Use the repository-pinned package manager (`corepack pnpm …` when `packageManager` pins pnpm).
4. A missing step is reported as "not configured", never as OK.

## Output

```
✅ Validation passed
- Typecheck: OK
- Lint: OK
- Tests: OK (N passed)
```

```
❌ Validation failed
- Typecheck: FAILED
- Lint: OK
- Tests: not configured
```

No detailed errors and no fixes: name the failing step and stop.
