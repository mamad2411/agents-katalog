---
name: appgarden
description: >
  Deploy and manage web applications on remote servers with AppGarden.
  Use when the user asks about deploying apps, configuring appgarden.toml,
  managing AppGarden servers/apps, viewing logs/status/metadata, or exposing
  local work through AppGarden tunnels.
user-invocable: false
---

# AppGarden CLI Skill

Use this skill when deploying or operating web applications with the `appgarden` CLI.

AppGarden is an agentless deploy tool: the local CLI connects over SSH, prepares the remote server, uploads or clones app source, writes Caddy/systemd/Docker files, and records state under the server's AppGarden root (default `/srv/appgarden`).

## Before running commands

- Prefer running from the AppGarden repo checkout when developing/testing AppGarden itself:

  ```bash
  cd /path/to/appgarden && uv run appgarden ...
  ```

  If AppGarden is installed in the environment, `appgarden ...` is also fine.

- Read-only/safe discovery commands are fine to run without confirmation: `appgarden --help`, `appgarden version`, `appgarden config show`, `appgarden server list`, `appgarden server ping`, `appgarden apps list`, `appgarden apps status`, `appgarden apps logs`, `appgarden tunnel list`.
- Ask before commands that create, mutate, deploy, restart, stop, delete, or expose services: `server add`, `server remove`, `server default`, `server init`, `deploy`, `apps start|stop|restart|redeploy|remove`, `apps meta set|replace|remove`, `tunnel open|close|cleanup`.
- Be especially careful with:
  - `appgarden server init --include ssh`: hardens SSH configuration and reloads sshd.
  - `appgarden server init --include firewall`: enables UFW and changes firewall policy.
  - `appgarden apps remove NAME --yes`: deletes app resources; add `--keep-data` only when preserving the app's `data/` directory is intended.
  - `appgarden deploy`: may overwrite uploaded source for an existing app and may update Caddy/systemd/Docker resources.
  - `appgarden tunnel open`: publicly exposes a local port/file/directory through the configured server until stopped.

## Configuration locations

Local config is stored at:

```text
~/.config/appgarden/config.toml
```

Server config shape:

```toml
default_server = "myserver"

[defaults]
method = "dockerfile"
container_port = 3000

[servers.myserver]
host = "203.0.113.10"              # or hcloud_name + hcloud_context
ssh_user = "root"
ssh_key = "~/.ssh/id_rsa"
domain = "apps.example.com"
app_root = "/srv/appgarden"        # optional; defaults to /srv/appgarden

[servers.myserver.init]
skip = ["upgrades"]               # optional persistent init skips
```

Remote state and resources are under `app_root`, usually:

```text
/srv/appgarden/garden.json          # app registry
/srv/appgarden/apps/<name>/         # per-app files/source/app.json/.env/data
/srv/appgarden/caddy/apps/*.caddy   # deployed app Caddy snippets
/srv/appgarden/caddy/tunnels/*.caddy
/srv/appgarden/tunnels/active.json
```

`appgarden config show` prints the local config. Use `--server <name>` / `-s <name>` or `APPGARDEN_SERVER` on commands that target a server; otherwise AppGarden uses `default_server`.

**Multiple gardens on one host:** you can run several AppGarden gardens on the same box by giving each a distinct `app_root` (e.g. `/srv/appgarden` and `/srv/appgarden-proto`). Per-garden state (`garden.json`), Caddy snippets, and the `/etc/caddy/Caddyfile` managed block are all keyed per `app_root`, so `server init` for one garden won't disturb another. Ports, however, are a **box-global** resource — every garden shares the host's TCP port space — so port allocations live in a single host-level registry at `/var/lib/appgarden/ports.json`, shared by all gardens under one lock. This is what prevents two gardens handing out the same host port; you don't configure port ranges. Caveats: systemd unit and Docker container names are box-global (`appgarden-<name>`), so **app names must be unique across gardens** on one host. If you're upgrading a host that pre-dates the shared registry, run `appgarden server init` once per existing garden — init reconciles each garden's already-deployed app ports into the shared registry (idempotent).

## Server setup

A server must be configured, reachable over SSH, and have DNS pointing at it.

```bash
appgarden server add myserver \
  --host <server-ip-or-hostname> \
  --ssh-user root \
  --ssh-key ~/.ssh/id_rsa \
  --domain apps.example.com

# Hetzner alternative: resolve IP through hcloud instead of --host
appgarden server add myserver \
  --hcloud-name <hetzner-server-name> \
  --hcloud-context <hcloud-context> \
  --domain apps.example.com

appgarden server list
appgarden server ping myserver
appgarden server default myserver
```

For subdomain deployments and tunnels, create wildcard DNS such as `*.apps.example.com` pointing at the server IP. Explicit custom hostnames also need DNS pointing at the server.

### Initializing a server

