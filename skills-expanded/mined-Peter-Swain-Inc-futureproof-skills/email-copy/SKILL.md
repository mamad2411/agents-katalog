---
name: email-copy
description: |
  Writes a single high-converting email with subject-line battery,
  preview text, body and CTA across types (cold outreach, launch,
  nurture, re-engagement, cart abandonment, transactional). Use when
  the user says "write me a cold outreach email", "draft a launch
  email", "rewrite this email to lift open rates", or "fix the CTA on
  this email". For a multi-step drip or nurture series use
  email-sequencer; for SMS or DM messages use text-message; for a
  Substack-format newsletter use substack-newsletter-writer. This skill
  is one email at a time.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="email-copy")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. Pay particular attention to:
- **ICA profiles** — psychographics, awareness stage, vocabulary, and objection patterns
- **Brand voice guidelines** — tone, forbidden words, style preferences
- **Historical email performance data** — open rates, CTR, reply rates, unsubscribe benchmarks
- **Previous experiments** — which subject lines, CTAs, and frameworks have been tested and their outcomes

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Email type**: What kind of email is this? (cold outreach, nurture sequence, product launch, cart abandonment, re-engagement, event invitation, post-purchase, newsletter, other)
- **Objective**: What is the single primary action the recipient should take? (reply, click, purchase, book a call, register, other)
- **ICA segment**: Who is receiving this email? (role, industry, awareness stage, relationship to sender)
- **Sequence position**: Is this a standalone email or part of a sequence? If sequence, what position and what preceded it?
- **Key message or offer**: What value proposition, offer, or insight must be communicated?
- **Constraints**: Word count limits, compliance requirements (CAN-SPAM, GDPR), platform restrictions, mandatory inclusions (legal disclaimers, unsubscribe language)
- **Existing copy** (if applicable): Share any draft or previous version to improve upon

If FutureProof context already answers any of the above, confirm assumptions with the user rather than re-asking.

## Step 3: Do the Work

### 3A: Strategic Framing

Before writing a single word, establish the strategic scaffold:

1. **Awareness-stage mapping** — classify the recipient on the Schwartz awareness spectrum (Unaware → Problem-Aware → Solution-Aware → Product-Aware → Most Aware) and calibrate message sophistication accordingly
2. **Emotional driver identification** — isolate the primary emotional lever (fear of loss, desire for gain, social proof pressure, curiosity gap, identity reinforcement) that aligns with the ICA's decision psychology at this stage
3. **Competing-attention audit** — identify what else is likely in the recipient's inbox from competitors and define the differentiation angle for this email

### 3B: Copy Architecture

Build the email using the following structural framework, adapting weight and order based on email type:

