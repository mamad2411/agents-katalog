---
name: tomba-companies-search
description: "Build target company lists by location, industry, size, revenue, type, keywords, SIC/NAICS, founding year, or lookalike domains using Tomba's companies_search tool."
user-invocable: true
argument-hint: "<criteria: location, industry, size, revenue, type, keywords...>"
version: 1.0.0
metadata:
    openclaw:
        emoji: "🔎"
        homepage: https://tomba.io
---

# Tomba Companies Search

This skill uses the `companies_search` tool from the Tomba MCP server. Use the hosted server at `https://mcp.tomba.io/mcp` (sign in with OAuth, or send API keys), or run the local npm package with `TOMBA_API_KEY` and `TOMBA_SECRET_KEY` set.

## When To Use

- The user wants a list of companies that match market criteria (an ICP or TAM list).
- Account-based prospecting before you look up contacts.

Do not use it when:

- The user already has a specific company: use `tomba-company-enrichment`.

## Inputs

| Parameter     | Type         | Required                         | Notes                                                                              |
| ------------- | ------------ | -------------------------------- | ---------------------------------------------------------------------------------- |
| `filters`     | object       | yes on local, optional on hosted | Filter object (see below); each key takes `{ "include": [...], "exclude": [...] }` |
| `page`        | number       | no                               | Page number, default `1`                                                           |
| `query`       | string       | no                               | Hosted server only: company name or keywords, 8-100 characters                     |
| `webhook_url` | string (URL) | no                               | Hosted server only: public URL that receives the result asynchronously             |

## Filter Keys

| Key                               | Values                                                                                                                   |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `location_country`                | ISO 3166-1 alpha-2 codes, e.g. `"DE"`, `"US"`. Full country names such as `"Germany"` return no results                  |
| `location_city`, `location_state` | Free text, e.g. `"Berlin"`, `"California"`                                                                               |
| `industry`                        | LinkedIn Industry Codes V2 names, e.g. `"Computer Software"`, `"Internet"`; use `keywords` if the industry is not listed |
| `type`                            | `education`, `government`, `nonprofit`, `private`, `public`, `personal`                                                  |
| `size`                            | `1-10`, `11-50`, `51-250`, `251-1K`, `1K-5K`, `5K-10K`, `10K-50K`, `50K-100K`, `100K+`                                   |
| `revenue`                         | `$0-$1M`, `$1M-$10M`, `$10M-$50M`, `$50M-$100M`, `$100M-$250M`, `$250M-$500M`, `$500M-$1B`, `$1B-$10B`, `$10B+`          |
| `keywords`                        | Free-text keywords                                                                                                       |
| `sic`, `naics`                    | Industry codes as strings                                                                                                |
| `founded`                         | Years as strings, e.g. `"2020"`                                                                                          |
| `similar`                         | Lookalike domains, e.g. `"stripe.com"`                                                                                   |
| `technologies`                    | Hosted server only: technologies the company uses, e.g. `"Shopify"`                                                      |

## Workflow

1. Translate the user's ideal customer profile into filters, using only the keys that are needed.
2. Call `companies_search`; page through results only if the user needs more.
3. For the top accounts, find contacts with `tomba-domain-search` or `tomba-email-finder`.

## Output Expectations

- A table of company, domain, industry, size, and location.
- Restate the filters you applied so the user can refine them.

## Example Usage

```
/tomba:tomba-companies-search IT companies in DE with 51-250 employees
/tomba:tomba-companies-search fintech startups in US founded 2020
/tomba:tomba-companies-search public companies in FR with revenue $100M-$250M
/tomba:tomba-companies-search companies similar to stripe.com in GB
```

## Example Tool Call

User: "IT companies in Germany with 51-250 employees"

```json
{
    "tool": "companies_search",
    "arguments": {
        "filters": {
            "location_country": {
                "include": ["DE"]
            },
            "industry": {
                "include": ["Information Technology and Services"]
            },
            "size": {
                "include": ["51-250"]
            }
        }
    }
}
```
