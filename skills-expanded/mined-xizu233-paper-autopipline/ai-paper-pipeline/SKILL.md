---
name: ai-paper-pipeline
description: End-to-end AI conference paper research pipeline for literature search, experiment design, real experiment execution, result analysis, paper drafting, LaTeX export, citation verification, review iteration, and rebuttal preparation. Use when Codex needs to run or manage a top-tier AI/ML paper workflow with staged research, experiments, reproducibility, human approval gates, and submission-quality writing.
---

# AI Paper Pipeline

Use this skill to manage a full AI/ML conference paper workflow without fabricating evidence. Treat it as a collaboration protocol: the agent advances plans, experiments, drafts, and audits; the human researcher approves gates, judges research taste, and owns final submission decisions.

## First Actions

1. Inspect the project before editing: `MEGA_PROMPT.md`, `RESTRICTS.yaml`, `docs/`, `code/`, `data/`, `results/`, `paper/`, and `PROGRESS.md` if present.
2. Check Git status and protect existing user changes.
3. Identify the current stage from `PROGRESS.md`; if absent, initialize the project using `references/project-layout.md`.
4. Create one plan file under `plans/` before each stage.
5. Update `PROGRESS.md` after each stage with version, status, evidence, issues, and next decision.

## Human Collaboration Rules

- Ask the human to approve gate stages: Stage 5 literature screening, Stage 9 experiment design, and Stage 20 quality gate.
- Ask the human before changing the paper's core contribution, weakening or removing a major claim, rewriting an already-submitted abstract, or spending substantial compute.
- Proceed without repeated confirmation for routine bookkeeping, local validation, pilot runs, obvious bug fixes, citation checks, and formatting fixes.
- Present decisions as `PROCEED`, `REFINE`, or `PIVOT`, with evidence and next actions.

## Modes

- `RESEARCH`: read-only investigation; do not edit files.
- `PLAN`: produce a plan, matrix, or revision strategy; do not execute.
- `EXECUTE`: carry out an approved plan.
- `REVIEW`: act as a strict top-conference reviewer; prioritize evidence gaps, weak baselines, missing ablations, and unsupported claims.

## Core Workflow

Read `references/pipeline-stages.md` for the complete 25-stage pipeline.

1. Define topic and problem tree.
2. Collect, screen, and extract real literature.
3. Synthesize gaps and generate falsifiable hypotheses.
4. Design experiments with strong baselines and ablations.
5. Run pilot, estimate time, execute real experiments, and refine failures.
6. Analyze results and decide `PROCEED` / `REFINE` / `PIVOT`.
7. Draft and revise the paper against actual evidence.
8. Export LaTeX, verify citations, and run quality gates.
9. Simulate external review and perform rebuttal-driven iteration.

## Evidence Rules

- Never invent papers, DOIs, citations, datasets, logs, metrics, statistical tests, or results.
- Never present environment setup, dependency installation, debugging logs, or infrastructure failures as research contributions.
- Never use random-number-generated curves as experimental evidence.
- Every experimental number in the paper must trace to `results/` or logs.
- Every cited paper must be real, relevant, and traceable to a source record.

## Experiment Rules

Read `references/experiment-standards.md` before experiment design or code generation.

- Run a small pilot before the main experiment and print `TIME_ESTIMATE: Xs`.
- Use real objectives, real metrics, convergence checks, and deterministic seeds.
- Include strong baselines and one ablation per claimed effective component.
- Detect NaN/Inf and fix root causes rather than masking errors.
- Version all results; do not overwrite prior experiment artifacts.

## Writing Rules

Read `references/paper-writing-standards.md` before paper drafting or revision.

- Keep the paper focused on one or two core contributions.
- Design Figure 1 before drafting the full paper.
- Keep the abstract close to the submitted placeholder unless facts require a change.
- Match every claim to evidence or citation.
- Use the target conference LaTeX template.

## Useful Scripts

- `scripts/init_paper_project.py`: create the expected project structure.
- `scripts/create_stage_plan.py`: create a plan file for a stage.
- `scripts/update_progress.py`: append a structured progress entry.

Prefer these scripts for routine structure and bookkeeping, then inspect generated files.

