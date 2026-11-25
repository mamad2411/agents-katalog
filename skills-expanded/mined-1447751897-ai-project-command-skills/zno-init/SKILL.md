---
name: zno-init
description: Use when the user writes /zno-init or wants to start a new software project from a requirement description. Clarifies the goal, scaffolds AI_DEVELOPMENT_RULES.md and core project docs, captures the frontend design direction and design tokens, and waits for user confirmation before any implementation.
---

# Zno-Init — Project Initialization

Document-first kickoff: clarify requirements, scaffold and fill core docs, confirm direction, only then implement.

This skill directory also hosts the shared resources for the whole zno-* command family:

- `references/` — shared rules other zno-* commands read on demand
- `assets/project-template/` — the project doc templates
- `scripts/init_project_docs.py` — the doc scaffolder

`<skills-root>` below means the directory containing all zno-* skills (e.g. `~/.claude/skills` or `~/.agents/skills`).

## Workflow

1. Inspect the workspace for existing docs and project files.
2. If core docs are missing, scaffold the essential set only:

   ```bash
   python <skills-root>/zno-init/scripts/init_project_docs.py <project-root>
   ```

   Progressive mode creates `AI_DEVELOPMENT_RULES.md` plus requirements, roadmap, frontend design (+tokens), development principles, and the docs README. All other docs are scaffolded on demand when later commands first need them. Use `--full` to generate everything at once; use `--overwrite` only if the user explicitly asks to replace existing docs.
3. Read `AI_DEVELOPMENT_RULES.md` and `docs/00_START_HERE.md`.
4. Restate the user's project goal in plain language.
5. Ask only the clarification questions that affect product scope, architecture, data, permissions, deployment, frontend design direction, or acceptance.
6. If the project has any user interface: identify the surface (website, mini program, browser extension, app, desktop app, internal tool, admin system, dashboard, other); collect or recommend 2-5 UI style references; record overall mood, colors, layout, card/component style, interaction states, and things to avoid in `docs/product/15-frontend-design.md`; generate initial token values in `docs/product/15-frontend-design-tokens.json`.
7. After the user confirms, fill or update the docs under `docs/`.
8. Do not start implementation until the requirements and initial docs are confirmed.

## Rules

- Never invent unknown business rules. Record open questions in the requirements doc and ask the smallest useful question.
- Major technology choices go through the technical selection gate: read `references/tech-gate.md`, present 2-3 options, wait for confirmation, record in `docs/engineering/04-tech-decisions.md`.
- Once this skill has been used in a project, treat the document-first loop as a standing agreement: later requests follow the matching zno-* command workflow without the user re-pasting any kickoff prompt.

## Shared references (read only when needed)

- `<skills-root>/zno-init/references/docs-map.md` — full doc set, doc update rules, scaffold triggers.
- `<skills-root>/zno-init/references/tech-gate.md` — technical selection gate and performance-aware design.
- `<skills-root>/zno-init/references/verification.md` — verification gate and final-response page test steps.
