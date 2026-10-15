---
name: relay0
description: >
  Use Relay0 as a scoped multi-tenant AI gateway and agent-ops API. Prefer the `relay0` CLI
  (`relay0 models`, `relay0 set`, `relay0 get`, `relay0 doctor`)
  over scraping config files or hand-rolled curl. Trigger when the user mentions Relay0; wants
  different models on Codex, Claude Code, Cursor, OpenClaw, or other coding tools; needs to
  discover models; configure base URL or gateway key; run the setup installer or cleanup; check
  usage/quotas; manage keys or provider connections; debug a model route or empty catalog; or
  pick Workspace (api.*) vs Grid (grid.*) hosts — without exposing upstream provider secrets.
---

# Relay0

Relay0 is an OpenAI-compatible gateway plus an agent-safe management API. Use it to:

1. Discover which models a gateway key can actually call.
2. Wire coding tools (Codex, Claude Code, Cursor, OpenClaw, …) to Relay0 **with the correct model ids per tool**.
3. Call chat / responses / messages endpoints.
4. Inspect usage, quotas, keys, and provider health.

**Critical rule:** never invent model names. Always use exact `id` values from model discovery for that key + host.

## Prefer the `relay0` CLI (agents: start here)

The CLI is the **tool-agnostic** path for discovery, health, and **changing models**.

```bash
export PATH="$HOME/.local/bin:$HOME/.relay0/bin:$PATH"

relay0 models                              # list ids (use exactly)
relay0 set codex model cx/gpt-5.5          # change a tool default
relay0 set claude model xai/grok-4.5
relay0 set claude model cx/gpt-5.4-mini --slot haiku
relay0 get codex model
relay0 get claude model
relay0 doctor
relay0 whoami
relay0 usage --period 7d
```

**Canonical model change:** `relay0 set <tool> model <exact-id>` — do not hand-edit configs when this works.

| User asks | Run |
|---|---|
| What models? | `relay0 models` |
| Switch tool to model X | `relay0 set <tool> model <id>` |
| What is tool using? | `relay0 get <tool> model` |
| Health | `relay0 doctor` |

**Rules for agents**

1. Prefer `relay0 models` / `relay0 set` / `relay0 get` over scraping configs or curl.
2. Prefer `~/.relay0/cli.json` over secrets in tool configs.
3. If `command not found: relay0`, try `$HOME/.local/bin/relay0`; else re-run setup.
4. Model ids must come from `relay0 models` (or `relay0 models --cache`) verbatim.
5. Fall back to `references/cli-tools.md` only when `relay0 set` does not support the tool.
6. **Network / DNS failures (critical — do not hang):**
   - Errors like `nodename nor servname provided`, `Name or service not known`, timeouts, or connection refused mean the sandbox/host cannot reach the gateway.
   - **Report once and stop.** Do not retry `relay0 models` more than once. Do not sit in a long “Working…” loop.
   - Immediately try offline path: `relay0 models --cache` and/or `relay0 set <tool> model <id>` (set/get work offline).
   - If the user already named a model id (e.g. `xai/grok-4.5`), run `relay0 set <tool> model <that-id>` without re-fetching the catalog.

## Install this skill

```bash
npx skills add relayzer0/relay0-skills --skill relay0
```

## Setup (env)

Read config in this order: **`relay0` profile** (`~/.relay0/cli.json`) → environment → tool configs (last resort).

Hosted SaaS defaults:

```bash
# Workspace (BYOK) — providers the user connects under /providers
export RELAY0_BASE_URL="https://api.userelay0.com/v1"

# Grid (prepaid pool) — admin-built capacity; use grid host + a Grid key
# export RELAY0_BASE_URL="https://grid.userelay0.com/v1"

export RELAY0_APP_URL="https://app.userelay0.com"
export RELAY0_API_KEY="sk-..."            # Relay0 gateway key (not OpenAI/Anthropic/xAI)
export RELAY0_AGENT_KEY="$RELAY0_API_KEY" # same key often works for agent-ops
```

Or pull exports:

```bash
eval "$(relay0 env pull --shell zsh)"
# or
set -a && source /path/to/relay0-agent.env && set +a
```

| Variable | Used for |
|---|---|
| `RELAY0_BASE_URL` | Gateway OpenAI-compatible API (`/models`, `/chat/completions`, `/responses`, `/messages`) |
| `RELAY0_API_KEY` | `Authorization: Bearer` on the gateway |
| `RELAY0_APP_URL` | Management host for `/api/cloud/agent/*` |
| `RELAY0_AGENT_KEY` | Bearer for agent-ops (often same as gateway key) |

Never ask for upstream provider secrets (OpenAI, Anthropic, Google, xAI, OAuth tokens). Only Relay0 gateway keys.

### Two products, not brand lanes

