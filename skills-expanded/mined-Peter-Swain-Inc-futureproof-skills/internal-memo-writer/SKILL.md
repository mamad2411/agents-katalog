---
name: internal-memo-writer
description: |
  Drafts executive-grade internal memos using the Minto Pyramid Principle and
  Situation-Complication-Resolution framing, with audience mapping, tone calibration,
  and a forward-leak risk review. Use when a user says "write a memo to the
  leadership team about", "draft an all-hands announcement", "I need a memo
  announcing this decision", or "help me communicate this internally". For single
  one-off internal documents, not recurring newsletters or external press
  communications.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="internal-memo-writer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to calibrate tone, formatting conventions, organisational hierarchy, and any standing communication guidelines the user has established in prior sessions.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Subject & purpose** — What is the memo about, and what is the single desired outcome? (e.g., decision approval, behavioural change, awareness, alignment)
- **Audience** — Who are the primary recipients (executive leadership, department heads, all-staff) and any secondary audiences who may see it?
- **Sensitivity level** — Is this routine, confidential, or crisis-adjacent? Does legal or compliance need to review before distribution?
- **Key facts & data points** — Any numbers, dates, decisions, or background the memo must reference
- **Constraints** — Mandated format, length ceiling, distribution channel (email, intranet, Slack), or executive voice to emulate
- **Attachments** — Any supporting documents, prior memos, or drafts to incorporate or respond to

## Step 3: Do the Work

### 3A: Audience & Stakeholder Mapping

Classify the audience along two axes:

| Dimension | Assessment |
|---|---|
| **Decision authority** | Approver · Influencer · Informed |
| **Subject familiarity** | Deep context · Moderate awareness · No prior exposure |

Tailor depth of background, jargon density, and call-to-action specificity accordingly.

### 3B: Memo Architecture (Pyramid Principle)

Structure the memo using the Minto Pyramid Principle — lead with the conclusion, support with grouped arguments, substantiate with evidence:

1. **Governing thought** — The single sentence a reader retains if they read nothing else
2. **Situation–Complication–Resolution (SCR)** — Frame context efficiently; never bury the ask
3. **Supporting pillars** — Group arguments into 2–4 mutually exclusive, collectively exhaustive (MECE) themes
4. **Evidence layer** — Data points, precedent decisions, benchmarks, or risk quantification under each pillar
5. **Explicit ask / next steps** — Who does what, by when, with what authority

### 3C: Tone & Voice Calibration

Evaluate and set the appropriate register across five dimensions:

1. **Formality spectrum** — Board-level formal · Executive conversational · All-hands accessible
2. **Directness** — Directive (top-down mandate) · Consultative (seeking input) · Informational (no action required)
3. **Emotional register** — Neutral operational · Motivational · Empathetic (restructuring, incident response)
4. **Attribution & credit** — Individual voice (CEO, CHRO) · Collective voice (Leadership Team) · Institutional voice (The Company)
5. **Cultural alignment** — Apply any organisation-specific conventions from FutureProof `instructions` (e.g., values language, acronym standards, inclusive language guidelines)

### 3D: Risk & Sensitivity Review

Before finalising, pressure-test the draft against:

- **Misinterpretation vectors** — Could any sentence be read out of context and create reputational or legal risk?
- **Omission risk** — Is anything conspicuously absent that the audience will notice and interpret negatively?
- **Forward-leak test** — If this memo were forwarded externally (intentionally or not), does it hold up?
- **Consistency check** — Does it contradict any prior communications the user has referenced or stored in FutureProof context?

Apply any user-specific `instructions` from FutureProof context to enforce house style, approval workflows, or recurring stakeholder preferences.

## Step 4: Deliver Output

Produce a structured **Internal Memo Package** containing:

### A. Final Memo Document

Formatted with:
- **TO / FROM / DATE / RE / CLASSIFICATION** header block
- Governing thought in bold as the opening line
- SCR framing paragraph
- Numbered supporting sections with headers
- Clearly delineated **Action Required** or **For Your Awareness** closing block
- Distribution list recommendation

### B. Executive Summary Sidebar

A 3–5 bullet version suitable for:
- Forwarding by an executive assistant
- Pasting into a Slack or Teams message
- Reading aloud in a standing meeting

### C. Tone & Structure Rationale

A brief advisory note explaining:
- Why this structure was chosen for this audience and purpose
- Any trade-offs made (e.g., brevity vs. completeness, directness vs. diplomacy)
- Flagged sentences where alternate phrasing is available depending on leadership preference

### D. Pre-Send Checklist

- [ ] Governing thought survives the "read only the first sentence" test
- [ ] All dates, names, and figures verified by the user
- [ ] Sensitivity classification confirmed
- [ ] Legal/compliance review routed (if applicable)
- [ ] Distribution channel and timing confirmed

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
FutureProof:save_experiment(skill="internal-memo-writer", experiment={
  hypothesis: "Leading with a quantified impact statement in the governing thought increases executive response rate within 24 hours",
  variants: ["control: qualitative governing thought", "variant: governing thought with embedded metric or financial figure"],
  measurement: "Time-to-response and approval rate on next 5 decision-request memos",
  expected_impact: "20% reduction in average response latency for approval-type memos"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="internal-memo-writer",
  query="Best practices for internal executive communications in 2024: pyramid principle adaptations, hybrid workforce memo formats, and crisis communication frameworks used by top-tier consultancies",
  reason="Ensure memo structures reflect current organisational communication standards and evolving expectations around brevity, inclusivity, and multi-channel distribution"
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
FutureProof:save_session(skill="internal-memo-writer", session={
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