---
name: compliance-tracking
description: Tracks ONGOING compliance program operations — SOC 2, ISO 27001, GDPR, HIPAA, PCI-DSS, FedRAMP, NIST CSF — including control inventory with cross-framework mapping, owner assignments, evidence collection cadence, evidence freshness SLAs, audit calendar with lead-time milestones, and gap register. Make sure to use this skill whenever the user says track our SOC 2 / ISO 27001 / GDPR / HIPAA / PCI / FedRAMP, where are we on compliance, who owns control X, what evidence do we have for [control], evidence is stale, audit prep status, build a compliance dashboard, what frameworks does control Y satisfy, we're adding [new framework] on top of existing — what's the delta, or describes any ongoing-program compliance work spanning weeks/months/quarters. Do NOT use for: customer-facing website legal page audits (use legal:legal-audit), pre-launch compliance check on a single proposed feature (use legal:compliance-check), SOX 404 financial control TESTING specifically (use finance:audit-support — though this skill can track the SOX program at a high level), GL/bank reconciliations (use finance:reconciliation), one-off regulatory questions (just answer them directly), or contract review (use legal:review-contract). Defining characteristic: ongoing program tracking, multi-control, multi-month horizon, evidence collection, audit calendar.
---

# Compliance Tracking

Ongoing tracking of compliance programs (SOC 2, ISO 27001, GDPR, HIPAA, PCI-DSS, FedRAMP, NIST CSF) — control inventory, cross-framework mapping, owner assignments, evidence collection, evidence freshness, audit calendar, gap register, dashboard.

## When to use vs. adjacent compliance/audit skills

| Skill | When to use it |
|---|---|
| **operations:compliance-tracking (this one)** | Ongoing PROGRAM tracking — SOC 2/ISO/GDPR/HIPAA/PCI/FedRAMP over weeks–months — control register, cross-framework map, evidence, calendar, gaps |
| `legal:legal-audit` | Audit a live customer-facing website legal page (ToS, privacy policy, HIPAA notice) |
| `legal:compliance-check` | Pre-launch go/no-go check on ONE proposed initiative or feature |
| `finance:audit-support` | SOX 404 internal financial control TESTING (this skill can track SOX as a program; finance:audit-support runs the testing cycles) |
| `finance:reconciliation` | GL/bank/intercompany reconciliations specifically |
| `legal:review-contract` | Contract review against playbook |

The defining characteristic: **ongoing, multi-control, multi-month horizon, evidence-driven, audit-calendar-driven**.

## What this skill maintains

### 1. Control inventory

Per program, a register of every control:

| Control ID | Description | Framework Mapping | Owner | Frequency | Evidence type | Last evidenced | Next due | Status |
|---|---|---|---|---|---|---|---|---|
| AC-01 | MFA enforced on all privileged accounts | SOC2 CC6.1, ISO A.9.4.2, NIST 800-53 IA-2, HIPAA §164.312(a)(2)(i), PCI 8.3 | Sec eng lead | Continuous | Auth logs export | 2026-04-01 | 2026-05-01 | OK |
| AC-02 | Quarterly access review of prod systems | SOC2 CC6.3, ISO A.9.2.5, PCI 7.1.4 | Sec eng lead | Quarterly | Signed review report | 2026-01-15 | 2026-04-15 | DUE |
| CM-01 | All prod changes via PR + approval | SOC2 CC8.1, ISO A.12.1.2 | Eng lead | Continuous | GitHub PR audit log | 2026-04-10 | 2026-05-10 | OK |
| ... | | | | | | | | |

### 2. Cross-framework mapping (collect once, satisfy many)

Most security controls satisfy several frameworks. Map them once so you don't duplicate evidence collection.

**Reference cross-mapping for common controls** (cybersec/SaaS focus):

