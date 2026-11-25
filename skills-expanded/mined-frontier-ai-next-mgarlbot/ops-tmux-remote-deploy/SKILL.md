---
name: ops_tmux_remote_deploy
description: Run remote deploy via SSH using tmux sessions (frps + app), with idempotent restart and health checks
triggers: [tmux, frps, frpc, remote deploy, deploy on server, run in tmux, session, daemon, background process, ssh deploy, запусти на сервере, через tmux, фрп, фрпс, удаленный деплой]
tools: [shell]
platform: all
---

## Remote deploy via tmux (single VPS baseline)

Use this skill when the user wants: "deploy on that server", "run frps and project in tmux", "keep processes alive after disconnect".

Always run commands on VPS via SSH wrapper:

```bash
ssh -F /data/.ssh/config vps 'REMOTE_COMMAND_HERE'
```

Never run host-level commands locally when the task is explicitly remote.

### Goal

Create and maintain two tmux sessions on the VPS:

- `frps` — FRP server process.
- `project_app` — project runtime process (docker compose or native command).

Both sessions must be idempotent and verifiable.

### Standard sequence

1. **Preflight**
   - Verify SSH connectivity.
   - Check core tools: `tmux`, `curl`, `ss` (or `netstat` fallback).
   - Install `tmux` if missing (non-interactive apt for Debian/Ubuntu).

2. **Prepare frps**
   - Ensure `frps` binary + config path are known (ask only if impossible to infer).
   - Restart `frps` session safely:
     - `tmux has-session -t frps` -> kill if exists.
     - start detached with explicit command and logs.

3. **Prepare app runtime**
   - If repo has compose files and user asked containerized deploy: use `docker compose up` in `project_app`.
   - Otherwise start provided app command in `project_app`.
   - Same idempotent session restart pattern as `frps`.

4. **Health checks (mandatory)**
   - `tmux ls` contains both sessions.
   - Process check (`pgrep -af frps`, app process or `docker compose ps`).
   - Port check with `ss -ltnp` for expected bind ports.
   - HTTP check with `curl -fsS` (or status code check) for app endpoint.

5. **Operational output**
   - Report only operational facts: session names, process status, listening ports, endpoint status.
   - Provide follow-up commands for logs:
     - `tmux capture-pane -pt frps -S -120`
     - `tmux capture-pane -pt project_app -S -120`

### Canonical command snippets

SSH preflight:

```bash
ssh -F /data/.ssh/config vps 'set -e; uname -a; command -v tmux >/dev/null || echo "__NO_TMUX__"'
```

Install tmux if required:

```bash
ssh -F /data/.ssh/config vps 'set -e; if ! command -v tmux >/dev/null; then DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y tmux; fi'
```

Restart `frps` session:

```bash
ssh -F /data/.ssh/config vps 'set -e; tmux has-session -t frps 2>/dev/null && tmux kill-session -t frps || true; tmux new-session -d -s frps "cd /opt/frp && ./frps -c /opt/frp/frps.toml"'
```

Restart app session (compose variant):

```bash
ssh -F /data/.ssh/config vps 'set -e; tmux has-session -t project_app 2>/dev/null && tmux kill-session -t project_app || true; tmux new-session -d -s project_app "cd /srv/myapp && docker compose up --build"'
```

Health checks:

```bash
ssh -F /data/.ssh/config vps 'set -e; tmux ls; pgrep -af frps || true; ss -ltnp | sed -n "1,120p"; curl -sS -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8080/'
```

### Rules

- Do not claim success until all mandatory checks pass.
- If checks fail, inspect tmux panes and fix one issue per iteration.
- Do not dump `.env`, private keys, or full secret-bearing configs in chat.
- Avoid destructive global actions; only touch sessions/processes related to this deploy.
