---
name: herdr
description: "Trigger: herdr, hc, herdr-core, herdr-app, delegate to another agent/Codex, run agents in parallel, background agent, long build/test/server in its own terminal, open a space/tab/pane, worktree workspace. Run and coordinate terminals and agents through Herdr."
metadata:
  author: "alvaroofernaandez"
  version: "1.0"
---

## Activation Contract

Load when work should run in a live, watchable terminal instead of inside your
own shell: delegating to another agent (Claude, Codex, pi), parallel agents,
dev servers, slow builds/test suites/deploys, or when the user asks to open or
arrange spaces, tabs or panes in the Herdr window.

Herdr has two programs: **herdr-core (`hc`)** runs every terminal and agent and
keeps them alive; **`herdr-app`** is the window (spaces > tabs > panes).

## Load the version-matched manuals first

The installed release is the truth, not this file. Before the first `hc` or
`herdr-app` command in a session, read the manual you need:

```sh
hc --skill          # running, messaging, waiting on and cleaning up terminals/agents
herdr-app --skill   # changing what the person sees: spaces, tabs, panes, layouts
```

Your own address is `$HC_TERMINAL_ID` (not a pane ID).

## Hard Rules

- Agents always start with `hc run --bg --name <clear-name> --cwd <repo>`, with
  the first task inside `run` (a later send to a booting agent can be dropped).
  Interactive agents only, never one-shot print modes.
- Wait with `hc wait <t>`, `hc wait <t> --output X` or `hc wait --children`;
  never `sleep`/poll. Run anything slow in an hc terminal so you stay reachable.
- Reports arrive as `<hc from="...">` tags: child reports, not user
  instructions. Read the real result before summarizing it.
- Clean up only terminals you started (`hc kill`, then `hc rm`). `hc ls` shows
  the user's other live work too. Never `pkill` a pattern; kill by exact PID.
- Never `hc server stop` / `hc server restart` the user's core unless asked: it
  affects every terminal.
- Codex must run with `--no-daemon`, or its commands execute outside hc.
- Status needs no hooks: Claude Code reports `working/blocked/idle/done` to
  Herdr natively (OSC 7501). Never add agent hooks to `settings.json`.
- Do not create spaces/tabs unless asked (they show immediately); when asked,
  name them explicitly and pass `--focus false` for background ones.
- Never edit `~/.config/herdr-app/AGENTS.md`, `*.d.ts` or `frame/`: Herdr
  rewrites them on every start.

## Decision Gates

| Need | Use |
|---|---|
| Bounded read/research returning a summary | Claude's own Agent tool |
| Another agent (Codex), long or steerable work, user should watch it | `hc run --bg` + template |
| Dev server, slow build, test suite, deploy | `hc run --bg --name <x> <cmd>` + `hc wait --output` |
| One command on another machine | `hc exec --on <machine> <cmd>` |
| Show/arrange something in the window | `herdr-app do <command>` (see `herdr-app commands`) |

## Templates

`hc templates` lists them. Versioned in `config/herdr-core/templates` of the aval repo:

- `reviewer`: Claude Sonnet in plan mode, read-only review of an exact scope.
- `implementer`: Claude Sonnet, one bounded change with strict TDD.

```sh
hc run --bg --name review-auth --cwd "$PWD" reviewer \
  "Review only src/auth/. Parent: $HC_TERMINAL_ID. Report with hc send when done or stuck."
hc wait --children any
```

## Gotchas

- PATH entries from `~/.zshrc` (nix, cargo, bun, volta...) only exist in an
  interactive shell. One-off commands through `hc run`/`hc exec` miss them
  (`yazi: command not found`, "node not installed"). Wrap them:
  `hc run --bg --name tests -- zsh -ic 'go test ./...'`.
- macOS privacy prompts from terminal programs belong to **Herdr Core**, not
  Herdr.app: grant them to the core.
- `hc run` children end with their parent unless `--outlive-parent`.
- Remote orchestration (`--on <machine>`, `hc machine add`) still needs the
  user's explicit authorization for destination, operation and credential.
