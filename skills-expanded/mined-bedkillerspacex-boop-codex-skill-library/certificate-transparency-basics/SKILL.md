---
name: certificate-transparency-basics
description: >
  Certificate Transparency basics for owned domains: CT logs, SCT expectations,
  monitoring new issuances (crt.sh/certstream), detecting unauthorized certs, and
  response playbooks. Use when CT monitoring, unexpected certificate issued, crt.sh
  domain search, or CAA + CT defense-in-depth — not for attacking CAs.
---

# Certificate Transparency Basics

## Scope And Authorization

- **In scope:** Domains and orgs you own; defensive monitoring of public CT logs.
- **Out of scope:** Attacking certificate authorities; abusing log infrastructure; doxxing.
- CT data is public — still handle internal hostnames carefully in reports.
- Pair with DNS CAA, `cert-manager-basics`, incident response.

## When To Use

- Detecting unexpected certificates for your domains (phishing, mis-issue, shadow IT).
- Understanding SCTs in modern TLS handshakes.
- Setting up continuous CT alerts (certstream, commercial ASM, custom).
- Investigating a suspicious cert found in CT.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Issuing/renewing certs in cluster | `cert-manager-basics` |
| Cert expiry UX/runbooks | `certificate-expiry-page` |
| CAA record operations only | DNS skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Meaning |
| --- | --- |
| CT log | Append-only public log of issued certs |
| SCT | Signed Certificate Timestamp proof of logging |
| Pre-cert | Precertificate entries often appear in logs |
| Monitors | Watch logs for names of interest |
| CAA | DNS policy which CAs may issue (complementary) |

## Workflow

### 1. Confirm scope and success criteria

1. Apex domains, wildcards, brand variants to monitor.
2. Success: alert on new CT entry not matching known issuers/automation; response runbook exists.
3. Known-good issuers list (LE, corporate PKI public intermediates, CDN-managed).

### 2. Baseline known certificates

```bash
# Manual search examples (public data)
# Use crt.sh in browser or API carefully rate-limited
curl -s "https://crt.sh/?q=%25.example.com&output=json" | head
# openssl show peer cert and check for SCTs (TLS 1.2+ extensions / OCSP)
echo | openssl s_client -connect www.example.com:443 -servername www.example.com 2>/dev/null | openssl x509 -noout -text | rg -i "CT Precertificate|1\.3\.6\.1\.4\.1\.11129"
```

1. Export inventory of expected CAs and automation paths.
2. Note multi-CDN setups that issue often.

### 3. Continuous monitoring options

| Approach | Notes |
| --- | --- |
| Commercial ASM / attack surface | Often includes CT alerts |
| certstream + filter | Real-time stream; ops to run |
| Periodic crt.sh / APIs | Simple cron; watch rate limits |
| CA account notifications | Some CAs email on issue |

```python
# Conceptual filter
# if name endswith .example.com and issuer not in ALLOWED: alert
```

1. Include common phishing patterns: `example.com.evil.tld` vs `examp1e.com` — brand monitoring may need separate tooling.
2. Alert channel: security on-call, not only email flood.

### 4. Investigate an unexpected cert

1. Record: leaf CN/SAN, issuer, notBefore/notAfter, serial, CT log entry links.
2. Is it **your** automation (cert-manager, ACM, Fastly)? Check accounts.
3. Is it a **CDN/partner** issuing for a CNAME you delegated?
4. If unauthorized: incident — consider CAA tightening, domain control recovery, browser/block reports, phishing takedown if fraudulent site.
5. Revocation may not protect all clients quickly — prioritize domain/DNS control and user warnings.

### 5. Defense-in-depth with CAA

```bash
dig CAA example.com +short
# Example policy: only specific CAs
# example.com. CAA 0 issue "letsencrypt.org"
# example.com. CAA 0 issuewild "letsencrypt.org"
# example.com. CAA 0 iodef "mailto:security@example.com"
```

1. CAA reduces accidental/unauthorized CA issuance; CT detects what still appears.
2. Coordinate CAA with all legitimate issuers (CDN, email, etc.).
3. Test changes — broken CAA blocks renewals.

### 6. SCT expectations

1. Modern public certs should be CT-logged; browsers enforce for public trust.
2. Private enterprise PKI may not use public CT — do not expect public log entries.
3. Troubleshooting “CT required” browser errors usually means mis-issued/private trust issues — not fixed by this skill alone.

### 7. Hand off

1. Runbook: alert → classify → contain → postmortem.
2. Keep allowed-issuer list updated when adding CDNs.
3. Quarterly review of CT hits volume and FP rate.
4. Automation code follows `code-quality-standards`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Coverage | All corporate domains monitored | Only homepage |
| Allowlist | Known CAs + automation | Alert on every LE renew without baseline |
| Response | Incident for unknown issuer | Ignore “probably fine” |
| CAA | Aligned with real issuers | CAA blocks own renewals |
| Scope | Defensive monitoring | Weaponize against random domains |
| Privacy | Careful with internal names in public tickets | Paste full internal maps publicly |

## Output Checklist

- [ ] Domain list for monitoring complete
- [ ] Known-good issuer/automation baseline
- [ ] Continuous CT monitoring configured
- [ ] On-call alert path tested
- [ ] Unexpected cert investigation steps documented
- [ ] CAA policy reviewed with issuers
- [ ] Partner/CDN issuance accounted for
- [ ] Incident contacts ready
- [ ] Automation quality standards applied

## Rules

- Defensive use of public CT data for your assets.
- CT complements CAA; neither replaces secure DNS/account hygiene.
- Unauthorized cert → security incident process.
- Respect rate limits of public CT query services.
- Issuance automation remains in cert-manager / CA skills.
