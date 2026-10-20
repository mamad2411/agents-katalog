---
name: test-setup
description: "Sets up the test strategy and infrastructure for the chosen stack — unit/e2e runners, testcontainers or a compose test profile, contract tests from GraphQL/OpenAPI, axe/Lighthouse/k6 hooks, CI stages, coverage thresholds — into docs/architecture/test-strategy.md and, with `--apply`, config files. Run after /setup-stack before the first story, for 'set up testing', 'add e2e tests'."
argument-hint: "[--apply]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion, Task
---

# Test Setup

Reply in the project conversation language (CLAUDE.md → Language); code, identifiers, paths and commit messages stay in English.

Template `templates/test-strategy.md`; reference `stack-reference/testing.md`; rules `rules/tests.md`.

In the steps below, `<templates>` is `.claude/docs/templates/` in copy mode and `${CLAUDE_PLUGIN_ROOT}/docs/templates/` in plugin mode; a studio agent is `web-studio:<name>` in plugin mode and `<name>` in copy mode; `<hooks>` is `.claude/hooks/` in copy mode and `${CLAUDE_PLUGIN_ROOT}/hooks/` in plugin mode.

## Phase 1: Stack and current state
1. **Read** `.claude/docs/technical-preferences.md`. When it is missing or its `**Type**:` is still `[TO BE CONFIGURED]`, stop with `BLOCKED (stack not configured — run /setup-stack first)` and write nothing.
2. **Inventory** what exists (`vitest.config`, `playwright.config`, `phpunit.xml`, `_test.go`, workflows) and list the gaps.
3. **Docker.** Run `docker --version`. Without docker, say that the compose test profile and testcontainers cannot run here; the strategy is still drafted, the Phase 4 compose self-check is named as skipped, and the verdict is `PARTIAL (missing tool: docker)`.

## Phase 2: Strategy (draft)
1. **Levels**: a table of tools per level and language.
2. **The `test` environment**: compose profile or testcontainers.
3. **Contract tests** per API style: GraphQL — codegen check + N+1 test; REST — schema validation.
4. **Stages and rules**: security/a11y/perf stages; thresholds; flaky rules (no fixed waits, errors by identity).
5. **PHP** under `php_architecture: layered`: the tests-by-layer table from `php.md` — domain with data providers and no doubles, application with mocked ports, infrastructure in `tests/Integration/` with containers — and the coverage gate with the thresholds from technical-preferences (default Domain 90 % / Application 80 %).
6. **Go** under `go_architecture: layered`: the tests-by-layer table from `go.md` — domain without doubles, use cases with fakes/`moq`, infrastructure with containers — and the coverage gate with the thresholds from technical-preferences (default domain 90 % / usecase 80 %).
7. **CI stages** within the budget rules of `stack-reference/tooling-devops.md` § CI: one job per toolchain, `paths:` filters, e2e and security on pull requests to the default branch, `concurrency: cancel-in-progress`, `runs-on: ${{ vars.CI_RUNNER || 'ubuntu-latest' }}`. Estimate the minutes per run and per month at the project's current merge rate. On a private repository the free tier is 2 000 minutes a month and every job is rounded up to the minute, so a seven-job pipeline of forty-second jobs costs seven minutes per push.
8. **Config list**: the files Phase 4 will create or change (per the Go and PHP lists there, the CI workflow, any compose fragment).

## Phase 3: Write gate
1. **Show** the strategy rendered as tables, and the config list.
2. **Ask** "May I write `docs/architecture/test-strategy.md` and the configs [list]?" as one `AskUserQuestion`: write (Recommended) · show the draft/diff first · not now. Configs are generated only with `--apply` or with consent in this answer; either way nothing is written before it.
3. After the "write" answer: `touch .claude/.write-consent` (rule 7 — the consent-guard hook checks the marker).
4. **Write** `docs/architecture/test-strategy.md`.

## Phase 4: Configs (`--apply` or with consent)
`test-engineer` via Task writes the configs and a first smoke test per level; `devops-engineer` writes the CI stages. The brief lists exactly the files the Phase 3 answer covered. A subagent cannot ask the user: anything beyond its brief comes back to the parent, which asks.

