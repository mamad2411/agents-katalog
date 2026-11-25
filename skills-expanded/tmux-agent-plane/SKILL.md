---
name: tmux-agent-plane
description: >-
  The system-wide index of the user's coding agents (Claude Code, Codex, Pi, OpenCode, Antigravity, Grok Build) across every tmux session, and the only way to work with them, through the `tmux-agent-plane` CLI. Load it first, before any tmux command, whenever a task touches another agent: the user names an agent (`claude-154`, `codex-26`, `reviewer`) or a pane, asks how an agent is doing or what agents are running, wants to check on, read, message, answer, wait for, show, close, start or spawn an agent (in a pane, window or session), wants work delegated to another agent, or wants a super agent that coordinates others, or asks to organize tmux sessions, clean up tmux projects or organize work into projects.
---

# tmux-agent-plane

A background daemon tracks Claude Code, Codex and Antigravity in the user's tmux. Pi and OpenCode require their opt-in publishers; Grok Build requires official leader mode and is currently supported on macOS. See the repository README More agents for installation. Without an optional integration, that kind stays untracked. Each agent has a name (`claude-154`, or one given at spawn), a tmux pane id (`%154`) and a state:

- `working`: running a turn.
- `blocked`: waiting on a person: a question, a permission prompt, a dialog. `detail` says what, when the agent reports it.
- `done`: finished a turn nobody has looked at yet.
- `idle`: ready for input, already seen.

You appear in this list when your kind's tracking requirements are met. `list` marks you with `*` (or `"self": true` in JSON) when caller identity is reliable.

## User configuration

When you load this skill, read `${XDG_CONFIG_HOME:-$HOME/.config}/tmux-agent-plane/config.toml` if it exists. It holds the user's preferences for agents using this skill and overrides this skill's defaults. When it is absent, use the defaults below.

- `instructions`: a list of rules; follow every one.
- `[spawn.<kind>]`: when you spawn that kind, pass its `args` after `--`, each array item as one shell-quoted argument (`spawn codex "<task>" ... -- '-m' 'gpt-6.1-sol'`), and follow its `instructions`. When the user's request names a different value for one of those options, use the user's value for that option.

## First: name yourself

The user tells agents apart by name. Preserve a name already assigned in your task. When you load this skill, run `list`. Codex callers have no self marker: use an explicit name supplied in your task, and never run `rename self` or use `$TMUX_PANE`. Other callers whose own marked name is still the default `<kind>-<number>` (`claude-154`) name themselves after their task:

```bash
tmux-agent-plane rename self <name>
```

A name is one short kebab-case word for the work, 2 to 3 words joined by `-`, at most 20 characters: `auth-refactor`, `billing-tests`, `release-notes`. Never rename an agent the user has already named.

Optional AI auto-naming is off by default and configured by the user with `o` in the sidebar. This bottom-left menu also sets per-kind launch model and effort defaults in config.json; the launcher and `spawn` apply them when no explicit agent arguments are supplied. Use arrows/j/k to select, Enter/Space to choose or toggle, Accept to close, and Esc/Ctrl+C to leave. It only names agents with a meaningful title and an unassigned default name. Explicit `--name`, `rename` and sidebar `r` assignments are always preserved.

## Caller identity

Codex tool shells can inherit `TMUX_PANE` from a shared app-server. Their `CODEX_THREAD_ID`/`CODEX_SESSION_ID` identifies a thread, but current published files do not reliably associate that thread with its TUI pane. Never use `$TMUX_PANE` from a Codex tool shell. `list` works and marks no caller row for Codex. Use explicit agent names supplied in your task. If your own name is unknown, ask the lead to identify/name you. The CLI fails on Codex self references (including the inherited pane value) and `spawn --in pane`, since it cannot safely choose a caller pane. Use `spawn --in window` or `spawn --in session` and name yourself as the parent with `--parent <your name>`; spawn refuses a Codex caller without it, or with a name that is not a Codex agent. Do not unset Codex identity variables to bypass this error. Other callers may use `self`.

## Rule: the CLI, never raw tmux

