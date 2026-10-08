---
name: finish-feature
allowed-tools: ["Bash(git:*)", "Read", "Write"]
description: Finalizes and merges a feature branch into develop using git-flow, then prunes stale branches and worktrees. This skill should be used when the user asks to "finish a feature", "merge feature branch", "complete feature", "git flow feature finish", or wants to finalize a feature branch.
model: haiku
argument-hint: "[feature-name]"
user-invocable: true
disable-model-invocation: true
---

## Workflow Execution

**Launch a general-purpose agent** that executes the finish-feature workflow.

Follow the pipeline in `../../references/gitflow-finish-pipeline.md`:
- **Workflow Type**: `feature`
- **Arguments**: `$ARGUMENTS`
