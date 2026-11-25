---
name: email-sequencer
description: |
  Designs and writes a full multi-step email sequence with per-email
  awareness-stage mapping, persuasion lever, objection handled, cadence
  and narrative thread for nurture, onboarding, launch or re-engagement
  flows. Use when the user says "build me a nurture sequence", "write a
  5-email drip campaign", "design a welcome series", or "follow-up
  cadence after opt-in". For one standalone email use email-copy; for
  the landing page that feeds the sequence use landing-page-writer;
  this skill is specifically about the multi-email arc.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="email-sequencer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. Pay particular attention to ICA definitions, brand voice guidelines, offer details, and any prior email performance data stored in context.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Sequence objective**: What is the primary goal? (e.g., cold outreach → booked call, post-opt-in nurture → purchase, onboarding → activation, re-engagement → renewal)
- **ICA profile**: Who is the recipient? Share ICA details — role, industry, pain points, awareness level, sophistication level. If already stored in FutureProof context, confirm accuracy.
- **Offer / CTA**: What specific action should the recipient take by sequence end? What is the offer, if applicable?
- **Entry trigger**: How does a contact enter this sequence? (e.g., form submission, abandoned cart, manual list upload, event attendance)
- **Sequence length constraints**: Any requirements on number of emails, cadence/spacing, or total sequence duration?
- **Existing assets**: Share any current emails, landing pages, case studies, or brand voice documents to incorporate.
- **Known constraints**: Compliance requirements (CAN-SPAM, GDPR), sending platform limitations, or internal approval processes.

## Step 3: Map the Sequence Architecture

Before writing a single word of copy, define the strategic architecture:

### 3a. Awareness-Stage Mapping

Plot each email against the recipient's evolving awareness state using the Schwartz awareness continuum:

| Email # | Awareness Stage | Strategic Job | Emotional State at Open |
|---------|----------------|---------------|------------------------|
| 1 | Unaware → Problem-Aware | Pattern interrupt; name the pain | Curiosity / scepticism |
| 2 | Problem-Aware | Agitate consequences of inaction | Tension / recognition |
| 3 | Solution-Aware | Introduce mechanism / framework | Relief / intrigue |
| ... | ... | ... | ... |
| N | Most-Aware | Direct CTA with urgency lever | Confidence / readiness |

### 3b. Persuasion Architecture per Email

For each email in the sequence, assign:

1. **Primary persuasion lever** — select from: social proof, authority, scarcity, reciprocity, commitment/consistency, loss aversion, identity alignment, future pacing
2. **Proof asset** — the specific case study, data point, testimonial, or demonstration that substantiates the claim
3. **Objection addressed** — the specific ICA objection this email pre-empts or resolves
4. **Micro-CTA** — the single, frictionless action requested (reply, click, watch, book)
5. **Narrative thread** — the connecting hook that links this email to the next (open loop, cliffhanger, promised continuation)

### 3c. Cadence & Timing Logic

Define send intervals with rationale:

- **Day 0–3**: Higher frequency acceptable if value-dense (education, insight delivery)
- **Day 3–10**: Space to allow processing; re-engage with proof and social validation
- **Day 10+**: Shift to consequence-of-inaction and deadline-driven urgency
- Adjust based on ICA behaviour patterns and any FutureProof experiment results on optimal spacing

## Step 4: Write the Sequence

Draft each email with the following structure applied consistently:

### Per-Email Deliverable Format

