---
name: go-testing-conventions
description: timesheet-bot Go testing conventions - every test in services/timesheet-core/test/, black-box only (ADR-0009), table-driven tests, hand-written fakes for ports, httptest for adapters, integration build tag for Postgres, fixed clocks and fixed weeks. Preloaded into test-engineer.
user-invocable: false
---

# Testing conventions

Go paths (`internal/`, `cmd/`, `migrations/`, `test/`) are relative to `services/timesheet-core/`. Go tools run there, or from the repo root with `go -C services/timesheet-core`.

## Placement (ADR-0009)

- Every test lives in `services/timesheet-core/test/<kind>/<package path>/`, never beside the code. `<kind>` is `unit`, `integration`, `contract`, `architecture` or `e2e`. This deviates from the Go convention by owner choice: `docs/adr/0009-tests-in-separate-tree.md`.
- The package path is shortened: `<context>/<layer>` (`timesheet/domain`), `adapters/<adapter>` (`adapters/tempo`; `integration/postgres` for integration), `shared/` dropped (`kernel`, `httpx`), every other package by its path (`config`, `interfaces/cli`). Full mapping: `docs/architecture/testing.md`.
- Black-box only: `package <name>_test`, importing `timesheet-bot/internal/...`. No unexported identifiers, no `export_test.go`. If a test needs a seam, report it; the existing ones are `slack.Searcher`, `slack.NewCollectorWithSearcher` and `httpx.ErrNoRewind`.
- Fuzz seed corpora go in the test folder's `testdata/fuzz/<FuzzName>/`.
- Production code never imports `test/...`; `make arch` enforces it.

## Layers

| Layer | How it is tested | Example |
|---|---|---|
| kernel, domain | Pure table-driven unit tests, no fakes needed | `test/unit/timesheet/domain/timesheet_test.go` |
| application | Hand-written fakes for every port, plus `memory.Repository` | `test/unit/timesheet/application/handlers_test.go` |
| HTTP adapters | `httptest.NewServer`, asserting method, path, auth header and JSON body | `test/unit/adapters/tempo/client_test.go` |
| SDK adapters | A narrow exported interface over the SDK method plus a fake | `test/unit/adapters/slack/collector_test.go` (fake `slack.Searcher`, built with `NewCollectorWithSearcher`) |
| Postgres | `//go:build integration`, skipped unless `TEST_DATABASE_URL` is set, a unique user id per run, its own pool to read the outbox | `test/integration/postgres/repository_test.go` |

## Test types and owners

| Type | Owner | Command |
|---|---|---|
| Unit, application, adapter | test-engineer | `make test` |
| Integration (Postgres) | test-engineer | `make test-int` |
| Architecture fitness | technical-architect | `make arch` (`test/architecture`) |
| Contract (official API specs) | qa-engineer | `make test` (`test/contract/`, planned) |
| End to end (CLI over httptest) | qa-engineer | `test/e2e/`, planned, build tag `e2e` |
| Fuzz | qa-engineer | `make fuzz` |
| Race | qa-engineer | `make test-race` |
| Coverage gate (domain, application at least 85%) | qa-engineer | `make cover` (`-coverpkg=./internal/...,./cmd/...`) |
| Vulnerabilities | security-engineer | `make vuln` |

Acceptance criteria ids from the BA (`AC-nnn.m`, where nnn is the story number) go in the test name or a comment on the test, such as `// AC-012.1`.

## Rules

- Use fixed data: week `2026-W41` (Mon 2026-10-05 to Fri 2026-10-09), and a `fixedClock` returning 2026-10-09 16:00 UTC. Never use `time.Now()` in assertions.
- Use `errors.Is` against sentinel errors. Do not match error strings, except to check that a message names a variable and never contains its value.
- Fakes are small structs in the test file that record calls (`created []Worklog`) and can be told to fail (`failFor map[int64]bool`). No mocking libraries.
- Each test name states the behaviour: `TestSubmitPartialFailureThenRetry`, not `TestSubmit2`.
- Assert the outcome that matters (no duplicate Tempo writes, a start time kept on retry), not the implementation details.
- Use `t.Helper()` in helpers and `t.Setenv` for environment variables. Never commit real tokens. Use obviously fake values (`tok`, `me@example.com`).

## High-value edge cases for this codebase

- ISO weeks: 2026-W53 exists, and 2027-01-01 belongs to 2026-W53.
- A Slack timestamp at Sunday 23:00 UTC is Monday 06:00 in Asia/Ho_Chi_Minh, and must count for Monday.
- A daily cap at exactly the limit is accepted. One more 15m step is rejected.
- A partial Tempo failure followed by a retry: only the failed entries are re-sent, and the slot is unchanged.
- A stale aggregate version on save gives `ErrConcurrentModification`.
- Malformed external payloads: a missing `tempoWorklogId`, a non-numeric Jira `id`, an HTTP 400 with a body.

## Commands

```bash
go -C services/timesheet-core test ./test/unit/<ctx>/... -run TestName -v
make -C services/timesheet-core cover          # coverage of production code; needs -coverpkg, which the target sets
go -C services/timesheet-core test -coverpkg=./internal/<ctx>/... -cover ./test/unit/<ctx>/...   # one context
TEST_DATABASE_URL=postgres://... go -C services/timesheet-core test -tags=integration ./test/integration/postgres/...
```
