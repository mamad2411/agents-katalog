---
name: verify-api-token
description: Verify an API token against an EventSourcingDB instance. Use when the user wants to check if their API token is valid.
allowed-tools: Bash, Read, AskUserQuestion
---

# Verify API Token

Verify that an API token is valid for an EventSourcingDB instance.

## Shared Instructions

First read `${CLAUDE_PLUGIN_ROOT}/shared/common.md`. It explains how to determine the base URL and API token, how to handle NDJSON responses, and which conventions apply. Follow it throughout this skill.

## Request

```bash
curl -s -i -X POST \
  -H "authorization: Bearer ${ESDB_API_TOKEN}" \
  "${ESDB_URL:-http://localhost:3000}/api/v1/verify-api-token"
```

## Response

Returns `200 OK` if the token is valid. Returns `401 Unauthorized` if the token is invalid. Inform the user accordingly.
