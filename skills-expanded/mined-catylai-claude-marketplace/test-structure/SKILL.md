---
name: test-structure
description: "Use when adding, running, restructuring or reviewing tests. Team conventions for mock placement, layout, tiers and markers, suite red flags, plus pytest and TypeScript/UI runner rules. Not for the done-gate (use zero-tolerance-testing)."
license: MIT
---

# Test structure

The conventions below are the ones this team holds to. Language detail lives in two references;
read the one that matches the suite you are touching:

- Python / pytest: [references/python.md](references/python.md) (per-worktree venv, markers,
  fixtures, commands)
- TypeScript / UI / end-to-end: [references/typescript.md](references/typescript.md) (runner per
  tier, query priority, end-to-end rules)

## Mock placement

Keep mocks, stubs and fakes in test directories (`tests/__mocks__/`, `__tests__/__mocks__/`,
`tests/fixtures/`). A double under `src/` ships in the production bundle and can be imported by
real code by accident.

The one exception is a double the public API deliberately offers consumers, such as an in-memory
adapter. Name it as a product (`InMemoryStore`, not `MockStore`) and document it.

Check for strays (adjust `src` to the repo's source root):

```bash
find src \( -name "*.mock.*" -o -name "*Mock*" -o -name "*Stub*" -o -name "*Fake*" -o -name "__mocks__" \)
grep -rlE "jest\.mock|vi\.mock|unittest\.mock|from pytest_mock" src/
```

## File layout

Pick one convention per repo and keep it.

- Unit tests: colocated (`src/utils/parse.ts` → `src/utils/parse.test.ts`) or mirrored under the
  test tree (`tests/unit/utils/test_parse.py`). Colocated tests are easiest to keep in sync.
- Integration and end-to-end: a separate tree (`tests/integration/`, `tests/e2e/`), because they do
  not map one-to-one onto source files.

## Tier boundaries

| Tier | Scope | External dependencies |
| --- | --- | --- |
| Unit | One function or class | All replaced; no network, database or filesystem |
| Integration | A module plus its real collaborators | Database or API real or containerized |
| End-to-end | The whole system | Nothing replaced |

A "unit test" that starts a database is an integration test; move it to that tier so the unit lane
stays fast and deterministic. Every test is selectable by tier (a directory plus a pytest marker or
a runner project), so CI and pre-push hooks can run one tier at a time.

## Mocking

Replace collaborators at a boundary you own: inject the dependency, or intercept at the network
layer. Assert on behaviour and outputs. A test that breaks on a behaviour-preserving refactor is
testing the implementation; a test that asserts only mock call counts is testing the mock.

## Red flags when reviewing a suite

- A skip (`it.skip`, `describe.skip`, `@pytest.mark.skip`, `xfail` without `strict=True`) with no
  linked issue. A skip is a hidden failure; see `zero-tolerance-testing` for the policy.
- `it.only` / `describe.only`: it silently narrows the whole run. Vitest rejects it when `CI` is
  set; for jest, enable the `jest/no-focused-tests` lint rule.
- A test that cannot fail: an empty body, an assertion inside a branch that is false in CI, a
  `try`/`except` around the assertion, a loop over an empty collection.
- A test that checks only that the call did not throw, with no assertion on the result.
- Many unrelated assertions under one vague name, so a failure does not say what broke.
- A fixture or test that supplies the value the code under test is supposed to compute.
- Test doubles under the source tree.

## Verify

Run the tier you touched and confirm it selects what you expect: the run reports a non-zero test
count, and a deliberately broken assertion turns it red before you restore it.

Without a checkout, apply the same rules to test code the user pastes, and say which checks
(stray-mock search, run counts) you could not perform.
