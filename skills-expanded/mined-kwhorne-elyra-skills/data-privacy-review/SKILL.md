---
name: data-privacy-review
description: Audit code and systems for GDPR/CCPA-style data privacy compliance - data minimization, consent, subject rights, retention, transfers, and breach readiness. Use when the user asks for a privacy review, GDPR check, data protection audit, or handling personal data correctly.
license: MIT
compatibility: elyra >=0.1, claude-code
allowed-tools: read, bash, grep
metadata:
  author: elyra-skills
  version: 1.0.0
  tags: [privacy, gdpr, ccpa, compliance, review]
---

# Data Privacy Review

A practical privacy audit. The goal isn't a certificate on the wall — it's that you can answer "what personal data do you have, why, for how long, and where?" without scrambling.

This is **engineering guidance, not legal advice**. For regulated industries or cross-border specifics, involve a DPO or counsel.

## When to use

- "Review for GDPR / CCPA / privacy compliance"
- "Are we handling personal data correctly?"
- "Audit data collection / retention / sharing"
- "Implement subject rights (deletion, export)"
- "Handle a data subject request"

## Scope first

Privacy reviews sprawl quickly. Pick one:

| Scope | Focus |
|---|---|
| Data inventory | What data do we hold, where, why |
| New feature review | What's this feature collecting and processing |
| Subject rights | DSAR / deletion / export pipelines |
| Vendor / sub-processor | Sharing with third parties |
| Breach readiness | Detection, notification, response |

## Procedure

1. **Build (or read) the data inventory**: what personal data, where stored, who can access, what for, how long
2. **Map data flows**: collection → processing → storage → sharing → deletion
3. **Walk the checklist** below per scope
4. **Surface gaps** with severity and concrete fixes

## Checklist

### Data minimization (the most important one)

- [ ] Each collected field has a **documented purpose** ("we need email to send receipts")
- [ ] No collecting "just in case" — fields without purpose get removed
- [ ] Optional fields are actually optional in the UI
- [ ] Truncate/hash where full data isn't needed (e.g., IP-prefix instead of full IP)
- [ ] Logs and analytics aren't smuggling PII you didn't intend to collect
- [ ] Don't store what you can fetch on demand from an authoritative source

> Rule of thumb: if you can't write a sentence explaining why this field exists, delete it.

### Legal basis (GDPR)

Every processing activity needs one of:

- [ ] **Consent** — freely given, specific, informed, unambiguous; **revocable**; logged
- [ ] **Contract** — necessary to provide the service the user signed up for
- [ ] **Legal obligation** — required by law (tax records, KYC)
- [ ] **Vital interests** — life-or-death (rare)
- [ ] **Public task** — gov / public-interest bodies
- [ ] **Legitimate interest** — balanced against user rights; documented in a LIA

Each field/feature should be tagged with the legal basis. "Because we want to" is not on the list.

### Consent (when that's the basis)

- [ ] Consent is **opt-in**, not pre-checked
- [ ] Granular: separate consent per purpose (newsletter ≠ product analytics ≠ third-party ads)
- [ ] **Withdrawal is as easy as giving consent** (no "email us to opt out")
- [ ] Consent records stored (what, when, version of the notice they saw)
- [ ] No "consent walls" before access to core functionality

### Special categories (GDPR Art 9)

Extra protection for: race, ethnicity, political opinions, religion, union membership, genetic, biometric (for ID), health, sex life, sexual orientation.

- [ ] Avoid collecting these unless absolutely necessary
- [ ] Explicit consent (or another Art 9 condition) required
- [ ] Separate access controls and logging

### Subject rights

Implement these as actual pipelines, not "email us":

| Right | What's required |
|---|---|
| **Access (DSAR)** | Return a copy of all personal data you hold on the user, in a machine-readable format, within 30 days |
| **Rectification** | User can correct inaccurate data |
| **Erasure ("right to be forgotten")** | Delete on request, subject to legal-retention overrides. Includes backups (or documented retention overlap window). |
| **Restriction** | Halt processing while a dispute is resolved |
| **Portability** | Provide data in a structured, common format (JSON, CSV) |
| **Object** | Stop processing for direct marketing, etc. |
| **Automated decision-making** | Right to human review of automated decisions with significant effect |

- [ ] DSAR endpoint or process exists and has been tested end-to-end
- [ ] Deletion really deletes (no orphan rows in audit tables, analytics, backups beyond retention)
- [ ] Identity verification step before fulfilling (don't ship someone's data to whoever asks)
- [ ] SLA: most regulations require ≤30 days

### Retention

- [ ] Each data class has a documented retention period tied to its purpose
- [ ] Retention enforced automatically (scheduled deletion job), not by hope
- [ ] Backups have a retention policy and overlap window documented
- [ ] Logs containing PII have a retention shorter than raw business data
- [ ] Customers offboarded → grace period → deletion

