---
name: tomba-usage-info
description: "Show the user's Tomba API usage statistics across all endpoints using the usage_info tool."
user-invocable: true
argument-hint: "(no arguments)"
version: 1.0.0
metadata:
    openclaw:
        emoji: "📊"
        homepage: https://tomba.io
---

# Tomba Usage Info

This skill uses the `usage_info` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- The user wants to see how much they have used each endpoint (searches, verifications, and so on).

Do not use it when:

- The user asks about remaining credits or their plan: use `tomba-account-info`.

## Inputs

This tool takes no parameters.

## Workflow

1. Call `usage_info` (no arguments).

## Output Expectations

- Usage for each endpoint, highlighting the heaviest consumers.

## Example Usage

```
/tomba:tomba-usage-info
```

## Example Tool Call

User: "Which Tomba endpoints am I using most?"

```json
{
    "tool": "usage_info",
    "arguments": {}
}
```
