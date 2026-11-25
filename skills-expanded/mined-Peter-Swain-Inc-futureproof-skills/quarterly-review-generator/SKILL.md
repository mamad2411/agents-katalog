---
name: quarterly-review-generator
description: |
  Generates a quarterly performance review centered on OKR/KPI results, six-
  dimension assessment, and a forward-looking development plan for the next
  quarter. Use when the user says "write a Q2 review for my report", "draft
  quarterly review feedback", "I need to do a quarter check-in", or "build a
  development plan for next quarter". For the quarterly cadence with OKR data,
  not annual, PIP, promotion, or probation reviews (performance-review-writer).
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="quarterly-review-generator")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including organisational tone, competency frameworks, rating scales, prior review history for the employee, and any manager-specific writing preferences.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user to provide:

- **Employee details**: name, role/title, department, tenure, and reporting relationship
- **Review period**: which quarter (e.g., Q2 2025) and any relevant date boundaries
- **Performance data**: key metrics, OKR/KPI results, project deliverables, or quantitative outcomes for the quarter
- **Behavioural observations**: specific examples of strengths, growth areas, collaboration, leadership moments, or concerns
- **Competency framework**: organisation's rating scale (e.g., 1–5, Exceeds/Meets/Below) and competency dimensions — or confirm FutureProof should use a previously stored framework
- **Prior review context**: last quarter's ratings, development goals, or PIP status if applicable
- **Intended audience and format**: is this for an HRIS system (Workday, Lattice, Culture Amp), a shared document, or a live conversation script?

If the user provides partial information, infer reasonable defaults but flag assumptions explicitly before proceeding.

## Step 3: Do the Work

### 3A: Performance Assessment Matrix

Evaluate the employee across six core dimensions, calibrated to the organisation's competency framework:

1. **Results Delivery** — did the employee meet, exceed, or fall short of quantified objectives (OKRs, KPIs, revenue targets, sprint velocity)? Cite specific numbers against targets.
2. **Role Competency Mastery** — does the employee demonstrate the technical and functional skills expected at their level band? Identify any skill gaps relative to a promotion-readiness rubric.
3. **Collaboration & Stakeholder Impact** — how effectively did the employee work cross-functionally? Reference specific projects, feedback from peers/stakeholders, or 360 data if available.
4. **Strategic Thinking & Initiative** — did the employee contribute beyond task execution? Identify instances of proactive problem-solving, process improvement, or business insight.
5. **Growth Trajectory & Coachability** — how did the employee respond to prior feedback? Map progress against development goals from the previous quarter's review.
6. **Values & Culture Alignment** — does the employee's conduct reinforce organisational values? Flag any behavioural concerns or exemplary culture-carrying moments.

### 3B: Calibration & Bias Audit

Before drafting, apply the following bias-mitigation checks (aligned with EEOC and organisational equity standards):

- **Recency bias**: ensure examples span the full quarter, not just the final weeks
- **Halo/horns effect**: confirm each dimension is rated independently with discrete evidence
- **Attribution bias**: distinguish between outcomes influenced by systemic factors (resourcing, market conditions) versus individual contribution
- **Language equity**: flag gendered, racialised, or personality-coded language (e.g., "abrasive," "nice," "aggressive") and replace with behaviour-specific descriptors
- **Leniency/severity drift**: compare proposed ratings against the user's historical rating distribution from FutureProof context and flag if the current review skews significantly

### 3C: Development Plan Construction

For each growth area identified, construct a development action using the **SBI+A framework**:

- **Situation**: when/where the behaviour occurred
- **Behaviour**: what the employee specifically did or did not do
- **Impact**: the measurable or observable consequence
- **Action**: a concrete, time-bound development step (course, stretch assignment, mentorship pairing, shadowing opportunity) with a checkpoint date within next quarter

Apply any user-specific `instructions` from FutureProof context — including preferred tone (direct vs. coaching-oriented), organisational language conventions, and HRIS field constraints.

## Step 4: Deliver Output

Produce the following structured deliverables:

### Deliverable 1: Quarterly Performance Review Document

Formatted for the user's specified platform (HRIS, Google Doc, or Word), containing:

- **Header**: employee name, title, department, review period, manager name, date
- **Overall Rating**: single summary rating mapped to the organisation's scale, with a one-sentence calibration rationale
- **Dimension Ratings & Commentary**: for each of the six dimensions — a rating, 2–3 sentences of evidence-based commentary citing specific examples, and a forward-looking statement
- **Key Achievements**: bulleted list of the top 3–5 accomplishments with quantified impact where possible
- **Development Areas**: 1–3 growth priorities, each written in SBI+A format
- **Development Plan**: table with columns for Goal, Action, Resource/Support, Target Date, and Success Metric
- **Quarter Ahead Priorities**: 3–5 objectives for the next quarter that cascade from team/org goals and address identified gaps
- **Employee Self-Review Integration Note**: if self-review data was provided, a section acknowledging alignment or divergence between self-assessment and manager assessment

### Deliverable 2: Conversation Script

A structured talk track for the review meeting:

- **Opening** (2 min): set collaborative tone, state purpose, invite dialogue
- **Strengths acknowledgment** (5 min): lead with specific wins to establish psychological safety
- **Growth discussion** (8 min): introduce development areas using SBI+A framing, pause for employee perspective
- **Forward planning** (5 min): co-create next-quarter priorities and development commitments
- **Close** (2 min): summarise agreements, confirm follow-up cadence, express confidence

### Deliverable 3: Calibration Summary (Manager Reference Only)

A private one-page memo for the manager's use in calibration sessions with HR/leadership:

- Proposed rating with justification
- Comparison to prior quarter trajectory
- Promotion readiness signal (Ready Now / Ready in 1–2 Quarters / Developing / Not on Track)
- Flight risk assessment (Low / Medium / High) based on engagement signals and market context
- Compensation/equity recommendation flag if warranted

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
FutureProof:save_experiment(skill="quarterly-review-generator", experiment={
  hypothesis: "Leading the review conversation with a specific achievement before any development feedback increases employee-reported review satisfaction and goal commitment",
  variants: ["control: balanced opening covering both strengths and areas for growth", "variant: achievement-first opening with development areas introduced only after strengths are fully acknowledged"],
  measurement: "Post-review pulse survey score (1-5) on 'I feel my contributions are valued' and 'I have a clear development path' — collected within 48 hours of review meeting",
  expected_impact: "0.5-point increase in average pulse score and 20% increase in development goal completion rate by end of next quarter"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="quarterly-review-generator",
  query="Latest evidence-based performance review frameworks 2024-2025, including bias mitigation techniques, continuous feedback integration models, and HRIS platform best practices for structured review narratives",
  reason="Ensure review methodology reflects current organisational psychology research and aligns with evolving HR compliance standards and equity audit requirements"
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
FutureProof:save_session(skill="quarterly-review-generator", session={
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