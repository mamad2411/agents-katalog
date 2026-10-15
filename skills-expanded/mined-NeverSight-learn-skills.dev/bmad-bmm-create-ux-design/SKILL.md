---
name: bmad-bmm-create-ux-design
description: >-
  Use this skill to create a comprehensive UX Design Specification through
  collaborative visual exploration and step-by-step facilitation between a UX
  facilitator and a product stakeholder. Invoke when the user says "create UX
  design", "create UX specifications", or "help me plan the UX", or when a PRD
  exists and the project is ready to define visual and interaction patterns
  before architecture decisions are finalized. The skill guides discovery of
  project context and UX challenges, core experience and platform, emotional
  responses and design inspiration, design system selection, visual foundation
  (colors, typography, spacing), design directions, user journey flows,
  component strategy, UX consistency patterns, and responsive accessibility.
  Output is a full UX Design Specification saved to the planning artifacts
  folder. Supports resuming incomplete workflows. Unlike bmad-bmm-create-
  architecture (which handles technical decisions), this skill focuses
  exclusively on the user experience layer.
argument-hint: "Optionally provide a project name or path to existing input documents (PRD, product brief, research)."
metadata:
  bmad:
    module: bmm
    type: workflow
---

# Create UX Design

Plan UX patterns and design specifications through collaborative visual exploration.

## Outcome

A comprehensive UX Design Specification created through collaborative visual exploration and informed decision-making between a UX facilitator and a product stakeholder.

## Your Role

UX facilitator collaborating with a product stakeholder. Continue to operate with your given name, identity, and communication_style, merged with this role.

## Core Rules

- NEVER generate content without user input — you are a facilitator, not a content generator.
- Treat this as collaborative discovery between UX facilitator and stakeholder.
- Execute steps in strict sequential order. Do not skip or reorder.
- Only one step active at a time. Do not look ahead.
- At every step menu, halt and wait for user input before proceeding.
- Track progress via `stepsCompleted` array in the output document's frontmatter.
- Always speak in your agent communication style using the configured `{communication_language}`.

## Initialization

Before starting Step 1, load and resolve configuration:

1. `Invoke skill: bmad-core-config` — loads core config and auto-delegates to `bmad-bmm-config` for module-specific values (`project_name`, `planning_artifacts`, `output_folder`, `product_knowledge`, `user_name`, `user_skill_level`, etc.).
2. Set `date` as system-generated current datetime.
3. Announce: **"UX Design Mode: Creating a new UX Design Specification."**

## Execution Order

Follow these steps in order. Each step file contains the full procedure.

1. [Initialize](./steps/initialize.md) — Detect continuation state, discover input documents, set up document
2. [Discover Project](./steps/discover-project.md) — Understand project context, target users, and UX challenges
3. [Define Core Experience](./steps/define-core-experience.md) — Define core user experience, platform, and experience principles
4. [Define Emotional Response](./steps/define-emotional-response.md) — Define desired emotional responses and feelings
5. [Analyze Inspiration](./steps/analyze-inspiration.md) — Analyze inspiring products and extract transferable UX patterns
6. [Choose Design System](./steps/choose-design-system.md) — Choose appropriate design system foundation
7. [Define Experience](./steps/define-experience.md) — Define the core interaction that makes the product special
8. [Establish Visual Foundation](./steps/establish-visual-foundation.md) — Establish color, typography, and spacing systems
9. [Explore Design Directions](./steps/explore-design-directions.md) — Generate and evaluate design direction variations
10. [Design User Journeys](./steps/design-user-journeys.md) — Design detailed user journey flows
11. [Plan Component Strategy](./steps/plan-component-strategy.md) — Define component library strategy and custom components
12. [Define UX Patterns](./steps/define-ux-patterns.md) — Establish UX consistency patterns
13. [Define Responsive Accessibility](./steps/define-responsive-accessibility.md) — Define responsive design and accessibility strategy
14. [Complete](./steps/complete.md) — Finalize workflow and suggest next steps

## Menu Pattern

Steps 2–13 share this menu pattern after content is drafted/discovered:

- **[A] Advanced Elicitation** — `Invoke skill: bmad-core-advanced-elicitation` with current step context, then ask user to accept improvements. Return to menu.
- **[P] Party Mode** — `Invoke skill: bmad-core-party-mode` with current step context, then ask user to accept changes. Return to menu.
- **[C] Continue** — Save content to document, update `stepsCompleted` frontmatter, proceed to next step.

Always halt at the menu and wait for user selection.

## Halt Conditions

- HALT if the UX Design Specification template (`./data/ux-design-template.md`) is unreadable
- HALT if the user cannot describe the product's target users or core use case after repeated prompting — UX decisions cannot be made without a defined user and context
- HALT if `bmad-core-config` fails and no `planning_artifacts` output path can be resolved
- HALT if the user cannot make a decision on the design system foundation after repeated facilitation — downstream component and pattern steps depend on this choice

## Data Files

- [./data/ux-design-template.md](./data/ux-design-template.md) — UX Design Specification document template for initialization

## External Skill Dependencies

- `bmad-core-advanced-elicitation` — Deep questioning and multi-perspective analysis
- `bmad-core-party-mode` — Collaborative brainstorming and ideation

## When to Use

Use this skill when:
- The user says "create UX design", "create UX specifications", or "help me plan the UX"
- The project needs a comprehensive UX Design Specification created through collaborative visual exploration
- A PRD exists and the project is ready to define UX patterns, design system, and component strategy

## Boundaries

This skill should NOT:
- Generate UX content without user input — it is a collaborative facilitator, not a content generator; all design decisions must be confirmed with the user before proceeding
- Make technical architecture decisions — it focuses exclusively on the user experience layer; use `bmad-bmm-create-architecture` for technical decisions
- Skip steps or reorder the sequential execution — the 13-step flow must run in order, as downstream steps (component strategy, accessibility) depend on earlier choices (design system, visual foundation)
- Look ahead to future steps or pre-fill content from a later step while a current step is still active
- Proceed past the design system selection if the user cannot make a decision — downstream component and pattern steps depend on this foundational choice

