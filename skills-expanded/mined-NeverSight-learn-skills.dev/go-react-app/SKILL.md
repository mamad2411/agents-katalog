---
name: go-react-app
description: Full-stack development constitution for Go+React projects. Covers OpenAPI-first design (ogen for Go, orval for React), integration testing with real PostgreSQL (no mocks), Playwright E2E testing against real backend APIs, service layer architecture with builder pattern, test-first development workflow, Playwright E2E infrastructure setup with AI-friendly reporter, and go-bus for async jobs and pub/sub messaging. Use this skill whenever working on a Go+React full-stack project, writing Go integration tests, implementing ogen handlers, setting up orval code generation, writing or fixing Playwright E2E tests against a real backend, designing service architecture with dependency injection, following OpenAPI-first API development, setting up Playwright in a new or existing project, configuring E2E test infrastructure, creating test helpers and AI reporters, implementing async jobs, background workers, pub/sub messaging, event-driven architecture, or when the user mentions project constitution, schema-first design, ServeHTTP testing, testcontainers, cmp.Diff assertions, AI-friendly test reporting, console error capture, E2E testing setup, go-bus, pgbus, message queues, or event publishing.
---

## Overview

This is the project constitution for full-stack applications with a Go backend and React frontend. Both sides share an OpenAPI specification as the single source of truth.

The constitution has two parts:
- **Go Backend** — Read `references/go-backend.md` for testing principles, service architecture, error handling, and development workflow
- **Frontend React** — Read `references/frontend-react.md` for E2E testing discipline, UI patterns, state management, and OpenAPI integration

## Core Philosophy

**When in doubt**: integration test over unit test, real database over mock, real API over stub.

## External Service Integration

When integrating third-party services (SaaS APIs, cloud platform APIs, payment providers, email services, etc.), always test against a real-compatible local server — never stub at the code level.

**Priority order:**

1. **Research locally installable API-compatible alternatives first** — Many services have open-source drop-in replacements that implement the exact same API (e.g., MinIO for S3, LocalStack for AWS, Mailpit for SMTP, fake-gcs-server for Google Cloud Storage). Use these in tests via testcontainers or docker-compose.

2. **If no compatible local server exists, build a Go mock server in the project** — Research the service's API contract (OpenAPI spec, REST docs, SDK source) and implement a lightweight HTTP server that responds with the same endpoints, request/response shapes, headers, and status codes. Place it in `backend/testutil/mock_<service>.go` or `backend/testutil/mock<Service>/`. The mock server runs as an `httptest.Server` in tests and the real service URL is swapped via configuration.

**The goal**: your application code uses the same HTTP client and configuration for both the mock and real service. Switching environments is a URL change, not a code change. Read `references/go-backend.md` (External Service Integration section) for implementation patterns and examples.

## Development Workflow (Mandatory Order)

For each user story, execute tasks in this exact order:

1. **Define OpenAPI Spec** — Add endpoints/schemas to `api/openapi/<domain>.yaml`
2. **Generate Code (both sides)**:
   - Backend: `cd backend && go generate ./...`
   - Frontend: `cd frontend && pnpm api:generate`
3. **Write Backend Tests** — Create failing integration tests in `backend/tests/`
4. **Implement Backend** — Write minimal Go code to make tests pass
5. **Write Frontend E2E Tests** — Create failing Playwright tests in `frontend/tests/e2e/`
6. **Implement Frontend** — Build UI components using generated React Query hooks
7. **Verify All Tests Pass** — Run both backend and frontend test suites
8. **Refactor** — Clean up code while keeping tests green

No implementation before tests. Run tests after every code change.

## Project Structure

```
api/
└── openapi/                  # OpenAPI specifications (shared source of truth)
    └── <domain>.yaml
backend/                      # Go backend application
├── api/gen/<domain>/         # ogen generated Go types and server
├── services/                 # Implements ogen Handler interface + domain services
├── handlers/                 # Server setup with ErrorHandler
├── internal/                 # Internal models, config
├── cmd/api/main.go
├── tests/                    # Go integration tests
frontend/                     # React frontend application
├── src/
│   ├── api/generated/        # Orval generated TypeScript types and hooks
│   ├── components/           # Reusable UI components (shadcn/ui)
│   ├── features/             # Feature-specific components
│   ├── routes/               # TanStack Router file-based routes
│   ├── hooks/                # Custom React hooks
│   ├── stores/               # Zustand stores
├── tests/e2e/                # Playwright E2E tests (against real backend)
│   └── utils/                # Test utilities, page objects
├── playwright.config.ts
├── orval.config.ts
```

