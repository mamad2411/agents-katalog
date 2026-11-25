---
name: ai-governance
description: Guides running an AI management system, covering ISO/IEC 42001 (with 42005/42006), NIST AI RMF and its profiles, the AI inventory and risk register, acceptable-use policy, model-vendor assessment, and how it evidences EU AI Act and AI-security duties. Use when the user asks about ISO 42001, NIST AI RMF, an AI policy or inventory, assessing an AI vendor, or AI governance for EU AI Act compliance.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# AI governance (the management-system layer)

This is the layer that decides **who approves an AI system, on what evidence, and how
often it is re-reviewed**. Threats and technical controls are in `load_skill ai-security`.
EU legal duties, roles and dates are in `load_skill eu-ai-act`. This skill is the operating
system that produces evidence for both. Practitioner orientation, not legal advice.

## Pick the anchor (status checked Nov 2026)

| Framework                      | What it is                                                                                                               | Use when                                                   | Status                                                                                                                                                                           |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ISO/IEC 42001:2023**         | Certifiable AIMS requirements: clauses 4 to 10, Annex A controls, Annex B guidance, C objectives/risk sources, D sectors | Customers ask for a certificate; you already run ISO 27001 | 1st edition, no amendment. Implementation guidance ISO/IEC 42003 is at an early work-item stage. verify: https://www.iso.org/standard/42001                                      |
| **ISO/IEC 42005:2025**         | AI system impact assessment guidance (individuals, groups, society)                                                      | Running the 42001 cl. 6.1.4 impact assessment              | Published May 2025. verify: https://www.iso.org/standard/42005                                                                                                                   |
| **ISO/IEC 42006:2025**         | Requirements for bodies auditing/certifying an AIMS (with ISO/IEC 17021-1)                                               | Choosing a certifier                                       | Published Jul 2025. verify: https://www.iso.org/standard/42006                                                                                                                   |
| ISO/IEC 23894:2023, 38507:2022 | AI risk-management guidance (ISO 31000 applied); board-level governance of AI use                                        | Risk method; board oversight wording                       | Stable                                                                                                                                                                           |
| **NIST AI RMF 1.0** (AI 100-1) | Voluntary: Govern / Map / Measure / Manage, plus Playbook                                                                | US customers, federal work, US state-law references        | **Revision in progress** (directed by the Jul 2025 AI Action Plan); no draft published. Formal review due by 2028. verify: https://www.nist.gov/itl/ai-risk-management-framework |
| NIST AI 600-1                  | Generative AI Profile: 12 GAI risks + actions                                                                            | GenAI use cases                                            | Final, Jul 2024                                                                                                                                                                  |
| NIST IR 8596 Cyber AI Profile  | CSF 2.0 profile: Secure / Defend / Thwart                                                                                | Bringing AI into a CSF programme (`load_skill nist-csf`)   | Preliminary draft only (Dec 2025; comments closed 30 Jan 2026); initial public draft still pending. verify: https://csrc.nist.gov/pubs/ir/8596/iprd                              |
| SP 800-53 AI overlays          | Control overlays (predictive, generative, agentic, developer)                                                            | Federal / 800-53 shops                                     | Annotated outlines only (Jan 2026); first public draft planned 2026 to early 2027. Project **renamed COSAiS → COSIS**. verify: https://csrc.nist.gov/projects/cosis              |

- **"Super Intelligence" is a relabel, not new scope.** EO 14434 (29 Sep 2026) has US agencies say
  "SI" in place of "AI" in non-statutory material, keeping the 15 U.S.C. 9401(3) definition. NIST
  pages are being renamed; obligations are not. verify: https://www.whitehouse.gov/wp-content/uploads/2026/09/eo-14434.pdf
- Usual pairing: **42001 as the management system**, NIST AI RMF/600-1 as the risk vocabulary, `ai-security` for controls.

## Build the AIMS (ISO 27001-shaped: run it as one integrated system)

- **Cl. 4 to 5:** your **role** per system (developer, provider, customer/user, partner); a scope
  statement naming the AI systems covered; AI policy (A.2) and accountability (A.3) under an exec
  owner, with the AI committee in the existing governance cadence (`load_skill security-governance`).
- **Cl. 6:** AI risk assessment and treatment (6.1.2 to 6.1.3) produce a **Statement of
  Applicability** against Annex A. The **AI system impact assessment** (6.1.4, method in 42005) is the piece unique to 42001: it covers harm to people, not only to the company.
- **Cl. 7 to 10:** resources (A.4); competence and AI literacy (AI Act Art. 4, live since Feb 2025 and softened by the AI Omnibus, Regulation (EU) 2026/1744, in force 27 Jul 2026: providers and deployers must take measures to support AI literacy but need not guarantee any level; the same omnibus moved Annex III high-risk duties to 2 Dec 2027 and adds an Art. 5 ban on non-consensual intimate imagery and CSAM generation from 2 Dec 2026;
  `load_skill security-awareness`); operation, audit, management review. Share these with the ISMS,
  not a parallel system: one audit programme, two SoAs (`load_skill iso27001`, `load_skill compliance-audit`).
- **Annex A**: 38 controls in 9 areas, A.2 to A.10 (policies, internal organisation, resources,
  impact assessment, lifecycle, data, information for interested parties, use, third
  parties). Cite control IDs; don't paste standard text into policies.
