---
name: rustunnel
description: "Expose local services via secure tunnels using rustunnel. Create public HTTPS/TCP/UDP URLs, peer-to-peer tunnels, and load-balanced pools for testing, webhooks, demos, and deployment — from any AI agent or harness."
version: 2.0.0
author: rustunnel
tags: [tunnel, ngrok, expose, devops, deployment, testing, webhooks, p2p, load-balancing]
---

# Rustunnel — Secure Tunnel Management

Expose local services (HTTP / TCP / UDP / P2P) through public URLs using
rustunnel. Perfect for testing webhooks, sharing local development, database
access, and AI agent workflows. Works through the **rustunnel MCP server**, so
any MCP-capable harness (Claude Code, Claude Desktop, Codex, Cursor, Windsurf,
Cline, or a custom agent) can drive it.

## When to Use

- **Webhook testing** — receive webhooks from Stripe/GitHub/etc. on a local server
- **Demo sharing** — share local development with stakeholders
- **CI/CD & previews** — expose preview environments
- **Database / TCP access** — expose PostgreSQL, Redis, SSH, raw TCP
- **UDP services** — game servers, DNS, custom UDP protocols
- **Peer-to-peer** — direct, NAT-punched connections between two peers
- **Load balancing** — spread traffic across multiple local backends with health checks

---

## Authentication — you need an API token (one-time)

rustunnel requires an API token. **Get one once, then reuse it:**

1. **Hosted (rustunnel.com):** sign up free at <https://rustunnel.com> →
   **Dashboard → API Keys** → create a key.
2. **Self-hosted:** create one with `rustunnel token create --name agent`
   (needs the server admin token), or from your dashboard.

**Where the token lives (in priority order):**

1. The `RUSTUNNEL_TOKEN` environment variable, set once in your MCP client
   config. **This is the recommended setup** — when it's set, you do **not**
   need to pass `token` on tool calls and you should **not** ask the user for it
   again.
2. A `token` argument passed explicitly to a tool call.
3. `~/.rustunnel/config.yml` (`auth_token:`) for the CLI.

**If no token is configured**, ask the user once: "What's your rustunnel API
token? Get one free at https://rustunnel.com → Dashboard → API Keys." Then
prefer storing it as `RUSTUNNEL_TOKEN` in the MCP config so it persists.

---

## IMPORTANT: Prefer MCP Tools over the raw CLI

Use the MCP tools for tunnel management — they handle the process lifecycle
automatically (no orphaned processes, automatic cleanup, tunnel IDs for tracking).
Only fall back to the CLI (`get_connection_info`) when the agent **cannot** spawn
subprocesses (e.g. a cloud sandbox).

| Method | Lifecycle | Use it when |
|--------|-----------|-------------|
| **MCP tools** (`create_tunnel`, `close_tunnel`) | Automatic cleanup | Default |
| **CLI** (via `get_connection_info`) | Manual (user runs it) | Cloud sandbox / no subprocess |

---

## MCP Tools

### `create_tunnel`

Open a tunnel and get a public URL. The token may be omitted when
`RUSTUNNEL_TOKEN` is set.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `token` | string | no¹ | API token (¹required unless `RUSTUNNEL_TOKEN` is set) |
| `local_port` | integer | yes | Local port to expose |
| `protocol` | `"http"` \| `"tcp"` \| `"udp"` \| `"p2p"` | yes | Tunnel type |
| `subdomain` | string | no | Custom subdomain (HTTP only) |
| `region` | string | no | `"eu"`, `"us"`, `"ap"`. Omit to auto-select by latency |
| `local_host` | string | no | Local hostname to forward to (default `localhost`) |
| `secret` | string | p2p only | Shared secret; publisher and subscriber must match |
| `peer_name` | string | p2p publish | Publish the local service under this name |
| `peer_target` | string | p2p connect | Connect to a published P2P tunnel by this name |
| `group` | string | LB | Load-balancing pool name (http/tcp only) |
| `group_key` | string | LB | Shared secret for the pool; members must agree |
| `health_check` | object | no | Health probe — see below |

`health_check` object: `{ type: "tcp"|"http", path, interval_secs, timeout_secs, max_failed, expect_2xx, alert_webhook }`.

**Returns:**
```json
{ "public_url": "https://abc123.eu.edge.rustunnel.com", "tunnel_id": "a1b2c3d4-...", "protocol": "http" }
```

