---
name: tomba-combined-enrichment
description: "Get person and company data together from a single email address using Tomba's combined_enrichment tool."
user-invocable: true
argument-hint: "<email>"
version: 1.0.0
metadata:
    openclaw:
        emoji: "🧬"
        homepage: https://tomba.io
---

# Tomba Combined Enrichment

This skill uses the `combined_enrichment` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- Full lead enrichment (person + company) from one email, for CRM or lead scoring.

## Inputs

| Parameter | Type   | Required | Notes         |
| --------- | ------ | -------- | ------------- |
| `email`   | string | yes      | Email address |

## Workflow

1. Call `combined_enrichment` instead of separate person and company lookups.

## Output Expectations

- Two short sections, Person and Company, with only the fields that were returned.

## Example Usage

```
/tomba:tomba-combined-enrichment snadella@microsoft.com
/tomba:tomba-combined-enrichment jane@acme.com
```

## Example Tool Call

User: "Enrich this lead: snadella@microsoft.com"

```json
{
    "tool": "combined_enrichment",
    "arguments": {
        "email": "snadella@microsoft.com"
    }
}
```
