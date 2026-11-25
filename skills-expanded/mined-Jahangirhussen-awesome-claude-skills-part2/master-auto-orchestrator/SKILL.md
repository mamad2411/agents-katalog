---
name: master-auto-orchestrator
description: Use first for any meaningful task - building, fixing, auditing, researching, designing, optimizing, migrating, deploying, testing, automating or documenting. Silently identifies project type and task intent, selects the smallest sufficient set of skills from the master library (planner, SEO, analytics, development, AI, research, marketing, devops, security, testing, design, automation) via the registry, runs them in order, verifies, and returns only the result. The user never names a skill or types a slash command. Not needed for trivial one-line questions.
---

# Master Auto Orchestrator

## Purpose
Central router for the whole library. Turns a plain request into the right skill set and execution order without exposing the routing.

## When to use
Any non-trivial request. Especially multi-domain work (build + database + auth + UI + tests) or when unsure which skill applies.

## When NOT to use
- Trivial answers needing no skills.
- A skill is already running and the task is unchanged.

## Inputs
User request, repo/project evidence (package files, framework, `docs/`, structure), `AUTO-ROUTER.md`, `registry/<domain>.md`.

## Core workflow
1. Project: identify type(s) from the request and repo evidence; several are allowed.
2. Intent: build, fix, audit, research, design, optimize, migrate, deploy, test, automate, document, explain.
3. Candidates: `AUTO-ROUTER.md` (project -> domains), then grep `registry/<domain>.md` for trigger terms. Never open every registry file or every SKILL.md.
4. Choose the smallest sufficient set: specific child > specialized > subcategory > domain > general. Prefer canonical, more complete, lower-token skills; never load duplicates.
5. Dependencies: load only what the task needs.
6. Order: planning -> architecture -> database -> backend/API -> auth/RBAC -> business logic -> frontend -> integrations -> security -> testing -> performance -> deployment -> docs.
7. Special rules: substantial software "build" -> `universal-development-planner` first; any SEO -> `seo-master`; dashboards/KPIs/charts -> `erp-saas-analytics-visualization`; research/thesis -> research domain, no dev skills.
8. Execute, passing only relevant context between skills; add or drop skills as needs change.
9. Verify with the matching check; fix and re-check.
10. Report the result as a short `DONE`.

## Decision rules
- One skill if one is enough; 2-5 for moderate tasks; more only when genuinely required.
- Confidence HIGH: act. MEDIUM: act with the primary skill. LOW and wrong work is costly: ask one short question; otherwise do not ask.
- Existing repo: route from evidence, not wording.
- No registry match: search `registry/99-UNCLASSIFIED.md`, related skills, dependencies; otherwise say no adequate skill exists and use general capability. Never invent skills.

## Edge cases and failure handling
- Two skills conflict -> pick the more specific; note the conflict only if it changes the result.
- A selected skill's prerequisite is missing (account, tool) -> skip it, use the nearest alternative, state the limitation.
- Registry stale (skill moved) -> fall back to `master-skills/REGISTRY.md` or a filesystem search.

## Validation
Code -> tests; web UI -> browser/E2E + responsive; SEO -> crawl/schema/GSC checks; database -> migration check; research -> reproducibility; deploy -> health check.

## Output requirements
The actual result, not the routing. Short `DONE`: changes, evidence, open issues. Do not mention skill names or scores unless asked.

## Example
"Build me a multi-branch POS with roles and reports" -> planner (38 docs) -> POS/saas, DB, backend/API, auth/RBAC, UI/UX, analytics-visualization, security -> implement -> tests/E2E -> DONE.

## Related / dependencies
`AUTO-ROUTER.md`, `REGISTRY.md`, `registry/`, `references/` (legacy routing combos, domain checklists, dry-run notes), `universal-development-planner`, `seo-master`, `erp-saas-analytics-visualization`, `master-skills`.

## References
`references/project-routing-combos.md`, `references/domain-checklists.md`, `references/routing-dry-run.md`.
