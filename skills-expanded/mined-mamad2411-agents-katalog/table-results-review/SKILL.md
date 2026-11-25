---
name: table-results-review
description: Review ML/AI result tables, LaTeX table files, captions, provenance, and paper table style. Use for benchmark, ablation, metric, model-spec, and compute tables.
allowed-tools: Read, Write, Edit, Bash, Glob, WebSearch, WebFetch
---

# Table Results Review

Audit standalone paper tables before they become paper evidence, meeting material, or rebuttal material.

Use this skill when:

- the paper stores tables as independent files such as `tables/results.tex` and inserts them into sections with `\input{tables/results}`
- the user has a benchmark, ablation, speed, model-spec, metric-definition, oracle, sanity-check, or appendix table
- a table caption may not match the table content
- row/column meanings, metric direction, bolding rules, footnotes, or missing values are unclear
- table numbers need provenance: result CSV, logs, configs, seeds, aggregation, rounding, or manual edits
- a paper claim depends on table evidence

Do not use this skill for rendered figure assets or plot styling. Use `figure-results-review` for `figures/*.pdf`, `figures/*.png`, and `figures/*.tex` figure bundles. Use `paper-evidence-board` when the main task is linking many figures and tables to claims across the whole paper.

Pair this skill with:

- `paper-result-asset-builder` when a paper-facing table needs to be generated or regenerated from CSV result files before table review
- `paper-evidence-gap-miner` when the table review reveals a missing comparison, slice, variance, or baseline and existing CSVs may already contain it
- `paper-evidence-board` when tables must be linked to paper claims, sections, reviewer risks, and actions
- `baseline-selection-audit` when a comparison table may miss important baselines or use unfair settings
- `result-diagnosis` when table numbers are surprising, unstable, negative, or contradictory
- `experiment-design-planner` when a table exposes missing controls, seeds, metrics, or ablations
- `experiment-report-writer` when raw logs need a structured report before table review
- `conference-writing-adapter` when final table narrative or compactness must match a target venue
- `research-project-memory` when claim/evidence/provenance/risk/action/handoff updates should persist across sessions

## Core Principles

- A table is evidence for a specific claim, not a dump of numbers.
- A table bundle has separate layers: standalone `.tex` source, table description, caption, main-text callout, and provenance.
- Table description and table caption are different artifacts. Describe what the table reports before interpreting why it matters.
- The reader's comparison path should be obvious from row/column grouping.
- If the comparison path is not obvious, prefer repeated key baselines, grouped columns, or a short callout over forcing the reader to infer the intended comparison.
- Bolding, underlining, arrows, missing values, and footnotes must have explicit rules.
- Numeric provenance matters. Record where values came from, how they were aggregated, how they were rounded, and whether they were manually edited.
- A strong table caption states the setup, comparison, metric, key parameter, and takeaway without becoming a full experiment report.
- When a table causes paper layout trouble, first localize the affected page and table source. Prefer local table/prose/placement fixes over global float spacing or paragraph settings; route broader submission-layout debugging to `submit-paper`.
- Wrapped right-side tables are layout objects, not normal floating tables. Do not nest a regular `table` float inside `wraptable`; use an inline block with local caption/label handling, then tune wrap line count, width, font size, `\tabcolsep`, and small local `\vspace` by visual iteration.

## Step 1 - Recover Table Context

Collect:

- standalone table path such as `tables/results.tex`
- paper section where it is inserted with `\input{tables/results}` or equivalent
- current caption, label, and main-text callout
- intended paper claim or reviewer question
- table purpose: main result, ablation, baseline comparison, speed/compute, model spec, metric definition, oracle, sanity check, or appendix detail
- experiment setup: dataset, split, model/checkpoint, baselines, metric, seeds, sampling budget, hyperparameters, compute budget, protocol
- table-generation setup: source CSV/log/report, aggregation rule, row/column selection, sorting, bolding rule, rounding rule, missing-value convention, and manual edits
- linked project memory IDs such as `CLM-###`, `EVD-###`, `TAB-###`, `RSK-###`, or `ACT-###`

