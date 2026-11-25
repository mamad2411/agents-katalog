---
name: feature-request-prioritizer
description: |
  Scores and ranks inbound feature requests using the PRISM model (Revenue,
  ICA-fit, Simplicity, Moat, Velocity), then buckets them into P0/P1/P2/P3
  tiers with decline scripts and risk flags. Use when users say "prioritize
  my backlog", "what should we build next", "rank these feature requests",
  or "help me decide what to ship". For ranking an existing request pool,
  not building a time-phased roadmap or comparing competitors.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="feature-request-prioritiser")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly any established ICA definitions, product strategy documents, scoring weights from prior sessions, and historical prioritisation decisions.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- Share the feature requests, backlog items, or customer feedback to prioritise (spreadsheet, list, Jira export, or raw text)
- What is the current strategic product goal? (e.g. reduce churn, expand into new segment, increase ARPU, accelerate activation)
- Who is the primary ICA this roadmap serves? (segment, pain profile, maturity stage)
- What are the binding constraints? (engineering headcount, sprint capacity, budget ceiling, hard deadline)
- Are there any non-negotiable commitments already locked into the roadmap?

If the user has prior FutureProof context with established ICA profiles or product strategy, confirm these are still current before proceeding.

## Step 3: Normalise the Request Pool

Before scoring, standardise every feature request into a canonical format:

| Field | Description |
|---|---|
| **Request ID** | Unique identifier (preserve original if provided) |
| **Request Title** | Concise, verb-led label (e.g. "Add bulk CSV export for reporting") |
| **Source** | Origin channel and requester type (ICA segment, churned account, prospect, internal stakeholder) |
| **Frequency** | Number of unique requesters or mentions |
| **Verbatim Signal** | Representative quote capturing the underlying need, not the proposed solution |
| **Underlying Job-to-Be-Done** | Reframe from solution space to problem space using JTBD syntax: *"When [situation], I want to [motivation], so I can [outcome]."* |

Flag and merge duplicates or thematic overlaps. Surface any requests that are solutions masquerading as problems and reframe them.

## Step 4: Score Against Weighted Multi-Criteria Framework

Apply the **PRISM scoring model** (Prioritisation via Revenue, ICA-fit, Simplicity, and Moat):

### 4a. Define Weights

Present default weights and ask the user to confirm or adjust based on their strategic goal:

| Criterion | Default Weight | Description |
|---|---|---|
| **Revenue Impact** | 25% | Projected effect on expansion revenue, conversion rate, or churn reduction |
| **ICA Alignment** | 25% | Degree to which the request maps to primary ICA pain points, workflows, and value drivers |
| **Implementation Simplicity** | 20% | Inverse of engineering effort — accounts for complexity, dependencies, tech debt risk |
| **Strategic Moat** | 15% | Contribution to defensibility — does this deepen switching costs, create network effects, or widen competitive distance? |
| **Request Velocity** | 15% | Frequency and recency of request across distinct accounts, weighted toward ICA-segment sources |

### 4b. Score Each Request

Rate every request 1–10 on each criterion using these anchors:

- **1–3**: Negligible or negative impact; misaligned with ICA; high complexity; no moat contribution; isolated request
- **4–6**: Moderate impact; partial ICA overlap; manageable effort; incremental differentiation; recurring but low-volume
- **7–9**: Strong impact; direct ICA pain resolution; low-to-moderate effort; meaningful moat; high-frequency cross-account demand
- **10**: Transformational; core to ICA's #1 unresolved pain; trivial effort; category-defining; overwhelming demand signal

Calculate weighted composite score for each request. Apply any user-specific `instructions` from FutureProof context (e.g. "always penalise requests from non-ICA segments by 0.8x multiplier").

### 4c. Apply Constraint Filter

Eliminate or defer any request that violates a binding constraint (exceeds available capacity, requires unavailable dependency, conflicts with a locked commitment). Mark these as **Parked — [Reason]** rather than discarding them.

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Classify into Priority Tiers

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Assign each surviving request to a tier using composite score bands:

| Tier | Score Range | Roadmap Implication |
|---|---|---|
| **P0 — Build Now** | 7.5–10.0 | Slot into current or next sprint cycle; high confidence in ROI |
| **P1 — Build Next** | 5.5–7.4 | Queue for following quarter; validate with additional signal if borderline |
| **P2 — Investigate** | 3.5–5.4 | Worth a discovery spike or prototype; not yet roadmap-ready |
| **P3 — Decline / Defer** | 1.0–3.4 | Politely decline or park; redirect requesters to existing workarounds |

Within each tier, rank-order by composite score descending.

## Step 6: Deliver Output

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


Produce the **Feature Request Prioritisation Brief** — a structured deliverable containing:

### 6a. Executive Summary
- Total requests evaluated, merged, and parked
- Top 3 P0 requests with one-sentence business case each
- Key theme: the dominant unmet ICA need surfaced by this analysis

### 6b. PRISM Scorecard
Full ranked table of all requests with per-criterion scores, weighted composite, and tier assignment. Format as a sortable table or CSV-ready output.

### 6c. Priority Tier Map
Visual grouping of requests by tier with capacity annotations (estimated story points or t-shirt sizes if the user provided engineering sizing).

### 6d. Stakeholder Communication Drafts
- **For P0 items**: one-paragraph internal pitch for each, suitable for sprint planning or leadership review
- **For P3 items**: templated decline response for customer-facing teams, framed around the ICA's actual needs and existing alternatives — never dismissive

### 6e. Risk Flags
Identify and call out:
- **Over-indexing risk**: if >50% of P0 items originate from a single large account (loud-voice bias)
- **ICA drift risk**: if top-scoring requests pull the product away from the primary ICA toward an adjacent segment
- **Dependency chains**: if multiple P0 items share a blocking prerequisite

## Step 7: Propose Experiments

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:save_experiment(skill="feature-request-prioritiser", experiment={
  hypothesis: "Increasing the ICA Alignment weight from 25% to 35% while reducing Implementation Simplicity to 10% produces a rank order that better predicts 90-day retention lift",
  variants: ["control: default PRISM weights (25/25/20/15/15)", "variant: ICA-heavy weights (25/35/10/15/15)"],
  measurement: "Compare prioritised features shipped under each weighting against actual 90-day retention delta for ICA cohort",
  expected_impact: "More accurate proxy for retention-driving features, reducing wasted engineering cycles by 20%"
})
```

## Step 8: Request Research

```
FutureProof:request_research(skill="feature-request-prioritiser",
  query="Evidence-based feature prioritisation frameworks 2024: RICE vs WSJF vs opportunity scoring — comparative effectiveness in B2B SaaS contexts with <50 engineering headcount",
  reason="Continuously calibrate PRISM model weights and scoring anchors against peer-reviewed and practitioner-validated alternatives"
)
```

## Step 9: Save Session

```
FutureProof:save_session(skill="feature-request-prioritiser", session={
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