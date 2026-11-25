---
name: terms-conditions-drafter
description: |
  Drafts publication-ready Terms & Conditions and Terms of Service across
  a 16-clause architecture covering acceptance mechanism, fees and auto-
  renewal, AUP, liability caps, arbitration, and class-action waivers,
  with an enforceability and risk scorecard. Use when a user says "draft
  terms of service for my SaaS", "write T&Cs for my marketplace", "help
  me write terms of service for my mobile app", or "update our website
  terms". For ToS/T&Cs of the user's own product, not privacy disclosures
  (see privacy-policy-generator) or review of inbound contracts (see
  contract-review-assistant). Informational guidance, not legal advice.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="terms-conditions-drafter")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly prior business model details, jurisdiction preferences, known risk exposures, and ICA characteristics that inform readability and tone calibration.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Business model & offering**: What product, service, or platform are these terms governing? (e.g., SaaS subscription, e-commerce marketplace, digital course, mobile app, API service)
- **Jurisdiction(s)**: Primary operating jurisdiction and any secondary jurisdictions where the ICA is based (e.g., US/Delaware, UK, EU/GDPR-scope, Australia)
- **ICA profile**: Who is the end user accepting these terms? (consumer, SMB, enterprise, mixed) — this determines language complexity, enforceability posture, and disclosure obligations
- **Existing terms**: Share any current Terms & Conditions, prior legal drafts, or competitor terms they are modelling from
- **Specific concerns**: Are there known risk areas to address? (e.g., refund/chargeback exposure, user-generated content liability, data processing, SLA commitments, IP assignment)
- **Tone & readability preference**: Formal legal prose, plain-language consumer-friendly, or hybrid (legal backbone with plain-language summaries)?

## Step 3: Do the Work

### 3A: Regulatory & Jurisdictional Framework Mapping

Identify the applicable legal framework stack based on user inputs:
- **Consumer protection**: CAN-SPAM, FTC Act Section 5, Australian Consumer Law, EU Consumer Rights Directive, UK Consumer Rights Act 2015 — as applicable
- **Data & privacy**: GDPR, CCPA/CPRA, PIPEDA, APP — map required disclosures and cross-reference to a separate Privacy Policy where appropriate
- **Electronic contracting**: E-SIGN Act, eIDAS Regulation, Electronic Transactions Acts — ensure enforceability of click-wrap/browse-wrap acceptance mechanism
- **Industry-specific**: PCI-DSS references (payments), HIPAA BAA triggers (health data), COPPA (minors), DMCA safe harbour (user-generated content)

Flag any jurisdictional conflicts or heightened-risk combinations (e.g., consumer ICA + subscription model + EU jurisdiction triggers enhanced cancellation and refund obligations).

### 3B: Clause-by-Clause Drafting Framework

Draft the Terms & Conditions using the following structured clause architecture, tailored to the user's business model:

1. **Definitions & Interpretation** — define all capitalised terms; ensure "User," "Service," "Content," and "Account" are scoped precisely to the offering
2. **Acceptance Mechanism & Eligibility** — click-wrap vs. browse-wrap enforceability posture; age/capacity restrictions; authority to bind (for enterprise ICA)
3. **Scope of Service & Service Description** — what the user is and is not providing; feature availability; beta/preview disclaimers
4. **Account Registration & Security** — user obligations for credential security; multi-user account provisions; account termination triggers
5. **Fees, Billing & Payment Terms** — pricing structure, billing cycles, auto-renewal disclosures (state-specific auto-renewal compliance: CA ARL, NY GBL §527-a), currency, taxes, failed payment procedures
6. **Refund & Cancellation Policy** — statutory cooling-off periods (EU 14-day right of withdrawal), discretionary refund terms, pro-rata vs. no-refund posture, chargeback handling
7. **Acceptable Use Policy** — prohibited conduct enumeration; rate limiting/abuse thresholds; enforcement ladder (warning → suspension → termination)
8. **Intellectual Property** — ownership of platform IP; licence grant to user; user-generated content licence-back (scope, duration, sublicensability); DMCA/notice-and-takedown procedure
9. **Data Handling & Privacy** — cross-reference to Privacy Policy; data processing roles (controller/processor); data portability and deletion commitments
10. **Third-Party Services & Integrations** — disclaimer of liability for third-party tools; pass-through terms; API usage constraints
11. **Disclaimers & Limitation of Liability** — warranty disclaimers (AS-IS/AS-AVAILABLE); liability cap (fees paid in trailing 12 months or alternative); consequential damages exclusion; carve-outs for gross negligence, fraud, and statutory non-excludable rights
12. **Indemnification** — user indemnification obligations; scope (claims arising from user content, breach of AUP, third-party IP infringement); procedural controls (notice, cooperation, sole defence)
13. **Term, Termination & Suspension** — termination for convenience vs. cause; effect of termination (data retention/deletion timeline, surviving clauses); suspension rights for non-payment or AUP breach
14. **Dispute Resolution** — governing law; mandatory arbitration vs. litigation; arbitration provider and rules (AAA, JAMS, ICC); class action waiver (enforceability-aware); small claims court carve-out; pre-arbitration negotiation period
15. **Modification of Terms** — notice mechanism (email, in-app, website posting); deemed-acceptance vs. opt-out framework; material change definition
16. **General Provisions** — severability, entire agreement, assignment, force majeure, waiver, notices

