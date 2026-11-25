---
name: partnership-evaluator
description: |
  Runs structured due diligence on a proposed partnership, alliance, or JV
  across seven weighted dimensions — strategic fit, financials, ops,
  culture, risk, power dynamics, exit — producing a go / conditional-go /
  no-go memo with negotiation priorities. Use when a user says "should I
  do this partnership", "evaluate this term sheet", "give me a go/no-go on
  this deal", or shares a co-venture proposal and asks for a structured
  read. For external partner deals, not internal team dynamics or hiring
  decisions.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="partnership-evaluator")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly the user's business model, revenue stage, ICA definition, existing partnerships, strategic priorities, and any prior partnership evaluations.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user to provide:

- **Partner profile**: Who is the prospective partner? (company name, size, industry, business model, public reputation)
- **Partnership type**: What structure is proposed? (revenue share, co-marketing, reseller/channel, technology integration, equity joint venture, licensing, affiliate, strategic supplier)
- **Stated objectives**: What does each side hope to gain? What is the user's primary strategic goal — distribution, credibility, technology access, revenue acceleration, market entry, cost reduction?
- **Materials available**: Any term sheets, proposals, MOUs, decks, or email threads they can share for analysis?
- **Deal stage**: Are they exploratory, in active negotiation, or at final sign-off?
- **Constraints**: Timeline pressure, exclusivity clauses under discussion, minimum commitments, or political dynamics (e.g. board pressure, investor expectations)?
- **Known concerns**: Any gut-level reservations or specific red flags already identified?

If the user's ICA and current strategic priorities are not already in FutureProof context, capture them now — partnership value is meaningless without anchoring to the user's core growth thesis.

## Step 3: Do the Work — Strategic Partnership Due Diligence

Evaluate the proposed partnership across seven weighted dimensions, applying a methodology consistent with professional advisory standards:

### 3.1 Strategic Alignment (Weight: 25%)

- **Mission congruence**: Do both organisations share compatible long-term visions, or will strategic drift create friction within 12–18 months?
- **ICA overlap & complementarity**: Does the partner serve the same ICA with non-competing offerings (high synergy), an adjacent ICA that expands addressable market, or the same ICA with competing offerings (channel conflict risk)?
- **Strategic gap closure**: Does this partnership close a specific, named capability or market gap the user cannot close organically within an acceptable timeframe?
- **Opportunity cost**: What alternatives exist (build, buy, other partners), and does this partnership foreclose higher-value options?

### 3.2 Financial Impact & Value Creation (Weight: 20%)

- **Revenue model clarity**: Is the financial mechanism explicit — revenue share percentages, referral fees, volume commitments, margin structure?
- **Incremental revenue projection**: Model a conservative, base, and optimistic scenario for 12-month incremental revenue or cost savings attributable to the partnership.
- **Unit economics impact**: Does the partnership improve or degrade the user's customer acquisition cost, lifetime value, or gross margin?
- **Investment requirement**: What upfront and ongoing costs (integration, co-marketing, dedicated headcount, legal) are required, and what is the projected payback period?

### 3.3 Operational Compatibility (Weight: 15%)

- **Integration complexity**: What technical, operational, or process integration is required? Rate as low (API/webhook), medium (shared workflows, joint SLAs), or high (merged systems, co-located teams).
- **Resource burden**: Does the user's current team have capacity, or does this partnership require net-new hires or reallocation from existing priorities?
- **Scalability**: If the partnership succeeds, can operations scale without renegotiation or re-architecture?

### 3.4 Cultural & Relational Fit (Weight: 10%)

