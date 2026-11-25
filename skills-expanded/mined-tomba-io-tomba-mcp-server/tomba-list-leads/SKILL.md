---
name: tomba-list-leads
description: "List the leads saved in the user's Tomba account, optionally filtered by domain, using the list_leads tool."
user-invocable: true
argument-hint: "[domain] [page N] [limit N]"
version: 1.0.0
metadata:
    openclaw:
        emoji: "🗂️"
        homepage: https://tomba.io
---

# Tomba List Leads

This skill uses the `list_leads` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- The user asks what leads they have saved, or whether a company is already in their leads.

## Inputs

| Parameter | Type   | Required | Notes                                  |
| --------- | ------ | -------- | -------------------------------------- |
| `page`    | number | no       | Page number, default `1`               |
| `limit`   | number | no       | Results per page (1-100), default `10` |
| `domain`  | string | no       | Only return leads for this domain      |

## Workflow

1. Call `list_leads`; add `domain` when the user asks about one company.
2. Page through results only when needed.

## Output Expectations

- A table of name, email, company, position, and list, with the total count.

## Example Usage

```
/tomba:tomba-list-leads
/tomba:tomba-list-leads zapier.com
/tomba:tomba-list-leads page 2 limit 50
```

## Example Tool Call

User: "Do I already have leads at acme.com?"

```json
{
    "tool": "list_leads",
    "arguments": {
        "domain": "acme.com",
        "limit": 20
    }
}
```
