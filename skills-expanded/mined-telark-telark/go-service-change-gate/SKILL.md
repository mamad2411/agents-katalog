---
name: go-service-change-gate
description: Use before reporting any change to Go code (a service under services/ or a shared package under internal/) as done, or when asked whether a Go change is green. Runs build, vet, tests and golangci-lint the way CI does, per service and shared package.
---

# Go service change gate

Goal: every Go service and shared package you touched passes what CI runs for it, and the tree you leave behind is the tree you checked. CI's definition lives in `.github/workflows/ci.yaml` (the `go` job), `.github/actions/go-ci/action.yaml` and `.github/scripts/go-ci-test.sh`; when anything below disagrees with them, they win.

## Commands

From the repository root (one Go module, `github.com/telark/telark`; no `go.work`):

```sh
go build ./...
go vet ./...
go test -race ./...

# last, after every edit and after deleting scratch files; once per service or shared package you touched
golangci-lint run ./services/<svc>/...   # or ./internal/<pkg>/...
```

A shared package in `internal/` is compiled into every service that imports it, so build, vet and test always cover the whole module. `make check` runs lint per service and shared package and `go test ./...`, plus `helm lint` (which needs `make deps` once).

## What to check

- **Coverage.** Tests live in `internal/tests/<area>/`, so only cross-package coverage means anything. When a change could move the coverage of a service or shared package, run what CI runs (`./internal/<pkg>/...` for a shared package) and compare with its floor in `ci.yaml`:

  ```sh
  go test -race -gcflags=all=-dwarf=false -ldflags=-w -coverpkg=./services/<svc>/... -coverprofile=coverage.out ./services/<svc>/...
  go tool cover -func=coverage.out | tail -1
  ```

  Raise the floor when coverage clearly improves; never lower it.
- **Test placement.** No `*_test.go` or `*_internal_test.go` beside production code. Move any test you or a sub-agent created outside `internal/tests/` (a shared package's `tests/`) before reporting done. Never add test seams to production code: no `*ForTest` functions and no exported setters or constructors that exist only for tests or mutate package state. Test through the exported API production already uses; export an unexported function only when production calls it the same way. The one in-package test file is discovery's `coalesce_internal_test.go`.
- **Lint result.** Zero errors, with the repository's root `.golangci.yml`. No `--no-config`, config-override flags or `//nolint`; when a finding is unclear, read `.golangci.yml`. Read the linter's summary instead of grepping for `file:line:col`, since the output can group issues by file. Pre-existing errors in files you didn't touch: flag them, don't silently fix them.
- **Linter version.** Lint with the golangci-lint version CI pins (`version:` in `.github/actions/go-ci/action.yaml`), not whichever one is installed: newer releases add checks, so an older local linter can report 0 issues on code CI then fails. Compare with `golangci-lint version`; when they differ, install the pinned one into a temporary directory (`GOBIN=<dir> go install github.com/golangci/golangci-lint/v2/cmd/golangci-lint@<version>`) and run that binary.
- **Linter and Go version.** golangci-lint only handles Go versions up to the one it was built with. If it reports that its Go version is lower than the targeted one, upgrade golangci-lint to the pinned version; don't pin `GOTOOLCHAIN` to an older Go.
- **A passing build proves nothing about lint.** `revive` flags design issues the compiler accepts, so show the lint result in your report.
- **Module files.** Dependencies live in the root `go.mod` and `go.sum` only. Never add a `go.work`, a nested `go.mod` or `replace` directives.

## Report

Name the services and shared packages you gated and give the lint result. If the change needs a new image before it takes effect, say so once; don't bump versions.
