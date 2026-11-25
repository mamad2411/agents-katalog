---
name: nis2
description: EU NIS2 Directive (2022/2555) gap analysis — scope determination (essential vs important entities across 18 sectors), governance obligations (Art 20), 10 baseline risk-management measures (Art 21), incident reporting timelines (Art 23), and Dutch implementation via the Cyberbeveiligingswet.
---

# NIS2 Gap Analysis

> **Disclaimer**: this skill is not legal advice. It helps with scoping and a technical gap analysis against the directive's text. Final legal qualification (entity classification, sanctions risk, contractual consequences) requires advice from a lawyer with NIS2 experience, possibly together with a compliance department or external counsel.

## When to use

The NIS2 directive (EU 2022/2555) replaces NIS1 and entered into force on 17 October 2024. The Netherlands implements it through the Cyberbeveiligingswet (`[verify current status — the legislative track has been in motion through 2024 and 2025]`). This skill covers both: the EU directive text as the primary source, the NL implementation as the application.

Triggers on:

- A question like "is our organization in scope of NIS2", "what do we need to do for NIS2", "NIS2 gap analysis", "do we have an incident-reporting obligation", "what are the 10 measures".
- An organization considering whether it is an essential or important entity (sectors in Annex I and II), or whose suppliers have that status (contractual carry-through).
- A handoff from `iso27001` or `risk-register`: NIS2 Art 21 maps onto ISO 27001 Annex A and onto NIST CSF.
- An incident where the question "must we report this to CSIRT-NL" comes up.

### When NOT (handoff)

- Technical implementation of the 10 measures at code/system level → the relevant security skills (`secure-coding`, `sast-orchestrator`, `ir-runbook`, etc.). NIS2 demands that you do things; how you do them lives in those skills.
- DORA compliance for financial entities → `dora`. DORA is lex specialis for financial; NIS2 is horizontal. Both can apply at financial organizations.
- GDPR/AVG notifications (data breaches) → `gdpr-pia` plus AVG Art 33/34. NIS2 incident reporting is additive, not a replacement.
- ISO 27001 certification as a goal → `iso27001`. NIS2 does not require certification.
- Contractual supply-chain obligations with technical implementation → `vendor-questionnaire` and `supply-chain`.
- Policy-document drafting → `policy-drafter`.

## Approach

Six phases. Phase 1 is the heaviest legally (scope determination), phases 2–4 are the core obligations, phase 5 translates into the NL implementation, phase 6 is the verification-loop.

### 1. Scope determination: essential vs important entity

NIS2 distinguishes two categories with different supervisory regimes:

- **Essential entities (Annex I)**: energy, transport, banks, financial-market infrastructure, health, drinking water, wastewater, digital infrastructure (DNS/TLD/IXP/data centers/cloud), ICT service management business-to-business, public administration, space.
- **Important entities (Annex II)**: post and courier, waste management, chemicals, food, manufacturing (selected sub-sectors), digital providers (online marketplaces, search engines, social networking), research.

Within those, **size caps** apply (Art 2): in principle only medium and large organizations (>50 FTE or >€10M turnover), with exceptions for critical small organizations (DNS providers, TLD registries, trust service providers, etc. are in scope regardless of size).

Reviewer checks:

- Which sector (Annex I/II and sub-code)?
- Size criterion exceeded?
- Qualifies as "providing services in the EU"? A non-EU establishment can still be in scope when it serves EU customers.
- Subsidiaries/holdings: NIS2 works at entity level, not group level. The parent company can be out of scope while a subsidiary is in scope.

Document edge cases with references to specific Annex entries. Ambiguity over essential vs important has real consequences (proactive vs reactive supervision, fine ceilings).

### 2. Governance (Art 20)

Management is liable for cybersecurity. This is a substantial shift from NIS1.

- **Art 20(1)**: the management body must approve cybersecurity risk measures and oversee their compliance.
- **Art 20(2)**: management must take training and employees must receive comparable training.
- Liability: directors can be held personally accountable for gross negligence in cybersecurity. In NL implementation, the exact substance is set via the Cyberbeveiligingswet.

Document requirements for the reviewer:

- A risk-management charter demonstrably approved by the board.
- At least one annual cyber briefing to the board, with agenda items and presentation.
- Security-awareness training for all employees, with a training log.

### 3. The ten baseline measures (Art 21)

NIS2 Art 21(2) lists ten categories of minimum measures. Every in-scope organization must demonstrably address these ten:

1. **Policies on risk analysis and information security** (policy-drafter / risk-register).
2. **Incident handling** (ir-runbook, detection-engineer).
3. **Business continuity** — backups, disaster recovery, crisis management.
4. **Supply-chain security** — including relationships with direct suppliers (vendor-questionnaire, supply-chain).
5. **Security in network and information system acquisition, development, and maintenance** — vulnerability handling (cve-triage, secure-coding, sast-orchestrator).
6. **Policies and procedures for effectiveness evaluation** of cybersecurity measures (audit-evidence).
7. **Basic cyber hygiene** and security-awareness training.
8. **Policies and procedures regarding cryptography**, including encryption where applicable.
9. **Personnel security, access policy, asset management**.
10. **MFA or continuous authentication, secure voice/video/text communication, emergency communication**.

These ten are deliberately framework-agnostic. Mapping to concrete frameworks:

- ISO 27001:2022 Annex A covers all ten.
- NIST CSF 2.0 (Govern/Identify/Protect/Detect/Respond/Recover) covers all ten, with the Govern function as additional coverage for Art 20.
- CIS Controls v8: 18 controls cover the ten themes.

Gap-analysis workflow: per measure name the current state (policy + evidence + gaps), tie to a framework control ID, owner, and deadline.

