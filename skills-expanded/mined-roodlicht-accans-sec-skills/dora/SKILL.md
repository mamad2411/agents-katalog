---
name: dora
description: EU Digital Operational Resilience Act (2022/2554) compliance — scope (financial entities + critical ICT TPPs), five pillars (ICT risk management, incident reporting, resilience testing incl. TLPT, third-party risk, information sharing), and Dutch oversight via DNB/AFM.
---

# DORA Compliance

> **Disclaimer**: not legal advice. This skill supports a technical gap analysis against DORA and the underlying Regulatory Technical Standards. Legal qualification (entity classification, contract clauses, sanctions risk) requires financial-law expertise, usually via a compliance department or external counsel.

## When to use

The Digital Operational Resilience Act (EU regulation 2022/2554) has been in force since 17 January 2025. It harmonizes ICT risk management for financial entities in the EU and extends supervision to critical ICT third-party providers. As a regulation (not a directive), DORA applies directly in NL law without an implementation act, although with a national supervision structure (DNB + AFM + ESAs).

Triggers on:

- A question like "DORA gap analysis", "is our entity in scope of DORA", "how do we classify an incident under DORA", "what is a TLPT", "set up a DORA third-party register", "DNB reporting pipeline".
- A financial entity (bank, insurer, investment firm, pension fund, payment institution, crypto-asset service provider, crowdfunding platform, trading venue, etc.) that needs to demonstrate compliance.
- An ICT service provider serving EU financial entities and considering whether it will be designated a "critical ICT third-party provider" by the ESAs.
- A handoff from `iso27001` or `nis2`: DORA replaces NIS2 for financial entities (lex specialis) on most points but not all.
- A security incident where classification and reporting timing must be determined.

### When NOT (handoff)

- General EU cybersecurity for non-financial → `nis2`. Note: in dual-scope cases (e.g. a payment institution that also delivers digital infrastructure) both can apply.
- GDPR/AVG breach notifications → `gdpr-pia`. DORA reporting is additive, not a replacement.
- Technical ICT risk-management implementation → the relevant security skills (`ir-runbook`, `detection-engineer`, `container-hardening`, etc.). DORA demands that you have things; how lives there.
- Threat-Led Penetration Testing execution itself → pentest skills (`recon-agent`, `web-exploit-triage`, `c2-hygiene`, `pentest-reporter`). This skill describes the TLPT regime, not how you run a test.
- Contract-legal review → legal expertise. This skill helps with technical clause mapping (e.g. which exit criteria must be in the contract).

## Approach

Seven phases, one per pillar plus scope determination and the verification-loop.

### 1. Scope determination

DORA Art 2 lists financial entities explicitly: credit institutions, payment institutions, e-money institutions, investment firms, crypto-asset service providers, central securities depositories, central counterparties, trading venues, credit rating agencies, insurers/reinsurers, intermediaries, pension funds, crowdfunding, etc. Plus **critical ICT third-party service providers** (CTPPs) designated by the ESAs.

Reviewer checks:

- Does the organization fall under one of the explicit categories (Art 2(1))?
- Do proportionality exceptions apply (Art 4)? Microenterprises have lighter regimes for some requirements, not all.
- Does the organization deliver ICT services to EU financial entities? Then possibly third-party scope, including possible CTPP designation under the ESA oversight framework.
- Is there overlap with NIS2? In principle DORA applies as lex specialis; see Art 1(2) for the exception. NIS2 keeps applying for the parts not covered by DORA.

### 2. Pillar 1 — ICT Risk Management (Art 5–14)

Governance and framework requirements. Core elements:

- **Art 5 Governance**: the management body is ultimately responsible, must approve the ICT risk-management framework and oversee it, and must have sufficient ICT expertise. Annual review required.
- **Art 6 ICT risk-management framework**: written, approved, roles/responsibilities named, budget allocated, audit trail for decisions.
- **Art 7–9 Identification + protection**: ICT-asset inventory, classification, periodic risk assessment plus on changes, info-security controls (access, segmentation, encryption, data integrity).
- **Art 10–13 Detection + response + recovery**: anomaly detection, logging, incident-response plan, business-continuity plan with RTO/RPO targets, recovery testing, backup strategies.
- **Art 14 Lessons learned**: post-incident review required, findings flow back into the framework.

