---
name: setup-stack
description: "Selects and pins the technology stack — project type, backend, frontend, UI kit, API style (GraphQL default), game engine, database, tests, CI, deploy target, observability, layout — and writes technical-preferences.md with exact versions from the stack reference. Run at project start after /init or when the stack changes, or for 'choose the stack', 'which framework should we use', 'pin the versions'."
argument-hint: "[type: site|spa|api|fullstack|game|game+backend] [--quick]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion
---

# Setup Stack

Language, `<hooks>`, command namespaces, gate mechanics and the documents-lane commit gate: `docs/coordination-rules.md` § Skill conventions.

Result: `.claude/docs/technical-preferences.md` without `[TO BE CONFIGURED]`, the record of the stack choice. The stack is a technical decision, so it never becomes a `D-NN` entry: `production/decisions.md` holds owner decisions only (its header: "Technical decisions are ADRs, not entries here").

Glossary: the reference — `.claude/docs/stack-reference/` (`index.md` for versions, `go.md`, `php.md`); every version a question quotes is read from it at question time, the skill carries none.

## Phase 1: Context
1. **Read** `technical-preferences.md`, `docs/specs/product-spec.md` (if any), `production/stage.txt` and the reference's `index.md`.
2. **Reference age.** Older than 60 days → say so and suggest `/stack-update` first; not blocking.
3. **Environment.** Run `go version`, `php -v`, `node -v`, `pnpm -v`, `docker --version`; report what is missing after Phase 2, for the chosen stack only (a Go-only `api` needs no pnpm). A tool the chosen stack needs is missing → stop after Phase 2: summarise the interview, write nothing, verdict `BLOCKED (missing tools: …)` naming what to install.

## Phase 2: Interview
One `AskUserQuestion` at a time, recommendation first. `--quick` takes every Recommended option without asking and shows the summary; the deploy target (step 7) has no universal default and is asked anyway; the Phase 3 write gate still applies.

1. **Project type** (argument or question), platforms (desktop/mobile-web/PWA), rendering (SPA/SSR/SSG).
2. **Backend**: **Go** (services, realtime, games) | **PHP** (content systems, existing PHP ecosystem) | **Node** (BFF/SSR) | none — recommendation by type. PHP chosen → read `references/interview-php.md` § Version and framework and ask its two questions in order.
3. **API style**: **GraphQL (SDL, default for the client API)** | REST/OpenAPI | both (GraphQL + REST for files/webhooks). Then:
   - `api_contract_path`: for a Go module `api/schema.graphqls` (Recommended; gqlgen reads it in place), otherwise `docs/architecture/api/schema.graphql`.
   - With gqlgen, `graphql_models`: **dto** (generated models mapped in resolvers — Recommended) | bind (domain types in `gqlgen.yml`).
4. **Frontend**: **Angular** (+ Material | Taiga UI) | **Vue / Nuxt** (+ UI kit) | vanilla TS (a game without a UI framework). For Angular, also the file naming style: v20+ without suffixes | classic.
5. **Game** (type game): three.js (3D) | PixiJS (2D) | Phaser | Babylon; networking: none | server-authoritative.
6. **Data**: PostgreSQL (+ Redis) — confirm; auth: sessions | OIDC | JWT+BFF.
7. **Infra**: Docker + compose, GitHub Actions — confirm. Then the **deploy target** and its **delegate**: read `references/deploy-target.md` (contract `.claude/docs/deploy-target-contract.md`) and ask its one `AskUserQuestion` — `compose-ssh` Recommended for a single server; a shared host with its own proxy repository → also ask `Infra repo` and `Proxy config`; `kubernetes` → also its § Kubernetes questions (chart path, environments, secrets, routing). Then **observability**: read `references/observability.md` and ask its one question — the studio stack Recommended. Then **supply chain**: read `references/supply-chain.md` and ask its one question — the studio default Recommended when a release image exists.
8. **Layout**: monorepo (`apps/`, `packages/`) | current structure — show a proposal. Go backend → also `go_layout` from `references/interview-go.md` § Layout, the directory tree shown.
9. **Architecture**: PHP chosen → read `references/interview-php.md` § Architecture, Go chosen → `references/interview-go.md` § Architecture; ask its questions in order, then show the resulting tree.

## Phase 3: Draft and write
1. **Draft** the full `technical-preferences.md`: exact versions from the reference, naming conventions for the chosen languages (the Angular file style from Phase 2), performance budgets, the `Deploy target` / `Deploy delegate` (plus `Infra repo` / `Proxy config`; the `Kubernetes` sub-block, or `n/a`) the `Observability` block with its four fields and the `Supply chain` block with its five (every `none` with its reason). Show it whole.
2. **Ask** "May I write `.claude/docs/technical-preferences.md`?" as one `AskUserQuestion`: write (Recommended) · show the draft/diff first · not now. The question also names, when they apply, the two `compose-ssh` files of step 4 and `production/stage.txt` → `specification` — only when the product spec exists **and** the current stage is `discovery` (a brownfield stage is never lowered).
3. After the "write" answer: `touch .claude/.write-consent`.
4. **Write** exactly the files the answer covered: `technical-preferences.md`; for `compose-ssh`, `cp .claude/docs/templates/deploy/compose-ssh.sh scripts/deploy/compose-ssh.sh` and create `docs/deploy/compose-ssh.md`; `production/stage.txt` when step 2 named it.

## Phase 4: Commit (documents lane)
Right after the write (§ Documents-lane commit gate; `.claude/docs/git-workflow.md` § Documents):
1. Record it: `<hooks>session-state.sh set Gate "/setup-stack Phase 4: commit?"`.
2. Ask, one `AskUserQuestion` (options: § Documents-lane commit gate); when HEAD is a story branch, name it: switch to `<default>` and commit there (Recommended — a pipeline-wide document) · commit here · leave uncommitted.
3. On "commit": `docs: stack decision`, staging exactly the written documents — `.claude/docs/technical-preferences.md`, `production/stage.txt` when changed, `docs/deploy/compose-ssh.md` when created. Nothing is committed without the answer.
4. Clear it: `<hooks>session-state.sh set Gate "—"`.
5. `scripts/deploy/compose-ssh.sh` is toolchain work, not a document: it never rides the `docs:` commit. Name it in the result and offer the chore lane for it (git-workflow.md § Chore / infra).

## Phase 5: Consequences
1. **Layout ADR**: propose it through `/web-studio:architecture-decision` (copy mode `/architecture-decision`), recording the directory shape (Phase 2 step 9) and, with `go_composition_root: main`, the composition-root deviation.
2. **Fork ADRs**: propose one per non-trivial fork (GraphQL vs REST, Angular vs Vue, game engine) — the same command. The user decides; no ADR is written here.
3. Propose `/test-setup` and `/threat-model` as the next mandatory architecture steps.

Verdict: `COMPLETE` | `BLOCKED (missing tools: …)`.

Next step — one `AskUserQuestion`; the Recommended option follows what Phase 1 found, never a default:

| Phase 1 found | Recommended | Alternatives |
|---|---|---|
| no `docs/specs/product-spec.md` | `/product-spec` | `/game-concept` (type game / game+backend) · revise the stack |
| the product spec, no `docs/specs/features/*.md` | `/feature-spec` | `/test-setup` · `/product-spec` (revise it) · revise the stack |
| the product spec and feature specs | `/create-stories` | `/feature-spec` · `/test-setup` · `/product-spec` (revise it) · revise the stack |
