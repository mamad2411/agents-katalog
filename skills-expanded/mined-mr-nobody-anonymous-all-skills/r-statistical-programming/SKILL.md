---
name: r-statistical-programming
description: "Analyse data in R: tidyverse workflows, statistical model fitting and diagnostics, reproducible R Markdown/Quarto reports and package-based project hygiene."
type: procedural
category: programming
domain: programming
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - r data analysis
  - ggplot2 chart
  - tidyverse pipeline
  - r statistical test
  - quarto report reproducible
keywords:
  - r
  - tidyverse
  - ggplot2
  - statistics
  - quarto
  - renv
source: custom
enabled: true
---

# R Statistical Programming

## Purpose

Analyse data in R: tidyverse workflows, statistical model fitting and diagnostics, reproducible R Markdown/Quarto reports and package-based project hygiene.

## When to Use

- You need exploratory analysis, statistical tests or publication-quality charts in R.
- A model's assumptions must be checked before its results are reported.
- An analysis has to be reproducible for reviewers.

## When NOT to Use

- The deliverable is production software rather than analysis and reporting.
- The team standard is Python/pandas and no R runtime is available.
- You need deep-learning model training; R is not the right default.

## Capabilities

- Build tidyverse pipelines that are readable and testable.
- Choose statistical tests from the data's structure and verify assumptions.
- Produce reproducible reports with Quarto/R Markdown and pinned dependencies.
- Report uncertainty (confidence intervals, effect sizes) rather than p-values alone.

## Inputs

- The dataset, its provenance and the question being answered.
- The study design (paired, repeated measures, observational) or the analysis intent.
- The reporting format expected by the audience.

## Workflow

1. Load and inspect the data, recording its provenance and any exclusions.
2. State the question and the pre-specified test before looking at the result.
3. Check assumptions (distribution, independence, variance) and pick a robust alternative if violated.
4. Report effect sizes with intervals, not just significance.
5. Knit the report from a clean session with `renv` to prove reproducibility.

## Tools

- R / RStudio
- tidyverse
- Quarto or R Markdown
- renv

## Examples

- `renv::snapshot()`
- `quarto render analysis/report.qmd`
- `t.test(value ~ group, data = df, var.equal = FALSE)`

## Safety

- Never report a result from a run you cannot reproduce; pin packages and seed randomness.
- Multiple comparisons inflate false positives; correct or pre-register.
- Do not remove outliers silently — document and justify every exclusion.

## Source

All-Skills canonical library (`skills/programming/r-statistical-programming`). First-party skill, maintained in this repository.

## Notes

- `set.seed()` belongs next to the random operation, not at the top of the script.
- Effect size and interval estimates matter more than the p-value threshold.
- Pairs with: `research/reproducible-research`, `data/data-analysis`.
