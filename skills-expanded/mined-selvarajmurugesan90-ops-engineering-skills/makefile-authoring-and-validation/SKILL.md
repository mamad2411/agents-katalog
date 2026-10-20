---
name: makefile-authoring-and-validation
description: >
  Authors Makefiles as a build/automation entry point for ops tasks —
  `.PHONY` target conventions, dependency graphs between targets,
  variable/default handling, and self-documenting `help` targets — and
  validates them with `make -n` (dry-run) and `checkmake`/shellcheck-style
  linting before they're relied on in CI or by other engineers. Use when
  the user asks to "write a Makefile for this project," "add a build/lint/
  test target to the Makefile," "why does `make` rebuild everything every
  time," "make targets phony," or "lint/validate this Makefile."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: iac-and-automation-tooling
  maturity: stable
---

# Makefile Authoring and Validation

## Purpose

A Makefile gives a project one consistent, discoverable entry point —
`make build`, `make test`, `make deploy` — for tasks that would otherwise
be scattered across READMEs, wiki pages, and tribal knowledge about the
"right" flags to pass a dozen different tools. Make's actual execution
model (file-timestamp-based dependency resolution, skipping targets whose
prerequisites haven't changed) is a genuine feature for build targets
that produce real files (compiled binaries, generated code), but it is
also the single most common source of Makefile bugs: a target that
doesn't produce the file it's named after, or is meant to always run
(`test`, `deploy`, `clean`), silently gets treated as "up to date" and
skipped, or a stale intermediate file causes `make` to skip work that
should have re-run. This skill covers writing Makefiles as reliable ops
automation, not the C/C++ compiled-build use case Make originated for.

## When to use

- Standardizing a project's build/test/lint/deploy commands behind a
  single `make <target>` interface instead of a scattered collection of
  shell scripts and README-documented raw commands.
- Adding a new target to an existing Makefile (a new lint check, a new
  deploy environment, a new codegen step).
- Debugging why `make <target>` either reruns every time even with no
  changes, or — the more dangerous direction — silently does nothing
  because Make thinks the target is already up to date.
- Reviewing or hardening a Makefile before it's relied on in CI, where a
  quietly-skipped target can pass a pipeline that should have failed.
- Wiring `make -n` (dry-run) into a review/validation step, or adding a
  linter (`checkmake`) to CI for Makefile changes.

## Prerequisites & environment

- GNU Make ≥ 4.0 is the practical baseline for most Linux/CI environments
  (supports `.ONESHELL`, `$(file ...)`, better function/variable
  handling); BSD/macOS ships an older `make` (BSD Make, not GNU Make) by
  default, which lacks several GNU-only functions (`$(shell ...)` works
  on both, but pattern-rule and function syntax differ) — confirm which
  `make` a script targets if portability across Linux and macOS matters,
  or require `gmake` explicitly.
- `checkmake` (a Makefile linter) and/or `shellcheck` for any embedded
  shell fragments inside recipe lines — recommended for any Makefile with
  more than a handful of targets or more than one contributor.
- A single shell assumed consistent per recipe: Make invokes each recipe
  line in a *new* shell by default (unless `.ONESHELL:` is set), which
  matters for anything using `cd`, `set -e`, or shell variables across
  lines (see pitfalls).
- Nothing runtime-specific beyond whatever the targets themselves invoke
  (Docker, a compiler, `terraform`, `kubectl`, etc.) — Make itself has no
  dependencies beyond being installed.

## Step-by-step guidance

1. **Mark every non-file-producing target `.PHONY`.** This is the single
   most important Makefile-authoring habit: without it, a target sharing
   its name with a file/directory in the working tree (`test`, `clean`,
   `docs`) silently does nothing once that file/directory exists, because
   Make treats the target as "a file that already exists and has no
   newer prerequisites."
   ```makefile
   .PHONY: build test lint clean deploy help

   build:
   	go build -o bin/app ./cmd/app

   test:
   	go test ./...

   lint:
   	golangci-lint run ./...

   clean:
   	rm -rf bin/
   ```
   > **Warning:** `clean` targets commonly `rm -rf` a build directory —
   > keep the removed path scoped and explicit (`rm -rf bin/`, never a
   > bare `rm -rf $(SOME_VAR)` where `SOME_VAR` could resolve empty and
   > expand to `rm -rf /`), and never mark a target that deletes anything
   > outside the project's own build artifacts as a "safe default" without
   > a confirmation step for anything destructive beyond local build output.

2. **Model real file-based dependency graphs for targets that actually
   produce files**, so Make's incremental-rebuild behavior works for you
   instead of against you:
   ```makefile
   bin/app: $(shell find ./cmd ./internal -name '*.go')
   	go build -o bin/app ./cmd/app

   .PHONY: build
   build: bin/app
   ```
   Now `bin/app` only rebuilds when a `.go` file actually changed —
   `build` itself stays `.PHONY` (always evaluated) but its real
   prerequisite (`bin/app`) is timestamp-based, giving correct
   incremental behavior without accidentally skipping the phony wrapper.

3. **Use `:=` (immediate expansion) for variables by default**, reserving
   `=` (recursive/lazy expansion) only when a variable's value must
   depend on something evaluated later:
   ```makefile
   GIT_SHA := $(shell git rev-parse --short HEAD)
   IMAGE_TAG := myapp:$(GIT_SHA)

   .PHONY: docker-build
   docker-build:
   	docker build -t $(IMAGE_TAG) .
   ```
   With `=` instead of `:=`, `$(shell git rev-parse ...)` would re-run on
   every reference to `GIT_SHA`, not just once — usually not what's
   intended and needlessly slow for anything shelling out.

4. **Give every target a default (safe) behavior and support overrides via
   variables, not hardcoded values**:
   ```makefile
   ENV ?= dev

   .PHONY: deploy
   deploy:
   	@echo "Deploying to $(ENV)"
   	./scripts/deploy.sh --env $(ENV)
   ```
   ```bash
   make deploy            # deploys to dev (the safe default)
   make deploy ENV=prod   # explicit override required for prod
   ```
   `?=` only sets the variable if it isn't already set (by the
   environment or a `make VAR=value` invocation), giving a safe default
   without silently overriding an explicit caller choice.

