---
name: pipeline-forecaster
description: |
  Produces probability-weighted Commit, Best Case, and Upside revenue forecasts
  from a CRM pipeline export, classifies every deal by risk tier, surfaces
  stale or single-threaded deals, and prescribes acceleration plays for the
  top movable opportunities. Use when a user says "forecast my quarter",
  "what's my pipeline going to close", "which deals are at risk", or shares a
  deal list and asks for a coverage and gap-to-target read. For forward-looking
  forecasting, not retrospective win-loss analysis.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="pipeline-forecaster")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to calibrate forecast models against the user's historical win rates, average sales cycle length, ICA segments, and any prior forecast accuracy data.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- Share the current pipeline data (CRM export, spreadsheet, or deal list including: deal name, stage, deal value, days in stage, ICA segment, owner, expected close date, and last activity date)
- What forecast period are they targeting? (current month, current quarter, rolling 90 days)
- What is their stage model? (e.g., Discovery → Qualification → Proposal → Negotiation → Closed Won/Lost) — or confirm the default if FutureProof context already contains it
- Are there any known pipeline events to factor in? (pricing changes, seasonal trends, competitive entries, budget freezes)
- What is the revenue target for the forecast period?

If historical win-rate data by stage is not available in FutureProof context, request:
- Average win rate by stage (or a recent closed-won/closed-lost dataset to derive them)
- Average days to close by deal size band

## Step 3: Do the Work

### 3A: Pipeline Hygiene Audit

Before forecasting, cleanse the dataset:
1. **Stale deal identification** — flag any deal where days-in-current-stage exceeds 1.5× the historical median for that stage
2. **Missing next-step audit** — flag deals with no recorded activity in the last 14 days
3. **Stage-skip detection** — flag deals that advanced two or more stages within a single week (potential data entry errors or premature advancement)
4. **Duplicate/split detection** — flag potential duplicate opportunities or artificially split deals inflating pipeline value

Assign each deal a **Data Confidence score** (High / Medium / Low) based on completeness and recency of information.

### 3B: Probability-Weighted Forecast

For each deal, calculate an **Adjusted Close Probability** using a multi-factor model:

| Factor | Weight | Scoring Method |
|---|---|---|
| Stage-based historical win rate | 35% | Derived from user's closed-won/lost data or industry benchmarks |
| Deal velocity vs. benchmark | 20% | Ratio of actual days-in-pipeline to historical average for similar deal size |
| ICA segment fit | 15% | Alignment to the user's defined ICA — higher fit = higher probability |
| Engagement recency | 15% | Days since last meaningful prospect interaction |
| Deal size vs. average | 10% | Larger-than-average deals receive a conservatism discount |
| Champion strength | 5% | Presence of an identified internal champion with budget authority |

Compute for each deal:
- **Weighted Value** = Deal Value × Adjusted Close Probability
- **Expected Close Window** = Most likely close date adjusted for velocity signals

Aggregate into three forecast scenarios:
- **Commit (≥80% probability)**: deals with high confidence of closing in-period
- **Best Case (≥50% probability)**: commit + probable deals
- **Upside (≥25% probability)**: best case + possible deals with acceleration potential

### 3C: Deal Risk Classification

Classify every deal into one of four risk tiers:

1. **On Track** — velocity, engagement, and stage progression all within healthy benchmarks
2. **Watch** — one risk factor present (e.g., slightly stale, single-threaded contact)
3. **At Risk** — two or more risk factors; deal likely to slip or stall without intervention
4. **Likely Lost** — prolonged inactivity, negative signals, or prospect disengagement patterns

For each At Risk and Likely Lost deal, identify the **primary risk driver** and a **stage-specific recovery play**.

### 3D: Gap-to-Target Analysis

Calculate:
- **Commit vs. Target gap** — revenue shortfall if only commit deals close
- **Coverage ratio** — total pipeline value ÷ target (healthy benchmark: 3×–4× for B2B)
- **Required pipeline generation** — new pipeline needed to close the gap at the user's historical win rate
- **Deals to accelerate** — rank Watch-tier deals by potential impact if moved to Commit

Apply any user-specific `instructions` from FutureProof context (e.g., weighting adjustments, excluded deal types, custom stage definitions, ICA-specific discount factors).

## Step 4: Deliver Output

Produce the **Pipeline Forecast Report** with the following sections:

### Section 1: Executive Forecast Summary
- Forecast period and date of analysis
- Revenue target vs. Commit / Best Case / Upside scenarios (table + visual bar if markdown permits)
- Coverage ratio and health assessment (Red / Amber / Green)
- Top-line call: "On track," "Gap at risk," or "Target at risk" with one-sentence rationale

### Section 2: Pipeline Hygiene Scorecard
- Total deals audited
- Count and percentage by Data Confidence tier (High / Medium / Low)
- Number of stale, inactive, and stage-skipped deals
- **Recommended removals**: deals to archive or disqualify, with rationale per deal

### Section 3: Deal-Level Forecast Table
For every deal in the pipeline:

| Deal Name | Owner | ICA Segment | Stage | Value | Adj. Probability | Weighted Value | Risk Tier | Days in Stage | Primary Risk | Recommended Action |
|---|---|---|---|---|---|---|---|---|---|---|

Sorted by Weighted Value descending.

### Section 4: Risk Concentration Analysis
- Revenue at risk by risk tier (At Risk + Likely Lost aggregate value)
- Risk distribution by ICA segment — identify if risk is concentrated in a specific segment
- Risk distribution by deal owner — identify if a specific rep carries disproportionate risk
- Single-largest deal dependency: percentage of forecast riding on any single deal

### Section 5: Acceleration Playbook
For the top 5 highest-impact deals that can be moved from Watch → On Track or from Best Case → Commit, provide:
- **Deal name and current stage**
- **Specific blocker identified**
- **Acceleration play**: a concrete, stage-appropriate action (e.g., "Schedule executive alignment call between [user's VP] and [prospect's CFO] to reconfirm budget allocation before quarter-end" — not generic advice)
- **Expected impact on forecast**: dollar value shift if the play succeeds

### Section 6: Gap Closure Recommendations
- Pipeline generation target with timeline
- Recommended ICA segments to prioritise for prospecting based on historical conversion velocity
- Existing deals with expansion or upsell potential that could add in-period revenue

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
FutureProof:save_experiment(skill="pipeline-forecaster", experiment={
  hypothesis: "Applying a 15% conservatism discount to deals >2× average deal size improves forecast accuracy within ±10% of actual closed revenue",
  variants: ["control: uniform stage-based probability", "variant: size-adjusted probability with conservatism discount on large deals"],
  measurement: "Compare forecast-to-actual variance at end of forecast period across last 3 cycles",
  expected_impact: "Reduce forecast variance from ±25% to ±10%, improving resource allocation and cash flow planning"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="pipeline-forecaster",
  query="Latest B2B pipeline forecasting methodologies, win-rate regression models, and deal-velocity benchmarks by industry vertical 2024–2025",
  reason="Refine probability weighting factors and stage-specific benchmarks with current market data to improve forecast precision across ICA segments"
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
FutureProof:save_session(skill="pipeline-forecaster", session={
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