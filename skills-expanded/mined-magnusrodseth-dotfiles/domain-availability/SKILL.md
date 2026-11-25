---
name: domain-availability
description: Check whether domain names are available to register across many TLDs, using DNS delegation + RDAP (whois's replacement) with a system-whois fallback — no MCP, no dependencies. Use when the user asks if a domain is available, wants to check a domain name, brainstorm or find available domains, or check a name across TLDs (e.g. "is acme.com free?", "find me a domain for X", "check acme across TLDs").
---

# Domain Availability

Check domain registration status across TLDs with a bundled, dependency-free script.
Run it, read the buckets, recommend from AVAILABLE.

## Run

From this skill's directory:

```bash
python3 scripts/check_domains.py <name-or-domain> [options]
```

- `acme` — check the name across the popular TLD set (.com/.io/.ai/.dev/…)
- `acme.com` — check that exact domain, plus the popular set
- `--all` — fan out across ~90 TLDs (popular + country + new)
- `--tlds com,io,ai,dev` — check exactly these
- `--json` — machine-readable output (buckets + per-domain signals)
- `--timeout 8` · `--concurrency 10` — tuning

## How it decides (signal hierarchy)

1. **DNS NS-delegation** (`dig NS`) — registered domains are delegated, so NS records in the parent zone ⇒ **taken**. Ground truth, no rate limits.
2. **RDAP** (`https://rdap.org/domain/<d>`) — whois's ICANN-mandated JSON successor. HTTP 200 ⇒ registered, 404 ⇒ available. Authoritative where the registry supports it.
3. **whois** — fallback only when RDAP is inconclusive (429 / timeout / TLD without RDAP), guarded against IANA non-answers.

Status per domain:
- **available** — not delegated AND (RDAP 404 or whois "no match")
- **taken** — NS delegated OR RDAP 200 OR whois shows registration data
- **unknown** — everything inconclusive; the `[ns:…, rdap:…]` tag shows why

Why not just whois: WHOIS is being retired under ICANN's RDAP transition, and macOS `whois` doesn't reliably follow registry referrals for new gTLDs — it misreads the IANA delegation record. Leading with DNS + RDAP is what actually works across gTLDs and ccTLDs.

## Recommending

- Lead with `.com` — still the default users expect — then relevant new TLDs (.ai for AI, .dev/.io for tooling, .shop for commerce).
- Treat **unknown** as "not confirmed", never as available.
- This is a strong heuristic, not registrar-grade truth. End by telling the user to confirm at a registrar before buying.

## Notes

- Zero dependencies: Python 3 stdlib + system `dig`/`whois` (present on macOS; `dig` may need `dnsutils`/`bind-utils` on Linux — without it the tool falls back to RDAP + whois).
- Standalone equivalent of the `mcp-domain-availability` MCP; needs no server.
