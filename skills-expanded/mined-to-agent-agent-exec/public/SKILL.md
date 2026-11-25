# SKILL: agent-exec
# Endpoint: GET /
# Description: Self-describing HTTP execution surface for AI agents

## What is this?

agent-exec lets an AI agent discover this machine, inspect what is allowed,
and execute only permitted commands through HTTP.

This is the root guide for this running agent-exec server.

### Root surface

The root surface points agents to the API documents used for discovery.

```json
{
  "method": "GET",
  "url": "/",
  "document": "/SKILL.s.js",
  "refs": [
    "/api/acl/SKILL.s.js",
    "/api/exec/SKILL.s.js"
  ]
}
```
<!-- ae:prev m["/"] -> all -->

## Start

### 1. Inspect allowed operations

Protected API calls require API_KEY.

Use `/api/acl` to inspect allowed and denied commands.

```bash
curl -s http://<host>/api/acl \
  -H "X-API-Key: <API_KEY>"
```

ACL request:

```json
{
  "method": "GET",
  "url": "/api/acl",
  "document": "/api/acl/SKILL.s.js",
  "request": {
    "headers": {
      "X-API-Key": "API_KEY",
      "Accept": "text/sjs"
    }
  },
  "refs": [
    "/api/exec/SKILL.s.js"
  ]
}
```
<!-- ae:prev m["/api/acl"] -> all -->

Allowed command values:

```json
["<command> [<arg>]...", "..."]
```
<!-- ae:prev m["/api/acl"].response.allow -> all -->

Allowed command item kind:

```json
"argv_string"
```
<!-- ae:prev m["/api/acl"].response.allow.kind -> all -->

Allowed command item syntax:

```json
"<command> [<arg>]..."
```
<!-- ae:prev m["/api/acl"].response.allow.syntax -> all -->

Allowed command item to exec args:

```json
["<command>", "<arg>", "..."]
```
<!-- ae:prev m["/api/acl"].response.allow.to_args -> all -->

Denied pattern values:

```json
["<denied pattern>", "..."]
```
<!-- ae:prev m["/api/acl"].response.deny -> all -->

### 2. Discover plugins

```bash
curl -s http://<host>/api/plugins \
  -H "X-API-Key: <API_KEY>"
```

The `skill` URL in the response is the next document to read.

### 3. Execute an allowed command

```bash
curl -X POST http://<host>/api/exec \
  -H "X-API-Key: <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"args": ["aexec", "--version"]}'
```

Execution request body:

```json
{"args": ["<command>", "<arg>", "..."]}
```
<!-- ae:prev m["/api/exec"].request.body -> all -->

Example command args:

```json
["aexec", "--version"]
```
<!-- ae:prev m["/api/exec"].request.body.args.example -> all -->

Execution surface:

```json
{
  "method": "POST",
  "url": "/api/exec",
  "document": "/api/exec/SKILL.s.js",
  "operation": "POST /api/exec AUTH {\"args\":[\"aexec\",\"--version\"]}",
  "request": {
    "headers": {
      "X-API-Key": "API_KEY",
      "Content-Type": "application/json",
      "Accept": "text/sjs"
    },
    "body": {
      "args": ["<command>", "<arg>", "..."]
    }
  },
  "refs": [
    "/api/acl/SKILL.s.js"
  ]
}
```
<!-- ae:prev m["/api/exec"] -> all -->

Command argument kind:

```json
"argv"
```
<!-- ae:prev m["/api/exec"].request.body.args.kind -> all -->

Command argument syntax:

```json
"<command> [<arg>]..."
```
<!-- ae:prev m["/api/exec"].request.body.args.syntax -> all -->

Execution response output:

```json
"<stdout>"
```
<!-- ae:prev m["/api/exec"].response.output -> all -->

Execution response length:

```json
0
```
<!-- ae:prev m["/api/exec"].response.length -> all -->

Execution response exit code:

```json
0
```
<!-- ae:prev m["/api/exec"].response.exitCode -> all -->

Execution response status:

```json
"done"
```
<!-- ae:prev m["/api/exec"].response.status -> all -->

Execution response duration:

```json
0
```
<!-- ae:prev m["/api/exec"].response.duration -> all -->

Execution response stderr:

```json
"<stderr>"
```
<!-- ae:prev m["/api/exec"].response.stderr -> all -->

## Authentication

Most `/api/*` endpoints and all `/private/*` endpoints require API_KEY.

Use:

- `X-API-Key: <API_KEY>`

## Navigation Links (Optional)

Append `?navigation=true` to include next-step links in responses.

Examples:

```bash
curl -s "http://<host>/SKILL.md?navigation=true"
curl -s "http://<host>/skills?navigation=true"
curl -s "http://<host>/api/acl?navigation=true" -H "X-API-Key: <API_KEY>"
```

Notes:

- This is a response feature provided by agent-exec. It is not part of the original skill definition content.
- In Markdown/HTML responses, navigation is appended as a section/footer.
- In JSON responses, navigation is returned as a `navigation` field.

## Memo Echo (Optional)

Clients may attach short opaque memo text to carry local context between
requests. agent-exec does not interpret or store it; responses echo it back.

Use one of:

- `?memo=<text>`
- `X-Agent-Memo: <text>`
- JSON body field `memo` where the endpoint accepts JSON

In SJS responses, the echoed value appears as `m.memo`.

Do not put secrets in memo.

## Boundary

The agent discovers. The server enforces.

Read `/api/acl` before executing commands. Do not assume permissions.
