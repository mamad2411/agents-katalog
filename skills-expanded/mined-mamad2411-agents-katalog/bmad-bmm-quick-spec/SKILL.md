---
name: bmad-bmm-quick-spec
description: >-
  Use this skill to quickly create a complete, implementation-ready technical
  specification for a small feature or change through conversational discovery
  and codebase investigation. Invoke when the user says "create a quick spec",
  "generate a quick tech spec", or when a small change needs a self-contained
  spec before implementation begins. The skill understands the requirement delta
  (current state vs. desired state), investigates the codebase to map technical
  constraints and anchor points, generates a full implementation plan with
  Given/When/Then acceptance criteria and dependency-ordered tasks, then reviews
  and finalizes. Output is a tech-spec file with no placeholders — ready for a
  fresh dev agent to implement without reading the workflow history. Unlike
  bmad-bmm-quick-dev (which implements), this skill only produces the spec.
  Unlike bmad-bmm-create-story (which is for full BMAD stories), this is a
  lighter-weight path for small changes. Do not use for multi-story features.
argument-hint: "Optionally provide a feature name, requirement, or path to existing planning documents."
metadata:
  bmad:
    module: bmm
    type: workflow
---

# Quick Spec

Very quick process to create implementation-ready quick specs for small changes or features.

## Outcome

An implementation-ready technical specification created through conversational discovery, code investigation, and structured documentation — complete enough that a fresh dev agent can implement the feature without reading the workflow history.

## Your Role

Elite developer and spec engineer. You ask sharp questions, investigate existing code thoroughly, and produce specs that contain ALL context a fresh dev agent needs to implement the feature. No handoffs, no missing context — just complete, actionable specs. Continue to operate with your given name, identity, and communication_style, merged with this role.

## Core Rules

- NEVER generate content without user input — you are a facilitator, not a content generator.
- Execute steps in strict sequential order. Do not skip or reorder.
- Only one step active at a time. Do not look ahead.
- At every step menu, halt and wait for user input before proceeding.
- Track progress via `stepsCompleted` array in the output document's frontmatter.
- Always speak in your agent communication style using the configured `{communication_language}`.

## Ready for Development Standard

A specification is considered "Ready for Development" ONLY if it meets the following:

- **Actionable**: Every task has a clear file path and specific action.
- **Logical**: Tasks are ordered by dependency (lowest level first).
- **Testable**: All ACs follow Given/When/Then and cover happy path and edge cases.
- **Complete**: All investigation results from Step 2 are inlined; no placeholders or "TBD".
- **Self-Contained**: A fresh agent can implement the feature without reading the workflow history.

## Initialization

Before starting Step 1, load and resolve configuration:

1. `Invoke skill: bmad-core-config` — loads core config and auto-delegates to `bmad-bmm-config` for module-specific values (`project_name`, `planning_artifacts`, `implementation_artifacts`, `user_name`, `communication_language`, `document_output_language`, `user_skill_level`, etc.).
2. Resolve:
   - `date` as system-generated current datetime
   - `project_context` = `**/project-context.md` (load if exists)

## Execution Order

Follow these steps in order. Each step file contains the full procedure.

1. [Understand](./steps/understand.md) — Analyze the requirement delta between current state and what user wants to build
2. [Investigate](./steps/investigate.md) — Map technical constraints and anchor points within the codebase
3. [Generate](./steps/generate.md) — Build the implementation plan based on the technical mapping
4. [Review](./steps/review.md) — Review and finalize the tech-spec

## Menu Pattern

Steps 1–2 share this menu pattern after content is drafted:

- **[A] Advanced Elicitation** — `Invoke skill: bmad-core-advanced-elicitation` with current step context, then ask user to accept improvements. Return to menu.
- **[P] Party Mode** — `Invoke skill: bmad-core-party-mode` with current step context, then ask user to accept changes. Return to menu.
- **[C] Continue** — Save content, update `stepsCompleted` frontmatter, proceed to next step.

Always halt at the menu and wait for user selection.

## Halt Conditions

- HALT if the user cannot describe a feature, change, or requirement after repeated prompting — a spec cannot be written without a defined target
- HALT if codebase investigation reveals no anchor points or existing code that the new feature can integrate with and the user cannot clarify the integration path
- HALT if the tech spec template (`./data/tech-spec-template.md`) is unreadable
- HALT if the generated spec still contains unresolvable placeholders or TBDs after the investigation step — the spec must be fully actionable before leaving this skill

## Data Files

- [./data/tech-spec-template.md](./data/tech-spec-template.md) — Tech spec document template for initialization

## External Skill Dependencies

- `bmad-core-advanced-elicitation` — Deep questioning and multi-perspective analysis
- `bmad-core-party-mode` — Collaborative brainstorming and ideation
- `bmad-bmm-quick-dev` — Implementation workflow (offered at completion)
- `bmad-core-review-adversarial-general` — Adversarial review of spec (offered at completion)

## When to Use

Use this skill when:
- The user says "create a quick spec" or "generate a quick tech spec"
- A small change or feature needs an implementation-ready technical specification created through conversational discovery and code investigation
- The user wants a complete spec that a fresh dev agent can implement without reading the workflow history

## Boundaries

This skill should NOT:
- Implement any code — its output is the tech-spec file only; hand off to `bmad-bmm-quick-dev` or `bmad-bmm-quick-dev-new-preview` for implementation
- Be used for multi-story features — it is for small, bounded changes; use the full BMAD epic/story workflow for anything spanning multiple stories
- Produce a spec with placeholders, TBDs, or unresolved anchor points — the spec must be fully self-contained and actionable before leaving this skill
- Generate content without user input — all scope, constraints, and preferences must be confirmed through conversational discovery
- Skip the codebase investigation step — the spec must be grounded in actual code findings, not assumptions

