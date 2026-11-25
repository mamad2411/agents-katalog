---
name: principles-tdd
description: Applies test-driven development discipline and defines the unit/integration/e2e test tier conventions. Invoked when an engineer is writing tests, practicing TDD, working test-first, implementing any behavior before or alongside writing tests, choosing between unit vs integration vs e2e tests, writing integration tests with Docker or LocalStack, setting up Playwright e2e tests, naming test files, using build tags for Go tests, go:build integration or e2e constraints, or testify suite lifecycle hooks (SetupSuite, SetupTest, TearDownTest, TearDownSuite). Governs red/green/refactor rhythm, test scope, test tiers, and when to commit. Cross-references superpowers test-driven-development for deeper guidance.
---

# TDD Principle

Write tests first. Every behavior change starts with a failing test.

## Process

**Red — write a failing test.**
Name the behavior you intend to add. Run the test suite and confirm it fails for the right reason (missing behavior, not a compile error or wrong assertion).

**Green — implement the minimum to pass.**
Write only enough production code to make the test pass. Resist the urge to generalize.

**Refactor — clean under green.**
Improve structure and remove duplication while the suite stays green. No new behavior during refactor.

**Behavior, not implementation.**
Tests assert observable outputs and side-effects, not internal wiring. Coupling tests to implementation details makes refactors painful and destroys the feedback loop.

**Fast and deterministic.**
Tests must pass or fail in milliseconds and return the same result on every run. Flaky or slow tests erode trust and get skipped.

**Isolate external dependencies via interfaces.**
Use ports/adapters (interfaces + test doubles) to keep tests free of I/O, clocks, randomness, and third-party services. See `principles-pragmatic-solid` for the interface discipline that makes this cheap.

**Commit at green.**
Each green bar is a known-good checkpoint. Commit before refactoring so you can roll back cheaply if the refactor breaks things.

## Test naming — Subject_Scenario_Expectation

**Every test case, in every language, is named `Subject_Scenario_Expectation`** (Roy Osherove xUnit three-part style). The name alone must identify the failure in CI without opening the source file. Add a one-line intent description alongside each case.

- **Subject** — the unit under test (class, function, component, page, or route).
- **Scenario** — the condition or input state being exercised.
- **Expectation** — the observable outcome that should result.

**Go.** The exported function name encodes all three parts. A one-line doc comment above the function surfaces in `go test -v` output and `go doc`:

```go
// TestOrderService_CreateOrder_ReturnsOrderIDOnSuccess verifies that a valid command
// produces a new order with a non-empty ID.
func TestOrderService_CreateOrder_ReturnsOrderIDOnSuccess(t *testing.T) { ... }
```

Inside a testify suite the method follows the same pattern:

```go
func (s *OrderServiceSuite) TestOrderService_CreateOrder_PersistsAndReturnsID() { ... }
```

**TypeScript / JS (Vitest · Jest).** The `describe(...)` block names the Subject; the `it(...)` / `test(...)` string carries the full `Subject_Scenario_Expectation` name so the title is self-describing in CI output independent of nesting:

```ts
describe('SignupForm', () => {
  it('SignupForm_InvalidEmail_ShowsValidationError', async () => { ... });
  it('SignupForm_EmptyEmail_ShowsRequiredError', async () => { ... });
});
```

**Playwright (e2e UI).** The `test(...)` title is the full three-part name:

```ts
test('CheckoutFlow_EmptyCart_RedirectsToProductsPage', async ({ page }) => { ... });
```

All per-tier guidance below applies this invariant. The tier (unit / integration / e2e) is encoded in the file name suffix, not the test title.

## Test tiers

**File naming and build tags are the tier contract.** Every test file lives next to the code it covers. In TypeScript the suffix signals scope; in Go the suffix plus a build-tag header gates which tier `go test` compiles.

| Tier | TypeScript | Go | Scope |
|---|---|---|---|
| unit | `*.unit.test.ts` / `*.unit.test.tsx` | `*_test.go` (no build tag) | Single unit; no I/O; runs in milliseconds. |
| integration | `*.integration.test.ts` / `*.integration.test.tsx` | `*_integration_test.go` + `//go:build integration` | Multiple pieces together with real adapters or controlled substitutes. |
| e2e | `*.e2e.test.ts` / `*.e2e.test.tsx` | `*_e2e_test.go` + `//go:build e2e` | Full app or SDK exercised through its public surface. |

**Go build-tag gate (Go 1.17+).** Unit tests use the plain `*_test.go` suffix with no build tag — `go test ./...` compiles and runs only this tier by default. Integration and e2e files must begin with a build-tag header followed by a blank line before the `package` declaration (the blank line is required; without it the directive is ignored):

```go
//go:build integration

package foo_test
```

The tag keeps tiers strictly separate: `go test ./...` excludes tagged files; tagged tiers compile in only with `-tags=integration` or `-tags=e2e`.

**Run commands (Go).**

