---
name: bodylife-quality-gates
description: Implementation guidance for BodyLife CRM quality gates across the v1 roadmap. Use when Codex defines, adds, or reviews tests for domain rules, application commands, PostgreSQL integration, migrations, report consistency, audit matrix coverage, Playwright tablet/phone E2E, restore rehearsals, go-live checks, or milestone acceptance criteria.
---

# BodyLife Quality Gates

Use this skill whenever implementation needs proof, not just code. The risky parts of BodyLife CRM are membership math, command atomicity, audit, reports, PostgreSQL constraints, UI double submits, and restore readiness.

## Start Here

Read `references/source-map.md`, then pick the gate that matches the milestone or workflow.

## Gate Types

- Domain tests: inclusive dates, remaining visits, negative visits, first negative date, freeze/non-working union days, canceled facts, backdated entries, snapshot immutability.
- Application command tests: permissions, validation, idempotency, stale/concurrency behavior, transaction rollback, recalculation hook, business audit, canonical reread target.
- PostgreSQL integration tests: migrations, FKs/checks, partial unique indexes, row locks, source facts vs derived cache rebuild, report query indexes.
- Report consistency tests: daily totals equal drill-down rows, corrections/cancellations are visible, Memberships state matches profile and reports.
- Audit tests: event matrix coverage, required fields, append-only policy, shared account/session labeling, backfill/fallback labels.
- UI E2E tests: Playwright tablet and phone flows for search, profile, issue membership, mark/cancel visit, payment correction, freeze, daily report, audit/history, busy/disabled duplicate-submit behavior.
- Operations tests: health check, structured log correlation, PII masking review, restore rehearsal, restore-check, paper fallback reconciliation drill.

## Milestone Rule

Every milestone should finish in a deployable, testable state. Do not accept code that only works through manual DB edits, UI optimism, or untested assumptions about PostgreSQL/hosting.

## Minimum Regression Shape

- Run build/analyzers and unit tests.
- Run PostgreSQL-backed integration and migration checks for persistence changes.
- Run relevant command/domain/report tests for changed workflows.
- Run Playwright on tablet and phone viewports for reception UI changes.
- Run restore rehearsal checks before production readiness claims.

## Guardrails

- Do not use SQLite/EF InMemory as proof for production persistence behavior.
- Do not skip tests around recalculation, audit, reports, or idempotency because the UI looks right.
- Do not call production ready before backup retention is configured and restore rehearsal has passed.
- Do not approve reports that duplicate Memberships formulas.
- Do not accept command success when source facts, recalculation, audit, and canonical reread can diverge.
