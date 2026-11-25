---
name: bmad-core-help
description: >-
  Use this skill to guide users to the next recommended BMAD workflow based on
  current project state, active module, and completed artifacts. Invoke when
  the user says "what should I do next", "help me navigate", or "bmad help", or
  when another skill needs to recommend next steps after completing a workflow.
  The skill loads a help catalog CSV, detects the active BMAD module, and
  resolves output artifact paths to infer which phases have been completed.
  Recommendations are sorted by phase and sequence, with required workflows
  blocking progress until completed. Universal tools with no phase assignment
  are always available. Display format varies by workflow type: command-based
  skills are shown as skill invocations, agent-based workflows prompt the user
  to load the agent first. All output is presented in the configured
  communication language. Each recommended workflow runs best in a fresh context
  window; validation workflows benefit from a different high-quality LLM when
  available.
argument-hint: "Optionally provide the workflow name or code just completed, or a conversational description of current state."
metadata:
  bmad:
    module: core
    type: task
---

# BMAD Help

Guide users to the next recommended workflow based on current project state.

## Outcome

Clear, prioritized next-step recommendations based on the user's current project state, active module, and completed workflows.

## Core Rules

- Stay in the active module — guide through the module's workflow based on phase+sequence ordering.
- Required workflows must complete before proceeding to later phases.
- Artifacts reveal completion — search resolved output paths for `outputs` patterns.
- Present all output in `{communication_language}`.
- Recommend running each workflow in a fresh context window.
- For validation workflows, recommend using a different high-quality LLM if available.

## Execution Order

Follow these steps in order.

1. [Load and Resolve](./steps/load-and-resolve.md) — Load help catalog CSV, resolve config and output locations, detect active module
2. [Analyze Input](./steps/analyze-input.md) — Determine what was just completed, infer state from context and artifacts
3. [Present Recommendations](./steps/present-recommendations.md) — Show next steps with proper display formatting

## Routing Rules

- Empty `phase` = anytime — universal tools work regardless of workflow state.
- Numbered phases indicate sequence — phases flow in order.
- Phase with no required items — entire phase is optional. If sequentially before another phase, it can be recommended, but always be clear about the true next required item.
- `required=true` blocks progress — required workflows must complete before proceeding.
- Descriptions contain routing — read for alternate paths.

## Display Rules

### Command-Based Workflows
When `command` field has a value: show the command as a skill name in backticks.

### Skill-Referenced Workflows
When `workflow-file` starts with `skill:`: display using the `command` column value as a skill name. Do NOT resolve as a file path.

### Agent-Based Workflows
When `command` field is empty: user loads agent first by invoking the agent skill, then invokes by referencing the `code` field.

## Halt Conditions

- HALT if the help catalog CSV cannot be loaded — no workflow recommendations can be offered without it
- HALT if the active module cannot be determined and the user cannot clarify which BMAD module they are using
- HALT if no output paths can be resolved to detect artifact presence — phase completion cannot be inferred

## When to Use

Use this skill when:
- The user says "what should I do next", "help me navigate", or "bmad help"
- Another skill invokes it to recommend next steps after completing a workflow
- The user has completed a workflow and needs guidance on what phase or workflow comes next in the BMAD process

