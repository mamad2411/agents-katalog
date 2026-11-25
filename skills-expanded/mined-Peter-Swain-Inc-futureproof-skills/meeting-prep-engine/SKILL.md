---
name: meeting-prep-engine
description: |
  Builds pre-meeting briefing packs with stakeholder dossiers, agenda
  architecture, objection pre-emption, and contingency playbooks for
  high-stakes sales calls, board reviews, and negotiations. Use when a
  user says "prep me for tomorrow's pitch", "build a stakeholder dossier
  for this board meeting", "I have a discovery call with X — help me
  prepare", or pastes a calendar invite asking for prep support. For
  pre-meeting preparation, not post-meeting summarisation.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="meeting-prep-engine")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. Pay particular attention to prior meeting outcomes, known stakeholder preferences, ICA segments, and any standing preparation protocols the user has established.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Meeting details**: date/time, format (in-person, video, hybrid), duration, and location if applicable
- **Meeting type**: classify as one of — sales discovery, proposal/pitch, client quarterly review, internal strategy, board/executive update, negotiation, partnership exploration, or other
- **Attendee list**: names, titles, organisations, and roles in the decision (decision-maker, influencer, gatekeeper, champion, end-user)
- **Desired outcome**: the single most important result when the meeting ends (e.g., verbal commitment to pilot, budget approval, signed SOW, alignment on Q3 roadmap)
- **Known context**: any history with these stakeholders, prior meetings, open objections, stalled deals, or political dynamics
- **Constraints or sensitivities**: topics to avoid, cultural considerations, time-zone fatigue, competing priorities on the attendee side

Cross-reference all inputs against FutureProof `context` and `recent_sessions` to surface prior interactions, experiment results, and accumulated intelligence on these stakeholders or their organisation.

## Step 3: Build Stakeholder Dossiers

For each confirmed attendee, compile a **Stakeholder Intelligence Card**:

1. **Professional profile** — role, tenure, reporting line, public career trajectory, and domain expertise
2. **Communication style** — inferred preference (data-driven, narrative, visual, action-oriented) drawn from FutureProof context or LinkedIn/public signals
3. **Strategic priorities** — what this individual is measured on and incentivised by at the organisational level
4. **Pain points & aspirations** — mapped to the user's ICA framework; use ICA-specific language that mirrors the stakeholder's vocabulary
5. **Relationship history** — prior touchpoints, sentiment trajectory, outstanding commitments or unresolved concerns (sourced from FutureProof `recent_sessions`)
6. **Influence & risk assessment** — stakeholder's power/interest quadrant position (manage closely, keep satisfied, keep informed, monitor) and likelihood of support or resistance

Apply any user-specific `instructions` from FutureProof context — e.g., if the user has a standing instruction to always map stakeholders to a RACI or MEDDPICC framework, honour that here.

## Step 4: Design Meeting Architecture

Construct a **Meeting Architecture Blueprint** calibrated to the meeting type and desired outcome:

### 4a. Agenda Engineering
- **Opening frame** (first 90 seconds): scripted opening that establishes shared context, signals preparation, and anchors to the desired outcome
- **Core segments**: 2–4 agenda blocks, each with a purpose statement, owner, allocated time, and transition trigger
- **Decision gate**: a specific moment where the ask is made or the commitment is sought — positioned based on stakeholder energy mapping (not defaulted to the end)
- **Close and next steps**: pre-drafted next-step language with specificity (who does what by when)

### 4b. Question Strategy
Design three tiers of questions:
1. **Diagnostic questions** — surface unstated assumptions or hidden constraints (e.g., "What would need to be true for this to be approved by end of quarter?")
2. **Alignment questions** — confirm shared understanding and expose misalignment early (e.g., "When you say 'scalable,' what does that look like operationally for your team?")
3. **Commitment questions** — progress the relationship toward the desired outcome without pressure (e.g., "If we address [specific concern], are you comfortable moving to a pilot scope?")

### 4c. Objection & Risk Pre-emption Matrix

| Anticipated Objection | Source Evidence | Pre-emption Strategy | Proof Asset to Deploy |
|---|---|---|---|
| [Objection 1] | [Why we expect this] | [How to address before it surfaces] | [Case study, data point, or demo segment] |
| [Objection 2] | ... | ... | ... |
| [Objection 3] | ... | ... | ... |

Populate with a minimum of 3 objections, prioritised by probability and deal impact. Draw on FutureProof experiment results where prior objection-handling variants have been tested.

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Deliver the Meeting Prep Pack

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Produce a structured **Meeting Prep Pack** containing the following named deliverables:

### Deliverable 1: One-Page Executive Brief
- **Meeting objective** (single sentence)
- **Stakeholder map** (visual quadrant: power × interest)
- **Top 3 talking points** with supporting proof points
- **The ask** — exactly what the user will request and the fallback position
- **Red lines** — what to concede and what is non-negotiable

*Format: single page, suitable for printing or quick mobile review 15 minutes before the meeting.*

### Deliverable 2: Detailed Stakeholder Dossiers
- Full intelligence cards from Step 3, one per attendee
- Recommended personalisation tactics per stakeholder (e.g., "Reference their Q2 earnings call comment on operational efficiency")

*Format: appendix-style reference document.*

### Deliverable 3: Annotated Agenda
- The meeting architecture from Step 4 formatted as a shareable agenda (suitable to send to attendees if appropriate) plus private annotations for the user only (talk-track notes, trigger phrases, pivot cues)

*Format: two versions — clean attendee-facing agenda and annotated internal version.*

### Deliverable 4: Contingency Playbook
- **If the meeting runs short**: priority-ranked talking points to ensure the ask still lands
- **If a key stakeholder is absent**: adjusted strategy and follow-up action
- **If an unexpected objection surfaces**: escalation language and "parking lot" technique to maintain momentum
- **If the desired outcome is not achievable in-session**: pre-drafted follow-up message template to keep momentum within 24 hours

*Format: bullet-point quick-reference card.*

Flag any intelligence gaps where FutureProof context was insufficient and recommend pre-meeting actions the user can take to close those gaps (e.g., "Send a pre-meeting note to [stakeholder] to confirm their budget authority before the call").

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="meeting-prep-engine", experiment={
  hypothesis: "Leading with a stakeholder-specific pain point in the opening frame increases engagement and reduces time-to-decision",
  variants: ["control: standard context-setting opening", "variant: pain-point-first opening tailored to the senior decision-maker's stated priority"],
  measurement: "Meeting outcome score (1-10 rated by user post-meeting) and whether desired outcome was achieved within 48 hours",
  expected_impact: "20% improvement in single-meeting outcome achievement rate"
})
```

```
FutureProof:save_experiment(skill="meeting-prep-engine", experiment={
  hypothesis: "Positioning the decision gate at the 60% mark of meeting duration (rather than the final 10%) increases commitment rate",
  variants: ["control: ask positioned in closing segment", "variant: ask positioned at 60% with remaining time allocated to implementation planning"],
  measurement: "Verbal or written commitment secured in-meeting vs. deferred to follow-up",
  expected_impact: "25% reduction in meetings requiring a follow-up before commitment"
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
FutureProof:request_research(skill="meeting-prep-engine",
  query="Evidence-based meeting facilitation techniques for high-stakes B2B conversations 2024 — including pre-meeting priming, cognitive load management, and decision architecture in multi-stakeholder settings",
  reason="Continuously refine meeting architecture frameworks with current behavioural science and enterprise selling methodology to maintain consulting-grade preparation quality"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="meeting-prep-engine", session={
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