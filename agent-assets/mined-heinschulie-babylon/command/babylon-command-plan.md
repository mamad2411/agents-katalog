# Plan

Create a plan to complete the task using the specified markdown `Plan Format`. Research the codebase and create a thorough plan appropriate to the task's complexity.

## Variables

adw_id: $1
prompt: $2

## Instructions

- If the adw_id or prompt is not provided, stop and ask the user to provide them.
- IMPORTANT: Create a plan to complete the task described in the `prompt`
- The plan should be appropriately detailed based on the task complexity:
- Simple tasks (chores, fixes): Focus on specific changes and validation
- Complex tasks (features, refactors): Include design, phases, and testing strategy
- Create the plan in the `temp/specs/` directory with filename: `plan-{adw_id}-{descriptive-name}.md`
- Replace `{descriptive-name}` with a short, descriptive name based on the task (e.g., "update-readme", "add-logging", "implement-api", "refactor-agent")
- Research the codebase starting with `README.md`
- IMPORTANT: When you finish your plan, return only the path to the plan file created.
- IMPORTANT: Replace every <placeholder> in the `Plan Format` with the requested value
- IMPORTANT: Include the current conversation ID in the plan's Metadata section as `conversation_id`. This allows humans or agents to trace back to the conversation that spawned the plan.
- Use your reasoning model: ULTRATHINK about the task requirements and appropriate level of planning needed
- Follow existing patterns and conventions in the codebase

## Codebase Structure

- `README.md` - Project overview and instructions (start here)
- `adws/` - AI Developer Workflow scripts and modules
- `apps/` - Application layer you'll be working in
- `.claude/commands/` - Claude command templates
- `temp/specs/` - Specification and plan documents

## Plan Format

```md
# Plan: <task name>

## Metadata

adw_id: `{adw_id}`
prompt: `{prompt}`
conversation_id: `{conversation_id}`
task_type: <chore|feature|refactor|fix|enhancement>
complexity: <simple|medium|complex>

## Task Description

<describe the task in detail based on the prompt>

## Objective

<clearly state what will be accomplished when this plan is complete>

<if task_type is feature or complexity is medium/complex, include these sections:>

## Problem Statement

<clearly define the specific problem or opportunity this task addresses>

## Solution Approach

<describe the proposed solution approach and how it addresses the objective>
</if>

## Relevant Files

Use these files to complete the task:

<list files relevant to the task with bullet points explaining why. Include new files to be created under an h3 'New Files' section if needed>

<if complexity is medium/complex, include this section:>

## Implementation Phases

### Phase 1: Foundation

<describe any foundational work needed>

### Phase 2: Core Implementation

<describe the main implementation work>

### Phase 3: Integration & Polish

<describe integration, testing, and final touches>
</if>

## Step by Step Tasks

IMPORTANT: Execute every step in order, top to bottom.

<list step by step tasks as h3 headers with bullet points. Start with foundational changes then move to specific changes. Last step should validate the work>

### 1. <First Task Name>

- <specific action>
- <specific action>

### 2. <Second Task Name>

- <specific action>
- <specific action>

<continue with additional tasks as needed>

<if task_type is feature or complexity is medium/complex, include this section:>

## Testing Strategy

<describe testing approach, including unit tests and edge cases as applicable>
</if>

## Acceptance Criteria

<list specific, measurable criteria that must be met for the task to be considered complete>

## Validation Commands

Execute these commands to validate the task is complete:

<list specific commands to validate the work. Be precise about what to run>
- Example: `bun run check` - Run svelte-check to validate types across all apps

## Notes

<optional additional context, considerations, or dependencies. If new libraries are needed, specify using `bun add`>
```

## Task

Use the task description from the `prompt` variable.

## Report

IMPORTANT: Exclusively return the path to the plan file created.

## Step Summary

IMPORTANT: You MUST end your output with this exact block. Fill in each field with a single line.

## Step Summary
- status: pass | fail
- action: <one line describing what you did>
- decision: <one line -- key choice and why>
- blockers: <one line, or "none">
- files_changed: <comma-separated list, or "none">
