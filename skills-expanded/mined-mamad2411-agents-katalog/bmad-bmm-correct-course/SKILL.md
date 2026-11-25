---
name: bmad-bmm-correct-course
description: >-
  Use this skill to manage significant changes that occur mid-sprint and
  require structured impact analysis before implementation can continue. Invoke
  when the user says "correct course" or "propose sprint change", or when a
  discovered issue, new requirement, or scope shift threatens the integrity of
  the current sprint. The user describes the triggering change and the skill
  systematically assesses impact across PRD, epics, architecture, and UX
  artifacts using a change-navigation checklist, then drafts explicit edit
  proposals for each affected document and compiles a Sprint Change Proposal
  with a clear implementation handoff. Output is an approved change proposal
  and optionally updated artifacts. Unlike bmad-bmm-edit-prd, this skill
  handles cross-artifact change management. Do not invoke for minor tweaks;
  use it when the change could affect multiple planning documents or story scope.
argument-hint: "Describe the issue or change that triggered the need for course correction."
metadata:
  bmad:
    module: bmm
    type: workflow
---

# Correct Course — Sprint Change Management

Manage significant changes during sprint execution.

## Outcome

A structured Sprint Change Proposal that analyzes the triggering issue, assesses impact across all project artifacts (PRD, epics, architecture, UX), and provides an actionable implementation handoff.

## Your Role

Scrum Master navigating change management. Analyze the triggering issue, assess impact, and produce an actionable Sprint Change Proposal with clear handoff. Continue to operate with your given name, identity, and communication_style, merged with this role.

## Core Rules

- Always communicate in `{communication_language}`, tailored to `{user_skill_level}`.
- Generate all documents in `{document_output_language}`.
- User skill level affects conversation style ONLY, not document updates.
- Document output: Updated epics, stories, or PRD sections. Clear, actionable changes.

## Initialization

Before starting Step 1, load and resolve configuration:

1. `Invoke skill: bmad-core-config` — loads core config and auto-delegates to `bmad-bmm-config` for module-specific values (`project_name`, `user_name`, `communication_language`, `document_output_language`, `user_skill_level`, `implementation_artifacts`, `planning_artifacts`, `project_knowledge`, etc.).
2. Set `date` as system-generated current datetime.
3. Set default output file: `{planning_artifacts}/sprint-change-proposal-{date}.md`.

## Execution Order

Follow these steps in order. Each step file contains the full procedure.

1. [Initialize Change](./steps/initialize-change.md) — Confirm change trigger, gather description, verify document access, choose mode
2. [Execute Analysis](./steps/execute-analysis.md) — Work through change navigation checklist interactively
3. [Draft Proposals](./steps/draft-proposals.md) — Create explicit edit proposals for each affected artifact
4. [Generate Proposal](./steps/generate-proposal.md) — Compile comprehensive Sprint Change Proposal document
5. [Finalize And Route](./steps/finalize-and-route.md) — Get approval, classify scope, route for implementation

## Halt Conditions

- HALT if the user cannot describe the triggering change or issue after repeated prompting — the change proposal cannot be written without a defined trigger
- HALT if no planning artifacts (PRD, epics, architecture) can be found in `{planning_artifacts}` — impact analysis is impossible without them
- HALT if the change-navigation checklist (`./data/change-navigation-checklist.md`) is unreadable
- HALT if the user rejects the draft proposals and cannot provide actionable guidance on what to change instead

## Data Files

- [./data/change-navigation-checklist.md](./data/change-navigation-checklist.md) — Systematic change analysis checklist

## External Skill Dependencies

- `bmad-bmm-sprint-planning` — Referenced for refreshing story tracking
- `bmad-bmm-dev-story` — Referenced for minor scope implementation handoff

## When to Use

Use this skill when:
- The user says "correct course" or "propose sprint change"
- A significant change occurs during sprint execution that impacts scope, architecture, or requirements
- The user needs to analyze impact of a change across PRD, epics, architecture, and UX artifacts
- A Sprint Change Proposal document needs to be created with actionable implementation handoff

## Boundaries

This skill should NOT:
- Apply changes directly to any planning artifact (PRD, epics, architecture, UX) — all modifications must go through explicit edit proposals that receive user approval before being applied
- Skip the cross-artifact impact analysis — the change-navigation checklist must be worked through before any proposals are drafted
- Handle single-artifact edits in isolation — use `bmad-bmm-edit-prd` for PRD-only changes; this skill is for changes that ripple across multiple documents
- Generate time estimates of any kind — AI development speed has fundamentally changed
- Route a change for implementation without explicit user approval of the Sprint Change Proposal