Do every agent job through `tmux-agent-plane`: finding agents, reading their screens, typing into them, starting, showing and closing them. Never run `tmux list-panes`, `capture-pane`, `send-keys`, `split-window`, `new-window` or `kill-pane` against agents yourself. The daemon already indexes every agent in every session; `list` answers in one call what tmux would make you piece together, and the CLI keeps names, parents and done/seen state right. Raw tmux is fine only for panes that are not agents or tasks (a log tail you opened yourself). Long-running commands go through `task` (see Background tasks).

## Commands

```bash
tmux-agent-plane list                     # all agents: name, kind, state, where, parent, cwd, task
tmux-agent-plane list --json              # the same with every field
tmux-agent-plane sessions list [--json]   # projects: exact name/id, windows, clients, group, agents
tmux-agent-plane sessions create <name> [--cwd DIR] # new detached project with a shell
tmux-agent-plane move <agent> --session <session>  # existing exact session name or id
tmux-agent-plane read <agent> [--lines N] # its screen, plus N lines of scrollback
tmux-agent-plane send <agent> "<prompt>" [--answer] [--wait] [--timeout S]
tmux-agent-plane keys <agent> <key>...    # tmux key names: Enter Escape Up Down Tab 1 2 y n
tmux-agent-plane rename <agent> <name>     # one word, unique; `self` requires reliable caller identity
tmux-agent-plane wait <agent> [--timeout S]
tmux-agent-plane focus <agent>            # bring it on screen for the user
tmux-agent-plane toggle-sidebar self  # requires known caller identity; opens/closes every sidebar
tmux-agent-plane kill <agent>             # close its pane, ending it
tmux-agent-plane quota [--json]           # how much of each plan is left (Claude, Codex, agy, Grok), read fresh
tmux-agent-plane spawn claude|codex|pi|opencode|agy|grok ["<task>"] [--in pane|window|session] [--session SESSION] [--cwd DIR] [--name NAME] [--parent NAME] [--wait] [--timeout S] [-- AGENT_ARGS...]
tmux-agent-plane task list [--json]       # background tasks: state, ports, cwd, starter, command
tmux-agent-plane task start <name> [--cwd DIR] -- <command>...  # reuses a running task with the same command
tmux-agent-plane task read <name> [--lines N]
tmux-agent-plane task restart <name>      # rerun its command in the same window
tmux-agent-plane task stop <name>         # end it; it leaves the list
tmux-agent-plane restore                  # agents from before tmux restarted; lists only
tmux-agent-plane restore --tasks|--no-tasks|--discard  # bring them back (with tasks or not), or forget them
```

`<agent>` is a name, pane id, or `self` when caller identity is reliable. `read` and `keys` also take any pane id, including a pane whose agent has not started yet.

## Checking on an agent

1. `list` to see its state and task.
2. `read <agent>` to see what it is doing. Add `--lines 200` for more history.
3. Report the state and the gist of the screen. Do not paste the whole screen back.

## Starting an agent

- `spawn` passes the agent command directly to tmux’s `default-shell` as an interactive login shell command, after startup files load. Aliases and flags apply, long and multi-line tasks arrive intact, and a fresh interactive login shell stays when the agent exits. It supplies its own command rather than tmux’s `default-command`.
- `--in pane` (default) splits a known caller's pane. Codex callers must use `--in window` or `--in session`. Use a window for independent work or a session for a separate project; follow the requested placement when caller identity permits it.
- A tmux session is a project. Use `--in window --session api` to start work in the existing `api` project, or `--in session --session api` to create that named project with its first agent. `--session` requires one of those placements. Existing destinations accept exact names or session IDs from `sessions list`; there is no fuzzy matching or implicit creation. New session names must have no dots, colons, control characters or surrounding whitespace. `--name` names the agent separately. An explicit existing destination uses that session's configured shell.
- `spawn` placements are final. Only agents started by hand join a session named after their folder automatically, once, with any client viewing them.
- Give the full task as the prompt: the new agent has none of your context. Say which files, what done looks like, and what to report back.
- Always name agents you spawn (`--name reviewer`), following the naming rule above.
- Pass agent CLI flags after `--`: `spawn codex "<task>" --in window --name reviewer -- -m <model>`. Each argument reaches the agent verbatim, ahead of the task; `spawn` adds none of its own.
- `spawn` prints `<name> <pane> <location>`. The spawned agent records you as its parent: from your pane, or from `--parent` for Codex. The link lasts as long as the spawned agent; `list` shows `ended` once its parent has exited.
- A folder the agent has not trusted yet stops at a trust prompt, and `spawn` reports that the agent did not start. `read <pane>`, then answer with `keys <pane> ...` only when the user asked for that folder.

