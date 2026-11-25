---
name: jumpserver-cli-api
description: Use when calling JumpServer OpenAPI operations through jumpserver-cli, discovering operation names, building request parameters, or using dry-run output.
---

# JumpServer CLI API Calls

The CLI exposes JumpServer OpenAPI operations as gh/glab-style module commands and also supports direct operationId calls.

## Discover

```bash
jms api list --search profile
jms api describe users_profile_read
```

## Call Operations

Prefer module commands when they exist:

```bash
jms users profile read
jms assets favorite-assets read --path id=asset-1
jms users profile password update --body '{"old_password":"old","new_password":"new","new_password_again":"new"}'
```

Use `api call` when an operationId is easier:

```bash
jms api call assets_favorite-assets_read --path id=asset-1
```

## Request Options

- `--path name=value`: path template parameter.
- `--query name=value`: query string parameter.
- `--param name=value`: path parameter if declared, otherwise query parameter.
- `--limit 20` and `--offset 40`: pagination controls.
- `--body '{"name":"value"}'`, `--body @payload.json`, or `--body -`.
- `--dry-run`: inspect the request without sending it.
- `--json`: print raw JSON instead of the compact table.

## Output

Default table output is for quick inspection. Use `--json` when another tool or agent needs complete response data.
