---
name: bmad-bmm-dev-story
description: >-
  Use this skill to autonomously execute the full implementation of a story
  from start to finish, following a context-rich story spec file without
  stopping mid-way. Invoke when the user says "dev this story", "implement the
  next story in the sprint plan", or when a story file has been prepared by
  bmad-bmm-create-story and is in ready-for-dev status. The skill discovers
  the target story, loads project context, marks it in-progress, then
  implements every task using a red-green-refactor cycle with inline validation
  until all acceptance criteria are satisfied and the story status is set to
  "review". Input is a story file path or auto-discovery from sprint status.
  Output is completed, tested code with an updated story and sprint status file.
  Unlike bmad-bmm-quick-dev (for small spec-driven tasks), this skill operates
  within the full BMAD story-and-sprint workflow. Do not stop for "milestones"
  or "session boundaries" unless a true blocking halt condition is triggered.
argument-hint: "Optionally provide a path to the story file to implement."
metadata:
  bmad:
    module: bmm
    type: workflow
---

# Dev Story

Execute story implementation following a context-filled story spec file.

## Outcome

A fully implemented story with all tasks completed, tests passing, file list updated, and story status set to "review" — ready for code review.

## Your Role

Developer implementing the story. Continue to operate with your given name, identity, and communication_style, merged with this role.

## Core Rules

- Only modify the story file in these areas: Tasks/Subtasks checkboxes, Dev Agent Record (Debug Log, Completion Notes), File List, Change Log, and Status.
- Execute ALL steps in exact order; do NOT skip steps.
- Absolutely DO NOT stop because of "milestones", "significant progress", or "session boundaries". Continue in a single execution until the story is COMPLETE (all ACs satisfied and all tasks/subtasks checked) UNLESS a HALT condition is triggered or the USER gives other instruction.
- Do NOT schedule a "next session" or request review pauses unless a HALT condition applies.
- User skill level (`{user_skill_level}`) affects conversation style ONLY, not code updates.
- Always communicate in `{communication_language}` and generate documents in `{document_output_language}`.

## Initialization

Before starting Step 1, load and resolve configuration:

1. `Invoke skill: bmad-core-config` — loads core config and auto-delegates to `bmad-bmm-config` for module-specific values (`project_name`, `user_name`, `communication_language`, `document_output_language`, `user_skill_level`, `implementation_artifacts`, etc.).
2. Set `date` as system-generated current datetime.
3. Set `story_file` from user argument if provided (auto-discovered if empty).
4. Set `sprint_status` = `{implementation_artifacts}/sprint-status.yaml`.

## Execution Order

Follow these steps in order. Each step file contains the full procedure.

1. [Discover Story](./steps/discover-story.md) — Find the next ready story and load it
2. [Load Context](./steps/load-context.md) — Load project context and detect review continuation state
3. [Mark In-Progress](./steps/mark-in-progress.md) — Update sprint status to in-progress
4. [Implement Tasks](./steps/implement-tasks.md) — Red-green-refactor cycle for each task/subtask with inline validation
5. [Complete Story](./steps/complete-story.md) — Final validation, status update, and user communication

## Halt Conditions

- HALT if no story file can be found and auto-discovery from `{implementation_artifacts}/sprint-status.yaml` yields no ready-for-dev stories
- HALT if the story file exists but has no tasks or acceptance criteria — implementation cannot proceed without a defined scope
- HALT if a blocking dependency (e.g., a prerequisite story) is not yet complete and the user cannot resolve it
- HALT if a task cannot be implemented due to a hard technical blocker (e.g., a required external API is unavailable or auth credentials are missing) and the user cannot provide a workaround

## Data Files

- [./data/definition-of-done-checklist.md](./data/definition-of-done-checklist.md) — Enhanced Definition of Done validation checklist

## External Skill Dependencies

- `bmad-bmm-create-story` — Referenced when no ready-for-dev stories found
- `bmad-bmm-code-review` — Suggested as next step after story completion

## When to Use

Use this skill when:
- The user says "dev this story [story file]" or "implement the next story in the sprint plan"
- A story file has been created by `bmad-bmm-create-story` and is in "ready-for-dev" status
- The dev agent needs to execute story implementation following a context-filled story spec file

## Boundaries

This skill should NOT:
- Stop mid-implementation because of "milestones", "significant progress", or "session boundaries" — continue until the story is COMPLETE unless a HALT condition is triggered
- Schedule a "next session" or request review pauses unless a HALT condition applies
- Modify story files outside of: Tasks/Subtasks checkboxes, Dev Agent Record, File List, Change Log, and Status
- Skip steps or reorder the execution sequence

