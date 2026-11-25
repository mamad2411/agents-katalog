---
name: existing-project-migration
license: MIT
compatibility: Requires git, npm, Node.js, access to the prepared Customware migration workspace, and the extracted import artifacts under `.import/`.
metadata:
  author: customware-ai
  version: "2.6"
description: >
  Use this skill for Customware existing-project migration tasks that move uploaded
  customer apps from other builders into the standard Customware stack while
  preserving the source product's routes, workflows, UI, UX, and styling with
  no intentional user-facing changes while replacing only the runtime
  foundation. This skill covers both `Migration build` and `Migration verify`
  and includes self-grading quality gates that must pass before the task can
  complete.
---

# Existing Project Migration

## Core Idea

Re-read this `SKILL.md` after every compaction before continuing work. Do not assume conversational memory is sufficient.

This skill is for tech stack migration, not product redesign.

- The customer already has an app.
- The job is to reorganize that app into the Customware stack.
- The source product's routes, workflows, labels, layout shell, page sections, section ordering, visual language, and styling should survive as a source-faithful port. The default expectation is no intentional user-facing UI or UX change.
- The runtime stack must change to the prepared Customware stack built from `template-be-setup` plus the required `client-only-spa` merge rule.

Do not treat this task like a fresh app build, a domain reinterpretation, or a chance to simplify the product into a smaller generic dashboard.
Do not encode expectations from any previous migration. This skill must work for whatever app the customer uploaded. Derive the preservation target fresh from the current imported source each time.
A customer familiar with the source app should feel they are using the same app on a new stack, not a remake.
If literal parity is blocked by a real stack constraint, a missing source artifact, or a source bug, keep the difference minimal and record it explicitly as a named deviation.

## Source Authority

The uploaded artifacts drive the migration.

Priority:

1. `.import/project/` from `projects.zip` is the primary authority for product behavior, routes, UI, workflows, integrations, and business logic.
2. `.import/database/` from `database.zip` is the primary authority for persisted entities, schema inference, and seed data when CSV rows exist.
3. `.import/domain/` and `.import/domain-source.txt` from `domain.zip` are supporting context only.
4. `.tasks/domain.md` plus org name, org description, logos, colors, and brand context are low-authority presentation context only.

Do not let org/company knowledge or `.tasks/domain.md` redefine the imported product's domain, routes, workflows, schema, or product framing. This migration intentionally does not rely on the domain skill as product authority.
While `.tasks/domain.md` may exist, treat it as effectively ignorable for product-definition decisions during migration. The real source of truth is the imported codebase in `.import/project/` plus the imported database files in `.import/database/`. Use domain material only if it helps clarify minor presentation context and never let it outrank source code or source data.

## Fixed Target Stack

Migrate into the prepared Customware full-stack target:

- Vite
- React Router
- TypeScript
- Zod
- Node
- Hono
- tRPC
- SQLite via `better-sqlite3`
- Drizzle ORM and migrations

Do not preserve the uploaded source app's original runtime stack.

## Required Phase References

Read the exact files for the active task before doing work.

- `Migration build`
  - `.agents/skills/existing-project-migration/references/phase-1/overview.md`
  - `.agents/skills/existing-project-migration/references/phase-1/artifacts.md`
  - `.agents/skills/existing-project-migration/references/phase-1/grading.md`
- `Migration verify`
  - `.agents/skills/existing-project-migration/references/phase-2/overview.md`
  - `.agents/skills/existing-project-migration/references/phase-2/artifacts.md`
  - `.agents/skills/existing-project-migration/references/phase-2/grading.md`

If the task text is unclear, read both phase overview files first, determine which phase is active, then load the matching artifact and grading references.

## Critical Migration Invariant

These are hard rules.

