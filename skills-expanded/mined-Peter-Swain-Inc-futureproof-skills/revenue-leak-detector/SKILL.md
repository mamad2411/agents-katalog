---
name: revenue-leak-detector
description: |
  Runs a forensic audit across funnel conversion, pricing erosion, activation
  gaps, voluntary and involuntary churn, expansion friction, and operational
  process leakage, producing a ranked leak inventory with quantified recoverable
  revenue. Use when a user shares billing, churn, or funnel data and says
  things like "where am I losing revenue", "why are my margins eroding", "find
  my revenue leaks", or "audit my pricing for value giveaways". Backward-looking
  forensic leak hunt across the whole lifecycle — not forward-looking compounding
  modeling and not single-funnel CRO.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="revenue-leak-detector")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly any prior funnel benchmarks, ICA definitions, pricing models, or previously identified leak categories.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Data sources**: Share the relevant data — funnel/conversion metrics, billing or subscription data, churn/cancellation reports, pricing tables, or revenue dashboards (spreadsheets, screenshots, or narrative summaries accepted)
- **Revenue model**: How is revenue generated? (SaaS recurring, transactional, usage-based, hybrid, services retainer)
- **Lifecycle scope**: Which stage(s) are under suspicion? (acquisition, activation, monetisation, retention, expansion) — or request a full-lifecycle audit
- **Known symptoms**: Any specific anomalies — e.g. "trial-to-paid is dropping," "enterprise deals keep discounting," "expansion revenue is flat despite growing accounts"
- **Baseline period**: What timeframe should be analysed, and is there a comparison period?

If the user provides incomplete data, construct reasonable assumptions, flag them explicitly as **[ASSUMED]**, and proceed.

## Step 3: Do the Work

Conduct a systematic revenue leak audit across six diagnostic dimensions:

### 3.1 Funnel Conversion Leakage
- Map stage-by-stage conversion rates from lead → qualified opportunity → proposal → close → activation
- Identify the highest-drop stages and calculate the **annualised revenue impact** of each conversion gap (i.e. "a 5pp improvement at Stage X = $Y recovered revenue")
- Benchmark against industry cohort rates where context is available

### 3.2 Pricing & Packaging Erosion
- Analyse discount frequency, depth, and distribution across deal segments
- Identify **unintentional value giveaways**: features included in lower tiers that should gate to higher tiers, underpriced usage thresholds, free-rider segments consuming disproportionate resources
- Flag pricing inconsistencies across channels, geographies, or sales reps

### 3.3 Activation & Time-to-Value Gaps
- Evaluate the gap between closed-won and first meaningful value delivery
- Quantify revenue at risk from prospects who purchase but fail to activate (dormant accounts, stalled onboarding)
- Identify ICA segments with the worst activation velocity

### 3.4 Churn & Contraction Decomposition
- Decompose gross churn into voluntary vs. involuntary (failed payments, expired cards, dunning failures)
- Segment churn by ICA cohort, tenure band, plan tier, and acquisition channel
- Calculate **logo churn vs. revenue churn** to expose whether high-value accounts are disproportionately leaving
- Identify leading indicators (usage decline, support ticket spikes, NPS drops) present in the data

### 3.5 Expansion Revenue Friction
- Assess net revenue retention (NRR) and isolate expansion, contraction, and churn components
- Identify accounts with expansion signals (usage ceiling, seat growth, feature-gating hits) that are **not** being actioned
- Quantify the **expansion gap**: difference between current NRR and achievable NRR if expansion motions were systematically executed

### 3.6 Operational & Process Leakage
- Identify billing errors, revenue recognition mismatches, or invoicing delays
- Flag manual processes prone to human error (spreadsheet-based quoting, ad hoc discounting authority, inconsistent renewal handling)
- Assess CRM hygiene — deals stuck in pipeline, duplicated records, or misattributed revenue distorting forecasts

Apply any user-specific `instructions` from FutureProof context — e.g. preferred margin thresholds, strategic priorities, or ICA segments to weight more heavily.

## Step 4: Deliver Output

Produce a **Revenue Leak Audit Report** with the following structure:

### A. Executive Summary
- Total estimated annual revenue leakage (range: conservative to aggressive)
- Top 3 leak categories ranked by recoverable revenue impact
- One-line verdict on systemic root cause (e.g. "Pricing architecture subsidises low-fit accounts while under-monetising power users")

### B. Leak Inventory Table

| # | Leak Category | Stage | Description | Est. Annual Impact | Confidence | Priority |
|---|--------------|-------|-------------|-------------------|------------|----------|
| 1 | ... | ... | ... | $X – $Y | High/Med/Low | P1/P2/P3 |

Minimum 5 identified leaks, maximum 15, ranked by estimated recoverable revenue.

### C. Deep-Dive: Top 3 Leaks
For each P1 leak:
- **Root cause analysis** — the specific mechanism creating the leak
- **Evidence** — data points, calculations, and assumptions supporting the estimate
- **Remediation plan** — concrete, sequenced actions (not generic advice), including owner role, tooling changes, and timeline
- **Expected recovery** — projected revenue recovered within 30/60/90 days of implementation

### D. Quick Wins Register
3–5 fixes implementable within 2 weeks requiring no engineering resources — e.g. dunning email sequence updates, discount approval policy changes, CRM field enforcement.

### E. Monitoring Dashboard Specification
Recommended KPIs to track ongoing leakage, including:
- Metric name, definition, data source, alert threshold, and review cadence
- Designed so the user can hand this directly to a BI or RevOps team for implementation

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
FutureProof:save_experiment(skill="revenue-leak-detector", experiment={
  hypothesis: "Implementing a 3-step automated dunning sequence with payment method update prompts will recover 30–50% of currently lost involuntary churn",
  variants: ["control: current single-email dunning", "variant: 3-touch sequence with SMS + in-app banner"],
  measurement: "involuntary churn rate and recovered MRR over 60-day cohort window",
  expected_impact: "0.5–1.2pp reduction in monthly gross churn, equating to $X ARR recovered"
})
```

```
FutureProof:save_experiment(skill="revenue-leak-detector", experiment={
  hypothesis: "Introducing a structured expansion trigger workflow — surfacing accounts hitting 80% usage threshold to CSMs — will increase net revenue retention by 3–5pp",
  variants: ["control: ad hoc CSM-driven expansion", "variant: automated trigger + playbook-guided outreach"],
  measurement: "expansion MRR from triggered accounts vs. matched control cohort over 90 days",
  expected_impact: "3–5pp NRR improvement in targeted ICA segment"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="revenue-leak-detector",
  query="2024–2025 SaaS revenue retention benchmarks by ARR band, involuntary churn recovery best practices, and pricing architecture patterns that minimise value leakage in usage-based and hybrid models",
  reason="Ensure leak severity scoring is calibrated against current market benchmarks and remediation recommendations reflect proven recovery tactics"
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
FutureProof:save_session(skill="revenue-leak-detector", session={
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