Mapping: ISO 27001:2022 Annex A largely covers Art 6-13. NIST CSF 2.0 covers the full span. Use your existing framework as a base and map specifically to DORA articles for the gap analysis.

### 3. Pillar 2 — Incident Reporting (Art 17–23)

Three-stage reporting comparable to NIS2, but with its own thresholds and regime:

- **Classification (Art 18)**: a major ICT-related incident when criteria from the RTS are exceeded (number of customers affected, duration, geographic impact, reputational impact, data impact, financial impact). The `[RTS on classification of major ICT-related incidents]` (Commission Delegated Regulation that sets the thresholds): verify the current version.
- **Initial notification**: within **4 hours** of classification as major, and at the latest **24 hours** after first detection of the incident. Different from NIS2 (24h early-warning), shorter.
- **Intermediate report**: within 72 hours of the initial, with more detail.
- **Final report**: within one month, with root cause, impact, and lessons learned.

Reporting goes to the competent authority (NL: DNB for banks/payment institutions/e-money, AFM for trading venues/investment firms/crowdfunding, etc.). The ESAs receive aggregate data.

Additionally: **significant cyber-threat reporting** (voluntary, Art 19). Despite "voluntary" in the text, in practice this is a peer-pressure question: if your peers report, not reporting stands out.

### 4. Pillar 3 — Digital Operational Resilience Testing (Art 24–27)

Two levels:

- **Basic testing (Art 25)**: required for all in-scope entities. Annually, via assessment methodologies: vulnerability assessments/scans, penetration tests, source-code reviews, network security assessments, scenario-based tests. Independent internal or external testers.
- **Threat-Led Penetration Testing (TLPT, Art 26–27)**: required for "significant" entities (designated by the ESAs based on systemic importance + size). Three-yearly testing with red-teaming against production-critical functions. Follows the TIBER-EU framework or equivalent national counterpart (in NL: TIBER-NL under DNB). Testers must be accredited (CREST, CBEST, TIBER-certified).

TLPT process (high level):

1. **Preparation**: scope definition, threat intelligence, test plan, coordination with the national TIBER office.
2. **Testing**: red team performs an attack against production-critical functions, with limited blue-team awareness ("white team" of insiders facilitates).
3. **Closure**: debrief, remediation plan, attestation to the competent authority.

See `recon-agent`, `c2-hygiene`, `post-exploit`, `pentest-reporter` for execution. This skill describes only the regime.

### 5. Pillar 4 — ICT Third-Party Risk Management (Art 28–30)

Probably the most operational impact for most financial entities, because it touches every contract.

- **Art 28 ICT third-party strategy**: a document containing criteria for selection, due diligence, contract management, exit.
- **Art 28(3) Register of information**: a machine-readable register of all contracts with ICT third parties, to be filed with the competent authority. Format standardized via an ITS (Implementing Technical Standard). Contains: provider identification, service description, contract key data, data processed, sub-outsourcing, concentration metrics.
- **Art 29 Pre-contractual assessment**: due diligence on the supplier: risk assessment, data locality, sub-outsourcing chain, concentration risk.
- **Art 30 Contract clauses (mandatory elements)**:
  - Full description of functions + service levels.
  - Location where data is processed plus the provider's locality.
  - Security obligations including notification on incidents.
  - Assistance obligations for ICT incidents at the financial entity.
  - Exit strategies with term and transition support.
  - Access/audit rights for the financial entity and the competent authority.
  - Termination rights under specific circumstances.
- **Critical ICT Third-Party Providers (CTPPs)**: designated by the ESAs. Subject to a direct oversight framework (Art 31+). Both the CTPP and its financial customers have additional obligations.

Workflow for this skill: walk through the contract portfolio, check per contract whether all Art 30 elements are present, build/maintain the register of information, calculate concentration metrics (% of critical functions dependent on one provider).

### 6. Pillar 5 — Information Sharing (Art 45)

