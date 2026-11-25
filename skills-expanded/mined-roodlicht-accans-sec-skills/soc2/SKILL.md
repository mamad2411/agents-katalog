---
name: soc2
description: SOC 2 Type II prep — AICPA Trust Services Criteria (Security required plus Availability/Confidentiality/Processing Integrity/Privacy), Common Criteria CC1–CC9, Type I vs Type II choice, evidence-collection rhythm, auditor-friendly packaging, Complementary User Entity Controls.
---

# SOC 2 Type II Prep

> **Disclaimer**: this skill supports preparation for a SOC 2 examination but does not replace an AICPA-licensed auditor. Only a licensed CPA firm can issue a SOC 2 report. This skill helps with pre-audit readiness.

## When to use

SOC 2 (System and Organization Controls 2) is an AICPA framework for service organizations that demonstrates that controls around Security and related Trust Services Criteria are effective. Popular in B2B SaaS because US customers (and increasingly EU customers) put it as a contractual requirement.

Triggers on:

- A question like "where do we start with SOC 2", "Type I or Type II", "which TSCs to select", "evidence for SOC 2", "explain CUECs to a customer", "overlap with ISO 27001".
- A B2B SaaS that hits a SOC 2 requirement on an RFP or master service agreement.
- A handoff from `iso27001` for a dual-attestation strategy.
- Preparation for the annual Type II cycle (observation period + report).

### When NOT (handoff)

- EU regulatory compliance (NIS2, DORA, AVG) → the relevant skills. SOC 2 is not legally required, only contractual.
- ISO 27001 as alternative or complementary → `iso27001`.
- Risk-assessment methodology → `risk-register`.
- Policy drafting itself → `policy-drafter`.
- Evidence-technical packaging → `audit-evidence`.
- Technical implementation of controls → the relevant security skills.
- SOC 1 (financial-reporting controls) is out of scope — different auditor objective.
- SOC 3 (public summary version) is mentioned in this skill but not developed in depth.

## Approach

Six phases. Phase 1 (TSC selection) sets the scope of the entire audit; phase 4 (evidence rhythm) is where most Type II projects fall down.

### 1. Scope and Trust Services Criteria selection

AICPA's Trust Services Criteria (TSC) have five categories. One is required, four are optional.

- **Security (Common Criteria CC1–CC9)** — required in every SOC 2. This is the base and the bulk of the controls.
- **Availability** — optional. Criteria around uptime, monitoring, capacity. Relevant if you have SLAs.
- **Confidentiality** — optional. Around customer data (other than personal data). Typically for enterprise SaaS with confidential customer information.
- **Processing Integrity** — optional. Around correctness/completeness of processing. Relevant for transactional systems.
- **Privacy** — optional. Around personal data; overlaps with AVG/GDPR. For EU customers, AVG compliance is usually a separate workstream.

Selection guidance:

- **Minimum/pragmatic**: Security only. Enough for most contractual requirements.
- **B2B SaaS with SLA**: Security + Availability.
- **Data processor for customers**: Security + Confidentiality.
- **Extra categories** add audit scope and cost; do not pick them "just in case".

**Scope description**: which product/service, which infrastructure, which data flows, which locations, which sub-service providers (cloud providers, payment processors, data centers). Sub-service providers require either a carve-out (their controls are not in your report) or inclusive (they are).

### 2. Type I vs Type II

- **Type I**: point in time. The auditor judges control design on one date. Faster (weeks), cheaper, limited value — it only says you have controls designed, not that they work. Typical starting choice for a first year.
- **Type II**: a period of 3–12 months, often 6 or 12. The auditor judges both design and operating effectiveness — pulls evidence from the period. This is what customers actually want. Annual cycle after the first time.

Strategy pattern: Type I after 3–6 months of implementation to clear initial contract gates, then immediately start the observation period for Type II in year 2. After year 2, a Type II every year.

### 3. Common Criteria (CC1–CC9) plus additional categories

Common Criteria (2017, updated to 2022) for Security:

- **CC1 Control Environment**: tone at the top, integrity/ethics commitment, board oversight, management philosophy, organizational structure, HR policies.
- **CC2 Communication and Information**: internal and external communications, information quality.
- **CC3 Risk Assessment**: objectives specified, risks identified, fraud assessed, change evaluated.
- **CC4 Monitoring Activities**: ongoing monitoring, internal/external evaluations, deficiencies communicated.
- **CC5 Control Activities**: controls developed, technology controls, policies deployed.
- **CC6 Logical and Physical Access Controls**: access controls, authentication, authorization, data transmission, physical access, environmental protection, data disposal.
- **CC7 System Operations**: vulnerability management, change management, incident management, backup/recovery.
- **CC8 Change Management**: changes authorized, tested, approved before deployment.
- **CC9 Risk Mitigation**: risk-mitigation strategies, vendor/BCP.

Each CC has sub-criteria (e.g. CC6.1, CC6.2, ...). Recommended: download the AICPA Trust Services Criteria document for the full tree.

Additional categories add their own criteria on top of the CC base: Availability (A1.1–A1.3), Confidentiality (C1.1–C1.2), Processing Integrity (PI1.1–PI1.5), Privacy (P1.1–P8.1).

Per criterion, name a **control** (how you address it), plus **evidence** (proof the control works).

### 4. Evidence-collection rhythm

Type II stands or falls on operating-effectiveness evidence. This is where teams fail during the observation period (often without noticing).

Evidence types:

