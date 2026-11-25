---
name: tomba-list-flags
description: "List the incorrect-data reports (flags) the user has submitted to Tomba using the list_flags tool."
user-invocable: true
argument-hint: "[page N] [limit N]"
version: 1.0.0
metadata:
    openclaw:
        emoji: "🚩"
        homepage: https://tomba.io
---

# Tomba List Flags

This skill uses the `list_flags` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- The user wants to review their data-quality reports or credit-recovery requests.

## Inputs

| Parameter | Type   | Required | Notes                                  |
| --------- | ------ | -------- | -------------------------------------- |
| `page`    | number | no       | Page number, default `1`               |
| `limit`   | number | no       | Results per page (1-100), default `10` |

## Workflow

1. Call `list_flags`.

## Output Expectations

- A table of type, value, reason, status, and date.

## Example Usage

```
/tomba:tomba-list-flags
/tomba:tomba-list-flags page 2 limit 50
```

## Example Tool Call

User: "Show the bad emails I've reported"

```json
{
    "tool": "list_flags",
    "arguments": {
        "limit": 20
    }
}
```
