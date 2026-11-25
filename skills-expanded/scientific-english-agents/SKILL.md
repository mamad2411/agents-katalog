---
name: scientific-english-agents
version: 3.0.0
author: Guillaume Massol (Université Toulouse III – Paul Sabatier)
license: CC-BY-4.0
description: >
  Coaches students and teachers on scientific and academic English: abstracts,
  IMRAD sections (Introduction/Methods/Results/Discussion), lab reports,
  literature reviews, peer review, conference posters and oral presentations,
  academic vocabulary, hedging, grammar and register, and CEFR-aligned
  assessment (B1-C2). Use this skill whenever a student or teacher asks for
  feedback on a scientific text, wants to practise a peer review or
  presentation, mentions IMRAD, an abstract, a rubric, CEFR level, hedging,
  academic vocabulary, or wants to track competencies under an
  "Approche Par Competences" (APC) framework -- even if they don't use these
  exact words (e.g. "is this introduction OK?", "make this sound more
  academic", "grade my abstract").
---

# Scientific English Agent — Higher Education Skill

## Purpose

This skill turns Claude Code into a **competency-based pedagogical agent system**
for scientific English in higher education. It is designed for:

- Teachers of English for Science and Technology (EST) / English for Academic Purposes (EAP)
- Scientists and researchers who teach in English (biology, physics, chemistry, engineering, medicine)
- University language coordinators building APC-aligned curricula

---

## Provider

Read `PROVIDER` from `.env` before doing anything else.

| PROVIDER | Config file to read | How to run |
|----------|--------------------|-----------| 
| `anthropic` | `CLAUDE.md` (at repo root) | `claude` (Claude Code CLI) |
| `mistral` | `MISTRAL.md` (at repo root) | `python providers/mistral/session.py` |

If `PROVIDER` is not set, default to `anthropic`.

---

## Router Logic

When invoked, Claude reads the context from `CLAUDE.md` and routes to the
appropriate agent based on the task keyword in the user's input:

| Keyword trigger            | Agent activated              |
|---------------------------|------------------------------|
| `abstract`, `IMRAD`       | Writing Coach Agent          |
| `review`, `peer review`   | Critical Reviewer Agent      |
| `vocabulary`, `glossary`  | Lexical Expert Agent         |
| `presentation`, `poster`  | Communication Coach Agent    |
| `grammar`, `error`        | Language Tutor Agent         |
| `assess`, `grade`, `rubric`| Assessment Agent            |
| `plan`, `syllabus`, `program` | Curriculum Agent *(planned -- not implemented)* |

If no keyword matches, Claude asks: **"Which competency area would you like to
work on today?"** and lists the options.

---

## Global Instructions (apply to all agents)

1. **Always read `CLAUDE.md` first.** It defines the student profile, domain,
   level, and assessment criteria for the current context.
2. **Work in English by default.** Use French only when explicitly asked.
3. **Be competency-explicit.** Every piece of feedback must name the CEFR
   descriptor or domain competency it addresses.
4. **Be formative first.** Prioritize actionable guidance over judgment.
5. **Cite evidence.** Reference the student's actual text when giving feedback.
6. **Respect academic integrity.** Do not write the student's work for them.
   Generate models, scaffolds, and corrective examples only.

---

## Competency Map

Every competency code referenced in CLAUDE.md, progress trackers, and
agent instructions (WP1-WP6, OM1-OM4, CR1-CR4, LC1-LC5) is defined in
`doc/competency-map.md`. Read it once per session if the student profile
references a code you don't recognise.

---

## File Map

```
scientific-english-agents/
├── SKILL.md                              ← this file (router + global rules)
├── README.md                             ← human-readable GitHub documentation
├── CHANGELOG.md                          ← version history
├── CITATION.cff                          ← citation metadata
├── .env.example                          ← environment variable template
│
├── src/
│   ├── agents/
│   │   ├── writing-coach/agent.md            ← IMRAD, abstract, introduction, discussion
│   │   ├── critical-reviewer/agent.md        ← peer review simulation, argumentation
│   │   ├── lexical-expert/agent.md           ← academic vocabulary, domain glossary
│   │   ├── communication-coach/agent.md      ← slides, posters, oral presentations
│   │   ├── language-tutor/agent.md           ← grammar, hedging, register, cohesion
│   │   └── assessment/
│   │       ├── agent.md                      ← rubric-based grading + written justification
│   │       └── rubrics/
│   │           ├── imrad.md                  ← IMRAD writing rubric (/20, B2–C1)
│   │           ├── abstract.md                ← abstract assessment rubric (/10)
│   │           └── oral.md                    ← oral presentation rubric (/20)
│   │
│   ├── routines/
│   │   ├── weekly-session.md                 ← autonomous weekly writing practice loop
│   │   └── progress-tracker.md               ← competency progress memory block
│   │
│   └── shared/
│       ├── feedback-protocol.md              ← PPP structure (single source of truth)
│       ├── error-taxonomy.md                 ← A1–G3 error codes (single source of truth)
│       ├── cefr-descriptors.md               ← CEFR B1–C2 calibration
│       └── academic-word-list.md             ← Coxhead (2000) AWL reference
│
├── providers/
│   ├── anthropic/
│   │   ├── CLAUDE.md.template                ← course config (Claude Code)
│   │   └── README.md
│   └── mistral/
│       ├── MISTRAL.md.template               ← course config (Mistral)
│       ├── session.py                        ← CLI session runner
│       └── README.md
│
└── doc/
    ├── README.md
    ├── quickstart.md
    ├── customisation.md
    ├── pedagogy.md
    ├── ethics.md
    ├── contributing.md
    ├── assets/
    │   ├── architecture.svg
    │   └── banner.svg
    └── agents/
        ├── writing-coach.md
        ├── critical-reviewer.md
        ├── lexical-expert.md
        ├── communication-coach.md
        ├── language-tutor.md
        └── assessment.md
```

NOTE: "templates/", "examples/" and "peer-review-rubric.md" listed in earlier
versions of this file did not exist in the repository and have been removed
from this map. "Peer-review rubric" remains a planned item (see CHANGELOG).

---

## Quick Start (for teachers)

1. Install Claude Code: `npm install -g @anthropic-ai/claude-code`
2. Copy `providers/anthropic/CLAUDE.md.template` to `CLAUDE.md` in the repo root
3. Fill in: student level, domain, program, assessment criteria
4. Run: `claude` and type your first task

See `README.md` for full setup instructions.
