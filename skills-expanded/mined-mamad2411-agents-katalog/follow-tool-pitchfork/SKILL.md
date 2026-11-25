---
name: follow-tool-pitchfork
description: Set up and use pitchfork to manage project daemons/processes
argument-hint: "[daemon-or-scope]"
related:
  - follow-tool-mise
  - follow-tool-github-actions
  - follow-tool-cargo
  - use-scripts
---

## Goal

Manage background daemons with pitchfork for development workflows

## Scope

Covers `pitchfork.toml`, daemon lifecycle, ready/health checks, shell hooks, file watching, cron, port management/reverse proxy, TUI, Web UI, MCP server, boot start, and container mode

- Use this skill for long-running background daemons — for one-off scripts or a task runner use `/use-scripts` or `mise` tasks via `/follow-tool-mise` instead

- Latest: `pitchfork@2.27.0` (crate `pitchfork-cli`) (verified 2026-09-26)
- Architecture: CLI/TUI/Web UI → supervisor → daemon processes (the supervisor auto-starts when a client needs it)

## Execute

### 1. Install

> Goal: have the pitchfork CLI ready

1. Recommended via `mise`: `mise use -g pitchfork` (global) or `mise use pitchfork@<version>` (pinned per project)
2. Alternatives: `cargo install pitchfork-cli --locked` or binaries from GitHub releases (builds exist for macOS, Linux, Windows)
3. If the project has no mise, do `/follow-tool-mise` first
4. Confirm with `pitchfork --version`
5. Install shell completion with `pitchfork completion <bash|zsh|fish>` (separate from the shell hook)
6. On Windows: the default daemon shell is `cmd /C` — for POSIX behavior put `sh.exe` on PATH and set `general.shell = "sh -c"`
7. See details in 

### 2. Create Configuration

> Goal: define the project's daemons

1. Create `pitchfork.toml` in the root or `.config/pitchfork.toml` with the schema line: `#:schema https://pitchfork.jdx.dev/schema.json`
2. Define `[daemons.<name>]` with `run = "..."` — use a foreground command; never `&` or daemonize flags
3. Use `ready_http`, `ready_output`, `ready_port`, `ready_cmd`, `ready_delay` for ready checks (object form accepted: `{ ..., timeout = "30s" }`)
4. Use `health_http`, `health_cmd`, `health_port` for health probes over the daemon's lifetime
5. Use `port` to assign ports (`port = 3000`, `port = [8080, 8443]`, or `port = { expect = [3000], bump = 10 }`) — the resolved port is in `$PORT`, `$PORT0..N`
6. Use `depends` for dependency ordering and `retry` (`0|N|true`) for auto-restart
7. Use `auto = ["start", "stop"]` for shell hooks, `watch` + `watch_mode` for restart on change, `cron` for scheduling, `boot_start` for start at login
8. Use the top-level `[env]` for shared env and per-daemon `env` — use the Tera template `{{ daemons.<name>.port }}` to wire services together
9. Use `pitchfork.local.toml` for local overrides (not committed) and `[groups.<name>]` for batch operations
10. See details in 

### 3. Manage Daemons

> Goal: start/stop/monitor daemons

1. `pitchfork start --all` (`-a`), `--local` (`-l`), `--global` (`-g`), `--group <name>`, or `pitchfork start <id>…`
2. `pitchfork list` (`--project`, `--namespace`, `--status`, `--json`) to see both running and available daemons
3. `pitchfork status <id> --json` for one daemon's details
4. `pitchfork logs <id> --tail` follows logs; filter with `--grep`, `--regex`, `--level`, `--field`, `--jq`, `--since/--until`, `-n`
5. `pitchfork stop <id>` or `--all`/`--local`/`--group` — graceful stop (SIGTERM → SIGKILL, reverse dependency order)
6. `pitchfork restart <id>` to apply config changes then restart (= `start --force`)
7. `pitchfork run <id> -- <cmd>` for an ad-hoc daemon without a config file; `pitchfork wait <id>` blocks until the daemon stops
8. `pitchfork enable|disable <id>` controls whether a daemon may start; `pitchfork clean [--prune]` removes stopped entries
9. `pitchfork daemons add <id> --run '...'` adds a daemon to the config from the CLI (`--local`, `--global`, `--watch`, `--cron-schedule`, etc.)
10. Use the qualified ID `namespace/name` when working outside the project directory
11. See details in [references/cli.md](references/cli.md)

### 4. Shell Hook & Project Sessions

> Goal: auto-start/stop when entering/leaving a directory

1. Add `eval "$(pitchfork activate bash)"` to `.bashrc` (zsh: `activate zsh`, fish: `pitchfork activate fish | source`)
2. Use `auto = ["start"]` to start on enter, `auto = ["stop"]` to stop on exit, `auto = ["start", "stop"]` for both
3. Autostop waits `general.autostop_delay` (default `1m`) after the last session leaves — set it in `[settings.general]`
4. IDEs/tools use `pitchfork project enter --pid <PID> [--directory <DIR>]` / `leave` / `list --json` instead of the shell hook
5. PID per shell: `$$` (bash/zsh), `$fish_pid` (fish), `$SHELL_PID` (nushell)
6. On Windows, crashed sessions aren't cleaned up automatically — run `project leave` yourself
7. See details in 

### 5. Lifecycle Hooks

> Goal: react to daemon events

