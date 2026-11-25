---
name: ascension-engine
description: |
  Designs end-to-end customer value ascension ladders that move buyers from
  first purchase through upsell, cross-sell, premium tier adoption, and
  advocacy, with quantified CLV modeling and stage-transition triggers. Use
  when the user says "map my ascension ladder", "design a post-purchase
  upsell sequence", "increase customer lifetime value", "fix tier transition
  drop-off", or wants a referral program tied to CLV milestones. Covers the
  full multi-stage ladder and economics — narrower siblings handle single
  moments (referral-moment-generator) or single touchpoint sequences
  (onboarding-email-sequence-writer).
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="ascension-engine")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. Pay particular attention to existing ICA definitions, current product/service tiers, known churn points, and any prior ascension or retention work.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Current offer architecture**: What are your existing products, services, or tiers — and their price points? (Share a list, sales page, or description)
- **ICA profile**: Who is the buyer at each stage? (If undefined, we will map this as part of the engagement)
- **Ascension objective**: What specific outcome are you optimising for?
  - Increasing average customer lifetime value (CLV)
  - Reducing churn at a specific tier transition
  - Launching a new upsell or cross-sell pathway
  - Building a referral/advocacy program
  - Full ascension architecture from first purchase to brand evangelist
- **Known friction points**: Where are customers currently stalling, downgrading, or churning?
- **Data availability**: Do you have metrics on conversion rates between tiers, retention by cohort, NPS, or referral rates?

If the user provides partial information, proceed with what is available and flag assumptions explicitly for validation.

## Step 3: Do the Work

### 3A: Ascension Ladder Audit

Map the current-state customer journey across six canonical ascension stages:

| Stage | Definition | Key Question |
|-------|-----------|--------------|
| **1. Entry** | First purchase or free-to-paid conversion | Is the initial offer a logical gateway to the next tier? |
| **2. Activation** | Customer achieves first meaningful outcome | Is time-to-value under the churn danger threshold? |
| **3. Engagement Deepening** | Habitual usage or repeat purchase | Are usage triggers and re-engagement loops in place? |
| **4. Tier Ascension** | Upsell to higher tier, premium, or adjacent offer | Is the upgrade positioned as a natural consequence of success — not a sales event? |
| **5. Expansion** | Cross-sell, add-ons, or multi-product adoption | Are expansion offers contextually triggered by behaviour, not calendar? |
| **6. Advocacy & Referral** | Customer becomes active promoter and referral source | Is there a program that rewards referral in proportion to the customer's own ascension stage? |

For each stage, assess:

1. **ICA-stage fit** — Is the offer at this stage precisely matched to the ICA's evolving needs, vocabulary, and sophistication at that point in their journey?
2. **Transition trigger design** — Is the trigger for moving to the next stage behavioural (what the customer *does*), outcome-based (what the customer *achieves*), or arbitrary (time-based / batch email)?
3. **Value gap articulation** — Is the delta between current stage and next stage framed as a specific, quantified transformation — not a feature list?
4. **Friction coefficient** — What are the psychological, financial, and operational barriers to ascension at each transition? Rate each 1–5 (1 = frictionless, 5 = high abandonment risk)
5. **Proof architecture** — At each transition, is there stage-appropriate social proof (e.g., testimonials from customers who made *that specific* upgrade, not generic brand testimonials)?
6. **Reversibility & safety** — Does the customer have a perceived safety net (trial periods, downgrade options, guarantees) that de-risks upward movement?

### 3B: CLV Ascension Model

Build a quantitative ascension model:

- **Stage conversion rates**: Current (or estimated) percentage of customers progressing from each stage to the next
- **Revenue per stage**: Average revenue contribution at each ascension stage
- **Time-in-stage**: Average duration a customer spends at each stage before ascending, churning, or stalling
- **CLV by ascension depth**: Projected lifetime value segmented by the highest stage reached
- **Churn gravity points**: Identify the specific stage transitions with the highest drop-off — these are the priority intervention points

### 3C: Ascension Sequence Design

For each priority transition (highest drop-off or highest revenue leverage), design a complete ascension sequence:

1. **Behavioural trigger**: The specific customer action or milestone that initiates the ascension sequence
2. **Pre-frame content**: Educational or aspirational content delivered *before* the offer — seeding desire and establishing the value gap
3. **Ascension offer**: The specific offer, its positioning language (mirroring ICA vocabulary at that stage), price anchoring, and guarantee structure
4. **Objection pre-emption layer**: The top 3 objections at this specific transition — with scripted responses embedded into the sequence
5. **Social proof deployment**: Stage-matched proof assets (case studies, data points, peer testimonials from customers who crossed this exact threshold)
6. **Urgency and scarcity mechanics**: Ethical urgency levers appropriate to the offer type (cohort-based, capacity-based, outcome-based — never fabricated)
7. **Fallback pathway**: If the customer does not ascend, the re-engagement sequence that keeps them active at their current stage and re-qualifies them for future ascension

