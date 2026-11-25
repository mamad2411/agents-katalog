---
name: tomba-domain-status
description: "Check whether a domain is a webmail provider or a disposable email service using Tomba's domain_status tool."
user-invocable: true
argument-hint: "<domain>"
version: 1.0.0
metadata:
    openclaw:
        emoji: "🛡️"
        homepage: https://tomba.io
---

# Tomba Domain Status

This skill uses the `domain_status` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- Screening sign-ups or leads for free webmail and throwaway domains.
- Deciding whether a domain belongs to a real company.

## Inputs

| Parameter | Type   | Required | Notes                                                 |
| --------- | ------ | -------- | ----------------------------------------------------- |
| `domain`  | string | yes      | Domain to check, e.g. `gmail.com` or `mailinator.com` |

## Workflow

1. Call `domain_status`.

## Output Expectations

- Whether the domain is webmail or disposable, and what that means for lead quality.

## Example Usage

```
/tomba:tomba-domain-status gmail.com
/tomba:tomba-domain-status mailinator.com
/tomba:tomba-domain-status zapier.com
```

## Example Tool Call

User: "Is guerrillamail.com disposable?"

```json
{
    "tool": "domain_status",
    "arguments": {
        "domain": "guerrillamail.com"
    }
}
```
