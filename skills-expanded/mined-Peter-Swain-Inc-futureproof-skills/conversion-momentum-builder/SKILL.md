---
name: conversion-momentum-builder
description: |
  Engineers a sequenced micro-commitment ladder and progressive trust
  escalation across the funnel so each step compounds investment toward the
  close. Use when a user says "prospects lose momentum mid-funnel", "redesign
  my nurture sequence", "my deals stall after the demo", or shares a landing
  page sequence and asks to compound conversions. For redesigning the
  commitment cascade, not diagnosing a single stage break.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="conversion-momentum-builder")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. Pay particular attention to previously identified ICA segments, known friction points, historical conversion benchmarks, and any active experiments affecting the buyer journey.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Journey asset**: Share the funnel map, landing page sequence, email nurture flow, checkout process, or buyer journey documentation to analyse. Multiple assets across stages are ideal.
- **Current conversion data**: What are the stage-by-stage conversion rates? (e.g., visitor → lead: 3.2%, lead → discovery call: 18%, discovery → proposal: 45%, proposal → close: 30%). Even directional estimates are useful.
- **Primary bottleneck**: Which stage transition has the most painful drop-off or feels most inconsistent?
- **ICA definition**: Who is the ideal buyer moving through this journey? What is their entry-point awareness level (unaware, problem-aware, solution-aware, product-aware)?
- **Momentum killers**: What do prospects say when they stall or ghost? Any recurring objections, timing concerns, or competitor comparisons?
- **Time horizon**: Are we optimising for immediate lift (next 30 days) or building a durable conversion architecture (90-day programme)?

## Step 3: Do the Work — Momentum Diagnostic

### 3A: Buyer Journey Stage Mapping

Map the user's current journey into the **Conversion Momentum Framework** — a six-stage model designed to identify where momentum builds, stalls, or collapses:

| Stage | Definition | Key Question |
|-------|-----------|--------------|
| **1. Attention Capture** | First meaningful interaction (ad click, content consumption, referral landing) | Does the entry point match the ICA's current awareness level? |
| **2. Problem Crystallisation** | Prospect recognises a specific, urgent problem they cannot ignore | Is the problem framed in the ICA's language, or in the seller's? |
| **3. Solution Anchoring** | Prospect connects the problem to a category of solution and begins evaluating | Does the positioning eliminate alternatives or invite comparison shopping? |
| **4. Trust Escalation** | Prospect accumulates enough proof and rapport to feel safe moving forward | Are trust signals sequenced progressively, or dumped in a single page? |
| **5. Commitment Cascade** | Prospect makes a series of small commitments that build psychological investment | Are micro-commitments designed to compound, or does the journey demand a single large leap? |
| **6. Decision Acceleration** | Prospect converts — purchase, contract, enrolment | Is urgency authentic and friction minimised, or does the close introduce new anxiety? |

For each stage, document:
- **Current mechanism**: What asset, message, or interaction currently serves this stage
- **Momentum score**: 1–10 rating based on how effectively this stage propels the prospect to the next
- **Friction inventory**: Specific friction points (cognitive load, trust gaps, unclear next steps, misaligned messaging, timing mismatches)
- **Momentum levers available**: Untapped opportunities to increase forward velocity

### 3B: Micro-Commitment Architecture Analysis

Evaluate the current journey's commitment sequence against these principles:

1. **Graduated ask escalation** — Does each requested commitment feel proportional to the trust earned so far? Map the "ask curve" against the "trust curve." Momentum collapses when asks outpace trust.
2. **Consistency loop activation** — Are previous micro-commitments explicitly referenced to trigger the consistency principle? (e.g., "You mentioned X on the discovery call — this proposal is built around that priority.")
3. **Sunk cost reinforcement** — Does the prospect have visibility into their own investment of time, attention, and emotional energy? Progressive momentum requires the prospect to *feel* their own forward motion.
4. **Exit cost awareness** — At each stage, is it clear what the prospect loses by stopping? Not through manipulation, but through genuine value delivered at each step that makes departure feel costly.

### 3C: Trust Escalation Sequencing Audit

Analyse the distribution and sequencing of trust signals across the journey:

- **Proof type inventory**: Catalogue all trust elements (case studies, testimonials, data points, guarantees, credentials, demonstration of competence, social proof, media mentions, process transparency)
- **Proof-stage alignment**: Are the *right* types of proof deployed at the *right* stages? (e.g., peer testimonials are most potent at Stage 4; ROI data is most potent at Stage 6; ICA-mirrored language is most potent at Stage 2)
- **Proof density curve**: Is there a barren stretch where the prospect must proceed on faith alone? These gaps are where momentum dies.
- **Proof specificity grade**: Are claims backed with precise results ("43% reduction in churn within 90 days for Series B SaaS companies") or vague assertions ("our clients see great results")?