- **Certification:** Stage 1/2, then a 3-year cycle with surveillance audits. Check the certifier is
  **accredited for 42001** by an IAF-member body (unaccredited "certificates" are common), and read
  the scope: a certificate covering one internal chatbot is often marketed as company-wide.

## AI system inventory (the backbone)

Without an inventory nothing else works. One row per system/use case, in `/work/ai-inventory.md`:

| ID  | System / use case | Business + tech owner | Decision or action supported | Our role (build/fine-tune/buy/embedded) | Model + version + provider | Data classes | Autonomy (advise/HITL/act) | Tools & actions | Affected people + jurisdictions | AI Act tier + role | Internal tier | Last impact assessment | SoA / control refs |
| --- | ----------------- | --------------------- | ---------------------------- | --------------------------------------- | -------------------------- | ------------ | -------------------------- | --------------- | ------------------------------- | ------------------ | ------------- | ---------------------- | ------------------ |

- **Where to find it:** procurement/expense data, SSO/OAuth grants, CASB/proxy logs for AI
  domains, model-API billing, code search for SDK imports, browser extensions, and **AI
  features switched on in SaaS you already run** (the biggest blind spot). A row with no
  owner is a finding (`report_finding`).

## Risk register and impact assessment

- **Two lenses, one register:** risk _to the organisation_ (6.1.2, scored like any risk:
  `load_skill risk-assessment`) and impact _on people_ (6.1.4/42005: discrimination, safety,
  privacy, lost opportunity). A system can be low risk to you and high impact on them.
- **Tier by consequence:** decisions about people (hiring, credit, health, access) → high; then
  autonomy, data sensitivity, scale, reversibility. High tier needs an impact assessment, an
  oversight design, a pre-launch adversarial test (red-team / adversarial testing) and committee sign-off.
- **Re-assess on:** a provider model/version change (often silent, so pin versions), a new data
  source, tool or user population, an incident, or a drift alert. Personal data also means a
  DPIA: run it jointly with the impact assessment, not twice (`load_skill privacy-engineering`).

## Acceptable-use policy (workforce)

- **Sanctioned-tool tiers:** approved for confidential data (enterprise terms, no training on
  inputs, retention set) / public data only / prohibited. Banning everything drives use into
  unmonitored personal accounts. Data rules follow classification (`load_skill data-security`).
- **The user owns the output** (verify before relying; disclose AI use where Art. 50 applies).
  **Prohibited:** Art. 5 practices, decisions about people without an approved process,
  impersonation/deepfakes, agents wired to email/payments/prod without review (`load_skill ai-security`).
- A reporting path for AI misbehaviour, wired into IR (`load_skill breach-notification-matrix`).

## Third-party / model vendor assessment

Add these AI asks to `load_skill third-party-risk`:

- **Data use:** are inputs/outputs used for training? Retention, zero-retention option,
  regions, sub-processors (model developer vs hosting provider).
- **Model change:** model/system card, version pinning, advance notice of model swaps and deprecation.
- **Evidence:** evals (safety, bias, robustness), red-team summary, prompt-injection mitigations,
  tenant isolation, logs you can get, an incident SLA covering AI failures. For GPAI, the AI Act
  downstream docs and Code of Practice status. Certificates count only with the AI service **in scope**.
- **Contract:** no-training clause, output IP indemnity, audit rights, and **who is AI Act
  provider** if you fine-tune or rebrand (`load_skill legal-contractual`). Re-tier a vendor
  when it launches an AI feature in a product you already use.

## Mapping the AIMS to the EU AI Act and to security

| AI Act duty                                             | AIMS artefact that evidences it                                                 |
| ------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Art. 4 literacy, Art. 5 prohibitions (both live)        | Cl. 7.2/7.3 competence records; AUP + inventory screening at intake             |
| Art. 9 risk management (high-risk)                      | 6.1 risk process + 42005 impact assessment, done **per system**                 |
| Art. 10 data, Art. 11 to 12 tech docs and logging       | A.7 data controls; A.6 lifecycle documentation and event logs                   |
| Art. 13 / 50 transparency, Art. 14 human oversight      | A.8 information for interested parties; A.9 use of AI systems                   |
| Art. 15 accuracy, robustness, cybersecurity             | `ai-security` controls + ISMS (`load_skill control-mapping`)                    |
| Art. 17 QMS                                             | The AIMS itself. **EN 18286** is the only harmonised standard cited (QMS)       |
| Art. 27 deployer FRIA                                   | 42005-style impact assessment                                                   |
| Art. 72 to 73 post-market monitoring, serious incidents | Cl. 9.1 monitoring + incident process (`load_skill breach-notification-matrix`) |

- **42001 certification gives no presumption of conformity with the AI Act.** It is the
  machinery that generates the evidence; conformity is still per system.
- **US hooks (verify):** Colorado SB 24-205 (with its NIST AI RMF/ISO 42001 affirmative defence)
  never took effect. SB 26-189 (signed 14 May 2026, effective 1 Jan 2027) replaced it with a narrower
  ADMT notice-and-explain regime. Federal agencies run AI inventories under OMB M-25-21.

## Operate and measure

- **Intake gate:** no AI reaches production without an inventory row, a tier and that tier's
  artefacts; exceptions go through normal risk acceptance. Security, privacy, legal and HR co-own it.
- **Metrics** (`load_skill security-metrics`): % of inventory with owner and tier; % of high-tier
  systems with a current impact assessment; shadow-AI finds/month; overdue vendor AI reviews.
- File governance gaps with `report_finding` so they land in `render_report` with the technical findings.
