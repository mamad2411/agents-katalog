---
name: sql-apps-diagnostics
description: "Use when a SQL Apps workflow fails or reads are slow, including local startup, readiness, SQL/DAB, authorization, API or persistence."
---

# Diagnose SQL Apps

Resolve `../../scripts/sql-apps.mjs` relative to this skill, not cwd. Quote its
absolute path; `home` selects the app containing input `docs/...`.
Confirm it with `workspace-check`; use bounded, project-owned evidence.

## Diagnose the selected app

Use `sql-apps-local` for workspace/readiness and safe lifecycle actions. Reproduce failures; pair negative authorization/input probes with a positive control. Verify fixes with `sql-apps-validation`.

For slow reads, follow `docs/reference/read-performance.md`: isolate browser/request/API-DAB/SQL/consumption timing before database escalation.

Collect read-only; never print tokens, credentials, environment variables or private files. Liveness is not acceptance. Preserve records; writes, resets, grants, installation and destructive recovery need explicit approval.

## Escalate the isolated issue

Load specialists only for evidenced boundaries; report unavailable companions, never duplicate their diagnostics.

- Slow SQL: `diagnose-slow-query`; plans: `read-execution-plan`; blocking: `diagnose-blocking-and-deadlocks`; resource/governance pressure: `diagnose-resource-pressure`.
- Publishing/cost guards: `sql-apps-cloud-preview`.
- Azure incidents: `azure-diagnostics`; platform costs: `azure-cost-optimization`.
- Cloud SQL connections: `diagnose-connection-errors`; local preview: `azuresql-db-faq`.
- DAB exposure/configuration: `dab-rest-and-graphql` or `azuresql-db-dab`, matching target.