5. **Add a self-documenting `help` target** so `make help` (or bare
   `make`) lists available targets with a one-line description, rather
   than requiring a reader to open the Makefile:
   ```makefile
   .DEFAULT_GOAL := help

   .PHONY: help
   help: ## Show this help
   	@grep -E '^[a-zA-Z0-9_-]+:.*##' $(MAKEFILE_LIST) | \
   		awk 'BEGIN {FS = ":.*##"}; {printf "  %-15s %s\n", $$1, $$2}'

   build: ## Build the binary
   	go build -o bin/app ./cmd/app

   test: ## Run the test suite
   	go test ./...
   ```

6. **Validate with `make -n` (dry-run) before trusting a new/changed
   target**, especially one with side effects:
   ```bash
   make -n deploy ENV=staging
   ```
   `-n` prints every recipe command Make *would* run, without executing
   any of them — the fastest way to confirm a target expands variables
   the way you expect (e.g. that `$(ENV)` resolved to `staging`, not an
   empty string) before it actually runs `./scripts/deploy.sh`.

7. **Lint the Makefile itself in CI**:
   ```bash
   checkmake Makefile
   ```
   `checkmake` flags missing `.PHONY` declarations, undefined variables
   referenced in recipes, and other structural issues that are easy to
   introduce and easy to miss in review since Makefile syntax (tabs vs.
   spaces, `$@`/`$<` automatic variables) is unfamiliar to many
   reviewers.

8. **Use `.ONESHELL:` deliberately when a recipe needs shared shell
   state across lines**, since Make's default (one new shell per line)
   silently discards `cd`/variable state between lines:
   ```makefile
   .ONESHELL:
   deploy-and-verify:
   	cd deploy/
   	terraform apply -auto-approve tfplan
   	./verify.sh
   ```
   Without `.ONESHELL:`, the `cd deploy/` on line one has zero effect on
   line two — `terraform apply` would run from the original directory,
   not `deploy/` — a very common and non-obvious Makefile bug.

## Best practices

- Set `SHELL := /bin/bash` (or `sh` with explicit POSIX-safe recipes)
  and, for any Makefile with multi-line recipes, `.SHELLFLAGS := -eu -o
  pipefail -c` so a failing command mid-recipe stops the target instead
  of Make silently continuing to the next line — mirroring the
  strict-mode discipline in
  [shell-scripting-best-practices](../shell-scripting-best-practices/SKILL.md).
- Prefix noisy/expected commands with `@` (suppress echoing the command
  itself) sparingly — full echoing is usually more useful for debugging a
  failing CI run than a quiet Makefile.
- Keep non-trivial logic in a real script (`scripts/deploy.sh`) invoked
  from a thin Makefile target, rather than growing a multi-line shell
  script inline inside a recipe — the script gets its own shebang, can be
  run/tested standalone, and is easier to lint with `shellcheck`.
- Never name a `.PHONY` target after a directory the project actually
  has (`docs`, `build`, `dist`) unless it is genuinely marked `.PHONY` —
  the collision is the single most common Makefile footgun (see pitfalls).
- Keep `deploy`-style targets requiring an explicit environment variable
  with no unsafe default (`ENV` with no `?=` fallback, or a fallback of
  `dev`/`staging` — never a fallback that resolves to production).
- Run `make -n` as a required CI check on any PR touching the Makefile,
  catching a broken/undefined variable reference before it's discovered
  by someone actually running the target.

