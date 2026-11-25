---
name: tomba-account-info
description: "Show the user's Tomba account details: plan, remaining credits, and usage limits, using the account_info tool."
user-invocable: true
argument-hint: "(no arguments)"
version: 1.0.0
metadata:
    openclaw:
        emoji: "🪪"
        homepage: https://tomba.io
---

# Tomba Account Info

This skill uses the `account_info` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- The user asks about their plan, credits, or quota, or before a large batch of lookups.

## Inputs

This tool takes no parameters.

## Workflow

1. Call `account_info` (no arguments).

## Output Expectations

- Plan name, credits remaining for each request type, and the reset date.
- The response includes the account's secret key (`secret_token`, starting with `ts_`) and session tokens. Never show, quote, or store them.

## Example Usage

```
/tomba:tomba-account-info
```

## Example Tool Call

User: "How many credits do I have left?"

```json
{
    "tool": "account_info",
    "arguments": {}
}
```
