---
name: tomba-linkedin-finder
description: "Find the professional email address behind a LinkedIn profile URL using Tomba's linkedin_finder tool."
user-invocable: true
argument-hint: "<LinkedIn profile URL>"
version: 1.0.0
metadata:
    openclaw:
        emoji: "💼"
        homepage: https://tomba.io
---

# Tomba LinkedIn Finder

This skill uses the `linkedin_finder` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- The user pastes a LinkedIn profile URL and wants an email (and optionally a phone number).

Do not use it when:

- Company pages (linkedin.com/company/...): use `tomba-domain-search` with the company's domain.

## Inputs

| Parameter                        | Type         | Required | Notes                                                                    |
| -------------------------------- | ------------ | -------- | ------------------------------------------------------------------------ |
| `url`                            | string       | yes      | Public LinkedIn profile URL, e.g. `https://www.linkedin.com/in/username` |
| `enrich_mobile` / `enrichMobile` | boolean      | no       | Also return mobile phone data when available (may use extra credits)     |
| `webhook_url`                    | string (URL) | no       | Hosted server only: public URL that receives the result asynchronously   |

Where a row shows two names (`hosted / local`), the hosted server at `mcp.tomba.io` uses the first and the local npm server uses the second. Use the name in the connected tool's input schema.

## Workflow

1. Call `linkedin_finder`.
2. Verify the email with `tomba-email-verifier` if the user needs a high-confidence result.

## Output Expectations

- Name, position, company, email, and confidence, plus mobile data if it was requested.

## Example Usage

```
/tomba:tomba-linkedin-finder https://www.linkedin.com/in/satyanadella
/tomba:tomba-linkedin-finder linkedin.com/in/username with mobile
```

## Example Tool Call

User: "Get the email for linkedin.com/in/satyanadella"

```json
{
    "tool": "linkedin_finder",
    "arguments": {
        "url": "https://www.linkedin.com/in/satyanadella"
    }
}
```
