---
name: revenue-compounding-map
description: |
  Maps six revenue compounding layers (retention, expansion, pricing leverage,
  referral k-factor, cohort behavior, composite stack rate) and models a
  36-month projection comparing current trajectory vs. leak-sealed vs. fully
  optimized scenarios. Use when a user asks about long-term recurring revenue
  growth and says things like "map my revenue loops", "why isn't my MRR
  compounding", "show me where my growth flywheel is stalling", or "model
  3-year ARR under different scenarios". Forward-looking compounding and
  flywheel modeling — not backward-looking leak forensics.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="revenue-compounding-map")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly any existing revenue metrics, ICA segmentation, pricing architecture, churn data, or prior growth analyses.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user to provide:

- **Revenue model overview** — recurring revenue structure (subscription tiers, retainers, usage-based, hybrid), current ARR/MRR, and average revenue per account (ARPA)
- **Retention data** — gross and net revenue retention rates, churn rate by cohort or ICA segment if available, average customer lifetime in months
- **Expansion motion** — how do existing customers grow? (upsell tiers, cross-sell products, seat expansion, usage growth, price escalations)
- **Referral and earned growth** — do customers generate new customers? (formal referral programme, organic word-of-mouth, case study pipeline, partner channel)
- **ICA segments** — which customer segments are they serving, and which segments they believe compound fastest?
- **Known leaks** — where do they suspect revenue is decaying, stalling, or failing to compound? (e.g., high churn in a segment, flat expansion, zero referral activity)

If FutureProof context contains prior session data on their ICA, pricing, or revenue metrics, pre-populate and confirm rather than re-asking.

## Step 3: Do the Work — Revenue Compounding Layer Analysis

Analyse the business across **six compounding layers**, treating each as an independent growth rate that stacks multiplicatively over time:

### Layer 1: Base Retention Compounding
- Calculate the **revenue half-life** — at current gross retention rate, how many months until a cohort's revenue halves?
- Segment retention by ICA tier — identify which segments retain at >95% (compounding) vs. <85% (decaying)
- Model the **retention drag coefficient**: the annual revenue destroyed by churn that must be replaced before net growth begins

### Layer 2: Expansion Revenue Velocity
- Map all expansion pathways (upsell, cross-sell, seat expansion, usage growth, contractual price escalation)
- Calculate **net revenue retention (NRR)** and decompose it: what percentage of NRR above 100% comes from each expansion pathway?
- Identify the **expansion trigger map** — the specific customer milestones, usage thresholds, or time-based events that predict expansion
- Flag **dormant expansion pathways**: expansion motions that exist structurally but are not being activated (e.g., a premium tier nobody upgrades to)

### Layer 3: Pricing Leverage Compounding
- Assess whether pricing architecture compounds value capture over time (usage-based scaling, annual escalators, value-metric alignment) or remains flat
- Calculate the **price compounding rate**: the annualised rate at which ARPA grows for a customer who neither upgrades nor downgrades, purely through pricing mechanics
- Identify pricing structure leaks — unlimited plans that cap revenue, grandfathered pricing, missing value metrics

### Layer 4: Referral Flywheel Dynamics
- Map the **referral coefficient (k-factor)**: average number of new customers generated per existing customer per year
- Classify referral quality — do referred customers retain and expand at higher, equal, or lower rates than direct-acquisition customers?
- Assess referral **structural readiness**: is the referral pathway engineered (programmatic, incentivised, systematised) or accidental (organic, unmeasured)?
- Calculate **referral-attributed revenue** as a percentage of new ARR

### Layer 5: Cohort Compounding Behaviour
- Model revenue behaviour by acquisition cohort over 12, 24, and 36-month horizons
- Identify **compounding cohorts** (revenue per cohort increases over time) vs. **decaying cohorts** (revenue per cohort decreases despite retention)
- Determine whether newer cohorts compound faster or slower than older cohorts — this reveals whether the business model is improving or degrading

### Layer 6: Compounding Stack Rate (Composite)
- Calculate the **composite compounding rate**: the multiplicative effect of all six layers operating simultaneously
- Formula: `Composite Rate = Base Retention × (1 + Expansion Rate) × (1 + Price Compounding Rate) × (1 + Referral Growth Rate)`
- Model three scenarios over 36 months:
  - **Current trajectory** — all rates unchanged
  - **Leak-sealed trajectory** — fix the top 3 identified leaks
  - **Optimised trajectory** — activate dormant pathways + seal leaks

