---
name: dense-testing
description: >
  Build the test grid that makes AI-written code safe — traceability from spec UC ids to
  tests, density floors per changed symbol, and a hard ban on skipping or weakening tests to
  get green. Use when deciding how many tests a change needs, wiring acceptance criteria to
  test names, generating tests for agent-written code, or when a suite is green but trust in
  it is low. Use also when choosing between a unit, integration or end-to-end test, or deciding
  which suites run on every commit and which gate a production release.
---

# Dense Testing

Tests catch hallucinated implementations; the grid must cover observable behaviour densely.

**Test count matters:** many focused tests pinning observable behaviours catch scattered agent
defects. Optimise for coverage of behaviours, not for DRY test code.

Stack conventions and commands live elsewhere: this project's `.claude/rules/` files, its
`.claude/sdlc.md` verification table, and any stack pattern skills it happens to have. This skill
is the *how much* and the *what must never happen*.

## Traceability: UC id in the test name

Every acceptance criterion in `specs/<TICKET>/spec.md` carries a stable `UC-<n>` id. Every
test that proves one carries that id in its name or annotation:

```go
func TestGetBalance_UC1_ReturnsIntegerMinorUnits(t *testing.T) { … }
```
```ts
it('UC-3: lists entries newest first', async () => { … })
```
```python
def test_uc2_rejects_a_total_that_does_not_reconcile(): ...
```

This makes coverage of the *spec* computable with grep, independent of line-coverage tools:

```bash
grep -rho 'UC-[0-9]\+' <test-dir> | sort -u    # UCs with at least one test
```

`/sdlc:qa` and the `auto-qa` agent build the UC×test matrix from exactly this. A UC with no
matching test is a gap, whatever the line coverage says.

## Tiers: many unit, few integration, fewer e2e

A test's tier is set by what it touches at runtime, not by how much code it covers:

| Tier | Touches | Never touches |
|------|---------|---------------|
| `unit` | one process, in-memory fakes, a fake clock | sockets, a real database, a browser |
| `integration` | one machine: real schema, migrations, filesystem, containers the suite starts | third-party networks, a browser |
| `e2e` | a deployed test environment through the user's surface | — |

Write every test at the **lowest tier that can observe its result**, and prove each behaviour at
exactly one tier: a rule re-asserted through the browser is paid for on every CI run and fails
for reasons unrelated to the rule. In one change, new `unit` tests outnumber new `integration`
plus new `e2e` tests combined, or the QA report says why.

`test: e2e` rows cover only flows in `Critical journeys:` in `.claude/sdlc.md` (if `none`, at
most one per spec). One scenario per flow carries the UC id and drives the real UI against a
seeded database, asserting visible text and roles; attach a screenshot of the result to QA. Pin
bugs found by e2e with a unit test; retain the journey check.

Tier definitions, the CI stage each tier runs at, and the production release gate:
[`test-tiers.md`](references/test-tiers.md).

## Density floors

Minimums, not targets. Applied to the diff, not the whole repo:

| Changed thing | Minimum tests | Tier |
|---------------|---------------|------|
| Acceptance criterion (`UC-<n>`) | 1 test carrying its id | the tier its spec row names |
| Public function / method / exported symbol | 1 test for the happy path | `unit` |
| Error return or thrown exception | 1 case per distinct error | `unit` |
| Validation rule | 1 rejection case per rule, asserting no side effect | `unit` |
| HTTP endpoint | happy path + validation rejection + authorization denial + not-found | `unit`, with fakes behind the handler |
| Conditional branch | 1 case per side | `unit` |
| UI component with logic | 1 case per render state: populated, empty, loading, error, denied | `unit` |
| Persistence effect (query shape, transaction boundary, constraint) | 1 case per effect, against the real engine | `integration` |
| Migration | up→down→up on a scratch DB, plus 1 case per new constraint | `integration` |
| Multi-screen flow in the spec | 1 scenario per flow | `e2e` |
| Bug fix | 1 test that fails before the fix and passes after | lowest tier that can see the bug |

Table-driven or parameterised tests cheaply cover multiple branches, one case per branch.

## Assert on observable behaviour

Assert what a caller can see: status code, response body, database row, rendered text,
emitted event, log line. Not: that a mock was called, that an internal method ran, that a
private field holds a value. A test coupled to the implementation passes for a
reimplementation that is wrong, which is the exact failure this grid exists to catch.

Mock only what you cannot run: third-party APIs, clocks, randomness, payment providers — plus,
at the `unit` tier, any collaborator that would otherwise drag a socket or a database into the
test. Never mock your own database or service layer in an `integration` test: proving that real
effect is the only reason that tier exists.

## Non-negotiable

These are enforced by the `Stop` hook, which blocks a session that violates them:

1. **Never delete a test** to make a suite green.
2. **Never skip a test** — `t.Skip`, `.skip(`, `.only(`, `markTestSkipped`,
   `@pytest.mark.skip`, `@Ignore`, commenting a test out.
3. **Never weaken an assertion** — loosening an exact match to a substring, removing a field
   check, widening an expected range, replacing an assertion with a log.
4. **Never assert current buggy behaviour** just to get green.

When a test contradicts the spec, **stop and report the contradiction.** One of the two is
wrong and deciding which is a human call, not a cleanup task. In an unattended run, write the
contradiction to `specs/<TICKET>/BLOCKED.md` and exit non-zero.

A test that is genuinely obsolete — its feature was removed, or a refactor folded it into
another file — is **retired**, not deleted quietly: add `<path-or-glob> <reason>` to
`.claude/retired-tests` (committed; `#` comments) and both the `Stop` hook and the runner's
`verify` gate let that deletion through.
An entry without a reason does not count. Unattended runs (`AISDLC_HEADLESS=1`) honour only
entries already on the default branch, so a human commits them — typically alongside the spec.
Skipped, focused or weakened tests are never retirable.

A flaky test is a defect in the test or the fixture. Fix the race, the shared state, or the
clock dependency. Never add a retry wrapper to hide it.

## Reporting

After a run, report in the spec's terms, not the tool's:

```
UC coverage: 7/8 (UC-6 has no test)
Tests: 412 → 448 (+36)
Tiers (new tests): unit 31 / integration 4 / e2e 1
Suites: <each one you ran> ✓
Skipped: 0        # any non-zero value is a finding, not a footnote
```

Coverage percentage is a secondary signal. `UC` coverage and skip count are the primary ones.
