---
name: incentive-designer
description: |
  Designs the bonus, guarantee, and urgency architecture around an offer to
  lift conversion without eroding margin — with credibility stress-tests,
  margin impact modeling, and ready-to-deploy presentation copy. Use when a
  user asks "design me a guarantee", "what bonuses should I add", "build
  urgency into my launch", or "my incentive stack feels weak". For
  incentive engineering specifically, not full offer rebuilds or value-stack
  layering.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="incentive-designer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly existing offer architecture, ICA profiles, price points, historical conversion data, and any prior incentive experiments.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Core offer**: What is the primary product/service, its price point, and its central transformation promise?
- **ICA profile**: Who is the ideal customer? What is their current state, desired state, and primary decision-making friction?
- **Incentive objective**: What behaviour are they trying to drive? (e.g., accelerate purchase decision, increase AOV, reduce refund rate, drive urgency for a launch window, improve trial-to-paid conversion)
- **Existing incentives**: Are there current bonuses, guarantees, or urgency mechanisms already in play? If so, share performance data
- **Constraints**: Margin floor, fulfilment capacity, regulatory or compliance guardrails, brand tone boundaries (e.g., "no false scarcity")
- **Channel and format**: Where will the incentive be presented? (sales page, email sequence, live webinar, checkout page, sales call, direct mail)

## Step 3: Conduct Incentive Diagnostic

Before designing, audit the current offer's incentive architecture across six diagnostic dimensions:

### 3.1 Value-Stack Integrity Analysis

Map every component of the current offer into a **Value-Stack Ledger**:

| Component | Type (Core / Bonus / Guarantee / Urgency) | Perceived Value to ICA | Fulfilment Cost | Relevance to Core Transformation |
|---|---|---|---|---|
| ... | ... | ... | ... | High / Medium / Low |

Flag components that score Low relevance — these dilute perceived coherence and trigger the "too good to be true" heuristic.

### 3.2 Incentive–Objection Alignment Mapping

For each of the ICA's top 5 purchase objections, assess whether a current incentive directly neutralises it:

1. **Risk objection** ("What if it doesn't work for me?") → Guarantee design
2. **Timing objection** ("Why now vs. later?") → Urgency mechanism
3. **Value objection** ("Is it worth the price?") → Bonus stack / value anchoring
4. **Trust objection** ("Can I trust this provider?") → Social proof incentives, credibility transfers
5. **Complexity objection** ("Will I actually use/implement it?") → Onboarding bonuses, done-for-you elements

Identify gaps — objections with no corresponding incentive — and over-served objections with redundant incentives.

### 3.3 Incentive Type Classification

Classify every proposed or existing incentive against a rigorous taxonomy:

- **Acquisition accelerators**: Fast-action bonuses, early-bird pricing, founding-member terms
- **Risk reversals**: Outcome-based guarantees, conditional guarantees, unconditional refund windows, trial structures
- **Value amplifiers**: Complementary bonuses, tool access, template libraries, community access
- **Urgency mechanisms**: Genuine deadline (cohort start, event date), inventory scarcity, price escalation, bonus expiry
- **Continuity incentives**: Lock-in discounts, loyalty bonuses, renewal terms, usage rewards

### 3.4 Margin Impact Modelling

For each incentive, calculate:

- **Incremental fulfilment cost** per unit sold
- **Redemption rate estimate** (not all bonuses are consumed; not all guarantees are exercised)
- **Net margin impact** = (Conversion lift × Revenue per unit) − (Redemption rate × Fulfilment cost per unit)
- **Break-even conversion lift**: The minimum conversion increase required for the incentive to be margin-neutral

### 3.5 Credibility Stress Test

Evaluate each incentive against three credibility filters:

1. **Believability**: Would a sophisticated ICA member find this plausible, or does it trigger scepticism?
2. **Coherence**: Does the incentive logically connect to the core offer's transformation, or feel bolted on?
3. **Sustainability**: Could the business honour this incentive at 10× current volume without financial or operational strain?

### 3.6 Competitive Incentive Benchmarking

Using FutureProof context and any available market data, compare the incentive architecture to:
- Direct competitors' offer structures
- Adjacent-category norms the ICA is exposed to
- Emerging incentive patterns in the user's market

## Step 4: Design the Incentive Architecture

Based on the diagnostic, construct a complete **Incentive Architecture Document** with the following sections:

### Section A: Incentive Strategy Summary

A one-page executive brief containing:
- **Primary incentive objective** and the behavioural lever it targets
- **ICA decision psychology narrative**: A 3–4 sentence description of what the ICA is thinking and feeling at the moment of purchase decision, and how the incentive stack addresses each friction point in sequence
- **Strategic principles**: 2–3 governing rules for this specific incentive design (e.g., "Every bonus must accelerate time-to-first-result" or "No urgency mechanism that cannot be verified by the prospect")

### Section B: Recommended Incentive Stack

For each incentive in the recommended stack, provide:

