---
name: tomba-company-enrichment
description: "Get firmographic data for a company domain (industry, size, revenue, location, social profiles) using Tomba's company_enrichment tool."
user-invocable: true
argument-hint: "<domain>"
version: 1.0.0
metadata:
    openclaw:
        emoji: "🏛️"
        homepage: https://tomba.io
---

# Tomba Company Enrichment

This skill uses the `company_enrichment` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- Researching a company before outreach, qualifying an account, or filling CRM company fields.

Do not use it when:

- You only have the company's name: resolve the domain with `tomba-autocomplete` first.

## Inputs

| Parameter | Type   | Required | Notes          |
| --------- | ------ | -------- | -------------- |
| `domain`  | string | yes      | Company domain |

## Workflow

1. Call `company_enrichment`.
2. Add `tomba-technology-finder`, `tomba-location`, or `tomba-similar-finder` only if the user asks for that extra context.

## Output Expectations

- A concise company profile: description, industry, size, revenue, HQ, founding year, and social links.

## Example Usage

```
/tomba:tomba-company-enrichment zapier.com
/tomba:tomba-company-enrichment figma.com
```

## Example Tool Call

User: "Tell me about figma.com"

```json
{
    "tool": "company_enrichment",
    "arguments": {
        "domain": "figma.com"
    }
}
```
