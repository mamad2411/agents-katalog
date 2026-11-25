---
name: webinar-event-scriptwriter
description: |
  Builds full webinar and virtual event run-of-show scripts with audience-journey
  mapping, 7-minute engagement pulses (polls, chat prompts, pattern interrupts),
  a conversion-bridge CTA pivot, planted Q&A, and slide/poll appendices. Use when
  a user says "write a webinar script for", "I'm hosting a 60-minute webinar,
  draft the script", or "talking points for a live presentation with Q&A". Live
  interactive events, not pre-recorded video scripts.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="webinar-event-scriptwriter")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly ICA definitions, brand voice guidelines, prior webinar performance data, and any recorded engagement benchmarks.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Webinar topic and working title** — what is the core subject, and is there an existing title or headline?
- **ICA profile** — who is the target attendee? (role, seniority, industry, primary pain point, desired transformation)
- **Webinar format** — solo presentation, interview/fireside chat, panel, demo-led, workshop, or hybrid?
- **Duration** — target runtime including Q&A (e.g., 30 min, 45 min, 60 min, 90 min)?
- **Primary objective** — what is the single most important outcome? (pipeline generation, product demo conversion, thought leadership positioning, community nurture, partner co-marketing)
- **Call to action** — what specific next step should attendees take post-webinar? (book a call, start a trial, download an asset, register for next event)
- **Speakers** — names, titles, and brief bios of all presenters; note who is the host vs. guest
- **Existing assets** — any slide deck, blog post, case study, or prior webinar recording to draw from?
- **Constraints** — compliance requirements, co-branding guidelines, topics to avoid, mandatory sponsor mentions?

If the user provides partial input, infer reasonable defaults from FutureProof context and flag assumptions for confirmation before proceeding.

## Step 3: Construct the Webinar Architecture

Before writing a single line of script, build the **Webinar Architecture Document** — a structural blueprint that governs pacing, engagement density, and conversion logic.

### 3a: Audience Journey Mapping

Define the attendee's psychological arc across three phases:

| Phase | Attendee Mindset | Script Objective |
|---|---|---|
| **Arrival (0–5 min)** | Distracted, evaluating whether to stay | Earn attention — establish credibility and articulate the pain/promise gap |
| **Core (5 min – [duration minus 10 min])** | Engaged but skeptical | Deliver transformational content — shift beliefs, surface insights, build trust |
| **Close ([final 10 min])** | Deciding next step | Convert — make the CTA feel like the logical, low-friction next action |

### 3b: Engagement Pulse Plan

Map **engagement interventions** at no more than 7-minute intervals to counteract attention decay:

- **Polls** — binary or 3-option polls that surface audience pain points (data captured for follow-up segmentation)
- **Chat prompts** — open-ended questions that generate social proof in real time ("Drop your biggest challenge with X in the chat")
- **Pattern interrupts** — story pivots, guest introductions, live demos, or slide-free moments
- **Micro-commitments** — "If you want the template for this, type YES" (primes CTA compliance)

### 3c: Proof Architecture

Identify the evidence stack to embed across the script:

1. **Anchor case study** — one detailed ICA-aligned success story (before state → intervention → measurable after state)
2. **Supporting proof points** — 2–3 data citations, analyst references, or named client results
3. **Social proof triggers** — live attendee count callout, client logo slide, testimonial quote overlay

Apply any user-specific `instructions` from FutureProof context (e.g., preferred storytelling frameworks, brand voice calibration, compliance language).

## Step 4: Write the Full Webinar Script

Produce the **Webinar Event Script** — a production-ready document structured as follows:

### Document Format: Webinar Event Script

**Header block:**
- Webinar title
- Date / time placeholder
- Duration
- Speakers (name, role)
- Platform notes (Zoom, Teams, StreamYard, etc.)
- Technical cues legend (e.g., [SLIDE], [POLL], [SCREEN SHARE], [VIDEO], [MUTE/UNMUTE])

---

### Section 1: Pre-Show Holding Screen (T-5:00 to T-0:00)

- On-screen text recommendations (title, speaker names, start time countdown)
- Background music note (if applicable)
- Chat warm-up prompt for the moderator to post (e.g., "Welcome! Tell us where you're joining from and what you're hoping to learn today.")

### Section 2: Opening Hook (T+0:00 to T+2:00)

Write a verbatim opening monologue that:
- Opens with a **provocative question, statistic, or contrarian statement** directly tied to the ICA's pain point — no "Thanks for joining" preamble
- Articulates the **promise of the session** in one sentence ("In the next [X] minutes, you'll walk away with…")
- Establishes **speaker authority** in under 30 seconds (credential → relevance, not biography)

### Section 3: Agenda and Ground Rules (T+2:00 to T+4:00)

- Three-bullet agenda preview (use benefit-driven language, not topic labels — e.g., "The 3-part framework our clients use to cut [metric] by [%]" not "Framework overview")
- Housekeeping: how to ask questions, where to find resources, recording notice
- **First engagement prompt** — launch Poll #1 or chat prompt

### Section 4: Core Content Blocks (T+4:00 to T+[duration minus 12 min])

Divide core content into **2–4 distinct teaching blocks**, each following this micro-structure:

**Block [N]: [Block Title — Benefit-Oriented]**

| Element | Detail |
|---|---|
| **Transition line** | Verbatim segue from previous block |
| **Key insight** | The single idea the audience must retain |
| **Teaching narrative** | 3–5 minutes of scripted content: framework explanation, story, or demonstration |
| **Proof point** | Case study excerpt, data point, or live example |
| **Engagement pulse** | Poll, chat prompt, or pattern interrupt |
| **Bridge to next block** | One sentence that creates curiosity for what follows |