| Control concept | SOC 2 | ISO 27001:2022 | NIST 800-53 | HIPAA | PCI-DSS 4.0 | GDPR |
|---|---|---|---|---|---|---|
| MFA on privileged access | CC6.1 | A.5.17, A.8.5 | IA-2 | §164.312(a)(2)(i) | 8.3 / 8.4 | Art. 32 |
| User access reviews | CC6.3 | A.5.18 | AC-2(7) | §164.308(a)(4) | 7.2.4 | Art. 32 |
| Logging & monitoring | CC7.2 | A.8.15, A.8.16 | AU-2, AU-6 | §164.312(b) | 10.2 | Art. 32 |
| Encryption in transit | CC6.7 | A.8.24 | SC-8 | §164.312(e) | 4.2.1 | Art. 32 |
| Encryption at rest | CC6.7 | A.8.24 | SC-28 | §164.312(a)(2)(iv) | 3.5 | Art. 32 |
| Vulnerability mgmt / scanning | CC7.1 | A.8.8 | RA-5 | §164.308(a)(1)(ii)(A) | 11.3 | Art. 32 |
| Change management | CC8.1 | A.8.32 | CM-3 | §164.308(a)(8) | 6.5 | — |
| Incident response | CC7.3, CC7.4 | A.5.24-A.5.27 | IR-4, IR-6 | §164.308(a)(6) | 12.10 | Art. 33-34 |
| Backup & recovery | A1.2, A1.3 | A.8.13 | CP-9 | §164.308(a)(7) | 9.4 (storage) | Art. 32 |
| Vendor / subprocessor mgmt | CC9.2 | A.5.19-A.5.22 | SA-9 | §164.308(b) | 12.8 | Art. 28 |
| Personnel onboarding/offboarding | CC1.4, CC6.2 | A.6.1-A.6.6 | PS-3, PS-4 | §164.308(a)(3) | 12.7 | Art. 32 |
| Risk assessment | CC3.1, CC3.2 | A.5.4, Clause 6.1 | RA-3 | §164.308(a)(1)(ii)(A) | 12.3 | Art. 32, 35 |

When a user asks "what does control X satisfy" or "we're adding HIPAA on top of SOC 2 — what's the delta," start from this table, then surface only the rows where the new framework adds a unique requirement (e.g., HIPAA §164.314 BAAs and §164.312(d) PHI auth — not covered by SOC 2 alone).

### 3. Evidence collection cadence + freshness SLA

For each control, define collection cadence AND freshness SLA. "Stale" = evidence is past its freshness SLA.

| Evidence type | Collection cadence | Freshness SLA (max age before STALE) | Typical source |
|---|---|---|---|
| Auth/access logs | Monthly export | 35 days | IdP (Okta/Entra), CloudTrail |
| Quarterly access review | Each quarter | 100 days | GRC tool, signed PDF |
| Vulnerability scan | Monthly (external) / weekly (internal) | 35 days (ext), 10 days (int) | Tenable/Qualys/Snyk |
| Pen test report | Annual | 13 months | Third-party report |
| Policy review attestation | Annual | 13 months | Signed attestation |
| Risk assessment | Annual | 13 months | Internal memo |
| BCP/DR test | Annual | 13 months | Test results memo |
| Backup restore test | Quarterly | 100 days | Restore log + memo |
| SOC 2 / ISO report (subprocessors) | Annual | 13 months | Vendor portal |
| Security awareness training | Annual per employee | 13 months | LMS export |
| Code change audit log | Continuous | 35 days | GitHub/GitLab |
| Incident response runbook test | Annual | 13 months | Tabletop memo |

**Stale evidence triage:** when any item exceeds its SLA → (1) auto-create gap entry, (2) ping owner, (3) raise to dashboard, (4) escalate at 2× SLA.

### 4. Audit calendar (forward view with lead-time milestones)

Forward view of audit milestones with lead-time backstops so nothing gets surprised:

| Date | Milestone | Auditor | Owner | Status |
|---|---|---|---|---|
| 2026-05-15 | SOC 2 Type II readiness review | Internal | Sec lead | In prep |
| 2026-06-01 | SOC 2 fieldwork start | A-LIGN | Sec lead | Scheduled |
| 2026-06-30 | SOC 2 fieldwork end | A-LIGN | Sec lead | — |
| 2026-08-15 | SOC 2 Type II report received | A-LIGN | Sec lead | — |
| 2026-09-01 | ISO 27001 surveillance audit | BSI | Sec lead | Scheduled |
| 2027-01-15 | HIPAA risk assessment refresh | Internal | Sec lead | Annual |

**Standard lead-time backstops** (raise alerts at each gate):

