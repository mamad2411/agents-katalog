---
name: cds-explore
description: "Socratic ideation and idea routing — think through ideas before committing to plans"
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Task
  - AskUserQuestion
---

<objective>
Open-ended Socratic ideation session. Guides the developer through exploring an idea via
probing questions, optionally spawns research, then routes outputs to the appropriate GSD
artifacts (notes, todos, seeds, research questions, requirements, or new phases).

Accepts an optional topic argument: `/cds-explore authentication strategy`
</objective>

<execution_context>
@$HOME/.claude/cds-workflow/workflows/explore.md
</execution_context>

<process>
Execute the explore workflow from @$HOME/.claude/cds-workflow/workflows/explore.md end-to-end.
</process>
