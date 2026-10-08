---
description: Academic Research Graphify (ARG) — Cursor AI agent instructions for academic research, paper writing, peer review, and pipeline orchestration.
globs:
alwaysApply: true
---

# Academic Research Graphify (ARG)

You are operating in the ARG repository — a suite of AI skills for rigorous academic research.

## Skills & Modes

- **deep-research** (7 modes): full, quick, socratic, review, lit-review, fact-check, systematic-review
- **academic-paper** (10 modes): full, plan, outline-only, revision, revision-coach, abstract-only, lit-review, format-convert, citation-check, disclosure
- **academic-paper-reviewer** (6 modes): full, re-review, quick, methodology-focus, guided, calibration
- **academic-pipeline** (1 orchestrator): coordinates all above in a 10-stage workflow

## Slash Commands

| Command | Description |
|---------|-------------|
| `/arg-full` | Full pipeline: research → write → review → revise → finalize |
| `/arg-plan` | Socratic chapter-by-chapter planning |
| `/arg-outline` | Detailed outline + evidence map |
| `/arg-abstract` | Bilingual abstract (zh-TW + EN) + keywords |
| `/arg-revision` | Revised draft + R&R responses |
| `/arg-revision-coach` | Revision Roadmap + Response Letter skeleton |
| `/arg-lit-review` | Annotated bibliography in paper format |
| `/arg-format-convert` | Convert to LaTeX / DOCX / PDF / Markdown |
| `/arg-citation-check` | Citation error report |
| `/arg-disclosure` | Venue-specific AI-usage statement |

When any of these commands are mentioned by the user, read the corresponding skill's `SKILL.md` file and `MODE_REGISTRY.md` for full details, then execute accordingly.

## Routing Rules

1. Use `academic-pipeline` for end-to-end workflows; use individual skills for single tasks.
2. `deep-research` = upstream research engine; `academic-paper` = downstream publication engine.
3. When the user's research question is unclear, suggest socratic mode.
4. When the user wants to plan a paper, suggest plan mode.

## Key Rules

- All claims must have citations.
- Evidence hierarchy: meta-analyses > RCTs > cohort > case reports > expert opinion.
- Contradictions disclosed with evidence quality comparison.
- AI disclosure in all reports.
- Default output language matches user input.

## Key Files

- `MODE_REGISTRY.md` — all 25 modes
- `academic-pipeline/SKILL.md` — pipeline orchestrator
- `academic-paper/SKILL.md` — paper writing skill
- `deep-research/SKILL.md` — research skill
- `academic-paper-reviewer/SKILL.md` — review skill
- `agents/*.md` — plugin agent definitions
- `shared/handoff_schemas.md` — Material Passport handoff schema
