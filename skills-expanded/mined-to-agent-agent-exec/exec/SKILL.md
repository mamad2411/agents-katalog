# SKILL: exec
# Endpoint: POST /api/exec
# Description: Execute an allowed command via HTTP

## Overview

Run an allowed command by passing arguments as an array.
Check `/api/acl` first. Do not assume permissions.

## Authentication

Required: `X-API-Key: <API_KEY>`.

## Request

### POST /api/exec

Content-Type: application/json

Request body:

```json
{
  "args": ["<command>", "<arg>", "..."]
}
```
<!-- ae:prev request.body -> all -->

- `args` — array of command arguments.
- `memo` — optional opaque memo text echoed back by agent-exec; not interpreted or stored.
- Commands must be sent in the JSON body. Query-string command execution is not supported.
- Body fields other than the listed fields are rejected. `cmd`, `command`, `env`, `cwd`, and `shell` return HTTP 400.

### Query Parameters

| Parameter | Values | Default | Description |
|---|---|---|---|
| `format` | `json` / `text` | `json` | Response format |
| `mode` | `buffered` / `stream` | `buffered` | Delivery mode. `stream` is direct-command only and is rejected for plugin commands. |

## Examples

### Buffered JSON (default)

```bash
curl -X POST /api/exec \
  -H "X-API-Key: <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"args": ["aexec", "--version"]}'
```

Response:
```json
{
  "output": "agent-exec v0.2.0\n",
  "length": 18,
  "exitCode": 0,
  "status": "done",
  "duration": 3
}
```

### Buffered text

```bash
curl -X POST "/api/exec?format=text" \
  -H "X-API-Key: <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"args": ["aexec", "--version"]}'
```

### Streaming (NDJSON)

Use streaming only for direct commands. If the command is handled by a plugin, use buffered mode or a plugin-specific `/api/command/:name/*` route.

```bash
curl -X POST "/api/exec?mode=stream" \
  -H "X-API-Key: <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"args": ["aexec", "--version"]}'
```

NDJSON — one object per line:
```
{"output":"line1\n","length":6,"status":"running"}
{"output":null,"exitCode":0,"status":"done","duration":42}
```

## Next step

Use `GET /api/acl` to inspect allowed commands before calling this endpoint.

## Execution Semantics

agent-exec executes `args` as argv. It does not run commands through a shell.
It does not run commands through a shell, and it does not interpret shell metacharacters such as `&&`, `;`, or `|`.

ACL rules are evaluated server-side against the submitted command and arguments.
`exec.deny` is evaluated before `exec.allow`.
Plain string patterns are exact matches only. Glob patterns may use `*`, and regexp patterns use `/.../` when the host intentionally wants broader matching.
A rule like `cmd *` allows any arguments to `cmd`; treat broad glob rules as host policy, not agent permission to assume safety.
