---
name: lmux
description: Drive the lmux terminal from inside it - open a workspace running another agent (Codex, Claude Code, any CLI), wait for it to finish or need the user, and read its result. Use when running in an lmux pane ($LMUX_PANE_ID is set) and the user asks to hand work to another agent, run something in a new workspace, or wait for another pane.
---

# lmux

You're in an lmux pane when `$LMUX_PANE_ID` is set; the `lmux` command is on `PATH`. Full
reference: https://github.com/sooftware/lmux/blob/main/docs/agents.md

## Commands

- `lmux new-workspace --background --cwd DIR --cmd "CMD"` opens a workspace running CMD without
  switching the user's screen to it, prints `workspace <id> pane <id>`. Always pass `--background`. Put the other agent's whole task in CMD
  (`codex 'Review …'`, `claude 'Fix …'`): from inside a pane, `lmux send` only types into your
  own pane.
- `lmux list --json`: every pane's `id`, `state` (`idle`, `running`, `needs input`, `done`,
  `failed`), `agent` (`claude`, `codex`, another agent's name or `""`), `session`, `cwd`,
  `title`, `workspaceTitle`.
- `lmux wait ID [--until done|needs-you|idle|any] [--timeout SECS] [--json]` blocks until the pane
  (or workspace) gets there. Default: until it's not running. Prints the state, then the reply
  of a done turn or the row's detail; `--json` adds `reply` (the last reply, when the agent's
  hooks gave it), `agent`, `session`. Exit 0 got there, 1 timeout, 2 target gone, 3 error.
- `lmux notify "TEXT"` notifies the user from your pane.

## Hand a task to another agent

```sh
out=$(lmux new-workspace --background --cwd "$PWD" --cmd "codex 'Review the uncommitted changes. Write your findings to .review.md.'")
pane=${out##* }
lmux wait "$pane" --until done --timeout 1800 && cat .review.md
```

- Ask the other agent to write its result to a file: its last reply can be cut short or missing.
- If `lmux wait "$pane"` returns `needs input`, the other agent is waiting for an approval or an
  answer. Tell the user which workspace needs them; don't try to answer it yourself.
- Always pass `--timeout`: a wait whose target never changes state never ends. Say what happened
  on exit 1 or 2 instead of retrying blindly.
- Don't close or type into panes you didn't open.
