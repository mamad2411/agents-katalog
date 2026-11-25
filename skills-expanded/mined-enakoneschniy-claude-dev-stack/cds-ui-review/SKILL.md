---
name: cds-ui-review
description: "Retroactive 6-pillar visual audit of implemented frontend code"
argument-hint: "[phase]"
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - Task
  - AskUserQuestion
---

<objective>
Conduct a retroactive 6-pillar visual audit. Produces UI-REVIEW.md with
graded assessment (1-4 per pillar). Works on any project.
Output: {phase_num}-UI-REVIEW.md
</objective>

<execution_context>
@$HOME/.claude/cds-workflow/workflows/ui-review.md
@$HOME/.claude/cds-workflow/references/ui-brand.md
</execution_context>

<context>
Phase: $ARGUMENTS — optional, defaults to last completed phase.
</context>

<process>
Execute @$HOME/.claude/cds-workflow/workflows/ui-review.md end-to-end.
Preserve all workflow gates.
</process>
