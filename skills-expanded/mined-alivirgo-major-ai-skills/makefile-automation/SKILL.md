---
name: makefile-automation
description: "Design Makefile targets, dependencies, variables, and discoverable repository automation commands."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["makefile", "make", "automation", "phony", "devops", "dx"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Makefile Automation AI Skill Guide

## Overview

Make is a dependency-aware task runner. A **Makefile** declares targets, prerequisites, and recipes so agents and humans share stable entrypoints (`make test`, `make build`, `make fmt`). Good Makefiles are self-documenting, use `.PHONY` for non-file targets, fail on errors (`set -e` semantics via flags), and avoid hiding destructive operations behind innocent names.

```
make <target>
     |
     v
dependency graph -> recipes (shell lines)
     |
     +--> tools: go test, npm, docker, terraform, ...
```

## When to use

- Standardizing repo commands across local and CI
- Encoding multi-step build/lint/test/release flows
- Generating help text for onboarding
- Wrapping messy tool invocations behind stable names

## Operational directives

1. Mark non-file targets `.PHONY` so Make does not skip them when a file/folder shares the name.
2. Use `SHELL := bash` and `.SHELLFLAGS := -eu -o pipefail -c` for safer recipes.
3. Provide a `help` target as the default goal.
4. Keep recipes idempotent where practical; name destructive targets explicitly (`destroy`, `reset-db`).
5. Prefer variables for versions and paths; allow overrides (`make build IMAGE_TAG=...`).

## Concrete examples

### Self-documenting Makefile

```make
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c

APP      ?= api
IMAGE    ?= ghcr.io/example/$(APP)
GIT_SHA  := $(shell git rev-parse --short HEAD)
TAG      ?= $(GIT_SHA)

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z0-9_-]+:.*?##/ {printf "  %-16s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: fmt
fmt: ## Format code
	go fmt ./...

.PHONY: test
test: ## Run unit tests
	go test ./...

.PHONY: build
build: test ## Build container image
	docker build -t $(IMAGE):$(TAG) .

.PHONY: run
run: ## Run API locally
	go run ./cmd/api

.PHONY: clean
clean: ## Remove build artifacts
	rm -rf dist/
```

### Pattern rules and generated files

```make
dist:
	mkdir -p dist

dist/app: $(shell find . -name '*.go') | dist
	go build -o $@ ./cmd/api
```

### Include env-specific fragments

```make
-include .env.mk
# .env.mk is gitignored; developers may set REGISTRY=...
```

### Parallelism note

```bash
make -j4 test build   # only when targets are safe concurrently
```

## Design table

| Pattern | Use when |
| :--- | :--- |
| `.PHONY` task | Lint/test/deploy verbs |
| Real file target | Compilation outputs under `dist/` |
| `##` help comments | Human discovery |
| `$(MAKE) -C dir` | Multi-module monorepos |

## Best practices

1. Keep recipes short; call scripts under `scripts/` for complex logic.
2. Mirror CI job names to Make targets so docs stay accurate.
3. Quote variables and paths with spaces carefully; prefer no spaces in artifact paths.
4. Document required tools (`make doctor` that checks versions).

## Limitations

- Make is not a full DAG workflow engine for cloud pipelines (still useful as a local facade).
- Windows users may need GNU Make via Git Bash/WSL - note that in README when relevant.
- Hidden recursive Make can obscure failures - keep nesting shallow.

## Related skills

- `docker` - common `make build` / `make compose-up` wrappers
- `pulumi` - `make preview` / `make up` guarded targets
- `trivy` - `make scan` gate before push
- `sqlite` / `mysql` - `make db-migrate` database helpers
