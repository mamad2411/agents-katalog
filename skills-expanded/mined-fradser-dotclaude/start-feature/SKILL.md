---
name: start-feature
allowed-tools: ["Bash(git:*)"]
description: Starts working on a new feature branch using git-flow. This skill should be used when the user asks to "start a feature", "create feature branch", "begin new feature", "git flow feature start", or wants to start a new feature. Accepts either a branch name or a natural-language description.
model: haiku
argument-hint: "[feature-name or description]"
user-invocable: true
disable-model-invocation: true
---

## Workflow Execution

**Launch a general-purpose agent** that executes the start-feature workflow.

Follow the pipeline in `../../references/gitflow-start-pipeline.md`:
- **Workflow Type**: `feature`
- **Arguments**: `$ARGUMENTS`
