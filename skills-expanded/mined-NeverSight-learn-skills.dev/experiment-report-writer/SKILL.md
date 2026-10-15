---
name: experiment-report-writer
description: Write structured experiment report documents from ML/research experiment notes, configs, logs, metrics, tables, and figures. Use this skill whenever the user asks to write an experiment report, research update, mentor update, weekly experiment summary, result analysis document, or presentation-ready experiment writeup, especially when the output should explain motivation, setup, algorithms, metrics, results, figures, interpretation, conclusions, limitations, and next steps.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Experiment Report Writer

Turn experiment evidence into a clear research report that a reader can evaluate without rerunning the experiment.

Use this skill to write a standalone document, a section for a paper or lab note, a mentor-facing update, or a presentation-ready experiment summary.

Pair this skill with `research-project-memory` when completed results should update project claims, evidence, risks, actions, figures, or worktree decisions.

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── templates/
    └── experiment-report.md
```

## Progressive Loading

- Use `templates/experiment-report.md` as the default Markdown skeleton when saving a report.
- If the user only wants a draft in chat, follow the same section order without needing to read or copy the template verbatim.

## Core Principles

- Ground every claim in evidence: configs, commands, logs, metrics, tables, figures, commit hashes, or user-provided notes.
- Separate observed results from interpretation. Do not present a hypothesis as a measured fact.
- Make the report reproducible enough that another researcher can identify what was run.
- Explain why the experiment matters before listing numbers.
- Compare against the right reference point: baseline, previous run, ablation control, expected behavior, or published number.
- Preserve uncertainty. If evidence is missing, mark it as missing and ask for the smallest useful clarification.
- Write for the intended audience. A lab notebook can be dense; a mentor update should emphasize decisions, evidence, and next steps.

## Step 1 - Classify the Report

Identify the report mode:

- `single-experiment`: one run or one controlled comparison
- `ablation-report`: several variants testing one factor
- `batch-summary`: many related runs from a sweep or experiment batch
- `mentor-update`: concise progress report with decision-oriented discussion
- `paper-section`: polished text intended to become part of a paper

Also identify:

- audience
- output format: Markdown, LaTeX, slide outline, or chat draft
- save path, if the user wants a file
- expected length
- whether figures, tables, configs, logs, or notebooks are available

If the user gives no format, default to Markdown. If they ask for a file and no path is given, use:

```text
docs/reports/experiment_report_YYYY-MM-DD.md
```

## Step 2 - Gather Evidence

Prefer primary evidence over memory.

Look for:

- experiment commands or scripts
- config files and parameter overrides
- random seeds and number of runs
- dataset name, split, preprocessing, and sample count
- model, method variant, checkpoint, or algorithm version
- hardware and runtime if relevant
- metrics, logs, result tables, figures, and failure cases
- git commit hash or code version, when available

Useful local checks include:

```bash
git rev-parse --short HEAD
find . -maxdepth 3 -type f \( -name "*.yaml" -o -name "*.yml" -o -name "*.json" -o -name "*.csv" -o -name "*.md" \)
find . -maxdepth 4 -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.pdf" -o -name "*.svg" \)
```

If the user only provides informal notes, use them but label missing reproducibility details explicitly.

## Step 3 - Extract the Experiment Story

Before drafting, organize the experiment into:

- question: what was this experiment trying to learn?
- motivation: why does the question matter?
- hypothesis: what did we expect and why?
- method: what changed compared with the baseline?
- controls: what stayed fixed?
- measurement: which metrics answer the question?
- outcome: what happened?
- interpretation: what does the outcome suggest?
- decision: what should happen next?

For ablations or sweeps, make the independent variable explicit and keep the comparison fair.

## Required Report Structure

Use these sections unless the user requests a different format:

```markdown
# [Experiment Report Title]

