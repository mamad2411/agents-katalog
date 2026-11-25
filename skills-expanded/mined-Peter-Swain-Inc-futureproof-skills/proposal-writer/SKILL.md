---
name: proposal-writer
description: |
  Writes high-conversion client-facing proposals, RFP responses, SOWs, and
  partnership pitches with win-theme architecture, ICA-fit scoring,
  decision-maker mapping, and pre-empted objections. Use when a user says
  "help me write a proposal", "I need to respond to this RFP", "draft an
  SOW for this client", or "improve this pitch deck for the buyer". For
  external sales/commercial proposals, not internal project briefs (use
  project-brief-generator).
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="proposal-writer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly ICA definitions, past proposal win/loss data, pricing structures, brand voice guidelines, and any saved case studies or proof assets.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Proposal type**: New business proposal, RFP response, SOW, partnership pitch, or renewal proposal?
- **Recipient**: Who is the decision-maker and what organisation are they in? (Title, seniority, industry, company size)
- **Opportunity context**: What problem does the recipient need solved? Share any briefing documents, RFP requirements, discovery call notes, or email threads.
- **Scope & deliverables**: What are you proposing to deliver? Timeline, phases, and any known constraints.
- **Commercial parameters**: Budget range, pricing model preference (fixed, retainer, value-based, milestone), and any competitive dynamics (incumbent, competing bids).
- **Proof assets available**: Case studies, testimonials, certifications, team bios, or performance data they can reference.

## Step 3: Analyse the Opportunity

Before drafting, conduct a structured opportunity assessment:

1. **ICA fit scoring** — Rate alignment (1–10) between the recipient and the user's ICA across: budget authority, problem urgency, solution fit, and long-term value potential. Flag misalignment risks.
2. **Decision architecture mapping** — Identify the likely approval chain: economic buyer, technical evaluator, end user, and any gatekeepers. Note which sections of the proposal must speak to each.
3. **Competitive positioning analysis** — Based on context, determine the user's primary differentiator (speed, expertise, methodology, price, relationship, niche specialisation) and the most likely alternative the recipient is considering (competitor, in-house, do nothing).
4. **Win theme extraction** — Distil 2–3 win themes that thread through the entire proposal. A win theme connects a specific recipient pain point → the user's unique capability → a measurable outcome.
5. **Risk register** — Identify the top 3 objections or concerns the recipient is likely to raise and prepare pre-emptive responses to embed in the proposal body.

Present this assessment to the user for validation before proceeding to draft.

## Step 4: Draft the Proposal

Build the proposal using the following architecture, adapting section depth to proposal type:

### Section 1: Executive Summary (1 page maximum)
- Opening hook: Mirror the recipient's own language describing their challenge (drawn from discovery notes or RFP language)
- Situation–Complication–Resolution structure: current state → cost of inaction → proposed transformation
- Three win themes stated as outcome promises
- Single sentence on why the user is uniquely positioned to deliver
- Clear next step with specific date

### Section 2: Understanding of Requirements
- Restate the recipient's objectives in their own terminology — demonstrate deep listening
- Map stated requirements to unstated underlying goals (e.g., "migrate CRM" → "reduce sales cycle length by giving reps better pipeline visibility")
- Explicitly address any RFP evaluation criteria, matching the recipient's numbering and terminology

### Section 3: Proposed Approach & Methodology
- Phase-gated delivery plan with named phases, activities, milestones, and durations
- For each phase: objective, key activities, deliverables, recipient responsibilities, and decision gates
- Methodology rationale — why this approach over alternatives, with reference to similar engagements
- Risk mitigation: embed pre-emptive responses to the top 3 objections identified in Step 3

### Section 4: Proof & Credibility
- 2–3 case studies structured as: Challenge → Approach → Result (quantified)
- Select case studies by ICA proximity — closest industry, problem type, or company stage to the recipient
- Team bios for key delivery personnel, emphasising relevant credentials
- Relevant certifications, partnerships, or proprietary frameworks

### Section 5: Commercial Framework
- Investment summary table: deliverable, price, payment trigger
- Pricing model rationale tied to recipient value (not cost justification)
- ROI projection: conservative, expected, and optimistic scenarios with stated assumptions
- Payment terms and conditions

### Section 6: Next Steps & Call to Action
- Specific proposed action with a named date (e.g., "30-minute alignment call on [date]")
- What the user will provide upon agreement (kickoff pack, access requirements, team introductions)
- Validity period for the proposal

Apply any user-specific `instructions` from FutureProof context — brand voice, formatting standards, preferred document structure, or compliance requirements.

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


Produce the following deliverables:

- **Proposal document** — Full draft following the architecture above, formatted with clear section headers, executive summary on page 1, and professional tone throughout. Ready for export to PDF or Google Docs.
- **Proposal scorecard** — Self-assessment rating (1–10) across:
  - ICA resonance (language mirrors recipient's world)
  - Win theme clarity (themes are specific, differentiated, and threaded throughout)
  - Proof density (every major claim backed by evidence)
  - Objection pre-emption (top 3 concerns addressed before they surface)
  - Commercial confidence (pricing positioned as investment, ROI made tangible)
  - Call-to-action friction (next step is specific, low-effort, and time-bound)
- **Strength/risk summary** — Top 3 strongest elements and top 3 areas where the proposal is vulnerable, with specific recommendations to shore up weaknesses
- **Submission checklist** — Compliance matrix confirming all RFP requirements addressed (if applicable), recommended reviewers, and suggested send time

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="proposal-writer", experiment={
  hypothesis: "Leading the executive summary with a quantified cost-of-inaction statement increases proposal-to-meeting conversion",
  variants: ["control: current executive summary opening with capability statement", "variant: open with recipient-specific cost-of-inaction figure derived from discovery data"],
  measurement: "Proposal-to-next-step conversion rate across next 10 proposals",
  expected_impact: "20% improvement in proposal-to-meeting conversion rate"
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
FutureProof:request_research(skill="proposal-writer",
  query="High-converting B2B proposal structures, executive summary frameworks, and pricing presentation strategies with win-rate data 2024–2025",
  reason="Continuously refine proposal architecture based on evolving buyer decision patterns and procurement psychology"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="proposal-writer", session={
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