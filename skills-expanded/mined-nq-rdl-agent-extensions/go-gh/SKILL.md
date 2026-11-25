---
name: go-gh
license: CC-BY-4.0
description: >-
  GitHub Actions CI for Go: workflows that build, test, lint or release Go code
  with actions/setup-go, including go.mod/go.work version files, version
  matrices, module and build caching, multi-module repositories, test
  artifacts, and runners without github.com access. Use when writing or
  reviewing a Go workflow or asking how to test Go in CI.
compatibility: >-
  Examples use actions/setup-go v7, actions/checkout v7 and
  actions/upload-artifact v7 (latest majors on 2026-09-29).
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# GitHub Actions for Go

Set up, build, test, and ship Go projects in GitHub Actions using
[`actions/setup-go`](https://github.com/actions/setup-go). Check its
[releases](https://github.com/actions/setup-go/releases) for the current major
before pinning; the cache and `go.mod` behaviour below changed in v6.

> **Reference docs** — detailed examples live in `references/`:
> - [references/advanced-usage.rst](references/advanced-usage.rst) — version
>   syntax, caching variants, restore-only caches, outputs, custom download
>   URLs, GHES and runners without github.com access
> - [references/build-test.rst](references/build-test.rst) — full workflow
>   patterns, matrix, artifacts

## Quick Start

Minimal CI workflow:

```yaml
name: Go CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-go@v7
        with:
          go-version-file: go.mod
      - run: go build -v ./...
      - run: go test -v ./...
```

## Core Guidelines

### 1. Prefer `go-version-file` over hardcoded versions

Let `go.mod` (or `go.work`, `.go-version`) be the single source of truth:

```yaml
- uses: actions/setup-go@v7
  with:
    go-version-file: go.mod   # v6+: `toolchain` directive if present, else `go`
```

Only hardcode for matrix strategies or versions not tracked in module files.

### 2. Version specification

| Format | Meaning | Example |
|--------|---------|---------|
| `1.25.5` | Exact patch | Reproducible builds |
| `1.25` | Latest patch of minor | Pre-installed on runners = fast |
| `^1.25.1` | SemVer range | Flexible matching |
| `stable` | Latest stable release | Always current |
| `oldstable` | Previous minor's latest patch | Compatibility testing |
| `1.25.0-rc.2` | Pre-release | Beta/RC testing |

### 3. Matrix testing across versions

```yaml
strategy:
  matrix:
    go-version: [oldstable, stable]   # or explicit minors such as '1.26'
    os: [ubuntu-latest, macos-latest, windows-latest]
steps:
  - uses: actions/checkout@v7
  - uses: actions/setup-go@v7
    with:
      go-version: ${{ matrix.go-version }}
  - run: go test -v ./...
```

### 4. Caching is on by default

setup-go caches the module and build caches by default (since v4). From v6 the
key hashes the root `go.mod`, not `go.sum`; a module elsewhere, or a
`go.sum`-only change, needs `cache-dependency-path`:

```yaml
# Monorepo — point to the right go.sum
- uses: actions/setup-go@v7
  with:
    go-version-file: go.mod
    cache-dependency-path: subdir/go.sum

# Multi-module — glob or multi-line
- uses: actions/setup-go@v7
  with:
    go-version-file: go.mod
    cache-dependency-path: |
      go.sum
      tools/go.sum

# Disable cache entirely
- uses: actions/setup-go@v7
  with:
    go-version-file: go.mod
    cache: false
```

### 5. Build and test pattern

Standard CI job structure:

```yaml
steps:
  - uses: actions/checkout@v7
  - uses: actions/setup-go@v7
    with:
      go-version-file: go.mod
  - name: Install dependencies
    run: go mod download
  - name: Build
    run: go build -v ./...
  - name: Test
    run: go test -v -race -coverprofile=coverage.out ./...
  - name: Upload coverage
    uses: actions/upload-artifact@v7
    with:
      name: coverage
      path: coverage.out
```

### 6. Test result artifacts

Export JSON test output for downstream analysis:

```yaml
- name: Test with JSON output
  run: go test -json ./... > test-results.json
- name: Upload test results
  uses: actions/upload-artifact@v7
  with:
    name: test-results-${{ matrix.go-version }}
    path: test-results.json
```

### 7. Use outputs for downstream steps

```yaml
- uses: actions/setup-go@v7
  id: setup
  with:
    go-version: '^1.24'
- run: echo "Installed ${{ steps.setup.outputs.go-version }}"
- run: echo "Cache hit: ${{ steps.setup.outputs.cache-hit }}"
```

## Common Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| Hardcoding `go-version: '1.25.3'` everywhere | Use `go-version-file: go.mod` |
| Running `go get .` for dependencies | Use `go mod download` (doesn't modify go.mod) |
| No `-race` flag in CI tests | Add `-race` — CI has the CPU budget |
| Caching `vendor/` manually | Let setup-go handle module cache automatically |
| Pinning an old major (`setup-go@v4`, `@v5`) | Use the current major; v6+ runs on Node 24 and reads the `toolchain` directive |
| No `actions/checkout` before setup-go | Always checkout first |

## External References

- [actions/setup-go — Advanced Usage](https://github.com/actions/setup-go/blob/main/docs/advanced-usage.md)
- [GitHub Docs — Build and test Go](https://docs.github.com/en/actions/tutorials/build-and-test-code/go)