## Launch requirements

`spawn` chooses each kind's interactive syntax, with any `--` agent arguments first: `claude <args> <task>`, `codex <args> <task>`, `grok <args> -- <task>`, `pi <args> -- <task>`, `opencode <args> --prompt <task>`, and `agy <args> --prompt-interactive <task>`. Install the Pi/OpenCode publishers or enable Grok leader mode before spawning those kinds. `spawn agy` requires a task and fails immediately without one. An agy started by hand appears after its first message and native folder trust acceptance; before then, address its pane ID with `read` or `keys`. A spawn timeout can mean an optional integration is missing; read the pane and check the documented opt-in setup.

Antigravity named projects (including resumed/forked projects) and `--settings` overlays excluding the cwd from `trustedWorkspaces` stay untracked because live trust cannot be proven.

Pi/OpenCode publish durable completion counters. Other kinds are sampled once per second, so `send --wait` and task-bearing `spawn --wait` can time out if an entire turn finishes between polls. Do not report such a timeout as a successful test.

## Talking to an agent and waiting

- `send <agent> "<prompt>" --wait` pastes the prompt, presses Enter, and returns when that turn ends or the agent blocks. It prints `<name> <state>: <task>`.
- Ordinary `send` refuses a blocked target before sending any input. `send <agent> --answer "<text>"` deliberately replies to a blocked question and fails if the target is working, idle or done. With `--wait`, it follows the reply turn; the original question does not settle the wait. Never retry a refusal automatically with `--answer`.
- `spawn ... "<task>" --wait` returns when the first turn ends or the agent blocks.
- `wait <agent>` returns as soon as the agent is not `working`, so it returns at once for an idle agent. Use it to wait for work already running; use `send --wait` for work you start.
- A turn wait returns when the turn ends or blocks; plain `wait` also returns immediately for an already idle/done agent. Sampled kinds have the fast-turn limitation above. Pass `--timeout` shorter than your shell tool limit, or run the wait in the background, then `read` the result.
- A command fails loudly on a timeout, when the agent exits, or when the daemon is not running.

## Background tasks

Use `task start` for anything that must keep running after the command that starts it: dev servers, watchers, tunnels, queue workers. Never use `&`, `nohup`, `disown` or your own background shell for those; they would be invisible to other agents and to the user, and die or linger unpredictably.

1. Run `task list` first. If a running task already does what you need (same command, same folder), use it: read its port from the list instead of starting another.
2. Otherwise `task start <name> --cwd <dir> -- <program> <args>...`, with a short descriptive name such as `site-dev` or `api-watch`. The program is one plain word (`npm`, `python3`, `cargo`); for pipes or other shell syntax use `-- sh -c '...'`. Starting the same name with the same command and folder is safe: it prints `(already running)`, or reruns it if it had exited. A different command or folder under a taken name fails and shows who started that task; pick another name rather than stopping someone else's task.
3. It returns at once with `<name> <pane> <state>`. Check it came up with `task read <name>` (add `--lines 100` for more) and `task list` for its ports, which appear within a few seconds of the server listening.
4. `exited <code>` in the list means its command ended; `task read` shows why. `task restart <name>` reruns it in place.
5. Tasks outlive you. Stop only tasks you started (`started_by` is your name) and no longer need, or that the user asks you to stop: `task stop <name>`.

Tasks are never agents: they do not appear in `list`, and agent commands do not take task names. Never `move` agents into the `agent-plane-tasks` session or reorganize it; it holds tasks only.

## Restore after tmux restarts

When the tmux server dies, its agents can be brought back. `↺ N` in the status bar, or `restore` listing agents, means some wait. Restoring reopens their conversations and windows, so do it only when the user asks: run `restore` to show them the list, then `restore --tasks` (agents and the tasks that were running) or `restore --no-tasks` as they choose, or `restore --discard` if they want them gone. Report what it printed, including agents that stay closed and why (Codex cannot be resumed).

