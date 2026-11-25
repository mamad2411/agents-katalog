---
name: testing-bun
description: CRITICAL - Invoke BEFORE writing ANY test code. Use when creating new tests, adding test cases, modifying or removing existing tests, writing `it()` or `describe()` blocks, touching any `*.test.ts` or `*.spec.ts` file, or running the mutation-testing kill matrix. Enforces no try-catch in positive tests, no early returns, no test skipping, and that every test catches something no other test catches.
allowed-tools: [Read, Edit, Grep, Glob, Bash]
---

# Testing Standards (Bun)

## Framework
- Use `bun:test` imports (`describe`, `test`, `expect`, etc.)
- Use Bun test runner, typically via workspace scripts (`bun run test`)
- Do not introduce Vitest or Jest in this repo
- For local e2e/integration runs, provide required env vars through the shell or `.env`

## Test Strategy
- **Default to API integration tests against real infrastructure** (real Postgres, real ClickHouse). Call a real endpoint, let data flow through the API into the DB, then verify by calling another endpoint. This is "e2e" from the API perspective only — frontend is out of scope here.
- **Never mock services, DB clients, or external APIs.** If a test would need a mock, write the integration test instead.
- **Unit tests are reserved for pure logical utilities** (parsers, formatters, pure functions). A service that "needs" a unit test is a smell — prefer the integration path above.

## Critical Rules

### 1. No Try/Catch in Positive Tests
```ts
// Bad - Hides real errors
test('creates user', async () => {
  try {
    const user = await createUser(input)
    expect(user.id).toBeDefined()
  } catch (error) {
    console.error(error)
  }
})

// Good - Let test framework handle errors
test('creates user', async () => {
  const user = await createUser(input)
  expect(user.id).toBeDefined()
})

// Good - Only for testing expected failures
test('rejects invalid input', async () => {
  await expect(createUser(invalid)).rejects.toThrow('Invalid email')
})
```

### 2. No Early Returns in Tests
```ts
// Bad - Silently skips test
test('calls API', async () => {
  if (!hasCredentials) return
  await callApi()
})

// Good - Fail when preconditions missing
test('calls API', async () => {
  expect(hasCredentials).toBe(true)
  await callApi()
})
```

### 3. No Hidden Skips for Missing Env Vars
```ts
// Bad
describe.skipIf(!process.env.CLICKHOUSE_URL)('integration', () => {})

// Bad
if (!process.env.CLICKHOUSE_URL) {
  test.skip('requires CLICKHOUSE_URL', () => {})
}

// Good - Let tests fail if env not configured
describe('integration', () => {
  const url = process.env.CLICKHOUSE_URL
  expect(url).toBeTruthy()
})
```

### 4. E2E Policy (Mandatory)
- E2E tests must never be conditional on env availability
- Never use `skip`, `skipIf`, guard `return`, or branching that bypasses e2e execution when env vars are absent
- Missing required env vars must cause test failure immediately
- Local e2e execution must provide the required vars through the shell or `.env`

```bash
# Required local command for env-dependent suites
bun run test:integration
```

### 5. Prefer Inline Setup Over `beforeEach`
```ts
// Bad - Unnecessary beforeEach
describe('Tests', () => {
  let queryBuilder: QueryBuilder
  beforeEach(() => {
    queryBuilder = new QueryBuilder(schema)
  })
})

// Good - Inline initialization
describe('Tests', () => {
  const queryBuilder = new QueryBuilder(schema)
})

// Good - Use beforeEach only for async cleanup
beforeEach(async () => {
  await client.query('DELETE FROM test_table')
})
```

## Best Practices

### Use assert() for Type Narrowing
```ts
// Good - Provides type narrowing
assert(checkoutRecord)
```

### Keep Tests Deterministic and Isolated
- Prefer plain `test(...)` blocks with explicit setup
- Use package-level scripts (`bun test src`) for focused runs when needed

## Every Test Earns Its Place (Kill Matrix)
Keep a test only if it catches something no other test catches. Prove it with the mutation-testing kill matrix before adding tests to a module, and when trimming its suite:

```bash
bun run test:kill-matrix apps/desktop/server/src/services/analysis/find-cursor.ts
# Several modules, explicit test files, options, extra `bun test` flags after --
bun run test:kill-matrix <module.ts>... [--test <file.test.ts>]... [--jobs <n>] [--timeout-ms <n>] [--json <out.json>] [-- <bun test flags>]
```

- Paths are relative to the repo root. Without `--test`, each module's sibling `<name>.test.ts` is used.
- Every mutant (swapped arithmetic, comparison, equality and logical operators, flipped booleans, negated conditions, changed literals, removed statements, `return undefined`) runs against every test alone (`bun test <file> --test-name-pattern '^<name>$'`), so the matrix records exactly which tests kill it. A run past the time limit counts as a kill.
- Mutants reach the tests through a `bun test --preload` hook; no file on disk is written, so an interrupted run leaves nothing behind.
- The report lists the matrix, kills and unique kills per test, **Tests that kill no unique mutant**, **Removable together**, and the survived mutants.
- Remove the tests under **Removable together**, then rerun: the killed count must not drop. Not every test without a unique kill can go: two tests that catch the same mutant both lack a unique kill, but one of them must stay.
- The matrix only knows the modules you pass. Before removing a test that also exercises other modules, pass those too (`<a.ts> <b.ts> --test <file.test.ts>`): it may be their only killer. The git cursor test in `find-cursor.test.ts` kills nothing unique in `find-cursor.ts` but 9 mutants of `packages/api-routes/src/analysis.ts`.
- A survived mutant is behaviour no test checks. Add a test only if that behaviour matters; some mutants change nothing observable.
- Test names must be static string literals, unique in their file. `test.each` and `test.if` cannot be attributed and are refused.
- Cost is one `bun test` process per mutant and test (find-cursor: 107 mutants × 5 tests in about 25 s with 5 jobs). Run it on unit-tested modules, not integration suites.

## Environment Variables
When adding new env vars for tests, update:
1. Package's `turbo.json` → `passThroughEnv` array
2. `.github/workflows/ci.yml` → `env` section
3. Run local e2e/integration suites with `bun run test:integration`
4. Treat missing vars as a hard failure, not a skip path