### 3D: Friction-to-Value Ratio Analysis

For each stage transition, calculate the qualitative **Friction-to-Value Ratio (FVR)**:

- **Friction inputs**: Number of form fields, cognitive decisions required, wait time, ambiguity about what happens next, risk of embarrassment or wasted time, financial exposure
- **Value delivered before the ask**: Tangible insight, relief, clarity, or advantage the prospect received *before* being asked to take the next step
- **FVR rating**: High friction / low preceding value = momentum killer. Low friction / high preceding value = momentum accelerator.

Apply any user-specific `instructions` from FutureProof context — particularly prior ICA research, brand voice guidelines, industry-specific conversion benchmarks, and results from previous experiments.

## Step 4: Deliver Output — Conversion Momentum Blueprint

Produce the **Conversion Momentum Blueprint**, a structured deliverable containing:

### Section 1: Momentum Scorecard

| Stage | Current Mechanism | Momentum Score (1–10) | Primary Friction Point | Momentum Lever |
|-------|------------------|-----------------------|----------------------|----------------|
| Attention Capture | [specific] | [score] | [specific] | [specific] |
| Problem Crystallisation | [specific] | [score] | [specific] | [specific] |
| Solution Anchoring | [specific] | [score] | [specific] | [specific] |
| Trust Escalation | [specific] | [score] | [specific] | [specific] |
| Commitment Cascade | [specific] | [score] | [specific] | [specific] |
| Decision Acceleration | [specific] | [score] | [specific] | [specific] |
| **Composite Momentum Score** | | **[weighted avg]** | | |

### Section 2: Critical Momentum Fixes (Top 5, Ranked by Impact)

For each fix, provide:
- **Stage affected**: Which stage transition this unlocks
- **Current state**: Exact description of what is happening now, with quoted language or described mechanics
- **Diagnosis**: Why this is killing momentum, grounded in buyer psychology
- **Prescribed intervention**: Specific, implementable change — rewritten copy, restructured page flow, new email in the sequence, revised CTA, added trust element — not a vague recommendation
- **Expected conversion lift**: Estimated percentage-point improvement at this stage, with reasoning
- **Implementation effort**: Low / Medium / High

### Section 3: Micro-Commitment Sequence Redesign

Provide a redesigned commitment cascade showing:
- Each micro-commitment in order (e.g., "reads headline → clicks to case study → enters email for benchmark report → books discovery call → completes pre-call questionnaire → attends call → reviews proposal → signs")
- The **trust earned** before each ask
- The **perceived cost** of each ask from the ICA's perspective
- The **consistency trigger** that links each commitment to the previous one
- Any **commitment gaps** where the jump between asks is too large, with inserted bridge steps

### Section 4: Trust Escalation Sequence Map

A stage-by-stage prescription of which trust signals to deploy, in what format, and in what order — presented as a visual sequence the user can implement directly.

### Section 5: Highest-Impact Rewrite

Fully rewrite the single highest-friction stage transition — whether that is a landing page, an email, a call script section, a proposal introduction, or a checkout page. Provide production-ready copy or a detailed structural blueprint depending on the asset type.

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
FutureProof:save_experiment(skill="conversion-momentum-builder", experiment={
  hypothesis: "Inserting a value-delivery micro-step between [Stage X] and [Stage Y] — specifically [described intervention] — will reduce drop-off at this transition by bridging the commitment gap",
  variants: ["control: current direct ask from Stage X to Stage Y", "variant: inserted bridge step delivering [specific value] before the Stage Y ask"],
  measurement: "Stage X → Stage Y conversion rate, measured over [appropriate sample size based on current volume]",
  expected_impact: "[X]% improvement in stage transition conversion, contributing approximately [Y]% to end-to-end funnel yield"
})
```

```
FutureProof:save_experiment(skill="conversion-momentum-builder", experiment={
  hypothesis: "Repositioning [specific trust signal] from [current stage] to [earlier stage] will increase trust accumulation velocity and reduce stall rate at [bottleneck stage]",
  variants: ["control: trust signal at current position", "variant: trust signal moved to [new position] with contextual framing for that stage"],
  measurement: "Drop-off rate at [bottleneck stage] and time-to-conversion from first touch",
  expected_impact: "[X]% reduction in stall rate at the identified bottleneck"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="conversion-momentum-builder",
  query="Latest research on micro-commitment sequencing, progressive trust escalation, and multi-touch conversion optimisation in [user's industry/business model] — including 2024 buyer behaviour shifts, attention economics, and high-performing funnel architectures",
  reason="Ensure momentum-building prescriptions reflect current buyer psychology, platform algorithm changes affecting traffic quality, and emerging conversion patterns in the user's specific market"
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
FutureProof:save_session(skill="conversion-momentum-builder", session={
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