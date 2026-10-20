---
name: amass-enum-basics
description: >
  OWASP Amass basics for authorized subdomain and asset enumeration: passive vs active
  modes, config/API keys, scoping, output parsing, and handoff to deeper recon. Use for
  owned domains, bug bounty in-scope roots, or labs — not for unsolicited scanning of
  third-party organizations.
---

# Amass Enum Basics

## Scope And Authorization

- **In scope:** Domains and ASNs you own, lab targets, or programs with explicit written scope.
- **Out of scope:** Enumerating assets of organizations that did not authorize testing; aggressive active scans against fragile production without approval.
- Prefer **passive** first; escalate to active DNS/brute only when allowed.
- Store API keys for data sources in secrets, not git.
- Redact out-of-scope discoveries and customer-specific hosts from public writeups.

## When To Use

- Building an initial subdomain inventory with Amass.
- Comparing passive intel vs DNS resolution results.
- Configuring Amass datasources (API keys) for better passive coverage.
- Exporting results to other recon tools within engagement methodology.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full engagement methodology | `recon-and-methodology` |
| 401/403 bypass on found hosts | `401-403-bypass-techniques` |
| TLS/cert deep analysis | TLS skills / `tls-plaintext-acquisition` as relevant |
| Network protocol analysis | `NetworkProtocolAnalysisSkill` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Mode | Behavior | When |
| --- | --- | --- |
| Passive | OSINT/APIs/CT logs; minimal direct target traffic | Default start |
| Active | DNS queries, brute, scraping that hits target infra | Only if allowed |
| Enum | Primary enumeration subcommand family | Inventory |
| Intel | Org/ASN/whois oriented intel (as available) | Scope expansion research (still authorized) |

## Workflow

### 1. Confirm scope and success criteria

1. Record in-scope roots (`example.com`), wildcards, out-of-scope exclusions, rate limits, program rules.
2. Success: reproducible subdomain list with sources; resolved IPs where allowed; clear timestamped output dir.
3. Legal: stop if scope ambiguous.

### 2. Install and configure

```bash
amass -version
# Config path often ~/.config/amass/config.yaml (varies by version)
```

```yaml
# config.yaml excerpt (illustrative)
scope:
  domains:
    - example.com
  # ips/asns only if authorized
options:
  passive: true
datasources:
  # Add API keys per Amass docs for VirusTotal, etc.
```

1. Put API keys in env or local config ignored by git.
2. Pin Amass version in notes for reproducibility.

### 3. Passive enumeration first

```bash
mkdir -p recon/amass
amass enum -passive -d example.com -o recon/amass/passive.txt -dir recon/amass/db-passive
# JSON (version-dependent flags)
amass enum -passive -d example.com -json recon/amass/passive.json
```

1. Review count and sample hosts.
2. Filter obvious out-of-scope (if program lists exclusions).

### 4. Controlled active enum (if authorized)

```bash
# Active DNS resolution / enumeration — confirm RoE
amass enum -active -d example.com -o recon/amass/active.txt -dir recon/amass/db-active
# Optional brute with wordlist only when allowed
# amass enum -active -brute -w subdomains.txt -d example.com -o recon/amass/brute.txt
```

1. Rate-limit; avoid huge wordlists on production DNS.
2. Track NXDOMAIN noise vs real discoveries.

### 5. Parse, resolve, and dedupe

```bash
sort -u recon/amass/passive.txt recon/amass/active.txt > recon/amass/all.txt
# Resolve (if not already)
while read h; do dig +short "$h" A; done < recon/amass/all.txt | sort -u > recon/amass/ips.txt
```

| Output | Use |
| --- | --- |
| Host list | Feed HTTP probe tools (in scope) |
| Graph/DB dir | Amass graph for relationships |
| JSON | Automation pipelines |

### 6. Triage findings

1. Flag interesting names: `admin`, `staging`, `dev`, `vpn`, `jira`, `grafana`.
2. Check certificate transparency diffs vs Amass set.
3. Hand off live web services to methodology skills; do not automatically exploit.

### 7. Hand off

1. Archive command lines, Amass version, config (redacted keys), timestamps.
2. Share lists via engagement workspace; not public gists if sensitive.
3. Update scope tracker with new confirmed assets after client confirmation if needed.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Auth | Written scope roots | “Just enum the Fortune 500” |
| Mode | Passive → active | Full brute first |
| Keys | Local secret config | API keys in screenshots |
| Output | Timestamped, deduped | Overwrite single file blindly |
| Next steps | Methodology handoff | Unscoped mass exploit |

## Output Checklist

- [ ] Scope roots and exclusions recorded
- [ ] Amass version and config (redacted) noted
- [ ] Passive enum completed
- [ ] Active/brute only if authorized, with limits
- [ ] Combined unique host list produced
- [ ] Interesting targets tagged
- [ ] Results stored in engagement directory
- [ ] Handoff to next recon/testing skill done
- [ ] No API keys leaked

## Rules

- Authorized domains only.
- Prefer passive collection; justify active techniques.
- Respect program rate limits and safe harbor.
- Amass is inventory — not exploitation.
- Redact secrets and out-of-scope personal assets from reports.
