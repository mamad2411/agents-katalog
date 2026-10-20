---
name: dispatching-to-codex
description: Use when the user explicitly asks to hand a task to Codex — "use codex", "delegate this", "send it to codex", "交给codex", "派给codex", or the /delegate command. Runs the full dispatch lifecycle with frozen acceptance criteria and a binding independent judge. NEVER auto-dispatch — delegation happens only on the user's word. If a task looks Codex-shaped (bulk mechanical edits, wide read-and-report analysis, test scaffolding), you may offer the option in ONE line; if the user doesn't take it, drop it.
---

# Dispatching to Codex

Claude is the brain; Codex is the hands. You plan, freeze the bar, and judge. Codex executes on its own quota, in its own process, so your context stays small and your tokens go to judgment — not grunt work.

## Iron Laws (no exceptions)

1. **NO DISPATCH WITHOUT FROZEN ACCEPTANCE CRITERIA COMMITTED TO GIT.** If you cannot write a concrete pass/fail check, the task is not ready to delegate — do it yourself.
2. **NO ACCEPTANCE WITHOUT A FRESH-CONTEXT JUDGE VERDICT.** A FAIL cannot be overridden — not by you, not by "the diff looks fine".
3. **MAX 2 RETRIES, THEN LOUD TAKEOVER.** Every failure path ends with you doing the work and telling the user delegation failed. Silent success is forbidden.

## Is it worth dispatching? (say so BEFORE starting)

Dispatch overhead is real: branch + freeze + judge ≈ minutes of wall-clock and some of both quotas. If you could finish the task faster than the overhead, tell the user plainly: *"This is faster for me to do directly — still want Codex on it?"* Then respect their answer.

Good dispatches: bulk/repetitive edits, migrations, mechanical test-writing against a clear spec, wide "read everything, report back" analysis, output-heavy runs.
Bad dispatches: design work, subtle debugging, anything ambiguous, tiny tasks.

## Lifecycle

0. **Preflight.** Run `${CLAUDE_SKILL_DIR}/preflight.sh`. Not ready → one-line explanation (e.g. "run `codex login` once and I can dispatch"), then do the work yourself. Never nag twice in a session.

**Analysis-only shortcut:** if the dispatch edits NO files (wide read-and-report, investigation), skip ISOLATE/FREEZE/JUDGE — run `codex exec --sandbox read-only` and review the report yourself. The gate exists for merges, not for reading. Everything below is the write path.

1. **Isolate.** `git switch -c codex/<slug>` — throwaway branch; main is never touched.
2. **Freeze.** Write `.codex/ACCEPTANCE.md`: one-line GOAL + the exact commands that must pass (exit codes, not vibes). Commit it BEFORE Codex exists. See skills/writing-codex-briefs for the format.
3. **Brief + dispatch.** Self-contained brief (Codex sees zero chat history). Stock config:
   `codex exec -m gpt-5.5 -c model_reasoning_effort="xhigh" --sandbox workspace-write "<brief>" 2>/dev/null`
   Model/effort overrides, in priority order: `PRAETOR_MODEL` / `PRAETOR_EFFORT` env vars (use verbatim if set) → preflight reported `config=custom` (active relay provider: DROP the `-m`/`-c` flags, keep `--sandbox`, respect their config) → stock default above. Never `danger-full-access`. Always a hard timeout. Big output → `-o <file>`, never into your context.
4. **Judge.** Spawn a FRESH subagent with `agents/codex-judge.md` + repo path + branch name. Codex's work is UNCOMMITTED — the judge reviews the working tree (`git diff HEAD`), runs every frozen check, checks the bar wasn't moved. Returns PASS or FAIL + evidence.
5. **Resolve.** PASS → you commit (Codex never commits), report in plain language, append the ledger. FAIL → re-brief with `codex exec resume --last "<fix>"` (≤2 retries) or take over loudly.
6. **Cleanup.** Merge or delete the branch. Append one line to `.codex/ledger.jsonl`: `{task, model, verdict_history, wall_seconds, dispatched_at}`.

**Kill switch:** a `STOP` file in the repo root halts all dispatching — check before every dispatch.

## Red Flags — excuses that mean STOP

| Excuse | Reality |
|---|---|
| "The diff looks obviously fine, skip the judge" | Obvious diffs are where silent regressions hide. Law 2. |
| "No time to write acceptance criteria" | Then there's no way to know Codex succeeded. Law 1. |
| "One more retry will fix it" | Retry 3+ burns both quotas for a coin flip. Law 3. |
| "Codex said tests pass" | Codex reporting ≠ judge verifying. Only exit codes count. |
| "It's just a small task, skip the branch" | Small tasks on main are how main breaks. Isolate or don't dispatch. |
| "User probably wants this delegated" | Probably ≠ said so. Offer in one line, then drop it. |
