---
name: tomba-email-enrichment
description: "Turn an email address into a contact profile (name, position, company, social links) using Tomba's email_enrichment tool."
user-invocable: true
argument-hint: "<email>"
version: 1.0.0
metadata:
    openclaw:
        emoji: "🧩"
        homepage: https://tomba.io
---

# Tomba Email Enrichment

This skill uses the `email_enrichment` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- The user already has an email and wants to know who is behind it.
- Filling in missing lead fields before outreach or a CRM import.

Do not use it when:

- The user wants company firmographics too: `tomba-combined-enrichment` returns both in one call.

## Inputs

| Parameter      | Type    | Required | Notes                                            |
| -------------- | ------- | -------- | ------------------------------------------------ |
| `email`        | string  | yes      | Email address to enrich                          |
| `enrichMobile` | boolean | no       | Local server only: also return mobile phone data |

## Workflow

1. Call `email_enrichment`.
2. If the user also wants phone numbers, follow up with `tomba-phone-finder` (or set `enrichMobile` on the local server).

## Output Expectations

- Name, position, company, location, and social profiles that were found.
- Mark any field that was not returned as unknown; do not guess it.

## Example Usage

```
/tomba:tomba-email-enrichment snadella@microsoft.com
/tomba:tomba-email-enrichment jane@acme.com
```

## Example Tool Call

User: "Who is behind snadella@microsoft.com?"

```json
{
    "tool": "email_enrichment",
    "arguments": {
        "email": "snadella@microsoft.com"
    }
}
```
