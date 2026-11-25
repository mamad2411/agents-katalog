---
name: swarms-marketplace-mcp
description: Use the Swarms Marketplace as an MCP server at https://swarms.world/mcp. Covers connecting from Claude Code, Claude Desktop, Cursor, the Python and TypeScript MCP SDKs, and raw JSON-RPC; authentication with a Swarms API key; the complete tool catalog (search and fetch agents, prompts, and tools; publish and edit listings; reviews; your own products and fees; bundles); response shapes; workflows; errors; limits; and troubleshooting.
---

# Swarms Marketplace MCP Server – Skill Reference

Use this skill when an agent should **search, read, publish, edit, review, or manage listings on the Swarms Marketplace (swarms.world) over the Model Context Protocol** instead of composing REST calls by hand.

The marketplace exposes every documented REST operation as an MCP tool. The tool list is generated from the site's own OpenAPI document (`https://swarms.world/openapi.json`), so it is always in step with the API. Discovery (`initialize`, `ping`, `tools/list`) is public; `tools/call` requires a Swarms API key.

Related references:
- REST equivalent of every tool: https://swarms.world/skill.md and https://swarms.world/openapi.json
- Machine-readable site map: https://swarms.world/llms.txt
- Swarms API (run agents and swarms): https://docs.swarms.ai
- Get an API key: https://swarms.world/platform/api-keys

---

## 1. At a glance

| | |
|---|---|
| Endpoint | `https://swarms.world/mcp` |
| Transport | Streamable HTTP (JSON-RPC 2.0 over `POST`), JSON responses, no server-initiated stream |
| Protocol versions | `2025-06-18` (default), `2025-03-26`, `2024-11-05` |
| Auth | `Authorization: Bearer <SWARMS_API_KEY>` on `tools/call`; `initialize`, `ping` and `tools/list` need no key |
| Sessions | None. The server is stateless; there is no `Mcp-Session-Id` to keep |
| Capabilities | `tools` only (no resources, prompts, sampling, or subscriptions) |
| Tool count | One per OpenAPI operation, 29 at the time of writing |
| Rate limit | 300 requests per minute per IP, shared with the rest of the marketplace API |
| Fallback path | `https://swarms.world/api/mcp` (same handler, see Troubleshooting) |

A browser `GET https://swarms.world/mcp` is redirected to the human catalog of MCP servers at `https://swarms.world/mcp-servers`. MCP clients never see that redirect because they `POST`.

---

## 2. Authentication

Create a key at https://swarms.world/platform/api-keys and send it on every `tools/call` request (sending it on every request is fine too):

```
Authorization: Bearer sk-...
```

`x-api-key: sk-...` is accepted as an alternative header.

The key is validated when a tool is called; `initialize`, `ping` and `tools/list` run without one. It is **forwarded to every tool call**, so tools that need ownership (your products, your fees, publishing, editing, reviewing) act as the account that owns the key.

| Situation | HTTP | JSON-RPC error |
|---|---|---|
| No key on `tools/call` | 401 | `-32001` "A Swarms API key is required…" + `WWW-Authenticate: Bearer` |
| Invalid, revoked, or deleted key | 401 | `-32001` "Invalid API Key…" |

Keys are secrets. Do not paste them into shared configs, and do not route them through MCP hosts you do not control.

---

## 3. Connecting

### Claude Code

```bash
claude mcp add --transport http swarms https://swarms.world/mcp \
  --header "Authorization: Bearer $SWARMS_API_KEY"
```

Then in a session: `/mcp` to confirm the connection, and the tools appear as `mcp__swarms__<tool>`.

### Cursor (`.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "swarms": {
      "url": "https://swarms.world/mcp",
      "headers": { "Authorization": "Bearer sk-..." }
    }
  }
}
```

### Claude Desktop and other stdio-only clients

Bridge with `mcp-remote`:

```json
{
  "mcpServers": {
    "swarms": {
      "command": "npx",
      "args": [
        "-y", "mcp-remote", "https://swarms.world/mcp",
        "--header", "Authorization: Bearer sk-..."
      ]
    }
  }
}
```

### Python (`mcp` SDK 2.x)

```python
import asyncio, json, os
import httpx2
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

URL = "https://swarms.world/mcp"
HEADERS = {"Authorization": f"Bearer {os.environ['SWARMS_API_KEY']}"}

