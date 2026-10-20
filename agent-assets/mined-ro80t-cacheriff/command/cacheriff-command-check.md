---
description: Run cacheriff's CI checks locally (gofmt, vet, build, test)
---

Run these checks in order and report the results. Stop and fix the root
cause of the first failure rather than continuing past it:

1. `gofmt -l .` — must print nothing. If it prints file names, run
   `gofmt -w .` and re-check.
2. `go vet ./...` — must be clean.
3. `go build ./...` — must succeed.
4. `go test ./... -race -cover` — must pass.

These are the same checks `.github/workflows/ci.yml` runs.
