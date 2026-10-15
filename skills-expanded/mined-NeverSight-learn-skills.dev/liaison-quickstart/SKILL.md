---
name: liaison-quickstart
version: 0.1.0
description: "Liaison Cloud one-shot bootstrap: create a connector + register an application + expose it via a public entry, in a single command. Use this skill when a user asks 'set up a new tunnel for my SSH server', 'I want to expose my local web app to the internet', 'create a new connector for my home box', or any other green-field 'go from nothing to a working public endpoint' request. Always read ../liaison-shared/SKILL.md first."
metadata:
  requires:
    bins: ["liaison"]
  cliHelp: "liaison quickstart --help"
---

# liaison-quickstart

**CRITICAL — read [`../liaison-shared/SKILL.md`](../liaison-shared/SKILL.md) first.**

## When to use this skill

Use `liaison quickstart` whenever the user is bootstrapping from zero. It does in one call what would otherwise take 3 separate API calls (connector create → application create → entry create), it polls for the connector to come online, and it returns a single structured JSON result so you can immediately tell the user "your service is now reachable at X".

**Don't** use quickstart when the user already has a connector and just wants to add an application or entry. For those, use the `liaison-application` or `liaison-entry` skills directly — quickstart will create a NEW connector each time it's called, which is almost never what the user wants in incremental flows.

## The five layers of `quickstart`

The command has five stages, each gated on a flag. Skip whichever you don't need.

| Stage | Required flag | Purpose |
|-------|--------------|---------|
| 1. Create connector | always runs | Create an edge record on the server, return ak/sk + install command |
| 2. Run install script locally | `--install` | Shell out to `bash -c` and execute `install.sh` on the **local** machine. This installs the binary, writes the config, **and registers a launchd (macOS) / systemd (Linux) service** so the connector survives reboots. Only safe when the CLI is on the same host that should be a connector. **macOS**: user-domain install, no sudo needed — safe to run non-interactively from an agent. **Linux**: writes to `/usr/local/bin` and `/etc/systemd`, still needs sudo — if no tty is available, the sudo prompt fails silently and the install returns an error. |
| 3. Wait for online | `--wait-online <duration>` | Poll the edge until `online == 1` or timeout. Required if the next stages need a working tunnel. |
| 4. Register application | `--app-name` + `--app-ip` + `--app-port` (+ optional `--app-protocol`) | Create the backend application metadata |
| 5. Expose via entry | `--expose` (+ optional `--entry-name`/`--entry-port`/`--entry-domain`) | Create a public entry pointing at the application |

## Recipes

### Recipe A — full closed-loop on the same machine (RECOMMENDED)

The user is on the machine that will run the connector. One command does everything — create connector, install it, wait for online, register app, expose publicly:

```bash
liaison quickstart --name mybox \
  --app-name ssh --app-ip 127.0.0.1 --app-port 22 --app-protocol ssh \
  --expose --install --wait-online 2m
```

**`--install` downloads and installs the connector agent on the current machine (needs sudo).** Combined with `--wait-online`, this is a fully closed loop — the command doesn't return until the connector is online and the entry is created.

Result:
```json
{
  "connector": { "id": 100042, "name": "mybox", "access_key": "...", "secret_key": "..." },
  "install_command": "curl ...",
  "installed": true,
  "online_achieved": true,
  "application": { "id": 1, "name": "ssh", "protocol": "ssh", "ip": "127.0.0.1", "port": 22 },
  "entry": { "id": 10, "name": "ssh", "port": 34567 }
}
```

Tell the user: `ssh -p 34567 user@liaison.cloud` — it works immediately.

### Recipe B — CLI on a different machine than the connector

The user's CLI is on their laptop, but the connector should run on a remote server. Omit `--install` — the user must run the install command on the target host manually.

```bash
liaison quickstart --name mybox \
  --app-name ssh --app-ip 127.0.0.1 --app-port 22 --app-protocol ssh \
  --expose --wait-online 2m
```

The flow:
1. Create connector → return ak/sk + install command
2. **You echo `install_command` to the user** — they run it on the target host
3. Poll for up to 2 minutes until the connector is online
4. Once online, create the application + entry
5. Return the entry's allocated port/domain

### Recipe C — just create the connector

User intent: "Create a new connector called mybox." They'll install and configure later.

```bash
liaison quickstart --name mybox
```

**Your job afterwards**: echo `install_command` to the user with the instruction "run this on the machine you want to make a connector".

### Recipe D — connector + app, no public exposure yet

The user wants to register a service but isn't ready to publish it.

```bash
liaison quickstart --name mybox --install --wait-online 2m \
  --app-name ssh --app-ip 127.0.0.1 --app-port 22 --app-protocol ssh
```

The connector is installed and the application is registered, but no public entry is created. The user can add an entry later with `liaison proxy create`.

### Recipe E — HTTP web app with a custom domain

```bash
liaison quickstart --name mybox --install --wait-online 2m \
  --app-name web --app-ip 127.0.0.1 --app-port 8080 --app-protocol http \
  --expose --entry-domain myapp.example.com
```

The user's DNS still has to point `myapp.example.com` at Liaison's edge nodes — quickstart does not configure DNS.

## Result shape (full)

