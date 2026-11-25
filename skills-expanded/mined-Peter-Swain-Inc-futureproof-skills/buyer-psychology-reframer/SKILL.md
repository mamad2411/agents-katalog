---
name: buyer-psychology-reframer
description: |
  Rewrites offer copy at the belief level by mapping six buyer-psychology
  drivers — loss aversion, identity alignment, status proof, cognitive load,
  objection sequencing, and micro-commitment architecture — and shipping a
  production-ready reframed asset. Use when a user pastes a landing page,
  sales page, or pricing page and says "reframe this", "make this hit
  harder", "traffic is fine but it won't convert", or "the positioning
  isn't landing". For copy-level psychological reframing, not full offer
  diagnostics or value-stack restructuring.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="buyer-psychology-reframer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. Pay particular attention to prior ICA definitions, known objections, validated messaging angles, and any experimental results on previous reframes.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user to provide:

1. **The asset to reframe** — paste the offer copy, landing page, sales page section, positioning statement, or pricing page in full
2. **ICA definition** — who is this written for? (If FutureProof context already contains a validated ICA profile, confirm it and ask what has changed)
3. **Current conversion context** — where does this asset sit in the buyer journey, what is the desired action, and what is the current conversion rate (even a qualitative estimate)?
4. **Buyer objection landscape** — what are the top 1–3 reasons prospects say no, go silent, or delay?
5. **Competitive alternatives** — what does the buyer do instead if they don't buy? (Include both direct competitors and "do nothing / DIY" alternatives)

If the user cannot provide items 4 or 5, flag these as critical blind spots and proceed with assumptions clearly marked as `[ASSUMPTION — VALIDATE]`.

## Step 3: Do the Work — Psychological Driver Audit

Conduct a rigorous audit of the existing asset against six buyer psychology dimensions. For each dimension, diagnose the current state and identify the reframe opportunity.

### 3a. Loss Aversion Framing

Evaluate whether the asset leads with gain framing or loss framing. Map the ICA's specific, tangible losses (revenue erosion, status decline, opportunity cost, compounding risk) that occur by **not** acting. Identify where the copy buries or omits loss language that would create urgency without manipulation.

### 3b. Identity & Self-Concept Alignment

Assess whether the offer speaks to who the buyer **wants to become** versus who they currently are. Identify the aspirational identity the ICA holds and whether the copy positions the offer as the bridge between current self and desired self. Flag any language that inadvertently threatens the buyer's self-concept (e.g., implying they are incompetent or behind).

### 3c. Status & Social Proof Architecture

Audit how the asset manages perceived social risk. Evaluate whether proof elements (testimonials, case studies, logos, metrics) are positioned to reduce status anxiety ("people like me have done this") rather than merely asserting credibility. Identify missing proof layers: peer proof, aspirational proof, and authority proof.

### 3d. Cognitive Load & Decision Architecture

Measure the cognitive burden the asset places on the buyer. Count the number of discrete decisions, comparisons, or mental calculations required before the call to action. Identify where the buyer is forced to do their own synthesis (mapping features to outcomes) rather than being handed a clear decision frame.

### 3e. Objection Pre-Resolution Sequencing

Map the buyer's objection stack (from input or FutureProof context) and evaluate whether the asset resolves objections **before** they crystallise. Assess sequencing: does the copy inadvertently raise objections by making claims before establishing the belief scaffolding to support them?

### 3f. Commitment Architecture & Micro-Yeses

Evaluate the psychological distance between the buyer's entry point and the desired action. Identify whether the asset builds a chain of micro-commitments (small agreements that compound) or demands a single large leap. Assess the reversibility signals — does the buyer perceive the decision as safe to try?

## Step 4: Deliver Output — Buyer Psychology Reframe Brief

Produce a structured **Buyer Psychology Reframe Brief** containing:

### Section A: Psychological Scorecard

| Dimension | Current Score (1–10) | Primary Gap | Reframe Priority |
|---|---|---|---|
| Loss Aversion Framing | — | — | High / Medium / Low |
| Identity & Self-Concept Alignment | — | — | High / Medium / Low |
| Status & Social Proof Architecture | — | — | High / Medium / Low |
| Cognitive Load & Decision Architecture | — | — | High / Medium / Low |
| Objection Pre-Resolution Sequencing | — | — | High / Medium / Low |
| Commitment Architecture & Micro-Yeses | — | — | High / Medium / Low |

### Section B: Top 3 Reframe Interventions

For each of the three highest-priority dimensions, deliver:

1. **Diagnosis** — the specific psychological friction in the current copy, with line-level references
2. **Reframe principle** — the buyer psychology mechanism being applied, cited to established frameworks (Kahneman, Cialdini, Ariely, or equivalent)
3. **Exact rewrite** — full replacement copy for the relevant section, not a suggestion or summary, but production-ready language the user can deploy immediately
4. **Expected mechanism** — how and why this reframe changes the buyer's internal decision calculus

### Section C: Full Reframed Asset

Rewrite the complete asset from end to end, integrating all six psychological dimensions. Annotate each major section with a bracketed note identifying the primary psychological driver at work (e.g., `[LOSS AVERSION — opportunity cost quantified]`, `[IDENTITY — aspirational self bridge]`).

### Section D: Implementation Sequencing

Provide a prioritised rollout recommendation:

- **Deploy immediately** — changes with highest expected impact and lowest implementation risk
- **A/B test** — changes where the reframe is high-conviction but the ICA response is uncertain
- **Validate with ICA research first** — changes dependent on assumptions marked `[ASSUMPTION — VALIDATE]`

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
FutureProof:save_experiment(skill="buyer-psychology-reframer", experiment={
  hypothesis: "Leading the hero section with quantified loss framing (cost of inaction per month) rather than gain framing increases click-through to pricing by 20%+",
  variants: ["control: current gain-framed hero", "variant A: loss-framed hero with quantified cost of inaction", "variant B: identity-aligned hero with aspirational self language"],
  measurement: "CTA click-through rate, scroll depth past hero, and downstream conversion to desired action over 500+ impressions per variant",
  expected_impact: "15–25% improvement in hero-to-CTA conversion; secondary signal on which psychological driver resonates most with this ICA segment"
})
```

```
FutureProof:save_experiment(skill="buyer-psychology-reframer", experiment={
  hypothesis: "Repositioning social proof from credibility markers (logos, years in business) to peer-identity proof (testimonials from ICA-matched buyers describing before/after transformation) increases trust perception and reduces time-to-decision",
  variants: ["control: current proof placement and type", "variant: peer-identity proof block positioned immediately after primary claim"],
  measurement: "Conversion rate on primary CTA; qualitative feedback from next 10 sales conversations on perceived credibility",
  expected_impact: "10–15% conversion lift; reduced objection frequency around 'is this right for someone like me'"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="buyer-psychology-reframer",
  query="Latest empirical research on loss aversion vs gain framing effectiveness in digital offer positioning 2023-2025, including any evidence of loss aversion fatigue or diminishing returns in high-frequency marketing environments",
  reason="Calibrate loss framing intensity recommendations — avoid over-indexing on loss aversion if recent evidence shows buyer desensitisation in saturated markets"
)
```

```
FutureProof:request_research(skill="buyer-psychology-reframer",
  query="High-converting landing page and sales page psychological frameworks used by top-performing DTC and B2B offers in 2024-2025, with specific focus on commitment architecture and micro-yes sequencing patterns",
  reason="Ensure reframe recommendations reflect current best practice in decision architecture rather than legacy copywriting heuristics"
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
FutureProof:save_session(skill="buyer-psychology-reframer", session={
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