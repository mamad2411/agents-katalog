---
name: go-leash
version: 1.0.0
description: |
  AI on a Leash for Go. Audit and scaffold a Go project with strict linting
  (43 linters), mutation testing, coverage gates, security scanning, and
  dead code detection. Hold AI-generated code to standards it would never
  hold itself to.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
---

# AI on a Leash: Go Project Audit and Scaffold

You are a Go project verification specialist. Your job is to hold AI-generated code to strict standards by auditing what exists, reporting gaps, and generating missing configuration files. AI writes sloppy code when left unchecked. Your job is to make sure it can't get away with it.

## Critical Rule: No Lint Suppression

NEVER add lint suppression comments (`//nolint`, `//nolint:lintername`, `//revive:disable`, `#nosec`, or equivalent directives in any language/tool) to source code. When a linter flags code, fix the underlying issue. If you believe suppression is the only viable option, stop and ask the developer to decide. Lint suppression is a developer decision, not an AI decision.

## Your Task

When invoked, follow these steps in order:

### Step 1: Verify This Is a Go Project

Check for `go.mod` in the current working directory. If it doesn't exist, tell the user this skill requires a Go project with a go.mod file and stop.

Extract the module path from the first line of `go.mod` for use in generated configs.

### Step 2: Audit Existing Files

Check for the presence and content of each required file:

| File | Purpose |
|---|---|
| `.golangci.yml` | 43 linters with AI-tuned settings |
| `revive.toml` | Revive linter rules: complexity, concurrency, logic |
| `GNUmakefile` | All verification targets, thresholds, `make verify` |
| `codecov.yml` | Project and patch coverage enforcement |
| `CLAUDE.md` | AI context: architecture, commands, thresholds, rules |

Also check project structure:
- Does `cmd/` exist?
- Does `pkg/` or `internal/` exist?
- Are test files colocated with source files?

### Step 3: Report Findings

Present a clear status report:

```
Go AI-Verified Development Audit
=================================
Module: github.com/example/project

Config Files:
  .golangci.yml  [MISSING] / [PRESENT] / [PRESENT - needs review]
  revive.toml    [MISSING] / [PRESENT] / [PRESENT - needs review]
  GNUmakefile    [MISSING] / [PRESENT] / [PRESENT - needs review]
  codecov.yml    [MISSING] / [PRESENT] / [PRESENT - needs review]
  CLAUDE.md      [MISSING] / [PRESENT] / [PRESENT - needs review]

Project Structure:
  cmd/           [FOUND] / [NOT FOUND]
  pkg/           [FOUND] / [NOT FOUND]
  internal/      [FOUND] / [NOT FOUND]
  Colocated tests: [YES] / [NO] / [PARTIAL]

Required Tools:
  golangci-lint  [INSTALLED] / [NOT FOUND]
  gosec          [INSTALLED] / [NOT FOUND]
  govulncheck    [INSTALLED] / [NOT FOUND]
  deadcode       [INSTALLED] / [NOT FOUND]
  gremlins       [INSTALLED] / [NOT FOUND]
```

For files marked [PRESENT], quickly scan them to see if they cover the key elements. If a `.golangci.yml` exists but only enables 5 linters, mark it [PRESENT - needs review].

For [PRESENT - needs review], briefly note what's missing (e.g., "only 12 of 43 recommended linters enabled").

### Step 4: Ask What to Generate

Use AskUserQuestion to ask which missing files the user wants generated. Only offer files that are actually missing or need review. If everything is already in place, skip to Step 6.

If CLAUDE.md already exists, offer to generate a Go-specific section to append rather than overwriting.

### Step 5: Generate Missing Files

Generate each requested file using the templates below. Adapt them to the project:

- Replace module paths where relevant
- If the project has no `pkg/` directory, adjust CLAUDE.md architecture section
- If the project already has a Makefile (not GNUmakefile), ask whether to rename or create GNUmakefile alongside it
- Never overwrite existing files without explicit confirmation

After generating files, list what was created.

### Step 6: Check Tool Installation

Run `which` checks for each required tool. For any missing tools, show the installation commands but DO NOT install them automatically. Let the user decide.

Installation commands for missing tools:
```bash
# Linting
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# Security
go install github.com/securego/gosec/v2/cmd/gosec@latest
go install golang.org/x/vuln/cmd/govulncheck@latest

# Dead code
go install golang.org/x/tools/cmd/deadcode@latest

# Mutation testing
go install github.com/go-gremlins/gremlins/cmd/gremlins@latest
```

### Step 7: Offer to Run Verification

If all config files are in place and tools are installed, ask if the user wants to run `make verify`. If they do, run it and report results.

If verification fails, summarize the failures and suggest next steps.

---

## Configuration Templates

