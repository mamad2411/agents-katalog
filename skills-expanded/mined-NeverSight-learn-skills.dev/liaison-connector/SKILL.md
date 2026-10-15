---
name: liaison-connector
version: 0.1.0
description: "Liaison Cloud connectors (a.k.a. edges): create, list, inspect, rename, enable/disable (kicks the live tunnel), and delete. A connector is the agent process installed on a user's host that tunnels traffic to the Liaison cloud. Use this skill for intents like 'create a new connector', 'list my connectors', 'take connector X offline', 'disable connector', 'what's connector 100017's status'. Always read ../liaison-shared/SKILL.md first."
metadata:
  requires:
    bins: ["liaison"]
  cliHelp: "liaison edge --help"
---

# liaison-connector

**CRITICAL — read [`../liaison-shared/SKILL.md`](../liaison-shared/SKILL.md) first** for auth, output format, and safety rules.

## Concept

A **connector** (internally also called "edge") is:
- A binary running on a user's machine
- Authenticated by an AccessKey + SecretKey pair issued at creation time
- Tunnelling traffic between that machine and the Liaison cloud
- The parent of one or more **applications** (backend services)
- Either `online` (connected) or `offline`, AND either `running` (status=1, allowed to connect) or `stopped` (status=2, rejected + kicked)

**Two independent state axes — don't confuse them:**

| Axis | Field | Values | Managed by |
|------|-------|--------|-----------|
| Connectivity | `online` | 1 = online, 2 = offline | Server — flips automatically when the tunnel connects/disconnects |
| Authorization | `status` | 1 = running, 2 = stopped | User — `stopped` immediately kicks the live tunnel and blocks reconnection |

When a user says "disable connector X" or "take connector X offline" they almost always mean **set status to stopped**, not wait for the physical tunnel to drop. The CLI models this as `liaison edge update <id> --status stopped`.

## Commands

All commands under `liaison edge`. Aliases: `connector`, `edges`, `connectors` (they all resolve to the same subcommand).

### List

```bash
liaison edge list                           # all connectors, JSON
liaison edge list --online 1                # only currently connected
liaison edge list --online 2                # only disconnected
liaison edge list --name prod               # substring filter on name
liaison edge list --page 2 --page-size 20   # pagination
liaison edge list -o table                  # aligned text for humans
```

**Response shape** (JSON):
```json
{
  "total": 3,
  "edges": [
    {
      "id": 100017,
      "name": "prod-server-01",
      "description": "hosting /etc/...",
      "status": 1,
      "online": 1,
      "application_count": 5,
      "created_at": "2026-04-10 12:34:56",
      "updated_at": "2026-04-14 08:02:11"
    },
    ...
  ]
}
```

### Get

```bash
liaison edge get 100017
```

Returns a single connector object with the same fields as a list entry.

### Create

```bash
liaison edge create --name my-lab-box --description "home lab mini PC"
```

**Response shape** — this is the ONLY time AccessKey/SecretKey are exposed; you cannot retrieve them again later:
```json
{
  "access_key": "MTc3...",
  "secret_key": "20S...",
  "command": "curl -k -sSL https://liaison.cloud/install.sh | bash -s -- --access-key=... --secret-key=... --server-http-addr=liaison.cloud --server-edge-addr=liaison.cloud:30012"
}
```

The `command` field is a one-liner the user runs on the **target host** (not on the machine running this CLI) to download and start the connector agent. Copy the string to the user — do NOT run it yourself unless you are certain the CLI is on the same machine that will host the connector.

### Update

Only pass flags you actually want to change — omitted flags are left alone.

```bash
# Rename
liaison edge update 100017 --name new-name

# Update description
liaison edge update 100017 --description "moved to rack 3"

# Take offline + kick the live tunnel
liaison edge update 100017 --status stopped

# Re-enable
liaison edge update 100017 --status running
```

`--status stopped` has three server-side side effects, in order:
1. `edges.status` flips to 2
2. The server calls frontier `KickEdge(id)` which closes the live tunnel
3. The connector's reconnect attempts are rejected at the auth layer (returns `edge is disabled`)

`--status running` reverses the auth-layer block — the connector will reconnect on its next retry tick (up to ~30 seconds).

### Delete

**Requires `--yes` for non-interactive safety.**

```bash
liaison edge delete 100017 --yes
```

Cascades: deletes the connector, its applications, its entries, and its pending tasks. There is no undo. Always confirm the target id with the user before running.

## Intent → command mapping (for agents)

| User says | Command |
|-----------|---------|
| "Create a connector for my home server" | `liaison edge create --name <name>` |
| "Show me my connectors" | `liaison edge list -o table` |
| "Is connector 100017 online?" | `liaison edge get 100017` then read `.online` (1=yes, 2=no) |
| "Disable / kick / take offline connector X" | `liaison edge update <id> --status stopped` |
| "Re-enable / start / bring back connector X" | `liaison edge update <id> --status running` |
| "Delete connector X" | confirm → `liaison edge delete <id> --yes` |
| "Rename connector X to Y" | `liaison edge update <id> --name Y` |

## The connector agent lifecycle (READ THIS before touching a host)

The connector is a long-running daemon (`liaison-edge`) that **must** run under a supervisor — `launchd` on macOS, `systemd` on Linux — so it auto-starts on boot and restarts on crash.

