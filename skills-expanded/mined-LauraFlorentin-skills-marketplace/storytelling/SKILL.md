---
name: storytelling
description: >
  Master storytelling for business: consulting decks, executive presentations, PPT storyboarding,
  meeting narratives, and data-driven stories. Use this skill whenever the user wants to:
  structure or storyboard a presentation, build a consulting deck, craft a narrative for a business
  meeting or pitch, apply the Pyramid Principle / SCQA / SCR frameworks, write action-oriented slide
  titles, turn data into a compelling story, or communicate complex ideas clearly to executives.
  Also trigger when users say things like "help me structure my deck", "make this more compelling",
  "how do I present this to leadership", "I need a story for this data", "storyboard my slides",
  "write slide titles", "how do I tell this story", "narrative for my presentation", or "executive
  communication". This skill covers both the strategic architecture (frameworks) and the
  slide-by-slide craft (titles, charts, flow). Always use this skill before drafting any presentation
  outline, slide structure, or narrative strategy.
---

# Storytelling Skill

A comprehensive guide to business storytelling — from consulting deck architecture to slide-level craft.
Claude uses this skill when helping with presentations, pitch decks, executive narratives, data stories, or meeting communication strategy.

## When to use which reference file

| Situation | Go to |
|-----------|-------|
| Structuring a full deck from scratch | `references/frameworks.md` |
| Choosing the right framework (Pyramid, SCQA, Gap, SCR, Hero's Journey, Amazon memo) | `references/frameworks.md` |
| Writing or improving slide titles | `references/slide-craft.md` |
| Horizontal/vertical logic, ghost slides, layer-by-layer reveal | `references/slide-craft.md` |
| Turning data/analysis into a story | `references/data-storytelling.md` |
| Choosing tone/mode (executive vs. persuasive vs. board) | `references/audience-modes.md` |
| Using analogies to explain complex concepts | `references/audience-modes.md` |
| Executive presence, delivery, Q&A management | `references/audience-modes.md` |

---

## Core Philosophy

**"You think bottom-up. You present top-down."** — Barbara Minto

Business storytelling is not about being creative. It is about being *clear, credible, and actionable* for a time-constrained audience who wants your recommendation before your reasoning.

The three pillars of every great business story:

1. **Structure** — A logical skeleton so ideas build on each other
2. **Narrative** — Emotional and contextual thread that makes it memorable
3. **Evidence** — Data and proof points that earn trust

All three must work together. Visuals without narrative are noise. Data without structure is a dump. A narrative without evidence is speculation.

---

## The Core Frameworks (Quick Reference)

### 1. Pyramid Principle (Barbara Minto / McKinsey)
Lead with your answer. Support with 3–5 key arguments. Back each with evidence.

```
ANSWER / RECOMMENDATION
    ├── Key Argument 1
    │       └── Evidence / Data
    ├── Key Argument 2
    │       └── Evidence / Data
    └── Key Argument 3
            └── Evidence / Data
```

Use for: body of any consulting deck, written recommendations, individual slide logic.

---

### 2. SCQA (Situation–Complication–Question–Answer)
The narrative wrapper for the introduction / executive summary.

- **Situation**: Undisputed, shared context ("Our retail division holds 23% market share.")
- **Complication**: The disruption or tension ("But margin has eroded 8 pts in 18 months.")
- **Question**: The implicit "so what do we do?" ("How do we restore profitability?")
- **Answer**: Your headline recommendation ("We recommend exiting 3 underperforming regions and reinvesting in digital.")

Use for: exec summary slide, meeting openers, email subject lines + intros.

---

### 3. SCR (Situation–Complication–Resolution)
The Hollywood version of SCQA — cleaner, more narrative, ideal for full-deck storyboarding.

- **Situation** (short): Ground truth, shared context. 1–3 slides max.
- **Complication** (short): The problem, tension, or opportunity. 1–3 slides.
- **Resolution** (long): Your answer, structured via Pyramid Principle. Bulk of the deck.

Use for: full-deck architecture. SCR sets the spine; Pyramid Principle structures the resolution.

---

### 4. Data Story Arc (Brent Dykes)
For data-heavy presentations: hook → context → conflict → aha moment → call to action.

See `references/data-storytelling.md` for the full framework.

---

## The Golden Rules

1. **One slide, one idea.** Every slide should be able to stand alone with one clear message.
2. **Lead with the answer.** Executives want the punchline first. Save the build for reports.
3. **Action titles, not topic titles.** "Revenue declined 12%" > "Revenue Analysis."
4. **MECE your structure.** Arguments must be Mutually Exclusive, Collectively Exhaustive — no overlaps, no gaps.
5. **Data supports narrative, not the other way around.** Never paste a chart without a headline that tells the audience what to see.
6. **Contrast creates meaning.** "$10M" is a number. "20% above target" is a story.
7. **Anticipate the next question.** Each slide should answer the question raised by the slide before it.

---

## Quick-Start Workflow

When a user asks for help structuring a presentation or deck, follow this sequence:

### Step 1 — Diagnose
Ask (or infer from context):
- Who is the audience? (Executive / board / client / internal team)
- What is the desired outcome? (Decision / approval / alignment / awareness)
- What do you want them to do after? (The call to action)
- Is there a burning platform / tension to create urgency?

### Step 2 — Choose the macro structure
- Short pitch / meeting opener → **SCQA** intro + Pyramid body
- Full consulting deck → **SCR** spine + Pyramid resolution
- Data presentation → **Data Story Arc** (see reference)
- Persuasion under uncertainty → use **Hero's Journey** variant (see `references/audience-modes.md`)

### Step 3 — Draft the storyboard
List 6–10 "slide headlines" as complete sentences (not topics) that tell the story without opening the deck. If the headlines alone make a compelling argument, the deck will work.

Example storyboard (SCR structure):
```
1. [SITUATION] XYZ Bank faces its most competitive environment in a decade
2. [COMPLICATION] Digital-first challengers have captured 18% of new accounts in 24 months
3. [RESOLUTION HEADLINE] We recommend a three-part response to retake market position
4. [ARG 1] Modernize the core platform to reduce time-to-market from 9 months to 6 weeks
5. [ARG 2] Launch a digital-only sub-brand to compete in the challenger segment
6. [ARG 3] Reallocate $200M in marketing from mass to precision targeting
7. [CALL TO ACTION] We need leadership approval on all three tracks by end of Q2
```

### Step 4 — Apply Pyramid logic to each argument slide
Each key argument becomes a slide with:
- **Action title** (the claim)
- **3 supporting bullets** (the logic)
- **One visual or data point** (the proof)

### Step 5 — Pressure-test
Run the "so what?" test on every slide title. If the answer is "I don't know" — the title is a topic, not a message. Rewrite it.

---

## Reference Files

- `references/frameworks.md` — Deep dive on Pyramid, SCQA, SCR, MECE
- `references/slide-craft.md` — Action titles, one-idea-per-slide, chart selection, visual hierarchy
- `references/data-storytelling.md` — Data Story Arc, Brent Dykes framework, chart annotation
- `references/audience-modes.md` — Adapting tone and structure for executive / board / client / skeptic audiences
