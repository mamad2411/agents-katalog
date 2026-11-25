# MyAdmin

## Stack

- **Language / Runtime**: TypeScript, Bun 1.4.0
- **Framework**: Angular 22.1+ for the web, Elysia for the server
- **Key dependencies**: `@ojiepermana/angular`, TypeBox, Bun SQL, `bun:sqlite`, CodeMirror 6
- **Package manager**: Bun

## Build approach

Fondasi dulu (fase A), lalu tiap feature sebagai irisan end to end, mengikuti urutan `struktur.md` bagian 7. Nomor feature = urutan build = nomor spec di `docs/specs/README.md`.

## Commands

```bash
# Install
bun install --frozen-lockfile

# Dev server
bun run dev

# Build
bun run build:web
bun run build:web:release

# Test
bun run test
bun run test:contract
bun run test:e2e

# Fast and smoke tiers
bun run test:fast
bun run test:acceptance

# Acceptance inventory and runtime evidence
bun run matrix:ac
bun run matrix:ac:run
bun run matrix:ac:validate
```

Quality gates include `bun run lint`, `bun run format:check`, `bun run typecheck`, `bun run check:boundaries`, and `bun run check:manifests`. Database integration tests need the disposable PostgreSQL or MySQL services and their environment variables.

## Specs

Specs live in `docs/specs/NNNN-title/` with `index.md`, `relation.md`, `test.md`, and `verify.md`. Build order and dependency meaning are indexed in `docs/specs/README.md`.

## Scope/spec synchronization and checklist integrity

- Treat `docs/scope/scope.md` as an evidence gate, not a plan or intention list. A checked Build, Test, or Verify item means that the corresponding work and its required proof have been completed and can be reproduced; an unchecked item means completion has not been established.
- Whenever scope, an acceptance criterion, dependency, implementation boundary, test plan, verification requirement, or evidence changes, inspect the affected `docs/specs/*/{index,relation,test,verify}.md` files and `docs/scope/scope.md` in the same change. Reconcile every affected checkbox and status with the new source of truth.
- If a changed or removed AC, test, dependency, or proof makes an existing checked item no longer relevant or no longer evidenced, uncheck or revise that item and its companion documentation. Preserve a checked item only when its current definition and evidence still prove completion; never retain it as historical or inferred completion.
- Keep Build, Test, and Verify independent. A passing focused test, source file, screenshot, local build, or generated artifact cannot substitute for a required integration, browser, performance, hosted, clean-environment, manual, security, signing, or external proof.
- After reconciling specs and scope, regenerate `docs/specs/ac-evidence-matrix.md` with `bun run matrix:ac` when its inputs changed, and update `docs/scope/progres.md` when the progress report is affected. Review the resulting diff for stale claims before committing.
- Before reporting a spec as done, verify that its current `index.md`, acceptance criteria in `test.md`, evidence in `verify.md`, and scope checkboxes agree. A stale checkbox is a documentation defect that must be fixed with the implementation or evidence change.

## Rules

- Apply Clean Architecture at module boundaries. Domain and application logic stay independent from frameworks and I/O, while outer layers implement inner ports.
- Use strict TypeScript, avoid `any`, keep public types explicit, and prefer exhaustive handling of closed unions.
- Keep exactly one root `package.json`. Treat `apps/*` and `packages/*` as source modules resolved by TypeScript aliases. Do not add nested manifests, Bun workspaces, Nx, or Turborepo without an accepted spec.
- Keep OpenAPI as the API source of truth. Generate contract types, keep Elysia routes aligned with the contract, and run contract drift checks after API changes.
- Angular feature code uses `@myadmin/sdk-angular`; do not use raw `fetch`, `HttpClient`, or API URL strings in feature components. Use `@ojiepermana/angular` as the single UI foundation and maintain a WCAG AA accessibility baseline.
- Keep `database-core` provider neutral. PostgreSQL and MySQL details belong in their provider modules and must not leak into core contracts.
- Validate configuration at startup. Redact credentials and tokens from logs, errors, audit details, WebSocket events, doctor output, and subprocess output.
- Use conventional commits. Git integration is active with `codex/` branch prefixes and commits per milestone. Pushes and pull requests require explicit confirmation.
- Use Bun tests for unit and integration coverage. Test domain logic without infrastructure doubles, and test infrastructure against disposable real systems when the acceptance criteria require it.

## Agent skills

- [angular-developer](/Users/ojiepermana/.agents/skills/angular-developer/): Angular standalone components, dependency injection, reactivity, forms, routing, accessibility, and builds
- [elysiajs](/Users/ojiepermana/.agents/skills/elysiajs/): Elysia server structure, typed validation, routes, and plugins
- [check](/Users/ojiepermana/.agents/skills/check/): runtime verification, acceptance evidence, and honest blockers
- [bun-sqlite](/Users/ojiepermana/.agents/skills/bun-sqlite/): Bun SQLite operations, prepared statements, transactions, and queries
- [playwright-cli](/Users/ojiepermana/.agents/skills/playwright-cli/): Playwright browser verification and local web testing

Declined: additional Agent Skill and MCP discovery

## Context files

- [apps/server/AGENTS.md](apps/server/AGENTS.md): Elysia composition root, route modules, per handler auth, realtime channels
- [apps/web/AGENTS.md](apps/web/AGENTS.md): Angular zoneless app, adding a page, route params, component test harness
- [packages/sdk-angular/AGENTS.md](packages/sdk-angular/AGENTS.md): SDK transport, facade registration, realtime client
- [packages/database-core/AGENTS.md](packages/database-core/AGENTS.md): provider contracts, quoting and binding rules, integration test environment
- [packages/internal-sqlite/AGENTS.md](packages/internal-sqlite/AGENTS.md): migrations, repositories, unit of work
- [tests/AGENTS.md](tests/AGENTS.md): test tiers, environment variables, e2e ordering, side effects

_Drafted by /audit from the repo, worth a quick human pass. Edit freely: once a line stops matching this draft, later runs treat it as curated and will flag rather than overwrite._