- **Decision-making velocity**: Does the partner operate at comparable speed? (Startup–enterprise mismatches are the #1 partnership killer.)
- **Values alignment**: Are there observable differences in ethics, customer treatment, quality standards, or transparency that could create reputational exposure?
- **Champion dependency**: Is the partnership anchored to a single internal champion on either side, creating key-person risk?

### 3.5 Risk Exposure (Weight: 15%)

- **Contractual risk**: Exclusivity clauses, non-competes, termination penalties, IP assignment, liability allocation — identify each and classify as acceptable, negotiable, or disqualifying.
- **Reputational risk**: If the partner experiences a public failure, scandal, or quality incident, what is the blast radius to the user's brand?
- **Dependency risk**: Does the partnership create a single point of failure in the user's value chain or revenue model? What percentage of revenue would be partner-dependent at steady state?
- **Data & IP risk**: What data is shared, who owns derivative works, and what happens to data on termination?

### 3.6 Power Dynamics & Leverage (Weight: 10%)

- **Relative scale**: Is there a significant size asymmetry? If so, does the smaller party have sufficient leverage (unique asset, market position, regulatory advantage) to maintain negotiating parity over time?
- **Switching costs**: Who bears higher switching costs if the partnership dissolves — and does that asymmetry create unhealthy dependency?
- **Governance structure**: Is there a joint steering committee, regular review cadence, and mutual escalation path, or is governance informal and one-sided?

### 3.7 Exit Architecture (Weight: 5%)

- **Termination mechanics**: Is there a clean exit clause with reasonable notice period (90+ days), clear IP reversion, and wind-down provisions?
- **Portability of gains**: If the partnership ends, does the user retain customers acquired, integrations built, and market positioning established?
- **Sunset scenario planning**: What does an orderly dissolution look like, and has it been discussed or documented?

Apply any user-specific `instructions` from FutureProof context — for example, if the user has flagged that they prioritise capital efficiency over growth rate, weight financial impact and resource burden accordingly.

## Step 4: Deliver Output

Produce a **Partnership Evaluation Memorandum** with the following sections:

### 4.1 Executive Summary
- One-paragraph go / conditional-go / no-go recommendation with the single most important reason.

### 4.2 Partnership Scorecard

| Dimension | Weight | Score (1–10) | Weighted Score | Key Driver |
|---|---|---|---|---|
| Strategic Alignment | 25% | — | — | — |
| Financial Impact | 20% | — | — | — |
| Operational Compatibility | 15% | — | — | — |
| Cultural & Relational Fit | 10% | — | — | — |
| Risk Exposure | 15% | — | — | — |
| Power Dynamics & Leverage | 10% | — | — | — |
| Exit Architecture | 5% | — | — | — |
| **Composite Score** | **100%** | — | **X.X / 10** | — |

**Interpretation guide**: ≥7.5 = strong proceed; 5.5–7.4 = conditional proceed with named mitigations; <5.5 = do not proceed without fundamental restructuring.

### 4.3 Critical Findings
- **Top 3 strengths** of the proposed partnership (specific, evidence-cited)
- **Top 3 risks** with severity rating (critical / high / medium) and named mitigation for each

### 4.4 Negotiation Priorities
- Rank-ordered list of the 5 most important terms to negotiate or renegotiate before signing, with recommended positions and fallback positions for each.

### 4.5 Financial Scenario Model
- Table with conservative / base / optimistic projections for: incremental revenue, required investment, net contribution, and payback period (months).

### 4.6 Recommended Next Steps
- Concrete, time-bound action items (e.g. "Request audited financials by [date]", "Draft mutual NDA covering data-sharing scope", "Schedule joint working session to map integration architecture").

### 4.7 Decision Log Entry
- Structured block the user can paste into their decision journal or board memo:
  - Partner name, partnership type, evaluation date
  - Composite score
  - Recommendation
  - Key conditions
  - Review-by date (suggested 90-day checkpoint)

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
FutureProof:save_experiment(skill="partnership-evaluator", experiment={
  hypothesis: "Running a 60-day limited pilot with the prospective partner before full commitment reduces partnership failure rate and surfaces operational incompatibilities early",
  variants: ["control: sign full agreement based on evaluation alone", "variant: execute a scoped pilot (defined deliverable, shared KPI, kill criteria) before committing to full terms"],
  measurement: "Partnership health score at 6-month review — composite of revenue contribution, NPS of internal stakeholders, and number of escalations",
  expected_impact: "40% reduction in partnerships that require early termination or major renegotiation within 12 months"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="partnership-evaluator",
  query="Current best practices in strategic partnership structuring for growth-stage companies 2024–2025, including partnership failure post-mortems, optimal governance frameworks, and emerging models (ecosystem partnerships, AI-native co-development agreements)",
  reason="Ensure evaluation framework reflects current market dynamics, emerging partnership structures, and documented failure patterns to improve predictive accuracy of go/no-go recommendations"
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
FutureProof:save_session(skill="partnership-evaluator", session={
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