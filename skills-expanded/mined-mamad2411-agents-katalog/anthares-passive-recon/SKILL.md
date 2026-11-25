---
name: anthares-passive-recon
description: Use when performing passive reconnaissance against a company perimeter for authorized pentests, bug bounty, or red team scoping - enumerating subsidiaries, domains, subdomains, IP ranges, ASNs, cloud assets, or gathering OSINT via search dorks (Google/Bing/Yandex/GHDB), TLS certificate transparency, WHOIS/RDAP across RIRs, or archived content
metadata:
  type: reference
---

# Anthares Passive Recon

## Overview

Reference playbook for **passive** reconnaissance of a company's external perimeter. Passive = no direct interaction that touches the target's infrastructure beyond standard DNS / public datasets.

## Recon Workflow

Work outside-in. Each phase feeds the next:

```
1. Org discovery    → who owns what (parent + subsidiaries)
2. Domains & IPs    → reverse WHOIS, RIRs, TLS certs, BuiltWith
3. Subdomains       → amass / subfinder / crt.sh / PureDNS
4. OSINT            → dorks, archived data, source code
5. Cloud assets     → SNI scans of major providers
6. Polish           → resolve, dedupe, validate scope
```

Re-run earlier phases when later phases reveal new pivots (new org name → re-do reverse WHOIS; new IP → re-do reverse DNS).

## Which reference to load

| Task | Load |
|---|---|
| Find subsidiaries, parent domains, IP ranges, ASNs, subdomains, cloud infrastructure | `asset-enumeration.md` |
| Build search-engine dorks (Google, Bing, Yandex, GHDB) or pull archived pages | `search-engine-dorking.md` |

Read only what's needed. The references are independent; you do not need to load all of them.

## Core principles

- **Outside-in, then pivot.** Start from the parent company name → expand to domains, IPs, subdomains, cloud. Every new asset (a new acquired company, an unexpected ASN, an unexpected cloud IP) is a pivot point to re-run earlier steps.
- **Cross-validate sources.** No single dataset is complete. Reverse WHOIS may miss assets the RIR shows; Certificate Transparency may show subdomains DNS bruteforce misses. Combine.
- **Respect API quotas.** SecurityTrails/Shodan/Censys have strict quotas - cache results, use `-passive` modes, and download bulk JSON once rather than re-querying.
- **GDPR limits European TLDs.** WHOIS data for `.es`, `.de`, `.fr`, etc. is often redacted. Use the country's NIC directly (e.g., dominios.es).
- **Validate before reporting.** Resolve every domain you list; flag dead ones. A scope full of NXDOMAIN entries wastes everyone's time.

## Quick reference: top tools per phase

| Phase | First-reach tools |
|---|---|
| Org discovery | Crunchbase, Aleph (occrp.org), Google |
| Reverse WHOIS | Whoxy, ViewDNS, NetworksDB |
| RIR lookups | IANA, ARIN, RIPE, APNIC, LACNIC, AFRINIC |
| TLS certs | crt.sh, Shodan, Censys, SecurityTrails (haktrails) |
| Subdomains | amass, subfinder, assetfinder, dnsenum, PureDNS, crt |
| Cloud | sni-ip-ranges (kaeferjaeger.gay) |

## When NOT to use this skill

- Active scanning (nmap, masscan, web fuzzing) - this skill is **passive** only
- Exploitation, post-exploitation, payload generation
- Internal-only assets reachable only from inside a corporate network
