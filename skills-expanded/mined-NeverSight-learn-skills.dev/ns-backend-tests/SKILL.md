---
name: ns-backend-tests
description: (NS) Create and maintain PHPUnit unit and integration tests in the backend package (bootstrap tests/ when missing). Mandatory Docker-only execution with phpunit --testdox --stop-on-failure --stop-on-error and 120s timeout. Use when writing or refactoring PHPUnit tests, implementing unit-test tasks, or scaffolding backend tests on greenfield Laravel/PHP projects — not when planning test task markdown (ns-spec-driven references/unit-test-task-generator.md). Read harness backend-tests rules when present.
license: Apache-2.0
metadata:
  author: nextstage-brasil
  version: "1.0"
depends:
  - ns-harness
---

# Create Backend Tests

Execution-phase PHPUnit implementation. Planning-phase: `ns-spec-driven/references/unit-test-task-generator.md`.

## Session boot

Load `.nextstage-harness/rules/backend-tests-rules.mdc` and `backend-rules.mdc` when present. See `references/backend-testing-architecture.md` for layout, run contract, and bootstrap summary.

## Phase 0 — Resolve or bootstrap backend test root

**Before any test class code**, locate the PHPUnit project or create minimal structure.

### 0.1 — Detect existing tests (brownfield)

Search the repo in this order:

1. `backend/phpunit.xml`
2. `phpunit.xml` at repo root
3. `tests/Unit/` or `tests/Feature/` under the directory that contains `composer.json` with PHPUnit

Record the directory containing `phpunit.xml` as **`{backend_root}`**. All paths below are relative to `{backend_root}`.

### 0.2 — Bootstrap when nothing exists (greenfield)

If backend application code exists (`app/`, `src/`, or equivalent) but no `phpunit.xml` and no `tests/`:

| Rule | Detail |
| ---- | ------ |
| Location | `backend/` when that package exists; else repo root |
| Tree | Per `references/backend-testing-architecture.md` — `phpunit.xml`, `tests/TestCase.php`, `tests/Unit/`, `tests/Feature/` |
| Dependencies | PHPUnit via existing `composer.json` — never add to frontend or unrelated packages |

Then set `{backend_root}` to that directory.

**Forbidden on greenfield:** assuming tests exist, running PHPUnit on the host, or scaffolding tests outside the backend package.

### 0.3 — Post-bootstrap documentation

When `docs/context/stack-confirmed.md` or `architecture-rules.md` exists, add or update the backend test row: `{backend_root}`, docker test container, and the PHPUnit run command from Phase 5.

Do not proceed to Phase 1 until `{backend_root}` is confirmed and `phpunit.xml` is readable.

## Phase 1 — Discovery (before feature code)

1. **Code under test** — read implementation files (Service, FormRequest, Controller, etc.)
2. **Existing tests** — read matching files under `tests/Unit/` and `tests/Feature/`; extend, do not duplicate
3. **Project patterns** — factories, `RefreshDatabase`, response envelope, multitenancy helpers from harness rules
4. **Task contract** — when implementing a unit-test planning task, follow its scenario checklist

## Phase 2 — Write tests

- Unit: mock dependencies — no real DB/queue/cache I/O
- Feature: HTTP tests with auth, 401/403, cross-tenant P0 when applicable
- Naming: `{Component}Test.php`, descriptive snake_case method names
- Match module paths: `tests/Unit/Modules/{Domain}/`, `tests/Feature/Modules/{Domain}/`

## Phase 3 — Run (mandatory contract)

See also `../../ns-harness/references/docker-and-testing.md`.

1. Run `docker ps` — confirm the documented **test** container (ask once if undocumented)
2. Execute **inside the test container** at `{backend_root}` workdir:

```bash
timeout 120 docker exec -w {workdir} {test_container} \
  vendor/bin/phpunit --testdox --stop-on-failure --stop-on-error {optional_filter}
```

3. **Timeout:** if the command is killed at 120s (e.g. exit 124), treat the run as **dead/hung** — abort, report blocker, do not silently retry
4. **Never** run `vendor/bin/phpunit` or `phpunit.sh` on the host

Filtered runs (single class or method) use the same flags and timeout.

## Phase 4 — Report

- Pass: list files added/changed
- Fail: first failing test name + assertion from `--testdox` output
- Hung/timeout: state 120s limit exceeded; invoke `ns-investigator` if root cause unclear

## References

| File | When |
| ---- | ---- |
| `references/backend-testing-architecture.md` | Layout, bootstrap, run contract |
| `../ns-spec-driven/references/unit-test-task-generator.md` | Task contract source |

## Related skills

- `ns-spec-driven` `references/unit-test-task-generator.md` — planning tasks
- `ns-investigator` — failing or hung test debugging
- `ns-coder` — ad-hoc fixes outside planned unit-test tasks
