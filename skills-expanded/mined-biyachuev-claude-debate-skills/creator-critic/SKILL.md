---
name: creator-critic
description: Run a two-voice idea loop where one side generates options and the other side pressure-tests them. Use for concepts, positioning, campaigns, product ideas, and strategic directions.
argument-hint: "[brief, optional creator, optional critic, optional finalizer, optional log file]"
disable-model-invocation: true
---

# Creator Critic

Use this skill when the user wants breadth first, then pressure-testing, then a tightened recommendation.

Treat `$ARGUMENTS` as the full brief.

## Default roles

- `Creator`: Claude
- `Critic`: Codex
- `Finalizer`: Claude

If the user overrides these roles, follow the override.

## Non-negotiable rules

1. If Codex is required by the selected roles and is not available, say that explicitly and stop. Do not fabricate Codex output.
2. Show both voices in the chat. Do not summarize one of them away.
3. Unless the user opted out of logging, save the full visible output to a resolved log path.
4. If logging is enabled, show the exact log path at the start and confirm save success or failure at the end.

## Log file resolution

Accept either `Log File:` or `Save As:` in the user brief.

Resolve the log path with these rules:

0. If the user passes `No Log`, `Log: none`, or `Log File: none`, skip all file writing. Do not resolve a path, do not create directories, do not save anything.
1. A bare filename such as `pricing-ideas` becomes `.claude/debate-logs/pricing-ideas.md`.
2. A filename that already ends with `.md` stays as given under `.claude/debate-logs/`.
3. A relative path with folders such as `notes/brainstorms/pricing-ideas.md` is used relative to the project root.
4. If omitted, default to `.claude/debate-logs/${CLAUDE_SESSION_ID}-creator-critic.md`.
5. Create parent directories if needed.

## Protocol

1. Extract or infer:
   - brief
   - goal
   - explicit constraints
   - creator
   - critic
   - finalizer
   - resolved log path (skip if logging is disabled)
2. The creator produces `3-5 options` or angles.
3. The critic reviews each option:
   - strongest value
   - biggest flaw
   - hidden assumption
   - likely failure mode
4. The creator produces `Creator v2`:
   - revise good options
   - discard weak options
   - narrow to `1-3 strongest`
5. The finalizer produces a recommended direction.
6. Add open risks and immediate next moves.

## Required chat format

- `Log Path` (omit if logging is disabled)
- `Brief`
- `Creator v1`
- `Critic Review`
- `Creator v2`
- `Final Recommendation`
- `Open Risks`
- `Next Moves`

## Logging requirements

If the user opted out of logging, skip this entire section — do not write any files and do not print log status lines.

Write the same visible output to the resolved log path.

If the file already exists, append a new entry unless the user explicitly asks to replace it.

Each saved entry must contain:

- date or session context if available
- raw user brief
- selected roles
- resolved log path
- every visible section from the answer

After saving, end with:

`Log saved: <path>` or `Log failed: <reason>`.

## Quality bar

- Prefer distinct options over minor variations.
- Make the critic genuinely adversarial but useful.
- Keep the creator from defending weak ideas just to preserve volume.
- End with a clear recommendation, not just a list.

## Example invocation

`/creator-critic Creator: Claude. Critic: Codex. Finalizer: Claude. Log File: pricing-brainstorm. Brief: Generate and pressure-test pricing concepts for an AI debate copilot for students and coaches. Constraints: low-trust market, need simple plans, avoid enterprise sales.`
