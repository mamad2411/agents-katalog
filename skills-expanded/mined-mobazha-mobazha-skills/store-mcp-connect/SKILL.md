---
name: store-mcp-connect
description: Connect an AI agent to a Mobazha store via MCP (Model Context Protocol). Use when the user wants their agent to directly manage store products, orders, and settings.
requires_credentials: true
credential_types:
  - API token (Bearer token generated from the store's admin panel)
  - SSH credentials (optional, only for tunneled connections to remote VPS stores)
---

# Connect AI Agent to Your Store (MCP)

Connect your AI coding agent to your Mobazha store via MCP (Model Context Protocol). Once connected, your agent can directly manage products, orders, messages, and more.

> **This skill requires credentials.** The agent needs an API token from your store to connect. The agent must ask for your explicit consent before initiating any connection to your store. Tokens should be stored in environment variables, never committed to source control.

## What You Get

After connecting, your AI agent has access to 30+ store management tools:

| Category | Tools | What They Do |
|----------|-------|-------------|
| **Products** | `listings_create`, `listings_update`, `listings_delete`, `listings_list_mine`, `listings_import_json` | Full product CRUD + bulk import |
| **Orders** | `orders_get_sales`, `orders_confirm`, `orders_ship`, `orders_refund` | Order lifecycle |
| **Chat** | `chat_get_conversations`, `chat_send_message` | Buyer communication |
| **Discounts** | `discounts_create`, `discounts_update`, `discounts_delete` | Promotions |
| **Collections** | `collections_create`, `collections_add_products` | Product organization |
| **Profile** | `profile_get`, `profile_update` | Store identity |
| **Notifications** | `notifications_list`, `notifications_mark_read` | Activity feed |
| **Search** | `search_listings`, `search_profiles` | Marketplace discovery |
| **Finance** | `exchange_rates_get`, `wallet_get_receiving_accounts`, `fiat_get_providers` | Payments and rates |

## Connection Method: Streamable HTTP (Recommended)

All Mobazha deployments include a built-in MCP endpoint using Streamable HTTP. This is the recommended method because:

- No additional binary to install or maintain
- Tools are always up-to-date with your store version
- Works with Claude Code, Cursor, Codex, and all modern AI agents
- Single endpoint URL — no sub-paths needed

### MCP Endpoint

| Deployment | MCP URL |
|------------|---------|
| **SaaS** | `https://app.mobazha.org/v1/mcp` |
| **Standalone (custom domain)** | `https://shop.example.com/v1/mcp` |
| **Standalone (local Docker)** | `http://localhost/v1/mcp` |
| **Native install (local)** | `http://localhost:5102/v1/mcp` |
| **Native install (VPS)** | `http://<vps-ip>:5102/v1/mcp` |

---

## Step 1: Get Your API Token

### Option A: Admin UI (Recommended)

1. Log in to your store admin panel
   - **SaaS**: `app.mobazha.org` → sign in with Google/GitHub/email
   - **Standalone**: `https://shop.example.com/admin` or `http://localhost:5102/admin`
2. Go to **AI Agents** (top-level navigation)
3. Click any AI client card → a token is auto-created and shown
4. Or expand **Connection Keys (Advanced)** → **Create Token**

### Option B: curl (requires existing credentials)

**SaaS** — First obtain a JWT by signing in, then create an API token:

```bash
curl -X POST https://app.mobazha.org/platform/v1/auth/tokens \
  -H "Authorization: Bearer <your-jwt>" \
  -H "Content-Type: application/json" \
  -d '{"name": "mcp-agent", "scopes": ["seller:*"]}'
```

**Standalone / Native** — Use your admin password (Basic Auth) to create a token:

```bash
# Standalone Docker (custom domain)
curl -X POST https://shop.example.com/v1/auth/tokens \
  -u "admin:<your-password>" \
  -H "Content-Type: application/json" \
  -d '{"name": "mcp-agent", "scopes": ["seller:*"]}'

# Native install (local or VPS, port 5102)
curl -X POST http://localhost:5102/v1/auth/tokens \
  -u "admin:<your-password>" \
  -H "Content-Type: application/json" \
  -d '{"name": "mcp-agent", "scopes": ["seller:*"]}'
```

For a remote VPS, use an SSH tunnel if the port is not public:

```bash
ssh -L 5102:localhost:5102 root@<vps-ip>
# Then use http://localhost:5102 from your local machine
```

> The `token` field in the response is shown **only once** — save it immediately.

---

## Step 2: Configure Your AI Agent

### Claude Code

Add to `~/.claude.json` (or project-level `.mcp.json`):

```json
{
  "mcpServers": {
    "mobazha-store": {
      "type": "streamable-http",
      "url": "https://shop.example.com/v1/mcp",
      "headers": {
        "Authorization": "Bearer <your-token>"
      }
    }
  }
}
```

### Cursor

Add to `.cursor/mcp.json` in your project:

```json
{
  "mcpServers": {
    "mobazha-store": {
      "type": "streamable-http",
      "url": "https://shop.example.com/v1/mcp",
      "headers": {
        "Authorization": "Bearer <your-token>"
      }
    }
  }
}
```

Or go to **Settings > MCP Servers > Add Server** and enter the MCP URL.

### Codex CLI

```bash
codex mcp add mobazha-store --transport http \
  --url "https://shop.example.com/v1/mcp" \
  --header "Authorization: Bearer <your-token>"
```

### OpenCode

Add to `opencode.json`:

```json
{
  "mcp": {
    "mobazha-store": {
      "type": "streamable-http",
      "url": "https://shop.example.com/v1/mcp",
      "headers": {
        "Authorization": "Bearer <your-token>"
      }
    }
  }
}
```

> Replace `https://shop.example.com` with your actual store URL from the table above.

---

## Step 3: Verify the Connection

Ask your AI agent:

> "List my store's products" or "Show my recent orders"

The agent should call `listings_list_mine` or `orders_get_sales` and return results. If it works, the connection is live.

For a guide on what you can do with MCP tools, see the `store-management` skill.

---

## Advanced: stdio Transport

For environments where Streamable HTTP is not supported by the AI agent, or for air-gapped setups, a `mobazha-mcp` stdio binary is available. It ships with the standalone Docker image and native install.

### When to Use stdio

- Your AI agent doesn't support Streamable HTTP MCP transport
- Air-gapped or restricted network environment
- Development/debugging of the MCP layer itself

### Using stdio from Standalone Docker

The binary is bundled in the container. For standalone nodes, you must set `--identity-path /v1/auth/identity`:

```bash
docker exec -it <container> mobazha-mcp \
  --gateway-url http://localhost:5102 \
  --identity-path /v1/auth/identity \
  --token <token>
```

### stdio CLI Reference

| Flag | Env Variable | Default | Description |
|------|-------------|---------|-------------|
| `--gateway-url` | `MOBAZHA_GATEWAY_URL` | `http://localhost:5102` | Store gateway URL |
| `--token` | `MOBAZHA_TOKEN` | (required) | API token (`mbz_` prefix) |
| `--identity-path` | — | `/platform/v1/auth/identity` | Identity API path. Use `/v1/auth/identity` for standalone/native |
| `--search-url` | `MOBAZHA_SEARCH_URL` | (optional) | Marketplace search API URL |

> **Important**: The default `--identity-path` is for SaaS mode. Standalone and native installs must pass `--identity-path /v1/auth/identity`, otherwise authentication will fail with 404.

### stdio Agent Configuration

```json
{
  "mcpServers": {
    "mobazha-store": {
      "command": "mobazha-mcp",
      "args": [
        "--gateway-url", "http://localhost:5102",
        "--identity-path", "/v1/auth/identity"
      ],
      "env": {
        "MOBAZHA_TOKEN": "<your-token>"
      }
    }
  }
}
```

---

## Troubleshooting

### "connection refused" or timeout

- Native install: verify the store is running with `curl http://localhost:5102/healthz`
- Standalone Docker: the MCP endpoint is at port 80/443 (not 5102), try `curl http://localhost/healthz`
- For remote stores, check that the domain resolves and HTTPS is configured

### "401 Unauthorized"

- Verify the token: `curl -H "Authorization: Bearer <token>" http://localhost:5102/v1/profiles`
- Token may have expired — generate a new one
- Ensure the token has the required scopes for the tools you want to use

### "tool not found"

- `search_listings` and `search_profiles` require the marketplace search service
- Some tools require specific scopes on the API token (e.g., `listings:write` for `listings_create`)

### Credential Safety

- **Never hardcode tokens** in source code or config files committed to git
- Store the token in environment variables or a secrets manager
- Add MCP config files to `.gitignore` if they contain tokens
- Tokens can be revoked and regenerated at any time from the store admin panel
- The agent must **never log, display, or transmit** tokens to any party other than the target store endpoint
