---
name: tomba-person-enrichment
description: "Get person data (name, position, company, social profiles) from an email address using Tomba's person_enrichment tool."
user-invocable: true
argument-hint: "<email>"
version: 1.0.0
metadata:
    openclaw:
        emoji: "👤"
        homepage: https://tomba.io
---

# Tomba Person Enrichment

This skill uses the `person_enrichment` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- The user wants a person profile only (no company data) for an email.

Do not use it when:

- The user also wants company data: use `tomba-combined-enrichment`.

## Inputs

| Parameter | Type   | Required | Notes         |
| --------- | ------ | -------- | ------------- |
| `email`   | string | yes      | Email address |

## Workflow

1. Call `person_enrichment`.

## Output Expectations

- Name, position, seniority, location, and social links; mark missing fields as unknown.

## Example Usage

```
/tomba:tomba-person-enrichment snadella@microsoft.com
/tomba:tomba-person-enrichment jane@acme.com
```

## Example Tool Call

User: "Look up the person behind snadella@microsoft.com"

```json
{
    "tool": "person_enrichment",
    "arguments": {
        "email": "snadella@microsoft.com"
    }
}
```
