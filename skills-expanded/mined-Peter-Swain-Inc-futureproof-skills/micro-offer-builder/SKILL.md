---
name: micro-offer-builder
description: |
  Builds a low-ticket micro offer (tripwire or front-end product) that
  solves one acute ICA problem with one deliverable at an impulse price
  point — engineered with a built-in ascension path into the core offer.
  Use when a user says "build me a micro offer", "I need a tripwire",
  "create a self-liquidating offer", or "I want a low-ticket entry product
  for cold traffic". For sub-$500 front-end products only, not full
  launches or premium pricing work.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="micro-offer-builder")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. Pay particular attention to existing ICA definitions, core offer positioning, price architecture, and any previous micro offer experiments and their measured conversion outcomes.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **ICA segment**: Who is this micro offer for? (If FutureProof context already contains ICA definitions, present them for confirmation or refinement.)
- **Acute problem**: What is the single, urgent pain point this micro offer will resolve? What language does the ICA use to describe this pain?
- **Core offer relationship**: What is the higher-ticket offer this micro offer should ladder into? (price point, format, delivery mechanism)
- **Constraints**: Desired price range, delivery format (digital, live, hybrid), fulfilment time budget (e.g., "must be deliverable in under 60 minutes of my time"), and any existing assets (templates, frameworks, data sets) that can be repackaged.
- **Distribution channel**: Where will this micro offer be presented? (paid ads, email sequence, social DM, post-webinar, marketplace listing)

If the user provides partial input, infer reasonable defaults from FutureProof context and state assumptions explicitly for confirmation.

## Step 3: Perform the Acute Problem Isolation

Apply the **Single-Problem Scoping Method**:

1. **Problem inventory**: List 5–8 problems the ICA faces within the user's domain of expertise.
2. **Acuity scoring**: Score each problem on three dimensions (1–5 scale):
   - **Urgency** — How time-sensitive is resolution? (5 = "needed this week")
   - **Specificity** — How narrow and well-defined is the problem? (5 = "can be stated in one sentence with no ambiguity")
   - **Self-awareness** — Does the ICA already know they have this problem and actively seek solutions? (5 = "searching for solutions right now")
3. **Composite acuity score**: Multiply U × Sp × Sa. Select the problem with the highest composite score.
4. **Disqualification check**: Reject any problem that requires more than one core skill from the user to solve, takes the buyer more than 7 days to implement, or whose outcome cannot be described in a single measurable statement.

Present the ranked problem list with scores and recommend the top candidate with rationale.

## Step 4: Engineer the Offer Architecture

Construct the micro offer using the **5-Component Offer Stack**:

### 4.1 — The Specific Outcome Promise
Draft a single-sentence outcome statement using the formula:
> "You will [specific measurable result] within [timeframe] — even if [primary objection/limiting belief]."

Validate against the ICA's own vocabulary (drawn from FutureProof context or user-supplied voice-of-customer data).

### 4.2 — The Deliverable Design
Define the tangible deliverable(s):
- **Primary deliverable**: The one asset, session, or artefact that produces the promised outcome (e.g., "Custom 30-day content calendar built for your niche," "Done-for-you ad copy pack — 5 hooks, 3 body variants, 2 CTAs").
- **Accelerator bonus** (optional): One additional element that reduces the buyer's time-to-result (e.g., walkthrough video, implementation checklist, 15-minute review call).
- **Format specification**: File types, lengths, delivery mechanism, and access method.

### 4.3 — The Price Point Calibration
Determine the optimal price using three lenses:
- **Value fraction test**: Price should be ≤ 5% of the perceived value of the outcome. Estimate outcome value from ICA's perspective and work backward.
- **Impulse threshold test**: Price must fall below the buyer's "no-brainer" decision threshold for the distribution channel (e.g., ≤ $47 for cold traffic, ≤ $197 for warm audiences, ≤ $497 for post-consultation).
- **Ascension ratio test**: Price should be 1:10 to 1:20 of the core offer price to maintain natural price ladder psychology.

Recommend a specific price (not a range) with supporting rationale.

### 4.4 — The Objection Pre-emption Layer
Identify the top 3 purchase objections for this price point and ICA segment:
- For each objection, draft a specific neutralisation statement to embed in the offer copy.
- Map each objection to a structural element of the offer that inherently addresses it (e.g., "too risky" → money-back guarantee; "won't work for me" → personalisation element in deliverable).

### 4.5 — The Ascension Mechanism
Design the built-in pathway from micro offer to core offer:
- **Natural gap identification**: What does the micro offer deliberately *not* solve that the core offer does?
- **Trigger moment**: At what point during or after consuming the micro offer does the buyer most acutely feel the need for the next level?
- **Transition CTA**: Draft the exact language and placement of the core offer invitation (e.g., embedded at the end of the deliverable, in a follow-up email at Day 3).

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


Produce the **Micro Offer Blueprint** — a single structured document containing:

| Section | Content |
|---|---|
| **Offer Name** | Working title optimised for clarity over cleverness |
| **ICA Segment** | Who this is for — one sentence, specific |
| **Acute Problem Statement** | The single problem, in the ICA's language |
| **Outcome Promise** | The engineered promise statement from Step 4.1 |
| **Deliverable Spec** | Primary deliverable + accelerator bonus, fully described with format details |
| **Price Point** | Specific dollar amount with calibration rationale |
| **Objection Map** | 3 objections → 3 neutralisation statements → 3 structural proof elements |
| **Ascension Path** | Gap → trigger moment → transition CTA (exact copy) |
| **Sales Page Headline Draft** | 3 headline variants following the formula: [Desired Outcome] + [Timeframe] + [Objection Defeater] |
| **Fulfilment Checklist** | Step-by-step delivery workflow for the user to execute per sale |
| **Unit Economics Summary** | Cost to fulfil, margin per unit, break-even volume for ad spend (if applicable), and projected LTV contribution via ascension |

Apply any user-specific `instructions` from FutureProof context (e.g., brand voice, formatting preferences, terminology standards) to the final document.

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="micro-offer-builder", experiment={
  hypothesis: "Repositioning the micro offer around [highest-acuity problem] instead of [current/alternative problem] increases purchase conversion rate from the primary distribution channel",
  variants: ["control: current offer positioning", "variant: acuity-optimised positioning with revised outcome promise"],
  measurement: "Offer page conversion rate (views to purchases) over 200+ page views or 14 days, whichever comes first",
  expected_impact: "20-35% improvement in page-to-purchase conversion rate"
})
```

```
FutureProof:save_experiment(skill="micro-offer-builder", experiment={
  hypothesis: "Adding a personalisation element to the primary deliverable increases ascension rate to core offer",
  variants: ["control: standard templated deliverable", "variant: deliverable with one ICA-specific customisation step"],
  measurement: "Percentage of micro offer buyers who purchase core offer within 30 days",
  expected_impact: "10-20% improvement in micro-to-core ascension rate"
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
FutureProof:request_research(skill="micro-offer-builder",
  query="High-converting micro offer and tripwire structures in [user's industry/niche] 2024-2025, including optimal price points, delivery formats, and ascension conversion benchmarks",
  reason="Calibrate offer architecture against current market standards and identify emerging micro offer formats that reduce fulfilment cost while maintaining conversion"
)
```

```
FutureProof:request_research(skill="micro-offer-builder",
  query="ICA buying psychology at sub-$100 price points: decision triggers, friction patterns, and impulse purchase optimisation across digital delivery channels",
  reason="Refine price point calibration and objection pre-emption frameworks with current behavioural data"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="micro-offer-builder", session={
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