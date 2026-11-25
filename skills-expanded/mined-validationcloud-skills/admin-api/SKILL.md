---
name: admin-api
description: >-
  Use when calling, exploring, or generating code for the Validation Cloud Node
  API Admin API. Triggers on requests to manage RPC endpoints (create, list,
  delete, enable, disable), check account plan / compute-unit quota & usage,
  list supported chains, or look up compute-unit costs — anything under
  /admin/v1. Also use for "how do I … with the VC Admin API", generating a
  curl/JavaScript/Python/Go snippet or client, or testing a vc_adm_ admin key.
allowed-tools:
  - Read
  - Write
  - Bash(bash ${SKILL_DIR}/scripts/call.sh *)
  - Bash(jq *)
---

# Validation Cloud — Node API Admin API

Help the user work with the Validation Cloud **Node API Admin API** — a
programmatic, API-key-authenticated surface under `/admin/v1` for managing RPC
endpoints and reading account/usage data without the web dashboard.

> **Agent setup (any assistant).** Throughout this file, `${SKILL_DIR}` is the
> absolute path to the directory containing this `SKILL.md`. Before running any
> command, resolve it to a real path. Under Claude Code, set
> `SKILL_DIR="${CLAUDE_SKILL_DIR}"` (Claude injects `CLAUDE_SKILL_DIR`); for any
> other agent, set it once to wherever this skill lives, e.g.
> `export SKILL_DIR=/path/to/skills/admin-api`. All assets
> (`scripts/`, `references/`, `templates/`) are siblings of this file, so the
> only environment-specific value is that one directory path. The skill needs
> nothing Claude-specific beyond resolving `${SKILL_DIR}` and having `bash`,
> `curl`, and (optionally) `jq` available.

This skill works in three modes; pick based on what the user wants. Don't
announce the mode — just do the right thing.

| The user wants to…                              | Mode          |
|-------------------------------------------------|---------------|
| Actually call the API and see results           | **Call**      |
| Understand the API / get a snippet              | **Reference** |
| Get a reusable client in their codebase         | **Scaffold**  |

The authoritative contract is `references/openapi.json` (OpenAPI 3.1). The
human-readable companion is `references/endpoints.md`. Error/scope/rate-limit
details are in `references/errors.md`. Read those files on demand — don't
pre-load them.

---

## The API at a glance

- **Base URL:** `https://api.validationcloud.io/admin/v1`.
- **Auth:** `Authorization: ApiKey vc_adm_...` — the `ApiKey` scheme, **not**
  `Bearer`. Keys are team-bound; everything is scoped to that team.
- **Scopes:** each key is `READ` or `WRITE`. Reads need `READ`; create / delete
  / enable / disable need `WRITE`. `GET /health` reveals a key's scope.
- **Operations** (all under `/admin/v1`):
  - `GET /health` — liveness + auth/scope check
  - `GET /account` — plan, CU quota, CU used/remaining, billing cycle
  - `GET /chains` — supported chains & networks
  - `GET /compute-unit-costs` — per-method CU price list
  - `GET /endpoints` · `POST /endpoints` · `GET|DELETE /endpoints/{id}`
  - `POST /endpoints/{id}/enable` · `POST /endpoints/{id}/disable`
  - `GET /usage` · `GET /endpoints/{id}/usage`

See `references/endpoints.md` for full request/response shapes and examples.

---

## Credentials & safety rules (always apply)

1. **The key comes from the environment, never from you.** The runner reads
   `$VC_ADMIN_KEY`. Never write a key into a file, and never put one on a
   command line you echo. If `$VC_ADMIN_KEY` isn't set, ask the user to export
   it: `export VC_ADMIN_KEY=vc_adm_...`.
2. **Never print a full key or RPC secret in chat.** When you must refer to a
   key or an endpoint's `api_key`/`urls`, redact to the last 4 characters
   (e.g. `vc_adm_…AB12`). The endpoint `urls` field embeds the live RPC secret —
   redact the key portion there too.
3. **Confirm before every write.** `POST /endpoints`, `DELETE /endpoints/{id}`,
   and enable/disable change the customer's account. State exactly what will
   happen (which endpoint) and get an explicit "yes" before running. `DELETE`
   is irreversible — be especially clear.

---

## Mode: Call

Run real requests via the bundled runner and report results.

**Runner:** `${SKILL_DIR}/scripts/call.sh`

```bash
bash "${SKILL_DIR}/scripts/call.sh" <METHOD> <PATH> [JSON_BODY]
```

- `<METHOD>`: `GET` | `POST` | `DELETE`
- `<PATH>`: a path under the API — `/account`, `/endpoints`,
  `/endpoints/{id}/usage?granularity=DAY`. **Do not** include the `/admin/v1`
  prefix; the runner adds it. Quote paths containing `?` or `&`.
- `[JSON_BODY]`: raw JSON for `POST /endpoints` only.

It reads `$VC_ADMIN_KEY` (required) and prints `HTTP <status>` then the JSON
body, exiting non-zero on HTTP ≥ 400.

**Flow:**
1. Confirm `$VC_ADMIN_KEY` is set.
2. For a write, confirm intent per the safety rules above.
3. Run the command. Summarize the result; for big payloads (chains,
   compute-unit-costs) filter with `jq` rather than dumping everything.
4. On an error, read the `code` from the envelope and explain it using
   `references/errors.md` (e.g. `403 forbidden` → key lacks WRITE scope).

**Examples:**
```bash
# verify the key and see its scope
bash "${SKILL_DIR}/scripts/call.sh" GET /health
# account quota
bash "${SKILL_DIR}/scripts/call.sh" GET /account
# create an endpoint (WRITE — confirm first)
bash "${SKILL_DIR}/scripts/call.sh" POST /endpoints \
  '{"name":"my-eth-mainnet","chain":"ethereum","network":"mainnet"}'
```

---

## Mode: Reference

Answer questions and produce snippets grounded in the bundled spec — do not
invent fields or endpoints.

- For "what does X return / what params does Y take", read
  `references/endpoints.md` (and `references/openapi.json` for exact schema).
- For a **curl** snippet, mirror the runner's headers:
  ```bash
  curl -H "Authorization: ApiKey $VC_ADMIN_KEY" \
       https://api.validationcloud.io/admin/v1/account
  ```
- For a **language** snippet, prefer the matching client in `templates/`
  (`client.ts`, `client.py`, `client.go`) and show how to call it.
- Only describe endpoints that exist in the spec. If asked about something not
  present (per-endpoint metrics, audit log, key issuance/rotation), say it's
  not exposed by this API and point to the dashboard.

---

## Mode: Scaffold

Drop a ready-to-use, dependency-light client into the user's project.

- **TypeScript** → `templates/client.ts` (uses global `fetch`, Node 18+)
- **Python** → `templates/client.py` (requires `requests`)
- **Go** → `templates/client.go` (stdlib only; package `vcadmin`)

**Flow:**
1. Ask the target language and where the file should go (default: the obvious
   location for that language in their repo).
2. Read the template, copy it in (adjusting package/module name or import path
   to fit their project).
3. Show a short usage example wiring the key from the environment, and note any
   dependency to install (`requests` for Python).
4. Never hardcode the key in the scaffolded code — read it from the environment.

---

## When something's missing

This API covers endpoint management, account/usage reads, chains, and CU costs.
Capabilities **not** in this surface (and where to point the user): admin-key
issuance/rotation, per-endpoint request/latency metrics, and audit logs live in
the **web dashboard**. Don't fabricate endpoints for them.
