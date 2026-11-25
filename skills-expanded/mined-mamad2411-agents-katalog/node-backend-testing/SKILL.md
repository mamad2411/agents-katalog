---
name: node-backend-testing
description: Testing strategy and workflow guide for Node.js backends using Mocha, Chai, Supertest, Rewiremock, and Docker Compose. Covers test execution, mocking and integration test authoring.
---

# Node Backend Testing

Use this skill when working on or reviewing tests in a Node.js/TypeScript backend project that follows the Mocha + Chai + Supertest + Rewiremock stack.

## Running Tests

Always run the full test suite through Docker Compose — never run `npm run test` directly outside the container, as the test database and dependent services are managed by Docker:

```bash
docker compose up dev_test
```

The `dev_test` service starts the test PostgreSQL database, applies migrations, seeds data, runs the suite, and exits. It depends on `postgres_test` being healthy and `install` having completed.

## Test Stack

| Tool | Purpose |
| --- | --- |
| Mocha | Test runner (parallel, 2 jobs, 30 s timeout, dot reporter) |
| Chai | Assertion library (`expect`) |
| Supertest | HTTP endpoint testing |
| Superwstest | WebSocket endpoint testing (when applicable) |
| Rewiremock | Module-level service mocking |

Configuration lives in `.mocharc.js`. Global setup and teardown is in `tests/global.ts`.

## Test File Conventions

- Test files must end with `.test.ts`
- Place test files under `tests/cases/` mirroring the source domain:
  - `tests/cases/api/v1/...` for REST endpoints
  - `tests/cases/websocketApi/...` for WebSocket handlers
  - `tests/cases/utils/...` for utilities
  - `tests/cases/scheduler/...` for scheduled jobs

## Integration Test Pattern

Each test file makes real HTTP calls via Supertest against a live app instance backed by an isolated test database. No manual per-test DB cleanup is needed — the global hooks handle it.

```typescript
import supertest from 'supertest'
import { expect } from 'chai'
import app from '../../../../../src/app'

const endpoint = '/api/v1/resource'

describe(`[POST] ${endpoint}`, () => {
  const request = supertest(app)

  it('returns 401 when unauthenticated', async () => {
    const response = await request.post(endpoint).send({})
    expect(response.status).to.eq(401)
  })

  it('returns 200 with valid payload', async () => {
    const response = await request
      .post(endpoint)
      .set('Authorization', `Bearer ${token}`)
      .send({ /* ... */ })
    expect(response.status).to.eq(200)
    // Validate response shape against the controller's responseSchema when available
    const { error } = responseSchema.validate(response.body)
    expect(error).to.eq(undefined)
  })
})
```

Always cover:

- Auth / authorization failure paths (401, 403)
- Validation failure paths (400/422)
- Success path with response shape assertion

## Database Isolation

`tests/global.ts` implements per-worker database isolation:

- `mochaGlobalSetup`: validates the test DB URL points to localhost, authenticates, syncs schema, runs seeders
- `mochaGlobalTeardown`: drops all worker databases matching `${testDatabaseName}_%` and closes the connection
- `mochaHooks` (per suite): drops the worker's database and clones a fresh one from the template before each suite

## Mock Patterns

External and third-party services are mocked at module level via Rewiremock. Mocks are registered in `tests/global.ts` and implementations live in:

- `tests/__mocks__/` — third-party library mocks (e.g. `@sentry/node`, `nodemailer`)
- `src/services/**/__mocks__/` — internal service mocks

### Rules for mocks

- Keep mock exports structurally aligned with the real service (same function names and return shapes)
- All mocked async methods return resolved promises by default
- When adding a new service call to a controller, verify a matching mock exists before writing tests
- For Axios-style services, mock all HTTP methods used: `get`, `post`, `put`, `patch`, `delete`
- For wrapped SDK clients (e.g. Redis), mock the specific methods called and match expected return shapes
- Do not use underscore-prefixed parameter names (`_param`) in mock implementations; omit unused params instead
- Register new mocks in `tests/global.ts` when they are module-level dependencies loaded at import time

### Adding a new service mock

1. Create the mock file at `src/services/__mocks__/myService.ts` (or equivalent path)
2. Export the same function names as the real service, returning resolved promises with expected shapes
3. Register in `tests/global.ts`:

   ```typescript
   rewiremock('../src/services/myService').by('../src/services/__mocks__/myService')
   ```

## Integration Test Authoring Workflow

When generating or updating integration tests for a controller:

1. Read the controller file and list all external/internal service calls made
2. Read the real service files and note their exported function signatures
3. Verify matching mocks exist in the appropriate `__mocks__/` directory
4. Add or update mock functions to expose the same names and return the expected shapes
5. Register new mocks in `tests/global.ts` if not already wired
6. Write tests covering auth, validation, and response structure assertions
7. Run `docker compose up dev_test` to confirm tests pass end-to-end

## Quality Gate

Before finalizing any change that touches business logic:

- Run `docker compose up dev_test` and confirm all tests pass
- Add or update tests for every behavior change