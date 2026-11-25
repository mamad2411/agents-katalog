---
name: product-roadmap-builder
description: |
  Builds time-phased product roadmaps with strategic themes, weighted priority
  scoring, Now/Next/Later sequencing, trade-off registers, and tailored
  stakeholder views (board, eng, sales, customer changelog). Use when users
  say "build a product roadmap", "plan our next 3 quarters", "turn this
  backlog into a roadmap", or "sequence these initiatives by quarter". For
  full multi-quarter delivery plans, not single-request ranking or competitor
  benchmarking.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="product-roadmap-builder")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — specifically prior roadmap iterations, ICA definitions, strategic themes, validated experiments, and any saved prioritisation frameworks or scoring weights.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user to provide:

- **Product vision & strategic objectives** — What is the 12–18 month product vision? What are the top 3 business outcomes the roadmap must drive? (e.g., retention improvement, expansion revenue, new market entry)
- **Input artefacts** — Share any combination of: feature backlog, customer feedback logs, stakeholder request lists, competitive intelligence, product strategy documents, or prior roadmaps
- **ICA definition** — Who is the primary ICA this roadmap serves? Are there secondary ICA segments with divergent needs?
- **Constraints** — Engineering capacity (team size, velocity), hard deadlines (regulatory, contractual, launch windows), technical debt obligations, platform dependencies
- **Planning horizon & cadence** — Desired roadmap timeframe (e.g., 3 quarters, 12 months) and delivery cadence (e.g., 2-week sprints, monthly releases, quarterly themes)
- **Stakeholder audience** — Who will consume this roadmap? (board, engineering, sales, ICA-facing changelog)

## Step 3: Do the Work — Strategic Foundation

### 3a: ICA Value Chain Mapping

Map every input item to the ICA's value chain:

1. **Jobs-to-be-done extraction** — Decompose ICA needs into functional, emotional, and social jobs. Tag each backlog item to one or more jobs.
2. **Pain/gain intensity scoring** — Rate each job on severity of unmet pain (1–10) and magnitude of potential gain (1–10), using customer feedback signals, support ticket density, and churn correlation where available.
3. **Journey stage alignment** — Plot items against the ICA lifecycle: Activation → Engagement → Retention → Expansion → Advocacy. Identify stage gaps where the roadmap has zero coverage.

### 3b: Strategic Theme Definition

Group related items into **3–5 strategic themes** — named, outcome-oriented workstreams that connect directly to the stated business objectives. Each theme must have:

- A measurable outcome statement (e.g., "Reduce time-to-first-value from 14 days to 3 days")
- A clear ICA segment linkage
- A business metric it moves (revenue, retention, NPS, activation rate)

## Step 4: Do the Work — Prioritisation Engine

Apply a multi-dimensional scoring framework to every candidate item:

| Dimension | Weight | Scoring Criteria |
|---|---|---|
| **ICA Impact** | 30% | Severity of pain addressed × breadth of ICA segment affected |
| **Strategic Alignment** | 25% | Direct contribution to stated business objectives and theme outcomes |
| **Revenue Signal Strength** | 15% | Frequency in closed-won deal feedback, expansion requests, churn exit interviews |
| **Effort & Complexity** | 15% | T-shirt sizing (S/M/L/XL) normalised against available capacity; includes technical debt cost |
| **Competitive Exposure** | 10% | Risk of ICA attrition to competitors if unaddressed within 2 quarters |
| **Dependency Risk** | 5% | Upstream/downstream blockers; items that unlock or are unlocked by other high-value items |