The official `install.sh` (at `https://liaison.cloud/install.sh`, invoked by `install_command` from `edge create` or by `liaison quickstart --install`) does three things, and all three are required for a healthy connector:

1. Downloads and installs the `liaison-edge` binary
   - **macOS**: `~/Library/Application Support/liaison/bin/liaison-edge` (user-owned, **no sudo**)
   - **Linux**: `/usr/local/bin/liaison-edge` (system, needs sudo)
2. Writes a config containing the ak/sk and server endpoints
   - **macOS**: `~/Library/Application Support/liaison/liaison-edge.yaml` (no sudo)
   - **Linux**: `/etc/liaison/liaison-edge.yaml` (sudo)
3. **Registers a supervised service**
   - **macOS**: `~/Library/LaunchAgents/com.liaison.edge.plist` (user launchd, no sudo)
   - **Linux**: `/etc/systemd/system/liaison-edge.service` (system systemd, sudo)

On **macOS** the install is fully user-domain — no sudo required — so `liaison quickstart --install` can run non-interactively from an agent. On **Linux** the install still needs root because systemd/system-wide paths are involved; in a non-interactive context (no tty for sudo to prompt), prefer emitting `install_command` for the user to run themselves.

> **Legacy macOS installs**: older versions of `install.sh` placed the binary at `/usr/local/bin/liaison-edge`. Re-running the new installer leaves the stale file in place and prints a warning; the current `uninstall.sh` cleans both locations (the legacy one still requires sudo).

### NEVER start `liaison-edge` manually

Do NOT do any of the following, even if the connector looks offline and "just running the binary" seems like a quick fix:

```bash
# ❌ All of these are broken in different ways
~/Library/Application\ Support/liaison/bin/liaison-edge -c ~/Library/Application\ Support/liaison/liaison-edge.yaml &
nohup liaison-edge -c /etc/liaison/liaison-edge.yaml >/tmp/edge.log 2>&1 &
sudo liaison-edge &
```

Why it bites later:
- **Dies on logout / reboot.** No supervisor → connector goes offline on the next restart and the user won't know why.
- **Fights the supervisor.** If the launchd/systemd unit is also present, two instances race for the same tunnel and the cloud bounces them.
- **No log rotation, no crash loop detection.** You'll miss failures.

Every offline-connector recovery path ends with `install.sh` or `systemctl restart` / `launchctl kickstart` — never a raw binary exec.

## Recovering an offline connector

When `liaison edge get <id>` returns `online: 2` (offline):

**Step 1 — confirm which side is broken.**

On the connector host, check the supervisor:

```bash
# macOS
launchctl print gui/$(id -u)/com.liaison.edge 2>&1 | head -20
# look for:  state = running   PID = <n>   LastExitStatus = 0

# Linux
systemctl status liaison-edge
```

**Step 2 — decide based on what you see.**

| What you observe | Meaning | Fix |
|---|---|---|
| Service is running + heartbeats in log (`liaison-edge.log`) but cloud says offline | Transient reconnect | Wait ~30s, or kick: `liaison edge update <id> --status stopped` then `--status running` |
| Service is loaded but exited / crashlooping | Daemon itself is sick | Read logs: macOS `~/Library/Logs/liaison/liaison-edge.log`, Linux `journalctl -u liaison-edge -n 100`. Then `launchctl kickstart -k gui/$(id -u)/com.liaison.edge` or `sudo systemctl restart liaison-edge` |
| Service does **not exist** at all (no plist / no unit file) | Agent was never installed on this host, or was uninstalled | **Re-run the installer** (see Step 3) — do NOT start the binary by hand |
| Service exists but config file missing / corrupted | Partial uninstall | Re-run the installer with the original ak/sk |

**Step 3 — reinstalling on a host where the service is gone.**

The `access_key` / `secret_key` are **only returned at `edge create` time** — the API will not re-emit them. So:

- **If the user still has the original `install_command`** (stashed in 1Password, shell history, etc.), have them re-run it on the target host. That's the cleanest recovery.
- **If the install command is lost**, the only path is to scrap and recreate:

  ```bash
  liaison edge delete <id> --yes       # cascades to apps + entries
  liaison quickstart --name <name> ... --install --wait-online 2m
  # ... then liaison application create + liaison proxy create for each service
  ```

  Warn the user first: cascade-delete wipes every application and entry that pointed at this connector. They'll need to recreate those too.

## What NOT to do

- **Do not invent ids.** Always list or accept an id from the user. IDs are big integers (~100000+) — guessing is not safe.
- **Do not execute the `install_command`** on your own machine. It installs a connector agent bound to a specific network identity; running it locally could register your CLI host as a connector you didn't intend.
- **Do not bulk-delete** without explicit per-id confirmation. Ask "delete connectors A, B, C?" and wait for an explicit yes.
- **Do not chain create + install + app + entry manually** — use the `liaison-quickstart` skill instead, which does all of it in one call and polls for online state.
- **Do not `liaison-edge &` to "fix" an offline connector.** See *The connector agent lifecycle* above. If the supervised service is broken, re-run the installer; if the binary is fine but needs a kick, use `launchctl kickstart` / `systemctl restart`.
