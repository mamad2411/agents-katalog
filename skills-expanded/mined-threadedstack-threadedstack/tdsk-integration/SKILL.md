---
name: "tdsk-integration"
description: "Knowledge base for the end to end integration tests across all services and applications"
---

# Integration Testing Skill

## Directory Structure

```
repos/integration/
├── configs/
│   └── vitest.config.ts              # maxForks 8, 120s timeout
├── playwright/
│   ├── utils/crud-helpers.ts         # Shared helpers (openDrawer, fillField, submitForm, searchInPage)
│   └── tier2/                        # E2E browser tests
│       ├── crud-sandboxes.spec.ts
│       ├── sandbox-connect-modal.spec.ts
│       └── sandbox-drawer-fields.spec.ts
└── src/
    ├── utils/
    │   ├── api-client.ts             # Typed fetch wrapper with Bearer auth
    │   ├── env.ts                    # TDSK_IT_* environment variables
    │   ├── jwt-auth.ts              # JWT acquisition from Neon Auth
    │   └── sandbox-helpers.ts        # Pod lifecycle helpers
    ├── tier1/                        # API contract tests
    └── tier3/                        # Live infrastructure tests
```

## Running Tests

```bash
cd repos/integration

# Full API test suite (tier1 + tier3, requires K8s)
pnpm test

# Single test file
npx vitest run --config configs/vitest.config.ts src/tier3/sandbox-connect.test.ts

# Playwright E2E tests only (tier2, requires admin UI running)
pnpm test:ui

# All tests (API + Playwright)
pnpm test:all
```

**GOTCHA**: Do NOT put `--` before the file path when running vitest directly -- it causes vitest to ignore the file filter and run ALL tests. The `--` is only for `pnpm` script passthrough: `pnpm test:api -- src/tier3/<file>.test.ts`

## Prerequisites

The K8s services are always running and local changes are automatically synced into the running containers. If needed the services can be restart with `tdsk dev start --clean` for K8s (Backend :5885, Proxy :7118), `cd repos/admin && pnpm start` for Admin UI (:5887), and `cd repos/threads && pnpm start` for Threads UI (:5886).

## Authentication

API key auth bypasses social login for automated testing. The proxy accepts `Authorization: Bearer tdsk_*` tokens. Direct backend access uses `X-User-Id` + `tdsk-backend` headers.

## Test Utilities

**`api-client.ts`**: Typed fetch wrapper with `get()`, `post()`, `put()`, `del()` shortcuts. Auto-prefixes `/_` for admin routes. Returns `{ status, ok, data }`.

**`jwt-auth.ts`**: Acquires real JWT from Neon Auth via email sign-in. Uses `TDSK_IT_AUTH_URL`, `TDSK_IT_USER_EMAIL`, `TDSK_IT_USER_PASSWORD`. Required for org creation tests.

**`env.ts`**: `TDSK_IT_API_KEY`, `TDSK_IT_ORG_ID`, `TDSK_IT_AUTH_URL`, `TDSK_IT_USER_EMAIL`, `TDSK_IT_USER_PASSWORD`, `TDSK_IT_PROVIDER_KEY`, `TDSK_IT_AGENT_ID`, `TDSK_IT_ZAI_AGENT_ID`, `TDSK_IT_PROJECT_ID`, `TDSK_IT_USER_ID`.

**`sandbox-helpers.ts`**: `waitForPodState()` (poll until Running/Failed), `execInPod()`, `getPodSubdomain()`, `connectSandbox()`, `getSessions()`, `setupRunningPod()` (full lifecycle: project → sandbox → pod → wait), `cleanupSandbox()` (best-effort teardown).

## Tier 1 -- API Contract Tests

Direct API calls validating CRUD envelopes, auth, and field persistence. No UI.

- `sandbox-config-crud.test.ts` — CRUD with projectId, SSH, git, idle timeout, builtIn fields
- `sandbox-runtime-crud.test.ts` — Runtime enum, runtimeCommand, initScript, builtIn enforcement, copy endpoint
- `sandbox-org-seeding.test.ts` — JWT auth org creation, 6 built-in preset verification
- `tsa-sandbox-client.test.ts` — TSA ApiClient.listSandboxes() against live backend

## Tier 2 -- Playwright E2E Tests

Headless browser tests for UI workflows. Require admin UI running.

- `crud-sandboxes.spec.ts` — Create/read/update/delete sandbox via DataTable
- `sandbox-connect-modal.spec.ts` — ConnectModal: SSH command, VS Code config, sessions
- `sandbox-drawer-fields.spec.ts` — Form fields: SSH toggle, image presets, git accordion, idle timeout

## Tier 3 -- Live Infrastructure Tests

Real K8s pods (The K8s services are always running), networking, SSH tunneling. ~2 min per spec.

- `sandbox-connect.test.ts` — POST `/connect` auto-start, concurrent deduplication
- `sandbox-route-cleanup.test.ts` — Stale route cleanup, subdomain proxy, WebSocket after cleanup
- `sandbox-runtime-pod.test.ts` — `TDSK_RUNTIME`/`TDSK_RUNTIME_CMD` env vars on live pods
- `sandbox-sessions.test.ts` — GET `/sessions` endpoint
- `sandbox-tunnel.test.ts` — WebSocket SSH tunnel, auth validation, session tracking