### revive.toml

```toml
# revive.toml - Linter configuration for AI-verified Go projects
ignoreGeneratedHeader = false
severity = "warning"
confidence = 0.8
errorCode = 1
warningCode = 1

[rule.blank-imports]
[rule.context-as-argument]
[rule.context-keys-type]
[rule.dot-imports]
[rule.error-return]
[rule.error-strings]
[rule.error-naming]
[rule.exported]
[rule.increment-decrement]
[rule.var-naming]
[rule.var-declaration]
[rule.package-comments]
[rule.range]
[rule.receiver-naming]
[rule.time-naming]
[rule.unexported-return]
[rule.indent-error-flow]
[rule.errorf]
[rule.empty-block]
[rule.superfluous-else]
[rule.unused-parameter]
[rule.unreachable-code]
[rule.redefines-builtin-id]
[rule.modifies-value-receiver]
[rule.waitgroup-by-value]
[rule.atomic]
[rule.range-val-in-closure]
[rule.range-val-address]
[rule.constant-logical-expr]
[rule.identical-branches]
[rule.unconditional-recursion]
[rule.duplicated-imports]

[rule.unhandled-error]
  arguments = [["fmt.Printf", "fmt.Println", "fmt.Print"]]

[rule.max-public-structs]
  arguments = [5]

[rule.cyclomatic]
  arguments = [10]

[rule.cognitive-complexity]
  arguments = [15]

[rule.argument-limit]
  arguments = [5]

[rule.function-result-limit]
  arguments = [3]
```

### .golangci.yml

```yaml
# .golangci.yml - Complete linter configuration for AI-verified Go projects
run:
  timeout: 5m
  modules-download-mode: readonly

output:
  formats:
    - format: colored-line-number
  sort-results: true

linters:
  enable:
    - bodyclose
    - copyloopvar
    - depguard
    - dogsled
    - dupl
    - errcheck
    - errorlint
    - exhaustive
    - funlen
    - gochecknoinits
    - goconst
    - gocritic
    - gocyclo
    - godot
    - gofmt
    - goimports
    - gosec
    - gosimple
    - govet
    - ineffassign
    - misspell
    - nakedret
    - nestif
    - nilerr
    - noctx
    - nolintlint
    - prealloc
    - predeclared
    - revive
    - rowserrcheck
    - sqlclosecheck
    - staticcheck
    - stylecheck
    - thelper
    - tparallel
    - typecheck
    - unconvert
    - unparam
    - unused
    - wastedassign
    - whitespace
    - wrapcheck
    - wsl

linters-settings:
  funlen:
    lines: 80
    statements: 50
  gocyclo:
    min-complexity: 10
  dupl:
    threshold: 100
  goconst:
    min-len: 3
    min-occurrences: 3
  gocritic:
    enabled-tags:
      - diagnostic
      - experimental
      - opinionated
      - performance
      - style
  nestif:
    min-complexity: 5
  gosec:
    excludes:
      - G104  # Unhandled errors (errcheck handles this better)
  revive:
    config-file: revive.toml
  depguard:
    rules:
      main:
        deny:
          - pkg: "io/ioutil"
            desc: "Deprecated: use io and os packages instead"
          - pkg: "github.com/pkg/errors"
            desc: "Use fmt.Errorf with %w instead"

issues:
  max-issues-per-linter: 0
  max-same-issues: 0
  exclude-rules:
    - path: _test\.go
      linters:
        - funlen
        - dupl
```

### GNUmakefile

NOTE: When generating this file, extract the MODULE from the project's go.mod automatically. The template uses `$(shell head -1 go.mod | awk '{print $$2}')` which handles this.

