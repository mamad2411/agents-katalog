---
name: mcp-scribe
description: Turn an OpenAPI/Swagger schema into a working MCP server. Use when someone wants to give a model tools from a REST API, connect an API to Claude Code/Desktop or Cursor, stand up a shared MCP endpoint for a team, or inspect/call/debug the tools a spec produces. Triggers on "OpenAPI to MCP", "make an MCP server for <API>", "add <API> as tools", "wrap this API for an agent", "mcp-scribe".
---

# mcp-scribe

Point it at an OpenAPI schema, get an MCP server. Every operation becomes a tool, with
JSON Schema, credentials, retries, rate limiting, and response shaping handled.

## Decide first: which command

This is the one decision that matters. Get it right and everything else follows.

| Situation | Command | Transport |
| --- | --- | --- |
| One person, one machine, using Claude Code / Desktop / Cursor | `install` | stdio |
| A shared endpoint for a team, agents, or CI | `deploy` | HTTP |
| Just looking — what tools does this spec make? | `inspect` | none |
| Testing one operation end to end | `call` | none |
| Handing someone a deployable artifact | `generate` | — |

**Do not reach for `deploy` for a personal setup.** It binds a port and a network
interface nobody asked for. `install` is the right answer for one user on one machine.

## Always inspect first

Before installing or deploying anything, look at what the spec produces. It costs one
command and catches the two most common problems — too many tools, and a credential
parameter still visible to the model.

```bash
mcp-scribe inspect --spec https://api.example.com/openapi.json
```

Then narrow, and look again:

```bash
mcp-scribe inspect --spec $SPEC --include-tag Agents --read-only
mcp-scribe inspect --spec $SPEC --tool run_agent          # one tool's full schema
```

**Two hundred tools is worse than twenty.** If the spec produces more than ~30 tools,
filter before going further. Model tool-selection accuracy degrades badly with surface
area.

## Install for one person

```bash
mcp-scribe install --spec https://api.swarms.world/openapi.json \
    --api-key sk-... --api-key-name x-api-key
```

Better, keeping the secret out of the client config (which is often synced):

```bash
mcp-scribe install --spec $SPEC \
    --env-file .env --api-key-env SWARMS_API_KEY --api-key-name x-api-key
```

- `--client` — `auto` (default), `claude-code`, `claude-desktop`, `cursor`, `project`, `all`, `print`
- `--dry-run` — show the JSON, write nothing. **Use this first when unsure.**
- `--scope` — Claude Code only: `local`, `user` (default), `project`

The server is built before any config is written, so a broken setup is never registered.
Existing configs are merged and backed up. Tell the user to restart their MCP client
afterward — it will not pick up the new server otherwise.

## Deploy a shared server

```bash
mcp-scribe deploy https://api.swarms.world/openapi.json --port 8000
```

`deploy` = HTTP transport + stateless + `/health` + `0.0.0.0` bind + automatic caller
credential passthrough when no server key is configured.

Then connect a client:

```bash
claude mcp add --transport http swarms http://localhost:8000/mcp \
    --header "x-api-key: <key>"
```

### Two things to say out loud when you run `deploy`

1. **uvicorn starting is expected.** HTTP transport *is* uvicorn + Starlette. It is not a
   stray process. If the user does not want it, they want `serve` (stdio).
2. **It binds `0.0.0.0`, not localhost.** The banner prints `localhost` for clickability,
   but the server is reachable on every interface. Add `--host 127.0.0.1` for local-only.

### Credentials on a shared server

A shared server holding one key means every caller shares one identity and one bill.
Passthrough forwards each caller's own credential instead:

```bash
mcp-scribe deploy $SPEC --port 8000          # passthrough on automatically (no server key)
```

Server-held key instead, passthrough off:

```bash
mcp-scribe deploy $SPEC --port 8000 \
    --env-file .env --api-key-env SWARMS_API_KEY --api-key-name x-api-key
```

Passthrough is an **allowlist** (`--passthrough-header`, default `x-api-key`), and
`authorization` is deliberately not in it. `required` fails closed — without it, a call
with no caller credential falls back to the server key, which is the leak you were
avoiding.

## Debug a tool without a client

```bash
mcp-scribe call run_agent --spec $SPEC --args '{"task": "hello"}'
mcp-scribe call run_agent --spec $SPEC --args '{...}' --dry-run
```

