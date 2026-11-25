---
name: mcp-starter-kit
description: >-
  Build a STANDARD MCP server (secure, online, with OAuth) for ANY project. When
  run, the skill ASKS to confirm: (1) the MCP project name; (2) whether the backend
  already has an API-key system — if NOT, it emits API-KEY-BACKEND-GUIDE.md so you
  can build one (mirroring the reference system). Then it scaffolds the MCP repo from
  templates/: Streamable HTTP + stdio + OAuth, verify-at-init, session cap/TTL,
  rate-limit, audit, Dockerfile. Use when the user says "create an MCP", "build an
  MCP server", or "connect project X to ChatGPT/Claude with a key".
---

# mcp-starter-kit — build a standard MCP server for any project

MCP is the machine-to-machine bridge between an AI agent (Claude Desktop/Web, ChatGPT,
your own agent) and a project's API. Each *tool* maps to one `/ext/*` endpoint and is
authenticated with an **API key + scopes**.

```
AI agent ──MCP (Streamable HTTP / stdio / OAuth)──▶ <project>-mcp ──REST + Bearer key──▶ Backend
```

This kit contains:
- `SKILL.md` (this file) — the workflow + confirmation flow.
- `templates/` — the full MCP source (just change the name + tool list).
- `API-KEY-BACKEND-GUIDE.md` — how to build the backend API-key system (when it's missing).

---

## STEP 0 — CONFIRM (required; ask before doing anything)

> Shortcut: if the user has filled [`feature.md`](feature.md) (project config + tool
> list), read it instead of asking — confirm the values, then jump to STEP 1. Otherwise
> ask the questions below (and offer to fill `feature.md` for them as you go).

Ask the user in order, wait for each answer before continuing:

**Q1 — MCP project name?**
> "What is the MCP project name? (e.g. `shop`, `acme`, `lms`) → the repo will be `<name>-mcp`."
Call this `<PROJECT>`. Do not invent it — always ask.

**Q2 — Does the backend already have an API-key system?**
> "Does your backend already have an **API-key tab** (hashed keys + scopes + an `/ext/me`
> endpoint)?  A) Yes   B) No"

- **No (B)** → **emit the guide**: copy this kit's `API-KEY-BACKEND-GUIDE.md` into the
  user's project (e.g. `<repo>/API-KEY-BACKEND-GUIDE.md`), then say:
  > "Your backend has no API-key channel yet — I've exported `API-KEY-BACKEND-GUIDE.md`.
  > Build that first (especially `/ext/me` + `/scopes` + `RequireAPIKey`), then come back
  > to scaffold the MCP. Want me to implement the backend part in your stack?"
  Stop here until the backend has a key channel (or the user asks you to build it now).
- **Yes (A)** → continue to Q3.

**Q3 — Connection details** (once a key channel exists):
> - **API base**: backend URL (public `https://api.../api/v1`; internal Docker `http://api:8080/api/v1`).
> - **Key prefix**: e.g. `sk_`, `pk_` (for early validation; leave empty if none).
> - **Tool list**: each tool = one `/ext/*` endpoint + one scope. If unsure, start with `whoami` + a couple of sample tools.

---

## STEP 1 — Scaffold the MCP repo

1. Create `<PROJECT>-mcp/` and copy the whole `templates/` into it (rename `gitignore` → `.gitignore`).
2. **Replace the placeholder** `__PROJECT__` → `<PROJECT>` in: `package.json`, `src/server.ts`, `src/http.ts`, `README.md`, `.env.example`.
3. Fill `.env` from `.env.example`: `MCP_API_BASE`, `MCP_KEY_PREFIX`.
4. Edit `src/server.ts` — add a `readTool(...)` per tool (one endpoint + a description that names the scope + zod input validation: uuid/regex/min-max).

```
<PROJECT>-mcp/
├── package.json  tsconfig.json  Dockerfile  .env.example  .gitignore  README.md
└── src/ index.ts config.ts apiClient.ts audit.ts server.ts http.ts oauth.ts stdio.ts
```

5. `npm install && npm run build` → fix any errors.

---

## STEP 2 — Test locally

