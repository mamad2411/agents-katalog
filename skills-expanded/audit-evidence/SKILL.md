---
name: audit-evidence
description: Evidence collection and packaging for security audits — evidence types (inspection/observation/inquiry/re-performance/automated), cadence per control, chain of custody, period tagging, WORM storage and retention, auditor delivery. Usable for SOC 2, ISO 27001, NIS2, DORA, and internal audits.
---

# Audit Evidence Collector

> **Disclaimer**: this skill covers operational evidence collection. Legal holds, forensics-grade chain of custody for legal proceedings, and legal evidentiary weight require separate expertise (forensics-assist/legal). This skill targets compliance-audit-grade evidence.

## When to use

Every audit runs on evidence. Compliance frameworks are the "what must you"; this skill is the "how do you prove it". It is the counterpart of what `iso27001` phase 5 and `soc2` phase 4 ask for: a systematic collection an auditor can consume without six weeks of back-and-forth questions.

Triggers on:

- A question like "how do we collect evidence for SOC 2 Type II", "what is control evidence", "evidence packaging for the auditor", "chain of custody for audit", "set up automated evidence collection", "how long do we keep audit evidence".
- Preparation for an external audit: SOC 2, ISO 27001 Stage 2, PCI-DSS, internal audit per ISMS Cl 9.2.
- A handoff from `iso27001`, `soc2`, `nis2`, `dora` where evidence requirements need to be operationalized.
- A vendor-security review that asks for evidence output toward customers (see `vendor-questionnaire` receiver mode).
- A post-incident review where evidence on controls must be reconstructed.

### When NOT (handoff)

- Forensics-grade evidence for court or incident response → `forensics-assist` plus legal. Audit evidence is lighter.
- Legal-hold procedures → legal.
- Policy drafting → `policy-drafter`.
- Risk-register data collection → `risk-register`.
- Technical implementation of logging/monitoring that produces evidence → `secure-coding`, `k8s-security`, `log-triage`, `siem-query`.
- Vendor-attestation review (you receive their SOC 2) → `vendor-questionnaire`.

## Approach

Seven phases. Phases 2–4 form the collection discipline; phase 5 is storage/retention; phase 6 is auditor delivery.

### 1. Evidence inventory per control

Every control has an evidence signature. Start with a matrix: control-ID → evidence type(s) → producer → frequency → storage location.

Example row for a SOC 2 CC6.1-style access control:

- Control: "User access is authorized before provisioning".
- Evidence types: ticket log (access requests with approval signature), quarterly access-review report (with exceptions logged), automated config snapshot of IAM roles.
- Producers: HR onboarding tool, IAM admin, CI/config-drift detection.
- Frequency: per event (ticket), quarterly (review), daily (snapshot).
- Storage location: GRC platform / evidence repo.

Do this per active control. A framework with 100 controls produces a matrix of 100-300 evidence items. This is one-off work plus maintenance on control change.

### 2. Evidence types and AICPA taxonomy

AICPA distinguishes five evidence types (relevant for SOC 2, broadly applicable):

- **Inspection**: written document review. Policies, tickets, access-review reports, change-management approvals, meeting minutes. Most common evidence for static controls.
- **Observation**: the auditor watches something happen. "Show me how a user is deactivated". Less used since remote audits, still relevant for physical controls.
- **Inquiry**: interview with the control owner. Rarely standalone evidence — must be supported by inspection or observation.
- **Re-performance**: the auditor performs the control themselves and compares results. "Give me five random access-review entries; I will validate them in the IAM console myself".
- **Automated evidence** (modern addition): system-generated logs and config snapshots produced without human intervention. Highest reliability for operating effectiveness.

Per control mix: inspection evidence for design adequacy, automated/re-performance for operating effectiveness.

### 3. Evidence quality: fresh, traceable, reproducible

Bad-quality evidence is evidence that does not count. Three criteria:

- **Fresh**: produced within the observation period, with a verifiable date/timestamp. A screenshot without a timestamp is half-value. Logs with tamper-prone timestamps (writable NTP) are lower-value.
- **Traceable**: full chain visible from subject → control → evidence. "This screenshot is of user X on date Y in system Z" must be explicit. Stripped metadata lowers value.
- **Reproducible**: an auditor can ask again and get comparable evidence. One-off, manually scraped-together evidence raises doubt about control operating effectiveness.

**Anti-pattern**: evidence "made for the audit" in the week before the auditor arrives. Visible in clustered timestamps. Auditors recognize this and downgrade the control to design-only or a nonconformity.

**Automated is almost always better** than manual evidence. Lower operational burden and better freshness/traceability.

### 4. Chain of custody and period tagging

For compliance-audit evidence, full forensic chain of custody is overkill. Lightweight variant:

- **Producer attribution**: who/what produced the piece of evidence (user-ID, system-ID, API endpoint)?
- **Collection point**: how was it moved into the evidence repo (automated pipeline, manual upload via a specific tool)?
- **Storage immutability**: no changes possible after collection. Hash verification afterward if needed.
- **Access log** on the evidence itself: who looked at it, when. Helps when the auditor asks "how do I know this was not changed afterward".

**Period tagging**: every evidence item must be tied to the audit period in which it was collected. Type I = point-in-time, but for Type II (3-12 months) you must know per item which week/month it falls in. Tagging as a metadata field: `observation-period: 2025-Q3`.

