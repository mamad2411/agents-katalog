---
name: data-pipeline-manager
description: Manage ML dataset pipelines before training. Use when the user needs to acquire, preprocess, split, or version datasets, design train/val/test protocols, audit data quality, check for train/test contamination, or make data decisions that affect experimental validity and reviewer trust.
argument-hint: "[project-dir] [--mode audit|split|quality|contamination|versioning|plan] [--dataset <name>]"
allowed-tools: Read, Write, Edit, Bash, Glob, WebSearch, WebFetch
---

# Data Pipeline Manager

Make deliberate, documented data decisions before training. This skill prevents the most common experimental validity failures: undocumented preprocessing, leaky splits, contaminated test sets, and irreproducible data pipelines.

Use this skill when:

- deciding how to acquire, access, or download a dataset
- designing or auditing train/val/test split protocols
- preprocessing choices need documentation before they affect results
- data quality issues could corrupt baselines or ablations
- contamination between training and evaluation data is a reviewer risk
- dataset versions, seeds, and pipeline steps need to be pinned for reproducibility
- a paper claim depends on a specific data protocol and the protocol is not yet written down

Do not use this skill for running experiments — use `run-experiment` once the pipeline is validated. Do not use this skill to write result sections — use `experiment-story-writer` after results exist.

Pair this skill with:

- `experiment-design-planner` to ensure the split protocol matches the experimental design's evaluation criteria
- `baseline-selection-audit` when dataset choice or protocol affects which baselines are comparable
- `research-project-memory` to record data decisions as claims, evidence, and risks
- `result-diagnosis` when surprising results may trace to a data artifact rather than a method failure
- `paper-evidence-board` when data protocol details need to appear in the paper's methods and evidence slots
- `init-python-project` when the project's `data/` layout and pipeline scripts need to be scaffolded

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
├── references/
│   ├── split-protocols.md
│   └── contamination-guide.md
└── templates/
    └── pipeline-plan.md
