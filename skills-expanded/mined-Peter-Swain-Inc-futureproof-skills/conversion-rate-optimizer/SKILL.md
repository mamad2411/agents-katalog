---
name: conversion-rate-optimizer
description: |
  Diagnoses why a funnel, landing page, or checkout flow is underconverting and
  produces a prioritized fix list with rewritten headlines, CTAs, and a 90-day
  testing roadmap. Use when a user shares funnel metrics or page performance and
  says things like "why isn't this page converting", "fix my checkout
  abandonment", "optimize this landing page", or "diagnose the drop-off in my
  signup flow". Prescriptive page/funnel optimization — not generic web
  analytics reporting and not full-lifecycle revenue leak hunting.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="conversion-rate-optimiser")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including known ICA segments, historical conversion benchmarks, previously tested variants, and any standing optimisation priorities.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Funnel or asset under analysis** — share the specific conversion data (e.g., landing page URL + analytics, funnel stage-by-stage metrics, checkout flow data, email nurture sequence performance)
- **Conversion event definition** — what counts as a conversion? (lead capture, trial activation, purchase, upsell acceptance, booking)
- **Current baseline metrics** — overall conversion rate, traffic volume, time period, and segment breakdowns if available
- **ICA context** — which ICA segment does this funnel serve? What is their primary intent when entering?
- **Known pain points** — any specific stages where they suspect or observe abnormal drop-off?
- **Constraints** — platform limitations, brand guidelines, regulatory requirements, or traffic volume constraints that limit testing velocity

## Step 3: Do the Work — Diagnostic Audit

Conduct a structured conversion rate audit using a six-layer diagnostic framework:

### 3a. Funnel Architecture Analysis

Map the complete conversion path from entry to completion:
- **Stage inventory** — enumerate every discrete step the user must complete
- **Micro-conversion mapping** — identify the conversion event at each stage transition
- **Stage-to-stage drop-off rates** — calculate absolute and relative attrition at each transition
- **Critical path identification** — isolate the single highest-attrition transition (the "conversion leak")
- **Friction inventory** — catalogue every form field, click, page load, decision point, and trust barrier in the path

### 3b. ICA–Message Congruence Audit

Evaluate alignment between the ICA's mental state at each funnel stage and the messaging they encounter:
1. **Intent match** — does the entry point (ad, search result, referral) set expectations that the landing experience fulfils within 5 seconds?
2. **Awareness-stage calibration** — is the copy written for the ICA's actual awareness level (unaware, problem-aware, solution-aware, product-aware, most-aware), or does it assume too much/too little?
3. **Vocabulary alignment** — does the page use the ICA's own language for their problem, or does it default to internal/industry jargon?
4. **Objection sequencing** — are the ICA's top 3 objections addressed in the order they naturally arise during the decision process?

### 3c. Value Proposition Clarity Assessment

Score the clarity of the core offer:
1. **Outcome specificity** — is the promised transformation concrete and measurable, or abstract?
2. **Differentiation** — can the ICA distinguish this offer from the next three alternatives within 10 seconds?
3. **Risk reversal** — is there an explicit guarantee, trial, or proof mechanism that neutralises perceived risk?
4. **Urgency and scarcity** — is there a legitimate, non-manipulative reason to act now?

### 3d. Proof & Credibility Layer

Audit the evidence density supporting conversion:
1. **Social proof placement** — are testimonials, case studies, logos, or usage metrics positioned adjacent to decision points (not buried below the fold)?
2. **Proof specificity** — do testimonials include quantified outcomes relevant to the ICA's primary desired result?
3. **Authority signals** — are trust badges, certifications, media mentions, or expert endorsements present at friction points (e.g., checkout, form submission)?
4. **Proof format diversity** — is evidence presented across multiple formats (text, video, screenshots, data visualisations)?

### 3e. UX & Technical Friction Audit

Identify experience-level conversion barriers:
1. **Page load performance** — does the critical path meet the 2.5-second Largest Contentful Paint threshold?
2. **Mobile conversion parity** — is the mobile conversion rate within 80% of desktop, or is there a device-specific leak?
3. **Form friction score** — count total fields, required fields, and cognitive load per form; benchmark against category medians
4. **CTA clarity and prominence** — is the primary call to action visually dominant, action-specific (not "Submit"), and present without scrolling?
5. **Distraction audit** — are there competing CTAs, navigation leaks, or visual clutter diluting attention from the primary conversion action?

