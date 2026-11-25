---
name: tomba-phone-finder
description: "Find phone numbers linked to an email address, a company domain, or a LinkedIn profile using Tomba's phone_finder tool."
user-invocable: true
argument-hint: "<email | domain | LinkedIn URL> [full]"
version: 1.0.0
metadata:
    openclaw:
        emoji: "📱"
        homepage: https://tomba.io
---

# Tomba Phone Finder

This skill uses the `phone_finder` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- The user wants a phone number for a person or company.

Do not use it when:

- The user already has a number and wants it checked: use `tomba-phone-validator`.

## Inputs

| Parameter     | Type         | Required                     | Notes                                                                  |
| ------------- | ------------ | ---------------------------- | ---------------------------------------------------------------------- |
| `email`       | string       | one of email/domain/linkedin | Email address                                                          |
| `domain`      | string       | one of email/domain/linkedin | Company domain                                                         |
| `linkedin`    | string       | one of email/domain/linkedin | LinkedIn profile URL                                                   |
| `full`        | boolean      | no                           | Return full phone details (carrier, line type, and so on)              |
| `webhook_url` | string (URL) | no                           | Hosted server only: public URL that receives the result asynchronously |

## Workflow

1. Use the most specific input you have: email, then LinkedIn, then domain.
2. Call `phone_finder`.
3. Optionally validate the number with `tomba-phone-validator`.

## Output Expectations

- Numbers in international format, with line type, carrier, and country when available.

## Example Usage

```
/tomba:tomba-phone-finder john@acme.com
/tomba:tomba-phone-finder zapier.com
/tomba:tomba-phone-finder https://www.linkedin.com/in/username full
```

## Example Tool Call

User: "Find a phone number for john@acme.com"

```json
{
    "tool": "phone_finder",
    "arguments": {
        "email": "john@acme.com",
        "full": true
    }
}
```
