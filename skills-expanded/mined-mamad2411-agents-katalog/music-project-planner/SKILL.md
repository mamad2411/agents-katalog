---
name: music-project-planner
description: Plans music production and release projects with milestones, task breakdowns, and Obsidian integration.
category: media
tags: [media, music, production, planning, project-management, obsidian]
agents: [opencode, freebuff, antigravity, codex]
---

# music-project-planner

## Purpose

Structures music production projects (EP, album, single, DJ mix release) into phased plans with milestones, task lists, and deadlines. Integrates with Obsidian project notes and links to relevant media skills.

## Invocation

**OpenCode / Codex:** `Invoke music-project-planner`
**Freebuff:** `/skill music-project-planner`

## Workflow Steps

1. **Define project:** Type (EP, album, live set, remix), target release date, scope.
2. **Phase:** Break into phases (Concept, Production, Mixing, Mastering, Release, Promotion).
3. **Tasks:** Generate task list per phase with estimated effort.
4. **Schedule:** Map tasks to calendar with buffer time.
5. **Save:** Write project plan to Obsidian under `Projects/Music/project-title.md`.
6. **Track:** Set up progress checkboxes and milestone markers.

## Inputs

- Project type (EP, album, single, remix, live set)
- Target release date and scope description
- Optional: existing partial plan or notes to incorporate

## Outputs

- Phased project plan saved to `Projects/Music/project-title.md` in Obsidian
- Task list per phase with effort estimates and calendar schedule
- Progress checkboxes and milestone markers

## Safety

- Creates planning documents only; no audio file modifications.
- Never auto-submit releases to streaming platforms.

## Failure Modes

- Incomplete project scope — prompt user to clarify before generating phases.
- Obsidian vault unreachable — output plan as plain Markdown for manual paste.

## References

- [Obsidian Tasks plugin](https://publish.obsidian.md/tasks/)
- [LANDR mastering guide](https://blog.landr.com/)

## Companion Skills

- `dj-set-architect`, `dj-mix-documentarian`, `obsidian-music-journal`, `music-listening-journal`
