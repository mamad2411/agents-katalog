---
name: session-hygiene
description: >-
  use this when you need portable session habits that work in any harness —
  context-floor checks, rewind options, permission discipline, and
  starting-context hygiene
license: MIT
metadata:
  portability: portable
---
# session-hygiene

Harness-agnostic habits for a clean agent session. Command names live in the
matching `*-habits` adapter. There is no `docs/HARNESS-MATRIX.md`.

## Session checks
Check your context floor after big operations; watch for silent jumps.
Use your harness's floor command (see the matching `*-habits` skill).

Confirm cwd is the named product before editing. `pwd` and `git remote -v`.
Wrong repo is a stop. Do not clean unrelated dirty files.

## Rewind options (escalating)
1. **Cancel mid-run / undo** — rewind a few messages.
2. **Conversation rewind** — back to a chosen point. Use your harness's rewind
   command (see the matching `*-habits` skill).
3. **Fresh scoped session** — start clean for a bounded task.
4. **Git recovery** — `git diff`, `git stash`, `git reset` as the last resort. Git is the ground truth.

## Working with the human's tools
- Select code, then ask — selection-scoped answers.
- Use diff views; two panes side by side when comparing.
- **Don't fight the IDE** — let it own formatting/lint.

## Execution modes
- Foreground for interactive; **background** for long jobs you monitor.
- If the harness blocks a command, prefer the supported path over forcing it.

## Permissions
Manage what the agent may run without asking. Approve deliberately;
**never blanket-allow destructive commands**.

## Starting-context hygiene
Keep starting context lean (see kill-context-bloat). Back up harness
settings and the skills directory before labs that reset harness config.

## Watch
Settings-file confusion (which file is active), skills confusion (which
skill actually fired), auto-update breakages. A settings edit is not live
until the harness relaunches.

## Anti-patterns
- Copying skill text into the product `AGENTS.md`.

## Related
kill-context-bloat · compact · cursor-habits · codex-habits · copilot-habits · gemini-cli-habits · claude-code-habits
