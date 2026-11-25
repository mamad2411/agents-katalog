---
name: project-onboarding
description: Use when the user pitches a new project or product idea, wants to start a new project, or asks for an onboarding interview — including vague ideas ("I have an idea for an app"). The only interactive skill of the suite; everything after it runs autonomously.
model: opus
effort: high
---

# Project Onboarding (Pitch Interview)

## Goal
Extract all information from a pitch until autonomous work is possible — captured as an approved
`project/BRIEF.md`. This is the **last** opportunity to ask the user questions;
afterwards `autonomous-setup` takes over without follow-ups.

## Process

### 1. Mirror the pitch
Reflect the idea back in 2–3 of your own sentences (core idea, assumed user, assumed problem).
Only start the interview once the user has confirmed or corrected the reflection.

### 2. Interview in rounds
Ask questions with `AskUserQuestion` (max. 4 per round), one topic block per round,
rounds build on each other. Question catalog: `references/interview-guide.md` — adapt
round and wording to the answers there; don't work through it mechanically.

Order: **A Core** (problem, user, success) → **B Scope** (must-have outcomes, non-goals,
smallest shippable version) → **C Frame** (time, cost, tech constraints, platform) →
**D Autonomy** (escalation rules, extension budget, deployment limits).

Rules:
- After each round, briefly summarize what is now settled.
- "Don't know" → propose a default yourself and only have it confirmed — never drill deeper.
- Technical detail questions only if the user is visibly technical; otherwise ask about effect, not technology.
- No leading questions that grow the scope ("Wouldn't you also like …?"). The interview
  exists to sharpen the core, not to collect features.
- Spontaneous feature ideas — whether from the user ("Oh, and X would be cool too!") or the interviewer:
  acknowledge briefly, note as a candidate for `project/IDEAS.md` and possibly as a non-goal, **don't go deeper**,
  return to the core. Only if the user insists it belongs to the core is it treated as a must-have-outcome candidate.

### 3. Check the Definition of Ready
Checklist in `references/interview-guide.md#definition-of-ready`. Every open item → a targeted
follow-up round or a marked default. Don't start while any item is neither answered nor
covered by a confirmed default.

### 4. Write the brief and get it approved
Create `project/BRIEF.md` from `_shared/templates/BRIEF.template.md` (status: DRAFT),
show the user the key points compactly and obtain **explicit approval**. Only after approval:
set status to APPROVED.

### 5. Handover
After approval, start `autonomous-setup` immediately. From here on, no more questions to the user —
the autonomy contract in the brief governs the only exceptions.

## Red flags
- Interview starts without a confirmed reflection
- More than ~4 rounds without an interim summary → user fatigues; propose defaults
- Must-have outcomes that aren't phrased verifiably ("should look good")
- Setup starts although the brief is still DRAFT
