---
name: deck-builder
description: >
  End-to-end consulting deck builder that combines strategic storytelling, structured narrative
  frameworks, and branded PPTX generation into one seamless workflow. Use this skill whenever
  the user wants to build, storyboard, write, or generate a presentation or slide deck from
  scratch — especially for consulting deliverables, client pitches, executive briefings, strategy
  decks, board presentations, or AI/transformation proposals. Also trigger when user says things
  like "build me a deck", "create slides for", "make a presentation about", "I need a PPTX",
  "help me structure a pitch", "create a consulting deck", "generate slides with my branding",
  "storyboard this presentation", or "turn this into a deck". This skill orchestrates the full
  pipeline: topic → narrative framework → storyboard → slide content → branded PPTX output.
  Always use this skill in place of the standalone storytelling, pptx, or brand-studio skills
  when the goal is a complete, ready-to-present deck.
---

# Deck Builder — Combined Plugin

Orchestrates three skills into one end-to-end pipeline:

```
STORYTELLING SKILL          BRAND-STUDIO SKILL         PPTX SKILL
(narrative + structure)  +  (colors, fonts, logo)   →  (branded .pptx output)
```

---

## The 4-Stage Pipeline

### Stage 1 — Diagnose & Choose Framework
### Stage 2 — Storyboard (slide titles only)
### Stage 3 — Write Slide Content
### Stage 4 — Generate Branded PPTX

Use all four stages, but reuse context and approved content the user already supplied. Pause for storyboard approval only when the narrative direction is materially uncertain or the user asks for a review checkpoint.

---

## Stage 1 — Diagnose & Choose Framework

Before writing a single word, answer these questions (infer from context, or ask if unclear):

| Question | Why it matters |
|----------|---------------|
| What is this deck for? | Determines framework and tone |
| Who is the audience? | Determines depth, language, format |
| What decision/action should result? | Defines the governing thought |
| What do they already know? | Sets starting point of the story |
| Is there urgency / a burning platform? | Informs the Complication section |
| How many slides? | Sets scope before writing begins |

**Then select the narrative framework:**

| Situation | Framework |
|-----------|-----------|
| Executive briefing, strategy update | Pyramid Principle + SCQA intro |
| Full consulting engagement deck | SCR + Pyramid for Resolution |
| Audience doesn't feel the problem yet | Gap ("What Is / What Could Be") |
| Change management / transformation | Hero's Journey |
| Data-heavy presentation to leadership | Data Story Arc |
| Board presentation | SCQA intro + Pyramid, max 10 slides |

→ Read `references/frameworks-cheatsheet.md` for framework quick-reference if needed.

---

## Stage 2 — Storyboard

Generate the deck spine as **action titles only** — complete sentence claims, not topics.

Output format:
```
DECK TITLE: [working title]
FRAMEWORK: [chosen framework]
AUDIENCE: [who]
GOVERNING THOUGHT: [one sentence — the answer/recommendation]
ARGUMENT ORDERING MODE: [structural / chronological / comparative / deductive / inductive]

SLIDE STORYBOARD:
1. [TITLE SLIDE] — [Deck title + subtitle]                              📝
2. [EXEC SUMMARY] — [Situation | Complication | Recommendation | 3 key supports | Ask]  📝
3. [SITUATION] — [Action title: undisputed context]                     📝
4. [COMPLICATION] — [Action title: the tension/problem]                 📊
5. [QUESTION] — [Action title: reframe the problem as a focused challenge]  📝
6. [RESOLUTION HEADLINE] — [Action title: your recommendation]          📝
7. [ARG 1] — [Action title: first supporting argument]                  🔢
8. [ARG 2] — [Action title: second supporting argument]                 📊
9. [ARG 3] — [Action title: third supporting argument]                  📝
10. [CALL TO ACTION] — [Action title: what you need from the audience]  📝
11. [APPENDIX MARKER] — Backup slides start here
```

> Note on the Question slide: In full SCQA decks, the Question earns its own slide — it reframes the complication as a focused challenge that *invites exploration rather than reaction*. For compressed decks (board, exec briefings), Question can be implicit. For client engagement decks, make it explicit.

