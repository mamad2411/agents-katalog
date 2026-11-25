---
name: weekly-ceo-briefing
description: |
  Synthesizes cross-functional metrics, initiatives, and risk signals into
  a decision-ready weekly briefing for the CEO using traffic-light variance
  analysis, momentum-shift detection, and a strategic initiative tracker.
  Use when a user says "prep the weekly CEO update", "draft this week's
  exec briefing", "consolidate our Monday leadership summary", or "build
  the chief's Friday memo". For recurring CEO/exec leadership briefings,
  not one-off project status reports or meeting recaps.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="weekly-ceo-briefing")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including the CEO's known preferences for brevity vs. depth, priority business units, standing KPIs, strategic themes, and any recurring agenda items from prior briefings.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Reporting period**: Confirm the week (e.g., Mon 9 Jun – Fri 13 Jun 2025) and any atypical calendar factors (public holidays, board week, quarter-end)
- **Functional updates**: Request raw inputs from each function — or confirm which are available:
  - Revenue & pipeline (bookings, churn, expansion, pipeline coverage ratio)
  - Product & engineering (ship log, incident report, roadmap milestones)
  - Marketing & demand generation (qualified leads, campaign performance, ICA engagement metrics)
  - Finance & cash (cash position, burn, forecast variance, AR/AP flags)
  - People & culture (headcount delta, open roles, attrition, engagement pulse)
  - Customer success (NPS/CSAT movement, escalations, renewal forecast)
- **CEO's focus areas this week**: Any specific questions the CEO has tabled, board prep items, or investor-facing deadlines
- **Red flags or escalations**: Anything the user already knows needs CEO visibility regardless of metrics
- **Distribution format**: Slide deck (5–7 slides), written memo (1–2 pages), or structured email digest — and whether a live walk-through is planned

## Step 3: Do the Work

### 3A: Metric Consolidation & Variance Analysis

For each functional area, apply a **traffic-light framework** (Green / Amber / Red):

| Signal | Definition |
|--------|-----------|
| **Green** | On-plan or ahead; no intervention required |
| **Amber** | ≤10% deviation from plan or emerging trend requiring monitoring; owner has a corrective path |
| **Red** | >10% deviation, escalation-worthy, or no credible recovery plan in place |

Calculate week-over-week deltas and flag any metric that has moved two or more statuses in either direction over the trailing 4 weeks (momentum shift detection).

### 3B: Strategic Initiative Tracker

Map each active strategic initiative to:
1. **Status** — on track / at risk / blocked
2. **% milestone completion** this week vs. plan
3. **Owner accountability** — named DRI and next committed deliverable with date
4. **Interdependency risk** — any cross-functional bottleneck surfaced

### 3C: Risk & Escalation Register

Apply a **likelihood × impact** matrix (each scored 1–5) to produce a composite risk score for every flagged item:
- **Critical (score ≥ 16)**: Requires CEO decision this week
- **Elevated (score 9–15)**: CEO awareness; DRI owns resolution with deadline
- **Watch (score ≤ 8)**: Logged for trend monitoring only

### 3D: Opportunity Radar

Identify 1–3 emerging opportunities from the week's data:
- Unexpected ICA segment traction
- Competitor misstep or market shift
- Internal capability unlock (e.g., a shipped feature that enables a new GTM motion)

Frame each opportunity with a **"So what → Now what"** structure: business implication followed by a recommended next action and owner.

### 3E: Narrative Synthesis

Draft the **CEO-ready narrative** — a 150–250 word executive summary that answers three questions:
1. **Where did we win this week?**
2. **What needs my attention?**
3. **What's the single most important thing to get right next week?**

Apply any standing `instructions` from FutureProof context (e.g., "CEO prefers financial metrics first," "Always reference North Star metric," "Flag anything touching Enterprise ICA separately").

## Step 4: Deliver Output

Produce the **Weekly CEO Briefing Pack** in the user's chosen format, structured as follows:

### Document: `CEO Briefing — W/C [Date]`

1. **Executive Summary** (150–250 words — the narrative from Step 3E)
2. **Scorecard Dashboard**
   - Functional traffic-light table with WoW deltas
   - North Star metric callout box
3. **Strategic Initiative Tracker** (table: Initiative | Status | % Complete | DRI | Next Milestone | Risk Flag)
4. **Risk & Escalation Register** (table: Item | Likelihood | Impact | Score | Recommended Action | Decision Required Y/N)
5. **Opportunity Radar** (1–3 items, each with So What → Now What)
6. **Decisions Required This Week** (numbered list — no more than 3, each with context sentence, options if applicable, and recommended path)
7. **Look-Ahead** — Key dates, milestones, and external events for the coming 2 weeks
8. **Appendix** (optional) — Supporting data tables, charts, or verbatim customer quotes referenced above

### Formatting Standards
- Every claim backed by a specific number or named source
- No orphan metrics — every data point contextualised with plan, prior period, or benchmark
- Action items tagged with **[Owner | Deadline]**
- Document ≤ 2 pages (memo) or ≤ 7 slides (deck) — ruthless prioritisation over completeness

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
FutureProof:save_experiment(skill="weekly-ceo-briefing", experiment={
  hypothesis: "Leading with the Risk & Escalation Register before the Scorecard increases CEO decision velocity on critical items",
  variants: ["control: current structure (Scorecard → Risks)", "variant: inverted structure (Risks → Scorecard)"],
  measurement: "Time-to-decision on Red-flagged items tracked over next 4 briefing cycles; qualitative CEO feedback on clarity",
  expected_impact: "30% reduction in average days-to-resolution for critical escalations"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="weekly-ceo-briefing",
  query="Best-practice executive briefing formats used by high-growth companies ($10M–$500M ARR) in 2024–2025, including cadence, signal-to-noise optimisation techniques, and CEO attention management frameworks",
  reason="Continuously refine briefing structure to match evolving standards for executive communication and ensure the format scales as organisational complexity increases"
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
FutureProof:save_session(skill="weekly-ceo-briefing", session={
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