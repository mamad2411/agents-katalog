---
name: session-heartbeat
description: Use this skill when the user asks "where are we", "status check", "health check", "checkpoint", "what have we done", or any progress review of the current session. Also use when the user wants to switch tasks, drop current work for something urgent, pause to review scope, or says the context/session is getting long. Covers session progress summaries, scope drift detection, task switching protocols, and context health checks.
---

# Session Heartbeat

Discipline decays silently in long sessions. After 50+ tool calls, rules start dropping — not because they're forgotten, but because momentum makes skipping feel productive. This skill re-injects the rules that matter most and catches drift before it compounds.

## Task Switch Protocol

When the user asks to switch to a different task — especially under urgency ("drop everything", "quick fix", "production issue") — perform this checkpoint BEFORE investigating the new task. The urgency is precisely why the checkpoint matters: rushed switches produce the most bugs.

1. **STOP.** Do not read files, run queries, or investigate the new task yet.
2. **Commit or stash current work**: `git stash` or commit with a WIP message. Uncommitted changes from the previous task will get tangled with the new task's changes.
3. **State what is being paused**: "We were working on [X]. That work is [committed/stashed/unverified]. We can return to it after."
4. **Run the 6-Point Check below** on the current state (takes 2 minutes).
5. **Only then** start investigating the new task — in a clean state, with rules re-injected.

The temptation to skip this and "just quickly look at" the new problem is the #1 source of tangled commits and lost work.

## Quick Heartbeat (30-second mode)

When a full 6-Point Check feels heavy mid-flow, run this abbreviated version instead. It covers the two highest-value checks:

```bash
git diff --name-only     # Scope: what have we touched?
git branch --show-current # Worktree: right branch?
```

Then re-read ONE rule from the Rule Re-injection section — whichever is most relevant to the current task (SQL work → tenant isolation, route work → route order, any edit → scope lock).

A Quick Heartbeat is better than no heartbeat. Use the full 6-Point Check at major milestones (before commits, before task switches, after compaction).

## The 6-Point Check

Run these in order. Each takes seconds. Together they catch the problems that slip through in long sessions.

### 1. Scope Snapshot

Run and report:

```bash
git diff --name-only          # What files have we actually touched?
git diff --stat               # How much change? Are we growing scope?
```

For each modified file, classify:
- **IN-SCOPE**: directly serves the original task
- **DRIFT**: unrelated cleanup, refactoring, or "while I'm here" changes
- **DEBT**: debug code (console.log, TODO comments, commented-out blocks)

State the original task in one sentence. If you cannot state it clearly, that is a red flag — scope has already drifted.

If drift detected: propose `git checkout -- [drifted-file]` to revert out-of-scope changes before they compound.

**Cortex-specific drift patterns to watch for:**
- Import cleanup in files you didn't need to touch
- Formatting/whitespace changes alongside functional edits
- Adding error handling to existing code that works fine
- "Improving" variable names in surrounding code
- Adding JSDoc comments to functions you only called

### 2. Worktree Check

```bash
git rev-parse --show-toplevel   # Are we in the right worktree?
git branch --show-current       # Correct branch for this task?
```

Verify we are not accidentally editing files in the wrong worktree or on `dev`/`master` directly. If on dev/master for non-trivial work, stop and create a worktree.

### 3. Verification Ledger

For each modified file, answer YES or NO:
- Was `run-verification` invoked AFTER the last edit to this file?
- Did it pass?

Format as a table:

| File | Verified? | Status |
|------|-----------|--------|
| `services/foo.js` | YES | PASS |
| `routes/bar.js` | NO | UNVERIFIED |

Any UNVERIFIED file is a risk. Flag it. Do not commit unverified files.

### 4. File Size Scan

```bash
wc -l [each modified file]
```

Classify each:
- **SAFE** (under 300 lines): continue normally
- **WARNING** (300-400 lines): mention it, consider extraction if adding more code
- **OVER LIMIT** (400+ lines): stop adding code to this file. Extract to a submodule using the pattern `services/serviceName/subModule.js` or `routes/routeName/subRouter.js`

This catches the "file is at 380 and I am about to add 60 lines" trap that CLAUDE.md's 400-line rule cannot enforce.

### 5. Rule Re-injection

These rules fade from working memory over time. Re-read and internalize each one now:

**SCOPE LOCK**: Only do what was asked. If you notice something else broken, note it in a comment to the user — do NOT fix it. The urge to fix "one small thing" is how scope creep starts.

**REVERT-FIRST**: If a test that was passing is now failing after your change: `git checkout -- [file]`. Do NOT update the test to match your code. Do NOT fix forward. Revert first, understand why, then re-approach.

