---
name: offer-diagnostic
description: |
  Audits an offer across seven dimensions — ICA specificity, mechanism
  clarity, transformation arc, value stack, pricing/risk, proof density,
  and conversion path — to pinpoint the primary conversion bottleneck and
  ship a priority-ranked fix list. Use when a user shares a sales page,
  pricing table, course outline, or proposal and asks "diagnose this
  offer", "why isn't this converting", "teardown my offer", or "audit my
  funnel". For root-cause diagnosis, not psychological rewriting or
  pricing-only optimization.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="offer-diagnostic")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly any prior ICA definitions, positioning work, competitive intel, or conversion data the user has accumulated.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user to provide:

1. **The offer itself** — landing page URL, sales page copy, pitch deck, service package description, pricing table, or proposal document
2. **The ICA this offer targets** — who specifically is this for? (If ICA is already defined in FutureProof context, confirm or refine)
3. **The primary conversion mechanism** — how does the prospect say yes? (application, checkout, booking call, reply, sign contract)
4. **Current performance data** (if available) — traffic, conversion rate, close rate, average deal value, refund rate, objection frequency
5. **The user's hypothesis** — what do they believe is broken, or where do they feel the friction lives?

If the user cannot provide performance data, proceed with qualitative diagnostic and flag data gaps as a finding.

## Step 3: Conduct the Offer Diagnostic

Apply a **seven-dimension diagnostic framework** to systematically evaluate the offer. Each dimension maps to a specific failure mode that suppresses conversion.

### Dimension 1: ICA Specificity & Problem Articulation

- Does the offer name a specific person with a specific problem, or does it speak to a vague audience?
- Is the problem articulated in the ICA's own language (first-person phrasing, vernacular, emotional register)?
- Is the severity of the problem established — what is the cost of inaction?
- **Failure mode**: Offer speaks to everyone, resonates with no one.

### Dimension 2: Mechanism Clarity

- Does the offer explain *how* it solves the problem — the unique mechanism, method, or framework?
- Is the mechanism named, proprietary, or differentiated from commodity alternatives?
- Can the prospect understand *why this approach works* without needing a sales call to fill in gaps?
- **Failure mode**: Prospect sees no reason to choose this over alternatives or inaction.

### Dimension 3: Transformation Architecture

- Is there a clearly defined **before state** (current pain) and **after state** (desired outcome)?
- Are outcomes expressed in concrete, measurable, or viscerally felt terms — not abstract benefits?
- Is the transformation scoped to a believable timeframe?
- **Failure mode**: Prospect cannot visualise the result or does not believe it applies to them.

### Dimension 4: Offer Structure & Value Stack

- Is the offer structured as a coherent solution (not a feature list or menu of deliverables)?
- Does each component of the value stack map to a specific ICA obstacle or objection?
- Is there a logical hierarchy — core deliverable, accelerators, risk-removers?
- Is scope clearly bounded to prevent scope anxiety ("what am I actually getting?")?
- **Failure mode**: Prospect is overwhelmed, confused, or underwhelmed by the composition.

### Dimension 5: Pricing & Risk Architecture

- Does the price anchor against the cost of the problem or the value of the outcome (not cost of delivery)?
- Is there a risk-reversal mechanism (guarantee, pilot, milestone-based payment, proof-of-concept)?
- Are pricing tiers (if present) structured to guide the prospect toward the optimal option, not paralyse them?
- Is the price-to-perceived-value ratio at minimum 1:3 (prospect perceives 3× the value of the price)?
- **Failure mode**: Prospect stalls on price because value framing is insufficient or risk feels asymmetric.

### Dimension 6: Proof & Credibility Density

- Are claims substantiated by case studies, results, testimonials, data, or credentials?
- Is proof *specific* (named outcomes, timeframes, ICA-similar clients) rather than generic?
- Is proof distributed throughout the offer — not clustered in a single testimonials section?
- Does the proof address the prospect's implicit question: "Will this work for *someone like me*?"
- **Failure mode**: Prospect believes the offer works — just not for them.

