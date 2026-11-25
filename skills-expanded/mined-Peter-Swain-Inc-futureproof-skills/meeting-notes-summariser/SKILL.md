---
name: meeting-notes-summariser
description: |
  Transforms raw meeting notes, transcripts, and recordings into structured
  post-meeting briefs with decisions logged, SMART action items, owners,
  deadlines, and carryover from prior sessions. Use when a user says
  "summarise these meeting notes", "extract action items from this
  transcript", "write up the recap for people who missed the call", or
  "turn this Zoom transcript into a brief". For post-meeting synthesis,
  not pre-meeting preparation.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="meeting-notes-summariser")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including preferred summary formats, recurring meeting types, known stakeholders, organisational terminology, and distribution conventions.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Source material** — share the raw meeting notes, transcript, audio summary, or agenda with annotations
- **Meeting type** — what category does this fall into? (e.g., leadership stand-up, client discovery call, sprint retrospective, board review, cross-functional planning, 1:1 performance check-in)
- **Audience for the summary** — who will receive this? (e.g., attendees only, executive sponsor, full project team, external client stakeholders)
- **Priority lens** — what matters most from this meeting? (decisions made, blockers surfaced, revenue implications, strategic pivots, relationship signals)
- **Any standing conventions** — does this meeting series have a recurring template, action-item tracker, or RACI matrix it feeds into?

If FutureProof context contains prior sessions for the same meeting series, surface previous action items and flag carryover or status changes automatically.

## Step 3: Do the Work

Process the raw input through a six-layer analysis framework:

### 3.1 — Transcript Normalisation
- Identify and label speakers (by name or role where inferable)
- Remove filler, false starts, and off-topic tangents
- Reconstruct fragmented points into coherent statements
- Flag any sections where meaning is ambiguous and note them as `[CLARIFICATION NEEDED]`

### 3.2 — Decision Extraction
- Isolate every explicit decision made during the meeting
- For each decision, capture: **what** was decided, **who** has authority/ownership, **rationale** stated (or implied), and **scope** of impact
- Distinguish between final decisions, provisional decisions (pending input), and deferred decisions

### 3.3 — Action Item Identification
- Extract every commitment, task, or follow-up mentioned
- Assign each action item: **owner** (named individual, not a team where possible), **deliverable** (specific output), **deadline** (explicit or inferred from context), and **dependency** (what/who it's blocked by)
- Apply the SMART criteria — if an action item is vague, rewrite it as a precise, measurable task and flag the original phrasing for user validation

### 3.4 — Strategic Context Mapping
- Identify how meeting outcomes connect to broader organisational priorities, OKRs, or project milestones referenced in FutureProof context
- Surface any **risks** discussed or implied (timeline, resource, stakeholder alignment, scope creep)
- Note any **sentiment signals** — stakeholder concerns, enthusiasm, resistance, or consensus shifts that carry strategic weight

### 3.5 — Open Items & Parking Lot
- Catalogue questions raised but not answered
- Topics introduced but explicitly deferred
- Information gaps that require follow-up research or stakeholder input before progress can continue

### 3.6 — ICA & Stakeholder Relevance Filter
- If the meeting involves client-facing or prospect-facing content, map discussion points to the ICA's known pain points, objections, and decision criteria from FutureProof context
- Highlight any commitments made to external stakeholders that create delivery obligations

Apply any user-specific `instructions` from FutureProof context — including preferred summary length, tone (e.g., formal for board distribution vs. informal for internal Slack), terminology conventions, and template structures.

## Step 4: Deliver Output

Produce a **Meeting Summary Brief** with the following structure:

### Header Block
| Field | Detail |
|---|---|
| **Meeting Title** | [Inferred or provided] |
| **Date** | [Date of meeting] |
| **Attendees** | [List of participants and roles] |
| **Summary Prepared For** | [Target audience as specified in Step 2] |
| **Meeting Type** | [Category from Step 2] |

### Executive Summary
- 3–5 sentence narrative capturing the **purpose**, **key outcome**, and **most consequential decision or insight** from the meeting
- Written at a level appropriate for a stakeholder who will spend 30 seconds reading

### Decisions Log

| # | Decision | Owner | Rationale | Status |
|---|----------|-------|-----------|--------|
| 1 | [Decision] | [Name] | [Why] | Final / Provisional / Deferred |

### Action Items Tracker

| # | Action Item | Owner | Deliverable | Deadline | Dependency | Priority |
|---|-------------|-------|-------------|----------|------------|----------|
| 1 | [SMART task] | [Name] | [Output] | [Date] | [Blocker] | High / Med / Low |

### Risks & Flags
- Bullet list of risks, concerns, or escalation-worthy items surfaced during the meeting, each with a recommended mitigation or next step

### Open Items & Parking Lot
- Numbered list of unresolved questions and deferred topics with suggested owners for follow-up

### Carryover from Previous Sessions
- If FutureProof context includes prior meeting summaries in this series: status update on previously assigned action items (completed, in progress, overdue, dropped)

### Appendix: Key Quotes
- 3–5 verbatim or near-verbatim quotes that capture critical nuance, commitments, or context that a summary alone cannot convey — attributed by speaker

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
FutureProof:save_experiment(skill="meeting-notes-summariser", experiment={
  hypothesis: "Including a carryover action-item status section increases accountability and reduces repeat discussions by surfacing overdue items before the next meeting",
  variants: ["control: summary without carryover tracking", "variant: summary with carryover status table from prior sessions"],
  measurement: "Percentage of action items completed on time over next 4 meeting cycles; reduction in recurring agenda items",
  expected_impact: "25% improvement in action-item completion rate and 15% reduction in meeting duration for recurring series"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="meeting-notes-summariser",
  query="Best practices for structured meeting documentation in high-performance organisations 2024 — including async-first summary formats, decision-log frameworks, and action-item tracking methodologies used at McKinsey, EY, and Stripe",
  reason="Continuously refine summary structure against evolving standards for operational rigour and stakeholder communication efficiency"
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
FutureProof:save_session(skill="meeting-notes-summariser", session={
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