async def main():
    async with httpx2.AsyncClient(headers=HEADERS, timeout=60) as http:
        async with streamable_http_client(URL, http_client=http) as streams:
            async with ClientSession(streams[0], streams[1]) as session:
                await session.initialize()
                tools = await session.list_tools()
                print([t.name for t in tools.tools])

                res = await session.call_tool(
                    "get_get-prompts", {"limit": 5, "is_free": True, "name": "research"}
                )
                page = json.loads(res.content[0].text)
                for row in page["data"]:
                    print(row["id"], row["name"])

asyncio.run(main())
```

For `mcp` 1.x the import is `from mcp.client.streamable_http import streamablehttp_client` and it takes `headers=` directly.

### TypeScript (`@modelcontextprotocol/sdk`)

```ts
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const transport = new StreamableHTTPClientTransport(new URL("https://swarms.world/mcp"), {
  requestInit: { headers: { Authorization: `Bearer ${process.env.SWARMS_API_KEY}` } },
});
const client = new Client({ name: "my-agent", version: "1.0.0" });
await client.connect(transport);

const { tools } = await client.listTools();
const result = await client.callTool({ name: "get_get-agents", arguments: { limit: 3, category: "Finance" } });
const page = JSON.parse((result.content as any)[0].text);
```

### Raw JSON-RPC (curl)

```bash
# initialize
curl -s -X POST https://swarms.world/mcp \
  -H "Authorization: Bearer $SWARMS_API_KEY" -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"curl","version":"1"}}}'

# list tools
curl -s -X POST https://swarms.world/mcp \
  -H "Authorization: Bearer $SWARMS_API_KEY" -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'

# call a tool
curl -s -X POST https://swarms.world/mcp \
  -H "Authorization: Bearer $SWARMS_API_KEY" -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_get-prompts","arguments":{"limit":2,"is_free":true}}}'
