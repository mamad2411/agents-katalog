---
name: golang-anti-patterns
description: >
  Recognize and remediate Go anti-patterns: concurrency mistakes, error handling,
  package design, config/secrets, and HTTP pitfalls. Use when reviewing or
  refactoring owned Go codebases.
---

# Golang Anti Patterns

## Research grounding

Catalog and remediation workflow for **common Go anti-patterns** that cause
bugs, races, outages, or vulnerabilities—used in code review and refactors.
Skill id: `golang-anti-patterns`.

## Scope And Authorization

- **In scope:** codebases you own or are authorized to change.
- **Out of scope:** unsolicited mass refactors of third-party projects without agreement.
- Prefer small reversible PRs; measure with tests/`-race`.
- Pair with `code-quality-standards`, `golang-best-practices`, `go-style-conventions`.

## When To Use

- Reviewing Go PRs for footguns.
- Stabilizing flaky tests or production races.
- Onboarding engineers to project conventions via bad/good examples.
- Focus tokens: **golang, anti, patterns**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Positive style guide | `go-style-conventions` / `golang-best-practices` |
| Security ASVS gates | `golang-asvs-gates` |
| Full reliability patterns | `retry-backoff-patterns`, `golang-backpressure` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus — anti-pattern catalog

| Anti-pattern | Why bad | Prefer |
| --- | --- | --- |
| Ignoring `error` | Silent failure | Handle, wrap with `%w` |
| `panic` for business control flow | Crash loops | Return errors |
| Naked goroutines without lifecycle | Leaks | `errgroup`, context cancel |
| Sharing maps without sync | Data races | `sync.Map` carefully or mutex |
| `init()` heavy side effects | Hard tests | Explicit `New` |
| Global mutable config | Race + order bugs | Dependencies injected |
| SQL string concat | Injection | Parameterized queries |
| `http.DefaultClient` no timeout | Hang forever | Custom client + timeouts |
| Context in struct long-lived | Cancellation bugs | Pass `ctx` as first arg |
| Huge interfaces | Brittle | Small interfaces at consumer |
| `interface{}` / overuse `any` | Lost safety | Generics or concrete types |
| Defer in loop holding resources | FD exhaustion | Scope function per iter |
| Capturing loop var wrong (pre-1.22 habits) | Wrong values | Understand Go version semantics |
| Secrets in structs logged | Leak | Redact, separate types |

## Workflow

### 1. Confirm scope and success criteria

1. Repo, packages in scope, authorization.
2. Success: top N anti-patterns eradicated or lint-gated; race tests green.
3. Do not boil ocean—prioritize by crash/security impact.

### 2. Inventory

1. Enable `go vet`, `staticcheck`, `golangci-lint`, `govulncheck`.
2. Run tests with `-race`.
3. Search for known smells (`http.Get`, `Query(` concat, `go func`).

### 3. Baseline

1. Record lint counts and known flaky tests.
2. Capture production symptoms tied to suspects.

### 4. Remediate in priority order

```go
// Bad: no timeout
resp, err := http.Get(url)

// Good
client := &http.Client{Timeout: 10 * time.Second}
req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
resp, err := client.Do(req)
```

```go
// Bad: fire-and-forget
go doWork()

// Good
g, ctx := errgroup.WithContext(ctx)
g.Go(func() error { return doWork(ctx) })
err := g.Wait()
```

1. Fix security anti-patterns first (SQL, command, path).
2. Fix concurrency with tests under `-race`.
3. Add linters as CI gates so patterns cannot return.
4. Document project-specific “don’ts” in CONTRIBUTING.

### 5. Verify with evidence

```bash
go test ./... -race -count=1
go vet ./...
staticcheck ./...
golangci-lint run
govulncheck ./...
```

1. Before/after flake rate.
2. Benchmark if hot path changed.
3. PR review checklist includes catalog items.

### 6. Observe and harden

1. CI required checks for lint/race.
2. Periodic “lint debt” burn-down.
3. Postmortems tag root-cause anti-pattern IDs.

### 7. Hand off

1. Update style docs with bad/good snippets.
2. Mentoring notes for common review comments.
3. Apply `code-quality-standards`.

## Review cheat sheet

| See this | Ask |
| --- | --- |
| `go ` keyword | Who cancels? Who waits? |
| `error` ignored | What if it fails? |
| `interface{}` | Can it be typed? |
| SQL/log/format | User controlled? |
| Mutex | Lock order? Copy of struct? |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Fix size | Incremental with tests | Rewrite everything |
| Proof | `-race` + lint gate | “Looks fine” |
| Context | Passed as parameter | Stored forever on server |
| Topic fidelity | Go anti-patterns list + fixes | Generic mega-batch fluff |

## Output Checklist

- [ ] Scope and priority list set
- [ ] Lint/race baseline captured
- [ ] High-impact anti-patterns fixed
- [ ] CI gates added/updated
- [ ] Docs with bad/good examples
- [ ] `code-quality-standards` applied

## Rules

- Prefer teaching fixes over shaming.
- Evidence via tools and tests.
- Focus on `golang-anti-patterns`.
- Do not disable race detector to hide bugs.
