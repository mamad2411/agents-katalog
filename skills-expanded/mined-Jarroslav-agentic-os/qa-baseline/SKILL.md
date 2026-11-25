---
name: qa-baseline
version: 0.1.0
license: Apache-2.0
description: >-
  Bootstrap the QA knowledge foundation for a repo: discover test files, coverage
  reports, CI test gates, and QA docs; configure adapters to external QA sources
  (test-case management, QA documentation, external test repos); then write two
  persistent guides — qa-strategy.md and qa-health.md — under
  .agentic/guides/testing/. Invoke on first-time QA setup, when the user says
  "qa init", "qa foundation", or "set up qa", or via the slash command
  /sdlc:qa-init. These guides are consumed downstream by the qa-scoping skill on
  every feature run, so run this once before the first /sdlc:start or /sdlc:story.
  Not for: per-feature test planning (qa-scoping), running gates (gate-runner), or day-to-day QA work once the foundation exists.

---

# qa-baseline

## Shared contract preflight

Before workflow actions, send this JSON request to the installed plugin's
`runtime/run.py` using Python 3.10+ (resolve the plugin root on the current host):

```json
{"api_version":"1.0.0","operation":"policy.resolve","entrypoint":"qa-baseline"}
```

Use the returned policy and `references/runtime-contracts.md` for contract identifiers,
limits and dependency floors. Unknown fields or incompatible versions block startup.
Task envelopes use `contract_version: "1.0.0"` and `task_input`; legacy `raw_input`
is accepted only by the explicit `input.normalize` compatibility adapter with `legacy: true`.
This preflight validates policy; durable lifecycle and host enforcement are separate
capabilities. Never infer those capabilities from a successful policy response.


Build a durable QA knowledge base by inspecting the current repo and (optionally)
external QA systems, then persisting what you learn as two guide files. Downstream,
`qa-scoping` reads both files on every feature run — this skill is the one-time
seed that makes that possible.

**Blast radius: R2** (writes repo guide files). No file is written until the user
approves at the Phase 4 gate. Phase 1 is strictly read-only.

> **Methodology owner.** How qa knowledge is gathered, structured and kept current is defined by the `qa-knowledge-base`
> blueprint in `agentic-qe`
> (`skills/qe-blueprints/references/catalog/analyze/qa-knowledge-base.md`). This skill
> executes; the blueprint is the authority on method. If the two ever disagree,
> the blueprint wins and this file is what gets corrected — one source of truth,
> so two agents cannot follow two different sets of practices.

## When to use

- First-time QA setup in a repo, before any pipeline run.
- Trigger phrases: `qa init`, `qa foundation`, `set up qa`.
- Slash command: `/sdlc:qa-init`.

Do **not** use this to run or author tests — it discovers and configures only.

## Outputs (path contract)

| File | Purpose |
|------|---------|
| `.agentic/guides/testing/qa-strategy.md` | How this repo tests: frameworks, types, coverage targets, conventions, anti-patterns, external sources. |
| `.agentic/guides/testing/qa-health.md` | Current QA state: coverage summary, risky untested areas, test debt, recent activity. |

Both artifacts overwrite on re-run. The skill is idempotent and safe to re-run.

## Flow

Five phases, in order. Nothing is written to disk before Phase 5, and Phase 5 is
gated on explicit user approval in Phase 4.

### Phase 1 — Discovery (read-only)

Scan the current repo for QA signals. For each signal record: absolute path,
type, and detected framework. Write nothing.

Signal catalog:

| Type | Paths / patterns |
|------|------------------|
| Test directories | `tests/`, `__tests__/`, `spec/`, `e2e/`, `cypress/`, `playwright/` |
| Coverage reports | `coverage/`, `.nyc_output/`, `htmlcov/`, `coverage.xml`, `lcov.info` |
| Test config | `jest.config.{js,ts,mjs,cjs}`, `pytest.ini`, `setup.cfg`, `playwright.config.{ts,js}`, `.nycrc`, `vitest.config.{ts,js}` |
| CI test gates | `.github/workflows/*.yml`, `.gitlab-ci.yml`, `Jenkinsfile` — extract steps matching: test, coverage, e2e, playwright, cypress, pytest, jest, vitest |
| Local QA docs | files matching `*test-plan*`, `*test_plan*`, `*strategy*`, `*test-cases*`, `*testcases*` |

**Coverage extraction.** If a coverage report exists, extract quantitative
metrics: overall line %, overall branch %, a per-module breakdown, and the set of
zero-coverage modules. Recognized formats: Istanbul/NYC JSON, pytest-cov XML,
lcov. If no report exists, mark coverage **qualitative-only** and do not fabricate
numbers.

