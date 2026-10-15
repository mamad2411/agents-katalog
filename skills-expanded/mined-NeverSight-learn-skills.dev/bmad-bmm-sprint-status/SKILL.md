---
name: bmad-bmm-sprint-status
description: >-
  Use this skill to read the sprint-status.yaml file and produce a clear,
  actionable summary of the current sprint state with risk detection and a
  recommended next workflow action. Invoke when the user says "check sprint
  status" or "show sprint status", when another skill needs machine-readable
  sprint data (use mode: data), or when the sprint-status.yaml integrity needs
  to be validated (use mode: validate). The skill parses all sprint entries,
  computes story and epic counts by status, detects risks (blocked stories,
  stalled reviews, missing files), selects the top recommended next action, and
  presents a formatted report or structured data output depending on the mode.
  Output is a sprint summary with next-step recommendation, structured data, or
  a validity result. Unlike bmad-bmm-sprint-planning (which generates the status
  file from epics), this skill reads and reports on an existing file. Do not
  invoke if no sprint-status.yaml exists yet — run sprint planning first.
metadata:
  bmad:
    module: bmm
    type: workflow
---

# Sprint Status

Summarize sprint status and surface risks.

## Outcome

A clear sprint status summary with story/epic counts, risk detection, and a recommended next workflow action — or structured data output for programmatic callers.

## Your Role

Scrum Master providing clear, actionable sprint visibility. No time estimates — focus on status, risks, and next steps.

## Core Rules

- Execute ALL steps in exact order; do NOT skip steps.
- Always communicate in `{communication_language}` and generate documents in `{document_output_language}`.
- No time estimates or predictions — only status facts, risks, and recommendations.

## Initialization

Before starting Step 1, load and resolve configuration:

1. `Invoke skill: bmad-core-config` — loads core config and auto-delegates to `bmad-bmm-config` for module-specific values (`project_name`, `user_name`, `communication_language`, `document_output_language`, `implementation_artifacts`, etc.).
2. Set `date` as system-generated current datetime.
3. Set `sprint_status_file` = `{implementation_artifacts}/sprint-status.yaml`.
4. Set `project_context` = `**/project-context.md` (load if exists).

## Execution Modes

This skill supports three execution modes, determined by the `mode` argument:

| Mode | Purpose | Output |
|------|---------|--------|
| `interactive` (default) | Full user-facing sprint report with interactive menu | Formatted summary + action menu |
| `data` | Machine-readable output for other skills | Structured key-value pairs |
| `validate` | Check sprint-status.yaml integrity | Validity result with error details |

If `mode` is not specified, default to `interactive`.

## Execution Order

Follow these steps in order. Each step file contains the full procedure.

1. [Locate and Parse](./steps/locate-and-parse.md) — Find sprint-status.yaml, parse all entries, validate statuses, map legacy values
2. [Analyze and Recommend](./steps/analyze-and-recommend.md) — Detect risks, compute counts, select next action recommendation
3. [Present Report](./steps/present-report.md) — Display summary (interactive), return data (data mode), or return validity (validate mode)

## Halt Conditions

- HALT if `{implementation_artifacts}/sprint-status.yaml` does not exist and the user has not run sprint planning — there is nothing to report on
- HALT if `sprint-status.yaml` exists but is unparseable YAML — integrity cannot be assessed on a corrupt file
- HALT if `validate` mode is requested but `sprint-status.yaml` is missing entirely

## External Skill Dependencies

- `bmad-bmm-sprint-planning` — Referenced when sprint-status.yaml is missing and needs to be generated
- `bmad-bmm-dev-story` — Recommended when in-progress or ready-for-dev stories exist
- `bmad-bmm-code-review` — Recommended when stories are in review status
- `bmad-bmm-create-story` — Recommended when all stories are in backlog

## When to Use

Use this skill when:
- The user says "check sprint status" or "show sprint status"
- Other skills need machine-readable sprint status output (use `mode: data`)
- The `sprint-status.yaml` file integrity needs to be validated (use `mode: validate`)
- The user wants to see story/epic counts, risk detection, and recommended next workflow action

## Boundaries

This skill should NOT:
- Make time estimates or predictions of any kind — only report status facts, risks, and next-step recommendations based on what the data shows
- Modify `sprint-status.yaml` — it reads and reports on the file only; use `bmad-bmm-sprint-planning` to generate or rebuild the file
- Downgrade a story or epic status that already exists at a more advanced state — only forward progress is valid
- Be invoked when no `sprint-status.yaml` exists — run `bmad-bmm-sprint-planning` first to generate the file
- Generate the sprint status file or create new stories — it is a read-only reporting skill

