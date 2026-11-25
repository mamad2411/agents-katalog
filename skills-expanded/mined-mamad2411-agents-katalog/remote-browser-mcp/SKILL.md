---
name: remote-browser-mcp
description: "Use when wiring remote Hermes to a local Mac browser MCP."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [mcp, browser, vessel, tailscale, reverse-tunnel, remote]
    category: software-development
    related_skills: [hermes-agent, computer-use]
---

# Remote browser MCP (hub Hermes → local Mac)

Connect Hermes running on a **Linux hub** (devbox) to a **browser MCP on a Mac** (Vessel, Chrome MCP, etc.) when both are on the same Tailscale tailnet.

## When to use

- User says browser MCP is on `:3100` / Vessel / local machine
- Hermes is on remote Linux; Mac holds the real browser
- SSH from hub → Mac fails (publickey) but Macs can dial **into** the hub
- Need a reliable path that does not depend on hub outbound SSH

## Architecture (this fleet)

| Role | Host | Notes |
|------|------|--------|
| Hermes agent | `devbox` (`*.<REDACTED>`) | Cannot reliably SSH to Macs |
| Browser MCP | Mac (`pro` / `coopers-macbook-pro` / `coopers-mac-studio`) | Vessel default port **3100** |
| Sync/SSH direction | Mac → devbox | Hub-and-spoke; Macs own sessions |

**Do not** default to stdio-over-SSH (`ssh mac … mcp`) from hub — that path dies on publickey unless keys are fixed. Prefer **HTTP MCP + reverse tunnel** (or Tailscale Serve).

## Preferred path: reverse tunnel + HTTP MCP

### 1. Confirm tunnel / listener on hub

On devbox:

```bash
ss -ltnp | grep 3100
# expect: 127.0.0.1:3100 LISTEN  (often no local PID → SSH -R)
```

Probe (expect 401 without token for Vessel):

```bash
curl -sS -m 3 -D- http://127.0.0.1:3100/mcp -o /tmp/mcp.body | head
# Vessel: HTTP 401 {"error":"Unauthorized — missing or invalid bearer <REDACTED>"}
# Wrong path: 404 Not found
```

If nothing listens: Mac must start the MCP **and** open the reverse forward:

```bash
# On Mac (MCP already on 127.0.0.1:3100)
ssh -N -o ExitOnForwardFailure=yes \
  -R 127.0.0.1:3100:127.0.0.1:3100 \
  cm@<REDACTED>
```

Durable variant: `autossh -M 0` + `ServerAliveInterval=30`, or a LaunchAgent.

### 2. Get the bearer <REDACTED> (Vessel)

Token lives **only on the Mac** (not in mutagen git/omp sync, not in himitsu by default):

```text
~/.config/vessel/mcp-auth.json   # { "endpoint", "token", "pid", ... }
```

Copy to hub (from Mac):

```bash
scp ~/.config/vessel/mcp-auth.json \
  cm@<REDACTED>:/var/lib/hermes/.hermes/credentials/vessel-mcp-auth.json
```

Or have the user paste the token. Do **not** invent tokens or spray guesses.

### 3. Register with Hermes

Hermes HTTP MCP + header auth:

```bash
# Interactive (prompts for bearer):
hermes mcp add vessel --url http://127.0.0.1:3100/mcp --auth header

hermes mcp test vessel
# In desktop session: /reload-mcp
```

Config shape (secret in `.env`, not plaintext in yaml when using CLI header auth):

```yaml
mcp_servers:
  vessel:
    url: "http://127.0.0.1:3100/mcp"
    headers:
      Authorization: <REDACTED>
    timeout: 180
    connect_timeout: 30
```

Env key pattern: `MCP_<SERVERNAME_UPPER>_TOKEN` (see Hermes `_env_key_for_server`).

Helper script (if present): `~/.hermes/scripts/wire-vessel-mcp.sh` — probes auth file and wires config.

### 4. Verify tools

After successful `hermes mcp test` / reload, tools appear as `mcp_vessel_*` (Vessel tools are often `vessel_*` under that prefix). Exercise a cheap read-only tool (e.g. current tab) before driving navigation.

## Alternate path: Tailscale Serve (no SSH -R)

If the MCP binds only loopback on the Mac:

```bash
# Mac
tailscale serve --bg --http=3100 http://127.0.0.1:3100
```

Then from hub:

```bash
hermes mcp add vessel --url http://<mac-magicdns>:3100/mcp --auth header
```

Use MagicDNS hostnames (`pro`, `coopers-macbook-pro`, …), never LAN IPs.

## Discovery checklist (do this order)

1. `tailscale status` — which Macs are online
2. Hub `ss`/`curl` on `127.0.0.1:3100` — tunnel already up?
3. If closed: probe Mac:3100 over Tailscale (`nc`/`curl` to MagicDNS)
4. Identify product by response body (Vessel → bearer <REDACTED> `/mcp`)
5. Fetch token from Mac path or user
6. `hermes mcp add` + `test` + `/reload-mcp`

## Pitfalls

- **Hub → Mac SSH publickey denial** — expected on this fleet until hub key is on Darwin `authorized_keys`. Do not thrash stdio-SSH; use reverse tunnel or Serve.
- **MCP bound 127.0.0.1 only** — Tailscale direct connect fails; tunnel or Serve required.
- **Wrong path** — Vessel is `/mcp` (streamable HTTP), not `/sse` or `/`.
- **Missing bearer** — 401 with Vessel’s exact JSON error; fix token, not network.
- **Token not on hub** — `mcp-auth.json` is Mac-local; scp/paste every Vessel restart if token rotates.
- **SSH -R listener has no PID in `ss`** — normal for remote-forward sockets owned by sshd.
- **PATH stripped in agent shells** — prefer absolute paths or `export PATH=/run/current-system/sw/bin:...` on NixOS hub before `curl`/`ss` pipelines.
- **Do not store live bearer <REDACTED> in skills or MEMORY.md** — credentials dir + `.env` only.

## Related

- Hermes native MCP reference: hermes-agent skill → `references/native-mcp.md`
- Desktop computer use (cua-driver) is a **different** path (stdio/SSH); see `computer-use` skill
- Session detail: `references/vessel-tailscale.md`
