---
name: auth-testing
description: >-
  How to test this repo at every layer: backend unit (Vitest), backend HTTP e2e (Vitest + Supertest,
  in-memory or real MongoDB), frontend unit/integration (Vitest + Testing Library with a fetch fake). Use
  whenever adding or changing behaviour, or fixing a bug (write the failing test first).
---

# Testing conventions

## Backend (`backend/`)

| Layer      | Where                                | How                                                                                                                                       |
| ---------- | ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Pure rules | `src/**/*.spec.ts` next to the file  | Vitest, table-driven `it.each`                                                                                                            |
| Services   | `src/modules/**/<x>.service.spec.ts` | `Test.createTestingModule` with the **real in-memory adapter** for the port. Stub only slow/external things (argon2 via `PasswordHasher`) |
| HTTP e2e   | `test/*.e2e-spec.ts`                 | Boot `AppModule.forRoot()` + `configureApp(app)` (same as prod), drive with Supertest. Env defaults in `vitest.config.e2e.ts`             |

- Backend is ESM: import with `.js` suffixes, use `vi.fn()`/`vi.spyOn()` (globals enabled).
- e2e defaults to `DB_DRIVER=memory`. Run it again with `DB_DRIVER=mongo` against a real MongoDB (`docker compose up -d mongo`) before merging persistence changes. Adapter behaviour must match exactly.
- Assert behaviour (status codes, body shape, cookies, "secrets never in body") over mock call counts.
- Every auth change covers the success path, each validation rule, and each failure (401, 409, reuse detection, missing cookie).
- Run: `npm test`, `npm run test:e2e`, `DB_DRIVER=mongo MONGODB_URI=mongodb://localhost:27017/x npm run test:e2e`.

## Frontend (`frontend/`)

| Layer      | Where                         | How                                                          |
| ---------- | ----------------------------- | ------------------------------------------------------------ |
| Schemas    | `features/**/schemas.test.ts` | `safeParse`, `it.each` per rule                              |
| API client | `api/client.test.ts`          | `mockApi({...})` fetch fake: refresh, replay, single-flight  |
| Flows      | `features/**/*.test.tsx`      | `renderApp('/path')` (real router + providers) + `userEvent` |

- `mockApi` (in `src/test/utils.tsx`) throws on unhandled requests, so declare every endpoint the flow calls, including `POST /api/auth/refresh` (fired on app load).
- Query by role/label (`getByLabelText('Email')`, `getByRole('button', { name })`), not by class names.
- Run: `npm test` (`npm run test:watch` while developing).