```sh
# Unit — default, no tag (runs on every PR)
go test -race -count=1 ./...

# Integration
go test -tags=integration -race -count=1 ./...

# e2e
go test -tags=e2e -race -count=1 ./...
```

Make targets: `make test-unit | test-integration | test-e2e | test`

**Go test naming.** The `TestSubject_Scenario_Expectation` three-part name (see **Test naming** above) is encoded directly in the exported function or suite method; a one-line doc comment goes above the declaration. The integration file example below shows both in full context.

**Playwright**: TypeScript-only. The Go e2e tier covers HTTP-SDK/API tests, not UI automation.

**unit** — isolated. No database, no network, no filesystem. External dependencies are test doubles injected via interfaces (see `principles-pragmatic-solid`). The full unit suite runs in seconds.

**integration** — real adapters, controlled infrastructure. Wire multiple pieces together:
- Databases: spin up a real instance with Docker (e.g., `testcontainers`); seed data before each test.
- AWS services: LocalStack.
- Third-party HTTP APIs without Docker: HTTP interceptors (`nock` / `msw` in Node; `httpmock` in Go).
- Server-side (Node): use `supertest` to call your server over HTTP; seed local DBs/services; tear down after.

**e2e** — full app or SDK exercised end-to-end:
- HTTP SDK tests call the real API within its own codebase — no mocks.
- UI: **Playwright** against `localhost` (TypeScript-only). Start the dev/test server before the suite; shut it down after. Go e2e tests cover HTTP-SDK/API tests, not UI automation.

**Setup/teardown at every level.**
Every test file — regardless of tier — must define all four lifecycle hooks, even if empty. Establish the scaffold upfront so setup and teardown are never retrofitted later.

TypeScript (Jest / Vitest):

```ts
beforeAll(async () => { /* start server, seed db, launch browser */ });
beforeEach(async () => { /* reset state */ });
afterEach(async () => { /* assert no leaked state */ });
afterAll(async () => { /* stop server, close browser, drop test db */ });
```

Go uses testify suite methods that map one-to-one to the four TypeScript hooks:

| TypeScript | Go (testify suite) | Role |
|---|---|---|
| `beforeAll` | `SetupSuite` | Start shared resources (DB container, server) |
| `beforeEach` | `SetupTest` | Seed fixtures, reset state |
| `afterEach` | `TearDownTest` | Rollback, assert no leaked state |
| `afterAll` | `TearDownSuite` | Stop shared resources |

Every suite type ALWAYS defines all four methods, even if empty:

```go
func (s *XSuite) SetupSuite()    {}
func (s *XSuite) SetupTest()     {}
func (s *XSuite) TearDownTest()  {}
func (s *XSuite) TearDownSuite() {}
```

**No skip path.** When a service dependency (database, queue, external API) is unreachable, integration and e2e tests must `t.Fatalf(...)` — never `t.Skipf(...)`. A silent skip lets a missing dependency ride a green badge over a regression.

**Integration test file example (Go).**

```go
//go:build integration

package order_test

import (
    "testing"

    "github.com/stretchr/testify/suite"
)

// TestOrderServiceIntegration_Suite is the testify entry point for the integration suite.
// Suite dispatcher funcs (the `func TestXxx(t) { suite.Run(t, ...) }` boilerplate) are
// EXEMPT from the Subject_Scenario_Expectation rule — they run no assertions themselves;
// the three-part naming applies to the suite's test METHODS, which are the real cases.
func TestOrderServiceIntegration_Suite(t *testing.T) {
    suite.Run(t, new(OrderServiceSuite))
}

type OrderServiceSuite struct{ suite.Suite }

func (s *OrderServiceSuite) SetupSuite()    { /* start DB container; t.Fatalf if unreachable */ }
func (s *OrderServiceSuite) SetupTest()     { /* seed fixtures */ }
func (s *OrderServiceSuite) TearDownTest()  { /* rollback / cleanup */ }
func (s *OrderServiceSuite) TearDownSuite() { /* stop DB container */ }

// TestOrderService_CreateOrder_PersistsAndReturnsID verifies that CreateOrder
// writes the record to the database and returns a non-empty order ID.
func (s *OrderServiceSuite) TestOrderService_CreateOrder_PersistsAndReturnsID() {
    // arrange / act / assert
}
```

**Optional coverage catalog.** A root `TESTING.md` listing each test suite and what scenarios it covers (one line each) is a low-tech way to track coverage. Update it per PR — no tooling required.

## Cross-references

- `superpowers:test-driven-development` — deep-dive skill for complex TDD scenarios, cycle examples, and anti-patterns.
- `test-design` — designs *what* to test (acceptance criteria + adversarial case enumeration + coverage-gap audit) that seeds the failing tests this skill's red/green rhythm then drives. This skill owns the rhythm/tiers/naming; `test-design` owns case design.
- `principles-pragmatic-solid` — interface/dependency-inversion rules that keep test doubles effortless.
- `principles-dry-kiss` — refactor phase guidance (don't over-abstract the resulting code).
