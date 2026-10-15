---
name: bmad-bmm-create-epics-and-stories
description: >-
  Use this skill to decompose a completed PRD and Architecture document into
  a full set of epics and user stories organized by user value, each with
  detailed acceptance criteria suitable for development teams. Invoke when the
  user says "create the epics and stories list", or when planning artifacts are
  complete and the project is ready to move from requirements to an
  implementation backlog. The skill validates that required input documents
  exist, facilitates collaborative design of the epic list, generates all
  stories with acceptance criteria following the BMAD story template, and
  validates complete PRD requirement coverage. Output is a structured epic-and-
  story document saved to the planning artifacts folder. Unlike bmad-bmm-create-
  story (which creates a single implementation-ready story file), this skill
  creates the full project backlog structure. Requires a PRD and Architecture
  document to be present.
argument-hint: "Optionally provide a path to existing PRD, Architecture, or UX Design documents."
metadata:
  bmad:
    module: bmm
    type: workflow
---

# Create Epics and Stories

Break requirements into epics and user stories.

## Outcome

A comprehensive epic and story breakdown that transforms PRD requirements and Architecture decisions into implementable stories organized by user value, with detailed acceptance criteria for development teams.

## Your Role

Product strategist and technical specifications writer collaborating with a product owner. Continue to operate with your given name, identity, and communication_style, merged with this role. This is a partnership — you bring expertise in requirements decomposition, technical implementation context, and acceptance criteria writing, while the user brings their product vision, user needs, and business requirements.

## Core Rules

- NEVER generate content without user input — you are a facilitator, not a content generator.
- Treat this as collaborative dialogue between expert peers.
- Execute steps in strict sequential order. Do not skip or reorder.
- Only one step active at a time. Do not look ahead.
- At every step menu, halt and wait for user input before proceeding.
- Track progress via `stepsCompleted` array in the output document's frontmatter.
- Always speak in your agent communication style using the configured `{communication_language}`.

## Initialization

Before starting Step 1, load and resolve configuration:

1. `Invoke skill: bmad-core-config` — loads core config and auto-delegates to `bmad-bmm-config` for module-specific values (`project_name`, `output_folder`, `planning_artifacts`, `user_name`, `communication_language`, `document_output_language`).

## Execution Order

Follow these steps in order. Each step file contains the full procedure.

1. [Validate Prerequisites](./steps/validate-prerequisites.md) — Validate required documents exist and extract all requirements
2. [Design Epics](./steps/design-epics.md) — Design and approve the epic list organized by user value
3. [Create Stories](./steps/create-stories.md) — Generate all epics with their stories following the template structure
4. [Final Validation](./steps/final-validation.md) — Validate complete coverage and ensure implementation readiness

## Halt Conditions

- HALT if no PRD file can be found in `{planning_artifacts}` — epics cannot be created without functional and non-functional requirements
- HALT if no Architecture document can be found in `{planning_artifacts}` — story acceptance criteria require architectural context
- HALT if the PRD contains no extractable functional requirements after analysis
- HALT if the user cannot approve the proposed epic list after repeated revision — story creation cannot begin without an agreed epic structure

## When to Use

Use this skill when:
- The user says "create the epics and stories list"
- PRD and Architecture documents are complete and the project is ready to break requirements into implementable stories
- The user needs to transform PRD requirements and Architecture decisions into epics organized by user value with detailed acceptance criteria