## Daemon diagnostics

A failed kind or observation is withdrawn while healthy agents keep tracking. The status bar shows active faults. Read `${XDG_STATE_HOME:-$HOME/.local/state}/tmux-agent-plane/daemon.log` for the full cause and recovery. Process/pane snapshot, index and log failures stop the watcher. `tmux-agent-plane daemon start` starts it when stopped; `tmux-agent-plane daemon restart` gracefully restarts the managed watcher on the current binary. Never guess a daemon PID or stop one with broad process matching.

## Blocked agents

Before **any status or escalation message**, inspect the target's current state with `list`. If it is blocked, defer the message or report through a lead whose current state permits a normal send. If no safe recipient is available, keep the report pending. **Status and escalation messages NEVER use `--answer`**, even when urgent or when a normal send refuses. A status update can be consumed as the answer to the target's question.

1. `read <agent>` to see the question or prompt.
2. Only when the answer is clear from the user's instructions, answer it: `keys <agent> 2` to pick option 2, `keys <agent> Enter` to confirm, `send <agent> --answer "<text>"` for a deliberate textual reply. Use `keys` for menus and permissions.
3. Otherwise, ask the user or escalate through a safe lead as above. Never guess credentials or approve a destructive or irreversible action on another agent's behalf without the user's say.

## Checking capacity

`quota` reads how much of each plan is left, fresh, and takes a few seconds. Run it before handing out a large batch of work, or when an agent reports a usage limit, then choose kinds with room left. In `--json`, each provider has `status` (`ok`, `stale`, `failed`, `not_set_up`, `needs_keychain`) and `groups`; each group has `percent_remaining` (the tightest window), `limiting_window` and `runway`: `on_pace` lasts to the reset, `empty_in` runs out first at `empty_at`, `exhausted_now`, or `unknown`. A failed provider says why in `error` and what to do in `remedy`; report it to the user rather than fixing logins yourself. Never press Enter for the user's Keychain consent.

## Working as a super agent

When coordinating several agents: spawn each with a self-contained task and a name, `send --wait` or `wait` on them, `read` their results, and check `list` for anything `blocked` or `done`. Give each agent its own files or worktree so they do not edit the same files. When the user wants to look at an agent, `focus` it. Close a finished agent only when the user wants it gone: `kill <agent>`.

## Organizing projects

Treat requests such as “organize my tmux sessions”, “clean up my tmux projects” or “organize my work into projects” as requests to organize the existing session/sidebar hierarchy. Each tmux session is one project, with its orchestrator and helpers inside it.

1. Inspect `sessions list --json` and `list --json`. The session inventory includes shell-only sessions, attached-client counts, window IDs, group membership and agent names. Linked agents appear in every session containing their window; `list` retains one canonical agent row. Use tasks, names, directories and parent links to understand the work and choose appropriate existing or new sessions. Read an agent if its task is unclear.
2. Create any needed project with `sessions create api --cwd /path/to/api`. Choose short, meaningful session names. Keep the user's established session/project boundaries.
3. Move each existing agent with `move reviewer --session api`. Move its orchestrator and helpers individually when they belong together. Each move detaches only that agent pane into a destination window; other agents and shells in a mixed source window stay there. Moving preserves the process, pane ID, name, parent and completion history, and sends no prompt or keys. It prints the new location immediately; the index/sidebar follows on the next daemon scan.
4. Start future helpers directly in that project: `spawn codex "<full task>" --in window --session api --cwd /path/to/worktree --name api-review`. Check `sessions list` and `list` to verify the result, then report the organization.

Moves keep destination clients on their current windows. A source window, and a detached session with no remaining content, may disappear naturally, including the plugin's lone-sidebar cleanup. A move that would end an attached source session is refused; leave another content pane/window there before retrying. Linked source windows and grouped source/destination sessions are refused because they share work across sessions. Report those limits rather than using raw tmux to bypass them. Existing shell-only windows remain for the user; organizing projects does not authorize killing agents or unrelated shells. Leave the `agent-plane-tasks` session alone: `sessions list` omits it and it is never a project.
