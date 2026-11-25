---
name: zno-retro
description: Use when the user writes /zno-retro or wants to conduct a retrospective after completing a project phase or milestone. Compares original plan vs actual outcome, identifies lessons learned, extracts reusable rules, and writes findings to docs/development/16-retrospective.md. Generalizable lessons are appended to AI_DEVELOPMENT_RULES.md.
---

# Zno-Retro — Retrospective

Extract lessons after a phase, milestone, or the whole project, so the next project benefits automatically.

`<skills-root>` below means the directory containing all zno-* skills (e.g. `~/.claude/skills` or `~/.agents/skills`).

## Workflow

1. Read what was planned vs what happened (skip files that don't exist):
   - `docs/product/06-roadmap.md` (original plan)
   - `docs/development/03-feature-changelog.md` (what was actually built)
   - `docs/development/10-current-status.md` (current state)
   - `docs/engineering/04-tech-decisions.md` (technical choices)
   - `docs/development/14-decision-log.md` (autonomous decisions)
2. Ask the user 3 reflection questions:
   - What went better than expected?
   - What was harder than expected or went wrong?
   - If you could restart this phase, what would you do differently?
3. If `docs/development/16-retrospective.md` does not exist yet, scaffold it first:

   ```bash
   python <skills-root>/zno-init/scripts/init_project_docs.py <project-root> --scaffold retro
   ```

4. Synthesize findings into the retrospective doc:

   ```markdown
   ## Retrospective: [Phase / Milestone]

   ### What Went Well
   - ...

   ### What Went Wrong
   - ...

   ### Reusable Rules (candidates for AI_DEVELOPMENT_RULES.md)
   - ...

   ### Action Items for Next Phase
   - ...
   ```

5. If any lesson is generalizable (not project-specific), ask the user whether to append it to `AI_DEVELOPMENT_RULES.md` in the "可选项目定制区" section.
6. Update `docs/development/10-current-status.md` to reflect that the retrospective was completed.

## Shared references (read only when needed)

- `<skills-root>/zno-init/references/docs-map.md` — full doc set, doc update rules, scaffold triggers.
