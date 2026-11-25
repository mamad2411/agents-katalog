---
name: research-board
description: Hypothesis- and experiment-centred kanban over ~/.research. Cards are research questions with experiments, headline metrics, key plots and linked omp/Orca sessions; `rboard` shows the board, a resume view per card, cross-experiment comparison with a comparability guard, HTML pages, and jumps into (or resumes) the Orca session working on an experiment. Use when the user asks what they were doing on a project, what a hypothesis or experiment status is, wants to compare experiments, attach results or plots to a card, link or reopen a session, or when a work session changed a hypothesis, experiment, result or next action. Complements research-log (why) and never replaces compass, journal or Morgen.
---

# research-board

Answers "what was I testing, what has been tried, what did it show, and where do I resume" for every
registered project. The unit is a **card**: one research question or attempt that can be started,
paused or closed independently. The schema is in `references/schema.md` — read it before writing or
editing a card. Working procedures are in `references/workflows.md`.

## Boundary with the other layers

| Layer | Owns | Not the board's job |
|---|---|---|
| **Card** (`projects/{slug}/cards/Q*.md`) | current work state, evidence verdict, next action, experiments, headline metrics, key plots, linked sessions | reasoning |
| `journal.md` | why a decision was made, lessons | current status |
| `compass.md` | direction, sub-goals, drift anchor (M4 stays Compass-based) | experiment detail |
| `state.md` | one-snapshot session pointer | history |
| Morgen | schedule, paper writing, non-research tasks | — |

Three axes are kept apart: `work` (board column), `verdict` (evidence badge), run `state`
(observation with a date). Never derive one from another.

## Tool

`scripts/rboard.py` (PEP 723, `uv run`; dependency: PyYAML). If `~/.local/bin/rboard` exists it is a
symlink to it. Store root defaults to `~/.research`; `--root`/`$RBOARD_ROOT` selects another (used
for staging).

| Command | Purpose |
|---|---|
| `rboard [-p slug] [board --closed]` | text board: columns by work state, verdict badge, last experiment, next action, session state, days since verified |
| `rboard show <slug:Qn>` | resume view: claim/scope, next action and blocker, what the verdict rests on, corrections and invalidations, experiments with metrics, arm comparisons, sessions |
| `rboard compare <refs…> [--html f]` | arm comparison inside an experiment; alignment across experiments only for identical name/unit/scope, otherwise `NOT COMPARABLE` with the reason |
| `rboard html [-o dir]` | static board + card pages (default `~/.research/board/`, gitignored, regenerable) |
| `rboard serve [--port 8765]` | serve the board at `http://127.0.0.1:8765/`, rebuilt from the cards on every page load. Use this for Orca's embedded browser: it blocks link clicks inside `file://` pages, so a `file://` board cannot open its card pages |
| `rboard refresh [ref] [--accept]` | recompute stored metric values and source hashes from `extract` specs; dry run unless `--accept` |
| `rboard lint [-p slug]` | schema errors (exit 1) and state warnings |
| `rboard link <ref> --here \| --terminal H \| --session P [--unlink id]` | link the omp session working on a card or experiment |
| `rboard open <ref> [--pick N] [--dry-run] [--no-focus]` | switch to the linked session's Orca terminal, or resume it there |
| `rboard sessions` | live omp sessions, their terminal handle and card link |
| `rboard render <slug:Qn/En/pn>` | run a plot recipe from the project root |

`<ref>` is `slug:Qn` or `slug:Qn/En` (`Qn` alone works when `-p slug` is given).

## Rules

1. **Draft, then approve, then write.** Card changes follow the research-log write rule: present the
   full card delta (and the journal draft when one exists) together, name each file, wait for
   approval, then write under `flock ~/.research/.locks/{slug}.lock`. `link` on an explicit user request
   and `refresh --accept` after showing the dry run are the only writes the tool makes itself.
2. **Reconcile before writing.** For any card built from existing records, compare journal, state,
   compass and result files by topic. Unresolvable disagreement becomes `needs_review: true` with a
   note. Never pick the newest file by default; each of them has been the stale one.
3. **No invented structure.** Engineering and exploration are cards with that `kind`, not hypotheses
   with a made-up falsifier. Backfilled falsifiers are `retrospective`. Unknown stays `unknown`.
4. **Scope carries every condition that changes a number** (split, horizon, pinned vs Z2, data,
   band). Two numbers align only when name, unit and full scope are identical; do not edit a scope to
   force an alignment.
5. **Results are stored, not recomputed on display.** Every metric carries an `extract` spec and the
   experiment lists its `sources` with hashes, so `refresh` can prove them or flag them stale. At most
   six headline metrics per experiment; `n` and `lo/hi` always.
6. **Plots are drawn from data with `scienceplot-py`** so the style is consistent. Pre-existing
   figures may be attached with `style: legacy` (labelled "style unverified"); redraw one only when the
   user asks.
7. **Sessions are linked at the end of work on an experiment**: `rboard link <ref> --here`. `open`
   never resumes a session that another process holds open.
8. A `running` run not observed for 3+ days is reported as *last observed running, currently unknown*;
   never copy an old `running` into a new observation.