## Technology Stack

### Backend
- Go 1.22+, PostgreSQL 15+
- ogen (OpenAPI -> Go code generation)
- GORM (database access)
- go-bus/pgbus (async jobs, pub/sub messaging)
- testcontainers-go (test database lifecycle)
- google/go-cmp (struct assertions)
- OpenTelemetry (distributed tracing)

### Frontend
- TypeScript ~5.9 (strict mode), React 19, Vite 8
- orval ^8.5 (OpenAPI -> TypeScript/React Query hooks)
- TanStack Query ^5.90, TanStack Router ^1.132
- shadcn/ui + Tailwind CSS ^4.1
- Zustand ^5.0 (client state)
- Playwright ^1.57 (E2E tests)
- React Hook Form + Zod (forms)

## Quality Gates

```bash
# Backend
cd backend && go test -v -race ./...

# Frontend
cd frontend && pnpm tsc --noEmit && pnpm test
```

- All backend integration tests pass with race detector
- All frontend E2E tests pass against real backend
- TypeScript compiles with zero errors
- Generated code is up-to-date
- No `any` types without explicit justification
- Never edit generated files (`frontend/src/api/generated/` or `backend/api/gen/`)

## OpenAPI-First Design

The OpenAPI spec is the single source of truth shared between Go backend (ogen) and React frontend (orval).

### Naming Conventions
- Paths: plural nouns, lowercase, kebab-case
- JSON fields and query params: camelCase
- Schema names: PascalCase
- `operationId`: camelCase verb + resource (e.g., `listUsers`, `getUser`)
- Enum values: lowercase or kebab-case
- IDs: always strings in API contracts

### Response Envelope
- Success: `{ data: ... }` (optional `meta`)
- Errors (non-2xx): `{ error: { code, message, details? } }`

### After OpenAPI Changes
```bash
cd backend && go generate ./...          # Update ogen types
cd frontend && pnpm api:generate         # Update orval types
```

## Root Cause Tracing

This applies to both backend and frontend:

1. **Reproduce** — Create reliable reproduction case (failing test)
2. **Observe** — Gather evidence through logs, debugger, tests
3. **Hypothesize** — Form theories about root cause
4. **Test** — Design experiments to validate/invalidate hypotheses
5. **Fix** — Implement fix addressing root cause, not symptoms
6. **Verify** — Ensure fix works and doesn't break existing functionality

Never weaken tests to make them pass. Never use `test.skip()`. Never revert to "simpler" approaches that avoid the actual issue. Never give up after initial failures.

## Bug Fix Flow

1. **Capture** the failing request (curl, error logs, user report)
2. **Write a failing reproduction test FIRST** — integration test for backend, E2E for frontend
3. **Verify the test fails** with the reported error
4. **Root cause analysis** — trace backward through call chain
5. **Fix at the source** — not symptoms
6. **Run full test suite** to verify no regressions

Test naming: `"BUG-<ID>: <brief description>"`

## Reference Files

- `references/go-backend.md` — Go backend testing principles, service architecture, error handling, code examples. Read when working on Go backend code.
- `references/go-bus.md` — go-bus async jobs and pub/sub messaging guide. Read when implementing async jobs, background workers, pub/sub messaging, event-driven patterns, or saga workflows.
- `references/frontend-react.md` — Frontend E2E testing discipline, Playwright setup and infrastructure, AI reporter, test helpers, UI principles, selector strategy. Read when working on React frontend code or setting up Playwright E2E testing.
- `references/playwright.config.ts` — Production-ready Playwright config with fast-fail timeouts. Copy to project root `playwright.config.ts`.
- `references/ai-reporter.ts` — AI-friendly Playwright reporter that outputs structured debugging context on failure. Copy to `tests/e2e/utils/ai-reporter.ts`.
- `references/test-helpers.ts` — Extended Playwright test with automatic debug capture fixtures. Copy to `tests/e2e/utils/test-helpers.ts`.
