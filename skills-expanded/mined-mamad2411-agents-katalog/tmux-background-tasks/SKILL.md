---
name: tmux-background-tasks
description: Run and manage long-lived background commands using tmux sessions instead of background processes. Use when starting backend/API servers, Expo/React Native dev servers, job workers, watchers, or any task that should keep running while other commands are executed.
---

# Tmux Background Tasks

If tmux is not installed, stop and ask the user to install it before proceeding.

## Overview

Use tmux to run and manage long-lived commands in the background. Do not keep these tasks alive with the default process tool; always launch them in tmux so they survive across commands and can be reattached.

## Workflow

1. Verify tmux is installed
If tmux is missing, stop and ask the user to install it (e.g., `brew install tmux` on macOS). Do not proceed until tmux is available.

2. Pick a stable session name
Use a predictable, unique name like `<repo>-<task>` (e.g., `myapp-api`, `myapp-expo`).

3. Start or reuse the session
Check for an existing session before starting a new one.

4. Provide attach/detach guidance
Tell the user how to attach to the session if they want to view logs or interact.

5. Stop or restart when requested
Terminate the session cleanly when the user asks to stop the task.

## Command Patterns

Check tmux:
- `command -v tmux`
- `tmux -V`

Create a new detached session running a command:
- `tmux new-session -d -s <name> -- <command>`
- If you need a login shell or env: `tmux new-session -d -s <name> -- bash -lc '<command>'`

Reuse or attach:
- `tmux has-session -t <name>`
- `tmux attach -t <name>`
- `tmux ls`

Send a stop signal or kill:
- `tmux send-keys -t <name> C-c`
- `tmux kill-session -t <name>`

Peek at recent output (non-interactive):
- `tmux capture-pane -pt <name> -S -200`

## Notes

- Prefer tmux for servers, watchers, workers, and dev tools that should remain running while other commands execute.
- Avoid creating duplicate sessions. If `tmux has-session -t <name>` succeeds, reuse it or attach.
