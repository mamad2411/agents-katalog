---
name: sql-apps-application
description: "Use when defining or changing a SQL Apps application, screen, client operation, API procedure, schema, or access rule."
---

# Build the application

Resolve `../../scripts/sql-apps.mjs` relative to this skill, not cwd. Quote its
absolute path; `home` selects the project containing input `docs/...`.
Review `projects create-plan "<name>"`, obtain approval, then
`projects create "<name>" --approval <id>`. Edit only the generated project.
`SQL_APPS_HOME` selects runtime, not skills.

## Agree on one useful slice

Read the saved brief with `guide`; the requested change is the useful slice. Ask only about missing users/access, fields, actions, validation or outcomes one question at a time. Summarize decisions/exclusions without repetition.

Consult `docs/guides/build-your-app.md` for unresolved scope; apply `docs/maintainers/application-boundary.md` before edits.

Keep `application.json` named for the app with `selectedExamples: []`. Use only `role-based-data`, capabilities `["data"]`. No copied examples, alternate runtime or unrequested capabilities. File storage/jobs belong outside SQL Apps, using maintained Azure skills.

Before implementing a new user-facing app or meaningful UI change, use `sql-apps-design`. Keep database and access decisions separate from visuals. A basic shell is an implementation milestone, not final design acceptance: small scope, not unfinished visual quality.

## Implement the slice

Reuse runtime/client/DAB/SQL. Apply the boundary's **Domain contracts and live acceptance**: text limits, exact values, mutation ordering, readiness and positive controls.

Use project-owned domain source and typed `@microsoft/sql-apps/browser` helpers;
never copy foundation runtime/scripts/infrastructure or edit installed tooling.

- Define the configured role and allowed member types.
- Expose only required procedures; the gateway chooses the DAB role from validated claims.
- Reject caller-supplied role escalation; preserve agreed owner isolation.

Verify browser save, fresh-document reload and visible failed-save feedback before
expanding. Product screens show account/access, never persona selectors.
Developer-page simulations do not prove Entra assignment or cloud tokens;
label mock/synthetic behavior.

For list/search/dashboard/detail reads, apply `docs/reference/read-performance.md`: bounds, ordering, freshness, latency and redundant requests. Preserve authorization and read-after-write; cache proposals need separate review.

## Check the application boundary

Use `sql-apps-validation` for checks, live evidence and required rendered browser review; follow its four-verdict report and repeat changed/original workflows.

Remove tests importing excluded examples; do not restore them. Report legacy database objects retained by non-destructive publishing; cleanup needs separate review and approval.

Use `sql-apps-local` for startup/resume and `sql-apps-cloud-preview` only for requested sharing.
