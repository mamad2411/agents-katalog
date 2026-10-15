---
name: fill-in-notes
description: >-
  Turn a textbook chapter, lecture, or paper into beautiful "fill-in" study notes —
  written to be READ (clean statements, intuition) yet engineered to be FILLED
  (blanks, proof skeletons, "your turn" computations) so the reader learns by
  active recall. Notes are typeset with the Loom XeLaTeX class in this repo. Use when
  the user wants study notes from a source with gaps to fill in, worked examples
  restaged as exercises, or theorems stated but proofs left open. Triggers:
  "make fill-in notes", "turn this chapter into notes I can fill in", "guided /
  skeleton study notes", "study notes from this book/PDF", "读+填 笔记",
  "被动+主动 learning notes". NOT for a plain summary, a polished paper, or notes
  with every detail spelled out (that kills the active layer).
---

# Fill-in notes — the Loom method

Produce study notes that a learner both **reads** (passive intake) and **fills**
(active recall). The source is the answer key; the notes are the scaffold. Lead with
a *spine* (one organizing idea) so a chapter becomes a single story, not a transcript.

## Pipeline

1. **Read the source; find the spine.** Skim the chapter/PDF, then name the ONE
   organizing idea and reorganize around it — a dictionary, an engine list, a single
   theorem the rest orbits. Do **not** transcribe section by section if a better shape
   exists. (Concentration → "8 engines"; Nonlinear Algebra → the algebra↔geometry
   dictionary.)
2. **Scaffold.** Copy `template/` (it brings `loom.cls` + a starter `main.tex`).
   Put the master spine on the front page (a cheat-table / map, partly blank), then
   `\input` one file per section under `sections/`.
3. **Draft each section in the Loom grammar** (see the table below).
4. **Engineer the gaps (~70% read / 30% fill).** Read `reference/method.md`. Blank the
   high-value *thinking* moves, never so much that reading breaks.
5. **Compile + verify.** `latexmk -xelatex main` (or `xelatex` twice). Fix the known
   `reference/pitfalls.md` traps. Rasterize a page (ghostscript) and read it back to
   check the look before declaring done.

## The Loom grammar — what goes where

| beat | device | role |
|---|---|---|
| one-line thesis | `strand` env | the big idea, read-only |
| when to use it | `\trigger{…}` | a cue line |
| sub-heading | `\block{…}` | quiet section lead |
| quick-reference | `tabularx` w/ `L` column | the cheat-sheet / dictionary |
| definition | `definition` env (madder knot) | state it, **blank a key clause** with `\fillin` |
| result | `theorem`/`lemma`/`prop`/`cor` (indigo knot) | state in full (read) |
| proof | `proof` + `\TODO{step}` | skeleton; the learner fills the step |
| worked instance | `example` (weld knot) | setup given |
| do-it-yourself | `yourturn` env + `\workspace[n]` | the active zone; the example, restaged |
| grok meter | `\warmth{0..5}` | self-assessment per section |
| margin recall | `\recall{question}` | a parked active-recall prompt |
| open thread | `\loose{…}` | an exercise to pull next time |
| cross-ref thread | `\warp{key}` / `\pick{key}` | declare and reuse a recurring object |

Full command reference: `reference/loom-commands.md`.

## Honest scoping

- The notes restate results from the source. For **personal study** this is fine; before
  making notes that closely track a *copyrighted* book **public**, attribute clearly and
  consider an original example instead (see the repo README's note).
- Keep the source's numbering in the knot title (e.g. `Theorem 4.1 (… Thm. 2.16)`); the
  bold auto-numbers are local to the notes.

## See also
- `../template/main.tex` — blank starter (a live cheat-sheet of every device).
- `../examples/nonlinear-algebra/` — full fill-in treatment (`\fillin`, `yourturn`).
- `../examples/concentration-of-measure/` — proof-skeleton style (`\TODO`).
- `../examples/demo/` — every visual feature on two pages.
