---
name: lightning-launch
description: |
  Builds a complete 7-14 day offer launch — positioning thesis, naming,
  pricing, guarantee, day-by-day calendar, and full copy kit — in one
  session, ready to execute. Use when a user says "I want to launch this
  fast", "help me launch a new offer", "I need a launch plan by next
  week", or "go from idea to market-ready in days not weeks". For
  end-to-end launch execution, not standalone positioning, micro offers, or
  pricing-only work.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="lightning-launch")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. Pay particular attention to existing ICA definitions, prior offer structures, proven messaging angles, and any pricing experiments already in flight.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **What is the offer?** Describe the transformation, deliverable, or outcome the buyer receives.
- **Who is this for?** Specify the ICA segment — role, situation, and acute trigger that makes this urgent for them right now.
- **What is the launch timeline?** When do they need to be live and accepting buyers?
- **What existing assets do they have?** (e.g. waitlist, audience, email list size, prior testimonials, adjacent offers already selling)
- **What is the revenue target for this launch?** (unit price × number of buyers, or total figure)
- **What feels unresolved?** Naming, pricing, packaging, positioning, distribution — where is the friction?

If FutureProof context already contains ICA profiles, offer history, or brand voice guidelines, surface these and confirm whether they still apply.

## Step 3: Establish Offer–Market Fit Thesis

Before building any launch assets, pressure-test the core thesis:

1. **ICA Situation Audit** — Define the specific before-state: what is happening in the ICA's world that makes this offer necessary *now*? Map the external trigger (market shift, seasonal pressure, regulatory change) and the internal trigger (frustration, ambition, fear of falling behind).
2. **Transformation Statement** — Draft a single sentence: *"This offer takes [ICA] from [painful before-state] to [desirable after-state] in [timeframe/mechanism]."* Pressure-test for specificity — reject any version that could apply to a different offer in a different market.
3. **Competitive Displacement Check** — Identify the 2–3 alternatives the ICA is currently using (including doing nothing). Articulate the specific inadequacy of each alternative that this offer resolves.
4. **Objection Pre-Mortem** — List the top 5 objections the ICA will raise (price, timing, trust, complexity, priority) and draft a one-line neutraliser for each. Flag any objection that cannot be neutralised — this is a positioning gap that must be resolved before launch.

Apply any user-specific `instructions` from FutureProof context (e.g. brand voice, pricing philosophy, sales model preferences).

## Step 4: Build the Offer Architecture

Structure the offer into a launch-ready package:

### 4a. Naming & Framing
- Generate 3 candidate offer names scored against: memorability, outcome-clarity, ICA resonance, and differentiation. Recommend one.
- Write a 15-word positioning line (the sentence that goes below the name on every asset).

### 4b. Pricing & Packaging
- Define the value stack: list every tangible and intangible component the buyer receives.
- Assign an *anchor value* to each component (what it would cost separately or what outcome it protects/produces).
- Recommend a price point using the 10x–20x value-to-price ratio as a floor, adjusted for ICA segment willingness-to-pay and competitive displacement pricing.
- If appropriate, propose tiered packaging (e.g. core / premium / VIP) with clear fence attributes between tiers.

