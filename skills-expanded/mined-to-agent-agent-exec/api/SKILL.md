# SKILL: api
# Endpoint: GET /api
# Description: agent-exec API — command execution and discovery endpoints

## Overview

The `/api` namespace provides the agent-facing execution and discovery surface.

## Endpoints

| Path | Method | Description |
|---|---|---|
| `/api/exec` | POST | Execute a command |
| `/api/acl` | GET | Get allowed/denied command list |
| `/api/plugins` | GET | List installed plugins |

Read each endpoint's SKILL.md for full documentation:
- [/api/exec/SKILL.md](/api/exec/SKILL.md)
- [/api/acl/SKILL.md](/api/acl/SKILL.md)
- [/api/plugins/SKILL.md](/api/plugins/SKILL.md)

## Authentication

Most `/api/*` endpoints require API_KEY.
`GET /api` and `GET /api/*/SKILL.*` are public documentation endpoints.

For protected API calls, send API_KEY:
- `X-API-Key: <API_KEY>`