| Lead time | Action |
|---|---|
| **T-180 days** | Confirm auditor + scope; budget locked |
| **T-90 days** | All controls operating; evidence backfill begins |
| **T-60 days** | Evidence collection sweep; gap closure plan |
| **T-30 days** | Internal readiness review; remediate any open items |
| **T-14 days** | Auditor request list reviewed; PBC list owners assigned |
| **T-0** | Fieldwork starts |
| **T+30 days** | Auditor exceptions resolved or accepted |

When summarizing the calendar: always surface the **next 90 days** of milestones AND any control with a T-X gate falling in the same window.

### 5. Open items / gaps register

| Gap | Framework requirement | Severity | Owner | Target close | Risk if not closed |
|---|---|---|---|---|---|
| No tested IR runbook for region X | SOC 2 CC7.4, ISO A.5.26 | High | IR lead | 2026-05-30 | Audit exception, possible qualified opinion |
| BAA missing for vendor Y | HIPAA §164.308(b) | High | Legal | 2026-05-15 | HIPAA breach exposure |
| Quarterly access review overdue | SOC 2 CC6.3 | Med | Sec eng | 2026-04-30 | Stale evidence on key control |

### 6. Compliance dashboard

Default summary view to produce:
- **Programs in scope** with status (in scope / in progress / certified / due-for-renewal / lapsed)
- **Controls:** # total, # operating effectively, # deficient, # not yet evidenced
- **Evidence freshness:** % current, % stale (>SLA), top 5 oldest items
- **Upcoming audit milestones:** next 90 days + the lead-time gates due in that window
- **Open gaps by severity:** High / Med / Low with target dates and aging
- **Cross-framework efficiency:** "X controls satisfy Y frameworks — N hours of duplicate evidence avoided"

## Suggested cadences

- **Weekly:** triage new gaps; evidence freshness check; 90-day calendar review
- **Monthly:** evidence collection sweep; dashboard refresh; owner reminder for stale items; lead-time gate review
- **Quarterly:** access reviews; scan reports; backup restore test; stakeholder report-out
- **Annually:** policy reviews; risk assessment; pen test; BCP/DR test; full control inventory refresh; security awareness training cycle

## Tools that should be connected for best output

- **GRC platform** (Vanta, Drata, Secureframe, Hyperproof, Tugboat) — control inventory + evidence
- **Identity provider** (Okta, Entra, JumpCloud) — MFA / access evidence
- **HRIS** (Rippling, Gusto, BambooHR) — onboarding/offboarding
- **Ticketing** (Linear, Jira, GitHub Issues) — change management evidence
- **Cloud provider audit logs** (CloudTrail, GCP Cloud Audit Logs, Azure Monitor)
- **Vulnerability scanner** (Snyk, Tenable, Qualys, Wiz)
- **Endpoint mgmt** (Kandji, Jamf, Intune) — laptop encryption/posture evidence

## When to chain other skills

- **Pre-launch on a new feature:** chain to `legal:compliance-check`
- **Ongoing SOX program testing cycles:** chain to `finance:audit-support`
- **External vendor onboarding:** chain to `legal:vendor-check` and `operations:vendor-review`
- **Newly published or revised customer-facing legal page:** chain to `legal:legal-audit`
- **DPA / BAA negotiation:** chain to `legal:review-contract`

## Puerto Rico operational note

For PR-domiciled operations, also track on the same calendar (these are NOT compliance frameworks but DO have audit/regulatory deadlines that often co-trigger reviews):
- **Act 20/22/60 grant compliance** — annual report to DDEC, employment thresholds, charitable contribution requirements
- **Hacienda (PR Treasury)** — monthly/quarterly filings (SUT, payroll withholding)
- **Departamento del Trabajo** — quarterly unemployment, workers' comp (CFSE)
- **Municipal patente** — annual volume of business filing

These appear on the audit calendar with their own owners (typically Finance/Legal, not Sec) but benefit from the same lead-time discipline.

## Output

Depending on prompt:
- **Snapshot status** — current dashboard view
- **Gap deep-dive** — one gap analyzed with remediation plan
- **Audit prep package** — control list + evidence list + open gaps for upcoming audit, anchored to lead-time gates
- **Evidence freshness report** — what is stale (past SLA) and by how much; owner + remediation
- **Cross-framework gap analysis** — delta when adding a new framework on top of existing (which controls already satisfy, which are net-new)
- **Lead-time alert** — for an upcoming audit, what gates are coming due in the next 30/60/90 days
