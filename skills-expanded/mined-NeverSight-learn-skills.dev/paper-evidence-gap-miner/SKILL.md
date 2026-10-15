---
name: paper-evidence-gap-miner
description: Mine existing results for paper evidence gaps before new compute. Use when claims lack support, CSVs may already contain evidence, or tables/figures can be derived.
argument-hint: "[project-dir] [--claim <claim-id-or-text>] [--mode mine|audit|plan]"
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Paper Evidence Gap Miner

Find the cheapest way to complete paper evidence. This skill starts from paper claims and writing gaps, searches existing results first, and only routes to new experiments when existing CSVs and derived assets cannot support the claim.

Use this skill when:

- writing reveals that a claim lacks enough evidence
- a paper section needs a missing table, figure, ablation, slice, variance estimate, or baseline comparison
- existing CSV results may already contain the needed evidence
- a claim needs result completion rather than new algorithm or method design
- the user wants to avoid unnecessary compute before submission
- reviewer simulation or consistency editing finds an evidence gap

Do not use this skill to generate final paper figures or tables. Use `paper-result-asset-builder` after this skill identifies reusable CSV evidence. Do not use this skill to design a full new experiment matrix unless existing results are insufficient; route to `experiment-design-planner` only as the last step.

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
├── references/
│   ├── gap-triage.md
│   └── result-reuse-patterns.md
└── templates/
    └── evidence-completion-plan.md
```

## Progressive Loading

- Always read `references/gap-triage.md` and `references/result-reuse-patterns.md`.
- Use `templates/evidence-completion-plan.md` when creating `paper/.agent/evidence-completion-plan.md`.
- Read local `paper/.agent/writing-contract.md`, `paper/.agent/paper-evidence-board.md`, `paper/.agent/writing-memory/`, `paper/.agent/result-inventory.md`, `paper/.agent/result-asset-provenance.md`, `paper/.agent/experiment-story-plan.md`, and `paper/.agent/provisional-results.md` when present.
- Read paper draft files and result CSV inventories before recommending new runs.
- Pair with `paper-result-asset-builder` when existing CSVs can produce a needed table or figure.

## Core Principles

- Missing evidence is not automatically a missing experiment.
- First ask whether the result already exists, can be re-aggregated, can be sliced differently, or can be turned into an appendix asset.
- Treat "补实验" as "补结果" until proven otherwise.
- Prefer the minimum evidence that defends the paper claim and reviewer risk.
- Do not propose expensive compute before checking existing CSVs, logs, reports, tables, figures, and paper evidence memory.
- If existing evidence only supports a narrower claim, recommend claim narrowing before new compute.
- Record whether a gap is solved by reuse, derivation, writing, diagnosis, or new experiment.

## Step 1 - Locate the Writing Gap

Extract the gap from:

- `paper/.agent/writing-contract.md`
- `paper/.agent/paper-evidence-board.md`
- `paper/.agent/consistency-report.md`
- reviewer simulation output
- draft sections such as abstract, introduction, results, limitations, and conclusion
- user-stated claim or missing evidence

Write:

```markdown
- Claim:
- Paper location:
- Current wording:
- Evidence expected:
- Current evidence:
- Why current evidence is insufficient:
- Reviewer risk:
```

## Step 2 - Search Existing Result Sources

Search in this order:

1. `paper/.agent/result-inventory.md`
2. `paper/.agent/result-asset-provenance.md`
3. `paper/.agent/paper-evidence-board.md`
4. `code/docs/results/**/*.csv`
5. `code/docs/runs/**/*.csv`
6. `code/docs/reports/**/*.csv`
7. `code/outputs/**/*.csv`, `results/**/*.csv`, `outputs/**/*.csv`
8. existing `tables/*.tex`, `figures/*.tex`, rendered figures, and experiment reports

If no result inventory exists, route to `paper-result-asset-builder` inventory mode or run its inventory script.

## Step 3 - Classify the Gap

Read `references/gap-triage.md`.

Classify each gap as:

- `already-supported`: evidence exists; prose or board needs update
- `supportable-from-existing-csv`: CSV contains the needed result
- `needs-reaggregation`: existing runs need a new aggregation, uncertainty estimate, or rounding rule
- `needs-slice`: existing results need a dataset/task/group/seed/baseline slice
- `needs-asset`: evidence exists but no paper-facing table/figure exists
- `needs-diagnosis`: existing result is ambiguous, unstable, suspicious, or contradictory
- `needs-claim-narrowing`: evidence supports a smaller claim
- `needs-new-compute`: no existing evidence can answer the claim
- `cut-or-defer`: claim is not worth supporting

## Step 4 - Mine Reusable Evidence

Read `references/result-reuse-patterns.md`.

Try reuse paths before new compute:

- build a main or appendix table from existing CSVs
- add variance or confidence intervals from existing seeds
- create a slice analysis from existing columns
- compare against a baseline already present in CSVs
- derive a trend, scaling, or sensitivity figure from stored runs
- convert a diagnostic result into a limitation or scope claim
- update result prose to use evidence that is already present

For each reuse path, identify exact source files and transformation rules.

## Step 5 - Create Evidence Completion Plan

Create or update:

```text
paper/.agent/evidence-completion-plan.md
```

If there is no `paper/` directory and the current directory is the paper repo, save to:

```text
.agent/evidence-completion-plan.md
```

Use `templates/evidence-completion-plan.md`.

Every gap needs:

- status
- reusable result source, if any
- table/figure asset to build
- prose or claim edit
- next skill
- whether new compute is required

## Step 6 - Route the Minimal Next Action

Route by classification:

- `already-supported` -> `paper-evidence-board` or `paper-writing-assistant`
- `writing-state-update` -> `paper-writing-memory-manager` when the gap changes section status, stale locations, or open writing threads
- `supportable-from-existing-csv`, `needs-reaggregation`, `needs-slice`, `needs-asset` -> `paper-result-asset-builder`
- `needs-diagnosis` -> `result-diagnosis`
- `needs-claim-narrowing` -> `paper-writing-contract-planner`, `limitations-scope-writer`, or `paper-writing-assistant`
- `needs-new-compute` -> `experiment-design-planner`, then `baseline-selection-audit` and `run-experiment` if needed
- `cut-or-defer` -> `paper-writing-contract-planner` and `paper-draft-consistency-editor`

When project memory exists, update:

- `memory/provenance-board.md` with checked sources, missing source classes, and provisional-result replacement needs
- `memory/handoff-board.md` with a `paper-evidence-gap-miner` -> `paper-result-asset-builder` handoff for reusable CSV/report evidence, or a `paper-evidence-gap-miner` -> `experiment-design-planner` handoff only after existing sources cannot fill the gap
- `memory/phase-dashboard.md` if the writing phase regresses to evidence production or paper asset building

## Final Sanity Check

Before finalizing:

- every gap has been checked against existing result sources
- no new compute is proposed when CSV reuse can answer the claim
- the proposed evidence asset has a clear claim job
- claim narrowing is considered when evidence is weaker than wording
- new experiments, if needed, are minimal and reviewer-relevant
- next skills and output files are explicit
