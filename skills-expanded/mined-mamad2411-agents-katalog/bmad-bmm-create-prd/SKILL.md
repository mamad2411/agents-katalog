---
name: bmad-bmm-create-prd
description: >-
  Use this skill to create a comprehensive Product Requirements Document from
  scratch through structured, step-by-step PM facilitation. Invoke when the
  user says "create a product requirements document", "create a new PRD", or
  when a product idea, brief, or research documents need to be formalized into
  a requirements specification. The skill acts as a collaborative PM peer,
  guiding discovery of project classification, product vision, success criteria,
  user journeys, domain requirements, innovation aspects, scope boundaries,
  functional and non-functional requirements, and final polish. Output is a
  complete BMAD-standard PRD saved to the planning artifacts folder. Supports
  resuming incomplete workflows. Unlike bmad-bmm-edit-prd (which modifies an
  existing PRD), this skill creates a new PRD. Do not invoke to update or fix
  an existing document — use bmad-bmm-edit-prd for that purpose.
argument-hint: "Optionally provide a project name or path to existing input documents (product brief, research, brainstorming)."
metadata:
  bmad:
    module: bmm
    type: workflow
---

# Create PRD

Create a PRD from scratch through structured PM facilitation.

## Outcome

A comprehensive Product Requirements Document created through structured collaborative facilitation between a PM facilitator and the user.

## Your Role

Product-focused PM facilitator collaborating with an expert peer. Continue to operate with your given name, identity, and communication_style, merged with this role.

## Core Rules

- NEVER generate content without user input — you are a facilitator, not a content generator.
- Treat this as collaborative dialogue between PM peers.
- Execute steps in strict sequential order. Do not skip or reorder.
- Only one step active at a time. Do not look ahead.
- At every step menu, halt and wait for user input before proceeding.
- Track progress via `stepsCompleted` array in the output document's frontmatter.
- Always speak in your agent communication style using the configured `{communication_language}`.

## Initialization

Before starting Step 1, load and resolve configuration:

1. `Invoke skill: bmad-core-config` — loads core config and auto-delegates to `bmad-bmm-config` for module-specific values (`project_name`, `planning_artifacts`, `implementation_artifacts`, `project_knowledge`, `user_skill_level`, etc.).
2. Announce: **"Create Mode: Creating a new PRD from scratch."**

## Execution Order

Follow these steps in order. Each step file contains the full procedure.

1. [Initialize](./steps/initialize.md) — Detect continuation state, discover input documents, set up document
2. [Discover Project](./steps/discover-project.md) — Classify project type, domain, and context
3. [Discover Vision](./steps/discover-vision.md) — Uncover product vision and differentiator
4. [Generate Executive Summary](./steps/generate-executive-summary.md) — Draft and append Executive Summary
5. [Define Success Criteria](./steps/define-success-criteria.md) — Define user, business, and technical success
6. [Map User Journeys](./steps/map-user-journeys.md) — Map all user types with narrative journeys
7. [Explore Domain](./steps/explore-domain.md) — Domain-specific requirements (optional, complex domains only)
8. [Explore Innovation](./steps/explore-innovation.md) — Detect and explore innovative aspects (optional)
9. [Explore Project Type](./steps/explore-project-type.md) — CSV-driven project-type specific discovery
10. [Define Scope](./steps/define-scope.md) — MVP boundaries and phased feature roadmap
11. [Define Functional Requirements](./steps/define-functional-requirements.md) — Synthesize the capability contract
12. [Define Non-Functional Requirements](./steps/define-nonfunctional-requirements.md) — Quality attributes that matter
13. [Polish](./steps/polish.md) — Optimize document for flow, coherence, and density
14. [Complete](./steps/complete.md) — Finalize workflow and suggest next steps

## Menu Pattern

Steps 2–13 share this menu pattern after content is drafted/discovered:

- **[A] Advanced Elicitation** — `Invoke skill: bmad-core-advanced-elicitation` with current step context, then ask user to accept improvements. Return to menu.
- **[P] Party Mode** — `Invoke skill: bmad-core-party-mode` with current step context, then ask user to accept changes. Return to menu.
- **[C] Continue** — Save content to document, update `stepsCompleted` frontmatter, proceed to next step.

Always halt at the menu and wait for user selection.

## Halt Conditions

- HALT if the PRD document template (`./data/prd-template.md`) is unreadable
- HALT if the user cannot provide a project name, problem statement, or product description after repeated prompting — a PRD cannot be created without a defined product concept
- HALT if `bmad-core-config` fails and no `planning_artifacts` output path can be resolved
- HALT if the user refuses to define any functional requirements after the full discovery workflow — the PRD cannot reach minimum viable completeness

## Data Files

- [./data/project-types.csv](./data/project-types.csv) — Project type detection signals, key questions, required/skip sections, innovation signals
- [./data/domain-complexity.csv](./data/domain-complexity.csv) — Domain complexity levels, key concerns, compliance requirements
- [./data/prd-purpose.md](./data/prd-purpose.md) — BMAD PRD philosophy, standards, and validation criteria
- [./data/prd-template.md](./data/prd-template.md) — PRD document template for initialization

## External Skill Dependencies

- `bmad-core-advanced-elicitation` — Deep questioning and multi-perspective analysis
- `bmad-core-party-mode` — Collaborative brainstorming and ideation
- `bmad-bmm-validate-prd` — Validation workflow (offered at completion)

## When to Use

Use this skill when:
- The user says "create a product requirements document" or "create a new PRD"
- A new product or feature needs a structured PRD created from scratch through PM facilitation
- The user has a product idea, brief, or research documents and needs to formalize requirements
- The project is starting Phase 2 of BMAD and needs a comprehensive PRD before architecture work

