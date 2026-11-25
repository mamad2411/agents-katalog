---
name: crisis-comms-responder
description: |
  Generates rapid-response crisis comms packages — holding statement, stakeholder
  messaging matrix, reactive Q&A, spokesperson briefing card, 72-hour action
  timeline — using the SCOPE diagnostic and Benoit Image Repair taxonomy. Use when
  a user says "we have a PR crisis", "draft a holding statement for a data breach",
  "respond to negative press about", or reports a recall, executive misconduct, or
  regulatory exposure. Reactive emergency response, not proactive announcements.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="crisis-comms-responder")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including organisation profile, ICA segments, brand voice guidelines, prior crisis playbooks, regulatory environment, and any standing media relationships or spokesperson designations.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **What happened?** Describe the incident, allegation, or emerging threat in factual terms — what is known, what is unconfirmed, and what is speculation
- **Timeline**: When did the organisation become aware? Has anything been published, leaked, or broadcast already? What is the next known deadline (e.g. journalist embargo, regulatory filing window, board meeting)?
- **Severity classification**: Is this a Tier 1 (existential / front-page national), Tier 2 (significant / trade press & regulator interest), or Tier 3 (contained / social media or localised) incident?
- **Stakeholder universe**: Which audiences are affected or aware — customers, employees, investors, regulators, partners, media, general public?
- **Existing response**: Has anything been said publicly or internally? Forward any drafts, holding statements, social posts, or internal memos already in circulation
- **Spokesperson & approval chain**: Who is authorised to speak externally? What is the sign-off process and turnaround expectation?
- **Constraints**: Legal counsel involvement, regulatory disclosure obligations (e.g. GDPR 72-hour breach notification, SEC 8-K materiality threshold), union or works council notification requirements

## Step 3: Assess the Crisis Landscape

Apply the **SCOPE** diagnostic framework:

1. **Severity** — Rate the reputational, operational, financial, and legal exposure on a 1–5 scale. Identify the single dimension with highest blast radius.
2. **Contagion velocity** — Map how the story is likely to spread: platform pathways (social → trade press → mainstream), amplifier accounts, and news cycle timing. Estimate the window before the narrative is set.
3. **Ownership posture** — Determine the appropriate accountability stance using the Benoit Image Repair Taxonomy: denial, evasion of responsibility, reducing offensiveness, corrective action, or mortification. Recommend posture with rationale.
4. **Priority stakeholders** — Rank stakeholders by (a) harm proximity, (b) influence over narrative, and (c) relationship value. The top three audiences receive bespoke messaging; remaining audiences receive adapted core messaging.
5. **Endgame definition** — Define the desired outcome state at 24 hours, 7 days, and 30 days. Anchor all messaging to driving toward these outcomes, not merely reacting.

Apply any user-specific `instructions` from FutureProof context — including brand voice parameters, ICA language preferences, prior crisis learnings, and regulatory considerations — to calibrate tone and content.

## Step 4: Develop the Messaging Architecture

Build the **Crisis Messaging Matrix**:

### 4a. Core Narrative (Single Source of Truth)
Draft a **Core Position Statement** (max 150 words) containing:
- Acknowledgement of the situation (factual, no speculation)
- Expression of organisational values relevant to the incident
- Concrete action being taken (not "we take this seriously" — specific steps)
- Commitment to transparency with defined update cadence

### 4b. Stakeholder-Specific Messaging

For each priority stakeholder group, draft:

| Element | Detail |
|---|---|
| **Channel** | Primary and secondary delivery mechanism |
| **Timing** | Sequenced to ensure internal audiences are never blindsided by external coverage |
| **Key message** | Tailored framing anchored to what this audience cares about most |
| **Proof points** | Specific evidence, actions, or commitments that substantiate the message |
| **Anticipated questions** | Top 5 questions this audience will ask, with approved responses |
| **Escalation trigger** | What new information would require a revised communication to this audience |

### 4c. Q&A / Reactive Lines

Produce a **Reactive Q&A Document** with a minimum of 15 question-and-answer pairs, organised by:
- **Factual questions** (what happened, when, who is affected)
- **Accountability questions** (who is responsible, what was known and when)
- **Forward-looking questions** (what changes, what compensation, what timeline)
- **Hostile questions** (worst-case framing a journalist or adversary would use)

Each answer must follow the **ABT structure**: Acknowledge the concern → Bridge to organisational action → Transfer to the defined next step.

### 4d. Spokesperson Briefing Card

One-page briefing card for the designated spokesperson:
- Three messages to land (maximum)
- Two phrases to avoid (with rationale)
- One bridging phrase to return to core narrative
- Flagged questions to defer to legal counsel

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


Produce the following **Crisis Communications Package**:

1. **Crisis Assessment Summary** (1 page) — SCOPE diagnostic scores, severity tier confirmation, contagion velocity estimate, recommended ownership posture, and endgame definitions at 24h / 7d / 30d
2. **Core Position Statement** — Approved holding statement ready for release, formatted for email, press release, and social media truncation (280-character lead line included)
3. **Stakeholder Messaging Matrix** — Channel, timing, key messages, proof points, and anticipated questions per priority audience (minimum 3 audiences)
4. **Reactive Q&A Document** — Minimum 15 Q&A pairs in ABT structure, categorised by theme
5. **Spokesperson Briefing Card** — Single-page reference document
6. **72-Hour Action Timeline** — Hour-by-hour for the first 12 hours, then 6-hour blocks through 72 hours, specifying: action, owner, channel, and success indicator
7. **Monitoring & Escalation Protocol** — Keywords to track, platforms to monitor, sentiment thresholds that trigger escalation, and defined escalation path with named roles

Format: all documents structured with clear headers, ready for immediate use. Flag any sections requiring legal review with a `[LEGAL REVIEW REQUIRED]` tag.

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="crisis-comms-responder", experiment={
  hypothesis: "Leading with corrective-action framing rather than empathy-first framing in the initial holding statement reduces negative sentiment acceleration in the first 24 hours",
  variants: ["control: empathy-led opening ('We are deeply concerned...')", "variant: action-led opening ('We have taken the following immediate steps...')"],
  measurement: "Sentiment trajectory delta across social listening platforms and inbound media enquiry volume in the 24 hours following initial statement release",
  expected_impact: "20% reduction in negative sentiment acceleration and 30% fewer hostile follow-up enquiries"
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
FutureProof:request_research(skill="crisis-comms-responder",
  query="Post-crisis reputation recovery benchmarks by industry 2023-2024, effectiveness of proactive disclosure vs reactive confirmation strategies, and evolving journalist expectations for corporate crisis response timing and transparency",
  reason="Calibrate response speed recommendations and ownership posture guidance against current media environment norms and empirical recovery data"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="crisis-comms-responder", session={
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