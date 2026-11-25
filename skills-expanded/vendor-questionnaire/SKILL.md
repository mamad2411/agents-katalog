---
name: vendor-questionnaire
description: Vendor security questionnaire workflow — vendor tiering, standardized questionnaires (CAIQ, SIG-Lite/Core, VSA), custom authoring, evidence reuse against existing attestations (SOC 2, ISO 27001), and ongoing vendor-risk monitoring.
---

# Vendor Security Questionnaire

> **Disclaimer**: this skill supports a security assessment of vendors. Contractual and legal review (data-processing agreements, liability clauses, jurisdiction) requires legal. This skill does not replace contract-legal expertise.

## When to use

Vendor Security Questionnaires are the standard mechanism organizations use to assess the security posture of their third-party providers. From both sides: you send them (as the buyer) AND receive them (as a provider serving B2B customers). This skill covers both roles.

Triggers on:

- A question like "which questionnaire do we use for this vendor", "fill out this SIG-Lite for customer X", "build CAIQ answers", "what is a reasonable questionnaire for a low-risk SaaS", "evidence reuse across questionnaires".
- A new vendor onboarding (sender side).
- An incoming security questionnaire from a customer (receiver side).
- A handoff from `supply-chain` (SBOM side), `dora` (Art 28-30 third-party risk), `nis2` (Art 21(4) supply-chain security), `policy-drafter` (vendor management policy).
- Annual re-review of existing vendors.

### When NOT (handoff)

- Contract drafting or legal review → legal team. This skill provides input for contracts, not contracts themselves.
- Policy layer of vendor management → `policy-drafter`.
- Technical dep/supply-chain evaluation (SBOM, provenance) → `supply-chain`. Complementary.
- Risk-scoring methodology → `risk-register`.
- Compliance-specific attestation production → `iso27001`, `soc2`, `audit-evidence`.
- Privacy-specific vendor assessment (sub-processors under AVG Art 28) → `gdpr-pia` context plus DPA review.
- Fraud / financial due diligence → out of scope, financial-controlling expertise.

## Approach

Seven phases. Phase 1 (tiering) decides all subsequent steps; phase 4 (evidence reuse) is where efficiency gains live.

### 1. Vendor tiering

Not every vendor receives the same attention. Tier sets the depth of due diligence.

**Tier criteria** (multi-dimensional):

- **Data access**: which data is processed (PII? Financial? Special categories Art 9 AVG?)?
- **System access**: does the vendor have access to production systems, admin roles, source code?
- **Business criticality**: how long do we survive an outage of this vendor?
- **Regulatory scope**: is this vendor part of a NIS2/DORA-subject chain?

**Tier definitions** (3-tier example):

- **Tier 1 (critical)**: touches PII or production, essential for core operations, regulatory-subject. Full questionnaire + SOC 2/ISO 27001 evidence required + annual review + on-site/remote audit rights.
- **Tier 2 (moderate)**: limited data exposure or moderate business impact. Mid-size questionnaire (SIG-Lite or CAIQ-Lite), attestation evidence sufficient, biennial review.
- **Tier 3 (low)**: no PII, no production access, replaceable. Lightweight questionnaire (10-20 questions), evidence optional, triennial review.

Document the tiering criteria as part of the Vendor Management Policy (see `policy-drafter`).

### 2. Standardized frameworks

Use existing frameworks where possible; building custom is expensive and double work.

- **CAIQ (Consensus Assessments Initiative Questionnaire)** — Cloud Security Alliance. 261 questions (v4.0.3) aligned with the Cloud Controls Matrix (CCM). Strongest for cloud service providers. Freely available.
- **SIG / SIG-Lite / SIG-Core (Standardized Information Gathering)** — Shared Assessments. SIG-Lite ~300 questions, SIG-Core ~1500, full SIG ~3000. Broadly applicable, commercial license for the full version.
- **VSA (Vendor Security Alliance)** — VSAQ (core) + VSAQ-full. Compact alternative aimed at modern SaaS.
- **NIST SP 800-171 self-assessment** — for vendors handling US-federal/DoD data (CUI).
- **CRA assessment** — expected role of vendors under the EU Cyber Resilience Act for software-product security.

Selection heuristic: if the vendor offers a framework themselves ("here is our completed CAIQ + SOC 2 report"), accept that first. Custom questionnaire only when existing frameworks really have gaps for your context.

### 3. Custom-questionnaire authoring (only when needed)

For organization-specific questions outside the standard frameworks. Keep it limited to the truly unique.

- **Top-level clustering**: governance, identity/access, data protection, ops/monitoring, incident response, supply chain, compliance, continuity.
- **Question phrasing**: closed questions with an evidence request (e.g. "Do you enforce MFA for admin access? [Y/N]. If yes, provide evidence screenshot/policy reference"), not open essays ("Please describe your security").
- **Length**: tier-dependent. Tier 1 can be 100+ questions; tier 3 not more than 20. Vendor fatigue is real.
- **Language**: NL or EN, not both (see `policy-drafter` phase 4).

Custom questionnaires must be a stable, versioned document, not an ad-hoc variant per vendor.

### 4. Evidence mapping and reuse

Most of the value in modern-day vendor security is in **not answering the same questions over and over**.

- **Attestation-first**: if a vendor has SOC 2 Type II or ISO 27001, ask for those reports first. Mapping table: CAIQ question X maps to SOC 2 CC6.1 control. Answer: "See attached SOC 2 report, section CC6.1, evidence in Appendix".
- **Cross-walks**:
  - CAIQ ↔ CCM ↔ ISO 27001 Annex A: CSA publishes the mappings.
  - SIG ↔ ISO 27001: Shared Assessments publishes them.
  - NIST CSF ↔ ISO 27001: many cross-walks publicly available.
