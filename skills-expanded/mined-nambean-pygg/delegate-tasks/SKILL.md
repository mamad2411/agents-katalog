---
name: delegate-tasks
description: Hand a self-contained coding subtask (a bug fix, tests, a refactor, a small feature) to cheaper agents through Pygg's MCP tools, then review and keep or discard the result. Use when the user asks to delegate, offload or run a subtask in the background or on a cheaper model, or names Pygg.
---

# Delegate a subtask through Pygg

Pygg runs the subtask in a separate Git worktree of this repository with other coding agents (OpenCode, Codex CLI, Claude Code, Gemini CLI), cheapest first, and checks each attempt with the checks the user approved for the workspace. The user's working tree is never changed: a result becomes a branch only when it is kept.

Pygg's task features are experimental. They need the Pygg app open (on macOS and Linux: `pygg gateway serve --tasks yes`) and a token allowed to start tasks, which the plugin asked for when it was enabled.

## Steps

1. **Pick a task that stands on its own.** The agent that runs it does not see this conversation. Write the whole task in `prompt`: what to change, in which files, and what done looks like (a test that passes, a command that succeeds).
2. **Start it** with `pygg_run_task`. Give a short `title` (it names the branch). Leave `steps` and `strategy` unset unless the user chose agents: the default tries the free and cheap agents first. Set `allow_shell` only when the user allowed shell commands.
3. **Wait** with `pygg_task_status`. A call waits up to 50 seconds; call it again while the task runs. Say what is happening between calls rather than calling silently many times.
4. **Review** with `pygg_task_diff` before telling the user it is done. Read the change; do not trust the agent's summary.
5. **Keep or discard** only as the user decides: `pygg_keep_result` makes a branch, `pygg_discard_result` throws it away. `pygg_stop_task` stops a running task.

## Things that wait for the user

- **A paid step waits for approval in the Pygg app.** No tool approves it. When `pygg_task_status` says a step waits for approval, tell the user to approve or decline it in Pygg.
- A task that changed a file defining a check (`package.json`, `Cargo.toml`), or one in a workspace with no approved checks, ends as `needs_review` and `pygg_task_status` says NOT READY: `pygg_keep_result` refuses it unless `accept_unchecked` is true. Read the whole diff first, and tell the user it is kept unchecked. Better: ask the user to approve a check in the Pygg app (it suggests some, each with what it covers), then `pygg_check_result` checks the result as it is.

## Other tools

- `pygg_agents`: the agents Pygg found on this computer and how they sign in.
- `pygg_list_tasks`: this client's tasks.
- `pygg_model_facts`: the connected models ranked for a role (plan, code, test, review).
- `pygg_brainstorm`, `pygg_board`, `pygg_board_move`: the board of a brainstorm started by asking for the model `pygg/brain` through the gateway; cards move only between Discovery and Ready from here.

## When something fails

- "PYGG_TOKEN is not set" or an authorization error: the token is missing or not allowed to start tasks. Ask the user to update the plugin's settings with a token from Endpoint → API Keys that has **May start tasks** on.
- "Pygg is not reachable": the app (or `pygg gateway serve --tasks yes`) is not running.
- "Pygg was not found": neither the app nor the `pygg` command line is installed.
