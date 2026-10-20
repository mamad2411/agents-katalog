---
paths:
  - "**/*.go"
  - "**/go.mod"
  - "**/go.sum"
---
# Go Conventions

## Architecture
ALWAYS follow Clean Architecture layers: Entities → Use Cases → Adapters → Frameworks.
NEVER let domain entities import adapter or framework packages.
ALWAYS define interfaces in the use-case layer, implement in adapters.
ALWAYS use structured logging with low-cardinality message strings.
NEVER use `any` or `interface{}` to stand in for a type you have not worked out — that is the defect
this rule exists to stop, and it is the Go spelling of the raw `any` that
`architecture-guardrails.md` #4 forbids in TypeScript. Go has no `unknown`, so the discipline is
carried by *where* the value is allowed to live rather than by a second keyword: narrow at the
boundary, and never let it travel inward.

Permitted only where Go's type system genuinely cannot express the thing, and only at these
boundaries:
- **JSON and wire boundaries** — decoding untrusted input, or building a JSON document such as a
  JSON Schema or an MCP argument map. Narrow into a typed struct at the first opportunity.
- **Reflection subjects** — a value handed to a reflector for schema generation or marshalling.
- **Variadic pass-through** to a standard-library API whose own signature is `...any` (`slog`,
  `fmt`). Matching the stdlib is not a violation.
- **Heterogeneous dispatch** where the alternative is a sum type Go does not have. Name the reason
  in a comment.

NEVER for a domain type, a struct field holding domain data, or a return the caller must
type-assert before it can act on it. If a reader has to guess what is inside, the rule is broken
regardless of which boundary it sits near.
ALWAYS handle errors explicitly — no silent swallows.
ALWAYS set explicit timeouts on network calls.
NEVER use raw SQL without parameterized queries.
ALWAYS use the expand/contract pattern for database migrations.

## Project Tooling
- **Modules**: Go modules (`go.mod`/`go.sum`) — no vendoring unless a specific reproducibility
  requirement demands it.
- **Formatter**: `gofmt` (or `goimports`, which also manages import grouping).
- **Linter**: `golangci-lint` — aggregates `staticcheck`, `govet`, `errcheck`, and others behind one
  config (`.golangci.yml`).

## Project Structure
Follows the community-standard layout ([golang-standards/project-layout](https://github.com/golang-standards/project-layout)):
- `cmd/` — application entrypoints (one subdirectory per binary)
- `internal/` — private application code (Go's compiler enforces this can't be imported by other modules)
- `pkg/` — public, reusable packages, only if something outside this module actually needs to import it
  (don't default everything into `pkg/` "just in case" — that's the same premature-generalization
  anti-pattern `shared/rules/design-principles.md` already warns against)

## Testing & QA Tooling
- **Unit testing framework**: standard library `testing`, table-driven tests via `t.Run()`, assertions
  via `testify/assert` and `testify/require` (`require` for setup/fatal conditions, `assert` for
  non-fatal checks within a test body). `testify/mock` for interface mocks.
- **Fake/synthetic data (faker-equivalent)**: [`gofakeit`](https://github.com/brianvoe/gofakeit)
  (`github.com/brianvoe/gofakeit/v7`) — the most actively maintained Go faker library, covers the usual
  categories (names, addresses, structured data via `gofakeit.Struct()`).
- **Factories / fixtures (fishery-equivalent)**: Go's community leans toward plain builder-pattern
  functions over reflection-heavy factory libraries — PREFER a hand-written
  `NewUserBuilder().WithName(...).Build()` pattern per domain type over pulling in a factory framework.
  If a team specifically wants a `factory_boy`/`fishery`-style declarative factory,
  [`factory-go`](https://github.com/bluele/factory-go) is the closest equivalent, but it's not as
  dominant a standard in Go as `fishery` is in the JS ecosystem — treat it as optional, not default.
- **E2E / API testing**: Playwright via [`playwright-go`](https://github.com/playwright-community/playwright-go)
  — note this is a **community-maintained** binding, not an official Microsoft one (unlike the
  JS/Python/.NET/Java bindings). Verify it's kept current with the Playwright version the rest of the
  stack uses before relying on it for anything beyond smoke coverage.
- **Mutation testing** (ADR-008 clause 2): [`gremlins`](https://github.com/go-gremlins/gremlins) v0.6.0,
  run on the changed lines only by loom's `cmd/diff-mutation`. Verified 2026-09-23 with three caveats
  that each produced a false result: `--diff` does not scope; default timeouts count as kills; and a
  package named unlike its directory (`package main`) is tested as the wrong package, so every mutant
  reads LIVED. Run it through a wrapper that handles all three, or its numbers are not evidence.
- **Performance testing**: k6. k6 scripts are always JavaScript regardless of the target service's
  language — "k6 for Go" means a Go service gets load-tested by the same k6 scripts as everything else,
  not a Go-specific k6 binding. See `shared/rules/testing-conventions.md` for the shared reporting
  pipeline.
- **Reporting**: [`gotestsum`](https://github.com/gotestyourself/gotestsum) wrapping `go test -json` — human-
  readable CI output plus `--junitfile` for JUnit XML export into whatever CI reporting aggregator is in
  use.
