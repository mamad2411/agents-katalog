# Go Project Structure

## Summary

**One-sentence:** Lay out a Go project with cmd/, internal/, pkg/ (only when public), migrations/, and a single Makefile-driven workflow.

**One-paragraph:** Standard Go project layout following community conventions: cmd/ for entry points, internal/ for private app code, pkg/ only for truly public API surface that external consumers will import, migrations/ for DB DDL, and a single Makefile orchestrating build/test/lint. Imports flow inward (cmd → internal/<feature>); cross-feature dependencies in internal/ go through interfaces declared at consumer side. Output is the directory layout + Makefile + initial wiring.

**Ефективно для:**

- Greenfield Go services adopting community-standard layout.
- Refactoring projects that grew into ad-hoc top-level dirs.
- Multi-binary repos (cmd/api, cmd/worker, cmd/migrate).
- Establishing reviewable boundaries before features compound.

## Applies If (ALL must hold)

- Go module project (Go 1.21+).
- Project size >=1kloc OR contains >=2 binaries.
- Team works in the repo (more than one author).
- Engineering wants enforceable import boundaries (internal/ enforcement).

## Skip If (ANY kills it)

- Single-file CLI experiment — pkg/cmd separation has no payoff.
- Library-only repo (no main) — different conventions apply.
- Project follows a different established pattern (Kubernetes-style, Buf) — adapt instead.
- Monorepo with framework-specific layout (Bazel rules) that overrides.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Module path (go.mod) chosen | go.mod | tech-lead |
| Entry point count (cmd/<name>) | list | tech-lead |
| Public-vs-private API decision: anything in pkg/? | ADR | tech-lead |
| Tooling decision: Make vs Mage vs Justfile | config | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[go-error-handling-patterns]] | apperror package lives under internal/. |
| [[go-concurrency-patterns]] | Worker packages live under internal/. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (cmd for entries, internal for private, pkg only for public, no cyclic deps, makefile orchestration, no top-level loose files) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for project structure spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: skeleton → entries → internal split → makefile → enforce import boundaries | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `skeleton_scaffold` | sonnet | Mechanical: create dirs + go.mod + Makefile. |
| `import_boundary_check` | sonnet | Run import-boundary linter; flag violations. |
| `makefile_authoring` | sonnet | Standard targets: build/test/lint/run/docker. |

## Templates

| File | Purpose |
|------|---------|
| `templates/scaffold-go.sh` | Bootstrap script: create cmd/, internal/, pkg/, migrations/, Makefile |
| `templates/Makefile` | Build/test/lint/run/docker targets |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-project-structure.py` | Validate project structure spec against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[go-standard-layout]]
- [[go-error-handling-patterns]]
- [[go-concurrency-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps project size, binary count, and public-API intent to a rule from `01-core-rules.xml`, telling the agent whether to apply the layout or skip in favour of an alternate convention. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/scaffold-go.sh`

```bash
# scaffold-go.sh — materialise a standard Go project tree
# Usage: ./scaffold-go.sh github.com/org/name api worker
# Creates: cmd/<bin>/main.go, internal/{config,database,handler,middleware,model,repository,service}/, pkg/, api/, Makefile, go.mod

set -euo pipefail

MOD="${1:?module path required (e.g. github.com/org/name)}"
shift
BINS=("$@")

if [[ ${#BINS[@]} -eq 0 ]]; then
  BINS=("api")
fi

mkdir -p api deployments docs scripts pkg

for bin in "${BINS[@]}"; do
  mkdir -p "cmd/$bin"
  cat > "cmd/$bin/main.go" <<GOEOF
package main

import "log"

func main() {
	log.Println("$bin: starting")
}
GOEOF
done

for pkg in config database handler middleware model repository service; do
  mkdir -p "internal/$pkg"
done

go mod init "$MOD"
gofmt -w . 2>/dev/null || true

echo "scaffold ready: $MOD | binaries: ${BINS[*]}"
```

### `templates/Makefile`

```text
# Makefile — standard Go project build automation
# Usage: make build | run | test | lint | clean

BINARY_NAME := api
BUILD_DIR   := ./build
MAIN_PATH   := ./cmd/api

.PHONY: build build-linux run dev test test-coverage lint fmt tidy clean docker-build docker-run

build:
	go build -o $(BUILD_DIR)/$(BINARY_NAME) $(MAIN_PATH)

build-linux:
	CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o $(BUILD_DIR)/$(BINARY_NAME)-linux $(MAIN_PATH)

run:
	go run $(MAIN_PATH)

dev:
	air -c .air.toml

test:
	go test -v ./...

test-coverage:
	go test -v -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html

lint:
	golangci-lint run ./...

fmt:
	gofmt -s -w .
	goimports -w . 2>/dev/null || true

tidy:
	go mod tidy
	go mod verify

clean:
	rm -rf $(BUILD_DIR) coverage.out coverage.html

docker-build:
	docker build -t $(BINARY_NAME):latest .

docker-run:
	docker run -p 8080:8080 $(BINARY_NAME):latest
```
