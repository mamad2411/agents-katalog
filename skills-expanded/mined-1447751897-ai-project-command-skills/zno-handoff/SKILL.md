---
name: zno-handoff
description: Use when the user writes /zno-handoff or wants to prepare the project for another developer or AI agent to take over. Writes or updates docs/handoff/05-handoff-guide.md with entry points, common tasks, and pitfalls.
---

# Zno-Handoff — Handoff Guide

`<skills-root>` below means the directory containing all zno-* skills (e.g. `~/.claude/skills` or `~/.agents/skills`).

## Workflow

1. Inspect the project: structure, key modules, how to run it locally, current status, and known pitfalls. Read `docs/development/10-current-status.md` and `docs/engineering/11-project-structure.md` if they exist.
2. If `docs/handoff/05-handoff-guide.md` does not exist yet, scaffold it first:

   ```bash
   python <skills-root>/zno-init/scripts/init_project_docs.py <project-root> --scaffold handoff
   ```

3. Write or update the handoff guide so a newcomer (human or AI) can enter the project without asking: where to start reading, important directories, common tasks and how to do them, conventions to follow, and traps to avoid.
4. Cross-check the guide against reality: commands must actually work, paths must exist. Do not document aspirational state.
5. Keep the final response short: what was updated and what a newcomer should read first.

## Shared references (read only when needed)

- `<skills-root>/zno-init/references/docs-map.md` — full doc set, doc update rules, scaffold triggers.
