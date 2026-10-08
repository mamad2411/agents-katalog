---
name: target-spec-bootstrap
description: "Create the target repository's local spec skeleton and reusable requirements/design/tasks templates. Use from repo-init-scan during first substantial plugin use, or from spec-writing flows when `spec/INDEX.md` or `spec/templates` is missing. Do not overwrite active project specs."
---

# Target Spec Bootstrap

Create target-local spec routing and templates. Specs are delivery artifacts for requirements, design, task acceptance, traceability, and task progress.

Load `references/templates.md` for exact file contents.

## Boundary

- Write into the target repository, never into the installed plugin package or plugin cache.
- Create missing files only. Do not overwrite active specs or project-specific templates.
- Do not copy this plugin repository's active specs, memory, or workflow examples into the target repository.
- Use specs for MEDIUM/LARGE requirements, design, tasks, acceptance checks, ADRs, progress ledger, and closeout evidence.
- A MEDIUM/LARGE feature spec is a Spec Bundle directory containing `requirements.md`, `design.md`, and `tasks.md`.
- Single-file SDD/design/plan artifacts are evidence only and must be split before implementation planning or execution.
- Link active specs to `memories/repo/current-workstreams.md` when persistent recovery is needed.

## Files To Create

- `spec/INDEX.md`
- `spec/templates/requirements-template.md`
- `spec/templates/design-template.md`
- `spec/templates/tasks-template.md`

## Spec Bundle Guard

When shell access is available and a MEDIUM/LARGE feature is about to leave spec/design review, run:

```bash
<best-copilot-skills-dir>/target-spec-bootstrap/scripts/validate-spec-bundle.sh <target-root>/spec/<feature-slug>
```

The validator is shallow: it checks the required three files and basic source links. It is not a substitute for content review.

## Task Progress Requirements

`tasks.md` templates must include:

- source links to `requirements.md` and `design.md`
- `## Progress Ledger`
- task status values from `core-workflow-contract/references/state-persistence.md`
- per-task owner lane, reviewer lanes, write set, dependencies, parallel group, parallel readiness, acceptance checks, verification command, ready artifacts, and stop conditions
- closeout checklist requiring task/spec/memory agreement

If an existing active `tasks.md` lacks progress tracking, do not rewrite its task definitions. Add a compatible `## Progress Ledger` near the top and initialize rows from visible task IDs.

## Procedure

1. Determine the target repository root from init evidence or PM packet.
2. Read existing `spec/INDEX.md` and templates when present.
3. Create absent files from `references/templates.md`.
4. Preserve active specs and project-specific templates.
5. Repair missing progress-ledger guidance only when it can be appended without overwriting local content.
6. Verify required paths and return created, preserved, repaired, and missing files.

## Verification

- Confirm `spec/INDEX.md` and missing templates exist in the target repository.
- Confirm existing active specs were preserved.
- Confirm `tasks-template.md` includes `## Progress Ledger` and memory/spec closeout rules.
- Confirm generated templates contain metadata, evidence, traceability, verification, task ownership, parallel readiness, and task progress sections.
- If invoked because `spec/**` was missing and required files still do not exist, return `BLOCKED target_spec_bootstrap_incomplete` with missing paths. Do not let the caller continue the substantive task as if initialization succeeded.