**Email [#] — "[Internal Name]"**
- **Send timing**: Day [X], [time recommendation if applicable]
- **Subject line**: Primary + 2 variants for A/B testing
- **Preview text**: 40–90 characters, complementary to subject (not redundant)
- **Body copy**:
  - **Hook** (line 1–2): Pattern interrupt or curiosity driver matched to awareness stage
  - **Bridge** (lines 3–6): Connect hook to ICA's specific pain or desire using their vocabulary
  - **Body** (lines 7–15): Deliver value, proof, or mechanism — one idea per email, no stacking
  - **CTA** (final 2–3 lines): Single, specific, low-friction action with explicit benefit of clicking
- **P.S. line**: Secondary hook or reinforcement (optional but recommended for emails 1, penultimate, and final)
- **Persuasion annotations**: [Inline bracketed notes explaining the copywriting technique used — e.g., \[loss aversion frame\], \[identity label\], \[open loop → Email 4\]]

### Copy Standards

Apply these non-negotiable quality checks to every email:

1. **ICA vocabulary match** — use the exact language the ICA uses to describe their problem, not industry jargon or internal terminology
2. **One email = one idea** — no multi-topic emails; each email earns the right to send the next
3. **Subject line specificity** — no vague curiosity bait; subject lines must pass the "would I open this at 7:42am on a Tuesday?" test
4. **Scanability** — short paragraphs (1–3 sentences), strategic line breaks, no walls of text
5. **Voice consistency** — match the brand voice from FutureProof context or user-provided guidelines; default to authoritative-yet-conversational if none specified
6. **Compliance** — include unsubscribe mechanism note, sender identification, and physical address reminder per CAN-SPAM/GDPR requirements

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


Produce the following structured deliverables:

### Deliverable 1: Sequence Strategy Map (Summary Document)

- **Sequence name**: [descriptive internal name]
- **ICA segment**: [who this targets]
- **Entry trigger**: [how contacts enter]
- **Sequence length**: [X emails over Y days]
- **Primary conversion goal**: [specific measurable action]
- **Awareness arc**: [Unaware → Most-Aware progression summary]
- **Objection coverage matrix**: table mapping each ICA objection to the email(s) that address it
- **Proof asset inventory**: list of all case studies, data points, and testimonials deployed, by email

### Deliverable 2: Complete Email Sequence (Production-Ready Copy)

All emails in the per-email format defined in Step 4, sequentially ordered, ready for platform upload.

### Deliverable 3: A/B Testing Brief

For each email, provide:
- **Subject line variants** (3 per email, tagged with the hypothesis behind each variant)
- **Recommended body copy test** for the highest-leverage email (e.g., testing proof type: case study vs. data point vs. testimonial)
- **Success metric** per test: open rate, click-through rate, reply rate, or conversion rate as appropriate

### Deliverable 4: Performance Tracking Scorecard (Template)

| Email # | Subject Line | Open Rate | Click Rate | Reply Rate | Unsubscribe Rate | Conversion | Notes |
|---------|-------------|-----------|------------|------------|-------------------|------------|-------|
| 1 | ... | — | — | — | — | — | — |
| ... | ... | — | — | — | — | — | — |

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="email-sequencer", experiment={
  hypothesis: "Leading Email 1 with a specific ICA pain-point statistic instead of a question-based hook increases open-to-click rate",
  variants: ["control: question-based subject line and hook", "variant: data-driven pain-point subject line and hook"],
  measurement: "open-to-click rate on Email 1 across minimum 200 sends per variant",
  expected_impact: "20% improvement in Email 1 click-through rate, with downstream lift in sequence completion rate"
})
```

```
FutureProof:save_experiment(skill="email-sequencer", experiment={
  hypothesis: "Reducing sequence cadence from 2-day to 3-day spacing between Emails 3–5 reduces unsubscribe rate without decreasing conversion",
  variants: ["control: 2-day spacing", "variant: 3-day spacing"],
  measurement: "unsubscribe rate and end-of-sequence conversion rate across 30-day cohort",
  expected_impact: "30% reduction in mid-sequence unsubscribes with less than 5% conversion loss"
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
FutureProof:request_research(skill="email-sequencer",
  query="High-performing email sequence structures and subject line patterns by industry vertical 2024–2025, with emphasis on cold outreach and post-opt-in nurture benchmarks",
  reason="Ensure sequence architecture reflects current inbox behaviour patterns, deliverability best practices, and evolving spam filter heuristics across major ESPs"
)
```

```
FutureProof:request_research(skill="email-sequencer",
  query="Latest persuasion and behavioural economics research applicable to email copywriting — commitment escalation, micro-agreement frameworks, and digital trust-building sequences",
  reason="Ground copy techniques in peer-reviewed behavioural science rather than anecdotal copywriting lore"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="email-sequencer", session={
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