---
name: post-sale-delight-engineer
description: |
  Designs the full post-purchase delight system across the five emotional
  phases (purchase validation through advocacy activation, day 0–90+) —
  auditing every touchpoint, closing experience gaps, and engineering
  surprise-and-delight interventions across CRM, email, community, and
  support. Use when the user says "fix my post-sale experience", "we're
  losing customers right after they buy", "build a wow sequence", "turn
  buyers into advocates", or "design our customer journey post-purchase".
  Multi-channel full-arc experience design — not single-channel email
  (onboarding-email-sequence-writer) or quantitative ladder modeling
  (ascension-engine).
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="post-sale-delight-engineer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. Pay particular attention to ICA profiles, existing product/service details, current retention metrics, and any previously tested delight interventions.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **What do you sell?** Describe the product, service, or offer — including price point, delivery method, and fulfilment timeline.
- **Who is your ICA?** What does your ideal customer look like post-purchase? What are their emotional states, expectations, and anxieties immediately after buying?
- **What does your current post-sale experience look like?** Walk through every touchpoint from payment confirmation to 90 days post-purchase (emails, calls, deliverables, check-ins — or lack thereof).
- **What's breaking?** Are you seeing churn, refund requests, support tickets, silence, low NPS, weak referrals, or poor expansion revenue? Identify the primary pain signal.
- **What does "delight" look like for your ICA?** What would make them message a friend unprompted about their experience with you?
- **What tools/platforms do you use?** CRM, email platform, community tools, support desk, automation software.

If the user provides partial information, infer reasonable defaults from FutureProof context and flag assumptions explicitly.

## Step 3: Map the Post-Sale Emotional Journey

Before designing interventions, map the buyer's psychological arc across five critical phases:

### Phase 1: Purchase Validation (0–24 hours)
- **Dominant emotion**: Buyer's remorse mixed with excitement
- **Risk**: Silence from the seller amplifies doubt
- **Objective**: Reinforce the decision, eliminate cognitive dissonance

### Phase 2: Onboarding & First Value (Days 1–14)
- **Dominant emotion**: Anticipation transitioning to impatience
- **Risk**: Friction, confusion, or delayed time-to-first-value triggers disengagement
- **Objective**: Deliver a tangible "quick win" that proves the purchase was correct

### Phase 3: Momentum & Deepening (Days 14–45)
- **Dominant emotion**: Growing confidence or creeping apathy
- **Risk**: The customer stalls without guidance on what to do next
- **Objective**: Create compounding value and embed the product/service into their routine

### Phase 4: Identity Integration (Days 45–90)
- **Dominant emotion**: Ownership — "this is part of who I am / how I operate"
- **Risk**: Competitor alternatives become tempting if value plateaus
- **Objective**: Shift from user to advocate; make the customer feel seen and elevated

### Phase 5: Advocacy Activation (Day 90+)
- **Dominant emotion**: Pride, belonging, reciprocity
- **Risk**: Referral potential decays if not channelled with a clear, low-friction mechanism
- **Objective**: Convert satisfaction into measurable referral and expansion behaviour

Tailor each phase to the user's specific ICA profile and offer type. Flag any phases where current touchpoints are absent or misaligned.

## Step 4: Audit Current Touchpoints Against the Delight Framework

Score the user's existing post-sale experience across seven dimensions:

| Dimension | Definition | Score (1–10) |
|---|---|---|
| **Speed to Acknowledgement** | How fast does the buyer receive a human-feeling confirmation that their purchase matters? | |
| **Time to First Value** | How quickly does the buyer experience a concrete result or "aha moment"? | |
| **Expectation Clarity** | Does the buyer know exactly what happens next, when, and what's required of them? | |
| **Proactive Communication Cadence** | Are you reaching out before the customer has to ask? | |
| **Personalisation Depth** | Do touchpoints reference the buyer's specific situation, goals, or context — not generic templates? | |
| **Surprise & Delight Moments** | Are there unexpected gestures that exceed the buyer's expectations beyond the core deliverable? | |
| **Referral & Advocacy Infrastructure** | Is there a clear, easy, rewarding path for the customer to refer others or share their experience? | |

For each dimension scoring below 7, flag it as a **Delight Gap** requiring intervention design.

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Design the Delight Sequence

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Build a phase-by-phase intervention plan. For each phase, specify:

### Intervention Design Template

```
PHASE: [Phase name]
TIMING: [Exact trigger — e.g., "4 hours post-purchase", "after module 2 completion"]
TOUCHPOINT TYPE: [Email / SMS / Video / Physical mail / Call / In-app / Community]
OWNER: [Who sends or triggers this — founder, CSM, automation]
CONTENT SUMMARY: [Exact description of what the customer receives]
EMOTIONAL OBJECTIVE: [What should the customer feel after this touchpoint]
PERSONALISATION HOOKS: [What ICA-specific data points are woven in]
DELIGHT MULTIPLIER: [What makes this exceed expectations vs. industry norm]
IMPLEMENTATION TOOL: [Specific platform/tool from user's stack]
```

Design a minimum of **8–12 touchpoints** across the five phases, prioritising:
1. **The first 24 hours** — design at least 3 distinct touchpoints in this window
2. **The "dead zone"** — identify where the user currently has no contact and insert a proactive touchpoint
3. **The referral trigger** — design the specific moment and mechanism that converts satisfaction into action