Rewrite the intended evidence relation:

```text
This table supports [claim] by showing [comparison/ranking/trend/tradeoff] under [setup].
```

If that sentence cannot be written, route to `paper-evidence-board` before polishing the table.

## Step 2 - Resolve the Table Bundle

For paper tables, identify the standalone source:

```text
tables/table_name.tex
```

Inspect:

- table environment: `table` or `table*`
- tabular structure: `tabular`, `tabularx`, `longtable`, `booktabs`, `resizebox`, `small`, or custom macros
- `\caption{}`, `\label{}`, footnotes, arrows, bold/underline, row groups, column groups, and missing values
- whether values appear hand-entered, macro-generated, or imported from a script
- nearby paper source: where the table is input and how the main text calls it out

Flag the bundle as incomplete if it lacks caption, label, callout, source provenance, or a clear bolding/rounding/missing-value rule.

## Step 3 - Describe Before Interpreting

Produce a table description before judging the caption.

The table description should state:

- table purpose and paper location
- row groups, column groups, metrics, units, and directionality
- comparison path: which rows/columns the reader should compare first
- highlighted values and the bolding/underlining rule
- missing values, footnotes, caveats, and decimal precision
- visible pattern: best method, strongest baseline, tradeoff, ablation trend, failure case, or inconsistency
- experiment parameters needed to interpret the numbers
- source of key values when available, and what is hand-entered versus generated
- what is directly visible versus inferred from logs, configs, filename, caption, or user statement

Do not put the full table description into the caption. Use it as the audit record that checks whether the caption and paper prose are faithful to the table.

## Step 4 - Audit Claim Support

For each table, answer:

- what exact claim does it support?
- is the table sufficient for that claim?
- is the claim too broad for the measured setup?
- are baselines, ablations, controls, seeds, or metrics missing?
- does the table contradict another figure, table, or section?
- is the table main-paper material, appendix material, diagnostic material, or not ready?

Assign one status:

- `supports-claim`
- `supports-narrower-claim`
- `ambiguous`
- `contradicts-claim`
- `diagnostic-only`
- `not-ready`

## Step 5 - Audit Table Integrity

Check:

- rows and columns follow the reader's comparison path
- main method and primary baselines are easy to compare
- metric direction is shown with arrows or text
- bolding and underlining rules are defined and not misleading
- decimal precision matches metric noise
- missing values and failed runs have footnotes
- compute, parameters, data, or NFE columns appear when relevant
- main results and ablations are not mixed in a confusing way
- appendix tables do not hide essential comparisons
- caption, label, row/column names, and paper callout match the table source
- table placement does not rely on fragile wrap behavior near a page boundary; `[H]` still may leave vertical skips, so fix local whitespace in or around the table before changing global settings
- for `wraptable` layouts, optional line count `[N]`, width, caption height, font size, and `\tabcolsep` are documented as local layout choices rather than unexplained magic constants

Flag any issue that could cause a reviewer to misread the result.

## Step 6 - Audit Statistical and Experimental Evidence

Check:

- number of seeds or repeated runs
- variance, confidence interval, standard deviation, or standard error when differences are small
- metric definition and aggregation
- data split and leakage risk
- baseline fairness and tuning budget
- compute, hardware, model size, data, prompt, or selection differences that could change the interpretation of a comparison
- compute or speed reporting when efficiency is part of the claim
- table-generation parameters: source file, filtering, aggregation, sorting, rounding, bolding, missing-value convention, and manual edits

If the table lacks necessary uncertainty or provenance, decide whether to rerun, add columns/footnotes, weaken the claim, or move the table to appendix/diagnostic status.

## Step 7 - Review Caption and Result Narrative

For each table, produce:

- table description
- provenance summary: table `.tex`, source data/log/config/report, table-generation parameters, experiment parameters, and source certainty
- caption-table alignment diagnosis
- caption diagnosis
- revised caption or caption outline
- one-sentence paper callout
- claims to avoid in nearby prose
- reviewer question answered
- missing setup details to add

