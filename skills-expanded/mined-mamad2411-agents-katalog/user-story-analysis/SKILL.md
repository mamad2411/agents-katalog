---
name: user-story-analysis
description: Analyze and decompose user stories into implementable tasks. Use
  when splitting stories for development.
metadata:
  tags: user, story, analysis
---

# User Story Analysis

## Use this skill when
- Decomposing a user story into tasks and sub-features
- Identifying story dependencies and sequencing
- Determining readiness criteria before starting work

## Do not use this skill when
- Requirements are at the epic/PRD level (use requirements-analysis)
- You need acceptance criteria only (use acceptance-criteria)

## Instructions
1. Restate the story in one sentence with a clear user and goal.
2. Identify the smallest vertical slice that delivers value.
3. Break the slice into tasks: data, API, UI, tests, docs.
4. Order tasks by dependency and risk.
5. Confirm each task has a testable outcome and estimation.
6. Output a task breakdown with dependencies and estimates.

## Output Format
- Story | Slice | Tasks | Dependencies | Estimate

## Common Mistakes
- Creating horizontal slices (all UI first, no backend)
- Making tasks so small they have no independent value
- Ignoring testing and security as tasks
