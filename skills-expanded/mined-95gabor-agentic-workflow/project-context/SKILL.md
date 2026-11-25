---
name: project-context
description: >-
  Orients agents to this repository: product goals, stack, docs index, UI
  language, and layout. Read this first for any task in this repository.
  Fill in the placeholders when adopting this template in a new project.
---

# Project Context

> **Template:** Replace bracketed placeholders below when you copy this workflow into a project.

## Product

- **Name:** [Your product name]
- **One-line purpose:** [Who it serves and what problem it solves]
- **Current focus:** [MVP / phase goals — keep short]

## UI language

- **End-user UI:** [e.g. English] — labels and copy shown to users.
- **Code and docs:** English (commits, `docs/`, code comments).

## Tech stack

| Layer           | Tech                                          | Path              |
| --------------- | --------------------------------------------- | ----------------- |
| Frontend        | [e.g. Next.js, TypeScript, Tailwind — or N/A] | [e.g. `apps/web`] |
| Backend         | [e.g. NestJS, TypeScript, Prisma — or N/A]    | [e.g. `apps/api`] |
| Database        | [e.g. PostgreSQL — or N/A]                    | —                 |
| E2E             | [e.g. Playwright — or N/A]                    | [e.g. `e2e/`]     |
| Package manager | [e.g. pnpm workspaces]                        | —                 |

Workspace package filters (if monorepo): `[e.g. @your-scope/web, @your-scope/api, @your-scope/e2e]`

If you use NestJS + Next.js, also enable the optional skills under `.agents/skills/optional/` (see root `README.md`).

## Documentation index

| Doc                            | Purpose                                   |
| ------------------------------ | ----------------------------------------- |
| `docs/PRODUCT_VISION.md`       | Vision, audience, non-goals               |
| `docs/REQUIREMENTS.md`         | Functional / non-functional requirements  |
| `docs/ARCHITECTURE.md`         | Services, modules, flows                  |
| `docs/DATA_MODEL.md`           | Entities and relationships                |
| `docs/DECISIONS.md`            | Architecture and product decision log     |
| `docs/AGENT_WORKFLOW.md`       | PM-orchestrated subagent workflow         |
| `docs/design/DESIGN_SYSTEM.md` | Brand tokens and illustration style       |
| `docs/handoffs/`               | Per-feature handoff artifacts             |
| `docs/adrs/`                   | Significant architecture decision records |

Add project-specific docs here as needed (roadmap, wireframes, domain specs).

## Repository layout

```text
[apps/web/]     # Frontend (if present)
[apps/api/]     # Backend (if present)
[e2e/]          # Playwright (if present)
docs/           # Product and technical specs
.cursor/agents/ # Custom subagents (PM delegates via /name)
.agents/        # Agent routing and skills
```

## Domain skills (optional)

Add domain-specific skills under `.agents/skills/<your-domain>/SKILL.md` and list them in `.agents/AGENTS.md`. Do not put product secrets or proprietary questionnaires in the shared template.

## Agent skills

Stack and practice skills live under `.agents/skills/`. See `.agents/AGENTS.md` for load order.

**Implementation quality:** `frontend-developer` and `backend-developer` must pass lint, keep formatting clean, run relevant tests, and add test coverage for new features and bug fixes — see `.agents/skills/developer-quality/SKILL.md`.