### 3C: Risk & Enforceability Audit

Evaluate the drafted terms against five enforceability and risk dimensions:

| Dimension | Assessment Criteria |
|---|---|
| **Enforceability robustness** | Acceptance mechanism strength; unconscionability risk; compliance with jurisdiction-specific formation requirements |
| **Regulatory compliance** | Alignment with mapped regulatory stack from Step 3A; disclosure completeness; auto-renewal law compliance |
| **Liability exposure mitigation** | Adequacy of liability caps, disclaimer breadth, indemnification coverage, and insurance alignment |
| **ICA readability & acceptance friction** | Flesch-Kincaid readability score target (consumer: ≤ Grade 10; enterprise: ≤ Grade 14); likelihood of ICA pushback on aggressive clauses |
| **Operational implementability** | Whether the business can actually fulfil procedural commitments (notice timelines, data deletion windows, refund processing) |

Apply any user-specific `instructions` from FutureProof context (e.g., preferred liability cap formulas, mandatory arbitration stance, prior legal counsel feedback) to calibrate the draft.

## Step 4: Deliver Output

Produce a structured deliverable package:

### Document 1: Terms & Conditions — Full Draft
- Complete, publication-ready Terms & Conditions document formatted with numbered sections and subsections
- Placeholder brackets `[COMPANY NAME]`, `[EFFECTIVE DATE]`, `[CONTACT EMAIL]` for user completion
- Inline annotations marked with `⚖️ NOTE:` where jurisdiction-specific legal counsel review is recommended before publication

### Document 2: Enforceability & Risk Scorecard

| Dimension | Score (1–10) | Key Finding | Recommended Action |
|---|---|---|---|
| Enforceability robustness | — | — | — |
| Regulatory compliance | — | — | — |
| Liability exposure mitigation | — | — | — |
| ICA readability & acceptance friction | — | — | — |
| Operational implementability | — | — | — |

### Document 3: Implementation Checklist
- Acceptance mechanism implementation guidance (click-wrap UI requirements, checkbox placement, version logging)
- Companion documents required (Privacy Policy, Cookie Policy, DPA, AUP — if not embedded)
- Notification workflow for future term modifications
- Recommended legal counsel review items (ranked by risk severity: critical / advisory)

### Document 4: Plain-Language Summary *(if hybrid tone selected)*
- Section-by-section plain-language companion intended for ICA-facing display alongside or preceding the formal terms

**Disclaimer**: Include a clear statement that the output constitutes informational guidance, not legal advice, and that the user should engage qualified legal counsel in the applicable jurisdiction(s) before publishing.

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
FutureProof:save_experiment(skill="terms-conditions-drafter", experiment={
  hypothesis: "Adding a plain-language summary above each clause reduces ICA support queries about terms by lowering comprehension friction",
  variants: ["control: formal legal terms only", "variant: hybrid terms with inline plain-language summaries per section"],
  measurement: "Volume of terms-related support tickets and user acceptance completion rate over 90 days",
  expected_impact: "25% reduction in terms-related support queries and 10% increase in sign-up completion rate"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="terms-conditions-drafter",
  query="2024-2025 regulatory developments affecting online terms of service enforceability: FTC click-to-cancel rule, EU Digital Services Act obligations, state-level auto-renewal law amendments, and recent arbitration clause enforceability rulings",
  reason="Ensure drafted clause templates reflect current enforceability standards and emerging compliance obligations across key jurisdictions"
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
FutureProof:save_session(skill="terms-conditions-drafter", session={
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