Run once per server:

```bash
appgarden server init myserver
```

Current `server init` behavior:

- Optional steps **on by default**; skip with `--skip`: `update`, `docker`, `caddy`, `upgrades`.
- Opt-in steps **off by default**; enable with `--include`: `firewall`, `ssh`, `fail2ban`, `group`.
- Essential steps always run: configure the AppGarden Caddyfile import block, create directories, install the privileged helper/sudoers entry, set ownership for the deploy user, initialize state files, and start Docker/Caddy where available.

Examples:

```bash
appgarden server init myserver --minimal              # essential steps only
appgarden server init myserver --skip upgrades        # skip unattended-upgrades
appgarden server init myserver --include group        # create/use appgarden group for non-root deploy users
appgarden server init myserver --include firewall     # configure UFW; confirm first
appgarden server init myserver --include ssh          # harden sshd; confirm first
```

For non-root SSH users, `server init` installs `/usr/local/bin/appgarden-privileged` and a sudoers rule restricted to AppGarden-scoped privileged operations.

## Preferred deployment flow: `appgarden.toml`

Create `appgarden.toml` in the project root and deploy named environments.

```toml
[app]
name = "myapp"
slug = "my-app"                  # optional; used by {app.slug}; falls back to name
server = "myserver"
method = "dockerfile"            # static | command | dockerfile | docker-compose | auto
source = "."                     # local path or git URL
container_port = 3000
subdomain = "{app.slug}"         # or path/url; supports placeholders
exclude = ["node_modules", ".git"]
gitignore = true                  # local uploads honor .gitignore by default
meta = { team = "frontend" }

[environments.production]
branch = "main"
subdomain = "{app.slug}"
env = { NODE_ENV = "production" }

[environments.staging]
branch = "staging"
subdomain = "{app.slug}-staging"
env_file = ".env.staging"
meta = { visibility = "internal" }
```

Deploy:

```bash
appgarden deploy production
appgarden deploy staging
appgarden deploy --all-envs
appgarden deploy --project /path/to/project production
```

If `appgarden.toml` is present and no environment/name is provided, `appgarden deploy` deploys all environments. If a positional environment is provided, it must exist.

### `appgarden.toml` semantics

- `[app].name` is required. Deployed app names are derived from it: `production` uses the base name, every other environment uses `<name>-<env>`. Example: `myapp` and `myapp-staging`.
- Values cascade in this order: hardcoded defaults < global `[defaults]` in `~/.config/appgarden/config.toml` < `[app]` defaults < `[environments.<name>]` < CLI flags / `APPGARDEN_*` environment variables.
- Dict fields `env` and `meta` merge by key; environment/CLI values override earlier keys.
- List fields `exclude` and `volumes` concatenate and deduplicate across layers.
- String values in project/environment config support placeholders: `{app.name}`, `{app.slug}`, `{env.name}`.
- Relative local `source` and `env_file` values resolve relative to the project directory or the directory containing the explicit `--project` file.

Useful fields in `[app]` or `[environments.<name>]`:

| Field | Meaning |
| --- | --- |
| `server` | Configured server name. |
| `method` | `static`, `command`, `dockerfile`, `docker-compose`, or `auto`. Default is `static`. |
| `source` | Local directory/path or git URL. Required for `static`, `dockerfile`, `docker-compose`, `auto`; optional for `command`. |
| `url` | Explicit public hostname/path, e.g. `example.com` or `example.com/docs`. |
| `subdomain` | Prefix combined with `domain` or the server domain, e.g. `docs` -> `docs.apps.example.com`. |
| `path` | Path under `domain` or server domain, e.g. `docs` -> `apps.example.com/docs`. |
| `domain` | Override the server's base domain for `subdomain`/`path`. |
| `port` | Host port; omitted means AppGarden auto-allocates from its port state. |
| `container_port` | Port exposed inside Dockerfile/auto containers. Default is `3000`. |
| `cmd` | Start command for `command` and `auto` methods. Required for both. |
| `setup_cmd` | Install/build command for `auto`; overrides the detected runtime default. |
| `branch` | Git branch for git sources. |
| `env` | Inline environment variables. |
| `env_file` | Local dotenv file. |
| `meta` | Arbitrary metadata stored with the app and shown in status. |
| `exclude` | Rsync exclude patterns for local uploads; also reused by `apps redeploy`. |
| `gitignore` | Whether local uploads pass rsync's `.gitignore` filter. Default `true`; CLI override is `--no-gitignore`. |
| `volumes` | Docker volume mounts (`host:container[:opts]`) for `dockerfile` and `auto`. |
| `created_at`, `updated_at`, `repo` | Optional metadata overrides. Dates accept short date, ISO string, or TOML dates; repo is otherwise auto-detected from local git origin when possible. |