```

## Progressive Loading

- Always read `references/split-protocols.md` when designing or auditing split protocols.
- Read `references/contamination-guide.md` when handling LLM evaluation, pre-trained model probing, retrieval benchmarks, or any setting where the model may have seen test-adjacent data.
- Read `templates/pipeline-plan.md` before writing a pipeline plan.
- Read `memory/claim-board.md` and `memory/evidence-board.md` when data decisions need to be linked to paper claims.
- Read `code/.agent/benchmark-plan.md` or equivalent when a benchmark protocol already exists.

## Core Principles

- Treat data decisions as experimental controls, not implementation details.
- Document every preprocessing step before it runs, not after results appear.
- Design splits from the evaluation goal backward: what question must the test set answer?
- Never let the model, hyperparameter search, or any paper-motivated decision touch the test set.
- Contamination is the paper's responsibility: assume reviewers will ask, and have an answer.
- Version the processed dataset alongside the code that created it.
- Seed-fix every shuffle, sampling step, and augmentation that affects reproducibility.
- Data quality issues found after training are ten times more expensive than those found before.

## Step 1 — Gather Context

Locate:

- project root: look for `data/`, `datasets/`, `code/data/`, or user-provided path
- existing pipeline scripts: `data_utils.py`, `preprocess.py`, `scripts/prepare_data.sh`, or equivalent
- existing documentation: `docs/data/`, `data/README.md`, or any dataset description
- experiment design: `code/.agent/benchmark-plan.md`, `memory/claim-board.md`
- paper methods draft: `paper/sections/experiments.tex` or equivalent when present

Record:

- what dataset(s) are in use or planned
- whether a split already exists
- what preprocessing is already applied or planned
- whether any data quality audit has been done
- whether contamination has been checked

If nothing exists, produce a draft pipeline plan and mark uncertain fields as `TBD`.

## Step 2 — Select Pipeline Mode

Choose based on the user's request or the current gap:

- `audit`: review an existing pipeline for completeness, reproducibility, and reviewer risk
- `split`: design or validate the train/val/test split protocol
- `quality`: run or plan a data quality audit (missing values, label noise, distribution shifts, class imbalance)
- `contamination`: check for data leakage between splits and pre-training / retrieved data
- `versioning`: pin dataset version, hashes, download scripts, and processing seeds
- `plan`: create a full pipeline plan covering all of the above for a new dataset

Default: use `audit` when a pipeline exists, `plan` when none exists.

## Step 3 — Design or Audit the Split Protocol

Read `references/split-protocols.md`.

For every dataset split, record:

```markdown
- Split: train | val | test | held-out
- Size: N examples (% of total)
- Stratification: class-stratified | time-ordered | random | grouped | domain-separated
- Overlap policy: none | explicit-allowed (state why)
- Leakage controls: [list controls]
- Assignment seed: <integer>
- Purpose: what hypothesis or metric this split answers
- Forbidden use: what must NOT touch this split before final evaluation
```

Flag any split designed after the method was partially tuned — this is a reviewer-visible risk. Flag any split where the validation set was used as a proxy test set.

## Step 4 — Data Quality Audit

Check:

- **Missing values**: are they meaningful (masked) or errors? What is the imputation or exclusion policy?
- **Label noise**: known label error rate, labeling protocol, inter-annotator agreement if applicable
- **Class imbalance**: imbalance ratio, whether baselines handle it equivalently
- **Distribution shift**: between train and test, or between this dataset and cited prior work
- **Duplicate or near-duplicate examples**: deduplication policy and its effect on split boundaries
- **Outliers**: what is excluded and on what criteria — is this reproducible?
- **Data leakage from preprocessing**: normalization fit on train only; no augmentation at test time

For each finding, classify as:

- `blocker`: will cause invalid results or comparison failures
- `risk`: should be disclosed in the paper's limitations or experiment settings
- `note`: worth tracking but not blocking

## Step 5 — Contamination Check

Read `references/contamination-guide.md`.

For LLM evaluation, retrieval, or pre-trained model probing:

- Check whether benchmark test examples appear in common pretraining corpora (e.g., via n-gram overlap, exact hash, or known contamination audits)
- Check whether model selection used test performance directly or indirectly
- Check whether retrieved context at test time could contain test-set answers
- Check whether data augmentation generated test-adjacent examples

For standard supervised tasks:

- Confirm no sample appears in both train and test after deduplication
- Confirm that grouping or stratification respects natural data boundaries (e.g., speaker IDs, document IDs, patient IDs)
- Confirm that any held-out reserve set was never used for threshold selection or model comparison

For every contamination finding, record the severity and the available mitigation.

## Step 6 — Version and Reproducibility Record

For reproducible experiments, the pipeline plan must include:

```markdown
- Dataset name and version: <name>==<version> or commit/hash
- Download source: <url or repo> (verified checksum or hash)
- Raw data hash: sha256=<hash>
- Processing script: <path/to/script> at git commit <sha>
- Processing seed: <integer> for every random step
- Processed data hash: sha256=<hash> of final splits
- Storage location: <path or remote>
- Excluded samples: <rule and count>
- Known issues: <list>
```

If any of these fields cannot be filled, mark as `TODO` and add to `memory/action-board.md`.

## Step 7 — Write the Pipeline Plan

Use `templates/pipeline-plan.md`.

Save to:

```text
code/.agent/data-pipeline-plan.md
```

If no `code/` directory exists, save to:

```text
.agent/data-pipeline-plan.md
```

When updating, preserve stable decisions and add a compact change note.

## Step 8 — Memory Writeback

After completing a pipeline plan or audit:

- Write data decisions that affect claims to `memory/claim-board.md`
- Write contamination risks to `memory/risk-board.md`
- Write unresolved data quality issues as actions to `memory/action-board.md`
- Write evidence about dataset characteristics to `memory/evidence-board.md` when they are cited in the paper
- Update `memory/current-status.md` when the dataset version or split protocol changes

## Step 9 — Route Follow-Ups

- `experiment-design-planner`: align experimental design with the finalized split protocol
- `baseline-selection-audit`: recheck baseline comparability after split or preprocessing changes
- `result-diagnosis`: diagnose surprising results that may trace to a data issue
- `paper-evidence-board`: add dataset protocol details to the paper's evidence slots
- `init-python-project`: scaffold `data/` layout and pipeline scripts

## Final Sanity Check

Before finalizing:

- every split has a documented purpose and a forbidden-use policy
- every preprocessing step is reproducible with a fixed seed and a version-pinned script
- data quality findings are classified as blockers, risks, or notes
- contamination checks are explicitly done or explicitly deferred with a risk entry
- dataset version, hashes, and download source are recorded or marked TODO
- memory writeback covers affected claims, risks, and actions
- next action is clear