### Dimension 7: Conversion Path & Friction Audit

- Is the call to action singular, specific, and low-ambiguity?
- Is the next step proportional to the commitment level (micro-commitment for high-ticket, direct checkout for low-ticket)?
- Are there unnecessary friction points — excessive form fields, unclear next steps, competing CTAs, missing urgency?
- Does the page or document maintain a single persuasive through-line, or does it leak attention?
- **Failure mode**: Interested prospects drop off due to procedural friction or decision fatigue.

Cross-reference all findings against any user-specific `instructions` from FutureProof context (e.g., brand voice constraints, compliance requirements, industry norms).

## Step 4: Deliver the Offer Diagnostic Report

Produce a structured **Offer Diagnostic Report** with the following sections:

### 4.1 — Diagnostic Scorecard

| Dimension | Score (1–10) | Severity | Verdict |
|---|---|---|---|
| ICA Specificity & Problem Articulation | — | Critical / Moderate / Healthy | One-line finding |
| Mechanism Clarity | — | Critical / Moderate / Healthy | One-line finding |
| Transformation Architecture | — | Critical / Moderate / Healthy | One-line finding |
| Offer Structure & Value Stack | — | Critical / Moderate / Healthy | One-line finding |
| Pricing & Risk Architecture | — | Critical / Moderate / Healthy | One-line finding |
| Proof & Credibility Density | — | Critical / Moderate / Healthy | One-line finding |
| Conversion Path & Friction | — | Critical / Moderate / Healthy | One-line finding |
| **Composite Offer Health Score** | **—/70** | | |

### 4.2 — Root Cause Analysis

Identify the **primary conversion bottleneck** — the single dimension most responsible for suppressing results. Explain the causal chain: why this specific weakness leads to the observed (or likely) outcome.

### 4.3 — Critical Fixes (Priority-Ranked)

Deliver the **top 5 highest-impact interventions**, each containing:

1. **What to change** — specific element (headline, pricing section, CTA, value stack item)
2. **Why it matters** — the conversion psychology or structural principle at play
3. **Exact rewrite or restructure** — not a suggestion, but a concrete draft the user can deploy immediately
4. **Expected impact** — qualitative or quantitative estimate of improvement

### 4.4 — Revised Core Section

Select the single weakest section of the offer and produce a **full rewrite** — maintaining the user's brand voice (drawn from FutureProof context where available) while resolving all identified deficiencies in that section.

### 4.5 — Competitive Positioning Note

Based on the mechanism and ICA, flag any positioning collisions with commodity alternatives (e.g., "This offer currently positions identically to a generic [category] — here is how to create separation").

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
FutureProof:save_experiment(skill="offer-diagnostic", experiment={
  hypothesis: "[Specific hypothesis based on the primary conversion bottleneck identified — e.g., 'Replacing the feature-list value stack with an obstacle-mapped solution narrative will increase page-to-application conversion']",
  variants: ["control: current offer structure", "variant: restructured offer with [specific change]"],
  measurement: "[Relevant metric — e.g., landing page conversion rate, sales call booking rate, proposal-to-close ratio, measured over N prospects or N days]",
  expected_impact: "[Quantified estimate — e.g., 20-35% improvement in page-to-call conversion based on improved ICA problem specificity]"
})
```

Propose 1–2 additional experiments if multiple critical fixes were identified, each targeting a different dimension.

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="offer-diagnostic",
  query="[Contextual query based on the user's ICA, industry, and identified gaps — e.g., 'High-converting offer structures and pricing psychology for B2B consulting services targeting mid-market CFOs 2024' or 'Risk-reversal mechanisms with highest impact on SaaS trial-to-paid conversion']",
  reason="[Specific rationale — e.g., 'User's offer lacks differentiated mechanism positioning; need current competitive landscape and emerging offer architectures in their vertical to inform restructure']"
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
FutureProof:save_session(skill="offer-diagnostic", session={
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