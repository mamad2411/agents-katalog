# Go CLI Expert Agents — Project Context

This repository contains **three specialized Claude Code subagents** for Go (Golang):
code quality, architecture analysis, and complexity metrics — all via CLI tools only.
No CI/CD, no SaaS dashboards, no web interfaces.

## Repository Structure

```
.claude/
├── agents/
│   ├── golang-compliance.md       ← Lint, vet, staticcheck agent
│   ├── golang-architecture.md     ← Dependency graphs, call graphs agent
│   ├── golang-metrics.md          ← Complexity & LOC metrics agent
│   ├── golang-profiling.md        ← CPU/mem/trace profiling agent
│   ├── golang-concurrency.md      ← Race detector, goroutines, channels
│   ├── golang-error-handling.md   ← Errors, panics, sentinel rules
│   ├── golang-testing.md          ← Coverage, mocks, test structure
│   ├── golang-project-structure.md ← Layout, internal/, import hygiene
│   ├── golang-security.md         ← CVEs, gosec, unsafe, secrets
│   └── golang-style-guide.md      ← gofmt, naming, comments, idioms
└── skills/
    ├── golang-compliance/
    │   ├── SKILL.md               ← Detailed linting workflows
    │   └── examples/
    │       └── golangci-config.yml
    ├── golang-architecture/
    │   ├── SKILL.md               ← Dependency & call-graph workflows
    │   └── examples/
    │       └── architecture-analysis.sh
    ├── golang-metrics/
    │   ├── SKILL.md               ← Complexity & LOC workflows
    │   └── examples/
    │       └── metrics-report.sh
    ├── golang-profiling/
    │   ├── SKILL.md               ← pprof, benchmarks, trace workflows
    │   └── examples/
    │       └── profile-report.sh
    ├── golang-concurrency/SKILL.md
    ├── golang-error-handling/SKILL.md
    ├── golang-testing/SKILL.md
    ├── golang-project-structure/SKILL.md
    ├── golang-security/SKILL.md
    └── golang-style-guide/SKILL.md
```

## Three Agents — When to Use Each

| Agent | Invoke when... | Tools |
|-------|---------------|-------|
| `golang-compliance` | "check code quality", "run linters", "find bugs" | `golangci-lint`, `staticcheck`, `go vet`, `revive` |
| `golang-architecture` | "show dependencies", "visualize architecture", "find cycles" | `goda`, `go-callvis`, `go list`, `go mod graph` |
| `golang-metrics` | "how complex is this?", "find hard functions", "lines of code" | `gocyclo`, `gocognit`, `gocloc` |
| `golang-profiling` | "why is this slow?", "memory leak", "run benchmarks", "profile CPU" | `go tool pprof`, `go test -bench`, `benchstat` |
| `golang-concurrency` | "check goroutines", "find data races", "context rules" | `go test -race`, `go vet`, `golangci-lint` |
| `golang-error-handling` | "check error wrapping", "find panics", "sentinel rules" | `golangci-lint`, `go vet`, `grep` |
| `golang-testing` | "run tests", "check coverage", "create mocks" | `go test`, `go tool cover`, `mockgen` |
| `golang-project-structure` | "check layout", "format imports", "find bad package names" | `go imports`, `goda`, `go list` |
| `golang-security` | "scan for vulnerabilities", "find hardcoded secrets" | `govulncheck`, `gosec`, `grep` |
| `golang-style-guide` | "format code", "check naming", "lint comments" | `gofmt`, `goimports`, `golangci-lint` |

## Mapping to SciTools Understand

| `und` command | Go Agent | Go CLI equivalent |
|---|---|---|
| `und analyze` | `golang-compliance` | `go build ./...` + `golangci-lint run` |
| `und codecheck` | `golang-compliance` | `golangci-lint run` / `staticcheck ./...` |
| `und metrics` | `golang-metrics` | `gocyclo`, `gocognit`, `gocloc` |
| `und export -dependencies` | `golang-architecture` | `goda graph ./...` / `go-callvis` |
| `und list` | `golang-architecture` | `go list ./...` / `go list -json ./...` |
| Performance analysis | `golang-profiling` | `go tool pprof`, `go test -bench`, `benchstat` |

## Scope Boundaries

**In scope:**
- Core Go toolchain (`go build`, `go vet`, `go mod`, `go list`, `go doc`)
- Static analysis & linting (`golangci-lint`, `staticcheck`, `revive`)
- Complexity metrics (`gocyclo`, `gocognit`, `gocloc`)
- Architecture & dependency visualization (`goda`, `go-callvis`, `graphviz`)

**Out of scope:**
- CI/CD pipeline setup (GitHub Actions, GitLab CI, etc.)
- Cloud/SaaS dashboards (SonarQube, CodeClimate, etc.)
- Docker, Kubernetes, deployment infra

## Tool Installation Reference

```bash
# Compliance
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
go install honnef.co/go/tools/cmd/staticcheck@latest
go install github.com/mgechev/revive@latest

# Metrics
go install github.com/fzipp/gocyclo/cmd/gocyclo@latest
go install github.com/uudashr/gocognit/cmd/gocognit@latest
go install github.com/hhatto/gocloc/cmd/gocloc@latest

# Architecture
go install github.com/loov/goda@latest
go install github.com/ofabry/go-callvis@latest
brew install graphviz   # macOS (для dot → SVG/PNG)

# Profiling & Testing
go install golang.org/x/perf/cmd/benchstat@latest
go install go.uber.org/mock/mockgen@latest
go install gotest.tools/gotestsum@latest

# Security & Style
go install golang.org/x/vuln/cmd/govulncheck@latest
go install github.com/securego/gosec/v2/cmd/gosec@latest
go install golang.org/x/tools/cmd/goimports@latest
```