**PRE-CODE CHECKLIST**: Before the next edit, recall gotchas from Obsidian vault: `search_vault(query="cortex coding gotchas PRE-CODE checklist")`. Quote the specific trap that applies. "Checked" is not enough — name the specific trap.

**TENANT ISOLATION**: Every INSERT needs `tenant_id`. Every SELECT/UPDATE/DELETE scopes to `tenant_id` in the WHERE clause. Exception: `products`, `inventory`, `suppliers` tables (shared across tenants in this codebase).

**SQL SAFETY**: `$1, $2` placeholders only — never template literals in SQL. `TIMESTAMPTZ` not `TIMESTAMP`. `IF NOT EXISTS` on all DDL.

**cortex-engine**: Prefer `cortex_read_symbol`/`cortex_outline`/`cortex_find_symbol` over Read/Grep for code exploration. If the index is stale or missing, run `cortex_status()` and `cortex_reindex()` first. Use Read only for full-file context, config/non-code files, or before editing.

**COMMIT DISCIPLINE**: Before committing, run `git diff --stat` and check:
- No debug code (console.log, debugger, TODO)
- No out-of-scope files
- Conventional commit prefix (feat:, fix:, refactor:, etc.)
- Tests pass on all modified code

### 6. Context Health

Estimate how deep into the context window we are:

- **Under 50%**: Continue normally. Schedule next heartbeat in ~25 tool calls.
- **50-70%**: Wrap up the current sub-task. Commit what is working. Prepare a mental summary of remaining work.
- **Over 70%**: STOP new work immediately. Save state to Obsidian vault (`/vault-capture`). Write handover doc to `docs/handovers/`. Commit everything. Tell user to `/clear`.


## Post-Commit Checkpoint

After every `git commit`, run this quick validation:

```bash
git log -1 --oneline           # Verify commit message is conventional
git diff --stat HEAD~1         # Verify only expected files were committed
git diff --name-only           # Verify working tree is clean (no leftovers)
```

Check the commit:
- Commit message has conventional prefix? (feat:, fix:, refactor:, etc.)
- No debug code in the diff? (search for console.log, debugger, TODO)
- No out-of-scope files committed?
- All committed files were in the verification ledger as PASS?

If any check fails: `git reset --soft HEAD~1` to uncommit (keeps changes staged), fix the issue, recommit.

## Session Summary Template

When wrapping up a session or writing a handover, use this structure:

```markdown
## What was done
- [1-3 bullet points of completed work]

## Current state
- Branch: [branch name]
- Modified files: [list from git diff --name-only]
- Verification: [PASS/FAIL/UNVERIFIED per file]
- Tests: [passing/failing count]

## What remains
- [numbered list of remaining tasks]

## Gotchas for next session
- [any traps discovered, rules that were almost violated]
```

## Skill Cross-References

When the heartbeat detects specific types of work, suggest the relevant skill:

| Detected Activity | Suggest Skill |
|-------------------|---------------|
| SQL query being written or modified | `sql-guard` — run the checklist before writing |
| REX/Shopify integration code | `integration-guard` — check field mappings |
| About to commit | `scope-check` — verify no drift |
| Approaching context limit | `handover-writer` — save state properly |
| Starting a new feature branch | `worktree-cleanup` — check for stale worktrees |
| Migration being created | `sql-guard` — migration safety section |
| Code exploration / symbol lookup | `cortex-engine` — `cortex_status`, then `cortex_outline`/`cortex_find_symbol` |

## When to Invoke

This skill works through repetition, not one-time use:

- **Every 20-30 tool calls** during active coding (Quick Heartbeat if mid-flow)
- **Before switching sub-tasks** (full 6-Point Check — commit first, then checkpoint, then switch)
- **After any context compaction** (rules get compressed — re-inject them)
- **After every commit** (Post-Commit Checkpoint)
- **When the user asks "where are we?"** or any progress/status check
- **When something feels off** — trust that instinct

## Anti-Patterns

These thoughts mean the heartbeat is overdue:

| Thought | Reality |
|---------|---------|
| "I'm almost done" | Last 10% produces the most bugs |
| "Everything is going well" | Silent violations feel like smooth progress |
| "It'll break my flow" | 2 minutes of checking saves 20 minutes of debugging |
| "I'll verify everything at the end" | You won't. Verify as you go. |
| "This cleanup is too small to matter" | Small drifts compound into large scope creep |
| "I already know these rules" | Knowing ≠ following. Re-read them. |
| "Drop everything — I'll checkpoint later" | Later never comes. Checkpoint now. |
| "I'll just quickly look at the new issue" | Task switches without checkpoints produce tangled commits |
