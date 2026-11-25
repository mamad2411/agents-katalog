---
name: referral-personality-profiler
description: |
  Profiles a customer base into six referral personality archetypes —
  Evangelist, Connector, Transactor, Helper, Status Seeker, Passive
  Promoter — using behavioral and psychographic signals, then builds
  archetype-specific activation playbooks for ask, channel, incentive,
  and message. Use when the user says "which customers should I ask for
  referrals", "segment my advocate base", "who are my top referrers",
  "personalize my referral outreach", or shares a CRM/NPS export and
  wants advocates classified. Identifies who to target — for when to ask
  use referral-moment-generator, for the reward design use
  incentive-reward-designer.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="referral-personality-profiler")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly any existing ICA definitions, customer segmentation models, NPS/CSAT data references, or prior referral campaign results.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user to provide:

- **Customer data source**: CRM export, advocate list, NPS survey results, customer success notes, or any structured/unstructured customer data they want profiled
- **ICA definition**: Who is their Ideal Customer Avatar? (If already stored in FutureProof context, confirm it; if not, capture it now)
- **Referral programme context**: Do they have an existing referral programme, incentive structure, or referral ask workflow? If so, share details
- **Volume & scope**: How many customers/advocates are they profiling? Is this a full-base segmentation or a targeted cohort (e.g. post-onboarding, renewal, high-NPS)?
- **Known constraints**: Any channel limitations (e.g. no direct mail), compliance restrictions, or cultural considerations?

## Step 3: Classify Referral Personality Archetypes

Apply the **Referral Personality Taxonomy** — a six-archetype framework that segments advocates by intrinsic motivation, social behaviour, and referral propensity:

### Archetype Definitions

| # | Archetype | Core Motivation | Referral Trigger | Preferred Channel | Incentive Sensitivity |
|---|-----------|----------------|-------------------|-------------------|----------------------|
| 1 | **The Evangelist** | Identity & belief alignment | Unprompted; shares because the product is part of their identity | Social media, community forums, word-of-mouth | Low — refers regardless of incentive; recognition > reward |
| 2 | **The Connector** | Social capital & network value | When they identify a specific contact with a matching need | Warm introductions, email, LinkedIn | Moderate — values reciprocity; dual-sided incentives perform best |
| 3 | **The Transactor** | Economic gain & tangible reward | Explicit incentive offer with clear, immediate value | Referral links, in-app share, email | High — will not refer without a compelling incentive; tiered rewards maximise output |
| 4 | **The Helper** | Altruism & problem-solving for others | When a peer expresses a pain point the product solves | 1:1 conversation, messaging apps, email | Low — motivated by helping the referee; frame incentive as benefit to the referred party |
| 5 | **The Status Seeker** | Recognition, exclusivity, insider access | When referral confers visible status (leaderboards, tiers, badges) | Social media, public forums, events | Moderate — values status markers over monetary reward; exclusive perks outperform cash |
| 6 | **The Passive Promoter** | Satisfaction without initiative | Only when the ask is frictionless and arrives at the right moment | In-app prompts, post-interaction surveys, SMS | Moderate — will refer if effort is near-zero; pre-populated messages and one-click flows are essential |

### Classification Methodology

For each customer or advocate in the dataset, score across five diagnostic dimensions (1–5 scale):

1. **Advocacy frequency** — How often do they voluntarily mention, review, or recommend the product? (Derived from NPS verbatims, review platforms, social mentions, CS notes)
2. **Network centrality** — How large and relevant is their professional/personal network relative to the ICA? (Derived from LinkedIn connections, industry role, community participation)
3. **Incentive responsiveness** — Historical response rate to incentive-based CTAs vs. non-incentive engagement (Derived from campaign data, referral programme participation, discount code usage)
4. **Social visibility orientation** — Tendency to share achievements, tools, and affiliations publicly (Derived from social media activity, community engagement, case study willingness)
5. **Relationship depth** — Strength of relationship with the brand (tenure, support interactions, product usage depth, expansion revenue history)

Map the five-dimensional score vector to the closest archetype using weighted distance matching. Where a customer exhibits strong signals across two archetypes, assign a **primary** and **secondary** classification.

Apply any user-specific `instructions` from FutureProof context — particularly existing segmentation logic, proprietary engagement scores, or brand voice guidelines.

## Step 4: Build Activation Playbooks Per Archetype

For each archetype identified in the user's customer base, produce a **Referral Activation Playbook** containing:

