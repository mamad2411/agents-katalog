---
name: project-conventions
description: Use when setting up a new project's repository conventions and house style, the _private vs docs vs code layout, .gitignore, CLAUDE.md, the conventions/pattern registry, and the recommended MCP setup. Run early (Phase 0) and consult when introducing new patterns.
---

# Project Conventions

**Announce at start:** "I'm using claude-engineer:project-conventions to set up the repo's house style."

## Folder contract
- **`_private/`** - UNCOMMITTED working area: drafts, screenshots, scratch notes, research. Add to `.gitignore`.
- **`docs/`** - COMMITTED non-code: `docs/plan/*` (the plan), `docs/decisions.md`, architecture, runbooks, API docs.
- **`.claude-engineer/`** - durable state (see `claude-engineer:project-memory`). Commit `memory.md`/`progress.md`; ignore `quality-gate-status.json`.
- **code** - the monorepo (`apps/`, `packages/`, `services/`, `libs/`; see `claude-engineer:monorepo-and-tooling`).

## Phase 0 setup (create a task per item)
1. `git init` (if not a repo). Create `.gitignore` covering `_private/`, `.claude-engineer/quality-gate-status.json`, `node_modules`, `.venv`, build dirs, `.env*`.
2. Create `_private/` and `docs/` (with `docs/plan/`).
3. Generate a **root `CLAUDE.md`** capturing: the stack, the iron laws (plan-gated, CX-first, services-in-docker/app-native, the four quality gates), how to run things, and where state lives. This is the project's standing instruction file.
4. Initialize the **conventions registry** at `docs/conventions.md` - the house style the agent must reuse instead of reinventing: naming, error handling, API response shape, folder patterns, and a UI pattern registry (component + token usage; generalize the design system's DESIGN.md into reusable patterns). Append to it whenever a new pattern is established.
5. Write **`docs/recommended-mcps.md`** from `templates/recommended-mcps.md` and tell the user which MCPs to install with their own keys.

## MCP policy (BYO keys)
Claude-Engineer **references** MCP servers; it never bundles secrets. Users install with their own keys via each provider's command. See `templates/recommended-mcps.md` for Playwright, Chrome DevTools, 21st.dev Magic, and designmd (getdesign.md).

## Red flags - STOP
- Committing screenshots/scratch to git → those belong in `_private/`.
- Inventing a new pattern that contradicts `docs/conventions.md` → reuse the house style or update the registry deliberately.
- Secrets or API keys written into committed files → never; use `.env*` (git-ignored) and document required vars.
