---
name: dns-lookup
description: DNS lookups, reverse DNS, WHOIS, and domain checks via MCP. Use when asked to check DNS records or domain ownership.
---

# DNS Lookup via MCP

Use this skill when you need to look up DNS records, perform reverse DNS, check WHOIS data, or verify nameservers. Zero auth required.

## Available Tools

| Tool                | What it does                                                  |
| ------------------- | ------------------------------------------------------------- |
| `dns_lookup`        | Look up A, AAAA, MX, TXT, NS, CNAME, SOA, SRV, or PTR records |
| `reverse_dns`       | Reverse DNS (PTR) lookup on an IP address                     |
| `resolve_all`       | Resolve A, AAAA, MX, TXT, NS, CNAME in one call               |
| `check_nameservers` | Get nameserver (NS) records for a domain                      |
| `whois`             | Query WHOIS data (follows IANA referrals to registrar)        |

## Workflow

1. For general domain investigation: start with `resolve_all` to see everything at once
2. For specific record types: use `dns_lookup` with the `type` parameter
3. For IP investigation: use `reverse_dns` to find the hostname
4. For domain ownership: use `whois`

## Key Patterns

- `dns_lookup` with `type: "MX"` is the go-to for email delivery debugging
- `resolve_all` returns all common record types in one call — most efficient for initial investigation
- `whois` follows IANA referrals automatically, so it works for any TLD
- No API keys or auth needed — uses Node.js built-in DNS and public WHOIS servers
