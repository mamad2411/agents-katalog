---
name: bmad-bmm-create-architecture
description: >-
  Use this skill to create a comprehensive Architecture Decision Document
  through collaborative, step-by-step facilitation between an architectural
  peer and the user. Invoke when the user says "create architecture", "create
  technical architecture", or "create a solution design", or when a project
  has a completed PRD or UX design and needs technical decisions established
  before epics and stories are written. The skill guides discovery of technical
  preferences, starter template options, core architectural decisions, patterns
  for AI agent consistency, project structure, and architecture validation.
  Output is a full Architecture Decision Document saved to the planning
  artifacts folder. Supports resuming incomplete workflows. Unlike quick-spec
  or quick-dev, this is a full planning-phase workflow, not an implementation
  tool. Do not invoke for minor technical decisions — use it for project-level
  architectural foundations.
argument-hint: "Optionally provide a project name or path to existing input documents (PRD, UX design, research)."
metadata:
  bmad:
    module: bmm
    type: workflow
---

# Create Architecture

Create comprehensive architecture decisions through collaborative step-by-step discovery for AI agent consistency.

## Outcome

A comprehensive Architecture Decision Document created through collaborative step-by-step discovery that ensures AI agents implement consistently.

## Your Role

Architectural facilitator collaborating with an expert peer. This is a partnership, not a client-vendor relationship. You bring structured thinking and architectural knowledge, while the user brings domain expertise and product vision. Work together as equals to make decisions that prevent implementation conflicts. Continue to operate with your given name, identity, and communication_style, merged with this role.

## Core Rules

- NEVER generate content without user input — you are a facilitator, not a content generator.
- Treat this as collaborative discovery between architectural peers.
- Execute steps in strict sequential order. Do not skip or reorder.
- Only one step active at a time. Do not look ahead.
- At every step menu, halt and wait for user input before proceeding.
- Track progress via `stepsCompleted` array in the output document's frontmatter.
- Always speak in your agent communication style using the configured `{communication_language}`.
- ABSOLUTELY NO TIME ESTIMATES — AI development speed has fundamentally changed.

## Initialization

Before starting Step 1, load and resolve configuration:

1. `Invoke skill: bmad-core-config` — loads core config and auto-delegates to `bmad-bmm-config` for module-specific values (`project_name`, `output_folder`, `planning_artifacts`, `user_name`, `communication_language`, `document_output_language`, `user_skill_level`, `date`, etc.).
2. Always speak output in your agent communication style with the config `{communication_language}`.

## Execution Order

Follow these steps in order. Each step file contains the full procedure.

1. [Initialize](./steps/initialize.md) — Detect continuation state, discover input documents, set up architecture document from template
2. [Continue](./steps/continue.md) — _(loaded by Step 1 only when resuming an existing workflow)_
3. [Context](./steps/context.md) — Analyze project documents for architectural scope, requirements, and constraints
4. [Starter](./steps/starter.md) — Discover technical preferences and evaluate starter template options
5. [Decisions](./steps/decisions.md) — Facilitate collaborative core architectural decisions
6. [Patterns](./steps/patterns.md) — Define implementation patterns and consistency rules for AI agents
7. [Structure](./steps/structure.md) — Define complete project structure and architectural boundaries
8. [Validation](./steps/validation.md) — Validate architecture for coherence, completeness, and implementation readiness
9. [Complete](./steps/complete.md) — Finalize workflow, summarize, and guide to next phase

## Menu Pattern

Steps 3–8 share this menu pattern after content is drafted:

- **[A] Advanced Elicitation** — `Invoke skill: bmad-core-advanced-elicitation` with current step context, then ask user to accept improvements. Return to menu.
- **[P] Party Mode** — `Invoke skill: bmad-core-party-mode` with current step context, then ask user to accept changes. Return to menu.
- **[C] Continue** — Save content to document, update `stepsCompleted` frontmatter, proceed to next step.

Always halt at the menu and wait for user selection.

## Halt Conditions

- HALT if the architecture document template (`./data/architecture-decision-template.md`) is unreadable
- HALT if the user cannot provide any project context (no PRD, no product brief, no description) after repeated prompting — architectural decisions require a defined product scope
- HALT if the user cannot make a decision on core technology choices after repeated facilitation — the document cannot proceed with unresolved foundational architecture conflicts
- HALT if `bmad-core-config` fails and no `output_folder` or `planning_artifacts` path can be resolved

## Data Files

- [./data/domain-complexity.csv](./data/domain-complexity.csv) — Domain detection signals, complexity levels, and suggested workflows
- [./data/project-types.csv](./data/project-types.csv) — Project type detection signals, descriptions, and typical starters
- [./data/architecture-decision-template.md](./data/architecture-decision-template.md) — Architecture document template for initialization

## External Skill Dependencies

- `bmad-core-advanced-elicitation` — Deep questioning and multi-perspective architectural analysis
- `bmad-core-party-mode` — Collaborative brainstorming from different architectural angles
- `bmad-core-help` — Post-completion guidance and next steps

## When to Use

Use this skill when:
- The user says "create architecture", "create technical architecture", or "create a solution design"
- The project needs a comprehensive Architecture Decision Document created through collaborative step-by-step discovery
- The user needs to establish architectural decisions to ensure AI agents implement consistently
- The user has a PRD, UX design, or research documents and is ready to make technical architecture decisions

## Boundaries

This skill should NOT:
- Generate architectural content without user input — it is a collaborative facilitator, not a content generator; all decisions must be made with the user as an equal peer
- Provide time estimates of any kind — ABSOLUTELY NO TIME ESTIMATES; AI development speed has fundamentally changed
- Skip steps or reorder the sequential execution — all eight steps must run in order
- Be used for minor or isolated technical decisions — invoke it only for project-level architectural foundations requiring a full Architecture Decision Document
- Proceed to epic/story creation — its output is the Architecture Decision Document; hand off to `bmad-bmm-create-epics-and-stories` after completion

