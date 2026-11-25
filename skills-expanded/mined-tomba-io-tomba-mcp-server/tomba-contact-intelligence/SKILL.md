---
name: tomba-contact-intelligence
description: Use Tomba MCP tools for contact discovery, verification, enrichment, and company research.
user-invocable: true
argument-hint: "<goal, e.g. find the head of sales at zapier.com>"
version: 1.0.0
metadata:
    openclaw:
        emoji: "\U0001F50D"
        homepage: https://tomba.io
---

# Tomba Contact Intelligence

Use this skill when the user needs contact discovery, email verification, lead enrichment, phone lookup, domain research, company research, or technology/competitor analysis.

This skill assumes the Tomba MCP server is already connected and the following tools are available in the session:

- `domain_search`
- `email_finder`
- `email_verifier`
- `email_enrichment`
- `author_finder`
- `linkedin_finder`
- `phone_finder`
- `phone_validator`
- `email_count`
- `similar_finder`
- `technology_finder`
- `companies_search`
- `email_sources`
- `email_format`
- `domain_status`
- `autocomplete`
- `location`
- `person_enrichment`
- `company_enrichment`
- `combined_enrichment`
- `account_info`
- `usage_info`
- `list_flags`
- `create_flag`
- `list_leads`
- `create_lead`
- `list_keys`
- `get_logs`

## Per-Tool Skills

For detailed inputs and examples, each tool has its own skill in `skills/tomba-<tool-name>/`. Skill names match the folder names and use hyphens instead of underscores (e.g. `email_finder` → `tomba-email-finder`, invoked as `/tomba:tomba-email-finder` in plugin hosts):

| Group        | Skills                                                                                                                                                                 |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Email        | `tomba-email-finder`, `tomba-email-verifier`, `tomba-email-enrichment`, `tomba-email-count`, `tomba-email-sources`, `tomba-email-format`                               |
| Discovery    | `tomba-domain-search`, `tomba-author-finder`, `tomba-linkedin-finder`                                                                                                  |
| Phone        | `tomba-phone-finder`, `tomba-phone-validator`                                                                                                                          |
| Company      | `tomba-companies-search`, `tomba-company-enrichment`, `tomba-similar-finder`, `tomba-technology-finder`, `tomba-autocomplete`, `tomba-location`, `tomba-domain-status` |
| Enrichment   | `tomba-person-enrichment`, `tomba-combined-enrichment`                                                                                                                 |
| Leads        | `tomba-list-leads`, `tomba-create-lead`                                                                                                                                |
| Data quality | `tomba-list-flags`, `tomba-create-flag`                                                                                                                                |
| Account      | `tomba-account-info`, `tomba-usage-info`, `tomba-list-keys`, `tomba-get-logs`                                                                                          |

## Hosted Server Notes

- On the hosted server (`https://mcp.tomba.io/mcp`), sign in with OAuth or send API keys. The local npm server needs `TOMBA_API_KEY` and `TOMBA_SECRET_KEY`.
- Some input names differ: the hosted server uses `first_name`, `last_name`, `full_name`, and `enrich_mobile`; the local server uses `firstName`, `lastName`, `fullName`, and `enrichMobile`. Always use the names in the connected tool's schema.
- Send phone numbers in E.164 format (e.g. `+33612345678`).

## When To Use

Use this skill for requests like:

- find the best person to contact at a company
- guess and verify an email address
- enrich a lead with company and contact data
- find phone numbers tied to an email, domain, or LinkedIn profile
- research a domain's scale, technology, or similar competitors
- build target company lists with industry, size, location, or revenue filters

Do not use this skill for general web research that does not need Tomba data, or when the user is asking for unsupported actions such as sending emails.

## Tool Selection

Choose tools based on the user's objective:

- Use `email_finder` when you have a person name plus company or domain.
- Use `email_verifier` after `email_finder` when the user needs a validated result.
- Use `email_enrichment` when the user already has an email and wants more profile data.
- Use `domain_search` when the user wants contacts for a company or domain without a specific person.
- Use `phone_finder` when the user wants phone numbers from an email, domain, or LinkedIn profile.
- Use `phone_validator` when the user provides a phone number and wants validation or carrier details.
- Use `linkedin_finder` when the user has a LinkedIn URL and wants an email.
- Use `author_finder` when the user provides an article URL and wants the author's contact.
- Use `email_count` to estimate the reachable contact surface for a domain.
- Use `technology_finder` to inspect a company's website stack.
- Use `similar_finder` to find comparable or competing domains.
- Use `companies_search` when the user wants a company list filtered by market, geography, size, revenue, type, or industry.
- Use `email_format` to learn a domain's email pattern when `email_finder` returns nothing.
- Use `email_sources` when the user wants to know where an email was found.
- Use `domain_status` to screen out webmail or disposable domains.
- Use `autocomplete` to turn a company name into a domain before other lookups.
- Use `location` to see where a company's employees are based.
- Use `person_enrichment`, `company_enrichment`, or `combined_enrichment` for profile, firmographic, or full lead enrichment.
- Use `list_leads` and `create_lead` to read or save leads in the user's Tomba account; only create leads when the user asks.
- Use `list_flags` and `create_flag` to review or report bad data; only flag data when the user asks.
- Use `account_info`, `usage_info`, `list_keys`, and `get_logs` for credits, usage, API keys, and request logs.

## Workflow Guidance

Prefer short multi-step workflows that improve confidence:

1. If the user names a person, start with `email_finder`.
2. Verify the result with `email_verifier` before presenting it as high-confidence.
3. If the user wants broader prospecting, use `companies_search` or `domain_search` first.
4. Add `email_enrichment`, `phone_finder`, `technology_finder`, or `similar_finder` only when they answer the user's actual goal.

When several plausible contacts exist, rank them by relevance to the requested department or role and say why the top result was selected.

If the user does not provide enough information, ask only for the missing fields that materially improve the result, such as company domain, full name, article URL, LinkedIn URL, or target department.

## Output Expectations

When returning results:

- distinguish clearly between confirmed data and inferred data
- mention whether an email was verified
- include the source input used for each lookup
- keep summaries concise and decision-oriented
- if no high-confidence result is found, say that directly and suggest the next best lookup path

## Common Playbooks

### Find A Person's Best Email

1. Use `email_finder` with the person's name and company.
2. Use `email_verifier` on the strongest candidate.
3. If requested, use `email_enrichment` and `phone_finder`.

### Research A Company For Outreach

1. Use `domain_search` to identify existing contacts.
2. Use `email_count` to estimate contact coverage.
3. Use `technology_finder` and `similar_finder` for company context.

### Build A Target Account List

1. Use `companies_search` with the user's market filters.
2. For top matches, use `domain_search` or `email_finder` for contact discovery.
3. Verify candidate emails before presenting them as final.
