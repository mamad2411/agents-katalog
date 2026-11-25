# SKILL: plugins
# Endpoint: GET /api/plugins
# Description: List available plugins and their skill documentation

## Overview

Use `/api/plugins` to see which plugins are installed on this server.
Each plugin has a skill document at `/private/skills/:name/SKILL.md` with detailed usage instructions.
Requires API_KEY.

## Request

```bash
curl -X GET http://<host>/api/plugins \
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
  "plugins": [
    { "name": "<plugin name>", "skill": "/private/skills/<name>/SKILL.json" }
  ]
}
```

Plugin list values:

```json
[
  { "name": "<plugin name>", "skill": "/private/skills/<name>/SKILL.json" }
]
```
<!-- ae:prev response.plugins -> all -->

The `skill` URL follows the response format. JSON responses point to
`SKILL.json`; Markdown responses point to `SKILL.md`; HTML responses point to
`SKILL.html`.

## Next step

For each plugin, read its skill document to understand what commands are available and how to use them:

```bash
curl -X GET http://<host>/private/skills/<name>/SKILL.json \
  -H "X-API-Key: <API_KEY>"
```

Plugin skill documents may also reference additional files under `/private/skills/:name/references/` for deeper documentation.

Related authenticated skill index:

```json
["/private/skills"]
```
<!-- ae:prev refs -> all -->
