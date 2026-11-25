---
name: planning-with-files
description: Implements file-based planning for complex tasks, creating persistent working memory (task_plan.md, findings.md) to manage goals, research, and progress.
allowed-tools:
- Read
- Write
- Edit
- Glob
- Grep
metadata:
  version: 0.2.0
  category: workflow
---
# Planning with Files

## Quick Start
```bash
# Create initial planning files
touch task_plan.md findings.md progress.md
```

## Workflow
1. **Initialize**: Create `task_plan.md` with goals, phases, and key questions.
2. **Research**: Document discoveries and decisions in `findings.md` every 2-3 tool calls.
3. **Execute**: Log progress, test results, and file changes in `progress.md`.
4. **Iterate**: Re-read the plan before major decisions and update after each phase.

## Rules & Constraints
- **RULE-1**: Never start a complex task (>5 steps) without a `task_plan.md`.
- **RULE-2**: Log ALL errors in `task_plan.md` with attempt numbers and resolutions.
- **RULE-3**: Multimodal content (images, browser results) must be captured as text in `findings.md` immediately.

## When to Use
- Multi-step tasks or research projects spanning >10 tool calls.
- Tasks that may span multiple sessions or require persistent memory.

## When NOT to Use
- Simple lookups or single-file edits with obvious scope.
- Tasks completable in under 5 tool calls.

## References
- [Skill Manual](references/planning-with-files-manual.md)
- [Templates](references/templates.md)
