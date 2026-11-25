---
name: sql-apps-validation
description: "Use when validating SQL Apps changes or collecting test, browser, SQL, access, ownership, or deployment evidence."
---

# Validate SQL Apps

Resolve `../../scripts/sql-apps.mjs` relative to this skill, not cwd. Quote its
absolute path; `home` selects the checkout containing input `docs/...`.
Inspect `package.json`: `sqlApps.project` identifies generated apps. Choose the smallest covering check; full suite only when warranted.

## Generated applications

After restore: `npm run build`, `npm run app:check`, declared tests and `npx --no-install tsc --noEmit`. Approved API checks: `npm run app:check-api -- "<verified-origin>"`. No copied foundation scripts, invented commands, new runners or project switching; report missing checks.

## Foundation and plugin maintenance

Foundation only: use declared `npm run plugin:check`, `npm run typecheck` and
relevant tests. Targeted passes are not full-suite passes.

Use `docs/maintainers/application-boundary.md` for source, SQL model and live API/database absence checks in either target.

## Live workflow evidence

For approved running local apps, run sequential launcher checks: `app-check` (clean database), `test` (read-only SQL), `app-test` (Development Alice admitted, Bob 403). Fixture writes/restarts need documented approval; startup belongs to `sql-apps-local`. Cloud probes follow the publisher contract.

Apply **Domain contracts and live acceptance** from the boundary reference:

- Use unique synthetic fixtures and owned sessions; snapshot preexisting records and remove only this run's fixtures.
- Supply the expected Origin and authorization. Pair invalid/foreign writes with a positive control; prove rejected writes leave data unchanged.
- Verify a real browser action, initial-load failure, failed-save retention and SQL save/reload. Reload means a new browser document and refetched SQL state.

Unavailable input/services/tools mean missing evidence. Forced DOM clicks, mocks, source review, health and compilation do not prove workflows.

For performance work or changed reads, apply `docs/reference/read-performance.md` for comparable before/after measurements, sample counts and correctness checks. Report unobserved performance as missing evidence within functional acceptance.

## Rendered browser review

Keep API/SQL acceptance, real browser workflow acceptance and rendered visual review distinct. Screenshots do not prove persistence/access; compile/API results do not prove visuals.

For new apps and meaningful UI changes, run `sql-apps-design`'s render-critique-improve loop before broad coverage. Verify the intended origin; use semantic browser inspection and real interactions. Never invent or confuse page/instance handles. Inspect desktop and narrow widths; if tooling fails, discover supported alternatives. Source review or opening a tab is not visual review. If blocked, state exact evidence not observed separately from user-reported feedback.

Record origin, source/build, viewport, state, artifact, findings/re-review in `docs/design-review.md` per `docs/reference/design-acceptance.md`; run `sql-apps check`. Progressive Ready additionally requires `creation accept` with retained current evidence; see `docs/reference/progressive-creation.md`.

## Four-verdict report

Record exact commands/results and four independent lines:

- **Implemented/built:** source/build evidence.
- **Running:** intended origin/readiness.
- **Functional acceptance:** accepted, partial or blocked, with browser/API/SQL evidence.
- **Design acceptance:** accepted, partial or blocked, reporting rendered coverage and design quality separately; a complete matrix is not a quality verdict.

Historical checkpoints and local simulation do not prove current cloud identity, networking or authorization.
