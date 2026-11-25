---
name: quality-gates
description: Use when a lint, test, or build gate fails during the VERIFY phase and you need the auto-fix procedure, when you need to classify an error and choose a fix strategy, or when WebSearch fallback is needed after repeated gate failures.
user-invocable: false
---

# Quality Gates Skill

Reference material for executing quality gates during `/cs-loop` VERIFY phase.

## Gate Execution Order

| Gate | Action | Pass Criteria |
|------|--------|---------------|
| LINT | Run lint command from profile | Zero errors |
| TEST | Run test command from profile | All tests pass |
| BUILD | Run build command if defined | Clean compilation |
| GIT | Check `git status` | Clean working state |

Advisory gates (report only, non-blocking): TYPE, DOCS, SECURITY.

## Auto-Fix Sub-Loop

When a gate fails, attempt automatic repair (max 3 attempts per gate):

### Error Classification

| Error Type | Fix Strategy |
|------------|-------------|
| Lint (auto-fixable) | Run `fix_command` from profile gates (e.g., `ruff check . --fix`) |
| Import ordering | Run format/sort command from profile gates |
| Type errors | Read file at error location, fix type annotations |
| Test failures | Read failing test + source under test, fix logic in source |
| Build errors | Read compiler output, fix compilation issues |

### Procedure

1. Gate fails -> classify error type from output
2. If profile has `fix_command` for this gate: run it, re-verify
3. If no `fix_command` or it didn't resolve: read error, apply manual fix, re-verify
4. Maximum 3 attempts per gate. Track: `[VERIFY] Auto-fix attempt {n}/3: {gate}`
5. If error count increases after any attempt: revert changes and stop
6. If all 3 attempts fail: fall through to WebSearch strategy

### Hard Constraints

- Never modify test assertions or expected values to make tests pass
- Never skip or disable quality gates
- If fix introduces new errors, revert immediately
- Report each attempt: `[VERIFY] Auto-fix attempt {n}/3: {gate} -- {strategy}`

## WebSearch Fallback

When auto-fix exhausts 3 attempts:

1. Extract error message from gate output
2. WebSearch("{language} {error_message} fix 2026")
3. If solution found: apply fix automatically
4. If still failing after 2 WebSearch attempts: stop and report

## MCP Integration

- **Puppeteer** (web projects): Navigate -> screenshot after UI changes
- **GitHub**: Check CI status on PRs (passing/failing/pending)
- **Vision**: Capture and analyze error screenshots for UI test failures

## CI Monitoring (Post-Commit)

After committing on a branch with a PR:
1. Check if current branch has an open PR
2. If PR exists, monitor CI:
   - Passing -> `[COMMIT] CI passed`
   - Pending -> `[COMMIT] CI running...` (continue)
   - Failing -> Auto-fix if lint/test/type error (max 2 attempts)
   - Infrastructure failure -> Report for manual review

## Commit Strategies

See `references/commit-strategies.md` for per-file and per-task commit strategies.
Default is `atomic` (single checkpoint commit). Override via `--commit-strategy` argument or `CLAUDE.local.md`.

## Advisory: Browser Verification (web projects)

**Trigger**: Web project profile AND Playwright/puppeteer MCP connected
**Action**: Navigate to dev server, take screenshot, validate against task intent
**Blocking**: No (advisory only)
**Gotcha**: Dev server must be running. If not, attempt `npm run dev` or equivalent in background, wait 5s, then screenshot.

## Gotchas

- **Never dismiss errors as "pre-existing"**: Fix ALL lint issues during VERIFY — even if they existed before your changes. If ruff reports it, fix it. This is an Integrity Rule.
- **Never modify test assertions**: When tests fail, fix the source logic, not the expected values. If tests are genuinely wrong, report to the user rather than "fixing" assertions.
- **post-tool-observer null exit_code**: Claude Code's PostToolUse may omit `exit_code` (yields null). post-tool-observer treats null as inconclusive (`passed: null`), not failure. Don't log spurious "Gate failed (exit null)" entries.
- **Large gate output truncation**: Stdout > 8000 chars is saved to `.claude/state/gate-output/` and replaced with a reference. If you see `outputRef` in gate_history.json instead of raw output, read the referenced file.
- **Error count regression**: If auto-fix attempt increases the error count, revert immediately. Don't try to "fix forward" — the fix introduced new problems.