### 4c. Guarantee & Risk Reversal
- Draft a specific guarantee aligned with the transformation promise — avoid generic "money-back" language. The guarantee should name the outcome or milestone the buyer can expect.

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Create the Launch Sequence Plan

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Produce a day-by-day launch execution plan spanning **7–14 days** (calibrated to the user's stated timeline):

### Phase 1: Seed (Days 1–3)
- **Narrative seeding**: 3 content angles to publish across the user's primary channels that surface the ICA's problem without revealing the offer. Specify format (email, social post, short video) and hook line for each.
- **Warm outreach**: Draft a direct message or email template for 1:1 outreach to high-intent prospects from existing audience/list.

### Phase 2: Open (Days 4–7)
- **Launch announcement**: Write the full launch email/post — subject line, body, call to action. Structure: problem → agitation → transformation proof → offer reveal → bonuses → guarantee → CTA with deadline.
- **Sales page brief**: Outline the 12-section sales page structure (headline, sub-headline, problem narrative, ICA callout, transformation promise, mechanism, proof/testimonials, offer stack, pricing, guarantee, FAQ, CTA). Provide draft copy for the headline, sub-headline, and CTA sections.
- **Urgency architecture**: Define the real scarcity or deadline mechanism (cohort cap, bonus expiration, price increase) — must be truthful and enforceable.

### Phase 3: Convert (Days 8–14)
- **Objection-handling content calendar**: Map one piece of content per day to each of the top 5 objections from Step 3.
- **Social proof deployment plan**: Specify when and how to surface testimonials, case studies, or interim results.
- **Final 48-hour sequence**: Draft the close-of-cart email series (3 emails: reminder, objection-buster, final call).

## Step 6: Deliver Output

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


Produce the following structured deliverables:

### Deliverable 1: Lightning Launch Positioning Brief (1 page)
| Section | Content |
|---|---|
| Offer Name | Recommended name and positioning line |
| ICA Definition | Segment, situation, trigger |
| Transformation Statement | Single sentence |
| Before / After | Two-column state comparison |
| Competitive Displacement | Why this beats the 2–3 alternatives |
| Top 5 Objections + Neutralisers | Table format |
| Price Point | Recommended price with value-stack justification |
| Guarantee | Full guarantee statement |

### Deliverable 2: Launch Execution Calendar
Day-by-day table with columns: **Day**, **Phase**, **Action**, **Asset Required**, **Channel**, **Owner** (default: user, unless team roles are known from context).

### Deliverable 3: Launch Copy Kit
- Launch announcement email (full draft)
- Sales page headline + sub-headline + CTA (full draft)
- Warm outreach DM/email (full draft)
- Close-of-cart email series — 3 emails (full drafts)

### Deliverable 4: Launch Scorecard
Pre-populate a tracking sheet the user can fill post-launch:

| Metric | Target | Actual |
|---|---|---|
| List/audience reached | [from input] | |
| Sales page views | | |
| Sales page conversion rate | | |
| Units sold | [from revenue target] | |
| Revenue | [from revenue target] | |
| Cost per acquisition | | |
| Top-performing content piece | | |
| Top objection encountered | | |

## Step 7: Propose Experiments

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:save_experiment(skill="lightning-launch", experiment={
  hypothesis: "Leading the launch announcement with a specific ICA pain-point story rather than the offer reveal increases click-through to sales page",
  variants: ["control: offer-first announcement", "variant: pain-story-first announcement"],
  measurement: "click-through rate from launch email to sales page across first 48 hours",
  expected_impact: "20–30% improvement in email-to-page click-through rate"
})
```

```
FutureProof:save_experiment(skill="lightning-launch", experiment={
  hypothesis: "Adding a named-outcome guarantee (e.g. 'hit milestone X or we work with you until you do') increases conversion versus a standard refund guarantee",
  variants: ["control: 30-day money-back guarantee", "variant: named-outcome guarantee"],
  measurement: "sales page conversion rate and refund rate over first 30 buyers",
  expected_impact: "10–15% lift in conversion rate with no increase in refund rate"
})
```

## Step 8: Request Research

```
FutureProof:request_research(skill="lightning-launch",
  query="High-converting launch sequence structures, urgency mechanisms, and offer positioning frameworks for digital and service-based businesses 2024–2025",
  reason="Ensure launch playbook reflects current buyer behaviour, attention economics, and platform algorithm changes affecting organic launch reach"
)
```

```
FutureProof:request_research(skill="lightning-launch",
  query="Pricing psychology for new offer launches — anchoring, decoy pricing, and tiered packaging effectiveness by ICA segment and price band",
  reason="Refine pricing and packaging recommendations with evidence-based frameworks rather than heuristic rules"
)
```

## Step 9: Save Session

```
FutureProof:save_session(skill="lightning-launch", session={
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