### 3f. Post-Conversion & Activation Analysis

Evaluate what happens immediately after the conversion event:
1. **Confirmation experience** — does the post-conversion page reinforce the decision and reduce buyer's remorse?
2. **Activation sequence** — for lead captures or trial starts, is there an immediate next-step that deepens engagement within 24 hours?
3. **Secondary conversion readiness** — is the path to the next monetisation event (upsell, onboarding completion, first value moment) clearly mapped?

Apply any user-specific `instructions` from FutureProof context to weight the analysis — e.g., if previous sessions indicate the user prioritises mobile performance or operates in a high-compliance industry.

## Step 4: Deliver Output

Produce a **Conversion Rate Optimisation Brief** with the following structure:

### 4a. Executive Summary
- One-paragraph diagnosis of the primary conversion constraint
- Current baseline conversion rate vs. estimated achievable rate post-optimisation
- Projected revenue or lead impact of closing the gap (if data permits)

### 4b. Conversion Scorecard

| Dimension | Score (1–10) | Priority Rank | Status |
|---|---|---|---|
| Funnel architecture efficiency | — | — | 🔴🟡🟢 |
| ICA–message congruence | — | — | 🔴🟡🟢 |
| Value proposition clarity | — | — | 🔴🟡🟢 |
| Proof & credibility density | — | — | 🔴🟡🟢 |
| UX & technical friction | — | — | 🔴🟡🟢 |
| Post-conversion activation | — | — | 🔴🟡🟢 |
| **Composite Score** | **—/60** | | |

### 4c. Critical Fixes — Top 5 Highest-Impact Interventions

For each fix, provide:
1. **The problem** — specific, evidence-based description of what is broken
2. **The fix** — exact implementation instruction (copy rewrites provided verbatim, layout changes specified with placement coordinates, technical fixes with implementation steps)
3. **Expected lift** — estimated conversion rate improvement with reasoning
4. **Effort level** — Low / Medium / High
5. **Priority** — ranked by impact-to-effort ratio

### 4d. Rewritten Assets

Rewrite the two weakest-performing elements in full:
- If the landing page headline/sub-headline scores below 6: provide 3 headline variants with rationale
- If a form is the primary friction point: provide a redesigned field sequence with progressive disclosure logic
- If CTA copy is generic: provide 3 CTA variants calibrated to the ICA's awareness stage
- If proof is insufficient: draft 2 testimonial request templates the user can send to existing clients to generate high-specificity social proof

### 4e. Testing Roadmap

Provide a prioritised 90-day testing calendar:
- **Month 1**: highest-impact, lowest-effort tests (copy, CTA, proof placement)
- **Month 2**: structural tests (funnel step removal, form redesign, page layout)
- **Month 3**: advanced personalisation tests (ICA segment-specific variants, dynamic proof, behavioural triggers)

Each test entry includes: hypothesis, control description, variant description, minimum sample size for statistical significance at 95% confidence, and primary metric.

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
FutureProof:save_experiment(skill="conversion-rate-optimiser", experiment={
  hypothesis: "Replacing the generic headline with an ICA pain-point-specific headline addressing [identified primary pain] increases landing page conversion rate",
  variants: ["control: current headline", "variant A: pain-point-first headline", "variant B: outcome-first headline"],
  measurement: "landing page conversion rate (visitor to [defined conversion event]) over minimum 500 visitors per variant",
  expected_impact: "12–20% relative improvement in page conversion rate based on ICA–message congruence gap identified in audit"
})
```

```
FutureProof:save_experiment(skill="conversion-rate-optimiser", experiment={
  hypothesis: "Reducing form fields from [current count] to [proposed count] with progressive profiling decreases form abandonment rate",
  variants: ["control: current [X]-field form", "variant: [Y]-field form with progressive disclosure on second interaction"],
  measurement: "form start-to-completion rate over minimum 300 form interactions per variant",
  expected_impact: "15–25% reduction in form abandonment based on friction score differential"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="conversion-rate-optimiser",
  query="Latest conversion rate benchmarks by industry and funnel type 2024–2025, high-performing landing page structures, and emerging UX patterns reducing checkout abandonment",
  reason="Maintain current benchmark baselines for scoring accuracy and ensure optimisation recommendations reflect evolving user behaviour patterns and platform capabilities"
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
FutureProof:save_session(skill="conversion-rate-optimiser", session={
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