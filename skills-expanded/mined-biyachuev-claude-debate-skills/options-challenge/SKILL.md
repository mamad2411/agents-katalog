---
name: options-challenge
description: Compare several strategic options, force explicit trade-offs, and rank the strongest path. Use when the user has multiple plausible directions and wants a sharper decision memo.
argument-hint: "[decision brief, optional finalizer, optional log file]"
disable-model-invocation: true
---

# Options Challenge

Use this skill for decisions where at least two plausible paths exist and the user wants ranking, trade-offs, and a final recommendation.

Treat `$ARGUMENTS` as the full decision brief.

## Non-negotiable rules

1. If Codex is not available in the current Claude Code session, say that explicitly and stop. Do not fabricate Codex output.
2. Show the option framing, challenge, and ranking visibly in the chat.
3. Unless the user opted out of logging, save the full visible output to a resolved log path.
4. If logging is enabled, show the exact log path at the start and confirm save success or failure at the end.

## Log file resolution

Accept either `Log File:` or `Save As:` in the user brief.

Resolve the log path with these rules:

0. If the user passes `No Log`, `Log: none`, or `Log File: none`, skip all file writing. Do not resolve a path, do not create directories, do not save anything.
1. A bare filename such as `go-to-market-options` becomes `.claude/debate-logs/go-to-market-options.md`.
2. A filename with `.md` stays as given under `.claude/debate-logs/`.
3. A relative path with folders such as `notes/decisions/go-to-market-options.md` is used relative to the project root.
4. If omitted, default to `.claude/debate-logs/${CLAUDE_SESSION_ID}-options-challenge.md`.
5. Create parent directories if needed.

## Protocol

1. Extract or infer:
   - decision brief
   - goal
   - constraints
   - selected finalizer
   - resolved log path (skip if logging is disabled)
2. Claude frames `2-4 distinct options`.
3. Codex challenges each option:
   - strongest upside
   - major downside
   - execution risk
   - what must be true for it to work
4. Claude revises the framing and produces a preliminary ranking.
5. Codex pressure-tests the top-ranked option and the runner-up.
6. The finalizer produces:
   - final ranking
   - recommendation
   - why not the alternatives

## Required chat format

- `Log Path` (omit if logging is disabled)
- `Decision Brief`
- `Option Set`
- `Codex Challenge`
- `Top Options Stress Test`
- `Revised Ranking`
- `Final Recommendation`
- `Why Not The Alternatives`
- `Key Assumptions`

## Logging requirements

If the user opted out of logging, skip this entire section — do not write any files and do not print log status lines.

Write the same visible output to the resolved log path.

If the file already exists, append a new entry unless the user explicitly asks to replace it.

Each saved entry must contain:

- date or session context if available
- raw user brief
- selected finalizer
- resolved log path
- every visible section from the answer

After saving, end with:

`Log saved: <path>` or `Log failed: <reason>`.

## Quality bar

- Options must be materially different, not cosmetic variants.
- Ranking must follow explicit trade-offs, not vague preference.
- The final recommendation should say what to do now, not just what sounds best.

## Example invocation

`/options-challenge Finalizer: Claude. Log File: gtm-paths-q3. Decision Brief: Compare three GTM paths for an AI debate product: direct-to-student subscription, educator-led adoption, or partnerships with debate organizations. Constraints: tiny team, low sales capacity, need traction in one quarter.`