URL resolution order is: explicit `url`; otherwise `subdomain` + domain; otherwise `path` + domain. For subdirectory routing (`domain/path`), multiple apps on the same domain share a generated Caddy config and AppGarden checks URL conflicts.

## Ad-hoc deployment without `appgarden.toml`

Use `--name` and flags. Most flags also have `APPGARDEN_*` environment variable equivalents (`APPGARDEN_NAME`, `APPGARDEN_SERVER`, `APPGARDEN_METHOD`, `APPGARDEN_SOURCE`, `APPGARDEN_URL`, `APPGARDEN_SUBDOMAIN`, `APPGARDEN_PATH`, `APPGARDEN_DOMAIN`, `APPGARDEN_PORT`, `APPGARDEN_CONTAINER_PORT`, `APPGARDEN_CMD`, `APPGARDEN_SETUP_CMD`, `APPGARDEN_BRANCH`, `APPGARDEN_ENVVAR_FILE`, `APPGARDEN_PROJECT`, `APPGARDEN_ALL_ENVS`).

```bash
# Static site / SPA
appgarden deploy --name mysite --method static --source ./dist --subdomain mysite

# Dockerfile app
appgarden deploy --name myapp --method dockerfile --source . --container-port 3000 --subdomain myapp

# Auto-generated Dockerfile; runtime is detected from package.json, requirements.txt,
# pyproject.toml, Gemfile, go.mod, or Cargo.toml. --cmd is required.
appgarden deploy --name myapp --method auto --source . --cmd "npm start" --subdomain myapp

# Bare process managed by systemd. --source is optional; --cmd is required.
appgarden deploy --name myapi --method command --source ./api --cmd "python app.py" --subdomain myapi

# Docker Compose stack; your compose file is used directly.
appgarden deploy --name mystack --method docker-compose --source ./project --subdomain mystack

# Explicit path routing instead of subdomain routing
appgarden deploy --name docs --method static --source ./docs --url apps.example.com/docs

# Env, metadata, excludes, and volumes
appgarden deploy --name myapp --method dockerfile --source . --subdomain myapp \
  --envvar NODE_ENV=production \
  --envvar-file .env.production \
  --meta team=backend --meta visibility=internal \
  --exclude node_modules --exclude .git \
  --volume ./data:/app/data \
  --no-gitignore
```

Deployment method notes:

| Method | Use for | Required inputs | Runtime behavior |
| --- | --- | --- | --- |
| `static` | HTML/CSS/JS/SPAs | `source` | Upload/clone source and serve directly with Caddy. |
| `command` | A local process without Docker | `cmd` (`source` optional) | Creates a systemd service with `PORT` set to allocated/explicit port. |
| `dockerfile` | Projects with a Dockerfile | `source` | Builds image remotely, writes AppGarden compose file, runs through systemd. |
| `docker-compose` | Existing compose projects | `source` | Runs your `docker compose up/down` through systemd; `volumes` config is not injected. |
| `auto` | Simple Node/Python/Ruby/Go/Rust projects | `source`, `cmd` | Detects runtime, writes Dockerfile, builds image, writes compose file. |

For local uploads, AppGarden uses rsync with `--delete`, honors `.gitignore` by default, and applies any `--exclude`/`exclude` patterns. For git sources, it clones the repo on the remote and optionally checks out the requested branch.

Environment variable precedence for deployed app `.env` files is: `appgarden.toml` `env` < `env_file` content < CLI `--envvar` values.

## Managing deployed apps

```bash
appgarden apps list [-s server] [--short]
appgarden apps status <name> [-s server]
appgarden apps logs <name> [-s server] [-n 100]
appgarden apps restart <name> [-s server]
appgarden apps redeploy <name> [-s server]
appgarden apps stop <name> [-s server]
appgarden apps start <name> [-s server]
appgarden apps remove <name> [-s server] [--keep-data] [--yes]
```

Operational guidance:

- Use `apps list` first when you do not know the exact app name.
- Use `apps status` to inspect URL, routing, method, port, repo/source, timestamps, and metadata.
- Use `apps logs NAME -n 200` before restarting when debugging.
- `apps redeploy` updates source: git apps run `git pull` (with the stored branch if present); local-source apps re-upload with stored `exclude`/`gitignore`; Dockerfile/auto apps rebuild images and preserve stored volumes; static apps reload Caddy.
- If changing an app name in `appgarden.toml`, remove the old app first to avoid URL/Caddy conflicts:

  ```bash
  appgarden apps remove old-name --yes
  appgarden deploy production
  ```

## Metadata

Metadata is arbitrary JSON-compatible key/value data stored with the app.

```bash
appgarden apps meta get myapp [-s server]
appgarden apps meta set myapp --meta team=backend --meta tier=premium [-s server]
appgarden apps meta replace myapp --json '{"team":"frontend"}' [-s server]
appgarden apps meta remove myapp tier visibility [-s server]
```

