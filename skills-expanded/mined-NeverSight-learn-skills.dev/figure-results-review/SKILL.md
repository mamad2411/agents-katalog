---
name: figure-results-review
description: Review ML or AI experiment figures, tables, plots, captions, result narratives, and paper visual style before they are shown in a paper, advisor meeting, report, slide deck, rebuttal, or submission. Use this skill whenever the user has experimental results, plots, tables, metrics, screenshots, captions, draft result sections, or wants to audit figure style choices such as color, typography, markers, symbols, line widths, sizing, and venue-consistent visual conventions.
argument-hint: "[project-dir-or-results-file] [--mode paper|meeting|slide|rebuttal|diagnosis] [--venue <venue>]"
allowed-tools: Read, Write, Edit, Bash, Glob, WebSearch, WebFetch
---

# Figure Results Review

Audit figures, tables, plots, captions, and result narratives before they become paper evidence or meeting material.

Use this skill when:

- the user has a figure, table, plot, result screenshot, caption, result section, or slide with experimental evidence
- a paper claim needs to be checked against the actual displayed evidence
- a plot may be missing baselines, error bars, seeds, labels, units, or fairness context
- a table layout hides the main comparison or makes the result look weaker than it is
- paper figures need a consistent visual style: color palette, markers, symbols, line widths, fonts, sizing, and notation
- new results require deciding whether to update writing, rerun experiments, diagnose failures, or narrow claims
- a rebuttal needs a clean result table or concise visual answer
- an advisor meeting needs figures that make the decision obvious

Do not use this skill to design experiments from scratch. Use `experiment-design-planner` before results exist. Use `result-diagnosis` when the primary issue is why a result is surprising or broken. Use `conference-writing-adapter` when the main task is prose style after the evidence is already accepted.

Pair this skill with:

- `paper-evidence-board` when figures/tables must be linked to paper claims, sections, reviewer risks, and actions
- `result-diagnosis` when a plotted result is suspicious, unstable, negative, or contradictory
- `baseline-selection-audit` when the visual exposes missing, weak, or unfair baselines
- `experiment-design-planner` when the fix requires new experiments, ablations, controls, or metrics
- `experiment-report-writer` when raw results need a structured report before figure review
- `conference-writing-adapter` when the final figure narrative or visual style must be adapted to a target venue
- `research-project-memory` when claim/evidence/risk/action updates should persist across sessions

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── references/
    ├── caption-and-narrative.md
    ├── claim-support.md
    ├── memory-writeback.md
    ├── paper-visual-style.md
    ├── report-template.md
    ├── statistical-evidence.md
    └── visual-integrity.md
```

## Progressive Loading

- Always read `references/claim-support.md`, `references/visual-integrity.md`, and `references/statistical-evidence.md`.
- Read `references/paper-visual-style.md` when figures/tables are intended for a paper, slide deck, rebuttal, camera-ready, or venue-specific rewrite.
- Read `references/caption-and-narrative.md` when revising captions, result prose, slide text, or paper figure callouts.
- Read `references/report-template.md` before writing the final review.
- Read `references/memory-writeback.md` when the project has `memory/`, component `.agent/` folders, or the user asks for persistent project memory.
- If the expected plotting or table conventions depend on a target venue, benchmark, or recent paper style, verify with current accepted papers, official benchmark protocols, or user-provided exemplars.
- If the actual image/table cannot be inspected, audit the provided data/caption/prose and clearly mark visual-layout judgments as unverified.

## Core Principles

- A figure is evidence for a specific claim, not decoration.
- Every plot/table should answer one reviewer question.
- The main comparison should be visually and numerically easy to find.
- Captions must state enough setup for the result to be interpreted without searching the paper.
- Statistical uncertainty, seeds, and variance matter when the claim depends on small differences.
- Compute, data, baseline, and protocol fairness must be visible when they affect interpretation.
- Paper figures should share a deliberate visual language. Style choices are part of writing because they control what reviewers notice first.
- A beautiful plot that does not support the claim should be revised or cut.
- New results must update claims, writing, reviewer risks, and next actions.

## Step 1 - Recover Evidence Context

Collect:

- figure/table file path, screenshot, raw data, caption, or result prose
- paper claim or section the result is meant to support
- experiment setup: dataset, model, baseline, metric, seed, split, hyperparameters, protocol
- target audience: paper, advisor meeting, slide, rebuttal, internal report, or appendix
- target venue or benchmark expectations
- current paper location, if any
- linked project memory IDs such as `CLM-###`, `EVD-###`, `FIG-###`, `TAB-###`, `RSK-###`, or `ACT-###`

Rewrite the intended evidence relation:

```text
This figure/table is supposed to show that [claim] because [metric/comparison/trend] under [setup].
```

If that sentence cannot be written, route to `paper-evidence-board` before polishing the visual.

## Step 2 - Audit Claim Support

Read `references/claim-support.md`.

For each figure or table, answer:

- what exact claim does it support?
- is the displayed evidence sufficient for that claim?
- is the claim too broad for the measured setup?
- are baselines, ablations, controls, or diagnostics missing?
- does the result contradict another figure, table, or section?
- is the result main-paper material, appendix material, diagnostic material, or not ready?

