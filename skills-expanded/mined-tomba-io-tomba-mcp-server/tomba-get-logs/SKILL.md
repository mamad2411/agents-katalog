---
name: tomba-get-logs
description: "Retrieve the user's Tomba API request logs from the last 3 months using the get_logs tool."
user-invocable: true
argument-hint: "[page N] [limit N]"
version: 1.0.0
metadata:
    openclaw:
        emoji: "📜"
        homepage: https://tomba.io
---

# Tomba API Logs

This skill uses the `get_logs` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- Debugging failed requests, auditing usage, or tracing which calls used credits.

## Inputs

| Parameter | Type   | Required | Notes                                  |
| --------- | ------ | -------- | -------------------------------------- |
| `page`    | number | no       | Page number, default `1`               |
| `limit`   | number | no       | Results per page (1-100), default `10` |

## Workflow

1. Call `get_logs`; page through results if needed.
2. Group the entries by endpoint or status when you summarise.

## Output Expectations

- Recent requests with endpoint, status, and timestamp, calling out errors.

## Example Usage

```
/tomba:tomba-get-logs
/tomba:tomba-get-logs limit 50
/tomba:tomba-get-logs page 2
```

## Example Tool Call

User: "Show my last 20 Tomba API calls"

```json
{
    "tool": "get_logs",
    "arguments": {
        "limit": 20
    }
}
```