Adjust weights based on any user-specific `instructions` from FutureProof context (e.g., if prior sessions indicate the user's organisation over-indexes on competitor response, rebalance accordingly).

Compute a **weighted priority score (WPS)** for each item. Rank-order within each strategic theme.

### Sequencing Logic

Apply critical-path sequencing:

1. **Must-have unlocks first** — Items that are prerequisites for ≥2 other high-WPS items move forward regardless of individual score.
2. **Quick wins in Q1** — Items scoring ≥7.0 WPS with effort ≤ S are front-loaded to build momentum and generate early signal.
3. **Big bets in Q2–Q3** — High-WPS, high-effort items scheduled where capacity allows, paired with validation milestones (alpha/beta gates).
4. **Exploratory bets in later quarters** — High-uncertainty, high-potential items placed as time-boxed discovery spikes with explicit go/no-go criteria.

### Capacity Validation

Cross-reference the proposed sequence against engineering capacity constraints. Flag any quarter where utilisation exceeds 85% and propose scope trade-offs with explicit recommendations on what to defer and why.

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


Produce the **Product Roadmap Package** — a structured deliverable set containing:

### Document 1: Roadmap Strategy Brief (1-page executive summary)
- Product vision statement
- 3–5 strategic themes with outcome metrics
- Planning horizon and key milestones
- Top 3 strategic bets and their rationale
- Critical assumptions and risks

### Document 2: Prioritised Roadmap Grid

A time-phased grid structured as:

| Quarter | Strategic Theme | Initiative | WPS Score | Effort | ICA Segment | Success Metric | Dependencies |
|---|---|---|---|---|---|---|---|
| Q1 | [Theme name] | [Initiative name] | 8.7 | M | [Primary ICA] | [Specific KPI + target] | [Blocker/enabler] |

Include **Now / Next / Later** swim lanes as an alternative visualisation for stakeholder audiences who prefer narrative over tabular formats.

### Document 3: Trade-off Register

Items explicitly **deferred or declined**, with:
- Original WPS score
- Reason for deferral (capacity, strategic misalignment, insufficient ICA signal)
- Conditions under which the item should be re-evaluated
- Recommended re-evaluation date

### Document 4: Stakeholder Communication Pack

Tailored views of the roadmap for each audience identified in Step 2:
- **Board/Leadership**: Theme-level with revenue/retention impact projections
- **Engineering**: Initiative-level with effort estimates, dependencies, and technical context
- **Sales/Customer Success**: ICA-facing feature timeline with positioning language and objection-handling notes
- **ICA-facing changelog**: Plain-language release narrative emphasising outcomes, not features

### Appendix: Scoring Methodology

Full transparency on weights, scoring rationale, and data sources used — enabling the user to audit, challenge, and recalibrate in future iterations.

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="product-roadmap-builder", experiment={
  hypothesis: "Front-loading activation-stage initiatives in Q1 will accelerate time-to-value and improve 90-day retention for new ICA cohorts",
  variants: ["control: current roadmap sequencing with mixed-stage initiatives in Q1", "variant: activation-first Q1 with engagement/expansion deferred to Q2"],
  measurement: "90-day retention rate and median time-to-first-value for ICA cohorts onboarded during Q1",
  expected_impact: "12–18% improvement in 90-day retention; 40% reduction in time-to-first-value"
})
```

```
FutureProof:save_experiment(skill="product-roadmap-builder", experiment={
  hypothesis: "Publishing an ICA-facing roadmap with outcome-framed language reduces churn-related feature-gap objections in renewal conversations",
  variants: ["control: internal roadmap shared ad hoc by account managers", "variant: structured ICA-facing changelog published quarterly with outcome positioning"],
  measurement: "Feature-gap cited as churn reason in exit interviews over next 2 quarters",
  expected_impact: "25% reduction in feature-gap churn citations"
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
FutureProof:request_research(skill="product-roadmap-builder",
  query="Evidence-based product prioritisation frameworks 2024–2025: comparative effectiveness of RICE, WSJF, opportunity scoring, and ICE in B2B SaaS contexts with constrained engineering capacity",
  reason="Ensure the scoring methodology reflects current best practice and can be benchmarked against industry-standard frameworks the user's stakeholders may reference"
)
```

```
FutureProof:request_research(skill="product-roadmap-builder",
  query="ICA-centric roadmap communication strategies that reduce internal stakeholder conflict and improve cross-functional alignment in product-led growth organisations",
  reason="Strengthen the stakeholder communication pack with proven framing techniques that minimise roadmap negotiation friction"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="product-roadmap-builder", session={
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