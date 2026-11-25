---
name: statistical-analysis-planner
description: Plan and report statistical rigor for ML experiment results. Use when significance testing, effect size reporting, confidence intervals, seed variance analysis, or multiple-comparison corrections are needed before including results in a paper or rebuttal.
argument-hint: "[project-dir] [--mode plan|report|audit] [--test <test-type>]"
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Statistical Analysis Planner

Design the statistical analysis before running, and report it correctly after results exist. This skill prevents underpowered claims, misleading averages-without-variance, and significance theater in ML papers.

Use this skill when:

- deciding which significance tests or confidence intervals to report for a result table
- seed variance is high and a single-run result may not be representative
- comparing methods and wanting to know if the difference is statistically meaningful
- a paper or rebuttal needs to defend a claim quantitatively against reviewer variance concerns
- an ablation result is close and the decision to include it depends on whether the difference is real
- multiple comparisons are being made and type-I error accumulation needs to be controlled

Do not use this skill to run the experiments — use `run-experiment`. Do not use this skill to interpret surprising results scientifically — use `result-diagnosis`. Use this skill after results exist (or in planning mode before deciding how many seeds to run).

Pair this skill with:

- `experiment-design-planner` to plan the number of seeds, runs, and controls before running
- `result-diagnosis` when the statistical analysis reveals that a result is not reliable
- `paper-evidence-board` to update evidence slots with confidence-annotated claims
- `table-results-review` to ensure result tables report variance and pass statistical requirements

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── references/
    └── test-selection.md
```

## Progressive Loading

- Always read `references/test-selection.md` when choosing a statistical test or confidence interval method.
- Read `memory/claim-board.md` and `memory/evidence-board.md` to understand what claims need statistical backing.

## Core Principles

- A mean result without variance is not an empirical claim — it is an anecdote.
- Report the number of seeds and independent runs, not just the metric value.
- Choose the test before seeing the results, not after. Post-hoc test selection biases results.
- Effect size matters more than p-value for practical significance in ML.
- Multiple comparisons require corrections. If you test 10 ablations, 0.5 of them will be "significant" at p<0.05 by chance.
- Reviewer variance concerns are common at NeurIPS/ICLR. Anticipate them with pre-planned variance analysis.
- If compute prevents many seeds, acknowledge the limitation explicitly rather than overclaiming.

## Step 1 — Identify What Needs Statistical Analysis

For each result that will appear in the paper, record:

- the claim being made ("Method A outperforms Baseline B on Task C")
- the metric and its expected distribution
- how many independent runs (seeds) exist
- whether the comparison is within-subject (same data, different methods) or between-subject (different data splits)

Classify each result as:

- `requires-analysis`: main claim or primary comparison
- `supporting-analysis`: ablation or secondary result
- `descriptive-only`: mean reported, no significance claim
- `single-run`: only one run exists, limitations must be acknowledged

## Step 2 — Choose the Analysis Plan

Read `references/test-selection.md`.

For each `requires-analysis` result:

```markdown
Result: <claim or comparison>
Metric: <metric name>
N seeds / runs: <count>
Distribution assumption: normal / non-normal / unknown
Test: <paired t-test / Wilcoxon / bootstrap CI / permutation test / McNemar>
Significance threshold: α = 0.05 (or 0.01 for primary claim)
Effect size measure: Cohen's d / Cliff's delta / relative improvement %
Multiple comparison correction: <Bonferroni / Holm / Benjamini-Hochberg / none>
Report format: mean ± std / 95% CI / p-value + effect size
```

For seed variance analysis, plan:

- minimum number of seeds to detect the expected effect size at power 0.8
- how to report variance: standard deviation across seeds, bootstrap CI, or min/max range

## Step 3 — Run or Verify the Analysis

For results that already exist, compute:

- mean and standard deviation across seeds
- 95% confidence interval (bootstrap recommended for non-normal distributions)
- p-value from the chosen test (if significance is being claimed)
- effect size (Cohen's d or relative improvement %)
- corrected p-values if multiple comparisons are made

For compute-limited settings (1–3 seeds):

- report mean and range (min/max) rather than standard deviation
- acknowledge the limitation explicitly in the paper
- do not claim statistical significance with fewer than 5 independent runs for parametric tests

## Step 4 — Report Format for Paper

For main result tables:

```
Method A: 82.3 ± 1.2 (mean ± std, N=5 seeds)
          [80.4, 84.1] 95% CI
          p < 0.05 vs Baseline B (paired t-test, Bonferroni-corrected)
          Effect size: d = 0.83 (large)
```

For text claims:

- "X outperforms Y by Z% (p < 0.05, d = 0.6)" is preferred over "X significantly outperforms Y"
- "X achieves [metric] = A ± B across N seeds" is preferred over "X achieves A"
- Avoid "significantly" without a reported test and threshold

For low-seed settings:

- "X achieves [metric] = A (range: [B, C], N=3 seeds); we note this result is based on limited seeds"

## Step 5 — Multiple Comparison Audit

If the paper reports more than 3 comparisons on the same held-out set:

- list all comparisons
- apply Bonferroni correction (divide α by number of tests) or Holm correction (less conservative)
- flag any comparison that loses significance after correction
- decide whether to include or describe as "trend" rather than "significant"

## Memory Writeback

- Update `memory/evidence-board.md` when statistical analysis changes the confidence level of a claim
- Update `memory/claim-board.md` to reflect corrected or strengthened claim wording
- Update `memory/risk-board.md` when low seed count or failed significance is a reviewer risk

## Final Sanity Check

Before finalizing:

- every main result table row has at least N, mean, and variance reported
- significance tests were chosen before seeing the specific results, or the analysis plan was declared a priori
- multiple-comparison corrections are applied when > 3 comparisons share a test set
- effect sizes are reported alongside p-values for claimed differences
- compute-limited seed counts are acknowledged as limitations
- claims in the paper match the statistical evidence (no overclaiming)
