---
name: tomba-autocomplete
description: "Resolve a partial company name to its official domain and logo using Tomba's autocomplete tool."
user-invocable: true
argument-hint: "<company name>"
version: 1.0.0
metadata:
    openclaw:
        emoji: "⌨️"
        homepage: https://tomba.io
---

# Tomba Company Autocomplete

This skill uses the `autocomplete` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- The user gives a company name but other tools need a domain.
- Disambiguating companies with similar names.

## Inputs

| Parameter | Type   | Required | Notes                          |
| --------- | ------ | -------- | ------------------------------ |
| `query`   | string | yes      | Partial company name or domain |

## Workflow

1. Call `autocomplete`.
2. If there are several matches, ask the user which one they mean (or pick the obvious one), then pass its domain to the next tool.

## Output Expectations

- Matching company names with their domains and logos.

## Example Usage

```
/tomba:tomba-autocomplete zapier
/tomba:tomba-autocomplete datadog
/tomba:tomba-autocomplete open ai
```

## Example Tool Call

User: "What's the domain for 'Datadog'?"

```json
{
    "tool": "autocomplete",
    "arguments": {
        "query": "datadog"
    }
}
```
