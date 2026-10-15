---
name: experiment-design-planner
description: Design hypothesis-driven ML/AI experiments before running them. Use this skill whenever the user wants to plan experiments, ablations, baselines, metrics, controls, seeds, logging, stop conditions, reviewer-proof evidence, or an experiment matrix for a paper claim before using run-experiment or writing results.
argument-hint: "[project-dir] [--claim <claim>] [--mode single|ablation|benchmark|theory|diagnostic]"
allowed-tools: Read, Write, Edit, Bash, Glob, WebSearch, WebFetch
---

# Experiment Design Planner

Turn a research claim into an experiment plan that can actually answer it. This skill is for planning before running, not for reporting completed results.

Use this skill when:

- a user is about to run a new experiment or ablation
- a paper claim needs evidence
- baselines, metrics, controls, or datasets are unclear
- the user is changing too many variables at once
- cluster/compute time should not be wasted on ambiguous runs
- reviewer-proof evidence is needed before submission

Pair this skill with:

- `research-project-memory` when the experiment plan should become project-level evidence, risk, and action memory
- `run-experiment` after the design is ready to execute
- `experiment-report-writer` after results exist
- `paper-reviewer-simulator` to stress-test whether the evidence will satisfy reviewers
- `baseline-selection-audit` before finalizing the experiment matrix when baseline choice, fairness, or reviewer-proof comparisons need deeper review
- `figure-results-review` after plotted or tabulated results exist and need claim-support review

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── references/
    ├── ablation-matrix.md
    ├── evidence-standards.md
    ├── metrics-and-controls.md
    └── report-template.md
```

## Progressive Loading

- Always read `references/evidence-standards.md` and `references/metrics-and-controls.md`.
- Read `references/ablation-matrix.md` when the plan compares variants, components, baselines, hyperparameters, datasets, or model sizes.
- Use `references/report-template.md` when saving or returning a substantial experiment plan.
- If the target repo has `memory/`, update planned evidence, experiment families, risks, and actions using `research-project-memory` conventions.
- If the experiment depends on current baselines, benchmarks, or leaderboard conventions, verify current sources with web search.

## Core Principles

- Start from the claim, not the command line.
- State the hypothesis before running experiments.
- Use a baseline before introducing a new method.
- Change one variable at a time unless the experiment is explicitly factorial.
- Define controls and nuisance variables before interpreting results.
- Make negative results useful by defining falsification and fallback decisions.
- Design the table or figure before running the experiment.
- Stop conditions matter: decide what result is enough to move on.

## Step 1 - Define the Claim and Question

Extract:

- paper or project claim
- research question
- target audience: internal debugging, advisor update, paper evidence, rebuttal, benchmark claim
- expected output: Markdown plan, LaTeX experiment section outline, run matrix, or saved file
- experiment mode:
  - `single`: one controlled comparison
  - `ablation`: component or variable isolation
  - `benchmark`: compare methods across datasets/tasks
  - `theory`: empirical support for a theoretical prediction
  - `diagnostic`: understand a failure mode or surprising result

Rewrite vague goals into testable questions:

```text
Vague: Does our method work?
Testable: Does component X improve metric M over baseline B on datasets D1/D2 under the same training budget?
```

## Step 2 - State Hypotheses

Write:

- primary hypothesis
- alternative explanations
- expected metric direction and rough effect size
- falsification condition
- decision rule

If the user cannot state a falsification condition, the experiment is not ready.

## Step 3 - Define Evidence Standard

Read `references/evidence-standards.md`.

Decide what evidence is needed:

- one table, one curve, one ablation, one qualitative example, one theorem-aligned diagnostic, or a benchmark suite
- number of datasets/tasks
- number of seeds or repeats
- required baselines
- acceptable variance
- whether statistical testing or confidence intervals are needed
- whether results must support a paper claim or only guide next steps

## Step 4 - Choose Baselines and Controls

Identify:

- primary baseline
- strongest prior method or current SOTA, if relevant
- simple baseline
- ablation baseline
- oracle or upper bound, if useful
- controlled variables
- nuisance variables

If no baseline exists, make the first experiment a baseline-establishment experiment.

## Step 5 - Choose Metrics and Logging

Read `references/metrics-and-controls.md`.

For each metric, specify:

- definition
- direction
- aggregation
- split
- variance reporting
- failure interpretation
- why it answers the question

Define required logging:

- command
- config path
- git commit
- dataset version
- seed
- hyperparameters
- hardware/runtime
- metrics
- artifacts: tables, figures, checkpoints, logs

## Step 6 - Build Run Matrix

Read `references/ablation-matrix.md` when there is more than one run.

Create a run table with:

- run ID
- changed variable
- fixed controls
- dataset/split
- metric
- seed/repeats
- expected result
- status
- output path

Split experiments if a run changes more than one conceptual variable.

## Step 7 - Define Stop Conditions and Next Decisions

Write:

- what result is sufficient to support the claim
- what result falsifies or weakens the claim
- what result triggers another ablation
- what result means stop and write/report
- compute budget ceiling
- deadline constraints

## Step 8 - Reviewer Risk Check

Before finalizing, ask:

- Would a reviewer complain that the baseline is weak?
- Is the comparison fair?
- Are seeds/repeats enough?
- Does the experiment isolate the claimed mechanism?
- Are metrics aligned with the claim?
- Is there a confounder that could explain the result?
- Would a negative result still teach something?

If the answer exposes a major weakness, update the design before execution.

## Step 9 - Write the Experiment Plan

Use `references/report-template.md`.

If saving to a project and no path is given, use:

```text
docs/experiments/experiment_plan_YYYY-MM-DD_<short-name>.md
```

If working inside a code repo or code worktree created by `init-python-project` / `new-workspace`, prefer:

```text
docs/reports/experiment_plan_YYYY-MM-DD_<short-name>.md
```

The final plan should be runnable by `run-experiment` and later reportable by `experiment-report-writer`.

## Step 10 - Write Back to Project Memory

If the project uses `research-project-memory`, update:

- `memory/evidence-board.md`: planned `EVD-###` items and `EXP-###` experiment families
- `memory/claim-board.md`: linked claims, marking unsupported or planned claims honestly
- `memory/risk-board.md`: baseline, mechanism, metric, seed, compute, and reviewer risks exposed by the design
- `memory/action-board.md`: runnable next actions, including which experiment to launch first
- relevant worktree `.agent/worktree-status.md`: experiment purpose and exit condition if a branch/worktree is involved

Use `planned` status for experiments that have not run. Do not record expected outcomes as observed evidence.

## Final Sanity Check

Before finalizing:

- claim and hypothesis are explicit
- baseline is defined
- independent variable is isolated
- controls and nuisance variables are listed
- metrics are tied to the question
- run matrix is concrete
- logging requirements are sufficient for reproduction
- stop condition and decision rule are explicit
- reviewer risks are stated
- project memory is updated when the repo has `memory/`