| Lane | Host | Who connects capacity | Typical model ids |
|---|---|---|---|
| **Workspace (BYOK)** | `https://api.userelay0.com/v1` | User/admin under `/providers` | Prefixed aliases: `xai/grok-4.5`, `cx/gpt-5.5`, `cc/claude-sonnet-…` |
| **Grid (prepaid)** | `https://grid.userelay0.com/v1` | Platform admin Grid pool only | Retail bare ids: `grok-4.5` (not `xai/grok-4.5`) |

- Brands ≠ capacity. xAI / ChatGPT / Claude can be **workspace BYOK** if the user connected them, or **Grid** if an admin put them in the pool.
- Wrong host for the key type → **403**. Grid keys must hit `grid.*`; workspace keys hit `api.*`.
- Console: Keys + Providers at `https://app.userelay0.com`.

If only `RELAY0_BASE_URL` is set, derive `RELAY0_APP_URL` only when obvious (`api.` / `grid.` → `app.`). Prefer asking for the app URL before calling agent-ops.

---

## Agent playbook: figure out models for any tool

When the user asks “what models can I use?”, “switch my model”, “use Grok/Claude/GPT in this tool”, or you need to configure a client:

### Step 1 — Discover

```bash
relay0 models
# if DNS/network fails (once only — do not hang):
relay0 models --cache
```

- Use exact model id strings.
- On DNS/network error: report once, use `--cache` or the id the user already named, then Step 3.
- Never retry `relay0 models` more than once when DNS fails.

### Step 2 — Pick an id

If the user already named a model (e.g. `xai/grok-4.5`), use it. Otherwise filter `relay0 models` / `--cache` output.

### Step 3 — Apply with CLI only (mandatory)

```bash
relay0 set <tool> model <exact-id>
```

Examples: `relay0 set codex model xai/grok-4.5` · `relay0 set claude model cx/gpt-5.5`

**Forbidden when CLI works:** hand-editing `~/.codex/config.toml`, Claude `settings.json`, etc.

### Step 4 — Verify with the wire format that tool uses

1. Change only the target tool (other tools keep their own defaults).
2. Restart the tool if it caches config.
3. Smoke-test:

```bash
# Most OpenAI-compatible clients
curl -sS -X POST "$RELAY0_BASE_URL/chat/completions" \
  -H "Authorization: Bearer $RELAY0_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"model\":\"$MODEL_ID\",\"messages\":[{\"role\":\"user\",\"content\":\"ping\"}],\"stream\":false}"

# Responses API clients (e.g. Codex)
curl -sS -X POST "$RELAY0_BASE_URL/responses" \
  -H "Authorization: Bearer $RELAY0_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"model\":\"$MODEL_ID\",\"input\":\"Reply with exactly: OK\",\"max_output_tokens\":20}"

# Anthropic Messages clients (e.g. Claude Code)
curl -sS -X POST "$RELAY0_BASE_URL/messages" \
  -H "Authorization: Bearer $RELAY0_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d "{\"model\":\"$MODEL_ID\",\"max_tokens\":64,\"messages\":[{\"role\":\"user\",\"content\":\"ping\"}]}"
```

4. Optional: `relay0 usage --period 7d` to see which connection served the request.

### Different models per tool (and per slot)

Supported and expected: Claude’s three slots, OpenClaw primary vs explorer, Cursor custom models, Codex default vs subagent — each can be a different discovery id.

Do **not** assume one global “Relay0 model” for all tools. Discover once, then set each tool independently.

---

## One-shot installer (recommended for humans)

Hosted setup script configures tools from a live catalog:

```text
https://app.userelay0.com/setup?token=sk-...&capacity=byok|grid&tools=all
# Non-interactive skill install (optional):
https://app.userelay0.com/setup?token=sk-...&capacity=byok&tools=all&skill=yes
```

- Prompts or uses `capacity=byok|grid` → correct host.
- Fetches `/models` and picks a sensible default for every selected tool.
- Writes each tool’s native config (Claude env slots, Codex provider + bearer, OpenClaw provider block, shell env, …).
- **Asks whether to install or update this Relay0 skill** (default yes). If the skill is already present, setup runs `npx skills update relay0` and re-adds from the package so agents get the latest. Force with `skill=yes` / `RELAY0_INSTALL_SKILL=1`, skip with `skill=no` / `0`.
- Cleanup: `tools=cleanup` removes Relay0 blocks without nuking the whole user config when possible.

After install, agents should still re-run `relay0 models` before recommending a different default.

---

## Safety rules

- Treat `RELAY0_API_KEY` / `RELAY0_AGENT_KEY` as secrets; do not print them.
- Reveal a full key only when the user asks and Relay0 just returned a one-time create response.
- Never request or log upstream provider API keys or OAuth tokens.
- Inspect before mutating keys/connections; ask before disable unless user requested automated remediation.
- Summarize mutations: endpoint, object id, old → new, reason.