**Recent test activity.** Capture the 5 most recent test files with (verbatim):

```
git log --diff-filter=AM -- '*test*' '*spec*' -n 5 --name-only --pretty=''
```

### Phase 2 — Interactive Q&A (external sources)

Ask **one question at a time**. Configure adapters — never hardcode a backend.
Seed these state variables:

```
external_test_repos: []
test_case_adapter: {system, access}
qa_docs_adapter: {system, access}
qa_docs_paths: []
```

- **Q1 — External test repos.** Any test suites living outside this repo? Collect
  answers into `external_test_repos`.
- **Q2 — Test case management.** Options: `Jira/Zephyr` | `TestRail` | `Azure
  DevOps (ADO)` | `none`. Store the choice as `test_case_adapter.system`. If not
  `none`, follow up for adapter access — an MCP tool, skill, or CLI — and store it
  as `test_case_adapter.access`. Access strings name a concrete adapter, e.g.
  `mcp__jira__jira_search`. When no access is configured, use the sentinel
  `not configured`.
- **Q3 — QA documentation location.** Options: `Confluence` | `Google Docs` |
  `local file path` | `within this repo` | `none`. Store as
  `qa_docs_adapter.system`.
  - `Confluence` or `Google Docs` → ask for adapter access → store
    `qa_docs_adapter.access`.
  - `local file path` → ask for absolute paths → store them into `qa_docs_paths`.

> Adapters keep the skill vendor-neutral: the same flow serves any ticket system,
> wiki, or doc store because access is a configured MCP/skill/CLI reference, not a
> baked-in integration.

### Phase 3 — Scan external sources

- Fetch external test-case summaries **only when** `test_case_adapter.access` is
  configured and not `not configured`. Pull up to **20** test case summaries.
- Fetch QA docs **only when** `qa_docs_adapter.access` is configured.
- Ground everything in what the adapters actually return — never invent test cases
  or doc content absent from the fetched inputs.

### Phase 4 — Approval gate (hard)

Present a summary of everything discovered and configured: repo signals, the
coverage verdict, adapter wiring, and the two files about to be written. **Do not
write any file until the user replies with approval.** On corrections, apply them,
re-show the full summary, and loop until the user approves.

### Phase 5 — Generate artifacts + handoff

Write both files (overwriting any prior versions), then hand off.

`.agentic/guides/testing/qa-strategy.md` sections:

- **Test Frameworks** — table: framework / type / config / dirs.
- **Test Types** — Unit / Integration / E2E, each with location, pattern, run
  command, and an example `path:line`.
- **Coverage Targets** — line %, branch %, coverage command.
- **Conventions** — naming, location, style.
- **Anti-Patterns** — table: bad / better / why.
- **External Sources** — test case management, QA docs, external repos.

`.agentic/guides/testing/qa-health.md` sections:

- **Header** — Last assessed; Coverage % (or qualitative).
- **Coverage Summary** — table: module / coverage / notes.
- **Risky Untested Areas** — table: path / coverage / risk reason.
- **Known Test Debt**.
- **Recent Test Activity** — the 5 most recent test files.

**Handoff.** Point the user at the next step: `/sdlc:start` or `/sdlc:story`.

## Decision rules (quick reference)

| Condition | Action |
|-----------|--------|
| Coverage report present | Extract quantitative line/branch %, per-module, zero-coverage set |
| No coverage report | Qualitative assessment only; no computed numbers |
| Q2 ≠ `none` | Ask for adapter access; store `test_case_adapter.access` |
| Q3 = Confluence / Google Docs | Ask for adapter; store `qa_docs_adapter.access` |
| Q3 = local file path | Ask for absolute paths; store `qa_docs_paths` |
| `test_case_adapter.access` configured (≠ `not configured`) | Fetch ≤20 test case summaries |
| `qa_docs_adapter.access` configured | Fetch QA docs |
| Before the Phase 4 approval reply | Write nothing |

## Inputs

- The current repository working tree (Phase 1 discovery).
- User answers to the Phase 2 questions.
- Whatever the configured adapters return in Phase 3 (bounded: ≤20 test cases).

## Non-goals

- Does not run or author tests.
- Writes nothing during Phase 1 or before the Phase 4 approval gate.
- Does not hardcode any test-case backend or QA-docs backend — all external
  access is adapter-driven (MCP / skill / CLI).
- Does not compute quantitative coverage when no report exists.

## Downstream

`qa-scoping` reads both `.agentic/guides/testing/qa-strategy.md` and
`.agentic/guides/testing/qa-health.md` on every feature run. Re-run this skill
when the repo's test posture changes to keep those guides current.
