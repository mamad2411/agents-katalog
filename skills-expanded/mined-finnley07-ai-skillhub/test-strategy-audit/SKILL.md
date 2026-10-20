---
name: test-strategy-audit
description: Audits a project's overall test strategy, infrastructure, and process from a tester/QA perspective — test pyramid balance (unit vs. integration vs. e2e ratio and execution time), real coverage numbers per module from the ecosystem's actual coverage tool (jest --coverage, pytest-cov, dotnet test /p:CollectCoverage, go test -cover, etc.) cross-referenced against high-change-frequency files, test quality (assertion-free tests, over-mocked tests, unreviewed snapshots, long-skipped/disabled tests via git blame), flaky-test evidence (CI retry configuration, sleep/timeout-based waits, ordering dependencies), test data & environment management (fixtures/factories vs. hardcoded duplication, isolated test DB vs. shared/prod-adjacent state, real vs. mocked external calls), existence of contract/load/performance/accessibility/security test automation, whether CI actually gates merges on test failure and coverage thresholds or just runs tests informationally (continue-on-error, allowed-to-fail, excluded required-checks), test maintainability (duplication, unclear names, implementation-coupled tests), and whether any written test strategy/plan exists at all — then reports the results as one table (check, area, status, evidence, recommendation). This is explicitly project-wide and process-level, not a diff-level check of whether one specific change has tests (that's code-review's C7/C22-C25 lane). Use this whenever the user asks for a "test strategy audit", "testing strategy review", "QA audit", "test infrastructure review", "teststrategie prüfen", "testabdeckung insgesamt", "teststrategie audit", "qa-audit", "how good is our testing", "is our test suite any good", "test pyramid check", "flaky test audit", "test coverage across the project", "gesamte testabdeckung", "test maturity assessment", "testreife prüfen", or asks about any specific item this covers (test pyramid, flaky tests, test data management, CI test gating, contract tests, missing test types, disabled/skipped tests, over-mocking) — even if they only name one or two of these and not the full skill name.
---

# Test Strategy Audit

A structured, evidence-based audit of a project's overall testing strategy, infrastructure, and
process — the tester/QA view of "is this project's testing actually working," not a review of
whether one specific diff came with tests. It investigates the test suite, coverage tooling, CI
configuration, and git history, then reports one table the user can act on.

**This skill is not `code-review`.** `code-review`'s test-coverage checks (C7, C22–C25) ask
whether *this specific change* has adequate tests. This skill asks whether the *project as a
whole* has a coherent, effective testing strategy — pyramid balance, coverage trends, flakiness,
environment management, and CI enforcement. If the user wants both, run them separately; don't
try to answer diff-level test-coverage questions here, point to `code-review` instead.

## Ground rules

- **Evidence or it didn't happen.** Every row needs a concrete pointer — a `file:line`, actual
  coverage-tool output with real percentages, the actual CI YAML/config snippet that does or
  doesn't gate on tests, or a `git log`/`git blame` result. Never write "testing looks adequate" or
  "coverage seems reasonable" — either you ran the tool and have the number, or you don't have a
  finding yet.
- **A coverage percentage alone proves nothing about test quality.** 90% line coverage from tests
  that only call a function and check it didn't throw is worse than it looks — a ✅ on any
  coverage-adjacent check needs evidence the tests actually assert meaningful behavior (real
  expected values, real state changes, real error conditions), not just that execution reached the
  line. Say this explicitly when a high coverage number and low-quality tests coexist — that's a
  ❌ or ⚠️ combination, not a ✅.
- **Don't invent scope you can't check, and don't silently drop scope either.** No service-oriented
  architecture → contract tests is `➖ N/A`, one line why. No load-test tooling anywhere → mark it,
  don't skip the row. Every check in this skill gets a row in the output.