## Summary
## 1. Experiment Motivation
## 2. Experiment Setup
## 3. Core Algorithm or Method
## 4. Metrics
## 5. Results
## 6. How to Read the Figures
## 7. Interpretation
## 8. Conclusion and Discussion
## 9. Limitations and Caveats
## 10. Next Steps
## Reproducibility Notes
```

If there is no core algorithm, write "Not applicable" and briefly explain whether the experiment changes data, hyperparameters, evaluation, infrastructure, or analysis instead.

If there are no figures, omit "How to Read the Figures" or replace it with "How to Read the Tables" when tables are the main evidence.

## Section Guidance

### Summary

Write 3-6 bullets covering:

- experiment question
- most important setup details
- headline result
- interpretation
- recommended next step

### 1. Experiment Motivation

Explain the research or engineering reason for the experiment:

- problem being tested
- expected mechanism
- why the result would affect the project
- what decision the experiment supports

### 2. Experiment Setup

Include enough detail to reproduce or audit the run:

- dataset, split, preprocessing
- baseline and compared variants
- key hyperparameters and parameter changes
- training/evaluation command, config file, or run ID
- random seed and number of trials
- hardware, runtime, and code version when relevant

Use a table for parameters when there are more than five important settings.

### 3. Core Algorithm or Method

Describe the algorithm only at the level needed to understand the experiment:

- what input it consumes
- what output it produces
- key steps or objective
- what is new or different from the baseline
- complexity, assumptions, or implementation details that affect interpretation

Do not over-explain standard background unless the audience needs it.

### 4. Metrics

For each metric, explain:

- definition
- direction: higher is better, lower is better, or target range
- unit
- aggregation: mean, median, best checkpoint, final epoch, confidence interval, or standard deviation
- why it is relevant to the experiment question

Flag metrics that can conflict with each other.

### 5. Results

Present results before interpretation.

Use:

- tables for exact numeric comparisons
- figures for trends, distributions, or qualitative examples
- short text for the main deltas

Always identify the baseline and report absolute values plus meaningful deltas when possible.

### 6. How to Read the Figures

For every figure, explain:

- what the figure is meant to show
- x-axis: variable, unit, and scale
- y-axis: metric, unit, and direction
- legend: method names, groups, colors, markers, or line styles
- error bars or shaded regions, if present
- whether points are individual runs, averages, checkpoints, epochs, or samples
- the main visual pattern the reader should notice

If an axis is log-scaled, normalized, clipped, or unitless, say so explicitly.

### 7. Interpretation

Connect the observed results back to the motivation:

- whether the hypothesis was supported
- what changed relative to the baseline
- likely explanation
- alternative explanations
- surprising or negative results
- whether the evidence is strong enough to act on

Use cautious wording when there is only one seed, weak statistical evidence, or missing controls.

### 8. Conclusion and Discussion

State the practical conclusion:

- what we learned
- what decision this supports
- whether to keep, reject, or further test the method
- how the result affects the broader project

### 9. Limitations and Caveats

Include risks that could change the conclusion:

- small number of seeds
- narrow dataset or subset
- missing baseline
- unstable training
- possible implementation bug
- metric mismatch
- data leakage or evaluation contamination risk
- hardware/runtime constraints

### 10. Next Steps

Recommend concrete follow-ups:

- one immediate verification step
- one high-value extension
- one cleanup or documentation task when needed

Tie each next step to the uncertainty it resolves.

## Project Memory Writeback

If the project uses `research-project-memory`, write back the result after the report is drafted:

- `memory/evidence-board.md`: completed `EVD-###` summary, source paths, linked claim IDs, limitations, and certainty
- `memory/claim-board.md`: mark claims as supported, weakened, revised, unsupported, or cut based on the observed result
- `memory/risk-board.md`: close mitigated risks or add new risks exposed by the result
- `memory/action-board.md`: next steps from the report, including rerun, write, revise-method, park, or kill decisions
- `memory/current-status.md`: latest reliable experiment state and next session entry point
- worktree `.agent/worktree-status.md`: latest result and exit condition if the experiment belongs to a worktree

Do not write an interpretation as a measured fact. Use `observed` for metrics from logs/tables and `inferred` for explanations.

## Output Quality Checklist

Before finalizing, check that:

- the report states the experiment question and decision context
- all key parameters and baselines are named
- metrics include direction and units
- results are separated from interpretation
- every figure/table has reading guidance
- missing evidence is labeled instead of invented
- conclusions do not overclaim beyond the data
- next steps are actionable
- project memory is updated when present and relevant