- This is a stack migration. Preserve the source product; replace the runtime foundation.
- Preserve the imported app's visible route map, route paths, navigation labels, page hierarchy, headings, page sections, section ordering, section styling, control surfaces, workflows, typography, theme tokens, and logo usage. Default assumption: zero intentional user-facing change.
- Preserve the imported app's actual screen archetypes and concrete page contracts from source. If the source page is a calendar, keep it calendar-first. If it is a dense table workspace, keep that structure. If it is a real config form, keep the same form-driven surface. Do not swap one screen archetype for another just because it covers a similar business area.
- Treat the imported frontend as the visual and information-architecture authority, and treat the source route/page files as translation targets. Read the active router/bootstrap, layout/navigation files, theme/root CSS files, key assets, and representative page files before deciding UI direction.
- Port the source page structure and styling tokens directly. Do not paraphrase the source UI into new summaries, helper text, explanatory panels, or generic product copy.
- Before any interactive verification pass, run a pre-interactive fidelity review directly against the source frontend code, migrated code, and any available source screenshots. Confirm the shared shell plus every source-visible screen still contains the expected layout blocks, named sections, section order, headings, labels, controls, actions, tables, charts, forms, tabs, and style direction before opening the browser.
- For each source-visible screen, extract the exact screen contract before implementation or grading. That contract must include exact button labels, tab labels, filter labels, section titles, table columns, key actions, named sections, and section order taken from the source app.
- Treat code-visible omissions as failures before interactive QA. If the source code clearly shows a sidebar, navigation section, header, tab strip, table header, filter row, form block, chart block, action cluster, or other visible section and the migrated code does not preserve it, the phase is still open even if the page can technically render.
- If any extracted exact contract item is missing, renamed, reordered, restyled beyond recognition, or replaced with a different surface without an explicit blocker, that grading pass fails. Use those failed exact items as the mandatory next-fix queue and keep iterating until the screen passes.
- When a user-noticeable UI difference is truly unavoidable, keep it minimal and log it explicitly in `migration-plan.json`, `migration-review.md`, and `migration-open-gaps.md`. Unrecorded drift is a fail.
- Do not invent migration-themed copy such as `Imported App Migration`, `Migration slice`, or any similar framing.
- No user-facing copy may mention imported, migrated, source, preserved, phase, CSV, seed, staging, readiness, review, or any equivalent provenance narrative unless the source app itself used that language.
- Do not collapse the imported app into a narrow vertical slice just because the CSV exports cover only part of the data model.
- Do not replace source-visible pages with generic hero cards, placeholder dashboards, filler prose, summary cards, readiness panels, or generic review/status shells.
- Interactive verification is always from the end-user perspective. Start from the first user-visible page on the actual review or preview host when that host exists, usually `/` while unauthenticated.
- Interactive verification must prove visible parity, not just DOM existence. A route counts as covered only when the expected shell, layout blocks, and key controls are visibly rendered on screen and at least one basic page-native action works. Hidden text, detached UI, or merely attached DOM nodes do not count as success.
- Phase 1 verification is exhaustive interactive QA, not broad automated suite authoring. Visit every available migrated page route from the user perspective, exercise at least one basic page-native action on each route, and cover common flows such as login, sign-out, navigation, search, filter, tabs, forms, detail views, and integration or configuration actions where those surfaces exist.
- Automated unit tests and end-to-end suites belong primarily to phase 2. Phase 1 may add or repair tests only when needed to unblock the migration or interactive QA, but phase-1 signoff depends on exhaustive interactive evidence rather than automated suite breadth.
- If a review or preview URL exists, localhost-only or debug-port-only verification is insufficient for signoff.
- A blank first page, blank login page, failed seeded login, failed first in-app navigation, fatal console error, or hydration/runtime boot error is an automatic failure.
- Do not keep legacy runtimes, back-compat handlers, or extra validator services just to make the migration look successful.
- Remove template demo pages, placeholder copy, and template-only tests when they no longer match the imported product.
- Use CSV rows from `.import/database/` as seed-data authority when present.
- Use the agent-owned review artifacts below as the enforcement layer. If the score fails or ordinary drift remains open, the phase is still open.
- Judge fidelity against the current imported app only. Do not let lessons from earlier migrations become hidden product requirements for later ones.

## Required Enforcement Artifacts

These files are mandatory quality gates during migration:

- `.import/migration-plan.json`
- `.import/migration-checklist.md`
- `.import/migration-review.md`
- `.import/migration-open-gaps.md`

Use these templates directly:

- `.agents/skills/existing-project-migration/assets/templates/migration-plan.json`
- `.agents/skills/existing-project-migration/assets/templates/migration-checklist.md`
- `.agents/skills/existing-project-migration/assets/templates/migration-review.md`
- `.agents/skills/existing-project-migration/assets/templates/migration-open-gaps.md`