```bash
MCP_TRANSPORT=http PORT=8787 MCP_API_BASE=<api> npm start   # GET /health
npx @modelcontextprotocol/inspector   # Streamable HTTP + URL + header Authorization: Bearer <key>
```
Expect: `tools/list` returns all tools; `tools/call whoami` returns the key name + scopes.

---

## STEP 3 — Host online (behind TLS)

- Run the container (Dockerfile) behind a TLS reverse proxy. Proxy the `/mcp` path:
  ```nginx
  location = /mcp {
      proxy_pass http://<project>-mcp:8787/mcp;
      proxy_http_version 1.1; proxy_set_header Host $host; proxy_set_header Connection "";
      proxy_buffering off; proxy_read_timeout 3600s; client_max_body_size 1m;
  }
  ```
  → public URL `https://<domain>/mcp` (no new subdomain/cert needed).
- **If using OAuth** (for the ChatGPT app / Claude web): proxy the OAuth paths and set the secret:
  ```nginx
  location ~ ^/\.well-known/oauth-(protected-resource|authorization-server) { proxy_pass http://<project>-mcp:8787; }
  location ^~ /mcp-oauth/ { proxy_pass http://<project>-mcp:8787; client_max_body_size 1m; }
  ```
  env: `MCP_OAUTH_SECRET=$(openssl rand -hex 32)` + `MCP_PUBLIC_URL=https://<domain>`.
  ⚠️ If the backend is an SPA that returns `200 index.html` for unknown paths, you MUST route
  the well-known paths to the MCP as above, otherwise OAuth clients report
  "Couldn't register with sign-in service".

Verify (replace `<domain>`, `<key>`):
```bash
curl -s -o /dev/null -w "%{http_code}\n" https://<domain>/.well-known/oauth-protected-resource/mcp   # 200 if OAuth is on
curl -s -X POST https://<domain>/mcp -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" -H "x-api-key: <key>" \
  -d '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"t","version":"1"}}}'
# → 200 + mcp-session-id + serverInfo
```

---

## STEP 4 — Connect a client

| Client | How |
|---|---|
| **Claude Desktop** | `mcpServers.<PROJECT>` = `npx -y mcp-remote https://<domain>/mcp --header "Authorization: Bearer <key>"` → Cmd+Q and reopen |
| **Claude web** | Custom connector: URL `/mcp`, header **`x-api-key`** = key (the `authorization` header is reserved by Claude for OAuth) |
| **ChatGPT app** | Needs **OAuth** enabled + a Business/Enterprise plan. Connector: URL `/mcp`, Auth **OAuth**, Streamable HTTP → paste the key on the consent page |
| **OpenAI API** | `tools:[{type:"mcp", server_url:".../mcp", headers:{"x-api-key":"<key>"}}]` — works right away |
| **Adding a new tool to a connected client** | Clients cache the tool list at connect time → you must **re-scan / remove + re-add the connector** (reloading the chat is not enough) |

---

## Security (already built into templates)

- Key via env (stdio) or header/OAuth (http) — never hardcoded, never commit `.env`.
- HTTP: **verify the key against the backend `/ext/me` at initialize** (blocks pre-auth DoS).
- **Session cap + idle-TTL sweep**, **per-IP rate limit** on the initialize path, **bind sha256(key) to the session**.
- OAuth: **PKCE S256**, redirect_uri **allowlist**, AES-256-GCM tokens (stateless), single-use codes.
- `apiClient` blocks cross-host SSRF + times out. Audit to **stderr** (stdout = JSON-RPC), secrets redacted.
- **Read-only (GET) by default**; for writes add a dedicated write scope and think it through.

## Handoff checklist
```
[ ] Ask: <PROJECT> name; does the backend already have a key channel?
[ ] If not → emit API-KEY-BACKEND-GUIDE.md, build the backend first (with /ext/me + scopes)
[ ] Scaffold from templates/, replace __PROJECT__, fill .env, add tools in server.ts
[ ] npm build passes; test with Inspector (tools/list + whoami)
[ ] Host behind TLS (path /mcp); enable OAuth if the ChatGPT app is needed
[ ] Verify with curl: initialize 200; (OAuth) well-known 200
[ ] Connect a client; .env not committed; rotate the key if leaked
```