**Go module** — templates from `<templates>go/`, copied with `cp`, never retyped:
1. `.golangci.yml` from `golangci.yml`: `MODULE_PATH` replaced from `go.mod`; the `depguard` block kept under `layered`, removed under `modular`; `go_domain_allow` entries added to the `domain` allow-list.
2. `scripts/coverage-gate.sh` from `coverage-gate.sh`, then `chmod +x` (a file created with Write has no exec bit).
3. The `fmt`/`lint`/`test`/`coverage-gate`/`layout-check`/`arch-check`/`ci`/`ci-full` targets from `Makefile.snippet`, merged into the Makefile with `GO_COVERAGE_DOMAIN`/`GO_COVERAGE_USECASE` set from technical-preferences; `layout-check` is dropped from `ci` under `go_composition_root: main`.
4. `moq` as a `tool` directive when a port has more than three methods.
5. `make ci` runs once and its output is in the result. A gate that has never failed on purpose is not known to work, so the run also shows `make coverage-gate GO_COVERAGE_DOMAIN=100` failing on the current numbers.

**PHP project** — templates from `<templates>php/`, copied with `cp`:
1. `deptrac.yaml`: `FRAMEWORK_NAMESPACES` replaced by the value the framework file names (`yii3.md`, `symfony.md`, `laravel.md`, `php.md` for slim/none); kept under `layered`, removed under `framework`; `php_domain_allow` namespaces added to the `Vendor` layer.
2. The analyser config for `php_static_analysis` (`phpstan.neon` / `psalm.xml`) and the coding-standard config for `php_cs_tool` (`ecs.php` / `.php-cs-fixer.dist.php`).
3. `phpunit.xml`, with `tests/Unit/` and `tests/Integration/` created and a `.gitkeep` in the empty one.
4. `scripts/coverage-gate.php`.
5. The `scripts` block from `composer-scripts.json` merged into `composer.json`, with the lines of the chosen tools, and the thresholds from technical-preferences written into the `coverage-gate` line.
6. `require-dev`: `deptrac/deptrac`, the analyser, the standard tool (with `slevomat/coding-standard` when it is `ecs` — the template's comment sniffs need it) and `phpunit/phpunit:^13`; pcov in the CI image.
7. `composer ci` runs once and its output is in the result; the run also shows `composer coverage-gate -- Domain=100` failing on the current numbers.

**CI** stages follow the Phase 2 budget rules. Every command run in this phase has its output in the result.

**Everything the generated CI references must exist after this run.** A compose profile or service named in a workflow (`docker compose --profile test …`) is created in the same run as a minimal `compose.yaml` fragment (profile + services with healthchecks). Otherwise stop with `BLOCKED (compose profile 'test' missing — story S-NNN adds it)`, naming the story — never a CI that cannot pass.

**Self-check** before finishing: `docker compose --profile test config` when docker is available, and every service named in `test-strategy.md` exists in compose.

## Phase 5: Commit (documents lane)
Right after the write, one commit gate (rule 7, `.claude/docs/git-workflow.md` § Documents): `docs: test strategy`, staging exactly the written pipeline documents. Record the gate before asking — `<hooks>session-state.sh set Gate "/test-setup Phase 5: commit?"` — and clear it after the answer (`<hooks>session-state.sh set Gate "—"`).
- On the default branch when no story work is in progress.
- When HEAD is a story branch, name it and ask one `AskUserQuestion`: switch to the default branch and commit there (Recommended — a pipeline-wide document) · commit here (the document belongs to this story) · leave uncommitted.
- Configs, CI workflows and scripts are toolchain work, not documents: they do not ride the `docs:` commit. Name them in the result and offer the chore lane for them (git-workflow.md § Chore / infra).

Nothing is committed without the answer.

Verdict: `COMPLETE` | `PARTIAL (missing tool: …)` | `BLOCKED (compose profile missing — …)` | `BLOCKED (stack not configured — …)`. The report states the estimated CI minutes per run and per month. Next step — one `AskUserQuestion`: `/create-stories` (Recommended) · `/qa-plan` · revise the strategy.
