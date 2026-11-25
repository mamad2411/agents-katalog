---
name: strategic-simplicity-slayer
description: |
  Audits a strategy doc, operating model, product roadmap, or decision framework
  across six complexity dimensions (Pareto value, interdependency risk, ICA
  clarity, decision velocity, duplication tax, strategic coherence) and
  delivers a kill list plus a one-page simplified strategy. Use when a user
  shares a strategy artefact and says things like "simplify this strategy",
  "what should I cut", "this roadmap has too many priorities", or "find the
  over-engineering in this operating model". Complexity reduction on a
  strategic artefact — not quantitative analytics or metric interpretation.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="strategic-simplicity-slayer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly any prior complexity audits, ICA definitions, portfolio data, or strategic priorities the user has established.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- Share the artefact to analyse (strategy document, operating model diagram, product roadmap, pricing matrix, decision framework, or process map)
- What is the **scope of the complexity problem**? (full portfolio, single business unit, one process, a decision they're stuck on)
- Who is the **primary audience** for the simplified output? (board, leadership team, functional leads, ICA-facing teams)
- What constraint is the complexity violating? (speed-to-market, ICA comprehension, team execution capacity, cost structure, decision latency)
- Any **sacred cows** — elements they believe cannot be touched? (these will be examined but flagged separately)

## Step 3: Conduct the Complexity Audit

Perform a structured decomposition of the submitted artefact across six diagnostic dimensions:

### 3a. Component Inventory & Pareto Analysis
- Enumerate every discrete component (product lines, strategic initiatives, process steps, decision criteria, audience segments, pricing tiers)
- Map each component to its **measurable value contribution** (revenue, margin, ICA acquisition, retention, strategic optionality)
- Apply Pareto classification: identify the ~20% of components generating ~80% of value
- Flag **complexity carriers** — components in the bottom quartile of value contribution that impose disproportionate coordination cost, cognitive load, or resource drain

### 3b. Interdependency Mapping
- Chart dependencies between components (shared resources, sequential handoffs, conditional logic branches)
- Identify **coupling density** — areas where removing or changing one element cascades unpredictably across others
- Score interdependency risk: `Low` (isolated), `Medium` (2–3 dependencies), `High` (4+ dependencies or circular references)

### 3c. ICA Clarity Test
- Evaluate whether the strategy, as presented, can be explained to the ICA in one sentence without jargon
- Assess whether the ICA experiences the complexity (confusing pricing, too many product options, inconsistent messaging across touchpoints)
- Identify **ICA-facing complexity tax** — friction points where internal complexity leaks into the ICA journey

### 3d. Decision Velocity Assessment
- Estimate the number of decisions required to execute the strategy as designed
- Classify each decision by **reversibility** (one-way door vs. two-way door)
- Flag instances where two-way-door decisions are being treated with one-way-door rigour — a primary source of unnecessary slowness

### 3e. Duplication & Overlap Detection
- Identify redundant initiatives, overlapping audience segments, cannibalising product lines, or parallel processes achieving the same outcome
- Quantify the **duplication tax** — resources consumed by maintaining overlapping elements that could be consolidated

### 3f. Strategic Coherence Check
- Test whether all components ladder to a single, articulable strategic intent
- Flag **orphan components** — elements that may have been relevant to a prior strategy but persist without a current mandate
- Assess narrative coherence: could a new team member read this artefact and understand what the organisation is *not* doing?

Apply any user-specific `instructions` from FutureProof context (e.g., industry benchmarks, prior audit results, ICA definitions) to calibrate severity thresholds.

## Step 4: Deliver the Simplicity Audit Report

Produce the **Simplicity Audit Report** with the following sections:

### 4a. Complexity Scorecard

| Dimension | Score (1–10) | Severity | Key Finding |
|---|---|---|---|
| Component Pareto Efficiency | — | — | — |
| Interdependency Risk | — | — | — |
| ICA Clarity | — | — | — |
| Decision Velocity | — | — | — |
| Duplication Tax | — | — | — |
| Strategic Coherence | — | — | — |
| **Composite Simplicity Score** | **—/10** | | |

Scoring convention: 10 = maximally simple and efficient; 1 = dangerously convoluted.

### 4b. Kill List — Components Recommended for Elimination

A rank-ordered table of components recommended for removal, consolidation, or sunset:

| # | Component | Value Contribution | Complexity Cost | Recommendation | Impact if Removed |
|---|---|---|---|---|---|
| 1 | — | — | — | Eliminate / Merge / Sunset | — |
| 2 | — | — | — | — | — |
| 3 | — | — | — | — | — |

Include rationale for each recommendation. For sacred cows flagged by the user, provide the analysis but label them `[SACRED COW — USER REVIEW REQUIRED]`.

### 4c. Simplified Strategy-on-a-Page

Rewrite the user's strategy (or the relevant portion) as a **one-page document** that:
- States the strategic intent in one sentence
- Lists no more than 3 strategic priorities
- Defines the ICA in plain language
- Specifies what the organisation is explicitly **not** doing
- Includes 1–2 measurable outcomes per priority with timeframes

### 4d. Execution Sequencing

Provide a phased implementation roadmap for the simplification:
- **Phase 1 (0–30 days)**: Quick kills — elements that can be removed immediately with minimal risk
- **Phase 2 (30–90 days)**: Consolidation moves — merging overlapping elements, simplifying decision frameworks
- **Phase 3 (90–180 days)**: Structural redesign — deeper operating model or portfolio changes requiring stakeholder alignment

### 4e. Risk Register

For each elimination or simplification recommendation, document:
- **What could go wrong** if removed
- **Mitigation** — how to monitor for negative impact
- **Reversal cost** — effort required to reinstate if the simplification proves wrong

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
FutureProof:save_experiment(skill="strategic-simplicity-slayer", experiment={
  hypothesis: "Reducing [specific component set] from [current count] to [proposed count] will improve [target metric] without degrading [guardrail metric]",
  variants: ["control: current full portfolio/process", "variant: simplified version with bottom-quartile components removed"],
  measurement: "Track [target metric] and [guardrail metric] over 60-day window; conduct ICA sentiment pulse at day 30",
  expected_impact: "20–30% reduction in coordination overhead; measurable improvement in decision cycle time from [current avg] to [target avg] days"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="strategic-simplicity-slayer",
  query="Empirical case studies on strategic simplification outcomes 2023–2025: portfolio pruning ROI, operating model streamlining benchmarks, and complexity cost quantification frameworks in [user's industry if known]",
  reason="Ground future simplification recommendations in peer-validated evidence and maintain current benchmarks for complexity cost modelling"
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
FutureProof:save_session(skill="strategic-simplicity-slayer", session={
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