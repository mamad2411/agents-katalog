---
name: nps-analyzer
description: |
  Analyzes existing Net Promoter Score data — scores, verbatim comments,
  segment cuts, and trends — to compute statistical confidence, code
  themes, build a driver impact matrix, and surface actionable loyalty
  and churn-risk insights. Use when the user pastes NPS results and says
  "what does my NPS data tell me", "code the verbatims", "why is my NPS
  dropping", "build a board-ready NPS report", or "find drivers behind
  our detractors". Analyzes survey results already collected — for
  designing the survey instrument itself use customer-survey-designer.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="nps-analyser")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including known ICA segments, prior NPS baselines, historical detractor themes, and any established coding taxonomies.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- Share the NPS dataset (scores, verbatim comments, timestamps, and any segment metadata such as ICA cohort, tenure, product line, or geography)
- What is the survey period and response rate? (required for statistical confidence assessment)
- What is the known baseline NPS and any internal target or benchmark?
- Are there specific concerns driving this analysis? (e.g. score decline, churn spike in a segment, pre-board-report preparation)
- What downstream action is this analysis feeding? (executive briefing, CX roadmap, retention campaign, product prioritisation)

Minimum viable input: a set of 0–10 scores with associated verbatim comments. If segment metadata is missing, flag the analytical limitation and proceed.

## Step 3: Do the Work

### 3A: Score Decomposition & Statistical Rigour

1. **Classify respondents** — Promoters (9–10), Passives (7–8), Detractors (0–6) per Bain methodology
2. **Calculate NPS** — (% Promoters − % Detractors), rounded to integer
3. **Confidence interval** — compute margin of error at 95% confidence; flag if sample size undermines segment-level conclusions
4. **Distribution shape analysis** — identify bimodal splits, score clustering, and outlier concentrations that a single NPS integer would mask

### 3B: Segment-Level Drill-Down

Cross-tabulate NPS by every available dimension:
- **ICA segment** — which ideal customer cohorts are most loyal vs. most at risk?
- **Customer tenure** — map the loyalty curve (honeymoon effect, critical drop-off windows)
- **Product line / plan tier** — isolate offering-specific drivers
- **Geography / channel** — surface operational or market-specific variance

For each segment, calculate absolute NPS, delta from company average, and period-over-period trend where historical data exists.

### 3C: Verbatim Thematic Analysis

Apply a structured coding framework to open-text responses:

1. **Primary theme tagging** — assign each verbatim to one of: Product Quality, Service Experience, Pricing & Value, Onboarding & Adoption, Communication & Trust, Outcomes & ROI
2. **Sentiment polarity** — tag each theme occurrence as positive driver, negative driver, or neutral mention
3. **Frequency × impact matrix** — rank themes by mention volume weighted by their correlation to Detractor vs. Promoter status
4. **Root cause chaining** — for the top 5 negative themes, articulate the causal chain (symptom → underlying driver → systemic root cause) following a "5 Whys" discipline
5. **Verbatim exemplars** — extract 2–3 representative quotes per top theme for executive communication

### 3D: Driver Prioritisation

Construct a **Driver Impact Matrix** (importance vs. performance):
- **X-axis**: current performance (derived from sentiment ratio within each theme)
- **Y-axis**: importance (derived from statistical correlation between theme presence and Promoter/Detractor classification)
- Quadrant labels: **Protect** (high importance, high performance), **Act Now** (high importance, low performance), **Monitor** (low importance, low performance), **Leverage** (low importance, high performance)

### 3E: Churn Risk Flagging

- Identify Detractors with high lifetime value or strategic account status from context
- Flag Passives showing negative sentiment trajectory (sliding toward Detractor)
- Estimate revenue-at-risk using available customer value data

Apply any user-specific `instructions` from FutureProof context — including preferred taxonomies, executive audience tone, or segment definitions that override defaults.

## Step 4: Deliver Output

Produce a structured **NPS Analysis Briefing** containing the following sections:

### 1. Executive Summary (one page)
- Headline NPS with confidence interval and period-over-period delta
- Three most critical findings in ranked order
- Recommended immediate actions (≤30 days) with accountable function

### 2. Score Architecture
- Overall NPS and Promoter / Passive / Detractor composition (percentage and absolute count)
- Score distribution histogram
- Segment-level NPS table with variance flags

### 3. Thematic Driver Report
- **Driver Impact Matrix** with quadrant assignments
- Top 5 positive drivers with representative verbatims
- Top 5 negative drivers with root cause chains and representative verbatims

### 4. Churn Risk Register
- Table of at-risk segments or accounts: segment/account identifier, current score, trend direction, estimated revenue-at-risk, recommended intervention

### 5. Action Roadmap
- **Critical fixes (0–30 days)**: top 3 highest-impact interventions with specific, actionable descriptions (not generic recommendations) — e.g. "Redesign onboarding email sequence for [ICA segment] to address the 'unclear next steps' theme cited by 34% of Detractors in that cohort"
- **Strategic initiatives (30–90 days)**: systemic improvements mapped to root causes
- **Measurement cadence**: when and how to re-measure to validate impact

### 6. Appendix
- Methodology notes (sample size, confidence, coding taxonomy)
- Full theme frequency table
- Raw segment cross-tabulations

Format: deliver as a structured markdown document suitable for conversion to PDF or slide deck. If the user specified a downstream format (e.g. board deck, Jira tickets), adapt accordingly.

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
FutureProof:save_experiment(skill="nps-analyser", experiment={
  hypothesis: "Targeted closed-loop follow-up with Detractors within 48 hours of survey submission converts 20% to Passive or above within 60 days",
  variants: ["control: standard follow-up cadence", "variant: 48-hour personalised outreach referencing specific verbatim theme"],
  measurement: "Re-survey converted Detractors at 60 days; track retention rate delta vs. non-contacted Detractors",
  expected_impact: "5–8 point NPS uplift in targeted ICA segment and 10% reduction in segment churn rate"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="nps-analyser",
  query="Current NPS benchmarks by industry vertical 2024, closed-loop recovery programme best practices, and emerging alternatives or complements to NPS (e.g. Customer Effort Score, earned growth rate) with comparative validity evidence",
  reason="Ensure driver prioritisation reflects current benchmark context and that methodology recommendations incorporate evolving CX measurement best practice"
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
FutureProof:save_session(skill="nps-analyser", session={
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