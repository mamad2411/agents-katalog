---
name: model-card-writer
description: Generate model cards, reproducibility statements, and datasheet documentation for ML models and datasets. Use when releasing a model, completing venue-required artifact documentation, or writing a reproducibility/datasheet section for NeurIPS, ICLR, ICML, or artifact evaluation.
argument-hint: "[project-dir] [--type model-card|datasheet|repro-statement|artifact-readme] [--venue <venue>]"
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Model Card Writer

Document models, datasets, and artifacts so that users, reviewers, and the research community can understand what was built, what it does well, where it fails, and how to use it responsibly.

Use this skill when:

- releasing a model checkpoint publicly (GitHub, HuggingFace, Zenodo)
- a venue submission requires a model card, datasheet, or reproducibility statement
- an artifact evaluation package needs a README with claims, environments, and expected outputs
- a dataset is being released and needs a datasheet (Gebru et al. format)
- a reproducibility section for NeurIPS/ICLR checklist needs to be filled

Do not use this skill to write the paper's main contributions or results — use `paper-writing-assistant`. Do not use this skill to prepare the full submission package — use `submit-paper` or `camera-ready-finalizer`.

Pair this skill with:

- `artifact-evaluation-prep` when the artifact is being prepared for formal artifact evaluation at a conference
- `release-code` to prepare the code repository before writing the model card
- `camera-ready-finalizer` when the model card is part of camera-ready materials
- `appendix-organizer` when the model card content should be summarized in a paper appendix

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── templates/
    ├── model-card.md
    └── datasheet.md
```

## Progressive Loading

- Read `templates/model-card.md` when writing a model card.
- Read `templates/datasheet.md` when writing a datasheet for a dataset.
- Read `memory/claim-board.md` and `memory/evidence-board.md` when filling performance and limitations sections.
- Read the paper abstract and contributions section when available.

## Core Principles

- A model card is a communication artifact, not a marketing document.
- Limitations and failure modes are as important as performance claims.
- Every performance claim in a model card should be backed by the same evidence as the paper.
- Scope: what tasks, domains, and use cases is the model intended for?
- Out-of-scope uses should be explicit: misuse is foreseeable and should be addressed.
- Bias, fairness, and social impact disclosures protect users and the research team.
- Keep model cards in sync with the actual released checkpoint — stale cards are misleading.

## Step 1 — Select Document Type

- **model-card**: documents a released model checkpoint, its intended use, performance, and limitations
- **datasheet**: documents a released dataset's composition, collection, preprocessing, and intended use (Gebru et al. 2018 format)
- **repro-statement**: a short reproducibility statement for a paper submission (NeurIPS/ICLR style)
- **artifact-readme**: a README for an artifact evaluation package

## Step 2 — Gather Model / Dataset Information

For a model card, collect:

- model name and version
- model type: architecture, parameter count, pretraining objective
- training data: dataset name(s), size, license
- intended tasks and domains
- evaluation results: metrics on standard benchmarks and paper-specific tasks
- known limitations: failure modes, out-of-distribution behavior, biases
- hardware and compute used for training
- code and checkpoint release location

For a datasheet, collect:

- dataset name and version
- collection method: web scraping, human annotation, sensor data, etc.
- annotation protocol and inter-annotator agreement (if applicable)
- dataset size and format
- train/val/test split design
- known biases or representational gaps
- license and terms of use
- PII, sensitive content, or consent considerations

## Step 3 — Write the Document

Use `templates/model-card.md` or `templates/datasheet.md`.

Save to:

- Model card: `<release-dir>/MODEL_CARD.md`
- Datasheet: `<release-dir>/DATASHEET.md`
- Repro statement: `paper/.agent/reproducibility-statement.md` or directly into the paper appendix
- Artifact README: `artifact/README.md` or `<artifact-dir>/README.md`

## Step 4 — Reproducibility Statement (Venue-Required)

For NeurIPS/ICLR/ICML submissions, the reproducibility statement should include:

- what code is available (URL, or "will be released upon acceptance")
- training hardware (GPU type, count)
- total compute for main result (GPU-hours)
- which hyperparameters are reported in the paper or appendix
- whether results are averaged over multiple seeds and how many
- whether the model checkpoint is available

For NeurIPS, this becomes a checklist answer. For ICLR, it is a free-text section. Use `appendix-organizer/references/venue-checklists.md` for the specific format.

## Step 5 — Bias and Limitations Section

Every model card should include:

- **Intended uses**: what tasks and domains the model was designed for
- **Out-of-scope uses**: applications the model was not designed for and should not be used for
- **Known failure modes**: conditions where the model reliably fails
- **Bias and fairness**: demographic groups or domains where performance is unequal
- **Social impact**: positive and negative potential societal effects

Do not write vague disclaimers. Specific known failure modes and bias sources are more useful and more trusted.

## Memory Writeback

- If a model card documents performance claims, verify against `memory/evidence-board.md`
- If a model card reveals a risk not yet on `memory/risk-board.md`, add it
- If a dataset datasheet is written for a project dataset, update `code/.agent/data-pipeline-plan.md`

## Final Sanity Check

Before finalizing:

- all performance claims are backed by evidence from the paper or experiments
- limitations and failure modes are specific (not just "may not generalize")
- intended use and out-of-scope use are explicit
- license and access information is correct
- for venue submissions, required checklist items are answered
- save path is committed or ready to commit with the release
