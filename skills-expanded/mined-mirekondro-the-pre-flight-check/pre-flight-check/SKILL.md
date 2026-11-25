---
name: pre-flight-check
description: Run this quality gate pipeline before committing code, completing a task, or when validating if a bug fix worked. It strictly checks Typechecking, Linting, Testing, and Security Audits sequentially.
---

# Pre-Flight Check

A mandatory, fail-fast quality gate. Runs Typecheck → Lint → Test → Security Audit sequentially via `scripts/run-pipeline.py`. The script auto-detects the project runtime (Node.js or Python) and exits with code `1` on the first failing stage, emitting a structured Markdown block you must parse.

## When to invoke

Run this skill **without being asked** at every one of these checkpoints:

- **Before announcing a task is "done"** — any task involving code edits.
- **Before staging, committing, or pushing** any change.
- **After applying a bug fix** — to confirm the fix holds across all gates, not just the failing test.
- **Before opening a PR** or marking work ready for review.

If you are about to say "done", "fixed", "complete", "ready to commit", or similar — stop and run this skill first.

## How to run

Execute from the repository root:

```bash
python .claude/skills/pre-flight-check/scripts/run-pipeline.py
```

The script writes a header per stage as it progresses, then emits one of:

- `### ✅ PRE-FLIGHT PASSED` — exit `0`. Safe to proceed.
- `### ❌ PRE-FLIGHT FAILURE: [STAGE_NAME]` — exit `1`. Stop and fix.
- `### ⚠️  PRE-FLIGHT SKIPPED: …` — exit `1`. Runtime undetected or no stages resolved. Resolve tooling before proceeding.

## Strict Fail-Fast Protocol

If the script outputs `### ❌ PRE-FLIGHT FAILURE: [STAGE_NAME]`, you are **FORBIDDEN** from:

- Declaring the task done.
- Committing, staging, or pushing any code.
- Switching to a different task, file, or feature.
- Suppressing the error (no `// @ts-ignore`, no `# noqa`, no `eslint-disable`, no `pytest.skip`, no removing the failing test, no widening `ignore` globs).
- Re-running the pipeline hoping for a flake. Failures are real until proven otherwise by a fix in source.

Your **only** permitted next action is to repair the specific error reported by the failing stage and re-run the pipeline. Continue this loop until you see `### ✅ PRE-FLIGHT PASSED`.

### Stage-specific repair rules

**TYPECHECK failure**
1. Parse `Context for AI Fix` for the file path and line number (e.g. `src/foo.ts:42`).
2. Read the offending file at that line with the `Read` tool.
3. Fix the type at its source — narrow the type, add the missing field, correct the signature, or update the call site.
4. Do **not** add `any`, `as unknown as X`, `# type: ignore`, or equivalent escape hatches to silence the checker. If a cast is genuinely required (e.g. external untyped boundary), it must be the minimum-width cast at the narrowest possible scope, with a one-line comment explaining why.
5. Re-run the pipeline.

**LINT failure**
1. Identify the rule ID and file from the context block.
2. Run the project's auto-fix command first:
   - Node: `npm run lint -- --fix` / `pnpm lint --fix` / `yarn lint --fix` / `npx eslint . --fix`.
   - Python: `ruff check . --fix` or the equivalent formatter (`ruff format .`, `black .`).
3. For rules the auto-fixer cannot resolve, edit the file manually to satisfy the rule.
4. Do **not** add the file to `.eslintignore` / `ruff` exclude lists, do **not** add file-level disables, do **not** weaken the rule globally. Inline rule disables are allowed only for a single line with a comment justifying why.
5. Re-run the pipeline.

**TEST failure**
1. Read the assertion message and the failing test name from the context block.
2. Determine whether the production code is wrong or the test's expectation is wrong. Default assumption: production code is wrong.
3. Fix the root cause. Do **not** delete, skip, or relax the assertion to make it pass.
4. Re-run the pipeline.

**SECURITY AUDIT failure**
1. Identify the vulnerable package and CVE / advisory ID from the context block.
2. Upgrade to the patched version range. If no patch exists, evaluate whether the package can be replaced or the affected code path is reachable.
3. Do **not** add the advisory to an ignore list to silence the audit without explicitly stating the risk acceptance to the user and getting confirmation.
4. Re-run the pipeline.

## Reading the structured error context — avoid the lazy loop

The `### ❌ PRE-FLIGHT FAILURE` block is engineered so you can act decisively. Use it as follows; do **not** spin in vague attempts.

1. **`Command Executed`** — confirms which tool produced the error. Use this to pick the correct repair recipe above. If you are guessing what tool failed, you are about to make a wrong fix.
2. **`Context for AI Fix`** (the fenced code block) — extract, in order:
   - The **file path** (relative or absolute).
   - The **line and column** (e.g. `:42:17`).
   - The **rule ID or error code** (e.g. `TS2345`, `E501`, `no-unused-vars`, `CVE-2024-xxxxx`).
   - The **diagnostic message** verbatim.
3. **Open the named file at the named line first.** Do not search the codebase, do not re-read unrelated files, do not refactor surrounding code. Repair the exact diagnostic.
4. **One failure, one fix, one re-run.** Do not bundle speculative changes alongside the repair. If the next pipeline run reveals a new failure, treat it as a new cycle.

### Lazy-loop anti-patterns — refuse these

- Re-running the pipeline unchanged hoping the result differs.
- Editing a file you were not directed to by the diagnostic.
- "Fixing" by deleting the failing test, suppressing the rule, or relaxing the type.
- Reporting "done" while a failure is on screen.
- Declaring a flake without evidence (a reproducible non-determinism, a network/timing issue documented in the test).
- Switching strategy after a single failure — repair, re-run, repeat.

## Success state

When the script prints:

```
### ✅ PRE-FLIGHT PASSED
All quality gates verified successfully.
```

…and exits `0`, you may proceed with the original action (commit, mark done, open PR). Not before.
