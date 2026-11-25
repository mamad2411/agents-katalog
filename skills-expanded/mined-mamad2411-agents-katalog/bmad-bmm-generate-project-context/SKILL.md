---
name: bmad-bmm-generate-project-context
description: >-
  Use this skill to collaboratively generate a project-context.md file
  containing the critical AI implementation rules, coding patterns, and
  guidelines that development agents must follow to produce consistent,
  high-quality code on a project. Invoke when the user says "generate project
  context" or "create project context", or when a project needs to capture
  unobvious technical rules before development begins. The skill discovers the
  existing tech stack and patterns, then guides the user through defining rules
  category by category (naming conventions, architecture patterns, anti-
  patterns, tooling requirements, etc.) while keeping content lean and
  optimized for LLM context consumption. Output is a project-context.md in the
  output folder. Unlike bmad-bmm-document-project (which generates descriptive
  docs about what the project does), this skill produces prescriptive rules for
  how AI agents should implement code. Do not use for writing narrative
  documentation about existing code.
argument-hint: "Optionally provide a project name or path to focus the context generation."
metadata:
  bmad:
    module: bmm
    type: workflow
---

# Generate Project Context

Create project-context.md with AI rules, patterns, and guidelines.

## Outcome

A concise, optimized `project-context.md` file containing critical rules, patterns, and guidelines that AI agents must follow when implementing code. Focused on unobvious details that LLMs need to be reminded of.

## Your Role

Technical facilitator working with a peer to capture the essential implementation rules that will ensure consistent, high-quality code generation across all AI agents working on the project. Continue to operate with your given name, identity, and communication_style, merged with this role.

## Core Rules

- NEVER generate content without user input — you are a facilitator, not a content generator.
- Treat this as collaborative discovery between technical peers.
- Execute steps in strict sequential order. Do not skip or reorder.
- Only one step active at a time. Do not look ahead.
- At every step menu, halt and wait for user input before proceeding.
- Keep content lean — optimize for LLM context efficiency.
- Always speak in your agent communication style using the configured `{communication_language}`.

## Initialization

Before starting Step 1, load and resolve configuration:

1. `Invoke skill: bmad-core-config` — loads core config and auto-delegates to `bmad-bmm-config` for module-specific values (`project_name`, `output_folder`, `user_name`, `communication_language`, `document_output_language`, `user_skill_level`, etc.).
2. Resolve:
   - `date` as system-generated current datetime
   - `template_path` = `./data/project-context-template.md`
   - `output_file` = `{output_folder}/project-context.md`

## Execution Order

Follow these steps in order. Each step file contains the full procedure.

1. [Discover](./steps/discover.md) — Context discovery and initialization: detect existing context, discover tech stack, identify patterns, initialize document
2. [Generate](./steps/generate.md) — Collaboratively generate specific context rules per category with A/P/C menus
3. [Complete](./steps/complete.md) — Review, optimize for LLM efficiency, finalize the document

## Menu Pattern

Step 2 presents this menu after each rule category is drafted:

- **[A] Advanced Elicitation** — `Invoke skill: bmad-core-advanced-elicitation` with current category context, then ask user to accept improvements. Return to menu.
- **[P] Party Mode** — `Invoke skill: bmad-core-party-mode` with current category context, then ask user to accept changes. Return to menu.
- **[C] Continue** — Save the current rules and proceed to next category.

Always halt at the menu and wait for user selection.

## Halt Conditions

- HALT if the project context template (`./data/project-context-template.md`) is unreadable
- HALT if the user cannot identify any technology stack, framework, or implementation patterns after repeated prompting — the context file requires at least one concrete rule to be useful
- HALT if `bmad-core-config` fails and no `output_folder` can be resolved for writing the output file

## Data Files

- [./data/project-context-template.md](./data/project-context-template.md) — Project context document template

## External Skill Dependencies

- `bmad-core-advanced-elicitation` — Deep questioning and multi-perspective analysis
- `bmad-core-party-mode` — Collaborative brainstorming and ideation

## When to Use

Use this skill when:
- The user says "generate project context" or "create project context"
- The project needs a `project-context.md` file with AI rules, patterns, and guidelines
- The user wants to capture critical implementation rules that ensure consistent, high-quality code generation across all AI agents

## Boundaries

This skill should NOT:
- Generate narrative documentation describing what the project does — use `bmad-bmm-document-project` for that; this skill produces prescriptive rules for how AI agents must implement code
- Generate rules without user input — all rule categories must be confirmed by the user before being saved to the output file
- Generate verbose content — every rule must be lean and optimized for LLM context efficiency; unnecessary elaboration reduces the file's usefulness
- Skip steps or reorder the sequential execution — discovery must precede generation, and generation must precede the optimization review
- Write rules for features or patterns that have not been confirmed to exist in the project

