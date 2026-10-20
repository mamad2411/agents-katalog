---
name: email-dmarc-reporting-ops
description: >
  Operate DMARC reporting for owned email domains: rua/ruf mailboxes, aggregate
  (RUA) report parsing, forensic (RUF) privacy caution, and policy ramp
  p=none → quarantine → reject with pct. Use when DMARC TXT, rua=, ruf=,
  aggregate XML/gz reports, or alignment failures for SPF/DKIM. Not app-level
  header injection (see email-header-injection-defenses).
---

# Email DMARC Reporting Ops

## Scope And Authorization

- **In scope:** DNS and mail domains your organization owns; reporting mailboxes you control.
- **Out of scope:** Changing DMARC on domains you do not operate; using RUF content to stalk individuals.
- Aggregate reports contain sending IPs and volumes—treat as semi-sensitive telemetry.
- Forensic (failure) reports may include message samples—prefer off or tightly restricted.
- Coordinate SPF/DKIM changes with mail and security owners before policy tighten.

## When To Use

- Standing up or operating DMARC for corporate/product domains.
- Parsing RUA reports (in-house or vendor) to find unauthorized senders.
- Ramping policy from monitor to enforce without breaking legitimate mail.
- Debugging SPF/DKIM alignment failures after ESP migration.
- Reviewing third-party senders (CRM, ticketing, marketing) for inclusion.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| CRLF / header injection in apps | `email-header-injection-defenses` |
| Email OTP send rate limits | `email-otp-rate-limits` |
| Generic DNS ownership | `external-dns-ownership` |
| Secrets hygiene | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Record | `_dmarc.example.com` TXT with `v=DMARC1` |
| RUA | Aggregate reports daily from major receivers |
| RUF | Optional; privacy/legal review first |
| Policy | `p=none` → `quarantine` → `reject`; use `pct` for gradual |
| Alignment | SPF or DKIM must align with Header-From domain |
| Coverage | Inventory every legitimate sending service |

## Workflow

### 1. Confirm scope and success criteria

1. Domain list (apex + relevant subdomains used in From:).
2. Success: RUA flowing; unauthorized sources known; enforce policy without legitimate loss > agreed threshold.

### 2. Inventory DNS and senders

```bash
dig +short TXT _dmarc.example.com
dig +short TXT example.com | grep -i spf
dig +short TXT default._domainkey.example.com
# List known ESPs: Google, M365, SendGrid, SES, etc.
```

1. Map each marketing/transactional system’s sending domain and DKIM selector.
2. Note legacy systems still sending as `@example.com`.

### 3. Baseline with p=none

```text
v=DMARC1; p=none; rua=mailto:dmarc-rua@example.com; fo=1; adkim=r; aspf=r
```

1. Create monitored mailbox or vendor RUA endpoint; allowlist report streams.
2. Collect **2–4 weeks** of aggregate data before tightening (or org-agreed window).
3. Prefer not enabling `ruf=` until privacy review.

### 4. Parse and act on aggregate reports

1. Ingest XML (often zlib-compressed email attachments) into a parser/dashboard.
2. Classify sources: **known good**, **forwarders**, **unknown/threat**.
3. For unknown: identify if ESP needs SPF include / DKIM config, or block-worthy spoofing.
4. Fix alignment: matching DKIM domain (`d=`) or SPF envelope domain vs From.

### 5. Policy ramp

| Stage | Record sketch | Exit criteria |
| --- | --- | --- |
| Monitor | `p=none` | >95% legitimate volume aligned |
| Soft enforce | `p=quarantine; pct=25` → 100 | Support tickets acceptable |
| Enforce | `p=reject` | Residual unaligned only unexplained threat/forwarders |
| Subdomain | `sp=reject` as appropriate | Subdomain abuse controlled |

```text
v=DMARC1; p=reject; rua=mailto:dmarc-rua@example.com; pct=100; adkim=s; aspf=s
```

1. Tighten alignment (`adkim=s` / `aspf=s`) only after relaxed alignment is clean.
2. Document break-glass: lower `pct` or revert to `quarantine` if outage.

### 6. Verify with evidence

```bash
dig +short TXT _dmarc.example.com
# Send test messages from each ESP; check Authentication-Results and DMARC disposition
# Review weekly: % pass, top failing sources
```

1. External checkers (authorized for your domain) as secondary signal only.
2. Confirm RUA mailbox not full / vendor integration healthy.
3. Track ticket volume after each policy step.

### 7. Hand off

1. Runbook: add new ESP (SPF include, DKIM, test, monitor).
2. On-call: DMARC-related delivery incidents; DNS change dual-control.
3. Quarterly review of report destinations and vendor contracts.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Start | `p=none` + working RUA | Immediate `p=reject` blind |
| RUF | Off or restricted | Full samples to shared inbox |
| ESP onboarding | DKIM aligned before enforce | Marketing tool sends unaligned forever |
| Evidence | Weekly pass-rate charts | DNS changed, reports ignored |
| Ownership | Mail + security co-own | Orphan `_dmarc` record |

## Output Checklist

- [ ] Domains and From: inventory complete
- [ ] DMARC TXT present with RUA
- [ ] Aggregate reports received and parsed
- [ ] Legitimate sources fixed for alignment
- [ ] Policy ramp plan with pct/rollback
- [ ] RUF privacy decision documented
- [ ] ESP onboarding runbook written
- [ ] Residual spoofing risk noted

## Rules

- Owned domains only.
- Do not jump to `reject` without data.
- Protect aggregate/forensic report content.
- Coordinate DNS TTLs and change windows.
- App header injection is a different skill.