---

## Health-check playbook

When asked to test/verify/check Relay0, **prefer the CLI**:

```bash
relay0 doctor
relay0 whoami
relay0 models
relay0 connections list
relay0 usage --period 7d
```

HTTP fallback (same order of intent):

1. `GET $RELAY0_APP_URL/api/cloud/agent/summary` — role, permissions, key active.
2. `GET $RELAY0_BASE_URL/models` — visible model count + sample ids.
3. `GET $RELAY0_APP_URL/api/cloud/agent/connections` — healthy vs unhealthy.
4. Live call on `/responses` or `/chat/completions` with a real model id.
5. `GET .../usage?period=7d&pageSize=5` — which `connectionId` served the request (failover may succeed after an error row).

---

## Chat and coding requests

Use the wire format your **client** speaks. Model id is always from discovery.

```bash
# OpenAI-compatible chat (most CLIs, SDKs, Cursor-like tools)
curl -X POST "$RELAY0_BASE_URL/chat/completions" \
  -H "Authorization: Bearer $RELAY0_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"<id-from-discovery>","messages":[{"role":"user","content":"Hello"}],"stream":false}'

# Anthropic Messages
curl -X POST "$RELAY0_BASE_URL/messages" \
  -H "Authorization: Bearer $RELAY0_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"model":"<id-from-discovery>","max_tokens":1024,"messages":[{"role":"user","content":"Hello"}]}'

# OpenAI Responses
curl -X POST "$RELAY0_BASE_URL/responses" \
  -H "Authorization: Bearer $RELAY0_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"<id-from-discovery>","input":"Reply with exactly: Relay0 OK","max_output_tokens":20}'
```

---

## Coding tool setup

Read **`references/cli-tools.md`** for per-tool config and “change model later” recipes.

Prefer:

1. Hosted `/setup` or `relay0 config pull --tool <name|all>`
2. Console setup snippets at `https://app.userelay0.com`
3. Manual file edits only when the user already uses a specific tool

Do not treat any single coding agent as the default product path.

---

## Agent operations

Prefer CLI: `relay0 whoami`, `relay0 usage`, `relay0 keys list`, `relay0 connections list`.

HTTP fallback:

```bash
curl "$RELAY0_APP_URL/api/cloud/agent/summary" \
  -H "Authorization: Bearer $RELAY0_AGENT_KEY"
```

| Task | Method + path |
|---|---|
| Summary | `GET /api/cloud/agent/summary` |
| Usage | `GET /api/cloud/agent/usage?period=7d&pageSize=20` |
| Keys | `GET` / `POST` / `PATCH /api/cloud/agent/keys` |
| Connections | `GET` / `PATCH /api/cloud/agent/connections` |
| Quotas | `GET /api/cloud/agent/quotas` |

Schemas and examples: `references/agent-api.md`.

### Connection health

From `GET .../connections`:

- `healthStatus`: `healthy` | `unhealthy`
- `lastHealthResult`, `lastError`, `priority`, model lock timestamps
- OAuth `token_invalidated` → **user must re-auth in the app**; do not auto-disable; routing may still succeed via another connection

---

## Error handling

| Signal | Action |
|---|---|
| `401` gateway | Check `RELAY0_API_KEY` / tool is using the Relay0 key (not an upstream key) |
| `403` gateway | Host/key capacity mismatch (api vs grid) |
| `403` agent-ops | Missing `manageKeys` / `manageConnections` |
| Empty model list | No visible providers for this key/lane |
| Model not found | Wrong id — re-run `relay0 models`; do not strip prefixes |
| Tool won’t route | Confirm base URL + key + **exact** model id for that tool’s wire format |
| Intermittent fail | `relay0 connections list` + `relay0 usage` (failover rows) |

```
401 on gateway           -> RELAY0_API_KEY; re-run setup or env pull for the affected tool
403 on gateway           -> api.* vs grid.* mismatch for key type
empty models             -> connect providers (BYOK) or publish Grid pool; wrong host
model not found          -> exact id from relay0 models for this host
OAuth token_invalidated  -> human reconnect in app; do not auto-disable
```

Tool-specific auth footguns (Claude env vars, Codex bearer + `wire_api=responses`, etc.) live in `references/cli-tools.md` — look them up **after** identifying which tool failed.

---

## User-facing summary pattern

```text
Relay0: checked <summary/usage/models/connections/tools>.
Host/lane: <api workspace | grid> <base url>.
Visible models: <count>; using <id> for <tool>.
Per-tool models: <tool>=<id>, … (only tools the user asked about).
Usage: <requests/tokens if checked>; routed via <connection if known>.
Actions: <none or mutation summary>.
Risk: <missing key / empty catalog / unhealthy OAuth / host mismatch / …>.
```
