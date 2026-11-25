---
name: universal-development-planner
description: ALWAYS use automatically before building or significantly changing any software product - web app, SaaS, ERP, POS, e-commerce, mobile app, API/backend, AI app, automation, dashboard, business system. Creates and cross-checks up to 38 project-specific planning docs in docs/, passes a pre-development gate, then develops from the plan, tests, verifies, and keeps docs in sync. Replaces saas-kickoff.
---

# Universal Development Planner

PLAN FIRST -> VERIFY PLAN -> DEVELOP -> TEST -> VERIFY -> DELIVER. User never names a document or a skill.

## 0. Resume check
If `docs/` already has the numbered planning files, do not regenerate: read only what the task needs (see Token rules) and continue from `docs/11-ROADMAP.md` / `36-TODO.md`.

## 1. Plan (new project or large feature)
1. Understand the request; infer sensible defaults; ask only if a decision changes the product, has fundamentally different readings, a business rule is unknown, or rework would be large. Record each default in `docs/10-SCOPE.md` (decisions section).
2. Create the 38 files in `docs/` (names/order/content: `references/file-specs.md`; templates: `references/*-template.md`). Project-specific content only. If a file does not apply write `Status: Not Applicable` + one-line reason. Never invent requirements. Keep an existing docs structure if one exists.
3. Order: overview -> PRD -> features -> requirements -> roles -> flows -> use cases -> stories -> scope -> roadmap -> architecture -> stack -> database -> API -> auth -> RBAC -> security -> UI/UX -> design system -> routes -> components -> integrations -> payments -> email -> notifications -> errors -> validation -> testing -> deployment -> environment -> monitoring -> performance -> backup -> changelog -> todo -> bugs -> change requests.
4. Consistency audit (read all once): PRD=Features=Requirements; Requirements->Architecture->Database->API->Auth; Roles=RBAC; UI/UX=Routes=Components; Testing covers Features+Requirements; Deployment=Tech stack+Environment. Fix contradictions, gaps (missing entities, endpoints, routes, screens, validation, security, tests, env vars, integrations, errors, monitoring, backup).
5. Traceability: Requirement -> Feature -> Story -> UI -> API -> DB -> Test (table in `04-FEATURES.md` or `05-REQUIREMENTS.md`). No major feature without requirement, location, and test.
6. Gate (`references/development-checklist.md`): all critical items resolved before code.

## 2. Develop
- Phases (adapt): Foundation, Database, Backend/API, Auth/RBAC, Core features, Frontend, Integrations, Security, Testing, Performance, Deployment, Final QA.
- Docs are source of truth (priority: latest approved requirement > PRD > requirements > architecture > specs > code > tests). Do not invent features while coding. If implementation forces a change: update the affected doc and dependents first, then code. Code vs plan conflict: surface and resolve.
- Select the needed skills yourself from the library (database, backend, frontend, UI/UX, security, payments, analytics-visualization, testing, devops). Do not announce it.

## 3. Test and verify
Unit, integration, API, E2E (Playwright for web), regression, security, performance, responsive as applicable. Finish only after PLANNING vs IMPLEMENTATION vs TESTING check: every feature/requirement/route/API implemented, relations right, auth + permissions work, UI matches spec, errors/validation work, tests pass, production build works.

## 4. Change management
New feature request: find affected docs, features, DB, API, UI, tests -> update docs -> implement -> update changelog/todo.

## Token rules
Do not re-read all 38 files. Load by task: DB -> `14` + `05` + `12`; API -> `15` + `14` + `16` + `17`; UI -> `19` + `20` + `21` + `22`; auth -> `16` + `17` + `18`; payments -> `24` + `14` + `15`; deploy -> `30` + `31` + `13`; tests -> `29` + `04` + `05`.

## Output
Short `DONE`: docs created/updated, assumptions made, what was built and verified, open issues.