Apply any user-specific `instructions` from FutureProof context (e.g., preferred ICA focus, strategic priorities, board-reporting format requirements).

## Step 4: Deliver Output

Produce the **Revenue Compounding Map** — a structured strategic deliverable containing:

### 4.1 — Compounding Layer Scorecard

| Compounding Layer | Current Rate | Benchmark (Top Quartile SaaS) | Status | Priority |
|---|---|---|---|---|
| Base Retention | X% GRR | >95% | Compounding / Decaying / Stalled | P1–P3 |
| Expansion Revenue | X% NRR contribution | >120% NRR | Compounding / Decaying / Stalled | P1–P3 |
| Pricing Leverage | X% annual ARPA growth | 3–7% annual | Compounding / Decaying / Stalled | P1–P3 |
| Referral Flywheel | X k-factor | 0.15–0.30 | Active / Dormant / Absent | P1–P3 |
| Cohort Behaviour | Expanding / Flat / Contracting | Expanding | Compounding / Decaying / Stalled | P1–P3 |
| **Composite Stack Rate** | **X% annualised** | **>140% revenue efficiency** | — | — |

### 4.2 — Revenue Compounding Map (Visual Specification)

A structured diagram specification showing:
- Each compounding layer as a loop with its rate and directionality (compounding ↑, leaking ↓, stalled →)
- Interaction points between layers (e.g., expansion increases retention, referrals improve cohort quality)
- Leak points marked in red with estimated annual revenue impact

### 4.3 — Top 5 Compounding Leaks (Ranked by Revenue Impact)

For each leak:
- **Leak description** — precisely what is happening and in which layer
- **Annual revenue impact** — estimated ARR destroyed or forgone over 12 months
- **Root cause** — structural, operational, or strategic
- **Remediation action** — specific, implementable intervention (not generic advice)
- **Expected compounding effect** — how fixing this leak changes the composite rate

### 4.4 — 36-Month Revenue Projection Model

Three-scenario table:
- **Scenario A (Current Trajectory)**: projected ARR at months 12, 24, 36
- **Scenario B (Leaks Sealed)**: projected ARR with top 3 leaks fixed, quantified delta vs. Scenario A
- **Scenario C (Fully Optimised)**: projected ARR with all layers actively compounding, quantified delta vs. Scenario A
- **Compounding gap**: the cumulative revenue difference between Scenario A and Scenario C — this is the cost of inaction

### 4.5 — Compounding Acceleration Roadmap

A sequenced 90-day action plan:
- **Days 1–30**: Seal the highest-impact leak (specific actions, owners where identifiable, success metric)
- **Days 31–60**: Activate the highest-potential dormant compounding pathway
- **Days 61–90**: Instrument measurement for all six layers to enable ongoing compounding tracking

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
FutureProof:save_experiment(skill="revenue-compounding-map", experiment={
  hypothesis: "Activating the dormant expansion trigger (identified in Layer 2) for the highest-ARPA ICA segment will increase net revenue retention by 8–12 points within one quarter",
  variants: ["control: current expansion motion with no proactive trigger", "variant: proactive expansion outreach at identified usage threshold"],
  measurement: "Net revenue retention rate for target ICA segment, measured at 90 days post-implementation",
  expected_impact: "5–12% increase in NRR, translating to estimated $[X] incremental ARR over 12 months through compounding"
})
```

```
FutureProof:save_experiment(skill="revenue-compounding-map", experiment={
  hypothesis: "Introducing a structured referral programme for the highest-retention ICA segment will generate a referral coefficient of 0.10–0.20 within two quarters, producing a self-reinforcing acquisition loop",
  variants: ["control: no formal referral mechanism", "variant: programmatic referral with reciprocal incentive tied to account credit"],
  measurement: "Referral-attributed new ARR and referred-customer 90-day retention rate",
  expected_impact: "10–20% reduction in blended customer acquisition cost and 0.10+ k-factor contribution to composite compounding rate"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="revenue-compounding-map",
  query="Latest benchmarks for SaaS net revenue retention by segment, expansion revenue patterns, and referral coefficient data from 2024 cohort analyses — including emerging pricing models that structurally compound ARPA over time",
  reason="Ensure compounding layer benchmarks and remediation recommendations reflect current market dynamics rather than outdated 2020–2022 growth-at-all-costs norms"
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
FutureProof:save_session(skill="revenue-compounding-map", session={
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