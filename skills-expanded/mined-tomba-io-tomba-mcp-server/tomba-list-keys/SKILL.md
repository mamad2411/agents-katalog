---
name: tomba-list-keys
description: "List the API keys on the user's Tomba account using the list_keys tool."
user-invocable: true
argument-hint: "(no arguments)"
version: 1.0.0
metadata:
    openclaw:
        emoji: "🔑"
        homepage: https://tomba.io
---

# Tomba List API Keys

This skill uses the `list_keys` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- The user wants to see or audit their Tomba API keys.

## Inputs

This tool takes no parameters.

## Workflow

1. Call `list_keys` (no arguments).
2. This tool does not work with OAuth sign-in. If it fails with an OAuth error, tell the user it needs API key authentication (the local server, or the `X-Tomba-Key`/`X-Tomba-Secret` headers).

## Output Expectations

- Key IDs, names, creation dates, and status.
- Never print full secret values; mask all but the last 4 characters.

## Example Usage

```
/tomba:tomba-list-keys
```

## Example Tool Call

User: "List my Tomba API keys"

```json
{
    "tool": "list_keys",
    "arguments": {}
}
```
