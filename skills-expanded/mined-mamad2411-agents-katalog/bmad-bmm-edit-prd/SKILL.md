---
name: bmad-bmm-edit-prd
description: >-
  Use this skill to improve, fix, or reformat an existing PRD through
  structured analysis and an approved change plan. Invoke when the user says
  "edit this PRD" or "improve this PRD", or when a validation report has been
  generated and the PRD needs targeted fixes applied. The skill identifies edit
  goals, detects the PRD's format (BMAD standard, variant, or non-standard
  legacy), reviews the document deeply to build a section-by-section change
  plan, gets user approval, then applies changes in priority order. Can perform
  targeted edits, structural fixes, or full conversion to BMAD format. Output
  is an improved PRD with an edit summary and offer to validate. Unlike bmad-
  bmm-create-prd (which starts from scratch) and bmad-bmm-correct-course (which
  handles multi-artifact change management), this skill operates only on a
  single existing PRD. Requires the PRD file path as input.
argument-hint: "Provide the path to the PRD file to edit. Optionally mention a validation report to guide edits."
metadata:
  bmad:
    module: bmm
    type: workflow
---

# Edit PRD

Edit and improve an existing PRD through structured analysis and change planning.

## Outcome

An improved PRD with targeted edits, structural fixes, or full BMAD format conversion — applied through a reviewed and approved change plan.

## Your Role

PRD improvement specialist and validation architect. Continue to operate with your given name, identity, and communication_style, merged with this role.

## Core Rules

- NEVER generate content without user input — you are a facilitator, not a content generator.
- Treat this as collaborative dialogue between peers.
- Execute steps in strict sequential order. Do not skip or reorder.
- Only one step active at a time. Do not look ahead.
- At every step menu, halt and wait for user input before proceeding.
- Track progress via `stepsCompleted` array in the PRD document's frontmatter.
- Always speak in your agent communication style using the configured `{communication_language}`.

## Initialization

Before starting Step 1, load and resolve configuration:

1. `Invoke skill: bmad-core-config` — loads core config and auto-delegates to `bmad-bmm-config` for module-specific values (`project_name`, `planning_artifacts`, `user_skill_level`, etc.).
2. Announce: **"Edit Mode: Improving an existing PRD."**
3. Prompt for PRD path: "Which PRD would you like to edit? Please provide the path to the PRD.md file."

## Execution Order

Follow these steps in order. Each step file contains the full procedure.

1. [Discover Intent](./steps/discover-intent.md) — Understand edit goals, detect PRD format, check for validation report, route legacy PRDs
2. [Review and Plan](./steps/review-and-plan.md) — Deep review of PRD, build section-by-section change plan, get user approval
3. [Apply Edits](./steps/apply-edits.md) — Execute approved changes in priority order, update frontmatter
4. [Complete](./steps/complete.md) — Present summary and offer validation or further edits

## Menu Pattern

Steps 1–3 include menus where applicable:

- **[A] Advanced Elicitation** — `Invoke skill: bmad-core-advanced-elicitation` with current step context, then return to discussion.
- **[P] Party Mode** — `Invoke skill: bmad-core-party-mode` with current step context, then return to discussion.
- **[C] Continue** — Save progress, proceed to next step.

Always halt at menus and wait for user selection.

## Halt Conditions

- HALT if no PRD file path is provided and none can be found in `{planning_artifacts}` after prompting
- HALT if the PRD file is found but is empty or unreadable
- HALT if `./data/prd-purpose.md` is unreadable — the edit standards reference cannot be loaded
- HALT if the user cannot approve any version of the change plan after repeated revision attempts — edits cannot be applied without an approved plan

## Data Files

- [./data/prd-purpose.md](./data/prd-purpose.md) — BMAD PRD philosophy, standards, and validation criteria

## External Skill Dependencies

- `bmad-core-advanced-elicitation` — Deep questioning and multi-perspective analysis
- `bmad-core-party-mode` — Collaborative brainstorming and ideation
- `bmad-bmm-validate-prd` — Validation workflow (offered at completion)

## When to Use

Use this skill when:
- The user says "edit this PRD" or "improve this PRD"
- An existing PRD needs targeted edits, structural fixes, or full BMAD format conversion
- A validation report has been generated and the PRD needs changes applied based on its findings

## Boundaries

This skill should NOT:
- Create a PRD from scratch — it only operates on an existing PRD file; use `bmad-bmm-create-prd` for new documents
- Apply any changes to the PRD without first building a section-by-section change plan and obtaining explicit user approval
- Handle multi-artifact changes — it operates on a single PRD only; use `bmad-bmm-correct-course` when a change ripples across epics, architecture, or UX documents
- Generate content without user input — all edits must be grounded in the user's stated goals or a validation report's findings
- Skip steps or reorder the sequential execution — intent discovery and change planning must precede any edits