### 4. Incident reporting (Art 23)

A three-phase timeline for "significant incidents" (apparent impact on service delivery, or exploitation of a third-party vulnerability):

- **24 hours**: early-warning to CSIRT/competent authority. Says whether there is malicious intent or cross-border impact.
- **72 hours**: incident notification with severity + impact assessment + indicators of compromise (as far as known).
- **1 month**: final report with root cause + measures taken + impact.

NL-specific: CSIRT-NL (Computer Security Incident Response Team, under NCSC-NL / Ministerie JenV). Competent authority differs per sector — for most non-government entities supervision falls to the Rijksinspectie Digitale Infrastructuur (RDI) once the Cyberbeveiligingswet enters into force. `[verify the current competent authority per sector]`.

Reviewer workflow for IR runbooks:

- Is there a procedure for the 24h early-warning? Who decides, who drafts?
- Is there a template for the 72h notification with required fields?
- Is there a follow-up discipline for the 1-month report?
- Who trains employees on "this looks like a NIS2 incident, escalate"?

### 5. Dutch implementation: Cyberbeveiligingswet (CBW)

The Cyberbeveiligingswet transposes NIS2 into Dutch law. `[verify current status — at the time this skill was published the legislative track was still in motion; check the parliamentary documents overview at tweedekamer.nl]`. Practical consequences to watch:

- **Registration obligation**: in-scope entities must register with the RDI (for most sectors) or a sector-specific supervisor.
- **Sanctions**: Art 34 of the directive names maximum fines of €10M or 2% of worldwide annual turnover for essential, €7M or 1.4% for important. The CBW operationalizes these.
- **Supervision modes**: essential entities are subject to ex-ante supervision (inspections, audits), important entities ex-post (after a trigger).
- **Information sharing**: the CBW facilitates threat-intel sharing via CSIRT-NL, with an anonymization option.

For verification, consult the current version of the law (wetten.overheid.nl once in force) and, in parallel, NCTV/NCSC-NL publications on implementation guidance.

### 6. Verification-loop

Layer 1: scope (all relevant entities within the organization included? all 10 measures addressed, no silent gaps?), assumptions (Cyberbeveiligingswet status correct as of the report date?), gap analysis (which measures would an auditor consider weakest?). Layer 2: article numbers from directive 2022/2555 correct, no invented Annex entries, NL-specific names (RDI, CSIRT-NL, NCSC-NL, NCTV) correctly spelled and currently scoped, `[verify]` markers in place where legislation is in motion.

## Output

```
NIS2 gap analysis — <organization/entity>
Date: YYYY-MM-DD | NIS2 entered into force: 2024-10-17 | NL CBW status: [verify]

Scope:
  Sector (Annex I/II):    <sector + sub-code>
  Size criterion:         <medium | large | small with exception>
  Classification:         <essential | important | out of scope>
  Rationale:              <1-3 sentences, article references>

Governance (Art 20):
  Board-approved cyber charter:    <yes/no + date>
  Annual board briefing:           <yes/no + last date>
  Awareness training employees:    <coverage%, log present>

Ten baseline measures (Art 21):
  1. Risk analysis + infosec policy:  <state | evidence | gap>
  2. Incident handling:                ...
  3. Business continuity:              ...
  4. Supply-chain security:            ...
  5. Acquisition/development/maintenance: ...
  6. Effectiveness evaluation:         ...
  7. Cyber hygiene + training:         ...
  8. Cryptography:                     ...
  9. Personnel + access + assets:      ...
 10. MFA + secure comms:               ...

Incident reporting (Art 23):
  24h procedure:          <present | gap>
  72h notification:       <template present | gap>
  1-month final report:   <procedure present | gap>
  CSIRT-NL contact:       <registered | pending>

NL implementation:
  RDI registration:       <required + done | n/a>
  Sector supervisor:      <which>
  Sanctions scope:        <max fines per category>

Priorities (fix-now/fix-sprint/fix-quarter):
  <list>

Verification-loop: ...
```

## References

- **EU Directive 2022/2555** (NIS2) — [https://eur-lex.europa.eu/eli/dir/2022/2555](https://eur-lex.europa.eu/eli/dir/2022/2555). Official text, NL language version available via the language selector.
- **ENISA NIS2** — [https://www.enisa.europa.eu/topics/nis-directive](https://www.enisa.europa.eu/topics/nis-directive). Guidance publications and implementation toolkit.
- **NCSC-NL** — [https://www.ncsc.nl/](https://www.ncsc.nl/). National CSIRT plus guidance.
- **NCTV** — [https://www.nctv.nl/](https://www.nctv.nl/). Policy context for NL cybersecurity legislation.
- **Rijksinspectie Digitale Infrastructuur (RDI)** — [https://www.rdi.nl/](https://www.rdi.nl/). Supervisor for several NIS2 sectors.
- **Cyberbeveiligingswet — legislative track** — [https://www.tweedekamer.nl/kamerstukken/wetsvoorstellen](https://www.tweedekamer.nl/kamerstukken/wetsvoorstellen). Search for "Cyberbeveiligingswet" for the most current version.
- **European Commission — NIS2 overview** — [https://digital-strategy.ec.europa.eu/en/policies/nis2-directive](https://digital-strategy.ec.europa.eu/en/policies/nis2-directive).
- **ISO/IEC 27001:2022** — [https://www.iso.org/standard/27001](https://www.iso.org/standard/27001). Mapping target for Art 21 measures.
- **NIST Cybersecurity Framework 2.0** — [https://www.nist.gov/cyberframework](https://www.nist.gov/cyberframework). Alternative mapping basis.

## Categories

- grc