- **Inspection**: documents (policies, incident tickets, access-review reports, change-management tickets).
- **Observation**: the auditor watches the activity happen (e.g. someone logging in via 2FA).
- **Inquiry**: an interview with the control owner.
- **Re-performance**: the auditor runs the control themselves.
- **Automated evidence**: system logs, configuration snapshots.

Evidence cadence per control type:

- **Daily logged**: authenticated access, backup success, change-deploy log.
- **Weekly/monthly**: vuln-scan output, patch compliance, incident review.
- **Quarterly**: access review (user accounts), risk-assessment update, vendor review.
- **Annually**: policy review, penetration test, BCP test, full risk reassessment.

Discipline: during the observation period, **centralize evidence** in a repository the auditor can reach. Do not wait for audit week to gather it. Compliance platforms (Vanta, Drata, Secureframe, Anecdotes, SafeBase) automate a large part of this — consider for Type II efficiency.

Per control, an evidence description that says: what, where, who produces, how often, where stored.

### 5. Auditor prep and report packaging

- **Pre-audit**: pick the auditor (a licensed CPA firm, ideally with SaaS experience). The engagement letter signs off scope, TSCs, observation period, deliverable. Kickoff meeting with control owners.
- **Interim review** (optional, for long observation periods): the auditor does a fast pass mid-period to identify gaps you can still fix.
- **Audit week**: the auditor tests evidence samples, interviews control owners, documents findings.
- **Report draft**: the auditor produces a draft SOC 2 report containing: management assertion, system description, trust services criteria + controls + test results, any exceptions/nonconformities.
- **Management response** to findings, remediation plan.
- **Final report** issued. Valid until the next cycle.

Report distribution: SOC 2 Type II reports are confidential. Share with customers under NDA. For public sharing: SOC 3 is the redacted variant.

**Complementary User Entity Controls (CUECs)**: controls your customers are responsible for (e.g. "the customer is responsible for password management of end-users within their tenant"). These appear explicitly in the report. Customers look at this to know what their side is.

### 6. Verification-loop and continuous compliance

Layer 1: TSC choice locked down with rationale?, all selected CCs/additional criteria address a control with an owner?, evidence repository present and populated over the entire period?, CUECs communicated to customers?. Layer 2: AICPA Trust Services Criteria naming correct, `[verify]` markers on CC numbering because criteria updates appear, overlap claims with ISO 27001 supported by cross-walks (not improvised), auditor-firm claims not delivered as a recommendation without qualification.

**Continuous compliance**: Type II is an annual cycle. The observation period does not stop before your next period starts — the evidence keeps running. Platforms automate this; without a platform it is a full-time job for at least one compliance lead in a mid-size org.

## Output

```
SOC 2 readiness — <service/product>
Auditor: <firm, if engaged> | Type: <I | II> | Period: <dates>

TSC selection:
  Security (CC1-9):      required — status per CC: ...
  Availability:          <yes/no>, rationale
  Confidentiality:       <yes/no>, rationale
  Processing Integrity:  <yes/no>, rationale
  Privacy:               <yes/no>, rationale

Scope:
  Product(s):            <...>
  Infrastructure:        <cloud provider(s) + regions>
  Sub-service providers: <list + carve-out/inclusive>
  Geographic:            <...>

Common Criteria coverage:
  CC1 Control Environment:  <N/X controls, evidence status>
  CC2 Communication:        ...
  CC3 Risk Assessment:      ...
  CC4 Monitoring:           ...
  CC5 Control Activities:   ...
  CC6 Access Controls:      ...
  CC7 System Operations:    ...
  CC8 Change Management:    ...
  CC9 Risk Mitigation:      ...

Evidence status:
  Centralised repo:         <platform | manual | gap>
  Cadence compliance:       <daily/weekly/monthly/quarterly streams>
  Gaps in observation period: <list>

Pre-audit readiness:
  Pre-audit walkthrough:    <date | planned | gap>
  Interim review planned:   <yes/no>
  Identified findings:      <list + remediation status>

CUECs for customers:
  Formulated:               <yes/no>
  Communicated:             <how>

Priorities:
  <fix-now/fix-sprint/fix-quarter>

Verification-loop: ...
```

## References

- **AICPA Trust Services Criteria** — [https://www.aicpa-cima.com/resources/download/2017-trust-services-criteria-with-revised-points-of-focus-2022](https://www.aicpa-cima.com/resources/download/2017-trust-services-criteria-with-revised-points-of-focus-2022). Official TSC document including the 2022 revision.
- **AICPA SOC 2 overview** — [https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2](https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2). Official landing page.
- **AICPA SOC 2 Reporting Guide** — via the AICPA store. For auditors and service organizations.
- **Cloud Security Alliance — STAR** — [https://cloudsecurityalliance.org/star](https://cloudsecurityalliance.org/star). Overlap of SOC 2 + the CSA Cloud Controls Matrix.
- **ISO 27001 <-> SOC 2 cross-walk** — [https://www.aicpa-cima.com/](https://www.aicpa-cima.com/) search for SOC 2 mapping. Useful for a dual-attestation strategy.
- **OSCAL** — [https://pages.nist.gov/OSCAL/](https://pages.nist.gov/OSCAL/). NIST format for machine-readable compliance content; usable for automated evidence collection.
- **NIST CSF 2.0** — [https://www.nist.gov/cyberframework](https://www.nist.gov/cyberframework). Frequent mapping basis between SOC 2 and other frameworks.

## Categories

- grc
