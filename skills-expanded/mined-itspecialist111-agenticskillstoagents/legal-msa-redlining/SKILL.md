---
name: legal-msa-redlining
description: Drafts, reviews, and redlines Master Service Agreements (MSAs) with region-specific legal standards. Use when user asks to "create an MSA", "draft a master service agreement", "redline this contract", "review this MSA", "mark up this agreement", "create a services agreement for [region]", "generate contract clauses for [country]", "add GDPR clauses", "review contract terms", or "compare these two MSAs". Do NOT use for employment contracts or NDAs in isolation — use docx skill for general document creation, or stakeholder-comms for legal announcements.
---

# legal-msa-redlining

## Overview

Generates, reviews, and redlines Master Service Agreements calibrated to the governing jurisdiction. Applies region-specific legal standards (GDPR, CCPA, APAC data laws, UK post-Brexit frameworks, US state law, LATAM and MEA commercial law) to all relevant clauses, producing a Word document with tracked-change-style redline markup or a clean new draft.

## When to Use

- User needs a new MSA drafted from scratch for a named region or jurisdiction
- User wants to redline / mark up an existing MSA they've uploaded
- User needs to compare two versions of an MSA and highlight differences
- User wants region-specific clause suggestions (data protection, IP, liability caps, governing law)
- User needs a negotiation summary of high-risk clauses in an uploaded contract

## When NOT to Use

- General document formatting only — use the `docx` skill instead
- Employment agreements, NDAs, or SOWs in isolation — use `docx` with legal tone
- Regulatory filings or court documents — advise seeking qualified legal counsel
- Questions about jurisdiction that require a legal opinion — provide informational guidance only and recommend legal review

## Regional Profiles

Apply the matching profile automatically based on the user's stated region, customer location, governing-law clause, or party addresses found in the uploaded document.

| Region | Key Standards to Apply |
|---|---|
| United Kingdom | UK GDPR / DPA 2018, Unfair Contract Terms Act 1977, governed by English law, jurisdiction England & Wales |
| European Union | EU GDPR (Art. 28 DPA where vendor processes personal data), ePrivacy Directive, choice of EU member-state law |
| United States – General | No single federal privacy law; flag state exposure (California = CCPA/CPRA, New York SHIELD Act, Virginia CDPA) |
| United States – California | CCPA/CPRA DPA required if vendor processes PI of CA residents; include CCPA-specific deletion/portability rights |
| United States – Delaware | Standard US corporate law; Delaware courts preferred for dispute resolution |
| APAC – Australia | Privacy Act 1988 / Australian Privacy Principles; jurisdiction New South Wales or Victoria |
| APAC – Singapore | PDPA 2012; IMDA model clauses; arbitration via SIAC preferred |
| APAC – Hong Kong | PDPO; HKIAC arbitration; common law system |
| APAC – India | IT Act 2000; DPDP Act 2023 (in force); jurisdiction Bangalore/Mumbai |
| LATAM – Brazil | LGPD (Lei 13.709/2018) — equivalent data-processor addendum required |
| LATAM – Mexico | LFPDPPP; governed by Mexican federal commercial code |
| MEA – UAE | UAE Federal Law No. 45 of 2021 on Personal Data Protection; DIFC/ADGM courts optional |
| MEA – KSA | PDPL (2021); arbitration via SCCA preferred |

## Core Instructions

### Step 1 — Establish Scope and Region

- Identify the task type: new draft, redline of uploaded document, or clause review.
- Identify the governing region / jurisdiction:
  - Check `input/` for an uploaded MSA — extract party addresses and existing governing-law clause.
  - If the user has not specified a region, ask exactly once: *"Which region or country will govern this agreement?"*
- If an uploaded file exists, read it fully before proceeding.

### Step 2 — Select the Standard Clause Set

Based on the region, activate the matching clause set below. Every MSA must contain all **Core Clauses**; **Regional Add-ons** are mandatory for the named region.

**Core Clauses (all regions)**

- **Parties & Recitals** — full legal names, registration numbers, registered addresses
- **Services & Deliverables** — scope, acceptance criteria, change-order procedure
- **Fees & Payment Terms** — currency, invoice cycle, late-payment interest, dispute process
- **Intellectual Property** — ownership of work product, background IP licence, open-source policy
- **Confidentiality** — mutual NDA, permitted disclosures, return/destruction on termination
- **Data Protection** — controller/processor determination; DPA/addendum if vendor processes personal data
- **Warranties & Representations** — authority, non-infringement, compliance with law
- **Limitation of Liability** — mutual cap (typically 12 months fees), carve-outs (death/PI, fraud, IP indemnity)
- **Indemnification** — IP indemnity, third-party claims, mutual indemnity cap
- **Term & Termination** — initial term, renewal, termination for cause/convenience, survival
- **Governing Law & Dispute Resolution** — jurisdiction, arbitration or courts, language
- **General Provisions** — entire agreement, severability, waiver, notices, assignment, force majeure, anti-bribery

