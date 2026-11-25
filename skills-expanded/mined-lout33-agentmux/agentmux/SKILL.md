---
name: agentmux
description: Use when working with agentmux, tmux-backed agent supervision, project managers, project workers, the local agentmux web UI, or durable terminal agent runtimes. Trigger on requests like create a worker, start a manager, supervise agents, attach to a worker, send input to an agent, import a tmux session, open the dashboard, or coordinate terminal agents in one repo.
---

# agentmux

Use `agentmux` as the supervision layer over `tmux`.

Core model:

- `tmux` keeps runtimes alive
- `agentmux` tracks durable agent identities, state, logs, and events
- prefer `agentmux` commands over raw `tmux` when the runtime should stay supervised

Default behavior:

- prefer `shell` harness for project managers and project workers unless the user explicitly wants `opencode`, `claude`, `codex`, `pi`, or `custom`
- use `opencode` harness only when the user specifically wants an OpenCode runtime inside the managed session
- if the user wants a plain terminal they can later attach to, use `shell`

Main commands:

```bash
agentmux ls
agentmux show <agent>
agentmux logs <agent>
agentmux attach <agent>
agentmux send <agent> "<text>"
agentmux stop <agent>
agentmux kill <agent>
agentmux resume <agent>
agentmux delete <agent> --force
agentmux events --session <agent>
agentmux watch
agentmux console
agentmux web --open
```

Project workflows:

- create a manager for a repo or lane:

```bash
agentmux project-sync <project> --workdir <repo-path> --harness shell
```

- create a project worker:

```bash
agentmux worker <project> <agent-name> --workdir <repo-path> --harness shell
```

- scope supervision to one project:

```bash
agentmux ls --project <project>
agentmux watch --project <project>
agentmux console --project <project>
agentmux events --project <project>
```

Import workflow:

- if a runtime already exists in tmux, adopt it instead of recreating it
- discover untracked sessions first:

```bash
agentmux discover
```

- import an existing session:

```bash
agentmux import --agent <name> --tmux-session <tmux-session> --harness <harness>
```

- for imported OpenCode sessions, include the native session id when known:

```bash
agentmux import --agent <name> --tmux-session <tmux-session> --harness opencode --session-id <ses_id>
```

Operator guidance:

- use `agentmux console` for terminal-first supervision with selection, logs, and prompt sending
- use `agentmux web --open` for browser-based project boards and per-project general-agent control
- use `agentmux attach <agent>` when the user wants direct terminal control of a runtime
- use `agentmux send <agent> "..."` for one-shot steering without attaching
- use `agentmux logs <agent>` or `agentmux show <agent>` before making assumptions about runtime state

Important details:

- local state lives in `.agentmux/agentmux.db`
- project manager and worker flows now default to `shell`; do not switch them to `opencode` unless requested
- `agentmux` runtime state is heuristic, so verify with `show`, `logs`, `attach`, or `watch` when status is unclear
- if `tmux` is missing, `agentmux` cannot operate

Opencode harness flags:

- `--model provider/model` — model override passed as `--model` to the `opencode` binary
- `--session ses_xxx` — resume an existing OpenCode session by passing `-s ses_xxx` to the `opencode` binary
- these flags only have effect on the `opencode` harness; other harnesses ignore them

Examples:

```bash
agentmux project-sync agentmux --workdir /absolute/path/to/agentmux --harness shell
agentmux worker agentmux researcher --workdir /absolute/path/to/agentmux --harness shell
agentmux send researcher "inspect the failing route and report back"
agentmux attach researcher
agentmux web --open
```

Autonomous explorer projects:

An "autonomous explorer" project gives an agent an open-ended goal and lets it self-direct. The manager monitors progress, unblocks when the agent needs human action, and updates the project tracker.

```bash
# Create project manager
agentmux project-sync my-project --workdir /absolute/path/to/project --harness shell

# Add autonomous explorer workers
agentmux worker my-project explorer-1 --workdir /absolute/path/to/repo1 --harness opencode
agentmux worker my-project explorer-2 --workdir /absolute/path/to/repo2 --harness codex

# Send initial mission
agentmux send explorer-1 "Read AGENTS.md. Start working toward the goal. Ask the human when you need external steps."

# Monitor
agentmux watch --project my-project
agentmux logs explorer-1
```

Workflow:
1. Create the project with `project-sync`
2. Add workers with `worker`
3. Send each worker its contract/mission as the initial prompt
4. Monitor via `logs` and `watch` — intervene only when stuck or needing human action
5. Kill and delete workers when the project is paused or killed
