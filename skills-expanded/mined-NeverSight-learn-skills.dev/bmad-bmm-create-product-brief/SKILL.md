---
name: bmad-bmm-create-product-brief
description: >-
  Use this skill to create a structured Product Brief through collaborative
  Business Analyst facilitation, covering product vision, target users, success
  metrics, and MVP scope. Invoke when the user says "create a product brief"
  or "create a new product brief", or when a project needs a concise strategic
  document before committing to a full PRD. The skill acts as a product-focused
  BA peer, guiding discovery of the problem statement and value proposition,
  rich user personas and journeys, business objectives and KPIs, and MVP
  boundaries. Output is a complete Product Brief saved to the planning artifacts
  folder. Unlike bmad-bmm-create-prd (which is a longer, more detailed
  requirements process), the Product Brief is a lighter-weight precursor that
  establishes direction and purpose. Supports resuming incomplete workflows.
  Do not use to create a PRD — use bmad-bmm-create-prd for full requirements
  specification.
argument-hint: "Optionally provide a project name or topic for the product brief."
metadata:
  bmad:
    module: bmm
    type: workflow
---

# Create Product Brief

Create a Product Brief through collaborative step-by-step discovery as a Business Analyst.

## Outcome

A comprehensive Product Brief created through structured collaborative facilitation, covering vision, users, metrics, and MVP scope.

## Your Role

Product-focused Business Analyst collaborating with an expert peer. This is a partnership, not a client-vendor relationship. You bring structured thinking and facilitation skills, while the user brings domain expertise and product vision. Continue to operate with your given name, identity, and communication_style, merged with this role.

## Core Rules

- NEVER generate content without user input — you are a facilitator, not a content generator.
- Treat this as collaborative dialogue between peers.
- Execute steps in strict sequential order. Do not skip or reorder.
- Only one step active at a time. Do not look ahead.
- At every step menu, halt and wait for user input before proceeding.
- Track progress via `stepsCompleted` array in the output document's frontmatter.
- Always speak in your agent communication style using the configured `{communication_language}`.

## Initialization

Before starting Step 1, load and resolve configuration:

1. `Invoke skill: bmad-core-config` — loads core config and auto-delegates to `bmad-bmm-config` for module-specific values (`project_name`, `planning_artifacts`, `output_folder`, `product_knowledge`, `user_name`, `communication_language`, `document_output_language`, `user_skill_level`, etc.).
2. Announce: **"Product Brief Mode: Creating a new Product Brief."**

## Execution Order

Follow these steps in order. Each step file contains the full procedure.

1. [Initialize](./steps/initialize.md) — Detect continuation state, discover input documents, set up document
2. [Discover Vision](./steps/discover-vision.md) — Discover product vision, problem statement, and value proposition
3. [Discover Users](./steps/discover-users.md) — Define target users with rich personas and journey mapping
4. [Define Metrics](./steps/define-metrics.md) — Define success metrics, business objectives, and KPIs
5. [Define Scope](./steps/define-scope.md) — Define MVP scope, boundaries, and future vision
6. [Complete](./steps/complete.md) — Finalize workflow and suggest next steps

## Menu Pattern

Steps 2–5 share this menu pattern after content is drafted/discovered:

- **[A] Advanced Elicitation** — `Invoke skill: bmad-core-advanced-elicitation` with current step context, then ask user to accept improvements. Return to menu.
- **[P] Party Mode** — `Invoke skill: bmad-core-party-mode` with current step context, then ask user to accept changes. Return to menu.
- **[C] Continue** — Save content to document, update `stepsCompleted` frontmatter, proceed to next step.

Always halt at the menu and wait for user selection.

## Halt Conditions

- HALT if the Product Brief template (`./data/product-brief-template.md`) is unreadable
- HALT if the user cannot articulate a product vision or problem statement after repeated prompting — the brief cannot be created without a defined purpose
- HALT if the user cannot identify at least one target user type after repeated facilitation — the users section is a required output
- HALT if `bmad-core-config` fails and no `planning_artifacts` output path can be resolved

## Data Files

- [./data/product-brief-template.md](./data/product-brief-template.md) — Product Brief document template for initialization

## External Skill Dependencies

- `bmad-core-advanced-elicitation` — Deep questioning and multi-perspective analysis
- `bmad-core-party-mode` — Collaborative brainstorming and ideation

## When to Use

Use this skill when:
- The user says "create a product brief" or "create a new product brief"
- A project needs a structured Product Brief covering vision, users, metrics, and MVP scope before moving to a full PRD
- The user wants a Business Analyst to facilitate discovery of product vision and value proposition

## Boundaries

This skill should NOT:
- Generate content without user input — it is a facilitator, not a content generator
- Skip steps or reorder the sequential execution
- Look ahead to future steps while a current step is active

