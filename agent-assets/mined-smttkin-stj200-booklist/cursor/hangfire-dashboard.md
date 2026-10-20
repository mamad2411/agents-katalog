---
description: Hangfire Dashboard stays on API port 5064 — do not relocate or re-lock
alwaysApply: true
---

# Hangfire Dashboard (API :5064)

- Hangfire Dashboard is served by the **BookList WebAPI** at path `/hangfire`.
- Canonical URL: **http://localhost:5064/hangfire** (Docker maps host `5064` → container `8080`).
- In Development (including Docker compose `ASPNETCORE_ENVIRONMENT=Development`), the dashboard uses `HangfireDashboardAllowFilter` so Docker/proxy access is not blocked by Hangfire’s default local-only auth.

## Do not change (unless the user explicitly asks)

- Do **not** move Hangfire off the API / port **5064**.
- Do **not** remove or replace `HangfireDashboardAllowFilter` with local-only auth in Development.
- Do **not** require Production or a different host/port for the dashboard in the Docker-dev stack.
- Frontend nginx `/hangfire` proxy may exist as a convenience; the **source of truth** remains the API on **5064**.
