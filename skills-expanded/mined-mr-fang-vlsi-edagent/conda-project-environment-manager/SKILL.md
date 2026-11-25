---
name: conda-project-environment-manager
description: Manage and standardize project conda environment usage as an auxiliary utility skill, including env discovery, package availability checks, explicit env selection, and reproducible `conda run -n ...` integration for scripts and workflows.
---

# Conda Project Environment Manager

Use this skill when the repo needs one stable helper for managing Python/conda environments across scripts, research utilities, and infrastructure workflows.

## When to use

Use this skill when:
1. the project needs to know which `conda` installations and envs are available,
2. a workflow needs a reproducible env choice for scripts such as model fitting, PDF processing, or slide generation,
3. packages are missing from the default shell Python and the project should standardize `conda run -n ...` instead of ad hoc shell state,
4. multiple conda roots (`miniconda`, `anaconda`) coexist and env provenance is becoming confusing,
5. env drift, missing packages, or conflicting Python roots are blocking project work.

## Scope boundary

This skill owns:
- project-level conda env discovery and reporting,
- explicit env-selection guidance for scripts and workflows,
- package-availability checks for target envs,
- environment snapshot artifacts for later maintenance or debugging,
- minimal reproducibility guidance for `conda run -n ...` use in this repo.

It does not own:
- workflow routing or workflow ownership,
- domain experiment conclusions,
- arbitrary package installation policy for unrelated user machines,
- replacing system package managers outside project needs.

## Preferred usage pattern

1. discover conda roots and envs,
2. record package availability in a snapshot artifact,
3. choose one explicit env per workflow/tool family,
4. call scripts through `conda run -n <env> ...` when reproducibility matters,
5. update the snapshot when environments change materially.

## Expected outputs

Typical outputs include:
1. `*.envs.tsv`
2. `*.summary.md`
3. a short recommendation on which env should back which script family
4. maintenance-log or KB refresh only when the environment contract changes materially

## Hard rules

1. Do not rely on accidental shell activation as the default reproducibility mechanism.
2. Prefer explicit `conda run -n <env>` when a script depends on non-system packages.
3. Keep the number of project-preferred envs small; do not create a new env for every one-off task.
4. Record when both `miniconda` and `anaconda` roots coexist so future users do not guess which one is active.

## Operational references

1. Load `references/background-knowledge-links.md` for the current environment topology and project conventions.
2. Load `references/update-mechanism.md` when environment structure or preferred env ownership changes.
3. Use `scripts/common/conda_project_env_report.py` to generate the canonical snapshot before recommending a new env binding.
