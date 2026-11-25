---
name: domainkits
description: How to use the DomainKits tools for domain data (newly registered, expired, and deleted domains; WHOIS, DNS, reverse nameserver, registrar, EPP status, and IP lookups; availability, prices, and registration trends). Use when calling these tools, to pick the right tool for each lifecycle stage, combine results, and report them.
---

# DomainKits tool guide

DomainKits tools return domain data; the analysis is yours. Their data is fresher than your training knowledge, so for anything recent, go by the tool result.

Each tool's description and input schema define its data, parameters, and accepted values. Follow them as written, and do not carry one tool's parameter values over to another.

This skill covers tool usage only. The plugin's workflow skills (brand-protection, domain-analyze, domain-cma-valuation, domain-generator, domain-name-advisor, keyword-intel, keyword-trend-hunter, domain-market-beat) and the `/domainkits:hunt`, `/domainkits:watch`, and `/domainkits:analyze` commands load on matching tasks.

Before a multi-tool sequence the user did not ask for, confirm the goal with the user. Tool calls count against their quota.

## Pick the tool by lifecycle stage

| Stage | Tools | What they find |
|---|---|---|
| Newly registered | `nrds` | Recent registrations by keyword or TLD, with filters |
| Registered | `active`, `aged`, `market` | Live registered domains. `aged` for long registration histories, `market` for names with marketplace listing data |
| Expired | `expired` | Domains in the deletion cycle, not yet open for registration |
| Deleted | `deleted` | Domains deleted after expiring, as of the latest data update |
| Changes | `domain_changes` | Recent registration and status changes to premium names |
| Unregistered | `unregistered_short_domains` | Short names unregistered as of the latest data update |

## Look up one domain

- `whois`: registration data. `epp_status` explains the status codes it returns.
- `dns`: DNS records.
- `ip_lookup`: network operator and approximate location of an IP or domain.
- `registrar`: a registrar's accreditation and parent company.
- `available`: whether one domain can be registered, and its price. `bulk_available`: the same question for a list of domains.
- `tld_check`: one name across TLDs, with per-TLD status. `bulk_tld`: for up to 50 names, how many TLDs each is registered in (counts only).
- `price`: registration and renewal prices by TLD. `market_price`: aftermarket listing price.
- `backlink_summary`: backlink profile. `keyword_data`: keyword search data.
- `keywords_trends`: what people are registering recently, as keyword lists. `tld_trends`, `tld_rank`: registration trends by TLD.

## Connect results when the user asks

- Infrastructure behind a domain: nameservers from `whois` or `dns`, then `ns_reverse` for other domains on those nameservers. `ip_lookup` adds the network operator.
- Lookalikes of a brand: `typosquat` for registered variants of a domain; `nrds` for new registrations containing the brand keyword.
- Current state of an `expired` result: `whois`.
- Registrability of a `deleted` or `unregistered_short_domains` result: `available`.
- Whether a domain is flagged as unsafe: DomainKits has no threat check. Use a URL threat-check tool the user has connected, or tell the user this check is unavailable.

## Report results

- For paged results, report the total separately from the number of results reviewed, and say how many pages were checked. Fetch more pages only when the user wants them.
- A tool's own message about a result, such as no records found, is part of the answer. Pass it on rather than treating it as a failure.
- On a limit or plan message, do not retry the same call. Tell the user what was limited. Plans and limits: https://domainkits.com/mcp

## Account tools

- `usage`: the user's current tier and remaining quota.
- `preferences`, `monitor`, `strategy`: stored on the user's DomainKits account. Create, change, or delete them only with the user's explicit consent.