### Cross-border transfers

If data leaves the user's jurisdiction:

- [ ] EU → US: appropriate mechanism (SCCs + supplementary measures, or adequacy decision)
- [ ] Map of which sub-processors are where
- [ ] Per-region data residency documented if you promise it
- [ ] Schrems II analysis done for high-risk transfers

### Vendors & sub-processors

- [ ] DPA (Data Processing Agreement) signed with every processor of personal data
- [ ] Sub-processor list publicly available, kept up to date
- [ ] Vendor security review on file (SOC 2, ISO 27001, or your own questionnaire)
- [ ] Onboarding new sub-processor triggers customer notification per your DPA

### Technical & organizational measures (TOMs)

- [ ] Encryption in transit (TLS 1.2+) and at rest for sensitive data
- [ ] Access controls: least privilege, MFA for admins, periodic review
- [ ] Audit logs for who accessed what personal data
- [ ] Pseudonymization where it serves the purpose (analytics IDs ≠ user IDs)
- [ ] Production data not used in dev/test (use synthetic or anonymized)

### Breach readiness

- [ ] Detection: alerts for anomalous access, large exports, exfil patterns
- [ ] Runbook: triage, contain, notify
- [ ] **72-hour notification** to supervisory authority (GDPR) — process tested
- [ ] User notification path if high risk to rights and freedoms
- [ ] Breach log kept (even for non-notifiable incidents)

### Children

If you might serve under-16s (or under-13 in the US):

- [ ] Parental consent flow
- [ ] No behavioral advertising
- [ ] Reduced data collection
- [ ] Age-gating where required

## Quick scans

```bash
# Find places that log full email / IP / phone (heuristic)
grep -RInE 'log.*(email|phone|ssn|address)\b' --include='*.{js,ts,php,py,rb,go}' .

# Direct PII in URLs (query strings end up in access logs)
grep -RInE 'GET .*\?(email|phone|name|ssn)=' --include='*.{js,ts,php,py}' .

# Long-lived tokens / no expiry
grep -RInE 'expires_in.*(86400|604800|2592000|31536000)' --include='*.{js,ts,php,py}' .

# Data residency assumptions
grep -RInE 'us-east-1|eu-west-1' --include='*.{tf,yaml,yml}' . | head
```

Heuristic, not authoritative.

## Output format

```markdown
## Privacy review: <scope>

**Data inventory snapshot:**
| Field | Purpose | Legal basis | Retention | Location |
|---|---|---|---|---|
| email | login, transactional email | contract | account life + 30d | EU |
| ip_address | abuse prevention | legitimate interest | 30 days | EU |
| analytics_id | product analytics | consent | 13 months | US (DPA: …) |

### 🔴 Blockers
- <finding>. **Risk:** <regulatory + reputational>. **Fix:** <…>.

### 🟠 Major
- …

### 🟡 Minor
- …

### Subject-rights readiness
- ✅ Access: <how, tested when>
- ✅ Deletion: <how, tested when>
- ❌ Portability: not implemented

### Sub-processor list status
- ✅ public list maintained
- ❌ DPA with <vendor> outstanding

### Recommendations (priority order)
1. …
2. …
```

## Anti-patterns

- ❌ "We don't have any personal data" (you do — emails, IPs, names, usernames)
- ❌ Free-text legal-basis field "for business reasons"
- ❌ Pre-ticked consent checkboxes
- ❌ "Deletion" that leaves the row but blanks the email
- ❌ Production PII in dev/staging
- ❌ Logging request bodies that contain PII
- ❌ "Email us at privacy@" instead of an actual DSAR pipeline
- ❌ Treating privacy as a one-time compliance project rather than ongoing engineering
- ❌ Storing analytics PII forever because "we might want it"
- ❌ Promising "we never share data" while integrating five analytics SDKs

## Tips

- **Privacy by design** is cheaper than retrofitting. Add the legal-basis field to the data model from day one.
- **Tag fields** with metadata: `@personal`, `@sensitive`, `@retention=30d`. A linter can then enforce that logging never references `@sensitive` fields without redaction.
- **Run a deletion drill quarterly** with a synthetic test user — actually request, actually fulfill, actually verify.
- **Document the *purpose* alongside the field definition**, not in a separate doc that drifts.
- **Customer-facing privacy notice should match what the code actually does.** Disagreement is the most common source of fines.

## References

- [GDPR full text](https://gdpr-info.eu/)
- [CCPA / CPRA](https://oag.ca.gov/privacy/ccpa) — California
- [ICO guidance (UK)](https://ico.org.uk/for-organisations/) — readable practical guidance
- [CNIL (France) developer's guide](https://lincnil.github.io/Guide-RGPD-du-developpeur/en/) — engineer-focused
- [OWASP Top 10 Privacy Risks](https://owasp.org/www-project-top-10-privacy-risks/)
