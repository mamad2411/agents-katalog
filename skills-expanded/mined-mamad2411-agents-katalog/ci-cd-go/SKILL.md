---
name: ci-cd-go
description: "Applies when creating or modifying CI/CD pipelines for Go projects. Covers module caching, go test -coverprofile, golangci-lint, and govulncheck."
---

# Go CI/CD

## Setup and caching

Use `actions/setup-go@v5` with `cache: true`. This automatically caches:
- `~/go/pkg/mod` (module download cache)
- `~/.cache/go-build` (build cache)

Key file: `go.sum`.

## Install

No separate install step needed. `go mod download` can be used to pre-populate the cache.

## Coverage

```bash
go test -v -race -coverprofile=coverage.out ./...
go tool cover -func=coverage.out
```

For Cobertura XML output (Codecov upload): `gocover-cobertura < coverage.out > coverage.xml`.

To enforce a threshold, parse `go tool cover -func` output or use a coverage action.

## Linting

Use `golangci/golangci-lint-action` — it runs in its own job with its own cache:

```yaml
- uses: golangci/golangci-lint-action@v6
  with:
    version: latest
```

This bundles `govet`, `staticcheck`, `gosec`, `errcheck`, `ineffassign`, and dozens more. Configure via `.golangci.yml`.

## Dependency audit

```bash
govulncheck ./...
```

## Go-specific gotchas

1. Always use `-race` in CI tests — the race detector catches data races that are invisible without it.
2. `golangci-lint` should run in a **separate job** from tests (it has its own heavy cache).
3. Set `GOFLAGS=-count=1` to disable test caching if you need truly fresh runs.
4. For CGo-heavy projects, cache `~/.cache/go-build` explicitly since build artifacts are large.
5. Pin Go version in `go.mod` (`go 1.23`) and match it in the workflow.

## Sources

- https://github.com/actions/setup-go
- https://golangci-lint.run/welcome/install/#ci-installation
