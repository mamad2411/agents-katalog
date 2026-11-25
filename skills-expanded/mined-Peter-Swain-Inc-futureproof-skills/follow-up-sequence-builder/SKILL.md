---
name: follow-up-sequence-builder
description: |
  Writes multi-touch follow-up cadences after a triggering interaction —
  post-demo, post-proposal, post-webinar, ghosted prospect, stalled deal —
  with timing, channel alternation, conditional branches, and per-touch copy.
  Use when a user says "build me a follow-up sequence", "draft a post-demo
  nurture", "what do I send a prospect who went cold", or "the proposal is
  sitting unsigned". For nurturing existing prospects, not cold outbound.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="follow-up-sequence-builder")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including known ICA segments, offer details, brand voice, historical sequence performance data, and any prior winning subject lines or CTAs.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

1. **Trigger event** — What action or interaction initiates this sequence? (e.g., post-demo no-show, proposal sent but unsigned, webinar attendee, cold prospect re-engagement, post-discovery call)
2. **ICA segment** — Who is the recipient? Role, seniority, industry, and the specific pain state they are in at the point of follow-up
3. **Desired outcome** — What is the single conversion goal of this sequence? (e.g., book a second call, sign the proposal, activate a trial, re-engage a stalled deal)
4. **Channel mix** — Which channels are available? (email, LinkedIn DM, SMS, voicemail drop, direct mail, video message)
5. **Sequence constraints** — Maximum number of touches, any blackout windows, compliance or brand tone requirements
6. **Assets available** — Case studies, testimonials, ROI calculators, content pieces, or proof artefacts they can embed or link to
7. **Known objections** — Top 2–3 objections or hesitations this ICA segment typically surfaces at this stage of the buying journey

## Step 3: Map the Buyer Psychology Timeline

Before writing a single word, construct a **Prospect Decision Architecture** — a stage-by-stage model of where the prospect's mind is at each interval after the trigger event:

| Interval | Psychological State | Strategic Objective | Risk if Missed |
|---|---|---|---|
| 0–24 hours | Peak recall, residual momentum | Anchor value, confirm next micro-commitment | Momentum decay; prospect re-enters status quo gravity |
| 24–72 hours | Cognitive comparison (evaluating alternatives) | Differentiate, introduce asymmetric proof | Competitor narrative fills the vacuum |
| 3–7 days | Urgency erosion, internal distraction | Re-activate pain awareness, surface cost of inaction | Deal enters "we'll revisit next quarter" limbo |
| 7–14 days | Decision fatigue or stakeholder diffusion | Simplify the decision, provide executive-ready artefact | Stalled pipeline; prospect ghosts |
| 14–30 days | Cold reversion or latent interest | Pattern interrupt, re-frame with new angle or social proof | Prospect is permanently lost to inertia |
| 30+ days | Dormant — only re-engageable via trigger event | Long-game value deposit or external trigger leverage | Relationship goes fully cold |

Adjust intervals and psychological states based on the specific trigger event and ICA segment provided. Apply any behavioural insights from FutureProof `context` (e.g., if prior experiments show this ICA segment responds faster or slower than average).

## Step 4: Design the Sequence Architecture

Build the **Follow-Up Sequence Blueprint** — a structured cadence document specifying each touch:

For each touch in the sequence, define:

