---
name: dmarc-spf-dkim-hardening
description: >
  Assess and harden email authentication for owned domains: SPF, DKIM, and DMARC (policy
  rollout, alignment, reporting). Use when reviewing DNS TXT records, spoofing resistance,
  p=none to quarantine to reject progression, third-party senders, BIMI readiness, or
  aggregate/forensic report setup on domains you control — not for forging mail or attacking
  third-party domains.
---

# DMARC SPF DKIM Hardening

## Scope And Authorization

- **In scope:** DNS and mail streams for domains you own or are contracted to operate.
- **Out of scope:** Spoofing third parties; harvesting forensic reports from others; weakening auth on domains without approval.
- Prefer `p=none` monitoring before `quarantine`/`reject` on production domains.
- Redact message samples that contain customer mail content in tickets.
- Pair with DNS skills and `secrets-management-hygiene` for DKIM private keys.

## When To Use

- Domain spoofing / BEC risk reduction.
- Onboarding ESP/CRM/third-party senders (Google, Microsoft, Salesforce, SendGrid, etc.).
- DMARC aggregate reports show failures; moving policy stricter.
- BIMI or insurance questionnaire asks for DMARC reject.
- SPF too long / too many lookups (permerror risk).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| DNSSEC for zone integrity | `dnssec-deployment-basics` |
| General DNS latency | `dns-latency-triage` |
| Phishing site takedown | abuse/process skills |
| App email templates | product/email UX skills |
| DKIM key storage | `secrets-management-hygiene` |
| Code quality baseline | `code-quality-standards` |

## Concepts

| Mechanism | Protects | DNS artifact |
| --- | --- | --- |
| SPF | Which IPs may send for domain (path A) | TXT on apex (or include chain) |
| DKIM | Message body/headers signed by selector key | TXT `selector._domainkey` |
| DMARC | Policy + alignment of SPF/DKIM with From | TXT `_dmarc.domain` |
| Alignment | SPF domain / DKIM d= must align with From | strict (`s`) vs relaxed (`r`) |
| ARC | Forwarder chain (awareness) | Not a replacement for DMARC |

## Workflow

### 1. Confirm scope and success criteria

1. Domains (apex + sending subs), mail platforms, third-party senders list.
2. Success: inventory complete; SPF under 10 DNS lookups; DKIM signing all streams; DMARC policy target reached with failure rate acceptable; reporting mailbox monitored.
3. Change windows for DNS and ESP config.

### 2. Inventory current records

```bash
# Owned domain checks
dig +short TXT example.com | findstr /i spf
dig +short TXT _dmarc.example.com
dig +short TXT selector1._domainkey.example.com
# Windows: use dig/Resolve-DnsName
Resolve-DnsName -Name _dmarc.example.com -Type TXT
```

1. Collect DMARC RUA samples (authorized mailboxes only).
2. List every system that can send as `@example.com`.

### 3. SPF hardening

```text
v=spf1 include:_spf.google.com include:sendgrid.net ip4:203.0.113.10 -all
```

1. Prefer `-all` (fail) once inventory complete; `~all` softfail during transition.
2. Stay within **10 DNS void/lookup** limit—flatten carefully or use SPF macros/subdomains for vendors.
3. Move bulk vendors to **subdomain** sending (`mail.example.com`) with own SPF to protect apex.
4. Remove stale includes.

### 4. DKIM hardening

1. Enable 2048-bit keys where supported; rotate on schedule.
2. One selector per platform; document owners.
3. Verify signatures on real messages (headers `DKIM-Signature`).
4. Protect private keys in ESP/HSM—not in git.

### 5. DMARC rollout

```text
# Monitor
v=DMARC1; p=none; rua=mailto:dmarc-agg@example.com; ruf=mailto:dmarc-for@example.com; fo=1; adkim=r; aspf=r; pct=100

# Later
v=DMARC1; p=quarantine; pct=25; rua=mailto:dmarc-agg@example.com; adkim=r; aspf=r

# Target
v=DMARC1; p=reject; rua=mailto:dmarc-agg@example.com; adkim=s; aspf=s
```

1. Start `p=none` → fix failing sources → `quarantine` with `pct` → `reject`.
2. Alignment: ensure From domain aligns with SPF envelope or DKIM `d=`.
3. Subdomain policy `sp=` if needed; third parties should send aligned.
4. Forensic `ruf` may be high volume/PII—often aggregate-only in practice.

### 6. Third-party senders

| Action | Detail |
| --- | --- |
| Custom domain / CNAME | DKIM CNAMEs vendor records |
| Return-path domain | SPF-aligned bounce domain |
| From domain | Prefer subdomain per vendor |
| BIMI | Needs DMARC enforce + brand evidence (separate work) |

### 7. Verify and operate

```bash
# Send test to internal + DMARC checkers you trust
# Review aggregate XML/JSON reports weekly during rollout
```

1. Monitor: unexpected sources, SPF permerror, DKIM fail spikes.
2. Document: DNS owners, selectors, rollback (`p=none` emergency only with ticket).
3. Re-audit after new marketing tools.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| SPF | Includes known; `-all` | `+all` |
| Lookups | Under 10 | Nested include explosion |
| DKIM | 2048-bit; rotating | Shared leaked key forever |
| DMARC | Staged to reject | Instant reject without inventory |
| Vendors | Aligned subdomain | Random ESP using naked From |
| Reports | Monitored RUA | `p=none` forever unwatched |

## Output Checklist

- [ ] All senders inventoried
- [ ] SPF correct and lookup-safe
- [ ] DKIM on all streams; keys managed
- [ ] DMARC record with RUA
- [ ] Policy stage plan executed with metrics
- [ ] Alignment verified on sample messages
- [ ] Third parties on aligned domains
- [ ] Stale DNS removed
- [ ] Ownership and rotation documented
- [ ] Residual spoof risk noted

## Rules

- Only domains you control; no spoofing tests against third parties without authorization.
- Monitoring before enforcement.
- SPF is not encryption; combine with DKIM+DMARC.
- Treat forensic reports as sensitive mail.
- Focus on email auth DNS and sender alignment.
