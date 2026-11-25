---
name: tomba-email-count
description: "Get how many email addresses Tomba knows for a domain, broken down by department and seniority, using the email_count tool."
user-invocable: true
argument-hint: "<domain>"
version: 1.0.0
metadata:
    openclaw:
        emoji: "🔢"
        homepage: https://tomba.io
---

# Tomba Email Count

This skill uses the `email_count` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- Estimating the size of a company's reachable contacts before prospecting.
- Comparing contact coverage across several domains.

Do not use it when:

- The user wants the actual addresses: use `tomba-domain-search`.

## Inputs

| Parameter | Type   | Required | Notes                      |
| --------- | ------ | -------- | -------------------------- |
| `domain`  | string | yes      | Domain to count emails for |

## Workflow

1. Call `email_count` (it is cheap and a good first step).
2. If the count is useful, continue with `tomba-domain-search` filtered by the largest relevant department.

## Output Expectations

- Total count, the split between personal and generic addresses, and the department and seniority breakdown when returned.

## Example Usage

```
/tomba:tomba-email-count zapier.com
/tomba:tomba-email-count hubspot.com
/tomba:tomba-email-count compare stripe.com and adyen.com
```

## Example Tool Call

User: "How many contacts does Tomba have at hubspot.com?"

```json
{
    "tool": "email_count",
    "arguments": {
        "domain": "hubspot.com"
    }
}
```
