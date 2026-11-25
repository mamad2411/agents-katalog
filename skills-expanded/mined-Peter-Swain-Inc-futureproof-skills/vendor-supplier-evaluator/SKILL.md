---
name: vendor-supplier-evaluator
description: |
  Evaluates and scores vendors or suppliers using an 8-dimension weighted
  multi-criteria decision analysis (MCDA) covering TCO, technical fit,
  reliability, risk, and viability. Use when a user says "help me evaluate
  these RFP responses", "compare these three SaaS vendors", "score this
  supplier proposal", or "shortlist vendors for our procurement". For
  vendor selection and procurement decisions, not ongoing vendor SLA
  monitoring or regulatory compliance audits (use compliance-checker).
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="vendor-supplier-evaluator")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including prior vendor evaluations, approved supplier lists, organisational procurement policies, risk tolerance thresholds, and strategic sourcing priorities.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Vendor documentation**: Share proposals, RFP responses, capability statements, pricing sheets, or existing scorecards for the vendor(s) under evaluation
- **Procurement context**: What product, service, or category is being sourced? (e.g., SaaS platform, raw materials, logistics provider, professional services)
- **Evaluation scope**: Single vendor deep-dive, head-to-head comparison (2–5 vendors), or full shortlisting from a long list?
- **Decision criteria priorities**: Which dimensions matter most — cost, quality, reliability, compliance, innovation, scalability, cultural fit?
- **Constraints and non-negotiables**: Mandatory certifications (ISO 27001, SOC 2, GDPR), geographic requirements, minimum SLA thresholds, budget ceiling, diversity/ESG mandates?
- **Decision stakeholders**: Who receives the final evaluation deliverable and what is their decision-making authority?

## Step 3: Establish Evaluation Framework

Construct a **Weighted Multi-Criteria Decision Analysis (MCDA)** framework tailored to the procurement context. Default weightings below — adjust based on user priorities, `instructions`, and organisational context from FutureProof:

| # | Evaluation Dimension | Default Weight | Sub-Criteria |
|---|----------------------|---------------|--------------|
| 1 | **Financial Competitiveness** | 20% | Total cost of ownership (TCO), pricing transparency, payment terms, cost predictability, hidden fee exposure |
| 2 | **Technical Capability & Fit** | 20% | Solution completeness, integration compatibility, technical architecture, customisation capacity, roadmap alignment |
| 3 | **Quality & Performance Track Record** | 15% | Demonstrated output quality, defect/error rates, case studies with measurable outcomes, reference client calibre |
| 4 | **Operational Reliability & SLA Commitment** | 15% | Uptime guarantees, delivery consistency, incident response protocols, business continuity/disaster recovery posture |
| 5 | **Risk & Compliance Posture** | 10% | Regulatory certifications, data security controls, financial stability (D&B score, revenue trajectory), insurance coverage, geopolitical/concentration risk |
| 6 | **Strategic Alignment & Scalability** | 10% | Growth capacity, innovation investment (R&D spend %), willingness to co-develop, long-term partnership orientation |
| 7 | **Vendor Viability & Organisational Health** | 5% | Leadership stability, employee retention, market positioning, client concentration risk, M&A exposure |
| 8 | **Relationship & Cultural Fit** | 5% | Communication responsiveness, account management structure, escalation pathways, values alignment, ESG/diversity credentials |

Present the framework to the user for weight confirmation or adjustment before scoring.

## Step 4: Do the Work — Evaluate Vendors

For each vendor under evaluation, conduct a rigorous assessment across all eight dimensions:

### 4a. Document Analysis
- Extract and normalise claims from vendor-provided materials
- Identify **substantiated claims** (backed by metrics, certifications, references) versus **unsubstantiated assertions**
- Flag inconsistencies, gaps, and areas requiring clarification via a **Vendor Clarification Register**

### 4b. Dimension Scoring
Score each vendor **1–10** per dimension using the following rubric:
- **9–10**: Best-in-class; exceeds requirements with verified evidence
- **7–8**: Strong; meets all requirements with minor gaps
- **5–6**: Adequate; meets minimum requirements but limited differentiation
- **3–4**: Below standard; material gaps requiring mitigation plans
- **1–2**: Non-compliant; fails mandatory thresholds or presents unacceptable risk