## Common pitfalls

- **Symptom:** `make test` (or `make clean`, `make deploy`) does nothing
  the second time it's run, printing `make: 'test' is up to date.`
  **Fix:** A file or directory literally named `test` (or `clean`,
  `deploy`) exists in the working tree, and the target isn't declared
  `.PHONY`, so Make treats it as a file target with no newer
  prerequisites. Add it to `.PHONY:`.

- **Symptom:** A recipe's `cd some-dir` on one line appears to have no
  effect — the next line's command runs from the original directory.
  **Fix:** Each recipe line runs in its own fresh shell by default; `cd`
  (and any exported variable) doesn't persist to the next line. Either
  chain commands with `&&`/`;` on one logical line (using `\` for
  continuation), or set `.ONESHELL:` for that Makefile/target so the
  whole recipe runs in one shell.

- **Symptom:** A recipe silently continues and reports success even
  though one of its middle commands actually failed.
  **Fix:** Make only fails a recipe if the *last* command on a given
  line/shell-invocation returns non-zero, by default, and doesn't apply
  `set -e` automatically. Set `.SHELLFLAGS := -eu -o pipefail -c`
  (with `SHELL := /bin/bash`) so any failing command in a recipe halts
  it immediately, the same as a well-written standalone shell script
  would.

- **Symptom:** A variable referenced in a recipe (`$(FOO)`) silently
  expands to empty instead of erroring, and a command runs with a
  missing argument.
  **Fix:** Make does not error on undefined variables by default — it
  substitutes an empty string. Run `make -n` to see the actual expanded
  command before running for real, and consider `ifndef FOO
  $(error FOO is not set) endif` guards for variables a target genuinely
  cannot run safely without.

- **Symptom:** Tab-vs-spaces indentation causes `make: *** missing
  separator. Stop.` on a Makefile that looks correctly indented in an
  editor with tab-to-space conversion enabled.
  **Fix:** Make recipe lines must be indented with a literal tab
  character, not spaces — configure the editor/`.editorconfig` to
  preserve real tabs for `Makefile`/`makefile` specifically, and run
  `checkmake` or `make -n` in CI to catch this before merge rather than
  relying on visual inspection.

## Worked example

**Scenario:** A service repo needs a Makefile standardizing build, test,
lint, and a guarded deploy, with a self-documenting help target and a
dry-run-validated deploy path.

```makefile
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

GIT_SHA := $(shell git rev-parse --short HEAD)
IMAGE_TAG := checkout-api:$(GIT_SHA)
ENV ?= dev

.PHONY: help build test lint docker-build deploy clean

help: ## Show available targets
	@grep -E '^[a-zA-Z0-9_-]+:.*##' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*##"}; {printf "  %-15s %s\n", $$1, $$2}'

bin/app: $(shell find ./cmd ./internal -name '*.go' 2>/dev/null)
	go build -o bin/app ./cmd/app

build: bin/app ## Build the binary (incremental on source changes)

test: ## Run the test suite
	go test ./...

lint: ## Run static analysis
	golangci-lint run ./...

docker-build: ## Build a tagged container image
	docker build -t $(IMAGE_TAG) .

deploy: build test ## Deploy to ENV (default: dev; override with ENV=staging|prod)
	@echo "Deploying $(IMAGE_TAG) to $(ENV)"
	./scripts/deploy.sh --env $(ENV) --image $(IMAGE_TAG)

clean: ## Remove build artifacts
	rm -rf bin/
```

Validation before trusting `deploy` against a real environment:
```bash
make -n deploy ENV=staging
# go build -o bin/app ./cmd/app
# go test ./...
# echo "Deploying checkout-api:a1b2c3d to staging"
# ./scripts/deploy.sh --env staging --image checkout-api:a1b2c3d

checkmake Makefile
# Makefile:0: PhonyRule: expected target "clean" to be phony (already declared, passes)
```
Reviewing the `-n` dry-run output before the first real `make deploy
ENV=staging` confirms `$(ENV)` and `$(IMAGE_TAG)` expand as intended and
that `build`/`test` genuinely run first as prerequisites — catching a
misconfigured variable before `deploy.sh` ever executes against a real
environment.

## Cross-references

- [shell-scripting-best-practices](../shell-scripting-best-practices/SKILL.md) — strict-mode/quoting guidance for any non-trivial script a Makefile target shells out to.
- [python-automation-scripting-for-ops](../python-automation-scripting-for-ops/SKILL.md) — an alternative for automation logic that's grown beyond what a Makefile recipe should reasonably contain inline.
- [ci-cd-pipeline-design](../../../devops/skills/ci-cd-pipeline-design/SKILL.md) — where `make build`/`make test`/`make deploy` targets typically get invoked from within a pipeline's stages.
