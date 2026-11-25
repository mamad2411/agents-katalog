---
name: privacy-policy-generator
description: |
  Generates jurisdiction-aware privacy policies mapped to GDPR, CCPA/CPRA,
  UK GDPR, LGPD, PIPEDA, COPPA and sector overlays, with a compliance
  matrix, cookie disclosures, and DSAR implementation checklist. Use when
  a user says "write a privacy policy for my SaaS", "I need a GDPR
  privacy policy", "update our CCPA disclosures", "what should my
  privacy policy say about cookies", or "draft privacy compliance docs
  for my app". For privacy/data-protection policies specifically, not
  general terms of service — see terms-conditions-drafter for ToS. AI-
  assisted draft only, not legal advice.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="privacy-policy-generator")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including known business model, prior data practices disclosed, jurisdictional requirements, and any previously generated policies that need revision.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Business overview**: What product or service does the business offer? (SaaS, e-commerce, mobile app, marketplace, content platform, etc.)
- **Data subjects**: Who are the end users? Describe the ICA — consumers, enterprise employees, minors, healthcare patients, etc.
- **Data inventory**: What categories of personal data are collected? (identifiers, financial, biometric, geolocation, browsing behaviour, user-generated content, device data)
- **Collection methods**: How is data collected? (forms, cookies/trackers, SDKs, APIs, third-party integrations, offline)
- **Third-party sharing**: Are any data processors, analytics providers, ad networks, or affiliates receiving personal data?
- **Jurisdictions**: Where are users located and where is the business incorporated? (EU/EEA, California, UK, Canada, Brazil, Australia, etc.)
- **Special circumstances**: Any sector-specific regulation? (HIPAA, COPPA, FERPA, PCI-DSS, PIPEDA, etc.)
- **Existing policy**: Share any current privacy policy for gap analysis, or confirm this is a net-new draft.

If FutureProof context already contains answers to any of the above, confirm them with the user rather than re-asking.

## Step 3: Do the Work

### 3A: Regulatory Framework Mapping

Identify all applicable regulatory frameworks based on disclosed jurisdictions and data types:

| Framework | Applicability Test | Key Obligations |
|---|---|---|
| **GDPR** (EU/EEA) | Data subjects in EU/EEA or establishment in EU | Lawful basis, DPIA, DPO, cross-border transfer safeguards, Art. 13/14 disclosures |
| **UK GDPR + DPA 2018** | UK data subjects or UK establishment | Mirrors GDPR with ICO-specific guidance |
| **CCPA/CPRA** (California) | Revenue >$25M, 100K+ consumers, or 50%+ revenue from selling data | Right to know, delete, opt-out of sale/sharing, sensitive PI disclosures |
| **LGPD** (Brazil) | Processing data of individuals in Brazil | Lawful basis, DPO appointment, ANPD registration |
| **PIPEDA** (Canada) | Commercial activity in Canada | Consent principles, breach notification to OPC |
| **COPPA** (US) | Actual knowledge of users under 13 | Verifiable parental consent, data minimisation |
| **Sector-specific** | HIPAA, FERPA, PCI-DSS, ePrivacy Directive | Layer sector requirements on top of general framework |

Flag any cross-border data transfer mechanisms required (SCCs, BCRs, adequacy decisions, APEC CBPR).

### 3B: Clause-by-Clause Drafting

Draft each section using precise, plain-language disclosure that satisfies the strictest applicable framework while remaining comprehensible to the ICA:

1. **Identity & Contact Details of the Controller** — legal entity name, registered address, DPO or privacy contact email
2. **Data We Collect** — itemised table of data categories, specific data elements, and whether each is mandatory or optional
3. **How We Collect Your Data** — direct collection, automated collection (cookies, pixels, device fingerprinting), and third-party sources
4. **Purposes & Lawful Basis** — each processing purpose mapped to its GDPR lawful basis (consent, contract, legitimate interest, legal obligation) and/or CCPA business purpose category
5. **Cookies & Tracking Technologies** — categorised cookie table (strictly necessary, functional, analytics, advertising) with names, providers, durations, and opt-out mechanisms
6. **Third-Party Sharing & Disclosures** — named categories of recipients, purpose of sharing, and whether sharing constitutes a "sale" or "sharing" under CPRA
7. **International Data Transfers** — destination countries, transfer mechanisms, and how to obtain copies of safeguards
8. **Data Retention** — retention periods per data category with rationale (contractual necessity, statutory obligation, legitimate interest balancing test)
9. **Your Rights** — jurisdiction-specific rights matrix (access, rectification, erasure, portability, restriction, objection, opt-out of sale, non-discrimination) with exercise mechanisms
10. **Children's Privacy** — age thresholds, verification mechanisms, and parental consent procedures (if applicable)
11. **Security Measures** — technical and organisational measures (encryption standards, access controls, incident response) at appropriate disclosure level
12. **Automated Decision-Making & Profiling** — disclosure of any algorithmic processing with meaningful information about logic, significance, and envisaged consequences (Art. 22 GDPR)
13. **Policy Updates** — versioning protocol, notification method, and effective date mechanism
14. **Contact & Complaints** — internal contact, supervisory authority details (with specific DPA identified), and escalation path

