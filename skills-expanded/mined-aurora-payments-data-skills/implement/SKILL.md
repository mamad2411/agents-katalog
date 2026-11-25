---
name: implement
description: "Implement a piece of pipeline work from a spec or tickets: models, tests, and a data diff against production."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

Use /tdd where possible, at pre-agreed seams.

Run a SQL linter plus a warehouse dry run regularly, which is free and catches broken SQL and column typos before any compute, and build single changed models into your dev schema regularly. At the end, run one state-selected build: everything modified plus its dependents, deferred against production (e.g. dbt: `dbt build --select state:modified+ --defer --state <prod-manifest>`), never a full rebuild.

Before review, diff the built data against production for every model you changed: row counts, schema, values (a data-diff tool where configured, e.g. `recce run`; targeted comparison queries otherwise). For models a registered dashboard reads, include the freshness columns in the diff, because a change that silently re-anchors the latest business period or the source load time breaks the surface's freshness element without failing any test. A pipeline failure is a plausible-wrong number, not a stack trace; the diff is the evidence the numbers moved on purpose. Carry it into review.

Once done, use /code-review to review the work.

Commit your work to the current branch.