- **Evidence library** (as receiver): maintain a structured repository with evidence per control type. New incoming questionnaire: 80% of answers come from the library, 20% are query-specific.
- **Trust centers / SafeBase / Whistic / VendorSPT**: publicly accessible portals where you host your attestations, SBOMs, and policy overviews for customers. Lowers incoming-questionnaire load. Standard for mature B2B SaaS.
- **CAIQ-based STAR** (CSA): public registry of CAIQ-completed vendors. Check before sending a custom questionnaire.

Missing evidence for a specific question is itself a finding: the vendor claims "yes" but cannot back it up.

### 5. Review + risk acceptance

After answers come in:

- **Red-flag pass**: auto-disqualifiers. No MFA on admin, no encryption-at-rest for PII, no incident-response plan, no breach-notification clause. Vendors that fail here are not negotiable unless the business case is huge and the risk is explicitly accepted.
- **Scoring**: tier-adjusted scoring. Tier 1 with gaps = go back to the vendor with a remediation request. Tier 3 with minor gaps = acceptable with compensating controls.
- **Risk acceptance**: if gaps remain, document in `risk-register` with an explicit accept decision, owner, deadline for re-review.
- **Contract clauses** that follow from the questionnaire: breach-notification timeline, right to audit, data-residency guarantee, sub-processor-approval chain, exit procedure with data return/destruction. Specifically required for DORA Art 30 for financial entities.
- **Complementary User Entity Controls (CUECs)**: which controls does the vendor count on you for? Document and communicate internally (see `soc2` phase 5).

### 6. Ongoing monitoring

A one-shot vendor assessment is not enough. Vendors change; risk exposure with them.

- **Re-assessment cadence** per tier (annual tier 1, biennial tier 2, triennial tier 3).
- **Event triggers**: incident at the vendor (public breach), significant organizational change, contract renewal, change in data scope.
- **Continuous monitoring tools**: BitSight, SecurityScorecard, Panorays, UpGuard. They produce outside-in risk ratings (DNS config, cert hygiene, leaked credentials, patch cadence). Not a replacement for the questionnaire but a red-flag detector between formal reviews.
- **Register**: aligned with DORA Art 28(3) register of information for financial entities (filed with DNB/AFM), or equivalent for non-financial.

### 7. Verification-loop

Layer 1: scope (all tier-1 vendors assessed, no shadow-IT vendors via P-card forgotten?), assumptions (vendor attestations still valid, not expired?), gaps (sub-processors mapped, not just the top-level vendor?). Layer 2: framework version numbers (CAIQ v4.0.x, SIG year) correct, cross-walk claims supported by CSA/Shared-Assessments publications, no invented SOC 2 mapping codes, contract-clause terminology technical and not legally over-reaching.

## Output

Two modes: sender (send a questionnaire + review answers) or receiver (answer an incoming questionnaire).

**Sender mode**:

```
Vendor security assessment — <vendor>
Tier: <1 | 2 | 3> | Onboarding date: <...> | Last review: <...>

Questionnaire:
  Framework:          <CAIQ v4 | SIG-Lite | custom>
  Sent:               <date>
  Received:           <date, N answers>

Attestations:
  SOC 2 Type II:      <present, period, issuer>
  ISO 27001:          <present, scope, expiry>
  Other:              <DORA CTPP, FedRAMP, ...>

Findings:
  Red flags:          <list, blocker for onboarding?>
  Gaps (non-blocker): <list with compensating controls or acceptance>
  Evidence gaps:      <claims without evidence>

Contract clauses (aligned with findings):
  Breach notification:<timing>
  Right to audit:     <scope>
  Data residency:     <region lock>
  Sub-processor:      <approval chain>
  Exit:               <return/destruction procedure>

Decision:
  Onboard:            <yes | with conditions | no>
  Risk accepted:      <register-ID in risk-register>

Verification-loop: ...
```

**Receiver mode**: a structured answer package with references to evidence-library items, cross-walked to the requested framework codes.

## References

- **CSA CAIQ** — [https://cloudsecurityalliance.org/research/cloud-controls-matrix](https://cloudsecurityalliance.org/research/cloud-controls-matrix). CAIQ + CCM, freely downloadable, cross-walks to other frameworks.
- **CSA STAR Registry** — [https://cloudsecurityalliance.org/star/registry](https://cloudsecurityalliance.org/star/registry). Public registry of CAIQ-completed providers.
- **Shared Assessments SIG** — [https://sharedassessments.org/sig/](https://sharedassessments.org/sig/). SIG family questionnaires, commercial.
- **Vendor Security Alliance** — [https://www.vendorsecurityalliance.org/](https://www.vendorsecurityalliance.org/). VSAQ-core and VSAQ-full.
- **NIST SP 800-171** — [https://csrc.nist.gov/pubs/sp/800/171/r3/final](https://csrc.nist.gov/pubs/sp/800/171/r3/final). For CUI-handling assessment.
- **EU Cyber Resilience Act** — [https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act](https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act). Relevant for vendor assessment of software products once it enters into force.
- **NIST SP 800-161 Rev. 1** — [https://csrc.nist.gov/pubs/sp/800/161/r1/final](https://csrc.nist.gov/pubs/sp/800/161/r1/final). Cybersecurity Supply Chain Risk Management practices.

## Categories

- grc