- **Existence, not depth, for the adjacent specialties.** Load/performance tests, accessibility
  test automation, and security test automation each get checked for *whether they exist and run*
  here — the actual depth/quality of what they check is `performance-audit`'s, `accessibility-
  check`'s, and `cybersecurity-check`'s job respectively. Don't re-derive their full checklists;
  one line on presence/absence is the correct scope for this skill.
- **Be genuinely thorough.** A project with no visible test strategy doc, an inverted pyramid, and
  a coverage tool nobody runs is a common real combination, not a rare edge case — don't stop
  after the first few checks because most of the table is turning red; that pattern itself is the
  finding worth fully documenting.

## Workflow

1. **Identify the test frameworks and organization.** Find what runs tests (Jest/Vitest/Mocha,
   pytest, xUnit/NUnit/MSTest, JUnit, go test, RSpec, Playwright/Cypress/Selenium, etc.) from
   `package.json`/`*.csproj`/`pyproject.toml`/`go.mod`/build files, and how tests are organized —
   dedicated `unit/`, `integration/`, `e2e/` folders or tags/categories, or everything flat in one
   place next to source. This determines whether pyramid-balance (T1) can even be measured
   structurally or has to be inferred from what each test actually touches (a DB, a network call, a
   browser).
2. **Run the actual coverage tool if one exists** rather than estimating from file structure:
   `jest --coverage`, `pytest --cov`, `dotnet test /p:CollectCoverage=true`, `go test -cover ./...`,
   `nyc`/`c8` for other JS runners, `bundle exec rspec` with SimpleCov, etc. If no coverage tool is
   configured at all, that absence is itself a finding (T2), not a reason to skip the check.
3. **Inspect the actual CI configuration** (`.github/workflows/*.yml`, `azure-pipelines.yml`,
   `.gitlab-ci.yml`, `Jenkinsfile`, etc.) to see what's actually gating merges — does the test job's
   failure block the pipeline/merge, or is it run with `continue-on-error`/allowed-to-fail/excluded
   from required status checks (T7)? Don't infer enforcement from the job merely existing.
4. **Cross-reference git history** where a check calls for it: `git log --format='' --name-only |
   sort | uniq -c | sort -rn` (or equivalent) for change-frequency-vs-coverage (T2), `git blame` on
   skip/disable annotations for how long they've been dormant (T3), `git log -p` on flaky-looking
   CI retry config for when/why it was added (T4).
5. **Work through the checklist below**, grouped by theme, every check gets a row marked
   ✅/❌/⚠️/➖. Sample actual test files — don't assume quality from file count or naming alone.
6. **Report as one table**, most severe findings first within each area, followed by the
   prioritized punch list and needs-review list.

## Test pyramid balance

**T1 — Pyramid shape and execution time per layer.** Count tests per layer (from folder/tag
structure, or by inspecting what each test actually exercises if there's no structural separation:
does it hit a real DB/HTTP client/browser, or is everything in-process). Report actual counts and,
if the runner reports it, actual execution time per layer (`jest --listTests` counts,
`pytest --collect-only -q` counts, a CI log's reported per-job duration). An inverted pyramid —
few or no fast unit tests, most coverage coming from slow, broad e2e/integration tests — is a real
architectural finding: it means feedback is slow and failures are hard to localize, not just "more
tests would be nice." State the actual ratio found (e.g. "14 unit / 6 integration / 41 e2e") rather
than a vague "mostly e2e."

## Coverage

**T2 — Real coverage numbers per module, cross-referenced against change frequency.** Run the
ecosystem's coverage tool (see Workflow step 2) and report actual per-module/per-file percentages,
not just the aggregate. Flag modules at critically low or 0% coverage explicitly. Then
cross-reference against git churn: `git log --since="6 months ago" --format='' --name-only | sort |
uniq -c | sort -rn | head -20` (adjust window/path as appropriate) to find files that change often
— a proxy for business-critical/actively-evolving code — and check their coverage specifically. A
frequently-changed file sitting at or near 0% coverage is a materially worse finding than a stable,
rarely-touched file with the same low number, and should be reported as such, not folded into one
generic "low coverage" line. No coverage tool configured anywhere in the project → this whole check
is `❌`, not `➖ N/A` — a project having no way to even measure coverage is itself the finding.

## Test quality vs. quantity

**T3 — Assertion-free, over-mocked, and disabled tests.** Sample test files across the layers
found in T1 and look for: tests whose body only calls the function under test and asserts it
didn't throw (no assertion on a return value, state change, or call arguments); tests so heavily
mocked that no real production logic executes between the mocked boundaries (every collaborator
stubbed, leaving only glue code under test); snapshot tests where the snapshot file's diff history
shows repeated re-approvals without any accompanying logic change (a sign snapshots are rubber-
stamped, not reviewed). Separately, grep for skip/disable markers — `.skip`, `xit`, `xdescribe`,
`@Disabled`, `[Ignore]`, `@pytest.mark.skip`, `t.Skip(`, `@unittest.skip` — and for each one found,
`git blame` the line to report how long it's been disabled and, if the commit message/history
says why, what the stated reason was. A test skipped for months with no tracked follow-up is a
worse finding than one skipped yesterday with a linked ticket.

## Flaky tests

**T4 — Evidence of flakiness and how it's being handled.** Check CI/test-runner config for retry
settings (`retries:` in a Playwright/Cypress/Jest config, `[Retry]` attributes, a CI step that
re-runs failed tests automatically, `flaky: true` annotations) — the presence of a retry mechanism
is itself evidence that flakiness exists and is being papered over rather than fixed; report it as
a finding, not a mitigation. If the CI platform exposes test-run history (a dashboard, a `gh run
list` history of the same job flipping pass/fail on unchanged code), sample it. Separately, grep
test code for real-time/sleep-based waits that are a common root cause: `Thread.sleep(`,
`time.sleep(`, a bare `setTimeout`/`page.waitForTimeout(` used to "wait for" something instead of
polling/waiting on an actual condition or event, `Task.Delay(` outside of intentional
throttle-testing. Also check for tests that depend on execution order (shared mutable fixtures/
global state set up by one test and consumed by another, tests that fail only when run in isolation
or only when run as a full suite) — a common non-determinism source separate from timing.

## Test data & environment management

**T5 — Fixtures/factories vs. ad hoc duplicated data.** Check whether test data is built through a
shared fixture/factory/builder pattern (e.g. `factory_boy`, a `TestDataBuilder` class, shared
`beforeEach` fixtures) or whether the same hardcoded literal test objects are duplicated across
many test files — duplication here means a schema change requires updating dozens of files instead
of one, and is worth flagging even though it's "just test code."

**T6 — Test environment isolation.** Confirm tests run against a dedicated, isolated test
database/environment (a container spun up per run, an in-memory DB, a clearly-separated test
schema/project) rather than a shared database also used by other environments, or worse, anything
pointed at production-adjacent infrastructure. Check the actual connection string/config used when
tests run, not just its variable name. Separately, check that unit tests mock/stub external
dependencies (third-party APIs, payment providers, email/SMS senders) rather than making real
network calls during a normal test run — grep for the actual HTTP client/SDK usage inside unit
test setup and confirm it's backed by a mock/fake/recorded-fixture layer (e.g. `nock`, `responses`,
`WireMock`, `httptest`) rather than reaching the real network, which would make the test suite slow,
flaky, and dependent on a third party's availability.

## Test types beyond functional

**T7 — Contract tests between services.** If the project is service-oriented (multiple
independently-deployable services/APIs communicating with each other): is there any contract
testing (e.g. Pact, a shared OpenAPI-schema-validation step) verifying producer/consumer
compatibility, or does compatibility rely purely on manual coordination? Single-service/monolith
project → `➖ N/A`, state that explicitly.

**T8 — Load/performance test suite (existence only).** Does any load/performance test suite exist
at all (k6, Gatling, JMeter, Locust, a simple scripted load test), and is it run anywhere (locally
only, or in CI/scheduled)? Full evaluation of its quality/coverage is `performance-audit`'s job —
this check only confirms presence or absence.

**T9 — Accessibility test automation (existence only).** Is there any automated accessibility
testing (axe-core, `jest-axe`, Lighthouse CI accessibility assertions, Pa11y) wired into the test
suite or CI? Full WCAG conformance depth is `accessibility-check`'s job — this check only confirms
presence or absence.

**T10 — Security-focused test automation (existence only).** Is there any SAST/DAST or security-
focused test automation in CI (a SAST scanner step, dependency-vulnerability scanning gating the
build, a DAST scan against a staging deploy)? Full depth is `cybersecurity-check`'s job — this
check only confirms presence or absence.

## CI gating

**T11 — Test failures actually block merge.** Open the CI config and confirm the test job's
failure genuinely fails the pipeline and is included in the repository's required-status-checks
list for merge — not run with `continue-on-error: true`, an allowed-to-fail flag, a non-blocking
"informational" stage, or a required-checks list that quietly excludes the test job by name. Quote
the actual config lines as evidence either way.

**T12 — Coverage threshold enforcement.** Beyond running the coverage tool (T2), is a minimum
coverage percentage actually gated in CI (a coverage-check step that fails the build below a
threshold, a code-review-tool coverage gate) or is the number produced but never enforced, meaning
it can silently regress over time with nothing stopping it? Report the configured threshold if one
exists, and whether it's enforced project-wide, per-module, or only on the diff (patch coverage).

## Test maintainability

**T13 — Test code duplication.** Near-identical setup/assertion blocks repeated across many test
files that should be extracted into a shared helper/fixture — same standard as production-code
duplication: flag genuinely repeated (three-plus occurrences), not merely similar, blocks.

**T14 — Unclear test names.** Test names that don't describe the scenario and expected outcome
(`test1`, `testFoo`, `should_work`) versus ones that do (`returns_404_when_user_not_found`) — cite
actual test names found, not a generic complaint.

**T15 — Over-coupling to implementation details.** Tests that assert on internal
implementation/private state or verify a specific sequence of internal mock calls rather than
observable behavior, such that a harmless internal refactor (renaming a private method, reordering
independent internal steps) breaks the test with no behavior change. Cite the specific test and
what internal detail it's coupled to.

## Documentation of test strategy

**T16 — Written test strategy exists.** Look for any document (a `TESTING.md`, a section in
`CONTRIBUTING.md`/`README.md`, a wiki page, an ADR) describing what's tested where and why — which
layers get unit vs. integration vs. e2e coverage, what the coverage expectations are, how flaky
tests get triaged. Absence means the current test layout is purely incidental/historical rather
than a deliberate strategy — report this as a finding in its own right, distinct from any single
gap above, since it explains *why* gaps like an inverted pyramid or unenforced coverage tend to
accumulate unchecked.

## Output format

Start with 2-3 sentences: what was audited (frameworks/tools identified, whether the coverage tool
could actually be run, whether CI config was reachable), what couldn't be checked (no CI test-run
history available, no access to a coverage dashboard, etc.), and the ground-rule caveat that a
coverage number alone doesn't prove test quality.

Then ALWAYS use this exact table — one row per check, none omitted:

| # | Check | Bereich/Area | Status | Befund/Evidence | Empfehlung/Recommendation |
|---|---|---|---|---|---|
| 1 | ... | Pyramid/Coverage/Quality/Flakiness/Test Data/Test Types/CI Gating/Maintainability/Strategy | ✅/❌/⚠️/➖ | actual numbers, file:line, or config snippet | only if not ✅ |

(Match the table's language to the conversation's language — the column names above are
illustrative, not fixed vocabulary. Keep evidence concrete: real coverage percentages, an actual
CI config excerpt, a `git blame` result, or "not found — checked X, Y, Z.")

Status legend:
- ✅ Pass — checked with actual tool output/config/git history and the concern is genuinely handled
- ❌ Fail — a concrete gap, imbalance, or unenforced control was found
- ⚠️ Needs human judgment — a genuine toss-up (is this pyramid ratio actually a problem for this
  project's risk profile, is this level of mocking appropriate here) where you've given your
  reasoning but a second opinion is warranted
- ➖ N/A — this check's surface doesn't exist in this project (state why in one clause, e.g. "single
  monolith, no inter-service contracts to test")

End with a **prioritized punch list**: every ❌, ordered by how much it undermines confidence in the
test suite as a safety net (unenforced CI gating and zero-coverage business-critical files first,
then flakiness being masked by retries, then quality/quantity gaps, then maintainability/style) —
each with the one-line fix. Follow it with a **needs-review list**: every ⚠️, since those need a
second set of eyes rather than a mechanical fix.
