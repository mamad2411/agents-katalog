---
name: token-guard
description: Use Codex Token Guard to reduce noisy command and tool-output tokens while preserving errors, file paths, line numbers, test names, user instructions, recent edits, and architecture decisions.
---

# Codex Token Guard

Use this skill when a Codex session needs lower token waste without lower output quality.

## Operating Rule

Default to quality over savings. If uncertain, preserve content.

## Workflow

1. Prefer focused search and reads:
   - `rg --files | sed -n '1,200p'` instead of `find .`
   - `rg "pattern" path/` instead of `grep -r`
   - `sed -n '1,160p' file.ts` instead of `cat` on large files
2. Keep full error context:
   - actual error message
   - file path
   - line and column
   - failing test name
   - stack frame where useful
3. Use CLI checks:
   - `codex-token-guard stats`
   - `codex-token-guard stats --session`
   - `codex-token-guard snapshot`
   - `codex-token-guard benchmark`
   - `codex-token-guard notifications status`
   - `codex-token-guard digest status`
4. Before compaction, preserve:
   - goal
   - current status
   - key decisions
   - files touched
   - bugs/errors
   - next steps

## Modes

- `safe`: only blocks obvious waste.
- `balanced`: default; blocks high-noise reads, warns on broad tests, compresses noisy output.
- `aggressive`: strict budgets and fail-closed hook errors.

## Quality Protection

Never remove user instructions, recent edits, architecture decisions, actual error messages, file paths, line numbers, API names, function names, or test names.

## Notifications

Notifications are on by default. They show Token Guard estimated avoided, raw, and sent-token totals for blocked commands, output compression above the configured threshold, benchmark results, and Stop summaries. They are not Codex context-window UI readings.

Runtime metrics and session state live under `.codex-token-guard/runtime/` so hooks do not edit tracked starter templates.

In-thread notices are enabled by default and stay one line at milestone scale:
`[token-guard] est. avoided 30k tokens (25%); guard sent 90k of 120k raw`.

Context Digest is enabled by default. It injects a small session digest only on resume-style prompts, large prompts, or long sessions after enough hook activity since the last digest. It should not run every turn.

If `/hooks` reports invalid JSON output, update Token Guard and restart Codex. If hooks appear twice, remove either the manual `~/.codex/hooks.json` Token Guard entries or the plugin-bundled install so Codex does not run both.

Use:

- `codex-token-guard notifications status`
- `codex-token-guard notifications on`
- `codex-token-guard notifications off`
- `codex-token-guard notifications in-thread on`
- `codex-token-guard notifications in-thread off`
- `codex-token-guard digest on`
- `codex-token-guard digest off`
- `codex-token-guard digest status`