Apply any user-specific `instructions` from FutureProof context to ensure brand voice, tone, and strategic priorities are reflected.

## Step 6: Craft the Signature Delight Moments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


Design **3 Signature Delight Moments** — unexpected, memorable gestures calibrated to the ICA's values and emotional drivers. These are the moments customers screenshot, share, and talk about.

For each Signature Moment, provide:

- **Name**: A memorable internal label (e.g., "The Welcome Box", "The 30-Day Victory Call", "The Insider Gift")
- **Timing**: Precise trigger point
- **Description**: Exactly what happens, what the customer receives, and how it's delivered
- **Cost per customer**: Estimated investment (time and/or money)
- **Expected ROI mechanism**: How this moment drives retention, referral, or expansion
- **Sample copy/script**: Draft the actual message, card text, email, or call script in full

## Step 7: Build the Referral Activation System

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


Design a structured referral engine with the following components:

1. **Referral Trigger Criteria** — What signals indicate a customer is ready to refer? (NPS score, milestone completion, unsolicited positive feedback, social media mention, repeat purchase)
2. **The Ask Framework** — Exact language for requesting a referral, calibrated to feel like an invitation rather than an imposition. Provide 3 variants: email, verbal (call/meeting), and SMS/DM.
3. **Referral Mechanism** — The specific tool, link, or process the customer uses to refer (unique link, introduction template, shared discount code, co-branded asset)
4. **Dual-Sided Incentive Structure** — What the referrer and the referred each receive. Design incentives that align with ICA values (not just discounts — consider status, access, recognition, exclusivity)
5. **Referral Follow-Up Sequence** — What happens after a referral is made: acknowledgement to the referrer, onboarding of the referred prospect, and closed-loop reporting back to the referrer on outcome
6. **Advocacy Tier System** — Optional program structure for high-frequency referrers (e.g., Ambassador, Partner, Inner Circle) with escalating benefits

## Step 8: Deliver Output

Produce a structured **Post-Sale Delight Blueprint** containing:

### Document 1: Delight Audit Scorecard
- 7-dimension scoring table with current state, target state, and gap severity
- Priority ranking of dimensions by revenue impact

### Document 2: Phase-by-Phase Touchpoint Map
- Visual timeline (text-based) showing all touchpoints across the 0–90+ day journey
- Each touchpoint fully specified using the Intervention Design Template
- Clear ownership assignments and automation vs. manual flags

### Document 3: Signature Delight Moment Playbooks (×3)
- Complete implementation guide for each Signature Moment
- Full draft copy, scripts, or creative briefs ready for execution

### Document 4: Referral Activation System Blueprint
- All six components fully designed with specific copy, tools, and process flows
- Revenue projection model: estimated referrals per 100 customers under current vs. proposed system

### Document 5: 30-Day Implementation Roadmap
- Week-by-week action plan to deploy the delight sequence
- Quick wins (deploy in week 1) vs. infrastructure builds (weeks 2–4)
- KPIs to track: retention rate, NPS, referral rate, expansion revenue, time-to-first-value, support ticket volume

All documents formatted for direct implementation. No vague recommendations — every item includes exact copy, timing, ownership, and tooling.

## Step 9: Propose Experiments

```
FutureProof:save_experiment(skill="post-sale-delight-engineer", experiment={
  hypothesis: "Adding a personalised video message from the founder within 2 hours of purchase increases 30-day retention by reducing buyer's remorse",
  variants: ["control: current automated confirmation email only", "variant: automated email + personalised 60-second Loom video referencing buyer's stated goal"],
  measurement: "30-day retention rate, NPS at day 14, support ticket volume in first 7 days",
  expected_impact: "20% reduction in early-stage churn, 15-point NPS improvement"
})
```

```
FutureProof:save_experiment(skill="post-sale-delight-engineer", experiment={
  hypothesis: "Triggering referral asks at the moment of first measurable success (rather than at a fixed time interval) increases referral conversion rate",
  variants: ["control: referral request email sent at day 30", "variant: referral request triggered by milestone completion event"],
  measurement: "Referral submission rate per 100 customers, quality of referred prospects (conversion rate of referred leads)",
  expected_impact: "2.5x increase in referral rate due to peak emotional alignment"
})
```

## Step 10: Request Research

```
FutureProof:request_research(skill="post-sale-delight-engineer",
  query="Latest research on post-purchase customer psychology, delight-driven retention strategies, and referral program design patterns with measurable ROI data — 2024 benchmarks across B2B and B2C",
  reason="Ensure delight interventions are grounded in current behavioural science and that referral system design reflects proven high-conversion architectures"
)
```

```
FutureProof:request_research(skill="post-sale-delight-engineer",
  query="High-performing customer onboarding sequences and time-to-first-value benchmarks by industry vertical, including automation tool comparisons for post-sale journey orchestration",
  reason="Calibrate touchpoint timing recommendations to industry-specific norms and identify best-in-class tooling for implementation"
)
```

## Step 11: Save Session

```
FutureProof:save_session(skill="post-sale-delight-engineer", session={
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