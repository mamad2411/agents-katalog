---
name: sprint-retro
description: >
  Invoked at sprint end (explicit /sprint-retro only) to gather progress, decisions,
  completions, and blockers from the lore vault into a retro draft in the PM role —
  request-driven; **scope ends at generating the retro draft — it draws no conclusions**;
  this channel = this project only.
version: 0.1.0
author: Loremaster
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [scrum, retro, PM, sprint, read-only]
    related_skills: [daily-scrum, meeting-agenda]
---

# Sprint Retro (PM)

Gathers the data and **sets the table for the retro**. Does no evaluating, judging, or concluding (that is the team's job, in the meeting).

## Sources to read (this sprint's scope)
- **Connections and patterns first via graphify (structure):** treat the **god-nodes** (highly connected core concepts) and **surprising connections** (unexpected cross-links) in `graphify-out/GRAPH_REPORT.md` as retro-material candidates. For delayed or blocked items, use `graphify explain "<concept>"` and `graphify path "<A>" "<B>"` to trace structurally **what the item depends on or connects to that caused the blockage** (e.g., "login delay" is connected to the "switch-to-Google decision" and "store review"). Do not read everything wholesale; read only the sources the graph points to.
- **Jira backlog**: done/in-progress/blockers + plan vs. actual (completion rate, carry-over) + (if recorded) **estimated vs. actual time**. Progress checklists are not in the lore vault (they live in each team member's dev repo), so **treat Jira as the source of truth for progress and time**.
- `wiki/` (concepts, decision history): decisions and reversals made during the sprint (only what graphify points to)
- `conflicts/`: conflicts that occurred and were resolved

## Retro draft structure
1. **Plan vs. actual** — completion rate, carry-over (as far as the data goes).
2. **Estimated vs. actual time feedback** — if Jira has estimate/actual times, lay them side by side per item to surface **estimation accuracy** (e.g., "login estimated 2d / actual 5d — 2.5x over"). If there is no data, mark "no time data" and gently remind the team to record estimates and actuals in Jira. This is for calibrating estimates, not for evaluation.
3. **What went well / what got stuck** — based on blocker and conflict patterns.
4. **Decision retro** — reasons behind reversed decisions (from decisions).
5. **Discussion questions** — phrase improvements **as questions** (never force conclusions).

## Provide the minutes form + polish
- Along with the retro draft, present an **empty meeting-minutes form** in Slack so a human can easily fill it into `raw/`:
  ```
  # Sprint Retro — <sprint>/<date>
  ## Attendees
  ## What went well
  ## What got stuck / causes
  ## Estimated vs. actual (estimate calibration)
  ## Action items (owner / due date)
  ```
- **Once a human fills in this form and records it in `raw/` (e.g., `raw/meetings/retro_<date>.md`), polish that meeting note on invocation** — typo fixes, structure cleanup, and item ordering only. **No content invention, no added conclusions** (blanks stay blank). The polished result is also applied only after human confirmation.

## Rules (invariants)
- **No evaluation, no blame, no judgment.** ("A was slow" ✕ → "task X delayed N days, cause needs discussion" ○)
- **Only what has evidence in the lore vault.** Never invent events or numbers. If there is no data, mark "no data".
- Retro outcomes (actions) are **recorded by a human as meeting notes in `raw/` → fed back through the normal pipeline**. This skill does not finalize decisions or actions.
- This channel = this project only. No mentioning or referencing other projects.

## Output
- Post the retro draft to Slack (sections 1–5 + evidence sources) + the empty minutes form. No automatic minutes writing (scope ends at providing the form and polishing).