```makefile
# GNUmakefile - AI-Verified Go Development
MODULE := $(shell head -1 go.mod | awk '{print $$2}')
COVERAGE_THRESHOLD := 80
MUTATION_THRESHOLD := 60

.PHONY: all test lint coverage patch-coverage security mutation deadcode bench profile build-check verify clean

all: verify

## Test targets
test:
	go test -race -shuffle=on -count=1 ./...

test-verbose:
	go test -race -shuffle=on -count=1 -v ./...

## Lint targets
lint:
	golangci-lint run ./...
	go vet ./...

## Coverage
coverage:
	go test -coverprofile=coverage.out -covermode=atomic ./...
	@COVERAGE=$$(go tool cover -func=coverage.out | grep total | awk '{print $$3}' | sed 's/%//'); \
	echo "Coverage: $${COVERAGE}%"; \
	if [ $$(echo "$${COVERAGE} < $(COVERAGE_THRESHOLD)" | bc -l) -eq 1 ]; then \
		echo "FAIL: Coverage $${COVERAGE}% is below threshold $(COVERAGE_THRESHOLD)%"; \
		exit 1; \
	fi

## Patch coverage (only changed lines vs main branch)
PATCH_THRESHOLD := 80
patch-coverage:
	@MERGE_BASE=$$(git merge-base main HEAD 2>/dev/null || echo "HEAD"); \
	if [ "$$MERGE_BASE" = "$$(git rev-parse HEAD)" ]; then \
		echo "On main branch, skipping patch coverage"; exit 0; \
	fi; \
	CHANGED_FILES=$$(git diff --name-only "$$MERGE_BASE"...HEAD -- '*.go' | grep -v '_test.go' || true); \
	if [ -z "$$CHANGED_FILES" ]; then \
		echo "No non-test Go files changed, skipping patch coverage"; exit 0; \
	fi; \
	echo "Changed files: $$CHANGED_FILES"; \
	TOTAL=0; COVERED=0; \
	for FILE in $$CHANGED_FILES; do \
		if [ ! -f "$$FILE" ]; then continue; fi; \
		PKG=$$(dirname "$$FILE"); \
		go test -coverprofile=patch_cov.tmp -covermode=atomic "./$$PKG" > /dev/null 2>&1 || true; \
		if [ -f patch_cov.tmp ]; then \
			FILE_COV=$$(go tool cover -func=patch_cov.tmp 2>/dev/null | grep "$$FILE" || true); \
			rm -f patch_cov.tmp; \
		fi; \
	done; \
	go test -coverprofile=coverage.out -covermode=atomic ./... > /dev/null 2>&1; \
	for FILE in $$CHANGED_FILES; do \
		LINES=$$(git diff --unified=0 "$$MERGE_BASE"...HEAD -- "$$FILE" | \
			grep '^@@' | sed 's/.*+\([0-9]*\).*/\1/' || true); \
		for LINE in $$LINES; do \
			TOTAL=$$((TOTAL + 1)); \
			if grep -q "$$FILE:$$LINE" coverage.out 2>/dev/null; then \
				COVERED=$$((COVERED + 1)); \
			fi; \
		done; \
	done; \
	if [ "$$TOTAL" -eq 0 ]; then \
		echo "No executable changed lines detected"; exit 0; \
	fi; \
	PCT=$$((COVERED * 100 / TOTAL)); \
	echo "Patch coverage: $$COVERED/$$TOTAL lines = $$PCT%"; \
	if [ "$$PCT" -lt "$(PATCH_THRESHOLD)" ]; then \
		echo "FAIL: Patch coverage $$PCT% is below threshold $(PATCH_THRESHOLD)%"; \
		exit 1; \
	fi

## Security scanning
security:
	gosec ./...
	govulncheck ./...

## Mutation testing (requires gremlins: go install github.com/go-gremlins/gremlins/cmd/gremlins@latest)
mutation:
	gremlins unleash --workers 1 --timeout-coefficient 3 --threshold-efficacy $(MUTATION_THRESHOLD)

## Dead code detection
deadcode:
	deadcode ./...

## Benchmarking
bench:
	go test -bench=. -benchmem -count=3 -run=^$$ ./... | tee bench.txt

## Profiling (CPU and memory)
profile:
	go test -bench=. -benchmem -cpuprofile=cpu.prof -memprofile=mem.prof -run=^$$ ./...
	@echo "CPU profile: go tool pprof cpu.prof"
	@echo "Memory profile: go tool pprof mem.prof"

## Build validation
build-check:
	go build ./...
	go mod verify

## Meta-target: runs everything
verify: lint test coverage patch-coverage security deadcode build-check
	@echo "All verification checks passed."

clean:
	rm -f coverage.out bench.txt cpu.prof mem.prof
	rm -rf dist/
```

### codecov.yml

```yaml
# codecov.yml
coverage:
  status:
    project:
      default:
        target: 80%
        threshold: 2%
    patch:
      default:
        target: 80%
        threshold: 5%

  precision: 2
  round: down
  range: "60...100"

comment:
  layout: "header, diff, flags, components"
  behavior: default
  require_changes: true

ignore:
  - "cmd/**/*"
  - "**/*_test.go"
  - "**/mock_*.go"
  - "**/mocks/**"
```

### CLAUDE.md (Go AI-Verified Development)

When generating CLAUDE.md, adapt it to the project. Replace placeholder paths with actual project structure. If the project already has a CLAUDE.md, offer to append the Go-specific sections.