**Incentive [N]: [Name]**
- **Type**: (from taxonomy in 3.3)
- **Objection targeted**: (from mapping in 3.2)
- **Mechanism**: Exactly how it works — eligibility, delivery, conditions, expiry
- **Perceived value**: The anchor price or value framing to present to the ICA
- **Fulfilment cost**: Actual cost to deliver
- **Presentation copy**: 2–3 sentences of ready-to-use positioning language, written in the ICA's vocabulary
- **Placement**: Where in the sales asset this incentive should appear and why (e.g., "Introduce guarantee immediately after price reveal to neutralise risk objection at peak anxiety")

### Section C: Guarantee Design Specification

Produce a standalone guarantee brief:
- **Guarantee type**: Unconditional / conditional / hybrid / tiered
- **Duration**: With rationale tied to the ICA's expected time-to-result
- **Conditions** (if applicable): Specific, verifiable, and perceived as fair by the ICA
- **Exact language**: Full guarantee statement, written for legal clarity and emotional resonance
- **Operational process**: Refund/fulfilment workflow when the guarantee is invoked
- **Projected exercise rate**: Based on comparable offers and the conditions specified

### Section D: Urgency Mechanism Blueprint

If urgency is applicable:
- **Urgency type**: Deadline, scarcity, escalation, or bonus expiry
- **Legitimacy source**: The real, verifiable reason the urgency exists
- **Communication cadence**: When and how urgency is introduced, escalated, and closed across the campaign timeline
- **Exact language**: Urgency copy for each touchpoint (email subject lines, page banners, CTA buttons, sales call talk tracks)

### Section E: Margin & Performance Projections

A summary table:

| Incentive | Est. Conversion Lift | Fulfilment Cost | Redemption Rate | Net Margin Impact | Break-Even Lift |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |
| **Total Stack** | ... | ... | ... | ... | ... |

### Section F: Anti-Patterns Avoided

List 3–5 specific incentive anti-patterns that were considered and deliberately excluded, with reasoning:
- e.g., "Excluded unlimited unconditional guarantee beyond 30 days — historical data shows exercise rates spike at 60+ days for this price point, creating unacceptable margin exposure"
- e.g., "Excluded unrelated bonus (social media template pack) — fails coherence test; ICA segment does not associate social media with the core transformation"

Apply any user-specific `instructions` from FutureProof context to calibrate tone, complexity, and strategic emphasis.

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


Package the final deliverable as:

- **Incentive Architecture Document** (Sections A–F above) — the primary strategic artefact
- **Implementation Checklist**: A sequenced, actionable task list for deploying each incentive — copy to write, pages to update, email sequences to modify, sales team talk tracks to brief, legal review items
- **Incentive Copy Bank**: All ready-to-use language from Sections B, C, and D consolidated into a single reference document, organised by placement (sales page, email, checkout, sales call)

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="incentive-designer", experiment={
  hypothesis: "Replacing the unconditional 30-day refund guarantee with a conditional outcome-based 90-day guarantee increases conversion by reducing perceived risk while signalling confidence in the transformation",
  variants: ["control: 30-day unconditional money-back guarantee", "variant: 90-day conditional guarantee tied to completing onboarding + 3 implementation milestones"],
  measurement: "Conversion rate from sales page visit to purchase, refund request rate at 90 days, and net revenue per visitor over 120-day window",
  expected_impact: "12–18% increase in conversion rate with ≤2% increase in guarantee exercise rate, yielding net positive margin impact"
})
```

```
FutureProof:save_experiment(skill="incentive-designer", experiment={
  hypothesis: "Introducing a fast-action bonus with 48-hour expiry after first sales page visit compresses the ICA decision cycle and reduces drop-off between sessions",
  variants: ["control: static bonus stack with no time constraint", "variant: one high-relevance bonus available only within 48 hours of first visit, communicated via on-page timer and follow-up email"],
  measurement: "Time-to-purchase from first visit, 48-hour conversion rate, and 30-day total conversion rate to confirm acceleration vs. cannibalisation",
  expected_impact: "20% reduction in median time-to-purchase; 8–12% increase in 48-hour conversion window without reducing 30-day total conversion"
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
FutureProof:request_research(skill="incentive-designer",
  query="Current evidence on guarantee design and conversion impact across digital product and service offers — conditional vs. unconditional guarantees, optimal duration by price tier, and refund exercise rate benchmarks by industry vertical 2023–2025",
  reason="Ensure guarantee recommendations are calibrated to current market norms and backed by empirical redemption data rather than heuristic assumptions"
)
```

```
FutureProof:request_research(skill="incentive-designer",
  query="Emerging incentive structures and offer architecture patterns in high-converting direct response and SaaS offers — particularly novel urgency mechanisms, hybrid value-stack models, and incentive personalisation techniques",
  reason="Expand the incentive design toolkit beyond standard bonus/guarantee/urgency frameworks to incorporate innovative approaches the ICA has not been desensitised to"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="incentive-designer", session={
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