Rules:

- `Migration build` creates any missing artifact only after deep source intake.
- `Migration verify` fails if any required artifact is missing at verify start.
- Update `migration-review.md` and `migration-open-gaps.md` after every meaningful implementation or verification pass.
- The review and open-gaps ledgers must track every source-visible screen individually, plus any shared shell or runtime rows needed for context.
- Do not replace the ledger tables in the templates with vague prose.
- The first real grading pass is not allowed to declare zero gaps unless an adversarial pass is already recorded and it genuinely found no blocking drift.
- If any critical rubric item fails, if the score threshold is missed, or if `migration-open-gaps.md` still contains ordinary migration drift, the task is not done.

## Phase Model

- `Migration build` is phase 1.
  - Deep source intake
  - Migration plan and checklist
  - Template merge
  - Source-derived schema, routes, pages, and workflows
  - Source-derived UI translation with route-by-route source-screen fidelity
  - Pre-interactive adversarial self-grading against source code and screenshots before browser QA
  - Exhaustive interactive verification from the user perspective across every available migrated page route
  - First passing migration grade with no unresolved user-visible drift
- `Migration verify` is phase 2.
  - Reload phase-1 artifacts
  - Reload phase-1 interactive QA evidence
  - Brief user-perspective sanity recheck after verify fixes
  - Fresh-database runtime verification
  - Unit-test authoring or repair
  - Playwright end-to-end coverage repair or expansion
  - Final passing migration grade
  - Cleanup of `.import/`, Playwright outputs, and temporary migration-only artifacts as the last step

Both phases must loop until the score threshold passes, all critical items pass, and no ordinary open gaps remain.
Do not run the rubric a couple of times, notice it is still failing, and stop. The point of grading is to force more iteration. Keep fixing and re-grading until the result clears the passing bar with a strong score, roughly in the high-pass range rather than barely scraping by.

Phase 1 is interactive-test-heavy. Phase 2 is automated-test-heavy.
Phase 1 should produce the source-faithful app plus exhaustive user-perspective route coverage evidence.
Phase 2 should turn that evidence into durable unit and end-to-end coverage, do only a light sanity recheck interactively, and then leave the repo clean.

Phase 1 already owns exact UI preservation. Do not defer meaningful screen parity to phase 2. By the end of phase 1, the migrated app should already look and behave like the same app with only the runtime swapped.
Because the agent can read the source frontend code directly, treat the original UI implementation as translation input, not inspiration. Port route-level composition, named page sections, section ordering, labels, actions, filters, forms, tables, charts, empty states, and style tokens as directly as the new stack allows.
A screen that is only visually close, only in the same business area, or explained with migration or provenance copy is a fail.
Do not wait for the browser pass to notice basic structural drift that the code already reveals. If the source app clearly has a persistent sidebar, navigation sections, a header block, a tab strip, a filter bar, a full table section, a table header band, a form section, or another major visible surface, confirm that the migrated code still contains it in roughly the same arrangement before the interactive pass.
Per-screen grading must be concrete, not impressionistic. Compare the migrated screen against the extracted exact contract item by item, fail the round on mismatches, fix them, and re-grade until the screen passes.

## Non-Negotiables

- Keep the migration zip-driven.
- Keep org context limited to presentation context, not product-authority context.
- Keep the runtime on the fixed Customware stack.
- Preserve `app/lib/trpc-provider.tsx` and `app/utils/error-logger.ts` when merging `client-only-spa` `app/`.
- No shipped route or page may contain migration-aware narrative or provenance commentary.
- No phase may pass if the real review or preview app boots to a blank screen or crashes before a user can reach login or the first post-login page.
- No phase may pass from attached-only or hidden-element checks. Verification evidence must show the expected UI is visibly rendered and usable from the user perspective.
- Do not search outside the prepared workspace for alternate template instructions unless the workspace already contains an allowed clone.
- Keep `.import/` and other temporary migration evidence through phase 1 and during phase-2 verification, then remove them in the final phase-2 cleanup step unless the task explicitly requires durable retention.
- Fail with a concrete blocker rather than self-approving a weak migration.
