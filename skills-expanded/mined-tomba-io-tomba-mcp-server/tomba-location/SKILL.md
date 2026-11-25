---
name: tomba-location
description: "Get a company's employee distribution by country for a domain using Tomba's location tool."
user-invocable: true
argument-hint: "<domain>"
version: 1.0.0
metadata:
    openclaw:
        emoji: "🌍"
        homepage: https://tomba.io
---

# Tomba Employee Locations

This skill uses the `location` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- Learning where a company's workforce is based, for territory planning or localisation.

## Inputs

| Parameter | Type   | Required | Notes          |
| --------- | ------ | -------- | -------------- |
| `domain`  | string | yes      | Company domain |

## Workflow

1. Call `location`.
2. Sort the countries by employee count.

## Output Expectations

- Countries with employee counts and percentages, highlighting the top three.

## Example Usage

```
/tomba:tomba-location zapier.com
/tomba:tomba-location gitlab.com
```

## Example Tool Call

User: "Where are GitLab's employees located?"

```json
{
    "tool": "location",
    "arguments": {
        "domain": "gitlab.com"
    }
}
```
