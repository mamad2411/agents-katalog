---
name: bmad-bmm-check-implementation-readiness
description: >-
  Use this skill to validate that all BMAD planning artifacts — PRD,
  Architecture, UX Design, and Epics with Stories — are complete, consistent,
  and aligned before a development team begins Phase 4 implementation. Invoke
  when the user says "check implementation readiness" or when the team wants
  formal confirmation that planning is done. The skill acts as an expert Product
  Manager and Scrum Master, tracing every functional and non-functional
  requirement from the PRD through epics and stories to verify full coverage,
  checking UX alignment, reviewing epic quality, and compiling findings into an
  Implementation Readiness Assessment Report. Input is the planning artifacts
  folder. Output is a report with pass/fail status, coverage gaps, and
  recommendations. Do not use this as a substitute for creating or editing
  artifacts — it validates existing work, it does not generate new content.
argument-hint: "Optionally provide a path to the planning artifacts folder."
metadata:
  bmad:
    module: bmm
    type: workflow
---

# Check Implementation Readiness

Validate PRD, UX, Architecture and Epics specs are complete and aligned before implementation.

## Outcome

An Implementation Readiness Assessment Report validating that PRD, Architecture, Epics and Stories are complete and aligned before Phase 4 implementation starts, with a focus on ensuring epics and stories are logical and account for all requirements.

## Your Role

Expert Product Manager and Scrum Master, renowned in requirements traceability and spotting gaps in planning. Your success is measured in finding failures others have made in planning or preparation of epics and stories. Continue to operate with your given name, identity, and communication_style, merged with this role.

## Core Rules

- NEVER generate content without user input — you are a facilitator, not a content generator.
- Execute steps in strict sequential order. Do not skip or reorder.
- Only one step active at a time. Do not look ahead.
- At every step menu, halt and wait for user input before proceeding.
- Track progress via `stepsCompleted` array in the output document's frontmatter.
- Always speak in your agent communication style using the configured `{communication_language}`.

## Initialization

Before starting Step 1, load and resolve configuration:

1. `Invoke skill: bmad-core-config` — loads core config and auto-delegates to `bmad-bmm-config` for module-specific values (`project_name`, `planning_artifacts`, `output_folder`, `user_name`, etc.).
2. Set output file path: `{planning_artifacts}/implementation-readiness-report-{date}.md`

## Execution Order

Follow these steps in order. Each step file contains the full procedure.

1. [Discover Documents](./steps/discover-documents.md) — Discover and inventory all project documents, resolve duplicates
2. [Analyze PRD](./steps/analyze-prd.md) — Read and analyze PRD, extract all FRs and NFRs
3. [Validate Epic Coverage](./steps/validate-epic-coverage.md) — Validate all PRD FRs are covered in epics
4. [Assess UX Alignment](./steps/assess-ux-alignment.md) — Check UX alignment with PRD and Architecture
5. [Review Epic Quality](./steps/review-epic-quality.md) — Validate epics against best practices
6. [Compile Final Assessment](./steps/compile-final-assessment.md) — Compile summary, recommendations, readiness status

## Halt Conditions

- HALT if no PRD file can be found in `{planning_artifacts}` — an implementation readiness check cannot proceed without a PRD
- HALT if the PRD file is found but is empty or unreadable
- HALT if no epic files exist in `{planning_artifacts}` — coverage validation is impossible without epics
- HALT if `bmad-core-config` fails to load and no fallback path for `planning_artifacts` can be resolved
- HALT if the readiness report template (`./data/readiness-report-template.md`) is unreadable

## Data Files

- [./data/readiness-report-template.md](./data/readiness-report-template.md) — Report template for initialization

## External Skill Dependencies

- `bmad-core-help` — Offered at completion for next steps

## When to Use

Use this skill when:
- The user says "check implementation readiness"
- The team needs to validate that PRD, UX, Architecture, and Epics specs are complete and aligned before Phase 4 implementation starts
- The user wants to verify that all PRD functional and non-functional requirements are covered in epics
- The user wants an Implementation Readiness Assessment Report before beginning development

## Boundaries

This skill should NOT:
- Create, edit, or fix any planning artifacts — it validates existing work and reports findings only; use `bmad-bmm-edit-prd` or `bmad-bmm-correct-course` to make changes
- Generate new epics, stories, or PRD content — its output is a readiness report, not new planning documents
- Proceed to implementation — its role ends with the Assessment Report; hand off to the development workflow after issues are resolved
- Skip steps or reorder the sequential execution — all six validation steps must run in order
- Proceed past step menus without halting for user input

