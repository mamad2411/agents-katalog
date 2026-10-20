---
name: golang-basics
description: >
  Go language fundamentals for productive work: modules, types, interfaces,
  concurrency basics, testing, and toolchains. Use when onboarding or teaching
  owned Go codebases.
---

# Golang Basics

## Research grounding

Teaching and reference runbook for **Go fundamentals** needed to work safely in
this skill library’s Go services—not a full language spec. Skill id:
`golang-basics`.

## Scope And Authorization

- **In scope:** learning and coding on repos you are allowed to change.
- **Out of scope:** using basics as substitute for domain security skills.
- Prefer official docs (go.dev) for deep language law.
- Pair advanced work with `golang-best-practices`, `go-style-conventions`, `code-quality-standards`.

## When To Use

- Onboarding engineers to Go microservices.
- Refreshers on modules, `go test`, contexts, and errors.
- Establishing shared vocabulary before deeper skills.
- Focus tokens: **golang, basics**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Production best practices shortlist | `golang-best-practices` |
| Anti-patterns deep dive | `golang-anti-patterns` |
| Security gates | `golang-asvs-gates` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus — core topics

| Topic | Must know |
| --- | --- |
| Toolchain | `go build`, `go test`, `go mod`, `gofmt` |
| Modules | `go.mod`/`go.sum`, semantic import versions |
| Types | structs, slices, maps, pointers |
| Methods/interfaces | small interfaces, implicit satisfaction |
| Errors | `error` values, wrapping `%w`, `errors.Is/As` |
| Concurrency | goroutines, channels, `select`, context cancel |
| Testing | `_test.go`, table tests, `-race` |
| Packages | `internal/` visibility |

## Workflow

### 1. Confirm goals

1. Learner level; target repo; authorization to clone/run.
2. Success: run tests; make small PR; explain context and errors.

### 2. Environment

```bash
go version
go env GOROOT GOPATH GOMODCACHE
# clone owned repo
go test ./...
```

1. Install supported Go version from `go.mod`.
2. Editor: gopls, format on save.

### 3. Modules and layout

```text
module example.com/myapp

require (
    // pinned versions
)
```

1. Prefer `cmd/`, `internal/`, `pkg/` (if public libs) layouts as used by the org.
2. Never commit secrets; use env/config.

### 4. Language drills (hands-on)

```go
func Div(a, b int) (int, error) {
	if b == 0 {
		return 0, fmt.Errorf("div by zero")
	}
	return a / b, nil
}

func TestDiv(t *testing.T) {
	_, err := Div(1, 0)
	if err == nil {
		t.Fatal("expected error")
	}
}
```

```go
ctx, cancel := context.WithTimeout(context.Background(), time.Second)
defer cancel()
// pass ctx to downstream calls
```

1. Practice table-driven tests.
2. Practice one worker pool with context cancel.
3. Read Effective Go + project CONTRIBUTING.

### 5. Verify learning

```bash
go test ./... -race -count=1
go vet ./...
gofmt -l .
```

1. Small task: add endpoint test or fix a lint.
2. Code review focuses on errors and context first.

### 6. Next steps

1. Route to `golang-best-practices` and domain skills (HTTP, authz).
2. Avoid premature concurrency.

### 7. Hand off

1. Checklist of completed drills.
2. Mentor sign-off if org requires.

## Command cheatsheet

| Command | Purpose |
| --- | --- |
| `go test ./...` | Run all tests |
| `go test -race` | Race detector |
| `go mod tidy` | Clean modules |
| `go vet ./...` | Basic static checks |
| `gofmt -w .` | Format |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Errors | Return and handle | Panic for normal faults |
| Context | First param on RPC | Globals for cancel |
| Modules | Commit go.sum | Random `replace` hacks |
| Topic fidelity | Go fundamentals | Generic mega-batch security fluff only |

## Output Checklist

- [ ] Toolchain matches go.mod
- [ ] Tests run locally
- [ ] Errors/context exercises done
- [ ] Small contribution merged or reviewed
- [ ] Path to next skills clear

## Rules

- Prefer clarity over cleverness.
- Focus on `golang-basics`.
- Do not skip tests while learning.
- Authorized repos only.