In a multi-audit context (simultaneous SOC 2 + ISO 27001): one evidence item can carry multiple tags, mapped to different control IDs. One collection, multiple uses.

### 5. Storage and retention

- **Repository choice**: GRC platform (Vanta, Drata, Secureframe, Archer, OneTrust) with built-in evidence management, or self-built (SharePoint/Confluence with versioning plus metadata). The platform wins on scale at ≥ 25 active controls with recurring cadences; manual is feasible up to ~15.
- **Immutability**: write-once-read-many (WORM) where critical (SOC 1 interface, financial). For SOC 2/ISO 27001 versioned-plus-access-controlled is sufficient.
- **Retention periods**: at least 1 audit cycle plus 1 year. For financial (DORA, SOX interfaces): 7 years common. For privacy-related evidence with personal data: AVG minimization principle conflicts — retention only as long as compliance requires, then delete. Document.
- **Backup and recovery**: evidence loss right before an audit is existential. Geo-spread backups, recovery test.
- **Access control**: tier-appropriate. Control owners can produce/upload; auditors (internal and external) can read; nobody can change retroactively.

### 6. Auditor delivery

The auditor wants evidence in a structure that matches their testing workflow.

- **Evidence Request List (ERL)**: the auditor usually delivers a list ahead of time with "I want to see X, Y, Z". Map each ERL item to repo locations. Confirm presence before audit week, not during.
- **Indexing per control**: every evidence request hangs on a specific control-ID. Delivery: the auditor receives access to the subset relevant to their engagement.
- **Sampling basis**: the auditor typically requests random samples from populations (e.g. "give me 10 random change tickets from the last quarter"). You deliver, the auditor traces back to verify the population is correct. The mechanism by which you sample must be reproducible; sampling "with a wink" shows on resampling.
- **Exceptions**: controls that did not run perfectly (a missed access review, a change without approval). Proactively document with root cause and corrective action. The auditor will otherwise find them and the impact on the report is larger.
- **Remote vs on-site**: remote audit has been the default since 2020. The auditor receives controlled access to a space (screen share, virtual evidence room, gated cloud share). Avoid emailing unmarked evidence — that fragments the chain and produces security findings on your own evidence hygiene.

### 7. Verification-loop

Layer 1: scope (all active controls have evidence signatures?, all evidence items period-tagged?, every evidence item has a producer trace?), assumptions ("automated evidence" really automated, not manually scheduled?), gaps (exceptions documented with root cause, not silently swept away?). Layer 2: AICPA evidence-type terminology correct, framework-specific retention requirements not invented (DORA/NIS2/AVG periods have a concrete legal basis, verify), no claim that "WORM" is in place when it is not actually write-once.

## Output

```
Evidence package — <audit type + period>
Auditor: <firm if engaged> | Framework: <SOC 2 Type II | ISO 27001 Stage 2 | ...>
Observation period: <start → end> | Delivery date: <...>

Evidence matrix:
  Controls in scope:    N
  Evidence items:       M
  Coverage:             <% of controls with complete evidence>
  Automated evidence:   <% automated vs manual>

Per control group (aligned with framework):
  CC1 / Cl 4-5 / ...:   N items, all complete | gaps: ...
  CC6 / Cl 8 / A.8.x:   ...
  ...

Evidence quality:
  Fresh (within period): <%>
  Traceable:             <%>
  Reproducible:          <%>

Chain + metadata:
  Producer attribution: <all items | gaps: ...>
  Period tagging:       <all items | gaps: ...>
  Immutability:         <WORM | versioned | ad-hoc>

Storage + retention:
  Repository:           <platform name or custom>
  Retention policy:     <policy + next purge date>
  Access log active:    <yes/no>

Exceptions register:
  Count:                N
  Root cause per item:  <...>
  Corrective executed:  <status>

Delivery mode:
  ERL mapping:          <ready | work in progress>
  Virtual data room:    <access link + credentials via separate channel>

Verification-loop: ...
```

## References

- **AICPA Audit Evidence Standards (AU-C 500)** — [https://us.aicpa.org/research/standards/auditattest](https://us.aicpa.org/research/standards/auditattest). Auditor guidance on evidence types and sufficient appropriate evidence.
- **AICPA SOC 2 Guide** — via the AICPA store. Covers evidence requirements per Trust Service Criterion.
- **ISO/IEC 27001:2022 Cl 9.2 + 9.3** — internal audit + management review. Expects evidence-based decisions.
- **ISO/IEC 27008:2019** — [https://www.iso.org/standard/67397.html](https://www.iso.org/standard/67397.html). Guidelines for assessors on ISMS controls.
- **NIST SP 800-53A Rev. 5** — [https://csrc.nist.gov/pubs/sp/800/53/a/r5/final](https://csrc.nist.gov/pubs/sp/800/53/a/r5/final). Assessing Security and Privacy Controls, evidence-gathering methods.
- **OSCAL** — [https://pages.nist.gov/OSCAL/](https://pages.nist.gov/OSCAL/). NIST format for machine-readable assessment plans, evidence records, and findings.
- **Shared Assessments Audit Program Evaluation Tool** — [https://sharedassessments.org/](https://sharedassessments.org/). For vendor-audit-evidence alignment.

## Categories

- grc