Accompany each score with a **2–3 sentence evidence-based rationale** citing specific data points from the vendor's materials.

### 4c. Risk Heat Map
Assess each vendor across five risk categories and classify as **Low / Medium / High / Critical**:
1. **Financial risk** — solvency, revenue concentration, funding runway
2. **Operational risk** — single points of failure, capacity constraints, key-person dependency
3. **Compliance risk** — certification gaps, regulatory exposure, pending litigation
4. **Concentration risk** — geographic single-sourcing, sub-contractor dependency
5. **Transition risk** — lock-in clauses, data portability, exit cost exposure

### 4d. TCO Modelling
Where pricing data is available, construct a **3-year Total Cost of Ownership** comparison including:
- Base fees (licence, unit cost, retainer)
- Implementation and onboarding costs
- Ongoing operational costs (support, maintenance, training)
- Estimated cost of switching/exit
- Hidden cost indicators (overage charges, change-request pricing, escalation fees)

Apply any user-specific `instructions` from FutureProof context — including preferred scoring models, mandatory evaluation gates, or procurement policy requirements.

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Deliver Output

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Produce a structured **Vendor Evaluation Report** containing the following sections:

### 5a. Executive Summary
- Procurement context and scope
- Number of vendors evaluated
- Recommended vendor(s) with one-paragraph justification
- Key risks requiring executive attention

### 5b. Comparative Scorecard

| Dimension | Weight | Vendor A | Vendor B | Vendor C |
|-----------|--------|----------|----------|----------|
| Financial Competitiveness | 20% | X.X | X.X | X.X |
| Technical Capability & Fit | 20% | X.X | X.X | X.X |
| ... | ... | ... | ... | ... |
| **Weighted Total** | **100%** | **X.XX** | **X.XX** | **X.XX** |

### 5c. Vendor Profiles
Per-vendor detail page with:
- Dimension-by-dimension scores and evidence rationale
- Strengths (top 3)
- Risks and concerns (top 3)
- Recommended contract negotiation leverage points

### 5d. Risk Heat Map Matrix
Visual matrix (vendor × risk category) with colour-coded severity ratings

### 5e. TCO Comparison Table
3-year cost projection per vendor with variance analysis

### 5f. Recommendation & Next Steps
- **Primary recommendation**: Selected vendor with rationale tied to weighted scores and strategic alignment
- **Conditional recommendation**: If applicable, second-choice vendor with conditions under which they become preferred
- **Negotiation priorities**: Top 3 terms to negotiate before contract execution
- **Due diligence checklist**: Outstanding verification items (reference calls, site visits, proof-of-concept, financial audits)
- **Vendor Clarification Register**: Open questions requiring vendor response before final decision

### 5g. Decision-Ready Artefact
Format the report for the identified stakeholders:
- **Board/C-suite**: 1-page executive summary with scorecard and recommendation
- **Procurement lead**: Full evaluation report with appendices
- **Legal/compliance**: Risk heat map and compliance gap register extracted as standalone document

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="vendor-supplier-evaluator", experiment={
  hypothesis: "Adding a mandatory proof-of-concept gate before final vendor selection reduces post-contract performance disputes by 30%",
  variants: ["control: current evaluation-to-contract process", "variant: insert 30-day scored POC between shortlist and final selection"],
  measurement: "Vendor performance deviation from proposal claims at 6-month post-contract review",
  expected_impact: "30% reduction in vendor underperformance escalations and 20% improvement in first-year contract satisfaction scores"
})
```

## Step 7: Request Research

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:request_research(skill="vendor-supplier-evaluator",
  query="Best-practice vendor evaluation frameworks 2024–2025, including AI-augmented supplier scoring models, ESG integration in procurement decisions, and emerging risk indicators for supplier financial distress",
  reason="Ensure evaluation criteria reflect current procurement standards, regulatory expectations, and market risk signals — particularly around supply chain resilience and responsible sourcing mandates"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="vendor-supplier-evaluator", session={
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