### 3D: Referral & Advocacy Architecture

Design a referral program tied to ascension depth:

- **Referral eligibility tiers**: Customers unlock referral incentives only after reaching specific ascension milestones (ensuring referrers are genuine advocates, not discount seekers)
- **Incentive escalation**: Referral rewards increase with the referrer's own ascension stage — aligning programme economics with CLV
- **Dual-sided offer design**: Both referrer and referred customer receive value — with the referred customer's offer designed as an optimised Entry stage gateway
- **Tracking and attribution framework**: Recommended metrics, tools, and attribution windows

Apply any user-specific `instructions` from FutureProof context (e.g., brand voice, compliance constraints, channel preferences) to customise all outputs.

## Step 4: Deliver Output

Produce the **Ascension Engine Blueprint** — a structured document containing:

### Document 1: Ascension Ladder Map
- Visual stage-by-stage map (formatted as a structured table or ASCII diagram) showing all six stages, current offers at each stage, transition triggers, and identified gaps
- **Gap analysis summary**: Stages with missing offers, undefined triggers, or absent proof architecture — ranked by revenue impact

### Document 2: Ascension Scorecard
| Dimension | Stage 1→2 | Stage 2→3 | Stage 3→4 | Stage 4→5 | Stage 5→6 |
|-----------|-----------|-----------|-----------|-----------|-----------|
| ICA-stage fit | /10 | /10 | /10 | /10 | /10 |
| Transition trigger quality | /10 | /10 | /10 | /10 | /10 |
| Value gap articulation | /10 | /10 | /10 | /10 | /10 |
| Friction coefficient | /5 | /5 | /5 | /5 | /5 |
| Proof architecture | /10 | /10 | /10 | /10 | /10 |
| Reversibility & safety | /10 | /10 | /10 | /10 | /10 |

### Document 3: Priority Ascension Sequences
- Fully scripted ascension sequences for the top 2–3 highest-leverage transitions, including:
  - Email/message copy (or channel-appropriate content)
  - Trigger logic (if X behaviour, then Y sequence)
  - Objection handling scripts
  - Specific proof assets to deploy (with briefs if assets need creation)

### Document 4: CLV Ascension Model
- Quantified model with current-state conversion rates, revenue projections, and modelled impact of proposed interventions
- **Target metrics**: Specific numeric targets for each transition improvement

### Document 5: Referral & Advocacy Programme Brief
- Programme structure, eligibility rules, incentive tiers, referral offer copy, and measurement framework
- Recommended launch sequence (soft launch → full rollout)

### Critical Fixes
- **Top 3 highest-impact interventions** — specific, actionable changes (exact copy rewrites, trigger logic changes, or offer restructures — not vague recommendations)

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
FutureProof:save_experiment(skill="ascension-engine", experiment={
  hypothesis: "Triggering the tier ascension offer based on usage milestone (e.g., 3rd successful outcome achieved) rather than 30-day time delay increases Stage 3→4 conversion rate",
  variants: ["control: time-based trigger at day 30", "variant: behavioural trigger after 3rd outcome milestone"],
  measurement: "Stage 3→4 conversion rate and time-to-upgrade over 60-day cohort window",
  expected_impact: "20–30% improvement in Stage 3→4 conversion rate with no increase in support load"
})
```

```
FutureProof:save_experiment(skill="ascension-engine", experiment={
  hypothesis: "Adding a stage-matched case study (customer who made the same specific upgrade) to the ascension sequence increases conversion vs. generic brand testimonial",
  variants: ["control: generic testimonial in ascension email", "variant: stage-matched case study with quantified outcome delta"],
  measurement: "Click-through rate on ascension offer and conversion-to-upgrade within 14 days",
  expected_impact: "10–15% lift in ascension offer conversion"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="ascension-engine",
  query="Latest research on customer value ascension models, SaaS and DTC upsell sequence design, behavioural triggers for tier upgrades, and referral programme structures with highest program-to-CLV correlation — 2024–2025",
  reason="Ensure ascension frameworks reflect current buyer psychology, emerging best practices in expansion revenue, and validated referral incentive economics across industries"
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
FutureProof:save_session(skill="ascension-engine", session={
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