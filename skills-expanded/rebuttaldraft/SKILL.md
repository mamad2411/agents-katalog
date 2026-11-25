---
name: rebuttaldraft
description: >-
  Draft grounded, paste-ready responses to academic peer reviews.
  Use when the user asks for help writing a rebuttal, responding to
  individual reviewers, analyzing reviewer concerns, finding analogous
  rebuttal precedents from ICLR, ICML, NeurIPS, or COLM reviews, or
  running additional experiments needed to support the response.
---

# RebuttalDraft

Turn a paper plus its reviews into per-reviewer, paste-ready rebuttal drafts. You (the host agent) play
every stage with your own model — no API key. You also run the experiments a rebuttal needs, in the
user's workspace, so the draft has real results instead of blanks.

## Guarantees (state these to the user up front)

- **Confidentiality:** the paper and the review text never leave this machine. Only short, abstract
  search queries you write reach the ReviewSearch API. Paper content is never sent.
- **No fabrication:** never invent an experiment result, a number, or a precedent citation. Un-run
  experiments are handled honestly, never with a made-up outcome.

## The workflow — stages 0 to 5

Read each stage's reference file (under `references/`, next to this SKILL.md) when you reach that stage,
and follow it. Run Stages 1, 2, 4 and 5 once per reviewer; Stage 3 is shared across reviewers.

**Paths in this skill are relative to this skill's own directory**, the one this SKILL.md was loaded
from. `references/` sits beside this file, and the search script lives in the sibling `reviewsearch`
skill at `../reviewsearch/scripts/search_reviews.py`. Both skills ship together, so that path always
resolves, in any host that discovers skills.

### Stage 0 — Intake & detection
Find the paper (PDF / `.tex` / `.md`) and the review(s) (`.md` / `.txt`) in the workspace.
- Both present → confirm with the user which files to use.
- Review missing → ask the user to paste the reviews or save them as files. Multiple reviewers may be one
  file each or one combined file; split them into R1/R2/R3.
- Paper missing → ask for the PDF or source path.
- You cannot read the PDF (some environments) → ask for `.tex` / `.md` / plain text instead.

### Stage 1 — Concern extraction (per reviewer)
Follow `references/stage1-concerns.md`. Produce, for each reviewer, a concern list (each concern: id,
one-sentence text, the underlying concern behind the wording, interpretation confidence, type, severity,
search_needed, abstract search_query) plus the reviewer_score.

### Stage 2 — Grounding (per concern)
Follow `references/stage2-grounding.md`. For each concern with `search_needed=true`, run
`../reviewsearch/scripts/search_reviews.py "<search_query>" --top-k 10` (full corpus, no
`--accepted-only`) ONCE, then walk the results in rank order and stop at the first genuinely
analogous case. Keep that ONE case whole, with the full past review and the full author rebuttal: it is
the exemplar Stage 4 learns from, and its layout (strong rebuttals answer quantitative concerns with a
table) is part of what it teaches. Keep none if nothing matches. Only the abstract query leaves the
machine. Ground one concern per pass and gate immediately; the raw payload is large. Write each gated case
to `rebuttal/experiments/grounding.md` as you go: Stage 4 reads it from there, not from your context.

### Stage 3 — Experiments: plan, get consent, run (the headline step)
Follow `references/stage3-experiments.md`. This is what the web app cannot do, and it runs once, shared
across reviewers: inventory what already exists (inside AND outside the repo), design a concrete experiment
per concern that needs one, dedup overlapping experiments, and present ONE consolidated plan table as the
only consent gate. Run every approved experiment, then write `rebuttal/experiments/RESULTS.md`,
the single source of numbers for Stage 4, marking each section with its provenance. Anything rejected,
failed, or infeasible is handled honestly in Stage 4 (no fabrication, no placeholders). With no compute at
all, follow the dry-run rules: quarantine to `rebuttal_DRYRUN/`, mark synthetic numbers `fabricated: true`,
and banner every draft.

### Stage 4 — Rebuttal Draft + Guide (per reviewer)
Follow `references/stage4-draft.md`. Read `rebuttal/experiments/grounding.md`, `rebuttal/experiments/RESULTS.md`
and the paper itself. Write the paste-ready draft filled with the REAL Stage 3 results, plus the per-concern
guide (with real precedent References) and the overall plan.

### Stage 5 — Critique + revise (per reviewer)
Follow `references/stage5-critic.md`. Score the draft against the rubric and revise (one pass; one more
only for a CRITICAL issue). Only the final draft is written out.

## Output

Create a `rebuttal/` directory in the workspace:
- `rebuttal/R1.md`, `rebuttal/R2.md`, … — per-reviewer, paste-ready (Overview → Draft → Guide).
- `rebuttal/experiments/grounding.md` — the Stage 2 exemplars, kept whole.
- `rebuttal/experiments/RESULTS.md` — the Stage 3 results pack, every section marked with its provenance.
- `rebuttal/experiments/` — Stage 3 run logs and artifacts.

In a dry run (no compute, synthetic numbers) the drafts go to `rebuttal_DRYRUN/` instead, never to
`rebuttal/`.

Then summarize inline: concern counts per reviewer, which experiments ran, which concerns rest on numbers
that were NOT measured, and the draft file paths.

## Notes

- The search API is a free demo and may cold-start (~1 min) after idle; if a call times out, wait ~1
  minute and retry once. Point at a different backend with the `RS_API_URL` env var.

## Attribution

Data: peer reviews from **OpenReview** (ICLR / ICML / NeurIPS / COLM), licensed **CC-BY-4.0**.