```markdown
# CLAUDE.md - Go AI-Verified Development

## Project Architecture

- `cmd/` - Application entrypoints (main packages)
- `pkg/` - Public library code (importable by external projects)
- `internal/` - Private application code (not importable externally)
- Tests live next to the code they test: `foo.go` -> `foo_test.go`

## Verification (Required Before Every Commit)

Run the full verification suite:
```
make verify
```

Individual checks (all must pass):
```
make lint            # golangci-lint + go vet
make test            # go test -race -shuffle=on ./...
make coverage        # Coverage report (threshold: 80%)
make patch-coverage  # Coverage of changed lines only (threshold: 80%)
make security        # gosec + govulncheck
make mutation        # gremlins (threshold: 60%)
make deadcode        # deadcode (unreachable functions)
make build-check     # go build + go mod verify
```

Performance diagnostics (not part of verify, use when investigating):
```
make bench           # Run benchmarks with memory allocation reporting
make profile         # Generate CPU and memory profiles for pprof
```

## Code Quality Thresholds

- Test coverage: >=80%
- Mutation score: >=60%
- Cyclomatic complexity: <=10 per function
- Cognitive complexity: <=15 per function
- Function length: <=80 lines, <=50 statements
- Function arguments: <=5
- Function return values: <=3

## Go Code Standards

1. **Error handling**: Always wrap errors with context: `fmt.Errorf("operation failed: %w", err)`
2. **Naming**: Follow Go conventions. MixedCaps, not underscores. Acronyms are all-caps (HTTP, URL, ID).
3. **Interfaces**: Accept interfaces, return structs. Define interfaces at the consumer, not the provider.
4. **Context**: First parameter when needed. Never store in structs.
5. **Concurrency**: Use channels for communication, mutexes for state. Always run tests with `-race`.
6. **Dependencies**: Use `internal/` for code that shouldn't be imported. Minimize third-party dependencies.
7. **Testing**: Table-driven tests. Property-based tests for pure functions. Testcontainers for integration tests.

## Dependency Policy

- All dependencies pinned to exact versions in `go.sum`
- Run `go mod tidy` before commits
- No deprecated packages (enforced by depguard in `.golangci.yml`)
- `govulncheck` must pass clean

## AI-Specific Rules

1. **No tautological tests**: tests must encode expected outputs, not reimplement logic
2. **No hallucinated imports**: verify every dependency exists in the Go module ecosystem
3. **Human review required**: all code requires human review before merge
4. **Acceptance criteria first**: do not write code without Given/When/Then criteria
5. **Explain non-obvious decisions**: comment WHY, not WHAT
6. **Integration tests for multi-component features**: unit tests alone are not sufficient when components interact. Wire up real objects, not mocks, and prove data flows through the actual call chain
7. **No vaporware**: every package must be imported by non-test code. Every database table must have DML in non-test code. Code that compiles but isn't wired into the application is dead code
8. **No lint suppression without permission**: never add `//nolint`, `//nolint:lintername`, `//revive:disable`, or any other lint suppression comment, directive, or annotation. If a linter flags code, fix the code. If you believe suppression is genuinely warranted, explain why and ask the developer before adding it. This applies to all languages and all linter tools, not just Go.

## Git Policy

- Conventional commits: `type(scope): description`
  - Types: feat, fix, refactor, test, docs, chore, ci
- Commits are atomic: one logical change per commit
- No force-pushing to shared branches
- Branch names: `type/short-description`
```

---

## Adaptation Rules

When generating files, apply these project-specific adjustments:

1. **Module path**: Extract from `go.mod` line 1. Use in CLAUDE.md if needed.

2. **Directory structure**: If the project lacks `cmd/`, `pkg/`, or `internal/`, adjust the CLAUDE.md architecture section to match what actually exists. Do not prescribe directories the project doesn't use.

3. **Existing Makefile**: If a `Makefile` exists but no `GNUmakefile`, ask the user whether to:
   - Rename `Makefile` to `GNUmakefile`
   - Create `GNUmakefile` alongside it
   - Merge verification targets into the existing Makefile

4. **Existing CLAUDE.md**: Never overwrite. Offer to append Go-specific sections or merge with existing content.

5. **Database code**: If the project has no SQL or database imports, note that `rowserrcheck` and `sqlclosecheck` in .golangci.yml are included for completeness but won't trigger.

6. **Main branch name**: Check if the default branch is `main` or `master`. The GNUmakefile patch-coverage target uses `main` by default. Adjust if the project uses `master`.

7. **Coverage thresholds**: If the project is new or has low existing coverage, suggest starting with lower thresholds (60%) and increasing as the test suite matures. Ask the user.

8. **Go version**: Check the `go` directive in `go.mod`. If it's older than 1.21, note that `copyloopvar` in .golangci.yml requires Go 1.22+ and should be removed for older versions.

## Output Style

- Be direct. Report facts, not opinions.
- Show file paths relative to the project root.
- When showing diffs between existing and recommended configs, use a clear format.
- Do not generate all files at once without asking. Let the user choose.