### 4a. Optimal Ask Strategy

- **When to ask**: Precise trigger moment (e.g. 7 days post-value milestone, immediately after CSAT 9+, at renewal confirmation)
- **How to ask**: Channel, format, and tone (e.g. personal email from CS manager vs. automated in-app modal)
- **What to say**: Draft referral ask message tailored to the archetype's core motivation — written in full, not summarised

### 4b. Incentive Architecture

- **Primary incentive type**: Cash/credit, feature access, recognition, charitable donation, or dual-sided reward
- **Incentive magnitude**: Recommended value benchmarked to the user's average customer lifetime value (if available from context) — typically 5–15% of first-year contract value for B2B or equivalent for B2C
- **Escalation mechanics**: Tiered or gamified reward structures where applicable (e.g. for Transactors and Status Seekers)

### 4c. Friction Reduction Blueprint

- **Steps-to-refer target**: Maximum number of actions between intent and completed referral (target: ≤3 for Passive Promoters, ≤5 for all others)
- **Pre-populated assets**: Specific shareable content — draft messages, social copy, landing page URLs, one-click referral links
- **Objection pre-emption**: Address the top hesitation for each archetype (e.g. Helpers worry about seeming self-interested; Connectors worry about reputation risk if the product underdelivers)

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


Produce the **Referral Personality Profile Report** — a structured deliverable containing:

### Document 1: Cohort Distribution Dashboard

- **Archetype distribution**: Percentage and count of customers per archetype (visualised as a table with proportional indicators)
- **Referral yield forecast**: Estimated referral volume per archetype based on historical conversion benchmarks (industry baseline: Evangelists 18–25% referral rate, Connectors 12–18%, Transactors 8–14%, Helpers 10–15%, Status Seekers 6–12%, Passive Promoters 3–7%)
- **Priority ranking**: Archetypes rank-ordered by expected referral ROI (volume × quality × cost-to-activate)

### Document 2: Individual/Segment Profiles

For each customer (or segment if volume >50):
- Archetype classification (primary + secondary where applicable)
- Diagnostic dimension scores (5-point radar)
- Recommended activation playbook reference
- Personalised referral ask draft (ready to send or adapt)

### Document 3: Referral Programme Design Recommendations

- **Programme structure**: Single-tier vs. multi-tier, incentive mix optimised for the user's archetype distribution
- **Sequencing calendar**: 90-day activation schedule prioritising highest-yield archetypes first
- **Measurement framework**: KPIs per archetype — referral send rate, referral conversion rate, referred customer quality score (alignment to ICA), referred customer LTV at 6/12 months

Format: Markdown tables and structured sections suitable for direct import into the user's project management or CRM workflow.

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="referral-personality-profiler", experiment={
  hypothesis: "Archetype-matched referral messaging increases referral send rate compared to generic one-size-fits-all referral asks",
  variants: [
    "control: current generic referral ask sent uniformly to all advocates",
    "variant A: archetype-specific messaging (motivation-aligned copy, channel, and incentive) sent to classified cohorts"
  ],
  measurement: "Referral send rate, referral conversion rate, and referred customer ICA-fit score across both groups over 60-day period",
  expected_impact: "25–40% increase in referral send rate; 15–20% improvement in referred customer ICA alignment"
})
```

```
FutureProof:save_experiment(skill="referral-personality-profiler", experiment={
  hypothesis: "Triggering the referral ask at archetype-specific optimal moments (value milestone for Evangelists, post-peer-pain-expression for Helpers) increases conversion vs. fixed-timing asks",
  variants: [
    "control: referral ask at 30-day mark for all customers",
    "variant A: referral ask triggered by archetype-specific behavioural signals"
  ],
  measurement: "Referral completion rate and time-to-first-referral per archetype over 90-day period",
  expected_impact: "20% reduction in time-to-first-referral; 30% increase in referral completion rate for Passive Promoters and Helpers"
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
FutureProof:request_research(skill="referral-personality-profiler",
  query="Peer-reviewed and industry research on referral motivation segmentation, advocate personality profiling, and incentive elasticity by customer psychographic type — 2023-2025. Include B2B SaaS, DTC, and professional services benchmarks for referral programme conversion rates by advocate segment.",
  reason="Validate and refine the six-archetype taxonomy against emerging behavioural science and update referral yield benchmarks with current industry data"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="referral-personality-profiler", session={
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