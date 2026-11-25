---
name: clone-product-with-my-techstack
description: Clone a product with no repo into a working rebuild — research, capture, parity, then /ship
argument-hint: "<url-or-product-name>"
related:
  - clone-github-project-with-my-techstack
  - deep-research
  - use-agents-capture
  - report-prompt-uxui-web-design
  - follow-my-techstack
  - follow-create-product
  - follow-create-web
  - implement-to-production
  - deep-review-codebase
  - improve
  - run-dev
  - deep-test
  - ship
  - report
  - suggest-next-action
---

## Goal

Clone a product (website/SaaS) that has no public source repo — research every route, capture the real UI as evidence, rebuild it on the canonical tech stack until it actually works, verify route-by-route parity, then ship end to end with `/ship`

## Scope

- Use when the target is a live product URL or product name with no public GitHub repo
- A public GitHub repo exists for the target → fall back to `/clone-github-project-with-my-techstack` instead (source-level analysis beats visual cloning)
- Clone means behavioral + visual parity re-implemented from scratch — never copy the target's proprietary code, brand assets, logos, or marketing copy (see `## Rules → 1`)
- Product with auth/payments/dashboard → build via `/follow-create-product`; a plain site → `/follow-create-web`
- This skill goes all the way to `/ship` — it is not research-only

## Execute

### 1. Resolve Target And Check For A Source Repo

> Goal: know what to clone and whether /clone-github-project-with-my-techstack owns it

1. Take the target URL or product name from the argument — unclear → `/ask-me`
2. Search for a public source repo: `gh search repos <product-name>`, site footer/About/Docs links, and `/deep-research` the product's GitHub presence
3. Repo found and accessible → hand off to `/clone-github-project-with-my-techstack` with the repo URL and stop here (fallback)
4. No repo → record the target URL, product name, and route scope as the contract for the rest of the steps

### 2. Research Every Route

> Goal: a complete route + feature inventory of the target, from evidence not memory

1. Run `/deep-research` on the product: features, content structure, pricing tiers, auth surfaces, integrations
2. Enumerate every route: crawl the site (`/use-agent-browser` or sitemap) — every route gets `path`, `page name`, `description`, `states` (empty/loading/error), `auth-required?`
3. Record real behavior: forms, flows, dynamic content, third-party calls — cite evidence (URL/route) per claim
4. Save the inventory as the parity checklist (route table via `/report`) — any route that can't be reached → mark it and state the assumption

### 3. Capture The Target For Real

> Goal: screenshot evidence of every route to clone against

1. Run `/use-agents-capture all` against the live target — every route × device size (desktop/tablet/mobile) in one run
2. Check `manifest.json` errors first; re-capture failed routes; view each image to extract layout, spacing, and content per route
3. Save captures under `.devin/temp/report/clone-<product>/target/` — this is the visual baseline for parity in step 7

### 4. Compose The UX/UI Parity Brief

> Goal: a full-app design brief covering all routes

1. Run `/report-prompt-uxui-web-design` with the route inventory from step 2 — one card per route, mobile view, desktop/tablet/mobile specs
2. Run `/follow-design-system` to define shared tokens (color, type, spacing) for the rebuild — own design system, not copied brand assets
3. Optionally render the grid via `/visualize-in-web` and confirm with the user before building

### 5. Pick Stack And Scaffold

> Goal: the rebuild starts on the canonical stack

1. Run `/follow-my-techstack` — pick every dependency from the canonical catalog (`follow-my-techstack/references/techstack-catalog.md`), not the target's stack
2. Route fixes drift here: deviating from a catalog default → record a reason or `/ask-me`
3. Scaffold via `/follow-create-product` (auth/payments/dashboard product) or `/follow-create-web` (plain site) with the page list from step 2
4. Secrets/env per `/follow-secret-manager` — never commit credentials

### 6. Implement Until It Really Works

> Goal: production code for every route, no stubs

1. Run `/implement-to-production` across the whole route table — every page, flow, and state is real, no TODO/MOCK/placeholder
2. Run `/run-dev` — the app must start clean; fix errors as they appear via `/resolve-errors`
3. Run `/deep-test website` per key route — routes render and flows pass, not just compile
4. Work the parity checklist from step 2 route by route until all are done

### 7. Verify Parity

> Goal: prove the clone matches the target with captured evidence

1. Run `/use-agents-capture all` against the rebuilt app — same routes, same device sizes → `.devin/temp/report/clone-<product>/ours/`
2. Compare ours vs target captures route by route; list every visual/behavioral gap
3. Run `/improve uxui` on the gap list and fix each finding; run `/deep-review-codebase` for accessibility/performance dimensions
4. Repeat 2–3 until parity passes or remaining gaps are intentional (record why)

### 8. Ship

> Goal: deliver the clone through the full gate

1. Run `/ship` — it already enforces `/follow-agents-md` → review/validate/tests → `/git-commit-and-push` → PR review gate → merge into `main`; never skip a failing gate
2. Report the live URL, route coverage, and parity status

### 9. Report

> Goal: summarize what was cloned and what was intentionally different

1. Run `/report` — table: `No.`, `Route`, `Parity`, `Evidence`, `Notes`
2. Run `/suggest-next-action` — e.g. `/bench-competitors` to beat the original, `/release-new-version`

## Rules

### 1. Clone Scope And Legality

- Re-implement behavior and layout only — never copy proprietary source, logos, brand names, or marketing text; write original content for the clone
- Check the target's ToS/pricing page before cloning paid features; report anything that looks illegal to clone instead of building it
- Logos/images: generate or use open assets, not the target's files

### 2. Evidence Over Memory

- Every route, feature, and layout claim comes from step 2/3 research or captures — never guess from memory
- The parity checklist from step 2 is the definition of done — the task ends only when every row is `done` or `intentional-diff`

### 3. Canonical Stack First

- `/follow-my-techstack` catalog is the default for the rebuild; copying the target's stack is not a reason to deviate
- Existing code wins over new installs per the techstack skill — don't add deps an existing one covers

### 4. Ship Discipline

- Do not stop at prototype: `/run-dev` healthy, parity passed, `/ship` gates green are all required
- Failing gate 3 rounds → stop and report blockers instead of forcing through

## Expected Outcome

- Route inventory + per-route target captures as the clone baseline
- A rebuilt product on the canonical stack with every route real (no TODO/MOCK)
- Parity verified by comparing our captures against target captures, gaps closed
- Shipped via `/ship` (AGENTS.md fresh, gates green, pushed, PR merged to `main`) with a live URL
- `/report` summary with parity table and next actions
