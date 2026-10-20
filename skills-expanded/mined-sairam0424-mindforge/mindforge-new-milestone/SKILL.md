---
name: "mindforge-new-milestone"
description: "Start a new milestone cycle — update PROJECT.md and route to requirements"
---

<objective>
Start a new milestone: questioning → research (optional) → requirements → roadmap.

Brownfield equivalent of new-project. Project exists, PROJECT.md has history. Gathers "what's next", updates PROJECT.md, then runs requirements → roadmap cycle.

**Creates/Updates:**
- `.planning/PROJECT.md` — updated with new milestone goals
- `.planning/research/` — domain research (optional, NEW features only)
- `.planning/REQUIREMENTS.md` — scoped requirements for this milestone
- `.planning/ROADMAP.md` — phase structure (continues numbering)
- `.planning/STATE.md` — reset for new milestone

**After:** `/mindforge-plan-phase [N]` to start execution.
</objective>

<execution_context>
@.agent/workflows/mindforge-new-milestone.md
@docs/References/questioning.md
@docs/References/ui-brand.md
@docs/Templates/Project/PROJECT.md
@docs/Templates/Project/REQUIREMENTS.md
</execution_context>

<context>
Milestone name: $ARGUMENTS (optional - will prompt if not provided)

Project and milestone context files are resolved inside the workflow (`init new-milestone`) and delegated via `<files_to_read>` blocks where subagents are used.
</context>

<process>
Execute the new-milestone workflow from @.agent/workflows/mindforge-new-milestone.md end-to-end.
Preserve all workflow gates (validation, questioning, research, requirements, roadmap approval, commits).
</process>