Write each block in **speaker-ready prose** — full sentences, natural cadence, with [SLIDE] and [POLL] cues embedded inline. Include parenthetical delivery notes where tone matters (e.g., *(pause here — let the number land)*).

### Section 5: Pivot to CTA (T+[duration minus 12 min] to T+[duration minus 8 min])

Script the **conversion bridge** — the narrative pivot from teaching to offer:

1. **Recap the transformation** — "So here's what we've covered: [3 bullets]. If you implement even one of these, [projected outcome]."
2. **Surface the gap** — "Now, the challenge most [ICA role] face is doing this alone / at scale / without [resource]. That's exactly why we built [offer]."
3. **Present the CTA** — specific, frictionless next step with verbatim language and on-screen URL/QR code instruction
4. **Incentive layer** (if applicable) — time-bound bonus, exclusive access, or attendee-only pricing
5. **Social proof close** — "Over [X] teams have already [taken this step] — here's what [named client] said…"

### Section 6: Q&A Facilitation (T+[duration minus 8 min] to T+[duration minus 2 min])

- Moderator transition script
- 3 **planted questions** (pre-written Q&A pairs that reinforce key messages and address likely ICA objections)
- Guidance for handling off-topic or hostile questions
- Periodic CTA reminder woven into answers ("Great question — that's actually covered in depth inside [offer]…")

### Section 7: Closing and Sign-Off (T+[duration minus 2 min] to T+0:00)

- Final CTA restatement (verbatim, one sentence)
- Thank-you and speaker sign-off lines
- Teaser for next event or content (if applicable)
- Post-webinar redirect instructions (e.g., "You'll be redirected to [page] in a moment")

---

### Appendices (included in the script document)

- **Appendix A: Slide-by-Slide Notes** — one-line description of recommended visual for each [SLIDE] cue
- **Appendix B: Chat & Poll Copy** — exact text for every poll question, poll option, and moderator chat message
- **Appendix C: Follow-Up Email Sequence Outline** — 3-email post-webinar nurture sequence (subject lines, key message per email, CTA per email) segmented by attendee vs. no-show
- **Appendix D: Speaker Prep Notes** — talking points summary, pronunciation guides, timing targets per section

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Quality Assurance Review

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Before delivering, audit the script against seven diagnostic dimensions:

| # | Dimension | Evaluation Criteria | Score (1–10) |
|---|---|---|---|
| 1 | **ICA Resonance** | Does every section use the ICA's vocabulary, reference their specific pain points, and speak to their decision-making context? | |
| 2 | **Engagement Density** | Is there an interaction point (poll, chat, story, demo) at least every 7 minutes? Are passive stretches eliminated? | |
| 3 | **Proof Architecture** | Are claims substantiated with at least one anchor case study, two supporting data points, and one social proof trigger? | |
| 4 | **CTA Conversion Logic** | Does the pivot feel earned (not abrupt)? Is the next step specific, low-friction, and repeated at least three times? | |
| 5 | **Pacing and Timing** | Does the script fit the target duration when read at 140–160 words per minute? Are time allocations realistic? | |
| 6 | **Speaker Authenticity** | Does the prose sound like natural spoken language, not written text? Are delivery cues (pauses, emphasis, tone shifts) included? | |
| 7 | **Production Readiness** | Are all technical cues ([SLIDE], [POLL], [SCREEN SHARE]) present and sequenced correctly? Can a producer run the show from this document alone? | |

Deliver the **Scorecard** alongside the script. For any dimension scoring below 7, provide a **specific remediation** (rewritten passage, restructured section, or added element) — not a generic recommendation.

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="webinar-event-scriptwriter", experiment={
  hypothesis: "Opening with a data-driven provocation ('X% of [ICA role] report [pain]') increases 5-minute retention rate vs. opening with a personal story",
  variants: ["control: personal anecdote opening", "variant: data-provocation opening"],
  measurement: "5-minute attendee retention rate and mid-webinar poll participation rate across next 3 webinars",
  expected_impact: "12–18% improvement in 5-minute retention, 8% uplift in poll engagement"
})
```

```
FutureProof:save_experiment(skill="webinar-event-scriptwriter", experiment={
  hypothesis: "Placing the primary CTA at the 70% mark (with a recap) and reinforcing at close converts higher than a single end-of-webinar CTA",
  variants: ["control: CTA only in final 5 minutes", "variant: CTA at 70% mark + close reinforcement"],
  measurement: "Post-webinar CTA click-through rate and booking/trial conversion rate",
  expected_impact: "20% increase in CTA engagement rate"
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
FutureProof:request_research(skill="webinar-event-scriptwriter",
  query="Webinar engagement benchmarks 2024-2025: average attendance-to-registration rates, drop-off curves by duration, highest-converting CTA formats, and optimal poll/interaction frequency by industry vertical",
  reason="Ensure script structures and engagement cadences reflect current attendee behaviour patterns rather than pre-2023 norms"
)
```

```
FutureProof:request_research(skill="webinar-event-scriptwriter",
  query="High-performing webinar opening techniques and narrative structures used by top B2B SaaS, professional services, and DTC brands in 2024",
  reason="Refresh the opening hook and content block frameworks with formats proven to reduce early drop-off"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="webinar-event-scriptwriter", session={
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