Assign one status:

- `supports-claim`
- `supports-narrower-claim`
- `ambiguous`
- `contradicts-claim`
- `diagnostic-only`
- `not-ready`

## Step 3 - Audit Visual and Table Integrity

Read `references/visual-integrity.md`.

Check:

- axes, labels, units, scales, and transformations
- legend readability and method names
- ordering of methods, datasets, metrics, and ablations
- whether the main result is visually salient
- table grouping, bolding, decimals, missing values, and footnotes
- whether color, markers, line styles, or hatching remain readable in grayscale
- whether figure size works for one-column, two-column, slide, or appendix usage
- whether captions and labels match the actual plotted data

Flag any issue that could cause a reviewer to misread the result.

## Step 4 - Audit Paper Visual Style

Read `references/paper-visual-style.md` when the output is paper-facing.

Check:

- color palette and colorblind/grayscale robustness
- stable method-to-color and method-to-marker mapping across all figures
- line width, marker size, hatch, symbol, and notation consistency
- font size, tick density, label length, and final-column readability
- figure dimensions for one-column, two-column, appendix, or slide use
- whether visual emphasis matches the paper's claim hierarchy
- whether the main method is recognizable without relying only on color
- whether theorem/method symbols in plots match the paper notation

If the paper has no visual style policy, propose one and record it in `paper/.agent/` or `.agent/conference-writing/project-style.md` when appropriate.

## Step 5 - Audit Statistical and Experimental Evidence

Read `references/statistical-evidence.md`.

Check:

- number of seeds or repeated runs
- variance, confidence intervals, standard deviation, or standard error
- significance or effect-size interpretation when differences are small
- data split and leakage risk
- metric definition and averaging
- baseline fairness and tuning budget
- compute or speed reporting when efficiency is part of the claim
- failure cases or negative results that should be shown

If the plot lacks necessary uncertainty, decide whether to rerun, add error bars, weaken the claim, or move the result to appendix/diagnostic status.

## Step 6 - Review Caption and Result Narrative

Read `references/caption-and-narrative.md` when output text needs revision.

For each figure/table, produce:

- caption diagnosis
- revised caption or caption outline
- one-sentence paper callout
- claims to avoid in nearby prose
- reviewer question answered
- missing setup details to add

Captions should not oversell. They should state the setup, comparison, metric, and takeaway.

## Step 7 - Route Fixes

For every issue, route to one or more actions:

- `edit-figure`: labels, ordering, scale, legend, layout, or visual emphasis
- `edit-table`: grouping, decimals, bolding, footnotes, missing values, or row/column order
- `rewrite-caption`: setup, metric, takeaway, caveat, or claim alignment
- `rewrite-results-text`: nearby paper prose overclaims or misses the takeaway
- `define-visual-style`: missing or inconsistent paper visual style policy
- `restyle-figure`: color, marker, line width, font size, symbol, panel layout, or emphasis
- `rerun`: missing seeds, variance, baseline, metric, or protocol
- `diagnose-result`: suspicious, negative, unstable, or contradictory pattern
- `baseline-audit`: missing or unfair baseline
- `narrow-claim`: evidence only supports a smaller statement
- `move-to-appendix`: useful but not central enough for main paper
- `cut`: visual does not support a paper need

Name the next skill when appropriate.

## Step 8 - Write the Review Report

Read `references/report-template.md`.

If saving to a project and no path is given, use:

```text
docs/results/figure_results_review_YYYY-MM-DD_<short-name>.md
```

The report must include:

- figure/table inventory
- claim-support status
- visual/table integrity issues
- visual style policy and consistency issues
- statistical evidence issues
- caption and narrative fixes
- reviewer-risk forecast
- routed actions and next skills
- memory update section

## Step 9 - Write Back to Project Memory

Read `references/memory-writeback.md` when memory exists.

Update the smallest useful set of entries:

- `memory/evidence-board.md`: figure/table evidence status, setup, and linked claims
- `memory/claim-board.md`: claims supported, narrowed, contradicted, or not ready
- `memory/risk-board.md`: reviewer risks from visual ambiguity, missing uncertainty, weak baselines, or overclaiming
- `memory/action-board.md`: figure edits, reruns, caption fixes, result diagnosis, or claim revisions
- `paper/.agent/`: figure/table map, paper locations, caption state, and stale visual warnings
- `.agent/conference-writing/project-style.md`: venue-facing figure style decisions when conference adaptation is active
- worktree `.agent/worktree-status.md`: result-generation or plotting tasks and exit conditions

Use certainty labels:

- `verified` for values checked against raw data, logs, or source figures
- `user-stated` for user-supplied context
- `inferred` for reviewer-risk and narrative judgments
- `unverified` for visual or statistical claims that could not be inspected

## Final Sanity Check

Before finalizing:

- every figure/table has a linked claim and reviewer question
- main comparison is easy to find
- axes, units, legends, captions, and table labels are unambiguous
- colors, markers, fonts, symbols, and figure sizes are consistent across the paper
- uncertainty is present or the lack of uncertainty is justified
- baseline and compute fairness are visible when relevant
- overclaims are narrowed
- fixes are routed to concrete next actions or skills
- project memory is updated when present
