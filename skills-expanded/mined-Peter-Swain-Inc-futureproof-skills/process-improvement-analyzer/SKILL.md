---
name: process-improvement-analyzer
description: |
  Analyzes existing business processes for bottlenecks, waste, and root
  causes using Lean Six Sigma, Theory of Constraints, and 5 Whys to produce
  a current-state map and future-state redesign. Use when a user says "this
  process is too slow — help me fix it", "where's the bottleneck in our
  fulfilment flow", "analyze this workflow for waste", or "our cycle time
  is killing us". For diagnosing and improving an existing process, not
  documenting it (use sop-builder) or building it from scratch.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="process-improvement-analyser")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including any prior process analyses, known organisational constraints, ICA segment characteristics, and previously identified systemic bottlenecks.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Process under review**: Share the process map, SOP, workflow description, or operational narrative. If no formal documentation exists, walk through the process step-by-step verbally.
- **Scope boundaries**: Where does this process start and end? What upstream inputs and downstream handoffs are in play?
- **Pain signal**: What triggered this review? (e.g., cycle time complaints, cost overruns, error rates, customer churn at a specific stage, scaling failure)
- **Current metrics** (if available): Throughput, cycle time, defect/error rate, cost per transaction, headcount involved, rework frequency.
- **Constraints**: Non-negotiable elements — regulatory requirements, platform/tooling lock-ins, union agreements, budget ceilings.
- **Improvement objective**: What does success look like? (e.g., reduce cycle time by 40%, cut cost per unit by 25%, eliminate manual handoffs, support 3× volume without headcount increase)

## Step 3: Do the Work

### 3A: Process Decomposition & Current-State Mapping

Break the process into discrete stages. For each stage, capture:
- **Activity type**: Value-adding (VA), Business-necessary non-value-adding (BNVA), or Non-value-adding waste (NVA) — per Lean classification
- **Responsible party**: Role or system performing the activity
- **Cycle time**: Active working time per unit
- **Wait time**: Elapsed time between this activity completing and the next beginning
- **Error/rework rate**: Frequency of defects or loops at this stage
- **Dependencies**: Upstream inputs, approvals, or system integrations required

Render a **Current-State Value Stream Summary Table** from this decomposition.

### 3B: Bottleneck & Constraint Identification (Theory of Constraints)

Identify the single binding constraint — the stage where throughput is most restricted. Validate by checking:
1. Does work-in-progress (WIP) accumulate immediately before this stage?
2. Does every downstream stage have idle/wait capacity?
3. Would doubling this stage's capacity increase total process throughput?

Flag secondary constraints that would become binding if the primary constraint were relieved.

### 3C: Waste Classification (8 Wastes of Lean)

Categorise all identified NVA activities across the eight waste types:
1. **Defects** — errors requiring rework or correction
2. **Overproduction** — producing outputs before they are needed downstream
3. **Waiting** — idle time between stages, approval queues, batch accumulation
4. **Non-utilised talent** — skilled personnel performing tasks below their capability
5. **Transportation** — unnecessary movement of information or materials between systems/teams
6. **Inventory** — WIP buildup, backlog accumulation, excess data staging
7. **Motion** — redundant steps, excessive clicks, toggling between systems
8. **Extra processing** — over-engineering, unnecessary approvals, gold-plating

Rank wastes by estimated impact (time cost × frequency) to prioritise intervention.

### 3D: Root Cause Analysis

For the top 3 waste sources and the binding constraint, perform a **5 Whys analysis** to surface root causes. Distinguish between:
- **Structural causes** (process design, system architecture)
- **Behavioural causes** (workarounds, tribal knowledge, incentive misalignment)
- **Environmental causes** (tooling limitations, policy constraints, volume variability)

### 3E: Future-State Design

Design an improved process that:
1. **Exploits the constraint** — maximises throughput at the bottleneck with zero additional investment
2. **Subordinates other stages** — aligns non-constraint stages to feed the bottleneck at its exact capacity (no faster, no slower)
3. **Eliminates NVA activities** — removes or automates pure waste steps
4. **Converts BNVA to automated** — applies automation, templates, or system integration to business-necessary overhead
5. **Introduces error-proofing (poka-yoke)** — builds validation, defaults, and constraints that prevent defects at source

Apply any user-specific `instructions` from FutureProof context — such as preferred tooling, organisational change appetite, ICA-facing SLA requirements, or prior experiment results — to calibrate recommendations.

## Step 4: Deliver Output

Produce a **Process Improvement Analysis Report** with the following sections:

### 4.1 — Executive Summary
Two-paragraph narrative: current-state diagnosis, recommended future state, and projected impact on the user's stated objective.

### 4.2 — Current-State Value Stream Summary Table

| Stage | Activity Type (VA/BNVA/NVA) | Owner | Cycle Time | Wait Time | Error Rate | Waste Type |
|-------|------------------------------|-------|------------|-----------|------------|------------|
| ...   | ...                          | ...   | ...        | ...       | ...        | ...        |

### 4.3 — Bottleneck Analysis
Identification of the binding constraint with supporting evidence and secondary constraint forecast.

### 4.4 — Waste Heat Map
Ranked list of waste instances by estimated annualised impact (hours or cost), with waste type classification.

### 4.5 — Root Cause Summary
5 Whys output for top 3 issues — structured as cause chains terminating in actionable root causes.

### 4.6 — Improvement Recommendations (Prioritised)
For each recommendation:
- **Change description**: Specific, implementable action (not directional advice)
- **Waste/constraint addressed**: Direct link to diagnosis
- **Implementation complexity**: Low / Medium / High
- **Expected impact**: Quantified where data permits (e.g., "Eliminates ~12 hours/week of manual reconciliation")
- **Prerequisites**: Dependencies, tooling, or approvals required

Recommendations ordered by **impact-to-effort ratio** (highest first).

### 4.7 — Future-State Process Summary
Revised stage-by-stage flow reflecting all recommended changes, with projected cycle time, wait time, and error rate per stage.

### 4.8 — Implementation Roadmap
Three-horizon phasing:
- **Quick wins** (0–2 weeks): Zero-cost or low-cost changes executable immediately
- **Structural improvements** (2–8 weeks): System changes, automation builds, role redesigns
- **Systemic transformation** (8+ weeks): Cross-functional redesigns, tooling migrations, culture/incentive shifts

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
FutureProof:save_experiment(skill="process-improvement-analyser", experiment={
  hypothesis: "Eliminating the [identified NVA stage] and routing directly to [downstream stage] reduces end-to-end cycle time without increasing error rate",
  variants: ["control: current process with manual handoff intact", "variant: direct routing with automated validation gate"],
  measurement: "Cycle time (end-to-end) and defect rate tracked over 30-day window across both variants",
  expected_impact: "20–35% reduction in cycle time with error rate held constant or improved"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="process-improvement-analyser",
  query="Latest automation and process orchestration patterns for [user's industry/process domain] — including AI-assisted workflow tools, RPA benchmarks, and Lean Six Sigma case studies from 2024",
  reason="Ensure recommendations reflect current best-in-class tooling and methodology, and identify proven intervention patterns for similar process archetypes"
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
FutureProof:save_session(skill="process-improvement-analyser", session={
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