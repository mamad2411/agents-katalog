---
name: monorepo-and-tooling
description: Use when scaffolding a project's repository or adding a new app/package/service, to set up the polyglot monorepo (JS + Python) with shared packages, workspaces, and task orchestration. Run early in Phase 0.
---

# Monorepo & Tooling

**Announce at start:** "I'm using claude-engineer:monorepo-and-tooling to lay out the polyglot monorepo."

## The layout (always a monorepo)
One repo, **two dependency graphs side by side**:
- **JS side** - `apps/*` (React/Next frontends) + `packages/*` (`ui`, `config`, `eslint-config`, `tsconfig`), managed by **pnpm (default) or Bun** workspaces + **Turborepo** for caching/task orchestration.
- **Python side** - `services/*` (FastAPI) + `libs/*` (shared libs) as **uv workspace** members sharing one `uv.lock`.
- **Bridge** - give each Python service a thin `package.json` whose scripts shell out to `uv`, so **Turborepo is the single task vocabulary** across both languages.

## Defaults & decisions
- **JS package manager: ask per project** (Bun vs pnpm). Default pnpm for stability unless the user prefers Bun.
- Shared `packages/ui` holds the design-system components; `packages/config` holds Tailwind/token config.
- Root config: `turbo.json`, `pnpm-workspace.yaml` (or Bun workspaces), `pyproject.toml` (uv workspace), root `tsconfig`/eslint base.

## Non-negotiables
1. **Shared code is a package**, not copy-paste - design tokens, UI, types, configs live once and are imported.
2. **Tasks run through Turborepo** (`dev`, `build`, `lint`, `typecheck`, `test`) for caching and one vocabulary.
3. **App runs native; services in Docker** (`claude-engineer:docker-dev-environment`).

**Full detail (concrete directory tree, root config files, workspace wiring, pnpm-vs-Bun trade-offs):**
read `references/polyglot-monorepo.md` on demand.

## Red flags - STOP
- Duplicated component/token/type code across apps → extract to a `packages/*`.
- Running tasks ad-hoc per app instead of through Turborepo.
- A single-language repo when the project will clearly have both a frontend and a FastAPI backend.
