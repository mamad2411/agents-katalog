---
name: claude-code-habits
description: >-
  use this when starting a Claude Code session, after a bad run you want
  to rewind, or before changing what the agent may run — /context checks,
  rewind options, bash modes, permission hygiene
license: MIT
metadata:
  portability: claude-code
---
# claude-code-habits

Claude Code instance of **session-hygiene** — read that skill first for the
portable doctrine. This skill is only the Claude-Code-specific mechanics.

## When
- Starting a Claude Code session — check `/context` early.
- After a bad run you want to rewind — escalate through the rewind options below.
- Before changing what the agent may run — review `/permissions`.
- Before labs that reset harness config — back up settings + skills first.

## Session checks
- `/context` — verify your context floor after big operations; watch for silent jumps.

## Rewind options (escalating)
1. **Undo / escape-cancel** — cancel mid-run, rewind a few messages.
2. **`/rewind`** — rewind to a point in the conversation.
3. **Slash-command session** — start a clean, scoped session.
4. **`git` recovery** — `git diff`, `git stash`, `git reset` as the last resort. Git is the ground truth.

## Slash commands worth knowing
- `/model` — check the model; switching mid-task changes behavior.
- `/permissions` — manage what the agent may run without asking.
- `/agents` — subagent management.

## Bash modes
- Foreground for interactive; **background** (`&`-style runs) for long jobs you monitor.
- If the harness blocks a command, prefer the supported path over forcing it.

## Settings backup
Back up your settings file (`~/.claude/settings.json`) and skills
directory before labs that reset harness config.

## Anti-patterns
- Forcing a blocked command instead of taking the supported path.
- Running a lab that resets harness config without backing up settings + skills.
- Launching a background run and not monitoring it.

## Related
session-hygiene
