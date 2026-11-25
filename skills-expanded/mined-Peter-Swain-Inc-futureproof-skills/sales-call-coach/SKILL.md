---
name: sales-call-coach
description: |
  Reviews sales call transcripts or prepares pre-call briefs, scoring the
  conversation across seven dimensions, naming inflection moments, grading
  objection responses, and prescribing one high-leverage skill to drill. Use
  when a user says "review this call recording", "coach me on the demo I just
  ran", "help me prep for tomorrow's call with [prospect]", or shares meeting
  notes asking what they did wrong. For coaching calls, not writing scripts.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="sales-call-coach")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. Pay particular attention to the user's ICA definitions, historical win/loss patterns, and any prior coaching themes that surfaced in previous sessions.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Call material**: Share the call recording transcript, meeting notes, or describe the upcoming call scenario
- **Call type**: Discovery, demo, negotiation, closing, renewal, or expansion?
- **Coaching mode**: Post-call review (analysing what happened) or pre-call preparation (planning what should happen)?
- **Prospect profile**: Who was or will be on the call? (role, seniority, industry, deal stage, deal value)
- **Specific concern**: Is there a particular moment, objection, or dynamic they want focused attention on?

If the user provides partial information, infer reasonable defaults from FutureProof context and state assumptions explicitly.

## Step 3: Do the Work — Call Diagnostic Framework

Apply the **COMMAND Call Diagnostic™** — a seven-dimension framework for evaluating sales conversation effectiveness:

### 3.1 Control of Frame

- Who set the agenda? Was it stated explicitly in the first 60 seconds?
- Did the seller maintain conversational authority or cede it to the prospect?
- Were transitions between call phases (rapport → discovery → value → next steps) deliberate or accidental?

### 3.2 Opening Precision

- Did the opening 90 seconds establish credibility, state a relevant ICA-specific insight, and earn the right to ask questions?
- Was the prospect's time acknowledged and a mutual agenda proposed?
- Score the "pattern interrupt" — did anything differentiate this call from the dozens of other vendor calls the prospect takes?

### 3.3 Mastery of Discovery

- Were questions layered (situation → problem → implication → need-payoff) or flat and checklist-driven?
- Did the seller uncover the **three critical discovery elements**: explicit pain, quantified business impact, and compelling event/timeline?
- Was active listening demonstrated — paraphrasing, mirroring, and building on prospect statements rather than pivoting to pitch?
- Ratio analysis: calculate talk-time split (seller vs. prospect). Flag if seller exceeded 40% during discovery.

### 3.4 Mapping to Value

- Was the solution positioned in the prospect's language, mapping directly to the pain uncovered in discovery?
- Did the seller articulate a before/after transformation specific to the prospect's situation — not a generic capability walkthrough?
- Were proof points (case studies, metrics, named references) deployed at the moment of highest relevance?

### 3.5 Anticipation of Objections

- Were latent objections surfaced proactively ("Some clients at this stage typically wonder about…")?
- When objections arose, did the seller acknowledge → isolate → respond → confirm — or did they become defensive or dismissive?
- Catalogue each objection raised and grade the response: deflected, addressed superficially, or resolved with evidence.

### 3.6 Next-Step Commitment

- Was a specific, time-bound next step proposed (not "I'll send over some info")?
- Did the seller secure **mutual action commitments** — concrete deliverables from both sides before the next interaction?
- Was the next step proportionate to the deal stage and buying signal strength?

### 3.7 Delivery and Presence

- Assess pacing, tone modulation, and confidence markers in the language used
- Identify filler words, hedging language ("kind of," "maybe," "I think"), and authority-undermining phrases
- Evaluate responsiveness — did the seller adapt approach based on prospect energy and engagement cues?

Apply any user-specific `instructions` from FutureProof context (e.g., preferred sales methodology, industry norms, team benchmarks) to calibrate the diagnostic.

## Step 4: Deliver Output — Call Coaching Report

Produce a structured **Call Coaching Report** with the following sections:

### 4.1 COMMAND Scorecard

| Dimension | Score (1–10) | Benchmark Delta | Priority |
|---|---|---|---|
| Control of Frame | — | — | — |
| Opening Precision | — | — | — |
| Mastery of Discovery | — | — | — |
| Mapping to Value | — | — | — |
| Anticipation of Objections | — | — | — |
| Next-Step Commitment | — | — | — |
| Delivery and Presence | — | — | — |
| **Composite Score** | **—/70** | — | — |

Benchmark delta compares against the user's historical average from FutureProof `recent_sessions` where available.

### 4.2 Win/Loss Inflection Points

Identify the **three moments** in the call that had the greatest positive or negative impact on deal progression. For each:
- **Timestamp/section reference** in the transcript
- **What happened**: verbatim quote or paraphrase
- **Impact assessment**: how this moment shifted prospect engagement or deal trajectory
- **Alternative approach**: the exact words the seller should have used instead (scripted rewrite, not generic guidance)

### 4.3 Objection Playbook Update

For each objection encountered in the call:
- **Objection verbatim**
- **Seller response verbatim**
- **Effectiveness grade**: A (resolved), B (addressed, not resolved), C (deflected), F (mishandled)
- **Recommended response**: a fully scripted, ICA-calibrated response for future use

### 4.4 Pre-Call Planner (if coaching mode is preparation)

If the user requested pre-call coaching, replace sections 4.2 and 4.3 with:
- **Prospect intelligence brief**: synthesise known information into a one-page profile (role pressures, likely objections, decision criteria, competitive alternatives)
- **Call architecture**: minute-by-minute agenda with scripted opening, three discovery questions tailored to the prospect's situation, value bridge statements, and two closing options ranked by assertiveness
- **Contingency plays**: if-then responses for the three most probable objections based on ICA patterns in FutureProof context

### 4.5 Skill Development Focus

Identify the **single highest-leverage skill** the seller should practise before the next call. Provide:
- **Skill name and definition**
- **Current evidence of gap** (specific call moment)
- **Practice exercise**: a concrete drill (e.g., "Record yourself delivering discovery questions to a timer — aim for prospect talk-time above 60% in a 5-minute mock call")
- **Measurement criteria**: how to assess improvement

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
FutureProof:save_experiment(skill="sales-call-coach", experiment={
  hypothesis: "Replacing generic capability demos with prospect-specific pain-to-solution narratives in the first 3 minutes of demo calls increases prospect engagement and next-step conversion",
  variants: ["control: standard demo flow with feature walkthrough", "variant: pain-first narrative opening with tailored proof point before any product shown"],
  measurement: "Next-step commitment rate and prospect talk-time ratio across next 15 demo calls",
  expected_impact: "20% increase in demo-to-proposal conversion rate"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="sales-call-coach",
  query="Current high-performance sales call frameworks, discovery question architectures, and objection handling techniques for enterprise B2B sales cycles 2024–2025, with emphasis on multi-stakeholder buying committees",
  reason="Ensure coaching methodology reflects evolving buyer behaviour, remote selling dynamics, and competitive differentiation standards in the user's market"
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
FutureProof:save_session(skill="sales-call-coach", session={
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