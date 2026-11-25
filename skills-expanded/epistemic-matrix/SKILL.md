---
name: epistemic-matrix
version: 1.0.0
description: |
  Compile an Epistemic Matrix — the Rumsfeld four-quadrant audit (known knowns /
  known unknowns / unknown knowns / unknown unknowns) applied to a scope, grounded
  in evidence on disk. The point is never the four lists; it is the MIGRATION
  machinery that moves items between quadrants. Use when: "epistemic matrix",
  "known knowns", "unknown unknowns", "rumsfeld matrix", "map what we know",
  "what are we blind to", "audit the blind spots", "where do surprises breed".
  Default scope is portfolio-wide; pass a subsystem to scope it (memory, a client
  engagement, a product, an instrument). Produces a paired .md + .html artifact.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Agent
slug: epistemic-matrix
category: operations
complexity: complex
author: "id8Labs"
triggers:
  - "epistemic-matrix"
  - "epistemic matrix"
tags:
  - development
  - tool-factory-retrofitted
---

# Epistemic Matrix


## Core Workflows

### Workflow 1: Primary Action
1. Analyze the input and context
2. Validate prerequisites are met
3. Execute the core operation
4. Verify the output meets expectations
5. Report results

Compile a Rumsfeld epistemic-matrix audit over a scope. Two of these already exist
on disk and define the house style — read them before writing:
- `EPISTEMIC-MATRIX-2026-07-08.md` (portfolio-wide, the canonical form)
- `EPISTEMIC-MATRIX-MEMORY-2026-07-14.md` (subsystem-scoped, shows a headline + addendum)

## The one rule

**The migration is the asset, not the four lists.** Every incident becomes an
unknown-unknown migrating to a known-known; the machinery that does that migration
is what the matrix audits. A matrix that just sorts facts into four buckets has
failed. End every matrix on the migration engine and ranked next moves.

## Doctrine (what makes this ours, not generic Rumsfeld)

1. **Q1 facts carry evidence on disk.** Every known known cites a file, a `file:line`,
   a dated log, a commit, or a board. No claim without a receipt. This is
   `feedback_verify_before_reporting` enforced structurally. If you cannot ground it,
   it is not a Q1 fact — it is a Q2 question.
2. **Q4 is breeding grounds, not items.** You cannot list unknown unknowns by
   definition. You name the *grounds where surprises breed* — and each named ground
   must already have produced at least one real surprise. Speculation without a prior
   incident is not a breeding ground; it is noise.
3. **Q3 is anchored to the J-space rule.** "An unsigned lesson is functionally
   unconscious — you can't steer what you can't say." Q3 hunts things already true on
   disk that no loop reads: dirty trees, inert insights, stale-but-adjudicated bets,
   tools never run, unsigned lessons. This is the weakest quadrant in most systems and
   the highest-value one to work.
4. **Stale claims are the enemy.** A written "fact" that has gone false is worse than
   an unknown. Flag known-knowns going stale as their own shelf, and treat any
   load-bearing doc last touched weeks ago as suspect until re-verified.

## Workflow

### 1. Fix the scope and gather ground truth
- Default scope: the whole portfolio. If the user named a subsystem (memory, a client
  engagement, a product, an instrument), scope to it.
- Enumerate the actual evidence sources for that scope and READ them, do not recall
  them. Portfolio-wide typically means: `ops/GROUND-TRUTH.md`, `FIELD_NOTES.md`,
  `TRAJECTORY.md`, `sales/PIPELINE.md`, live health alerts, the latest audit, recent
  DELTA-BRIEF. A subsystem means that subsystem's own instruments (lint output, census,
  logs, manifests). Run the commands; do not assume their output.
- For a heavy sweep (grep across many files, log trawls), spawn a subagent and keep
  only the findings here — do not flood the compile with raw output.
- Build the dated `Grounded in:` line from what you ACTUALLY consulted. It is a
  provenance claim; it must be true.

### 2. Sort into the four quadrants
Use `TEMPLATE.md` as the skeleton. Fill each quadrant per the doctrine above:
- **Q1 Known Knowns** — verified facts with on-disk evidence, grouped by theme, plus a
  "going stale / watch these" sub-shelf.
- **Q2 Known Unknowns** — a table `# | Question | Owner / gate | Why it matters`. Every
  row has a named owner and a reason it matters. No orphan questions.
- **Q3 Unknown Knowns** — prose bullets, anchored to the J-space rule. Things on disk
  no loop reads.
- **Q4 Unknown Unknowns** — named breeding grounds, each with a prior surprise cited.

### 3. Write the headline (optional but preferred)
If the audit surfaced one dominant finding, lead with a bolded headline paragraph
before Q1 (see the MEMORY matrix). If findings are evenly distributed, skip it.

### 4. Close on the migration engine
- A health-check table: `Quadrant | Owning mechanism | State`. For each quadrant, name
  the portfolio mechanism that owns migrating items OUT of it, and grade its health.
- Then **ranked recommendations** in showrunner Call/Alt framing: the highest-leverage
  single move first, with one alt for perspective. These are the actual output — the
  matrix exists to produce them.

### 5. Render and file
- Filename: `EPISTEMIC-MATRIX[-SCOPE]-YYYY-MM-DD.md` (SCOPE omitted for portfolio-wide,
  uppercased for a subsystem, e.g. `-MEMORY-`). Use the TEMPORAL block for the date.
- Produce the paired `.html` (`feedback_html_paired_render_default`). If a render-doc
  pipeline is available for the tree, use it; otherwise a clean self-contained HTML
  render of the same content.
- Footer: `*Compiled YYYY-MM-DD by [instrument]. Instruments: [list]. Companion:
  [link to prior/related matrix].*`
- If items were resolved the same day, append a dated `## Addendum` execution log
  rather than editing the body — the matrix is a snapshot; the addendum shows the
  migration happening.

## Failure modes to avoid
- **Sorting without migrating.** Four tidy lists and no engine table = failed matrix.
- **Q1 claims from memory.** If it lacks a receipt, demote it to Q2.
- **Q4 as speculation.** No prior surprise on that ground = cut it.
- **Stale provenance.** The `Grounded in:` line naming a source you did not actually
  open is the exact stale-claim failure the matrix is built to catch. Do not commit it.