**Ladder-up check:** Read the storyboard as a hierarchy:
```
GOVERNING THOUGHT
    ├── Arg 1 title (does it support the governing thought?)
    ├── Arg 2 title (does it support the governing thought?)
    └── Arg 3 title (does it support the governing thought?)
```
Every argument title must be a direct logical pillar under the governing thought. If you can't see the connection, the argument is off-pyramid.

**Storyboard quality check — run before proceeding:**
- Read only the action titles aloud in sequence. Do they tell the full story?
- Does every title pass the "so what?" test? (Complete sentence + specific implication)
- Is the governing thought stated by slide 5 at the latest?
- Are the arguments MECE? (No overlap, no gaps)

Present the storyboard for approval when changing direction later would waste substantial work. If the user asked for an end-to-end build and the brief is clear, continue while making the storyboard visible in the final deliverable or handoff.

---

## Stage 3 — Write Slide Content

For each slide in the approved storyboard, generate:

```
SLIDE N: [Action Title]
TYPE: [argument / data / transition / title / exec-summary]
LAYOUT SUGGESTION: [two-column / stat callout / bullets / chart / quote]

BODY:
• [Bullet 1 — specific insight with data if available]
• [Bullet 2 — specific insight with data if available]
• [Bullet 3 — specific insight with data if available]

VISUAL SUGGESTION: [chart type / icon / data callout / image concept]
CHART DATA (if applicable): [labels and values]

SPEAKER NOTES:
[2–4 sentences: what to say, what to emphasize, what question this slide answers]
```

**Content rules (from storytelling skill):**
- One idea per slide. One title claim. 3 bullets max in most cases.
- Bullets are specific insights with data, not topic labels.
- Every chart needs an action title (not a metric label).
- The "so what?" of every data point must be stated in the title or annotation.

→ See `references/slide-content-rules.md` for full guidance.

---

## Stage 4 — Generate Branded PPTX

### Step 4a — Load Brand Config
Read the project brand at `${CLAUDE_PROJECT_DIR}/.brand-studio/brand-config.md`, falling back to the personal default at `${CLAUDE_PLUGIN_DATA}/brand-config.md`.

- **If configured:** extract Primary color, Secondary color, Accent color, Heading Font, Body Font, logo path, brand name. Use these throughout.
- **If NOT configured:** use a bundled palette from `references/default-palettes.md` unless brand choice is decision-critical, in which case ask for direction.

### Step 4b — Generate PPTX
Use the host's available presentation-creation capability and follow its required rendering and verification workflow. Do not assume a fixed filesystem path for another skill.

**Slide layout assignments:**
| Slide type | Layout to use |
|-----------|--------------|
| Title slide | Full-bleed Primary color bg, white text, logo centered |
| Executive summary | Two-column or structured summary box layout |
| Situation / Complication | Clean content slide, accent color left bar |
| Argument slide | Two-column: text left, visual/stat right |
| Data/chart slide | Full chart with annotated action title above |
| Call to action | Dark bg (Primary), bold centered text, clear ask |
| Appendix | Light bg, smaller font, labeled A1/A2/A3 |

**Brand application checklist:**
- [ ] All slide backgrounds use brand Background color
- [ ] All slide titles use brand Primary color + Heading Font
- [ ] All body text uses brand Body Font
- [ ] Accent shapes/dividers use brand Secondary or Accent color
- [ ] Callout boxes use Primary color background, white text
- [ ] Charts cycle: Primary → Secondary → Accent colors
- [ ] Logo placed on title slide and optionally on all slides (bottom-right, small)
- [ ] No `#` prefix on any hex color (PptxGenJS requirement)

### Step 4c — QA
Render the deck with the host presentation tooling and visually inspect every slide for text overflow, overlap, clipping, low contrast, chart legibility, and placeholder content. Fix issues and re-render before delivery.

### Step 4d — Deliver
- Save as `[BrandName]_[DeckTitle]_[YYYY-MM-DD].pptx`
- Save it in the workspace or artifact location provided by the host environment.
- Report the final filename and any unresolved content or rendering limitations.

---

## Reference Files

| File | When to read |
|------|-------------|
| `references/frameworks-cheatsheet.md` | Stage 1 — framework selection detail |
| `references/slide-content-rules.md` | Stage 3 — slide writing rules and templates |
| `references/default-palettes.md` | Stage 4 — if brand not configured |

---

## Quick Mode (Power User)

If the user provides full context upfront, compress stages 1–3 and proceed directly to generation unless the user requested an approval checkpoint.
