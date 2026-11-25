---
name: tomba-email-format
description: "Find the email address patterns (e.g. {first}.{last}) a company uses, using Tomba's email_format tool."
user-invocable: true
argument-hint: "<domain>"
version: 1.0.0
metadata:
    openclaw:
        emoji: "🔤"
        homepage: https://tomba.io
---

# Tomba Email Format

This skill uses the `email_format` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- The user asks how a company's emails are structured.
- Building a best-guess address when `tomba-email-finder` returns nothing.

## Inputs

| Parameter | Type   | Required | Notes                              |
| --------- | ------ | -------- | ---------------------------------- |
| `domain`  | string | yes      | Domain to get the email format for |

## Workflow

1. Call `email_format`.
2. Apply the most common pattern to the person's name.
3. Validate the guess with `tomba-email-verifier` before you present it.

## Output Expectations

- The patterns ranked by share or percentage.
- Label any constructed address as a guess until it has been verified.

## Example Usage

```
/tomba:tomba-email-format zapier.com
/tomba:tomba-email-format shopify.com
/tomba:tomba-email-format build Jane Doe's email at acme.com
```

## Example Tool Call

User: "What email format does shopify.com use?"

```json
{
    "tool": "email_format",
    "arguments": {
        "domain": "shopify.com"
    }
}
```