Tunnel stays open until `close_tunnel` is called or the MCP server exits.

### `close_tunnel`

Close a tunnel by ID. The public URL stops working immediately.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `token` | string | no¹ | API token |
| `tunnel_id` | string | yes | UUID from `create_tunnel` / `list_tunnels` |

### `list_tunnels`

List active tunnels (public URL, protocol, traffic count). `token` optional¹.

### `get_tunnel_history`

Past tunnels (duration, owning token). Params: `token` (optional¹),
`protocol` (filter, optional), `limit` (default 25).

### `list_regions`

Available server regions. No auth required.

### `get_connection_info`

Returns the CLI command (and, for load-balanced tunnels, a config file) to run
the client manually — without spawning anything. Use in cloud sandboxes. Accepts
the same arguments as `create_tunnel`.

---

## Common Workflows

### Expose a local web app
```
create_tunnel(local_port=3000, protocol="http")
→ return public_url; close_tunnel(tunnel_id) when done
```

### Custom subdomain
```
create_tunnel(local_port=5173, protocol="http", subdomain="myapp-preview")
```

### Database / TCP
```
create_tunnel(local_port=5432, protocol="tcp")  → host:port to connect
```

### UDP service
```
create_tunnel(local_port=27015, protocol="udp")
```

### Peer-to-peer — publish, then connect
```
# Publisher (machine A)
create_tunnel(local_port=3000, protocol="p2p", secret="shared", peer_name="my-svc")
# Subscriber (machine B)
create_tunnel(local_port=8000, protocol="p2p", secret="shared", peer_target="my-svc")
```

### Load-balanced pool with health checks
Run one `create_tunnel` per backend; members sharing `(group, group_key)` form
one pool (requires the edge to have `[load_balancing] enabled = true`):
```
create_tunnel(local_port=3000, protocol="http", subdomain="pool",
              group="web", group_key="shared-secret",
              health_check={ "type": "http", "path": "/health", "interval_secs": 10 })
create_tunnel(local_port=3001, protocol="http", subdomain="pool",
              group="web", group_key="shared-secret",
              health_check={ "type": "http", "path": "/health" })
```

### Cloud sandbox (CLI fallback)
```
get_connection_info(local_port=3000, protocol="http")
→ output the command for the user to run locally
→ list_tunnels() to confirm and fetch public_url
```

---

## Prerequisites

The `rustunnel` CLI must be installed and on `PATH` (the MCP server spawns it):

```bash
# Homebrew (macOS/Linux)
brew tap joaoh82/rustunnel && brew install rustunnel

# Or build from source
git clone https://github.com/joaoh82/rustunnel.git && cd rustunnel
make release   # builds rustunnel, rustunnel-mcp
```

## Adding rustunnel to your harness

See **[docs/agent-integration.md](https://github.com/joaoh82/rustunnel/blob/main/docs/agent-integration.md)**
for copy-paste MCP config for Claude Code, Claude Desktop, Codex, Cursor,
Windsurf, Cline, and generic/custom agents — plus a one-command installer:

```bash
curl -fsSL https://raw.githubusercontent.com/joaoh82/rustunnel/main/integrations/install.sh | bash
```

A minimal MCP config looks like:
```json
{
  "mcpServers": {
    "rustunnel": {
      "command": "rustunnel-mcp",
      "args": ["--server", "eu.edge.rustunnel.com:4040", "--api", "https://eu.edge.rustunnel.com:8443"],
      "env": { "RUSTUNNEL_TOKEN": "<your-token>" }
    }
  }
}
```

## Security Notes

- Tokens travel over HTTPS (use `--insecure` only in local dev with self-signed certs).
- MCP tools clean up subprocesses automatically; tunnels close when the MCP server exits.
- Protect the config file: `chmod 600 ~/.rustunnel/config.yml`.

## Resources

- [GitHub](https://github.com/joaoh82/rustunnel)
- [Agent Integration Guide](https://github.com/joaoh82/rustunnel/blob/main/docs/agent-integration.md)
- [MCP Server Docs](https://github.com/joaoh82/rustunnel/blob/main/docs/mcp-server.md)
- [Load Balancing](https://github.com/joaoh82/rustunnel/blob/main/docs/load-balancing.md)
- [P2P Tunnels](https://github.com/joaoh82/rustunnel/blob/main/docs/p2p-tunnels.md)
