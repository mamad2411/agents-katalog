---
name: tomba-email-finder
description: "Find a person's professional email address from their name plus company domain or company name using Tomba's email_finder tool."
user-invocable: true
argument-hint: "<full name> <domain or company>"
version: 1.0.0
metadata:
    openclaw:
        emoji: "📧"
        homepage: https://tomba.io
---

# Tomba Email Finder

This skill uses the `email_finder` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- The user names a specific person and a company or domain and wants their email.
- Guessing the work email of a prospect, candidate, or journalist.

Do not use it when:

- The user wants every contact at a company with no person named: use `tomba-domain-search`.
- The user only has a LinkedIn URL: use `tomba-linkedin-finder`.

## Inputs

| Parameter                        | Type         | Required                   | Notes                                                                  |
| -------------------------------- | ------------ | -------------------------- | ---------------------------------------------------------------------- |
| `domain`                         | string       | one of domain/company      | Company domain, e.g. `stripe.com` (preferred, more accurate)           |
| `company`                        | string       | one of domain/company      | Company name when the domain is unknown                                |
| `full_name` / `fullName`         | string       | full name, or first + last | Full name of the person                                                |
| `first_name` / `firstName`       | string       | full name, or first + last | First name                                                             |
| `last_name` / `lastName`         | string       | full name, or first + last | Last name                                                              |
| `enrich_mobile` / `enrichMobile` | boolean      | no                         | Also return mobile phone data when available (may use extra credits)   |
| `webhook_url`                    | string (URL) | no                         | Hosted server only: public URL that receives the result asynchronously |

Where a row shows two names (`hosted / local`), the hosted server at `mcp.tomba.io` uses the first and the local npm server uses the second. Use the name in the connected tool's input schema.

## Workflow

1. Collect a name and a domain. If you only have a company name, resolve the domain with `tomba-autocomplete` first.
2. Call `email_finder`.
3. If the user needs certainty, verify the result with `tomba-email-verifier`.
4. If nothing is found, check the domain's pattern with `tomba-email-format` and present a clearly labelled guess.

## Output Expectations

- The email, its confidence score, and whether it has been verified.
- The person's position and sources when returned.
- Say plainly when no email was found.

## Example Usage

```
/tomba:tomba-email-finder Satya Nadella microsoft.com
/tomba:tomba-email-finder John Smith at acme.com
/tomba:tomba-email-finder "Jane Doe" Acme Inc
/tomba:tomba-email-finder Satya Nadella microsoft.com with mobile
```

## Example Tool Call

User: "Find the email of Satya Nadella at Microsoft"

```json
{
    "tool": "email_finder",
    "arguments": {
        "domain": "microsoft.com",
        "first_name": "Satya",
        "last_name": "Nadella"
    }
}
```
