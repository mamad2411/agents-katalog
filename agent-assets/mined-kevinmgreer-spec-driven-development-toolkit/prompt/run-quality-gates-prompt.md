---
description: "Run all available quality gates (lint, format, typecheck, build, test) and iterate until they pass. Use after implementation or refactoring to verify code quality before PR."
agent: agent
tools: [read, search, execute]
argument-hint: "Optional: specific gate to run (test, lint, format, typecheck, build, all)"
---

Run quality gates for the current project and fix any failures.

Gate to run: ${input:all}

## Steps

1. **Load the project profile — mandatory.** Read `docs/project-profile.md` and use the
   commands and gate availability listed in the `Tooling` and `Quality Gates Available`
   sections.

   **If `docs/project-profile.md` does not exist, stop.** Do not detect gates on the fly —
   that causes the profile to never get written and means future runs will detect everything
   from scratch. Run `/analyze-project` first, then return here.

2. **Run gates in order**:
   - **Lint** — run the linter. Auto-fix what's fixable, report the rest.
   - **Format** — check formatting. Auto-fix and report.
   - **Type check** — run the type checker. Fix any type errors.
   - **Build** — run the build. Fix any compilation errors.
   - **Test** — run the full test suite. Fix any failures (in production code, never in tests).

3. **Fix and iterate**: For each failure:
   a. Read the error output
   b. Diagnose the root cause
   c. Fix the issue
   d. Re-run that gate
   e. After the gate passes, re-run ALL gates to check for regressions
   f. Maximum 3 fix attempts per gate — escalate to user if still failing

4. **Report results**:

```markdown
## Quality Gate Results

| Gate       | Status | Command            | Notes         |
| ---------- | ------ | ------------------ | ------------- |
| Lint       | ✅     | `npx eslint .`     |               |
| Format     | ✅     | `npx prettier .`   | 2 files fixed |
| Type check | ✅     | `npx tsc --noEmit` |               |
| Build      | ✅     | `npm run build`    |               |
| Tests      | ✅     | `npx vitest run`   | 12/12 passing |

**Overall**: ✅ All gates passed
```

## Rules

- **Never modify test files** to pass a test gate — fix the implementation
- **Auto-fix** lint and format issues when the tool supports it
- **Report** issues that cannot be auto-fixed — don't silently ignore them
- **Skip** gates that don't apply (e.g., no linter configured) — note as "N/A" in the report
- **Match CI** — if CI config exists, ensure local gates cover the same checks

Reference: `docs/atdd/quality-gates.md`