1. Define `[daemons.<name>.hooks]` with `on_ready`, `on_fail`, `on_retry`, `on_stop`, `on_exit`, `on_output`
2. `on_output` takes a shorthand string or `{ run, filter?, regex?, debounce? }` (filter/regex are mutually exclusive)
3. Hooks are fire-and-forget and run in the background — they never block the daemon — don't use `on_ready` for setup that must finish before serving
4. Available environment variables: `PITCHFORK_DAEMON_ID`, `PITCHFORK_DAEMON_NAMESPACE`, `PITCHFORK_RETRY_COUNT`, `PITCHFORK_EXIT_CODE`, `PITCHFORK_EXIT_REASON`, `PITCHFORK_MATCHED_LINE`, `PITCHFORK_PORT0..N`
5. See details in 

### 6. Ports, Proxy & Dashboards

> Goal: stable URLs and monitoring UIs

1. Enable the reverse proxy in `~/.config/pitchfork/config.toml`: `[settings.proxy] enable = true` — the slug URL `https://<slug>.localhost` stays stable even when the port changes
2. Manage slugs with `pitchfork proxy add <slug> [--dir --daemon]`, `proxy status`, `proxy remove`, `proxy trust`/`untrust` (HTTPS cert)
3. `pitchfork tui [--namespace|--project]` for the terminal dashboard (vim keys, `?` for help)
4. Web UI: `PITCHFORK_WEB_PORT=3120 pitchfork supervisor start --force` or `[settings.web] auto_start = true`
5. MCP server: client config `{ "command": "pitchfork", "args": ["mcp"] }` — tools: status, start, stop, restart, logs
6. Use `mise = true` per daemon (or `[settings.general] mise = true`) when a daemon needs mise tools/env outside an interactive shell
7. `pitchfork boot enable` registers the supervisor at login (macOS launchd / Linux systemd) + `boot_start = true` per daemon
8. See details in  and [references/apis.md](references/apis.md)

## Rules

### 1. Naming & Namespaces

- Daemon names allow ASCII alphanumeric, `_`, `-`, `.` only — no double dashes, slashes, spaces, leading/trailing dashes, or parent references
- IDs come in two forms: short `api` and qualified `frontend/api` (`--` is reserved for internal encoding)
- The namespace defaults to the directory name unless `namespace = "..."` is set — the global config uses the namespace `global`
- If the directory name isn't valid, a top-level `namespace` must be set in the config, otherwise parsing fails
- Git worktrees automatically get a namespace from the directory name (disable with `general.worktree = false`)

### 2. Configuration

- Precedence within a directory: `.config/pitchfork.toml` → `.config/pitchfork.local.toml` → `pitchfork.toml` → `pitchfork.local.toml` (highest, not committed)
- Prefix the final command with `exec` so the PID matches the daemon binary: `run = "cd /app && exec node server.js"`
- Multiple ready checks are "any", not "all" — if every check times out, startup fails with exit code `124`
- `ready_delay` is only a fallback when no other check exists (default 3s)
- Health-check `retries` = failed probes; daemon `retry` = restart attempts — different things
- Deprecated: `expected_port`, `auto_bump_port`, `port_bump_attempts` — use `port = { expect = [...], bump = N }` instead

### 3. Example pitchfork.toml

```toml
#:schema https://pitchfork.jdx.dev/schema.json

[env]
APP_ENV = "development"

[daemons.redis]
run = "exec redis-server --port $PORT"
port = { expect = [6379], bump = 10 }
ready_cmd = { run = "redis-cli -p $PORT ping", timeout = "15s" }

[daemons.api]
run = "exec node server.js"
port = 3000
depends = ["redis"]
env = { REDIS_URL = "redis://127.0.0.1:{{ daemons.redis.port }}" }
ready_http = { url = "http://127.0.0.1:3000/health", timeout = "30s" }
health_http = { url = "http://127.0.0.1:3000/health", interval = "10s", retries = 3 }
watch = ["src/**/*.ts", "package.json"]
auto = ["start", "stop"]
retry = 3

[daemons.backup]
run = "./scripts/backup.sh"
cron = { schedule = "0 0 2 * * *", retrigger = "finish" }
mise = true

[daemons.api.hooks]
on_fail = "echo 'api failed: $PITCHFORK_EXIT_CODE'"
on_output = { filter = "connected", run = "echo 'api ready'" }

[groups.backend]
daemons = ["redis", "api"]
```

### 4. Common Commands

- `pitchfork start --all` / `pitchfork run demo --port 8000 -- python3 -u -m http.server 8000`
- `pitchfork list --project` / `pitchfork status api`
- `pitchfork logs api --tail` / `pitchfork logs api --level error --jq '.fields.status >= 500'`
- `pitchfork restart api` / `pitchfork stop --local` / `pitchfork wait api`
- `pitchfork tui` / `pitchfork supervisor start --force` / `pitchfork logs pitchfork`
- `pitchfork settings get general.autostop_delay` / `pitchfork settings explain <key>`
- `pitchfork project enter --pid $$` / `pitchfork project leave --pid $$`
- `pitchfork proxy add api` / `pitchfork boot enable` / `pitchfork mcp`

- Use /follow-tool-mise if needed (mise integration)
- Use /follow-tool-github-actions if needed (tool pitchfork)
- Use /follow-tool-cargo if needed

## References
- [CLI reference](references/cli.md)
- [HTTP API & MCP](references/apis.md)
- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- pitchfork installed and working through mise
- `pitchfork.toml` defines the full daemon set with ready/health checks, dependencies, retry
- Daemons auto-start/stop via the shell hook or IDE project sessions
- File watching, cron, port bumping, reverse proxy, lifecycle hooks used as needed
- Monitoring via `pitchfork list`, `logs`, `tui`, the Web UI, or the MCP server
