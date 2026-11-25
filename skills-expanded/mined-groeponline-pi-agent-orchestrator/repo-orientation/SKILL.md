---
name: repo-orientation
description: Navigate and contribute to the pi-agent-orchestrator repo. Use for any task touching src/, test/, docs/, workflows, or the build/release pipeline of this package. Covers architecture, dev commands, conventions, and common pitfalls.
---

# Pi Agent Orchestrator — Repo Orientation

This package (`@groeponline/pi-agent-orchestrator`) is a **pi extension** that runs inside a
[pi coding-agent](https://github.com/GroepOnline) host. The three `@earendil-works/pi-*`
packages are the host platform and are **peer deps only** — never direct dependencies.

## Dev environment

- **Node.js 22+** (LTS). Public CI, test, and lint use GitHub-hosted `ubuntu-latest` (free on a public repo). Deploy, release, and publish stay on the GroepOnline fleet. macOS/Windows CI legs stay out of the matrix.
- Install once after clone: `npm install`
- Optional local git hooks (biome + tsc on commit, full tests on push):
  `npm run setup:hooks` (copies `scripts/git-hooks/` → `.git/hooks/`).

## Core commands

```bash
npm run typecheck     # tsc --noEmit
npm run lint          # Biome check (lint; formatter disabled)
npm test              # vitest run --retry=2
npm run bench:all     # perf benchmarks
npm run build         # tsc → dist/ (also runs in prepublishOnly)
# Full gate:
npm run typecheck && npm run lint && npm test
```

Lint auto-fix: `node_modules/.bin/biome check --write --unsafe src/ test/ scripts/`.
**Never run Prettier or ESLint** — removed from the project.

## Architecture (key `src/` modules)

- `index.ts` — extension entry point (registered via `package.json` → `"pi": { "extensions": ["./dist/index.js"] }`)
- `agent-types.ts` — permission model · `agent-permissions.json` (root) — resource allow/deny for the docs site
- `agent-runner.ts` / `agent-manager.ts` / `agent-registry.ts` / `default-agents.ts` / `custom-agents.ts` — agent lifecycle & config
- `settings.ts` — persistent settings (`SubagentsSettings`)
- `compaction-snapshot.ts` / `context.ts` — upstream compaction observation / parent context
- `handoff.ts` — handoff protocol · `hooks.ts` — lifecycle hooks
- `memory.ts` / `prompts.ts` / `validators.ts`
- `schedule*.ts` — scheduling engine · `swarm-join.ts` / `group-join.ts` / `batch-orchestrator.ts` / `orchestration-dispatch.ts` — multi-agent topologies
- `cross-extension-rpc.ts` — inter-extension RPC · `worktree.ts` — git worktree ops · `debug-capture.ts`
- `ui/` — TUI (dashboard, widget, conversation-viewer, theme, animation, menus)

## Project config (for pi / agents)

- `.pi/subagents.json` — project subagent tuning (concurrency, thinking, UI style)
- `agent-permissions.json` — resource permission model for the public docs site (read-only)
- `scripts/setup-git-hooks.sh` — local pre-commit/pre-push hooks
- `.github/workflows/` — CI / QA / publish / release (see `release` skill for the release flow)

## Conventions

- **Conventional Commits** (`feat:`/`fix:`/`docs:`/`refactor:`/`test:`/`chore:`/`ci:`/`build:`).
- **Biome**: double quotes; formatter disabled.
- **ESM**: import specifiers need `.js` extensions even in TypeScript.
- Tests live in `test/` (NOT `tests/`). 95+ vitest files.
- Branch from `main`; PRs require CI pass + review.

## Common pitfalls (from AGENTS.md)

- YAML booleans from `js-yaml` are strings → use the parsing helpers in `src/custom-agents.ts`.
- ESM imports need `.js` extensions.
- Don't add `pi-*` as direct deps.
- `schedule.test.ts` / `schedule-store.test.ts` are flaky on Windows (temp-dir races) — CI marks `continue-on-error`; don't let them block.

## Docs

- `docs/architecture.md` (module map) · `docs/api-reference.md` · `docs/custom-agents.md`
- `AGENTS.md` (repo agent contract + 15-item common-mistakes checklist) · `CONTRIBUTING.md`
- `llms.txt` / `llms-full.txt` for machine-readable context.

## When adding built-in agents / settings

- New agent type → `src/default-agents.ts` (`DEFAULT_AGENTS`) + `test/default-agents.test.ts` + README agent-types table.
- New setting → `src/settings.ts` (`SubagentsSettings` + defaults) + `src/output-handler.ts` (`buildSettingsSnapshot` + settings menu) + `docs/api-reference.md`.
