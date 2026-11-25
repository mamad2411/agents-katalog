---
name: verify-before-done
description: MANDATORY before declaring ANY code change "done", "fixed", "working", "ready", "shipped", or before ending a turn after editing source. Use whenever you modified code, config, scripts, SQL, infra, or tests and are about to say it works. Forces you to RUN something that exercises the change (test, build, lint, typecheck, smoke script, reproducible command) and record the evidence. Triggers on "done", "fixed", "working", "all tests pass", "build succeeded", "should work now", "ready to merge".
---

# Verify Before Done

**A clean compile is not verification. Types passing is not verification. "I updated the handler" is not verification.**

You can state facts about what you *ran*. You cannot state facts about what *should* happen.

## The rule

> **No "done" without evidence.** Run a command that exercises the change, read the output, then claim completion.

## Step 1 — Pick the right verifier (smallest proof that falsifies your claim)

| You changed… | Minimum proof |
|---|---|
| App logic / API | Targeted test or `curl`/request that hits the path |
| UI behaviour | Render + interaction check (pair with `visual-quality` for pixels) |
| Build / types | `build`, `tsc --noEmit`, `cargo check`, etc. |
| Refactor only | Tests that cover touched modules |
| Config / env | Command that loads config or a smoke script |
| SQL / migration | Dry-run, `EXPLAIN`, or migration against a scratch DB |

If nothing can be run, say **"unverified — manual step required"** and list exactly what the human must run. Do not imply it works.

## Step 2 — Run it (in this session)

Use Bash (or the project's test tool). Prefer the **narrowest** command that still falsifies the bug.

Examples (adapt to the repo):

```bash
npm test -- --runInBand path/to.test.ts
pnpm vitest run src/foo.test.ts
pytest tests/test_checkout.py -q
cargo test -p mycrate checkout::
go test ./internal/checkout/...
xcodebuild test -scheme App -destination 'platform=iOS Simulator,name=iPhone 16'
npm run build
pnpm lint && pnpm typecheck
```

Read failures literally. Fix, re-run, until green **or** you document a known flake with evidence.

## Step 3 — Record evidence in your reply

Include:

1. **Command(s) run** (copy-paste exact)
2. **Outcome** (pass/fail, exit code, key log lines)
3. **Scope** (what this does *not* prove, if anything)

## Step 4 — Sentinel (required to end the turn after code edits)

When verification is genuinely complete, end your assistant message with:

```
VERIFY-BEFORE-DONE: PASS — <command> → <outcome>
```

Example:

```
VERIFY-BEFORE-DONE: PASS — pytest tests/test_invoice.py -q → 4 passed
```

The Stop hook looks for this line after code edits. Without it, the turn may be blocked.

## Kill switch

False positive (docs-only change, user said skip tests): `touch .verify-before-done-off` in the project root, or `export VERIFY_BEFORE_DONE_GATE=off`.

## Pairs with

- **`visual-quality`** — run *after* code verifies; screenshots are not tests.
- **`scope-guard`** — don't verify the wrong files by editing the whole tree.