In `appgarden.toml`, `meta` dictionaries merge like `env` dictionaries:

```toml
[app]
name = "myapp"
meta = { team = "backend", visibility = "internal" }

[environments.production]
meta = { visibility = "public" }
# result: { team = "backend", visibility = "public" }
```

## Localhost tunnels

Use tunnels to expose a local dev server, file, directory, or command through the remote server with HTTPS. A tunnel blocks until Ctrl+C unless `--close-on-cmd-exit` is used with `--cmd`/`--serve`.

```bash
# Expose an existing local server. URL omitted => random three-word subdomain.
appgarden tunnel open 3000

# Use server domain subdomain shorthand or an explicit URL
appgarden tunnel open 3000 --subdomain preview
appgarden tunnel open 3000 --url preview.apps.example.com

# Run a local command while the tunnel is open
appgarden tunnel open 3000 --cmd "npm run dev"
appgarden tunnel open 3000 --cmd "npm run dev" --close-on-cmd-exit

# Serve a local file or directory. LOCAL_PORT is optional with --serve.
appgarden tunnel open --serve ./dist --subdomain docs-preview
appgarden tunnel open --serve ./dist --include "*.html" --exclude "node_modules"

# Reclaim a URL a dead run still holds, then open (idempotent re-open)
appgarden tunnel open 3000 --url preview.apps.example.com --replace

appgarden tunnel list [-s server]
appgarden tunnel list --json [-s server]      # machine-readable, for scripting
appgarden tunnel close <tunnel-id> [-s server]
appgarden tunnel cleanup [-s server]
```

`--cmd` and `--serve` are mutually exclusive. `--include`/`--exclude` only apply when `--serve` points to a directory. Tunnels allocate a remote port, write a Caddy snippet under `caddy/tunnels`, and register state in `tunnels/active.json`; cleanup removes those resources.

**`--replace` is what makes an unattended re-open work.** A tunnel's Caddy snippet is keyed by its own tunnel id, so a run killed without cleanup (a reboot, a `SIGKILL`) leaves a snippet still claiming the hostname; the next `tunnel open` for the same `--url` then fails Caddy's reload with *ambiguous site definition* and rolls itself back. `--replace` closes any tunnel already registered against that URL first. It requires an explicit `--url`/`--subdomain` — with a generated subdomain there is nothing it could match, so it is refused rather than silently doing nothing. Note `tunnel cleanup` is not a substitute: it only reaps tunnels whose remote port has nothing listening.

A tunnel closes cleanly on **SIGTERM** as well as Ctrl+C, so a supervised `stop` (supervisord, systemd, `docker stop`) releases the registration, the Caddy snippet and the remote port instead of stranding them.

`tunnel list --json` emits a JSON array (empty when there are no tunnels, never the human "No active tunnels." line) — parse that rather than the table.

## Troubleshooting workflow

1. Confirm config and server targeting:

   ```bash
   appgarden config show
   appgarden server list
   appgarden server ping <server>
   ```

2. Inspect app state and logs:

   ```bash
   appgarden apps list --short
   appgarden apps status <app>
   appgarden apps logs <app> -n 200
   ```

3. Redeploy or restart only after reading the error:

   ```bash
   appgarden apps redeploy <app>
   appgarden apps restart <app>
   ```

4. Common local-source upload issues:
   - `rsync` must be installed locally.
   - Encrypted SSH keys need an agent: `eval $(ssh-agent) && ssh-add ~/.ssh/id_rsa`.
   - Permission errors on non-root deploys usually mean rerun `appgarden server init --include group` or fix remote ownership.

## Reference files in this repository

The generated `src/appgarden/*.py` files say "AUTOGENERATED"; implementation edits should usually be made in the corresponding `pts/appgarden/*.pct.py` source files. For skill/use questions, read these files as needed:

- `README.md` — user-facing guide and CLI reference.
- `src/appgarden/cli.py` / `pts/appgarden/10_cli.pct.py` — command definitions and options.
- `src/appgarden/config.py` / `pts/appgarden/00_config.pct.py` — local config model and default config path.
- `src/appgarden/environments.py` / `pts/appgarden/08_environments.pct.py` — `appgarden.toml` parsing, merge semantics, placeholders.
- `src/appgarden/server.py` / `pts/appgarden/04_server.pct.py` — server init steps.
- `src/appgarden/deploy.py` / `pts/appgarden/05_deploy.pct.py` — deployment behavior and remote state.
- `src/appgarden/apps.py` / `pts/appgarden/06_apps.pct.py` — app lifecycle and redeploy behavior.
- `src/appgarden/routing.py` / `pts/appgarden/03_routing.pct.py` — Caddy routing and URL conflict behavior.
- `src/appgarden/tunnel.py` / `pts/appgarden/09_tunnel.pct.py` — tunnel behavior.