### 3C: Compliance Cross-Check

Validate the draft against a 12-point compliance audit:

1. All Art. 13/14 GDPR mandatory disclosures present
2. CCPA §1798.100–199 notice-at-collection requirements satisfied
3. Lawful basis specified for every processing purpose (no blanket "legitimate interest" without balancing test documentation)
4. Retention periods are specific (not "as long as necessary" without qualification)
5. Third-party recipients identified by category with adequate specificity
6. Cookie disclosures align with ePrivacy Directive / PECR requirements
7. Cross-border transfer safeguards documented
8. Rights exercise mechanisms are actionable (not just "contact us")
9. Plain language readability — target Flesch-Kincaid grade level ≤ 10
10. Consistent terminology throughout (no switching between "personal data" and "personal information" without jurisdiction-specific context)
11. Sector-specific overlays properly integrated (HIPAA BAA references, COPPA verifiable consent, etc.)
12. Version number, effective date, and last-reviewed date included

Apply any user-specific `instructions` from FutureProof context (e.g., brand voice guidelines, preferred legal counsel review workflow, prior regulatory feedback).

## Step 4: Deliver Output

Produce the following structured deliverables:

### Deliverable 1: Privacy Policy (Full Draft)
- **Format**: Markdown document with clear heading hierarchy (H2 sections, H3 subsections)
- **Naming convention**: `privacy-policy_[company-name]_v1.0_[YYYY-MM-DD].md`
- **Ready for**: Legal counsel review → website/app publication
- **Includes**: Table of contents, effective date, version number, and jurisdiction badges at the top

### Deliverable 2: Compliance Matrix
- **Format**: Table mapping each policy section to the specific regulatory article/section it satisfies
- **Columns**: Policy Section | GDPR Article | CCPA/CPRA Section | Other Applicable Law | Status (✅ Addressed / ⚠️ Needs Legal Review / ❌ Gap)
- **Purpose**: Provides legal counsel with an audit trail for review efficiency

### Deliverable 3: Implementation Checklist
- **Format**: Actionable task list for the user's team
- **Includes**:
  - Cookie consent mechanism implementation (CMP recommendation)
  - Data subject access request (DSAR) workflow setup
  - Internal record of processing activities (ROPA) template reference
  - DPO appointment or privacy contact designation
  - Staff training requirements
  - Review cadence recommendation (quarterly for high-risk, bi-annually minimum)

### Deliverable 4: Gap Summary (if existing policy was provided)
- **Format**: Side-by-side comparison table
- **Columns**: Existing Clause | Issue Identified | Recommended Revision | Regulatory Risk Level (High/Medium/Low)

**Disclaimer**: Include a clear notice that the output constitutes an AI-assisted draft and does not constitute legal advice. Recommend review by qualified privacy counsel before publication, particularly for high-risk processing activities.

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Propose Experiments

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


```
FutureProof:save_experiment(skill="privacy-policy-generator", experiment={
  hypothesis: "Restructuring the privacy policy with a layered-notice approach (short-form summary + full policy) increases user comprehension and reduces support enquiries about data practices",
  variants: ["control: single long-form policy", "variant: layered notice with expandable sections and plain-language summary header per section"],
  measurement: "User comprehension score via post-read survey, support ticket volume related to privacy questions over 90 days",
  expected_impact: "30% reduction in privacy-related support enquiries and improved consent quality metrics"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="privacy-policy-generator",
  query="Latest privacy regulatory enforcement actions, emerging state-level US privacy laws (2024-2025), and updated EDPB/ICO guidance on AI-specific transparency obligations and cookie consent best practices",
  reason="Ensure generated policies reflect current enforcement priorities, newly effective legislation (Texas TDPSA, Oregon CPA, Montana CDPA), and evolving AI transparency requirements under the EU AI Act"
)
```

## Step 7: Save Session

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:save_session(skill="privacy-policy-generator", session={
  summary: "...[fact-dense: ICA, format, tone, constraints, what was delivered, amends made. End with: Next session defaults: ...]",
  outcomes: [
    "Format: [format chosen]",
    "Tone: [tone and constraints]",
    "ICA: [ICA description]",
    "Deliverable: [what was produced]"
  ],
  metadata: {}
})
```