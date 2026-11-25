---
name: thesis-quality-gate
description: Manage a thesis project's machine-readable state, numeric-evidence ledger, literature-verification registry, unified Doctor checks, stage artifact provenance, and tri-state submission gates. Use when Codex or Claude needs to refresh paper status, trace every thesis number to evidence, diagnose Python/LaTeX/font/citation/caption/statistics/DOCX/PDF readiness, or return PASS, REOPEN_WRITING, or REOPEN_ANALYSIS for an advisor-review, predefense, blind-review, or final-delivery package.
---

# Thesis Quality Gate

Use the deterministic CLI in this Skill as the control plane for thesis state and delivery
readiness. Keep project evidence, decisions, reports, and private data in the thesis project;
keep only reusable code and sanitized templates in this Skill.

## Locate the project

Run commands from the thesis project root, which must contain `.project/`. Prefer the
project-local launcher when present:

```bash
python3 scripts/thesis_quality.py state refresh
```

Otherwise invoke the Skill entry directly:

```bash
python3 <skill-path>/scripts/thesis_quality.py --project <project-root> state refresh
```

Read [references/project-contract.md](references/project-contract.md) before onboarding a
new project or changing paths and schemas.

## Operate the quality loop

1. Refresh state before relying on branch, commit, version, page count, stage, risk, or
   last-build information.
2. Refresh the numeric ledger after changing thesis numbers. Treat automatic classification
   as provisional; never auto-mark evidence as verified.
3. Sync the literature registry after changing `ref.bib`. Mark a source verified only after
   checking a real bibliographic source.
4. Run Doctor after meaningful source, environment, build, or delivery changes.
5. Before formal delivery, require confirmed research anchors, an accepted current-stage
   artifact contract, a closed revision ledger, a current deterministic de-AI report, and an
   isolated AI review report.
6. Run the gate matching the requested delivery stage. A blocked gate is a result to explain
   and resolve, not an instruction to weaken policy. Interpret the machine decision as
   `PASS`, `REOPEN_WRITING`, or `REOPEN_ANALYSIS`; when both kinds fail, analysis takes
   precedence while writing failures remain listed.

```bash
python3 scripts/thesis_quality.py evidence refresh
python3 scripts/thesis_quality.py evidence validate
python3 scripts/thesis_quality.py literature sync
python3 scripts/thesis_quality.py doctor
python3 scripts/thesis_quality.py gate --mode predefense
```

Use `--json` on evidence, literature, Doctor, and gate commands when another tool needs
machine-readable output.

## Preserve validation integrity

- Never invent raw data, calculation scripts, enterprise records, citation verification, or
  author confirmation.
- Preserve reviewed ledger entries when rescanning; retire reviewed entries that disappear
  from the manuscript instead of silently deleting their audit history.
- Keep human-controlled state fields intact when refreshing machine-derived fields.
- Treat repository HEAD as an observed snapshot; bind manuscript artifacts and reviews to the
  stable `manuscript_commit` plus the current source-tree digest.
- Reuse an existing Doctor only when engine version, Skill commit, script digest, source tree,
  policy, evidence, literature, PDF, and DOCX provenance all match.
- Treat PDF parsing or OCR failure as a failed or skipped check; never reconstruct missing
  content from inference.
- Do not copy project data, company information, or absolute user paths into this Skill.
- Do not change gate policy merely to obtain `PASS`.

Read [references/evidence-ledger.md](references/evidence-ledger.md) when classifying evidence.
Read [references/gate-policy.md](references/gate-policy.md) when adding checks, changing gate
modes, or interpreting a blocked delivery.
Read [references/stage-artifact-contracts.md](references/stage-artifact-contracts.md) when
binding a stage handoff to exact inputs, outputs, hashes, acceptance checks, and reopen route.

## Integrate with other thesis Skills

- Let `thesis-orchestrator` decide when to call this Skill; keep check implementation here.
- After `thesis-analyze` changes statistics, refresh and validate the evidence ledger.
- After `thesis-literature` verifies sources, update and validate the literature registry.
- After `mem-thesis-build` or `thesis-docx` creates artifacts, refresh state and run Doctor.
- Before `thesis-review` approves delivery, run the appropriate gate and cite its report.

Do not duplicate the scripts inside those Skills. Add only short routing hooks and commands.