```json
{
  "connector": {
    "id": 100042,
    "name": "mybox",
    "access_key": "MTc3NjI2OTc4NjM1MTAx",
    "secret_key": "20S6Yr8EralcxwWGOQyjgAnaqEfmlx0odRJN4x5UHIw",
    "description": "..."
  },
  "install_command": "curl ... | bash -s -- ...",
  "installed": true,                 // true if --install was passed and bash exit was 0
  "online_waited": true,             // true if --wait-online > 0
  "online_achieved": true,           // true if the connector reported online before the deadline
  "application": {                   // only present if --app-name was passed
    "id": 1,
    "name": "ssh",
    "protocol": "ssh",
    "ip": "127.0.0.1",
    "port": 22
  },
  "entry": {                         // only present if --expose was passed
    "id": 10,
    "name": "ssh",
    "protocol": "ssh",
    "port": 34567,
    "domain": ""
  },
  "next_steps": [
    "Connector did not come online within 2m — check the install succeeded on the host."
  ]
}
```

`next_steps` is a hand-curated list of strings — surface them to the user verbatim. They're often the difference between a working bootstrap and a confused user.

## Hard rules for agents

- **Never pass `--install` to a server-side machine that is not the user's intended connector host.** Doing so installs a long-running daemon under a service identity the user didn't intend to create.
- **Always check `online_achieved` before declaring success.** If false, the application/entry exist but no traffic will flow until the user runs the install command.
- **Do not call quickstart twice for the same logical setup.** Each call creates a NEW connector (and new ak/sk). If a previous call created a connector but the user closed the tab, find it with `liaison edge list` instead.
- **Always echo `install_command` to the user** — they need it to actually bring the connector online.
- **Always echo allocated ports/domains** from `entry.port` / `entry.domain` — these are how the user actually reaches their service.
- **Never bypass `install.sh` by starting `liaison-edge` directly.** If `online_achieved == false` and you're tempted to "just start the agent manually", DO NOT. A raw `liaison-edge &` works for one session but registers no launchd/systemd unit, so the connector silently goes offline after reboot or logout. Re-run `install.sh` with the ak/sk (or `liaison quickstart --install` for a fresh one) instead. See the `liaison-connector` skill's "Recovering an offline connector" section for the full diagnostic flow.
- **ak/sk are a one-shot secret.** The server only returns `access_key` / `secret_key` from `edge create` (including inside `quickstart`) — they cannot be retrieved later. If the user loses them and the connector host's service is gone, the only recovery is `edge delete` (which cascades to apps + entries) followed by a fresh `quickstart`.
- **Handling sudo on Linux `--install`.** `install.sh` on Linux writes to `/usr/local/bin` and `/etc/systemd/system`, which need root. When the CLI runs under an agent (no tty), `sudo` cannot prompt and the install errors out with `a terminal is required`. Probe first — `sudo -n true 2>/dev/null`. If that succeeds you have passwordless sudo and `--install` will work; otherwise skip `--install`, echo `install_command` to the user, and tell them to run it themselves (in Claude Code, prefix with `!` so the command runs in the user's shell and sudo can prompt). **macOS is not affected** — the install is fully user-domain and needs no sudo.

## Quickstart vs step-by-step

`quickstart` bundles 3 API calls into 1. Use it for greenfield setups. For incremental changes, use the individual commands:

| Goal | Quickstart | Step-by-step |
|------|-----------|--------------|
| New connector + app + entry from scratch | `liaison quickstart --name mybox --app-name web --app-ip 127.0.0.1 --app-port 8080 --app-protocol http --expose` | `edge create` → `application create` → `proxy create` (3 calls) |
| New connector only | `liaison quickstart --name mybox` | `liaison edge create --name mybox` |
| Add app to EXISTING connector | **Don't use quickstart** | `liaison application create --name ssh --protocol ssh --ip 127.0.0.1 --port 22 --edge-id <ID>` |
| Expose EXISTING app | **Don't use quickstart** | `liaison proxy create --name ssh --protocol ssh --application-id <ID>` |

### Step-by-step example (full flow)

```bash
# 1. Create connector — note the edge ID from output
liaison edge create --name my-server
# => { "access_key": "...", "secret_key": "...", "command": "curl ..." }

# 2. Install connector on the target host (copy the command from step 1)
# curl -k -sSL https://liaison.cloud/install.sh | bash -s -- --access-key=... --secret-key=...

# 3. Register backend application (use edge ID from step 1)
liaison application create \
  --name my-ssh --protocol ssh \
  --ip 127.0.0.1 --port 22 \
  --edge-id 100017
# => { "id": 100046, ... }

# 4. Expose via public entry (use application ID from step 3)
liaison proxy create --name my-ssh --protocol ssh --application-id 100046
# => { "port": 41752, ... }
# User can now: ssh -p 41752 user@liaison.cloud
```

## When NOT to use quickstart

- The user already has a connector and wants to add a second application → use `liaison-application`
- The user already has an application and wants a second public exposure → use `liaison-entry`
- The user wants to LIST or INSPECT existing resources → use `liaison-connector`/`-application`/`-entry`
- The user wants to delete or disable something → use `liaison-connector` or `liaison-entry`