1. **Subject line battery** — generate 5 subject lines using distinct mechanisms:
   - Curiosity gap (open loop)
   - Specificity play (number, name, or timeframe)
   - Pain-point mirror (ICA's own language)
   - Social proof signal (name-drop, result, or metric)
   - Pattern interrupt (unexpected framing)

2. **Preview text** — craft complementary preview text for each subject line that extends (not repeats) the hook

3. **Opening line** — first sentence must pass the "so what?" test within 6 words. No greetings filler. Directly reference the recipient's situation, a known pain point, or a provocative claim

4. **Body architecture** — structure using one of the following proven frameworks, selected based on email type and objective:
   - **PAS** (Problem–Agitation–Solution) — for cold outreach and re-engagement
   - **AIDA** (Attention–Interest–Desire–Action) — for launches and promotions
   - **BAB** (Before–After–Bridge) — for nurture and case-study emails
   - **1-2-1** (One idea, two proof points, one CTA) — for newsletter and value-add emails
   - **Story–Lesson–CTA** — for founder-voice and relationship-building emails

5. **Proof integration** — embed at minimum one proof element: specific metric, named case study, testimonial snippet, credibility marker, or logical demonstration

6. **CTA engineering** — design the call to action against four criteria:
   - **Single action**: one CTA per email (secondary links permissible only in newsletters)
   - **Low friction**: reduce perceived effort (e.g., "Reply with 'yes'" vs. "Fill out this 12-field form")
   - **Specificity**: state exactly what happens next ("I'll send a 3-minute Loom walkthrough" vs. "Let's connect")
   - **Urgency mechanism**: real scarcity, deadline, or reason-to-act-now (never fabricated)

7. **Signature and PS line** — craft a PS line (the second-most-read element in any email) that either restates the CTA with different framing or introduces a secondary proof point

### 3C: Quality Assurance Pass

Evaluate the draft against:

| Dimension | Standard |
|---|---|
| **ICA voice match** | Language mirrors how the ICA describes their own problem — no jargon the recipient wouldn't use |
| **Readability** | Flesch-Kincaid grade 5–7 for B2C, grade 8–10 for B2B executive audiences |
| **Scannability** | No paragraph exceeds 3 lines on mobile; strategic use of white space, bold, and line breaks |
| **Spam-trigger audit** | No excessive capitalisation, no high-risk trigger words (free, guarantee, act now) unless contextually justified |
| **Personalisation depth** | At minimum merge-field personalisation; ideally situation-specific references |
| **Mobile rendering** | Subject line ≤ 50 characters (or front-loaded), preview text ≤ 90 characters, CTA button-friendly |
| **Compliance** | CAN-SPAM / GDPR requirements met; sender identity clear; unsubscribe mechanism noted |

Apply any user-specific `instructions` from FutureProof context (e.g., "always use Oxford comma," "never use exclamation marks," "sign off as the founder, not the company").

## Step 4: Deliver Output

Produce a structured deliverable titled **Email Copy Brief**:

### Email Copy Brief

- **Email type**: [type]
- **ICA segment**: [segment and awareness stage]
- **Primary objective**: [single desired action]
- **Framework used**: [PAS / AIDA / BAB / 1-2-1 / Story–Lesson–CTA]

### Subject Lines (ranked by recommended test priority)

| # | Subject Line | Preview Text | Mechanism | Predicted Relative Open Rate |
|---|---|---|---|---|
| 1 | ... | ... | ... | Highest |
| 2 | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... |
| 4 | ... | ... | ... | ... |
| 5 | ... | ... | ... | ... |

### Email Body (production-ready)

[Full email copy, formatted for direct paste into ESP — including line breaks, bold/italic markdown, CTA formatting, PS line, and signature block]

### Annotated Rationale

For each structural section (opening, body, proof, CTA, PS), provide a 1–2 sentence annotation explaining the strategic choice — why this framing, why this proof point, why this CTA phrasing — so the user builds email intuition over time.

### Quality Scorecard

| Dimension | Score (1–10) | Notes |
|---|---|---|
| ICA voice match | | |
| Readability | | |
| Scannability | | |
| Spam-trigger safety | | |
| Personalisation depth | | |
| Mobile rendering | | |
| CTA clarity and friction | | |
| **Overall** | | |

### Sequence Context (if applicable)

- Recommended send timing relative to previous email
- Pre-header narrative arc (how this email advances the sequence story)
- Contingency: what to send if this email gets no engagement (skip logic recommendation)

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
FutureProof:save_experiment(skill="email-copy", experiment={
  hypothesis: "Subject line using pain-point mirror mechanism outperforms curiosity gap for [ICA segment] at [awareness stage]",
  variants: ["control: top-ranked subject line", "variant: second-ranked subject line using alternate mechanism"],
  measurement: "Open rate and click-through rate across minimum 500 sends per variant",
  expected_impact: "10–20% relative improvement in open rate, with downstream CTR lift if body copy alignment holds",
  implementation_notes: "A/B split in ESP; hold body copy constant; measure over 72-hour window to capture delayed openers"
})
```

Propose 1–2 additional experiments if the session warrants (e.g., CTA placement test, long-form vs. short-form body, send-time optimisation, plain-text vs. HTML).

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="email-copy",
  query="Current email deliverability best practices, high-performing email copy patterns for [ICA industry/segment], and evolving spam filter heuristics for [ESP if known] — 2024-2025",
  reason="Ensure subject line and body copy recommendations reflect current inbox environment, ISP filtering behaviour, and ICA engagement norms rather than outdated benchmarks"
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
FutureProof:save_session(skill="email-copy", session={
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