---
name: writing-artifacts
description: Turn a fuzzy subject — a problem description, an incident, a decision, a long-form idea — into a polished deliverable in the user's chosen format (md, html page, Artifact, image, or plain prose). Runs the writing production line (mine → structure → tighten) with stop-slop discipline, then hands rendering to using-design-skills. Invoke when the user wants something EXPLAINED WELL as a document/page, not when they just want code changed.
---

# writing-artifacts

A production line: raw thoughts in, publishable artifact out. You orchestrate
stations; each station's method lives in its own SKILL.md — read it at that
stage, never work from memory of it.

## Stage 0 — frame (one question round, then move)

Pin three things before writing anything: the SUBJECT (one sentence), the
READER (who must understand it), and the OUTPUT FORMAT. Default format by
destination: quick share → `md` · something the user will look at twice or
show someone → `html` page or Artifact · visual metaphor / hero image needed →
add an image stage. If the user already said the format, don't ask.

**Genre branch, decided here:** in-repo SOFTWARE documentation (README, API
docs, tutorials, how-to guides — anything living under the repo) swaps the
structure station: run `documentation-writing` (Eight Rules + Diataxis, docs/
location and linking rules) as Stage 2 instead of the writing-beats/shape
pair, keeping Stage 1 mining and Stage 3 `stop-slop` discipline unchanged.
Everything else — problem writeups, incidents, decisions, long-form prose —
takes the default line below.

## Stage 1 — mine (diverge)

`writing-fragments`: dump everything known about the subject as raw
fragments — evidence, timeline, feelings, half-thoughts — no structure yet.
For a genuinely fuzzy idea (not a known incident), run `adhd` first for
parallel divergence, then fragment the survivors.

## Stage 2 — structure (converge)

Pick ONE:
- `writing-beats` — when the reader must be LED somewhere: problem
  narratives, incident writeups, decision rationales. Grounds each term
  before a beat leans on it.
- `writing-shape` — when the material is already roughly ordered and just
  needs shaping paragraph by paragraph.

## Stage 3 — tighten

`edit-article` over the draft, with `stop-slop` loaded as criteria for the
whole run (not just this stage): no filler, no hedging, no AI-slop cadence.

## Stage 4 — render (format branch)

- `md` / plain prose → deliver the tightened text directly; done.
- `html` page / Artifact / diagram / image → hand the FINISHED TEXT to
  `using-design-skills` as the content contract and let IT compose the
  pipeline (it owns authority selection, imagegen delegation, and the
  screenshot-evidence quality loop). Never style inline yourself; the text is
  frozen content by this point — design changes layout, not wording.

## Boundaries

- Words first, pixels second: never enter Stage 4 with an untightened draft —
  redesigning slop produces well-dressed slop.
- One pass back is allowed: if rendering reveals a structural hole (a section
  that can't be visualized because it was never actually explained), return
  to Stage 2 for THAT section only, then re-render.
- This skill owns written deliverables about a subject — prose AND in-repo
  software docs (the genre branch in Stage 0 picks the structure station).
  A plan page from a discussion → `html-plan` directly.
