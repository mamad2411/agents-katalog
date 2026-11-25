---
name: clone-github-project-with-my-techstack
description: Clone a GitHub repo into a working rebuild — deep-analyze, canonical stack, parity, then /ship
argument-hint: "<owner/repo-or-url>"
related:
  - clone-product-with-my-techstack
  - deep-analyze
  - follow-my-techstack
  - follow-create-product
  - follow-create-web
  - implement-to-production
  - use-agents-capture
  - report-prompt-uxui-web-design
  - deep-research
  - deep-review-codebase
  - deep-test
  - run-dev
  - ship
  - report
  - suggest-next-action
---

## Goal

Clone an existing GitHub project into a fresh, working rebuild — `/deep-analyze` the real codebase for the full feature/route map, re-implement it on the canonical tech stack via `/follow-my-techstack`, verify parity, then ship end to end with `/ship`

## Scope

- Use when the target has a public (or accessible) GitHub repo — source-level analysis beats visual guessing
- No repo, only a live product URL → use `/clone-product-with-my-techstack` (it falls back here when it finds a repo)
- Clone means re-implementing features/behavior on our own stack — not vendoring the original code, unless the license permits it (see `## Rules → 1`)
- Goes all the way to `/ship` — not an analysis-only skill

## Execute

### 1. Resolve And Fetch The Repo

> Goal: have the real source as read-only reference

1. Take `owner/repo` or a repo URL from the argument — unclear → `/ask-me`
2. Run `gh repo view <repo>` — record description, primary language, route/deploy hints; then `git clone` into a reference dir (e.g. OS temp via `/create-files-in-os-temp`) — reference only, never the build target
3. Read the license (`LICENSE`, `package.json` `license`): permissive → may reuse code with attribution; proprietary/non-commercial → re-implement behavior only, record the constraint in the plan
4. If a deployed live instance exists → note its URL for captures in step 6

### 2. Deep-Analyze The Codebase

> Goal: the complete truth of what the project does, from source

1. Run `/deep-analyze` across every dimension: structure, routes/pages, features, data models, API surface, auth, payments, integrations, config, deps, CI/CD
2. Build the parity checklist from real source: every route with `path`, `page name`, `description`, `states`, `auth-required?` — every feature with its evidence `file:line`
3. Run `/deep-research` for anything the source references but doesn't contain (external APIs, SaaS embeds, proprietary services)
4. Report the analysis as a route + feature table via `/report` — this table is the definition of done

### 3. Pick The Canonical Stack

> Goal: rebuild on our stack, not theirs

1. Run `/follow-my-techstack` — map each need found in step 2 (validator, ORM, router, UI lib, auth, payments, hosting) to the catalog Default; the original project's stack choices are not binding
2. Genuine gap in the catalog → `/deep-research dependencies`, then propose a catalog update — never silently adopt a non-default
3. Report the chosen stack as a table: `Original dep` → `Our pick` → `Reason`, so drift is visible

### 4. Scaffold The New Project

> Goal: a correct project skeleton before any feature work

1. Product with auth/payments/dashboard → scaffold via `/follow-create-product`; plain site → `/follow-create-web` with the route list from step 2
2. New project location: `/create-new-project-in-drive-d` for a fresh repo
3. Set up env/secrets per `/follow-secret-manager` — original secrets never copied; placeholders + `/open-web-for-config-secret` for the user to fill

### 5. Implement To Production

> Goal: every route and feature real, no stubs

1. Run `/implement-to-production` down the parity checklist — each feature becomes working production code with no TODO/MOCK/placeholder left
2. Run `/run-dev` continuously while building; errors → `/resolve-errors` immediately
3. Reuse is allowed only within the step 1 license verdict — anything copied carries attribution in code comments

### 6. Verify Parity

> Goal: prove the rebuild matches the original with evidence

1. If a live instance exists → run `/use-agents-capture all` against it (original routes × device sizes); otherwise capture the original from local run or rely on source-level checklist
2. Run `/use-agents-capture all` against the rebuild → compare per route; list every gap
3. Run `/report-prompt-uxui-web-design` on the rebuild route list to sanity-check full-app coverage (all routes present, states covered); close UX gaps via `/improve uxui`
4. Run `/deep-test all` — unit/integration/e2e green; run `/deep-review-codebase` on the rebuild for quality dimensions; fix via `/deep-review-codebase-then-fix`
5. Repeat until every checklist row is `done` or `intentional-diff` (with reason)

### 7. Ship

> Goal: deliver through the full gate

1. Run `/ship` — it already enforces `/follow-agents-md` → review/validate/tests → `/git-commit-and-push` → PR review gate → merge into `main`
2. Report the live URL, coverage vs original, and license-driven exclusions

### 8. Report

> Goal: summarize the clone

1. Run `/report` — table: `No.`, `Route/Feature`, `Parity`, `Evidence`, `Notes`
2. Run `/suggest-next-action` — e.g. `/bench-competitors` to beat the original, `/update-github-metadata` for the new repo

## Rules

### 1. License Before Copy

- The license decides: permissive → copy with attribution allowed; restrictive/proprietary → behavior re-implementation only, no copied source or assets
- Trademarks, brand names, and marketing copy are never cloned in any case
- Unclear license → `/ask-me` before implementing, not after

### 2. Source Is The Spec

- Feature/route claims come from real source evidence (`file:line`) — never from the README alone or memory
- Dead/unwired code found in the original is not cloned — parity targets working behavior, verified by running it

### 3. Canonical Stack First

- `/follow-my-techstack` catalog defaults win over the original's stack; deviations need a recorded reason
- Keep it minimal: don't clone features the original ships but the user doesn't want — confirm scope with `/ask-me` first

### 4. Ship Discipline

- Not done until: dev server healthy, `/deep-test all` green, parity verified, `/ship` gates green — never skip a failing gate
- Failing gate 3 rounds → stop and report blockers

## Expected Outcome

- Route + feature parity checklist built from real source analysis
- A fresh project on the canonical stack implementing every row for real (no TODO/MOCK)
- Parity verified by captures and tests, with license constraints recorded
- Shipped via `/ship` (AGENTS.md fresh, gates green, pushed, PR merged to `main`) with a live URL
- `/report` summary with parity table and next actions