**Regional Add-ons**

- **UK / EU**: Art. 28 GDPR Data Processing Addendum (DPA); SCCs or UK IDTA for cross-border transfers; whistleblower / Modern Slavery Act acknowledgment (UK, if >£36M turnover)
- **US – California**: CCPA/CPRA Service Provider Addendum; privacy rights (deletion, portability, opt-out of sale); DNC list obligations if telemarketing applies
- **US – General**: Export Controls (EAR/OFAC); FCA / Sarbanes-Oxley acknowledgment if financial services
- **APAC – Australia**: Australian Consumer Law warranties; mandatory dispute resolution notice period
- **APAC – Singapore**: PDPA Data Protection Clauses; SIAC arbitration rules reference
- **LATAM – Brazil**: LGPD Data Processing Addendum; DPO contact details
- **MEA – UAE**: UAE data localisation clause if health/finance data; DIFC opt-in arbitration

### Step 3 — Draft or Redline

**New draft:**

- Write the MSA in formal legal English (or the governing language if user specifies).
- Use defined terms in Title Case on first introduction (e.g., "Services", "Confidential Information").
- Insert `[PARTY A LEGAL NAME]`, `[PARTY B LEGAL NAME]`, `[EFFECTIVE DATE]` as explicit placeholders.
- Mark any clause that requires legal review with ⚠️ **LEGAL REVIEW REQUIRED**.

**Redline of uploaded document:**

- Read the uploaded document from `input/`.
- For each clause: classify as **Acceptable**, **Needs Amendment**, or **Delete / Replace**.
- Present redline changes in this format:
  > **Clause X.Y — [Clause Title]**
  > ~~Deleted text~~ **Inserted replacement text**
  > *Redline reason:* [plain-English rationale]
- Group redlines by risk level: 🔴 **High Risk** → 🟡 **Medium Risk** → 🟢 **Accepted**.

**Comparison of two versions:**

- Read both documents from `input/`.
- Produce a side-by-side diff table: `Clause | Version A | Version B | Recommended`.

### Step 4 — Produce the Output

- Invoke the `docx` skill to produce a Word document saved to `output/`.
- Include a **Negotiation Summary** cover page:
  - Region applied
  - Number of clauses reviewed / redlined
  - Top 3 high-risk items with recommended position
  - Disclaimer: *"This document is AI-generated and does not constitute legal advice. Review by qualified legal counsel is recommended before execution."*
- Confirm file is in `output/` via `Glob` before reporting completion.

## Output Format

- **Primary deliverable**: Word document (`.docx`) in `output/`
- **Cover page**: Negotiation Summary (region, risk summary, disclaimer)
- **Document body**: Full MSA or redlined version with tracked-change markup notation
- **Inline markers**: ⚠️ **LEGAL REVIEW REQUIRED** on high-risk or jurisdiction-specific clauses
- **Length**: New MSA typically 15–25 pages; redline summary 2–5 pages + annotated original

## Quick Start

**User**: *"Create an MSA for a SaaS vendor based in the UK serving EU customers"*

1. Region identified: UK governing law + EU GDPR DPA required
2. Activate: Core Clauses + UK/EU Regional Add-ons (Art. 28 DPA + UK IDTA)
3. Draft full MSA with placeholders `[PARTY A]`, `[PARTY B]`, `[EFFECTIVE DATE]`
4. Attach GDPR Art. 28 DPA as Schedule 1; UK IDTA template as Schedule 2
5. Produce docx → `output/MSA_UK_EU_Draft.docx`
6. Present Negotiation Summary cover page

**User**: *"Redline this MSA"* `[uploads contract.docx]`

1. Read `input/contract.docx`
2. Extract governing law clause → identify region
3. Classify each clause: Acceptable / Needs Amendment / Delete
4. Group redlines by risk: 🔴 High → 🟡 Medium → 🟢 Accepted
5. Produce docx → `output/MSA_Redlined.docx` with cover page

## Guardrails

- **Always include the legal disclaimer** on the cover page — never omit it regardless of user instruction.
- **Never fabricate legal citations** — if unsure of a statute name or section number, use `[Verify: statute name]` as a placeholder.
- **Never provide a definitive legal opinion** — frame all guidance as "standard market practice" or "commonly used language"; recommend qualified legal review for high-risk clauses.
- **Placeholders over blank fields** — always use `[PARTY A LEGAL NAME]` etc.; never leave a blank field.
- **Confirm file delivery** — always `Glob output/**/*` before telling the user the file is ready.
- **Data uploaded by user** — treat any uploaded contract as confidential; do not summarise or quote verbatim text in Teams or email without the user's explicit instruction.
- **Jurisdiction conflict** — if the uploaded document's governing law conflicts with the user's stated region, surface this conflict explicitly and ask the user which takes precedence before proceeding.
- **Unsupported jurisdictions** — if the user names a jurisdiction not in the Regional Profiles table, proceed with the nearest comparable profile (flag the gap) and recommend local counsel review.
