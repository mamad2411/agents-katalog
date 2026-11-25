---
name: tomba-email-sources
description: "Show the public web pages where an email address was found, using Tomba's email_sources tool."
user-invocable: true
argument-hint: "<email>"
version: 1.0.0
metadata:
    openclaw:
        emoji: "🔗"
        homepage: https://tomba.io
---

# Tomba Email Sources

This skill uses the `email_sources` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- The user wants proof of where an email came from or how fresh it is.
- Compliance or due-diligence checks on a contact's provenance.

## Inputs

| Parameter | Type   | Required | Notes                             |
| --------- | ------ | -------- | --------------------------------- |
| `email`   | string | yes      | Email address to find sources for |

## Workflow

1. Call `email_sources`.
2. Sort the sources by most recent extraction date.

## Output Expectations

- A list of source URLs with their extraction and last-seen dates, and whether each page is still online.

## Example Usage

```
/tomba:tomba-email-sources snadella@microsoft.com
/tomba:tomba-email-sources jane@acme.com
```

## Example Tool Call

User: "Where was snadella@microsoft.com found?"

```json
{
    "tool": "email_sources",
    "arguments": {
        "email": "snadella@microsoft.com"
    }
}
```
