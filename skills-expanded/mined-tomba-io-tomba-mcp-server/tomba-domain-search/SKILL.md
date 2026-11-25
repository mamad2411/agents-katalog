---
name: tomba-domain-search
description: "List the email addresses and contacts Tomba has for a company domain, optionally filtered by department and country, using the domain_search tool."
user-invocable: true
argument-hint: "<domain or company> [department] [country] [limit 10|20|50] [page N]"
version: 1.0.0
metadata:
    openclaw:
        emoji: "🏢"
        homepage: https://tomba.io
---

# Tomba Domain Search

This skill uses the `domain_search` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- The user wants contacts at a company without naming a specific person.
- Finding the right person in a department (sales, marketing, engineering, and so on).

Do not use it when:

- The user names a person: use `tomba-email-finder`.
- The user only wants a count: use `tomba-email-count`, which is cheaper.

## Inputs

| Parameter       | Type         | Required          | Notes                                                                                                                                                                                                          |
| --------------- | ------------ | ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `domain`        | string       | domain or company | Company domain                                                                                                                                                                                                 |
| `company`       | string       | domain or company | Company name                                                                                                                                                                                                   |
| `limit`         | string       | no                | `"10"`, `"20"` or `"50"`; default `"10"`                                                                                                                                                                       |
| `page`          | number       | no                | Page number, default `1`                                                                                                                                                                                       |
| `department`    | string       | no                | One of: engineering, sales, finance, hr, it, marketing, operations, management, executive, legal, support, communication, software, security, pr, warehouse, diversity, administrative, facilities, accounting |
| `country`       | string       | no                | Uppercase ISO 3166-1 alpha-2 code, e.g. `US`                                                                                                                                                                   |
| `enrich_mobile` | boolean      | no                | Hosted server only: also return mobile phone data                                                                                                                                                              |
| `webhook_url`   | string (URL) | no                | Hosted server only: public URL that receives the result asynchronously                                                                                                                                         |

## Workflow

1. Pick the department that matches the user's goal (e.g. `marketing` for a marketing tool pitch).
2. Call `domain_search`; page through results only if the user needs more.
3. Rank contacts by seniority and relevance, then verify the top picks with `tomba-email-verifier`.

## Output Expectations

- A short table of name, position, department, email, and confidence.
- Company summary fields (organization, industry, size) when returned.
- Explain why the top contact was chosen.

## Example Usage

```
/tomba:tomba-domain-search zapier.com
/tomba:tomba-domain-search zapier.com marketing
/tomba:tomba-domain-search stripe.com engineering US limit 50
/tomba:tomba-domain-search "Acme Inc" sales page 2
```

## Example Tool Call

User: "Find marketing contacts at zapier.com"

```json
{
    "tool": "domain_search",
    "arguments": {
        "domain": "zapier.com",
        "department": "marketing",
        "limit": "10"
    }
}
```
