---
name: experiment-story-writer
description: Turn ML/AI tables, figures, ablations, and metrics into claim-aware results prose. Use for result paragraphs, figure/table narrative, and provisional metrics.
argument-hint: "[paper-dir] [--section results|experiments|analysis] [--mode plan|draft|revise]"
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Experiment Story Writer

Write experiment and results sections as evidence stories. This skill maps claims to figures, tables, ablations, metrics, and paragraphs, then drafts or revises result prose that explains what the evidence supports.

Use this skill for:

- deciding experiment section order
- writing result paragraphs from tables and figures
- interpreting main results, ablations, diagnostics, efficiency results, and qualitative examples
- handling mixed, negative, or surprising results without undermining the main claim
- marking provisional result placeholders while experiments are running
- aligning result prose with paper claims and evidence status

Do not use this skill to design new experiments from scratch. Use `paper-writing-memory-manager` to record result-prose dependencies, stale claim locations, and open result-writing threads. Use `paper-result-asset-builder` when raw CSV results still need to become paper-facing tables or figures. Use `paper-evidence-gap-miner` when the result story exposes a missing claim support and existing results should be searched before new compute. Use `experiment-design-planner` for truly new experiment planning, `baseline-selection-audit` for baseline fairness, `figure-results-review` for visual audit, `table-results-review` for table audit, and `paper-evidence-board` for claim/evidence inventory.

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
├── references/
│   ├── result-narrative-patterns.md
│   └── mixed-results-and-placeholders.md
└── templates/
    └── experiment-story-plan.md
```

## Progressive Loading

- Always read `references/result-narrative-patterns.md`.
- Read `references/mixed-results-and-placeholders.md` when results are negative, mixed, unstable, provisional, or still running.
- Use `templates/experiment-story-plan.md` when creating `paper/.agent/experiment-story-plan.md`.
- Read local `paper/.agent/writing-contract.md`, `paper/.agent/writing-memory/`, `paper/.agent/paper-evidence-board.md`, `paper/.agent/evidence-completion-plan.md`, `paper/.agent/result-inventory.md`, `paper/.agent/result-asset-provenance.md`, `paper/.agent/provisional-results.md`, `paper/.agent/visual-style.md`, and figure/table review reports when present.
- Read paper files such as `sections/experiments.tex`, `sections/results.tex`, `figures/*.tex`, `tables/*.tex`, and experiment logs or reports under `docs/results/`, `docs/reports/`, or `docs/runs/` when present.

## Core Principles

- Result prose should answer a claim question, not merely describe a table.
- The order of experiments should match the paper's contribution hierarchy.
- Main results establish the claim; ablations explain why; diagnostics bound when; efficiency results explain cost; qualitative results make behavior concrete.
- Every result paragraph should name the comparison, metric, setting, and conclusion.
- Do not hide mixed results. Explain how they narrow, qualify, or motivate the claim.
- Do not invent final numbers. Use marked provisional placeholders only as writing scaffolds.
- If a result contradicts a claim, route to `result-diagnosis` or narrow the claim before writing strong prose.

## Step 1 - Build Results Snapshot

Extract:

```markdown
## Experiment Story Snapshot
- Target venue:
- Paper archetype:
- Primary claims:
- Figures:
- Tables:
- Main metrics:
- Baselines:
- Ablations:
- Verified results:
- User-stated results:
- Provisional or missing results:
- Mixed or negative results:
- Claims at risk:
```

Use claim IDs when available. If no IDs exist, assign local `CLM-TMP-*` IDs and suggest syncing to `paper-evidence-board`.

## Step 2 - Choose Section Story

Read `references/result-narrative-patterns.md` and choose a section order:

- claim-first main results
- benchmark leaderboard plus analysis
- study findings sequence
- mechanism-first ablations
- systems performance stack
- diagnostic or failure-mode sequence

The section order should follow the paper's main claim, not the chronological order in which experiments were run.

## Step 3 - Create Experiment Story Plan

Create or update:

```text
paper/.agent/experiment-story-plan.md
```

If there is no `paper/` directory and the current directory is the paper repo, save to:

```text
.agent/experiment-story-plan.md
```

Use `templates/experiment-story-plan.md`.

For each figure, table, and result paragraph, record:

- evidence job
- claim supported
- result status
- required interpretation
- risk or caveat

## Step 4 - Draft Result Prose

For each paragraph:

- open with the claim question or experiment purpose
- state the setup only as much as needed for interpretation
- describe the most relevant comparison
- interpret why the result supports, narrows, or complicates the claim
- close with the implication for the next experiment or paper claim

Avoid listing numbers without interpretation.

## Step 5 - Handle Provisional and Mixed Results

When results are not final:

- use searchable placeholders such as `[[PROVISIONAL_RESULT:...]]`
- add them to the placeholder ledger
- avoid final superlatives
- write surrounding prose so replacement is localized

When results are mixed:

- say where the method works
- say where it does not
- explain whether the limitation affects the main claim, scope, or future work
- route serious contradictions to `result-diagnosis`

## Step 6 - Final Checks

Before finalizing:

- each main claim has at least one result paragraph
- each main table/figure has a narrative job
- ablations explain mechanism or design choices
- captions and prose do not disagree
- numbers match verified sources or are marked provisional
- mixed results are scoped rather than hidden
- missing blocker evidence is routed first to `paper-evidence-gap-miner`, then to `experiment-design-planner` only if existing CSV results cannot fill the gap
- result-claim dependencies and stale locations are written back through `paper-writing-memory-manager`
