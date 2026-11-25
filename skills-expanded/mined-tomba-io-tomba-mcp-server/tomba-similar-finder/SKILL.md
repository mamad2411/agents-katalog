---
name: tomba-similar-finder
description: "Find competitor or lookalike company domains similar to a given domain using Tomba's similar_finder tool."
user-invocable: true
argument-hint: "<domain>"
version: 1.0.0
metadata:
    openclaw:
        emoji: "🧭"
        homepage: https://tomba.io
---

# Tomba Similar Finder

This skill uses the `similar_finder` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- Competitor research, lookalike account lists, or market mapping.

## Inputs

| Parameter | Type   | Required | Notes            |
| --------- | ------ | -------- | ---------------- |
| `domain`  | string | yes      | Reference domain |

## Workflow

1. Call `similar_finder`.
2. Optionally enrich the top matches with `tomba-company-enrichment`, or build a filtered list with `tomba-companies-search` using the `similar` filter.

## Output Expectations

- A list of similar domains with company names, noting that similarity comes from Tomba's data.

## Example Usage

```
/tomba:tomba-similar-finder zapier.com
/tomba:tomba-similar-finder asana.com
```

## Example Tool Call

User: "Who are Asana's competitors?"

```json
{
    "tool": "similar_finder",
    "arguments": {
        "domain": "asana.com"
    }
}
```
