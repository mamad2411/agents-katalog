---
name: roadguard-test-selection
description: Use when selecting or running sufficient RoadGuard build, endpoint, SQL Server, test, tooling, failure-diagnosis, or handoff verification without stale binaries or redundant suites.
---

# RoadGuard test selection

Read the assigned scope, applicable AGENTS, `planning/V2/TASK_LIFECYCLE.md`, task source checkpoint, changed paths and behavior risk. Reuse already-read rules and still-valid evidence. This skill chooses verification, not permission to broaden implementation. Read [commands and evidence](references/commands.md) only when preparing commands or diagnosing build/test selection.

## Choose breadth once from known impact

| Change | Sufficient verification |
|---|---|
| Docs/tooling only | Relevant static verifier/diff/link check; no runtime tests |
| Entity-local invariant/calculation | Focused UnitTests |
| Service policy/controller | Focused tests for changed policy plus real endpoint smoke |
| EF mapping/migration/SQL transaction/rowversion/idempotency/outbox/spatial | Focused SQL Server IntegrationTests and affected endpoint smoke |
| Shared auth, serializer, middleware or cross-feature runtime behavior | Affected test-project suite(s), with focused architecture checks where relevant |
| Solution references, broad integration or release | Full solution when required by scope/repo gate; do not run focused then full merely out of habit |

For Postman-only changes, use a static collection/environment check: parse JSON, assert Collection v2.1, inspect request names/IDs, variables, URLs, headers, bodies and references. Do not call this an API runtime test. For API changes, include that check with the endpoint verification selected by the changed behavior.

Focused, affected-project and full-solution are alternative **breadths**, not a mandatory ladder. A focused selection may include multiple required projects (e.g. API + SQL + architecture); do not drop a risk to claim only one command. Choose approximately 1–3 high-value cases for a small change, but cover all changed invariants and mandatory gates; this is not a hard cap. Add regression tests for reproduced behavior bugs, not implementation-mirroring assertions or trivial documentation edits.

## Build fresh artifacts

Build the changed production project if the repository requires that gate. Before `dotnet test --no-build`, also ensure the selected **test project and its referenced dependencies** were built from the current source in the same configuration/framework. A production-only build does not establish that test output or copied dependencies are fresh.

Build each required test project once, then run its selected tests with matching options and `--no-build --nologo -v q`. If no separate production-only build is required, a test-project build may cover its production references; verify the graph first. Never build the whole solution merely to refresh one test project. On source edits, invalidate affected build/test evidence; do not reuse stale binaries.

## Interpret results honestly

- Check positive executed counts, failures and required skips. Zero tests, invalid filters, absent required projects and skipped required tests are failed gates.
- Inspect endpoint status, body, headers and durable effects; verify unauthorized/wrong-scope behavior when changed. Use secrets through local environment, never echo tokens.
- Use SQL Server/Testcontainers for SQL Server-specific claims. Mocks/SQLite cannot prove rowversion, spatial behavior, constraints or rollback semantics.
- Keep normal logs quiet; inspect a bounded diagnostic around the actual failure. No local coverage unless explicitly required. Do not re-run unchanged successful commands at handoff or commit.
- After two unsuccessful fixes for the same failure, reassess evidence and scope before another attempt. Continue only with a materially new supported diagnosis inside authorization; otherwise report the minimal blocker. Do not weaken assertions, skip required tests or expand implementation to obtain green output.
- Report exact command, configuration, count, environment, result and unverified items in task completion history. State which evidence was reused or invalidated. Never call a static skill review an executed backend test or set an API task `DONE` from docs checks.
