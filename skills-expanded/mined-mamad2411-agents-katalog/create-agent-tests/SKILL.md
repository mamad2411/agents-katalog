---
name: create-agent-tests
description: "Author, scaffold, and run coding-agent-driven tests: Markdown case files executed by a coding agent against a live environment (browser, API, DB, logs, cloud, telemetry) with an auditable PASS/FAIL/BLOCKED report. Use when a deterministic test would be premature, brittle, too expensive, or too narrow."
---

# Agent Tests

Producer skill for **agent tests**: a coding agent executes a Markdown case file
against a target environment and returns an auditable report. Verification is the
executing agent's judgment plus the evidence it collects (browser, API, DB, logs,
cloud, telemetry), rather than fixed deterministic assertions.

This skill **authors and runs** agent tests. Each case produces an auditable
report — a report path, a final `PASS`/`FAIL`/`BLOCKED`/`ABORTED` status, and the
collected evidence artifacts — for whatever invoked it to consume.

## When To Use Agent Tests

Use agent tests when verification requires flexible, tool-driven judgment across
UI, API, database, logs, files, network, or live-environment state, and a
deterministic test would be premature, brittle, too expensive, or too narrow.

Especially useful for:

- UI changes needing visual, interactive, browser-console, network, or trace
  verification.
- API and DB workflows where confidence requires live requests plus persisted
  state inspection.
- Full-stack flows crossing frontend, backend, storage, jobs, external mocks,
  and cleanup.
- Exploratory regression checks before converting a stable path into a standard
  unit, contract, integration, YAML E2E, or other deterministic test.

Agent tests are **not** a replacement for deterministic tests. Prefer converting
high-value stable agent flows into a standard deterministic test (unit, contract,
integration, YAML E2E, or other) once the path stabilizes.

## Project Layout

Agent tests live under `tests/agent/` in the target repo:

```text
tests/agent/agent-test-suites.json   suite manifest (project-owned)
tests/agent/<feature>/<case>.md       case files, one logical journey each
tests/agent/run-agent-verification.ts runner/orchestrator
agent-test-reports/                    generated reports; do not hand-edit
```

The repo owns its real `agent-test-suites.json`, case files, fixture setup,
auth/session bootstrap, CI wiring, engine secrets and MCP config,
staging/production mutation policies, and cleanup ownership.

## Use The Local Convention First

Before authoring, check for `tests/agent/agent-test-template.md`. If it exists,
treat it as the authoritative local convention. Do not rediscover or replace it
through broad search unless the user explicitly asks to update the convention.

If no local harness exists and an agent test is the cheapest sufficient proof,
scaffold it on demand by copying the bundled starters from this skill:

- `<skill-dir>/assets/agent-test-template.md` → `tests/agent/agent-test-template.md`
- `<skill-dir>/assets/agent-test-suites.example.json` → `tests/agent/agent-test-suites.example.json`
- `<skill-dir>/assets/run-agent-verification.ts` → `tests/agent/run-agent-verification.ts`

Copy these only when a project actually adopts agent tests; do not pre-seed repos
that have none. Then create a real manifest from the example:

```bash
cp tests/agent/agent-test-suites.example.json tests/agent/agent-test-suites.json
```

## Authoring A Case

Write each case from `<skill-dir>/assets/agent-test-template.md` (or the local
template). A good case makes the executing agent unlikely to guess:

- State the requirement, risk, or behavior under test and link its sources.
- Fill real project context: URLs per environment, accounts/orgs, fixture and
  mutation policy, DB/log/cloud access, production synthetic-data policy, and
  cleanup ownership.
- Separate **environment preflight** (prove the target can execute the case)
  from **product verification** (run the checks).
- List concrete checks: browser pages/states, API routes and status codes, DB
  tables/rows, audit events, log filters, telemetry queries, timing.
- Make each assertion **unconditional** for state the test itself creates. A
  check gated on an optional affordance ("if the UI offers X, verify Y") lets
  the agent skip Y and still PASS whenever X isn't found — silently dropping the
  coverage the case exists to provide. For fixtures you control (a freshly
  created token, org, etc.), require the affordance and assert on it directly;
  reserve conditional wording for genuinely environment-dependent surfaces.
- Name the exact evidence each behavior requires.
- Keep cases portable; bind environment specifics under the testing-environments
  section, not in the steps.
- Never store raw secrets. Record variable names, roles, and access patterns
  only.

## Running

Add a package script in the target repo, adjusted for its package manager:

```json
{ "scripts": { "agent:verify": "tsx tests/agent/run-agent-verification.ts" } }
```

Run a suite or a single case:

```bash
pnpm agent:verify --target local --suite smoke --project-name "<project name>"
pnpm agent:verify --target local --case tests/agent/<feature>/<case>.md
```

`references/runner.md` documents the runner defaults, flags, matching
environment variables, and the report status contract in full.

## Report Status Contract

Every case report must end with exactly one line:

```text
Status: PASS
Status: FAIL
Status: BLOCKED
Status: ABORTED
```

- `PASS` / `FAIL`: environment preflight completed and product verification ran.
- `BLOCKED`: environment/setup could not execute the case (missing DB/log access,
  unreachable URL, failed login/session bootstrap, missing fixtures or approval).
  Do not report `FAIL` for an environment blocker.
- `ABORTED`: orchestration interruption only. Release gates ignore ABORTED and
  rerun the case; never end with PASS/FAIL/BLOCKED for an interruption.

Required cases fail the runner unless they return `PASS`.

When a case drives a browser, collect auditable evidence — HTML report,
screenshot set, video, trace, or project-standard equivalent. Text-only browser
claims are not sufficient.

## Output

A run leaves an auditable report at its report path, ending with exactly one
`Status:` line, plus any collected evidence artifacts (HTML report, screenshots,
video, trace, logs). That report and its evidence are the deliverable — whatever
invoked this skill consumes them.

## When Not To Use

- When a deterministic unit, contract, integration, or YAML E2E test is the
  cheaper, more durable proof — use the standard deterministic format instead.
- When no live environment, access, or fixtures are available — record the
  blocker rather than authoring an unrunnable case.
