---
name: bmad-bmm-sprint-planning
description: >-
  Use this skill to generate or refresh the sprint-status.yaml tracking file
  by parsing all epic files and auto-detecting the current status of every
  story. Invoke when the user says "run sprint planning" or "generate sprint
  plan", or when epic files are complete and implementation is about to begin,
  or when the sprint status file needs to be rebuilt from current file-system
  state. The skill discovers all epic files, extracts every story entry, detects
  story statuses by looking for existing story files and their states, builds a
  structured sprint-status.yaml, and displays a completion summary. Output is
  a sprint-status.yaml in the implementation artifacts folder. Unlike bmad-bmm-
  sprint-status (which reads and reports on an existing status file), this skill
  creates or rebuilds the tracking file from source epic documents. Run this
  before the first story is developed, or whenever the sprint status file is
  missing or out of sync with the epics. Requires at least one epic file.
metadata:
  bmad:
    module: bmm
    type: workflow
---

# Sprint Planning

Generate sprint status tracking from epics.

## Outcome

A complete `sprint-status.yaml` file generated from epic files, with story statuses auto-detected and a structured tracking report.

## Your Role

Scrum Master generating and maintaining sprint tracking. Parse epic files, detect story statuses, and produce a structured sprint-status.yaml.

## Core Rules

- Execute ALL steps in exact order; do NOT skip steps.
- Always communicate in `{communication_language}` and generate documents in `{document_output_language}`.
- Never downgrade a status that already exists at a more advanced state.

## Initialization

Before starting Step 1, load and resolve configuration:

1. `Invoke skill: bmad-core-config` — loads core config and auto-delegates to `bmad-bmm-config` for module-specific values (`project_name`, `user_name`, `communication_language`, `document_output_language`, `implementation_artifacts`, `planning_artifacts`, etc.).
2. Set `date` as system-generated current datetime.
3. Set `tracking_system` = `file-system`.
4. Set `project_key` = `NOKEY`.
5. Set `story_location` = `{implementation_artifacts}`.
6. Set `epics_location` = `{planning_artifacts}`.
7. Set `epics_pattern` = `*epic*.md`.
8. Set `status_file` = `{implementation_artifacts}/sprint-status.yaml`.
9. Set `project_context` = `**/project-context.md` (load if exists).

## Execution Order

Follow these steps in order. Each step file contains the full procedure.

1. [Parse Epics](./steps/parse-epics.md) — Discover and load all epic files, extract every work item
2. [Build Structure](./steps/build-structure.md) — Build sprint status entries for each epic, story, and retrospective
3. [Detect Status](./steps/detect-status.md) — Apply intelligent status detection from existing files
4. [Validate and Report](./steps/validate-and-report.md) — Validate coverage, generate YAML, and display completion summary

## Halt Conditions

- HALT if no epic files matching `*epic*.md` can be found in `{planning_artifacts}` — sprint planning requires at least one epic to parse
- HALT if found epic files are all empty or contain no story entries after parsing
- HALT if `{implementation_artifacts}` path cannot be resolved — the `sprint-status.yaml` output file has nowhere to be written
- HALT if the sprint status template (`./data/sprint-status-template.yaml`) is unreadable

## Data Files

- [./data/sprint-status-template.yaml](./data/sprint-status-template.yaml) — Example template showing expected YAML format
- [./data/checklist.md](./data/checklist.md) — Validation checklist for sprint planning output

## External Skill Dependencies

- `bmad-bmm-create-story` — Referenced when stories need to be created
- `bmad-bmm-sprint-status` — Complementary skill for checking sprint status after generation

## When to Use

Use this skill when:
- The user says "run sprint planning" or "generate sprint plan"
- Epic files exist and a `sprint-status.yaml` tracking file needs to be generated or refreshed
- Story statuses need to be auto-detected from existing files and compiled into structured tracking