```

---

## 4. Protocol details

Supported methods:

| Method | Behaviour |
|---|---|
| `initialize` | Returns `protocolVersion` (echoes yours if supported, else `2025-06-18`), `capabilities.tools`, `serverInfo` (`swarms-marketplace` 1.0.0), and `instructions` |
| `notifications/*` | Any message without an `id` → `202 Accepted`, no body |
| `ping` | `{ "result": {} }` |
| `tools/list` | The full tool catalog. No pagination; there is no `nextCursor` |
| `tools/call` | Runs one tool; see §6 for the result shape |

Anything else, including `resources/list` and `prompts/list`, returns `-32601`.

HTTP methods on the endpoint:

| Request | Response |
|---|---|
| `POST` JSON-RPC message | JSON-RPC response, always `application/json` (never `text/event-stream`) |
| `GET` with `Accept: text/event-stream` | `405` (no server-to-client stream; clients fall back to plain POST) |
| `DELETE` | `204` (nothing to end) |
| `OPTIONS` | `204` with permissive CORS |

Batches (JSON arrays) are rejected with `-32600`. Send one message per request.

---

## 5. Tool catalog

### Naming

Tool names are derived from the REST operation: `<method>_<path without /api/>` with `/`, `{`, and `}` turned into `_`. So `GET /api/get-prompts/{id}` is `get_get-prompts_id`, and `POST /api/v1/publish/bundle` is `post_v1_publish_bundle`. Names are stable as long as the REST path is.

### Argument conventions

- Every tool's `inputSchema` is an object with `additionalProperties: false`. An unknown argument is rejected with `-32602` naming the bad key.
- `get_*` tools map arguments to query-string parameters. The OpenAPI document types them as strings, so `is_free` is `"true"`/`"false"`, `limit` is `"20"`; JSON booleans and numbers are accepted too and stringified.
- `post_*` tools map arguments to the JSON body. Types are the real JSON types.
- Path parameters (`id`) are always required.
- List tools accept `page` (1-based, default 1) and `limit` (1–100, default 20).

### 5.1 Discover the catalog (read-only)

| Tool | Arguments | Returns |
|---|---|---|
| `get_get-agents` | `name`, `tag` (comma-separated, any match), `use_case`, `category`, `language`, `req_package`, `is_free`, `min_price`, `max_price`, `page`, `limit` | `{ data: AgentListItem[], pagination: { total, page, limit, has_more } }` |
| `get_get-prompts` | `name`, `tag`, `use_case`, `category`, `is_free`, `min_price`, `max_price`, `page`, `limit`, `id` | `{ data: PromptListItem[], pagination: {…} }` (`id` performs a direct lookup) |
| `get_get-tools` | `name`, `tag`, `use_case`, `category`, `is_free`, `min_price`, `max_price`, `page`, `limit` | `{ tools: ToolListItem[], pagination: { page, limit, total, total_pages, has_next, has_prev } }` |
| `get_get-tokenized-products` | `type` (`agent` \| `prompt` \| `tool`), `page`, `limit` | `{ user_id, username, total, counts, data: [...], pagination }` — **your** tokenized listings with token metadata |
| `post_get-tokenized-products` | same fields in the body (`page`, `limit` as numbers) | same as above |
| `post_query-agents` | `agent_id`, `username`, `agent_name`, `limit` | Agents matching any of the given selectors |
| `post_query-prompts` | `prompt_id`, `username`, `prompt_name`, `limit` | Prompts matching any of the given selectors |

`name` and `use_case` are case-insensitive substring matches. `category` is an exact match against: MCP, Skill, Developer, Automation, Data & Analytics, Security, Productivity, Content & Writing, E-Commerce, Legal, Gaming, Healthcare, Finance, Education, Technology, Marketing, Sales, Customer Support, Research, Public Safety, Other.

### 5.2 Read one listing

| Tool | Arguments | Returns |
|---|---|---|
| `get_get-agents_id` | `id`* | Public fields; `agent` (source) only for free agents; `access_info` |
| `get_get-agents_id_full` | `id`* | The agent including source code, subject to access |
| `get_get-prompts_id` | `id`* (prompt id **or exact name**) | Public fields; `prompt` (body) only for free prompts; `access_info` |
| `get_get-prompts_id_full` | `id`* | The prompt including full body, subject to access |
| `get_prompt-raw_id` | `id`* | The prompt as **Markdown text** with a YAML front matter block (`id`, `name`, `description`, …), not JSON |
| `get_get-tools_id` | `id`* | The tool including source for free tools |
| `get_reviews` | `model_id`* | `{ reviews: [...], average_rating, total }` |

`access_info` looks like `{ has_access, is_owner, is_free, has_purchased, requires_purchase }`. When `requires_purchase` is `true` the body or source is withheld; the listing must be bought on swarms.world first.

### 5.3 Your account (act as the key's owner)

| Tool | Arguments | Returns |
|---|---|---|
| `get_product_list` | `type` (`agent` \| `prompt` \| `tool` \| `bundle` \| `all`, default `all`) | `{ user_id, total, counts: { agents, prompts, tools, bundles }, products }` |
| `post_user-products` | `page`, `limit`, `product_type` (`agent` \| `prompt` \| `tool` \| `all`) | `{ user_id, username, total_products, prompts, agents, tools, pagination, summary }` |
| `get_get-agents_fetch-agent-count` | none | Count of your agents |
| `get_get-prompts_fetch-prompt-count` | none | Count of your prompts |
| `get_product_fees` | one of `url`, `id`, `ca`, `tokenAddress`, `ticker`, `product` | Claimable and claimed creator fees for a tokenized product you own, with USDC equivalent |

### 5.4 Publish and edit

| Tool | Required | Notable optional |
|---|---|---|
| `post_add-agent` | `name`, `description` | `agent` (source), `language`, `requirements`, `useCases`, `tags`, `category`, `is_free` (default true), `price_usd`, `image_url` / `image_base64`, `links`, `x402_url`, `mcp_url`, tokenization fields (see §7.3) |
| `post_add-prompt` | `name`, `prompt`, `description` | `useCases`, `tags`, `category`, `is_free`, `price_usd`, `image_url` / `image_base64`, `links`, tokenization fields |
| `post_edit-agent` | `id`, `name`, `agent`, `description` | Same optional fields as add; must own the listing |
| `post_edit-prompt` | `id`, `name`, `prompt` | Same optional fields as add; must own the listing |
| `post_v1_publish_bundle` | `name`, `items` (1–50) | `description`, `tags`, `business_model`, `links`, `image_url` / `image_base64` |
| `post_update-token-address` | `id`, `type`, `tokenAddress` | `tokenSymbol`; attaches a launched token to a product you own |
| `post_reviews` | `model_id`, `model_type` (`agent` \| `prompt` \| `tool`), `rating` (1–5), `comment` | One review per product per account; `409` if already reviewed |
| `post_get-agents_log-agents` | `data` | Usage telemetry for an agent |

Bundle `items` entries are either a listing reference `{ "url": "https://swarms.world/prompt/<uuid>" }` or an inline custom prompt `{ "name", "description", "content" }`.

Successful publishes return `{ id, listing_url, ... }`; the listing lives at `https://swarms.world/agent/<id>` or `/prompt/<id>`.

### 5.5 Run models

`post_swarms_agent-completions` takes `agent_config` and `task`, and `post_swarms_swarm-completions` takes `agents` and `task`, as their REST operations document in `/openapi.json`. Each run is billed to the API key you connected with. A tool call gives up after 30 seconds, so longer runs fail here: for those, call the Swarms API directly (`https://api.swarms.world/v1/agent/completions`, see https://docs.swarms.ai) or use the hosted Swarms API MCP server at `mcp.swarms.world`.

---

## 6. Result shapes

Every `tools/call` returns MCP content: one `text` block whose `text` is a JSON document (pretty-printed) or, for `get_prompt-raw_id`, Markdown.

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [{ "type": "text", "text": "{\n  \"data\": [...],\n  \"pagination\": {...}\n}" }]
  }
}
```

Parse `result.content[0].text` with a JSON parser; do not regex it.

When the upstream REST call fails, the call still succeeds at the protocol level and the result is flagged so the model can read and recover:

```json
{
  "result": {
    "content": [{ "type": "text", "text": "{\n  \"status\": 404,\n  \"tool\": \"get_get-agents_id\",\n  \"error\": { \"error\": \"Agent not found\" }\n}" }],
    "isError": true
  }
}
```

`status` is the upstream HTTP status; `error` is the upstream body (parsed when JSON, otherwise text).

Protocol-level problems (bad arguments, unknown tool) are JSON-RPC errors, not `isError` results (§8).

---

## 7. Workflows

### 7.1 Find something and read it

1. `get_get-prompts` with `name`, `tag`, or `category`, `is_free: "true"` if the body is needed without purchase, `limit` small.
2. Take `data[i].id` and call `get_get-prompts_id` (or `get_prompt-raw_id` for plain Markdown).
3. Check `access_info.requires_purchase`. If `true`, only metadata is available; link the user to `https://swarms.world/prompt/<id>`.

The same shape works for agents (`get_get-agents` → `get_get-agents_id` / `_full`) and tools (`get_get-tools` → `get_get-tools_id`).

### 7.2 Publish a listing

Minimum prompt:

```json
{ "name": "tools/call", "arguments": {
  "name": "post_add-prompt",
  "arguments": {
    "name": "Meeting Notes Summarizer",
    "description": "Turns raw meeting transcripts into decisions, owners, and deadlines.",
    "prompt": "You are a meticulous meeting secretary...",
    "useCases": [{ "title": "Weekly standups", "description": "Summarize a 30-minute standup" }],
    "tags": ["productivity", "summarization"],
    "category": ["Productivity"],
    "is_free": true
  }
}}
```

For a paid listing set `is_free: false` and `price_usd`. Response carries `id` and `listing_url`. Edit later with `post_edit-prompt` (send the full record; it is a replace, not a patch).

### 7.3 Tokenize at publish time

`post_add-agent` and `post_add-prompt` accept `tokenized_on: true` with `ticker`, `creator_wallet`, `private_key`, `fee_selection` (`market` | `frenzy`), `quote_mint` (`SOL` | `USDC`, agents only), and `vault_mode`. The private key signs the launch transaction and the wallet must hold enough SOL. **Only do this from a client and host you fully control**; never pass a private key through a shared or third-party MCP host. Read the tokenization guide first: https://docs.swarms.ai/docs/marketplace/tokenization_details.

### 7.4 Check earnings

`get_product_fees` with `ticker` (leading `$` optional), `ca`, `id`, or `url`. Returns fees in the pool's quote currency plus a USDC equivalent. Only works for products the key's account owns.

### 7.5 Leave a review

`post_reviews` with `model_id`, `model_type`, `rating` 1–5, and a `comment`. One per product per account.

### 7.6 Curate a bundle

Collect prompt URLs with `get_get-prompts`, then `post_v1_publish_bundle` with `name`, `description`, and `items` (up to 50). Custom inline prompts and marketplace references can be mixed.

---

## 8. Errors

| Where | Code / status | Meaning | What to do |
|---|---|---|---|
| HTTP 401, JSON-RPC `-32001` | Missing or invalid key | Add `Authorization: Bearer`, or create a new key |
| HTTP 400, `-32700` | Body is not JSON | Fix the request |
| HTTP 400, `-32600` | Batch array, wrong `jsonrpc`, or no `method` | Send one well-formed message |
| HTTP 200, `-32601` | Unsupported method | Only `initialize`, `ping`, `tools/list`, `tools/call` exist |
| HTTP 200, `-32602` | Unknown tool, missing required argument, or unknown argument key | Call `tools/list`; the message names the field |
| HTTP 200, `-32603` | Internal error (for example `openapi.json` unreachable) | Retry; report if persistent |
| HTTP 200, result with `isError: true` | Upstream REST call failed | Read `status` and `error`; 404 means the id does not exist, 401/403 means not yours, 409 on reviews means already reviewed, 422/400 means validation |
| HTTP 429 JSON `{ "error": "Too many requests" }` | Marketplace rate limit | Back off; 300 requests per minute per IP |
| HTTP 429 **HTML** "Vercel Security Checkpoint" | Bot challenge from the edge firewall | See Troubleshooting |

Tool calls time out after 30 seconds upstream and return an `isError` result.

---

## 9. Limits and behaviour to know

- **Rate limit:** 300 requests per minute per IP across `/api/*` and `/mcp`, counted per server instance.
- **Tool catalog refresh:** the catalog is built from `/openapi.json` on first use and cached for one hour per instance; a new deploy always starts fresh. New REST operations appear as tools without any client change.
- **No pagination on `tools/list`**, no `listChanged` notifications, no resources or prompts.
- **Free vs paid:** free listings return their body or source; paid listings return metadata plus `access_info` until purchased on the site.
- **Edits are full replacements.** `post_edit-*` expects the complete record.
- **Images:** pass `image_url` (public URL) or `image_base64`; the marketplace stores and serves them.
- **Timestamps** are ISO-8601 UTC. Prices are USD unless a field says otherwise.

---

## 10. Troubleshooting

**`initialize` fails with an HTML page or "Server returned an error response".**
The Vercel edge firewall bot-challenges some automated clients on `/mcp`. Point the client at `https://swarms.world/api/mcp` instead; it is the same handler without the challenge, and the redirect for browsers does not apply there.

**401 on every call although the key is set.**
Check the header is exactly `Authorization: Bearer <key>` (one space) or `x-api-key: <key>`. Keys that were deleted in the dashboard return "Invalid API Key".

**A tool rejects an argument I copied from the REST docs.**
Tool schemas are strict. Run `tools/list` and use the property names it advertises; for `get_*` tools remember the values are query strings.

**`get_get-prompts_id` returns metadata but no `prompt`.**
The listing is paid (`access_info.requires_purchase: true`) or the key's account does not own it. Buy it on the site or use the owner's key.

**Empty `data` with `total: 0`.**
The filters excluded everything. Drop `category` (exact match) and try `name` or `tag` alone.

**Client opens a GET stream and logs a 405.**
Expected. The server has no server-to-client channel; SDKs treat 405 as "no stream" and continue over POST.

---

## 11. Quick reference

```
Endpoint      https://swarms.world/mcp            (fallback: https://swarms.world/api/mcp)
Auth          Authorization: Bearer <SWARMS_API_KEY>
Discover      get_get-agents | get_get-prompts | get_get-tools | get_get-tokenized-products | post_query-agents | post_query-prompts
Read          get_get-agents_id[_full] | get_get-prompts_id[_full] | get_prompt-raw_id | get_get-tools_id | get_reviews
Mine          get_product_list | post_user-products | get_get-agents_fetch-agent-count | get_get-prompts_fetch-prompt-count | get_product_fees
Write         post_add-agent | post_add-prompt | post_edit-agent | post_edit-prompt | post_v1_publish_bundle | post_update-token-address | post_reviews
Result        result.content[0].text → JSON (or Markdown for get_prompt-raw_id); isError:true carries {status, tool, error}
Errors        401/-32001 key · 400/-32700 JSON · 400/-32600 shape · -32601 method · -32602 tool/args · -32603 internal
```
