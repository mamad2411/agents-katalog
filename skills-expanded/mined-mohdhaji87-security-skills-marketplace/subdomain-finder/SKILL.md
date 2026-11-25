---
name: subdomain-finder
description: Enumerate subdomains of a target domain using passive and active techniques for authorized security testing. Use when user asks to find subdomains, enumerate DNS, discover attack surface, perform reconnaissance, or do subdomain discovery for bug bounty or penetration testing. Combines certificate transparency logs, public APIs, DNS brute-forcing, and zone transfer attempts.
---

# Subdomain Finder

Enumerate subdomains using passive sources (crt.sh, HackerTarget, RapidDNS) and active techniques (DNS brute-force, zone transfers).

**Authorization required**: Only use against domains you have explicit permission to test.

## Quick Start

```bash
# Install dependency
pip install dnspython

# Full enumeration (passive + active)
python scripts/subdomain_finder.py example.com

# Passive only (no direct DNS queries to target)
python scripts/subdomain_finder.py example.com --passive

# Active only with custom wordlist
python scripts/subdomain_finder.py example.com --active -w /path/to/wordlist.txt

# Save results as JSON
python scripts/subdomain_finder.py example.com -o results.json -f json
```

## Scripts

| Script | Purpose |
|--------|---------|
| `subdomain_finder.py` | Main tool combining all techniques |
| `passive_enum.py` | Passive enumeration only (CT logs, APIs) |
| `active_enum.py` | Active enumeration (brute-force, zone transfer) |

## Passive Sources

- **crt.sh**: Certificate Transparency logs
- **HackerTarget**: DNS lookup API
- **RapidDNS**: Subdomain database

## Active Techniques

- **DNS brute-force**: Test common subdomain prefixes against target
- **Zone transfer (AXFR)**: Attempt to dump full DNS zone (rarely works)

## Options

```
-w, --wordlist    Custom wordlist for brute-forcing
-t, --threads     Concurrent threads (default: 20)
-n, --nameserver  Custom DNS resolver IP
--passive         Passive enumeration only
--active          Active enumeration only
--no-resolve      Skip IP resolution
-o, --output      Save results to file
-f, --format      Output format: text or json
-q, --quiet       Output subdomain list only
```

## Example Workflow

```bash
# 1. Start with passive recon (safe, fast)
python scripts/passive_enum.py target.com -o passive.json

# 2. Review results, then active scan with larger wordlist
python scripts/active_enum.py target.com -w wordlist.txt -o active.json

# 3. Or run full enumeration
python scripts/subdomain_finder.py target.com -o full_results.json -f json
```

## Wordlists

Built-in wordlist covers ~200 common prefixes. For thorough scans, use external wordlists. See `references/wordlists.md` for recommendations.
