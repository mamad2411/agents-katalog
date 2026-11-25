---
name: tomba-technology-finder
description: "Reveal the technology stack (CMS, analytics, frameworks, marketing tools) a website uses with Tomba's technology_finder tool."
user-invocable: true
argument-hint: "<domain>"
version: 1.0.0
metadata:
    openclaw:
        emoji: "🛠️"
        homepage: https://tomba.io
---

# Tomba Technology Finder

This skill uses the `technology_finder` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- Technographic prospecting, competitive analysis, or checking whether a company uses a given tool.

## Inputs

| Parameter | Type   | Required | Notes                     |
| --------- | ------ | -------- | ------------------------- |
| `domain`  | string | yes      | Website domain to analyse |

## Workflow

1. Call `technology_finder`.
2. Group the technologies by category.

## Output Expectations

- Technologies grouped by category; answer directly any "do they use X?" question.

## Example Usage

```
/tomba:tomba-technology-finder zapier.com
/tomba:tomba-technology-finder airbnb.com
/tomba:tomba-technology-finder does shopify.com use React?
```

## Example Tool Call

User: "What tech stack does airbnb.com run?"

```json
{
    "tool": "technology_finder",
    "arguments": {
        "domain": "airbnb.com"
    }
}
```
