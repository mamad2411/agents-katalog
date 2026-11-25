# SKILL: acl
# Endpoint: GET /api/acl
# Description: Get the access control list for exec

## Overview

Use `/api/acl` to see which commands are allowed or denied on this server.
Requires API_KEY.

## Request

```bash
curl -X GET http://<host>/api/acl \
  -H "X-API-Key: <API_KEY>"
```

Request headers:

```json
{
  "X-API-Key": "API_KEY",
  "Accept": "text/sjs"
}
```
<!-- ae:prev request.headers -> all -->

## Response

```json
{
  "allow": ["aexec --version", "date", "echo agent exec ok"],
  "deny": ["/^sudo/", "/rm\\s+-rf/", "/--yolo/"]
}
```

Allowed command values:

```json
["<command> [<arg>]...", "..."]
```
<!-- ae:prev response.allow -> all -->

Allowed command item kind:

```json
"argv_string"
```
<!-- ae:prev response.allow.kind -> all -->

Allowed command item syntax:

```json
"<command> [<arg>]..."
```
<!-- ae:prev response.allow.syntax -> all -->

Allowed command item to exec args:

```json
["<command>", "<arg>", "..."]
```
<!-- ae:prev response.allow.to_args -> all -->

Denied pattern values:

```json
["<denied pattern>", "..."]
```
<!-- ae:prev response.deny -> all -->

## Pattern types

| Pattern | Example | Match |
|---|---|---|
| String | `"aexec --version"` | Exact match for this command and argument |
| Glob | `"hermes *"` | Explicit wildcard match; allows any arguments to `hermes` |
| Regexp | `"/^sudo/"` | Regex match against full args string |

`deny` is evaluated before `allow`. If a command matches both, it is denied.
A rule like `cmd *` allows any arguments to `cmd`; treat broad glob rules as host policy, not agent permission to assume safety.

## Next step

Once you know which commands are allowed, use `POST /api/exec` to execute them.
See `/skills/exec/SKILL.md` for details.

Related skill documents:

```json
["/skills/exec/SKILL.s.js"]
```
<!-- ae:prev refs -> all -->
