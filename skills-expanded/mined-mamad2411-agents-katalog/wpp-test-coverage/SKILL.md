---
name: wpp-test-coverage
description: Authoritative test specification for the Warehouse Pick Path Optimizer (warehouse_pick_path) starter pack. Documents API endpoints, UI interactions, optimization flows, and infrastructure components. Split into phase-specific files.
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, WebFetch, Write, Edit
argument-hint: [section] (optional — "api", "ui", "infra", or omit to run all three)
---

# Warehouse Pick Path Optimizer — Test Coverage Specification

Source of truth for what to test on a deployed warehouse_pick_path stack. Covers the WPP frontend (React SPA served by `serve`), the FastAPI backend with NVIDIA cuOpt GPU solver, Oracle 26ai database, and OCI infrastructure.

**Frontend repo:** `oci-ai-incubations/oci-warehouse-pick-path-optimizer` — `frontend/` (React, Vite, served by `serve`)
**Backend repo:** `oci-ai-incubations/oci-warehouse-pick-path-optimizer` — `backend/` (FastAPI, NVIDIA cuOpt, Oracle 26ai)
**Deployment:** Terraform -> OKE -> Corrino Blueprint (2-service deployment group: backend + skin frontend)

---

## Test Files

| File | Phase | What it covers |
|---|---|---|
| [api-tests.md](api-tests.md) | Phase 6a | Backend API: health, auth, CSV upload, optimization, batch |
| [ui-tests.md](ui-tests.md) | Phase 6b | Frontend UI: login, setup, file upload, optimization run, results |
| [infra-tests.md](infra-tests.md) | Phase 5 | Pod health, service endpoints, ingress, Oracle 26ai connectivity |

## How to Use

Invoke with an optional section argument:

- `/wpp-test-coverage` — load all three files
- `/wpp-test-coverage api` — API tests only
- `/wpp-test-coverage ui` — UI tests only
- `/wpp-test-coverage infra` — infrastructure tests only

The `/testing-pack` skill references this specification during Phase 5-6 for warehouse_pick_path deployments.