Same code path as the server — auth, retries, response shaping. `--dry-run` prints the
request without sending it, which is the fastest way to confirm a credential lands in the
right header.

## Trim the surface

Filters compose and work on every command.

```bash
mcp-scribe deploy $SPEC \
    --include-tag Agents --include-tag Swarms \
    --exclude-path '^/internal' \
    --read-only
```

- `--include-tag` / `--exclude-tag` — exact OpenAPI tag names
- `--include-path` / `--exclude-path` — **regexes** against the path
- `--read-only` — GET/HEAD/OPTIONS only. The cheapest way to make a server safe to hand
  to an agent you don't fully trust.

Includes apply before excludes. An empty include list means everything.

## Credentials: pick the least leaky option that works

| Rank | Method | Use when |
| --- | --- | --- |
| 1 | `--env-file` + `--api-key-env` | Local / personal. Keeps the secret out of client config. |
| 2 | `MCP_SCRIBE_API_KEY` env var | Containers, CI. |
| 3 | Config file with `${VAR}` | Anything checked into a repo. |
| 4 | `--api-key` flag | Quick test only — visible in `ps` and shell history. |

Schemes: `--api-key` (+`--api-key-name`, `--api-key-in`), `--bearer-token`,
`--header 'Name: value'`. Basic and OAuth2 client credentials are config/env only.

**Never put a real key in a command you show the user as an example.** Use `sk-...`.

## Ship a standalone artifact

```bash
mcp-scribe generate --spec $SPEC -o ./my-server --freeze
```

Emits `server.py`, `config.yaml`, `Dockerfile`, `requirements.txt`, `mcp.json`,
`.env.example`, `README.md`. `--freeze` vendors the spec so startup needs no network —
worth it for anything deployed.

## Configuration

Precedence: **defaults < config file < environment < flags.**

```bash
mcp-scribe deploy --config swarms.yaml --port 8000
```

```yaml
spec:
  url: https://api.swarms.world/openapi.json
  cache_ttl: 3600
auth:
  - type: api_key
    name: x-api-key
    api_key: ${SWARMS_API_KEY}
filters:
  include_tags: [Agents]
  read_only: true
retry:
  retry_non_idempotent: false
rate_limit:
  requests_per_second: 5
```

The config section is `schema:` (not `json_schema:`). Unknown keys are a **startup
error**, so a typo fails loudly rather than doing nothing.

Env vars use the `MCP_SCRIBE_` prefix — `MCP_SCRIBE_SPEC`, `MCP_SCRIBE_API_KEY`,
`MCP_SCRIBE_PORT`, `MCP_SCRIBE_READ_ONLY`, and so on.

## Defaults worth knowing before you change them

| Behaviour | Default | Why |
| --- | --- | --- |
| POST/PATCH retried | **no** | Re-sending a billable request is worse than failing |
| Response truncation | 100 KB | Context windows are a resource |
| `outputSchema` declared | off | Clients must reject non-validating responses; real APIs drift |
| Credential params hidden | on | The model is never asked for a secret it doesn't have |
| Simple bodies flattened | on | `{"task": ...}` beats `{"body": {"task": ...}}` for accuracy |
| `additionalProperties: false` | on | Models can't invent arguments |

## Troubleshooting

| Symptom | Cause / fix |
| --- | --- |
| A uvicorn server started unexpectedly | HTTP transport. Use `serve` (stdio) if no port wanted. |
| Reachable from outside the machine | `deploy` binds `0.0.0.0`. Use `--host 127.0.0.1`. |
| `HTTP transport needs the 'http' extra` | `pip install 'mcp-scribe[http]'` |
| Model asked to supply an API key | Credential not configured. Set `--api-key-name` to the exact header the spec declares, confirm with `inspect --tool`. |
| Calls rejected for missing credential | `passthrough.required` is on. Send the header, or configure a server key. |
| `$ref` not resolving in a client | `--inline-refs` |
| Config change does nothing | Precedence — a flag or env var is overriding the file. |
| Response cut off | `response.max_bytes`. Raise it or narrow the request. |
| Model picks the wrong tool | Too many tools. Filter, then `inspect`. |

## Reference

- Guide: `docs/DOCS.md`
- Every flag, config key, env var, Python API: `docs/REFERENCE.md`