Caption pattern:

```text
[What the table reports.] We compare [methods] on [task/dataset] using [metrics; direction] under [key experiment parameters].
[Grouping or fairness detail.] [Takeaway tied to the claim]. Bold marks [bolding rule].
```

For model-spec, metric-definition, or method-comparison tables:

```text
[What the table defines or compares.] Columns summarize [fields] used in [paper section or experiment].
[Interpretive note.] [Takeaway tied to the claim or reader task].
```

Do not put every hyperparameter in the caption. Include the parameters needed to interpret the claim. Put full provenance in the review report, appendix, artifact, or `paper/.agent/` record.

## Step 8 - Route Fixes

For every issue, route to one or more actions:

- `fix-table-wrapper`: stale caption, label mismatch, unclear bolding rule, wrong resize, broken footnote, or row/column mismatch in `tables/*.tex`
- `edit-table`: grouping, decimals, bolding, footnotes, missing values, row/column order, or metric arrows
- `rewrite-caption`: setup, metric, takeaway, caveat, bolding rule, or claim alignment
- `write-description`: missing table description or missing provenance record
- `rewrite-results-text`: nearby paper prose overclaims or misses the takeaway
- `build-result-asset`: raw CSV evidence exists but the paper-facing table needs to be generated with documented aggregation, rounding, and provenance
- `mine-existing-results`: missing comparison, slice, variance, or baseline may already exist in CSVs or reports
- `rerun`: missing seeds, variance, baseline, metric, or protocol after existing results are checked
- `diagnose-result`: suspicious, negative, unstable, or contradictory numbers
- `baseline-audit`: missing or unfair baseline
- `narrow-claim`: evidence only supports a smaller statement
- `move-to-appendix`: useful but not central enough for main paper
- `cut`: table does not support a paper need

Name the next skill when appropriate.

## Step 9 - Write the Review Report

If saving to a project and no path is given, use:

```text
docs/results/table_results_review_YYYY-MM-DD_<short-name>.md
```

The report must include:

- table inventory
- table bundle map: source `.tex`, input location, label, caption, paper callout location
- table descriptions
- table-generation and experiment parameter provenance
- claim-support status
- table integrity issues
- statistical evidence issues
- caption and narrative fixes
- reviewer-risk forecast
- routed actions and next skills
- memory update section

## Step 10 - Write Back to Project Memory

When memory exists, update the smallest useful set of entries:

- `memory/evidence-board.md`: table evidence status, source `.tex`, setup, table-generation parameters, experiment parameters, and linked claims
- `memory/claim-board.md`: claims supported, narrowed, contradicted, or not ready
- `memory/risk-board.md`: reviewer risks from table ambiguity, missing uncertainty, weak baselines, missing provenance, or overclaiming
- `memory/action-board.md`: table edits, reruns, caption fixes, result diagnosis, baseline audit, or claim revisions
- `paper/.agent/`: table map, source/input pairings, paper locations, table descriptions, caption state, provenance gaps, and stale table warnings
- worktree `.agent/worktree-status.md`: result-generation or table-generation tasks and exit conditions

Use certainty labels:

- `verified` for values checked against raw data, logs, generated table, or paper text
- `user-stated` for user-supplied context
- `inferred` for reviewer-risk and narrative judgments
- `unverified` for numeric or statistical claims that could not be inspected

## Final Sanity Check

Before finalizing:

- every table has a linked claim and reviewer question
- every paper table has a resolved standalone source when the project uses `tables/*.tex`
- every reviewed table has a table description separate from its caption
- table-generation parameters and experiment parameters are recorded or explicitly marked unknown
- row/column meanings and metric directions are unambiguous
- bolding, underlining, footnotes, rounding, and missing values have rules
- uncertainty is present or the lack of uncertainty is justified
- baseline and compute fairness are visible when relevant
- overclaims are narrowed
- fixes are routed to concrete next actions or skills
- project memory is updated when present
