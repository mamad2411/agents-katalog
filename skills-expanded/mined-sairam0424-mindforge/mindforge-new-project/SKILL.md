---
name: "mindforge-new-project"
description: "Initialize a new project with deep context gathering and PROJECT.md"
---

<context>
**Flags:**
- `--auto` — Automatic mode. After config questions, runs research → requirements → roadmap without further interaction. Expects idea document via @ reference.
</context>

<objective>
Initialize a new project through unified flow: questioning → research (optional) → requirements → roadmap.

**Creates:**
- `.planning/PROJECT.md` — project context
- `.planning/config.json` — workflow preferences
- `.planning/research/` — domain research (optional)
- `.planning/REQUIREMENTS.md` — scoped requirements
- `.planning/ROADMAP.md` — phase structure
- `.planning/STATE.md` — project memory

**After this command:** Run `/mindforge-plan-phase 1` to start execution.
</objective>

<execution_context>
@.agent/workflows/mindforge-new-project.md
@docs/References/questioning.md
@docs/References/ui-brand.md
@docs/Templates/Project/PROJECT.md
@docs/Templates/Project/REQUIREMENTS.md
</execution_context>

<process>
Execute the new-project workflow from @.agent/workflows/mindforge-new-project.md end-to-end.
Preserve all workflow gates (validation, approvals, commits, routing).
</process>