Voluntary exchange of cyber-threat information between financial entities, via trusted communities (ISACs). Not required, but explicitly permitted and legally protected: for organizations doubting whether sharing is legally allowed, DORA is the yes answer.

NL ISAC structure: FI-ISAC NL and sector-specific platforms. Operational coupling to threat-intel feeds (see `ioc-hunter`).

### 7. Verification-loop

Layer 1: scope (all in-scope entities included, including the group structure?), assumptions (RTS/ITS versions up to date?), gap analysis (all five pillars addressed without silent exclusions?). Layer 2: article numbers from regulation 2022/2554 correct, RTS/ITS references current (these are updated by the ESAs), NL supervisor split (DNB vs AFM) correct per activity type, TIBER-framework names correct.

## Output

```
DORA compliance assessment — <entity>
Date: YYYY-MM-DD | DORA in force since: 2025-01-17

Scope:
  Entity category (Art 2):   <bank | insurer | ... | CTPP | n/a>
  Proportionality:           <full | lighter — rationale>
  NL supervisor:             <DNB | AFM | n/a>

Pillar 1 — ICT Risk Management:
  Framework document:        <present | gap>
  Board approval + review:   <date + cadence>
  Asset inventory + classif: <coverage%>
  Incident response plan:    <present | gap>
  BCP with RTO/RPO:          <last tested: date | never>

Pillar 2 — Incident Reporting:
  Classification procedure:  <present | gap>
  4h notification pipeline:  <tested | never>
  Authority contact:         <DNB/AFM details on hand>

Pillar 3 — Resilience Testing:
  Annual basic testing:      <last: date, scope>
  TLPT required?:            <yes (significant) | no>
  TIBER-NL trajectory status:<planned | executed | n/a>

Pillar 4 — Third-Party Risk:
  Strategy document:         <present | gap>
  Register of Information:   <complete | gaps: ...>
  Contract clauses Art 30:   <coverage% per element>
  CTPP dependencies:         <list of critical providers>
  Concentration metrics:     <% per critical function>

Pillar 5 — Info Sharing:
  ISAC membership:           <FI-ISAC NL | other | none>
  Threat-intel pipeline:     <active | passive | n/a>

Priorities:
  <fix-now / fix-sprint / fix-quarter with DORA article ref>

Verification-loop: ...
```

## References

- **EU Regulation 2022/2554** (DORA) — [https://eur-lex.europa.eu/eli/reg/2022/2554](https://eur-lex.europa.eu/eli/reg/2022/2554). Primary text.
- **ESAs Joint Committee — DORA implementation** — [https://www.esma.europa.eu/policy-activities/digital-finance/digital-operational-resilience-act-dora](https://www.esma.europa.eu/policy-activities/digital-finance/digital-operational-resilience-act-dora). All RTS/ITS publications collected.
- **DNB — DORA page** — [https://www.dnb.nl/](https://www.dnb.nl/). Search for "DORA" for NL-specific expectations for banks/PSP/EMI.
- **AFM — DORA** — [https://www.afm.nl/](https://www.afm.nl/). For investment firms, trading venues, crowdfunding.
- **TIBER-EU** — [https://www.ecb.europa.eu/paym/cyber-resilience/tiber-eu/html/index.en.html](https://www.ecb.europa.eu/paym/cyber-resilience/tiber-eu/html/index.en.html). Framework for TLPT.
- **TIBER-NL** — [https://www.dnb.nl/voor-de-sector/tiber/](https://www.dnb.nl/voor-de-sector/tiber/). Dutch implementation of TIBER.
- **EBA — DORA** — [https://www.eba.europa.eu/regulation-and-policy/digital-operational-resilience](https://www.eba.europa.eu/regulation-and-policy/digital-operational-resilience). EBA-specific guidance for banks.
- **EIOPA — DORA** — [https://www.eiopa.europa.eu/digital-operational-resilience-act-dora_en](https://www.eiopa.europa.eu/digital-operational-resilience-act-dora_en). For insurers.
- **Register of Information ITS** — `[verify current version via the ESAs website]`. Template and required fields for Art 28(3).

## Categories

- grc