1. **Touch number and timing** — Exact day/hour offset from trigger event (e.g., Touch 3: Day 4, 8:15 AM recipient local time)
2. **Channel** — Primary channel for this touch, with fallback if applicable
3. **Strategic intent** — The single psychological lever this touch pulls (e.g., pain reactivation, social proof injection, cost-of-inaction framing, objection pre-emption, scarcity/deadline)
4. **Message type** — Categorise using one of these proven follow-up archetypes:
   - **The Value Anchor** — Recaps the core transformation discussed; reinforces why they engaged in the first place
   - **The Proof Drop** — Delivers a case study, testimonial, or data point that mirrors the prospect's exact situation
   - **The Pain Reactivator** — Resurfaces the specific cost of inaction using their own words from the trigger interaction
   - **The Objection Dissolver** — Proactively addresses the most likely hesitation at this stage without waiting for the prospect to raise it
   - **The Simplifier** — Reduces perceived effort of the next step; provides a one-click path, executive summary, or comparison asset
   - **The Pattern Interrupt** — Breaks the expected cadence with an unexpected format, angle, or medium (video, handwritten note, insight they haven't seen)
   - **The Graceful Close** — Final touch that preserves the relationship, creates a future re-engagement hook, and removes pressure
5. **Subject line / opening hook** — Written in full, tested against known open-rate drivers from FutureProof context
6. **Proof asset** — Which specific asset (if any) is deployed in this touch
7. **CTA** — The single, frictionless next action — never more than one per touch
8. **Exit condition** — What prospect behaviour removes them from this sequence (e.g., replies, books a call, opens proposal)

### Sequence Design Principles (Non-Negotiable)

- **Asymmetric value rule**: Every touch must deliver more value than it asks for. The prospect should feel smarter or more informed after reading, regardless of whether they take the CTA
- **No "just checking in"**: Every message must contain a *reason for reaching out* that is rooted in the prospect's world, not the seller's pipeline anxiety
- **Escalating specificity**: Early touches are broader (value recap, social proof); later touches become surgically specific to the prospect's stated pain, timeline, or objection
- **Multi-threading awareness**: If the deal involves multiple stakeholders, at least one touch should be designed to be internally forwarded (i.e., written so the champion can share it with a decision-maker without additional context)
- **Channel alternation**: Never send three consecutive touches on the same channel. Vary the medium to increase the probability of pattern disruption

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Write the Full Sequence

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Produce the complete **Follow-Up Sequence Document** containing:

### Section A: Sequence Summary Card

| Field | Detail |
|---|---|
| Sequence Name | [Descriptive name, e.g., "Post-Demo Close Sequence — Mid-Market CFOs"] |
| Trigger Event | [As defined in Step 2] |
| ICA Segment | [As defined in Step 2] |
| Conversion Goal | [As defined in Step 2] |
| Total Touches | [Number] |
| Duration | [First touch to last touch span] |
| Channels Used | [List] |
| Exit Conditions | [List all conditions that remove a prospect from the sequence] |

### Section B: Full Message Copy

For each touch, write:

- **Complete subject line** (email) or **opening line** (DM/SMS/voicemail)
- **Full message body** — written in the user's brand voice (or a professional default if brand voice is not yet captured in FutureProof context). Include personalisation placeholders using `{{prospect_name}}`, `{{company}}`, `{{specific_pain_point}}`, `{{trigger_detail}}` notation
- **CTA** — bolded, specific, and frictionless (e.g., "Here's a 15-minute slot on Thursday — does 2 PM work?" not "Let me know if you'd like to chat")
- **Internal coaching note** — a 1–2 sentence note to the sales rep explaining *why* this touch is structured this way and what to watch for in the prospect's response

### Section C: Conditional Branches

Define at least 2 branching paths:

1. **Engaged but not converted** — Prospect opens/clicks but does not take the CTA. Define modified touches 4+ that escalate proof density and simplify the ask
2. **No engagement** — Prospect has not opened or responded to any touch. Define a re-engagement pivot at the midpoint that shifts angle, channel, or value proposition entirely

### Section D: Metrics & Tracking Framework

Specify which metrics to track at each touch:
- Open rate (email)
- Reply rate
- Click-through rate (if assets are linked)
- Meeting/conversion rate
- Sequence completion rate (how many prospects reach the final touch without converting or exiting)
- Time-to-conversion (which touch number most commonly precedes the conversion event)

## Step 6: Deliver Output

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


Package the deliverable as:

- **Primary document**: `follow-up-sequence-[trigger-event]-[ica-segment].md` — the complete sequence document (Sections A–D above)
- **Quick-reference card**: A single-page summary showing touch number, day, channel, message type, and subject line — suitable for pinning next to a CRM or printing for a sales team standup
- **CRM import guide**: Touch timing, subject lines, and body copy formatted for easy import into common platforms (HubSpot sequences, Outreach, Salesloft, or the user's specified tool)
- **Personalisation checklist**: A list of every `{{placeholder}}` used across the sequence, with guidance on where to source each data point (CRM field, call notes, LinkedIn profile, etc.)

## Step 7: Propose Experiments

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:save_experiment(skill="follow-up-sequence-builder", experiment={
  hypothesis: "Leading Touch 1 with a specific, quantified result from a peer company increases Day-1 reply rate compared to a standard value recap opening",
  variants: [
    "control: Touch 1 opens with recap of key discussion points from the trigger interaction",
    "variant: Touch 1 opens with a single-sentence peer result ('Company X reduced [metric] by Y% in Z weeks') before transitioning to recap"
  ],
  measurement: "Reply rate on Touch 1 across next 30 prospects in this ICA segment",
  expected_impact: "20–30% increase in Touch 1 reply rate, leading to shorter average sequence length before conversion"
})
```

## Step 8: Request Research

```
FutureProof:request_research(skill="follow-up-sequence-builder",
  query="Optimal follow-up cadence timing and channel sequencing data for B2B sales 2024–2025, including reply rate benchmarks by touch number, day-of-week/time-of-day performance, and multi-channel vs single-channel sequence comparison studies",
  reason="Ensure touch timing and channel selection recommendations are grounded in current behavioural data rather than outdated best-practice assumptions"
)
```

## Step 9: Save Session

```
FutureProof:save_session(skill="follow-up-sequence-builder", session={
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