---
name: audit-test-suite
description: >-
  Load this skill to find out whether a passing suite would catch a defect: assertion quality,
  mutation testing, flaky tests, tests that mirror the code. Trigger on "are these tests any good",
  "mutation testing", "flaky test", "tests pass but the bug shipped", or after generating tests.
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Requires the target project's own test runner already working (`pytest` via `uv run`, or
  `vitest` via `bun`), since every check runs the suite. Mutation testing additionally needs a
  mutation tool as a dev dependency (`mutmut` for Python, `@stryker-mutator/core` for JS/TS) plus
  network access; without one, skip that check rather than assuming it is present.
license: Apache-2.0
---

# Audit a Test Suite

Green means the tests ran, not that they check anything. A suite generated in bulk — by a person in
a hurry or by a model — reliably contains tests that pass on broken code. This skill finds them.

The task is done when checks 1 and 2 have run, every later check has run or is named as unrun with
its command, and each finding in the report quotes the code it is about.

Run the checks in order: each is cheaper than the one after it, and the cheap ones find most of it.

## What waits for a request

Checks 1 and 2 are fast and scoped, so they apply without being asked. The rest are slow runs and
wait for a request: the mutation run (check 3), the repeated and parallel passes (check 4), the
durations run (check 5), and the coverage run (check 6). When one of those would help and was not
requested, name the command and what it would reveal, and state what stays unverified.

## Procedure

### 1. Assertion audit (seconds, no tooling)

Grep the suite for the four shapes that pass on almost any bug:

Tests with no assertion at all (Python — exact, via the AST rather than a regex):

```bash
python - <<'PY'
import ast, pathlib

def checks(fn):
    for n in ast.walk(fn):
        if isinstance(n, ast.Assert):
            return True
        if isinstance(n, ast.Call):
            f = n.func
            name = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "")
            if name.startswith(("assert", "expect")) or name in ("raises", "warns"):
                return True
    return False

for p in pathlib.Path("tests").rglob("test_*.py"):
    for n in ast.walk(ast.parse(p.read_text(encoding="utf-8"))):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith("test_"):
            if not checks(n):
                print(f"{p}:{n.lineno} {n.name}")
PY
```

Match on the node shape, not on `ast.dump()` text — a dump contains the function's own name, so a
test called `test_assertion_shape` looks like it asserts when it does not.

Assertions that are true for almost any value:

```bash
rg -tpy 'assert .* is not None$|assert .*len\(.*\) *>=? *0|assert True'
rg -tts -tjs 'toBeDefined\(\)|toBeTruthy\(\)|not\.toBeNull\(\)|toHaveBeenCalled\(\)$'
```

| Shape                                                      | Why it is worthless                | Fix                                  |
| ---------------------------------------------------------- | ---------------------------------- | ------------------------------------ |
| No `assert` in the test body                               | Only checks that nothing raised    | Assert the value                     |
| `assert x is not None` / `toBeDefined()` alone             | True for every wrong value too     | Assert the actual value              |
| `toHaveBeenCalled()` alone                                 | Passes on wrong arguments          | Assert the arguments                 |
| `assert len(result) > 0`                                   | Passes on wrong contents           | Assert the contents                  |
| Test asserts a value it computed with the code's own logic | Agrees with the code however wrong | Hard-code the literal expected value |

That last one is the signature defect of generated tests, and grep will not find it — read the
assertions in any file you did not write by hand.

For each suspect test, try to write its value line: `protects: <behavior>; fails_when: <the
defect it catches>; why_new: <what no other test covers>`. A test with no nameable `fails_when` is
worthless, and one whose `why_new` names another test is a duplicate. List both as deletion
candidates in the report.

### 2. Delete-the-code check (minutes, no tooling)

Pick the three most important behaviors. For each, break the source deliberately — invert a
comparison, return a constant, delete a line — and re-run.

**A test suite that stays green while the code is broken has told you exactly what it is worth.**

Do this by hand before reaching for mutation tooling; it takes two minutes and usually finds
something.

### 3. Mutation testing — on the diff only

The automated form of check 2: mutate the source, re-run the tests, report which mutations survived.
A surviving mutant is a change to production code that no test noticed.

```bash
# Python — changed files only
mutmut run --paths-to-mutate "$(git diff --name-only main...HEAD -- '*.py' | tr '\n' ',')"
mutmut results

# TypeScript
bunx stryker run --mutate "$(git diff --name-only main...HEAD -- '*.ts' | tr '\n' ',')"
```

**Always scope it to the diff.** Whole-repo mutation runs take hours and produce a report nobody
reads; that is why mutation testing gets adopted and abandoned. Diff-scoped, it finishes in minutes
and every finding is about code you just wrote.

Reading the output: fix surviving mutants in code you care about, and ignore survivors in logging,
`__repr__`, and defensive branches that cannot be reached. The number is not a target — the list of
survivors is the deliverable.

If the tool is not installed, do not install it unprompted: report the one-line command
(`uv add --dev mutmut`, `bun add -d @stryker-mutator/core`) and continue with the other checks.
Installing edits the lockfile, which an audit has no mandate to change.

Cap the run, for example `timeout 900 mutmut run ...`. Run it after checks 1 and 2 so a timeout
still leaves the cheap findings intact, and if it does not finish, report partial results and say
the run was truncated.

For a large or slow suite, delegate the whole audit to a background subagent with this skill loaded
and tell it to use report-only mode (below) — the run is long and high-output, which is exactly what
a background subagent is for.

### 4. Flakiness and order dependence

```bash
pytest -p randomly --count=3          # random order + seed, three passes
pytest -n auto                        # parallel — shared state surfaces here
pytest tests/unit/test_one.py         # each file alone
vitest run --sequence.shuffle
```

Any test that passes alone and fails in a suite (or vice versa) is sharing state: module-level
globals, a database row nobody rolled back, a patched clock, a cached singleton, `Date.now()`,
an unseeded RNG. Fix the sharing — never fix it by pinning the order or adding a sleep.

When the victim is known but the polluter is not, bisect for it. Run the victim after the first
half of the tests that precede it, then after whichever half reproduces the failure, until one
test is left. For a test that leaves stray files or rows rather than a failure, run each test
alone and check what exists afterwards (`git status --porcelain`, a row count) instead.

```bash
pytest tests/a.py tests/b.py tests/victim.py::test_x -p no:randomly   # fails? polluter is in a or b
```

A flaky test is worse than no test: it trains everyone to re-run until green, which is how a real
failure gets ignored.

### 5. Level and speed

```bash
pytest --durations=10
```

A "unit" test taking hundreds of milliseconds is doing I/O — it is an integration test in the wrong
directory, and it is slowing the loop that is supposed to be fast. Either mock the boundary or move
the file.

Also check the shape of the pyramid: if E2E tests outnumber unit tests, failures will be slow and
will not localize.

### 6. Coverage — used correctly

```bash
pytest --cov=app --cov-branch --cov-report=term-missing     # branch, not line
vitest run --coverage                                       # v8/istanbul report branches by default
```

**Always pass `--cov-branch`.** The default is line coverage, which counts an `if` with no `else` as
fully covered when only the true side ever ran — so the report is green exactly where the untested
half lives. Branch coverage is the cheapest upgrade available in this list.

Use it to find **files and branches at zero**, which are genuine blind spots. Do not use it as a
score to raise: coverage rises fastest by executing code without asserting on it, so a chased target
actively rewards worthless tests. Mutation survivors (check 3) are the metric with teeth.

Stronger structural criteria exist — condition coverage, MC/DC, def-use path coverage — and they are
not worth reaching for here: they cost far more to satisfy than diff-scoped mutation testing and
find less. Use them only under an external mandate (DO-178C, IEC 61508 and similar).

## Rules

- **Never delete or skip a failing test to get the suite green.** A red test is information; deleting
  it destroys the information and keeps the bug. If a test is genuinely wrong, fix its assertion and
  say why in the commit.
- **Never weaken an assertion to make it pass.** Widening `== 42` to `is not None` converts a real
  failure into a permanent blind spot.
- **Never mark a test as expected-to-fail (`xfail` / `.skip`) without an issue reference and a
  reason.** Unexplained skips accumulate until nobody knows what the suite covers.

## Output

Report worst-first, each finding with file and line, and separate what you fixed from what needs a
decision. **Quote or suppress:** every finding quotes the code it is about, as `path:line` plus the
line itself. A finding you cannot anchor to quoted code goes below the list as unverified, never in
it.

```
CRITICAL  tests/unit/test_billing.py:41  no assertion — only checks no exception raised
CRITICAL  tests/unit/test_pricing.py:88  expectation computed with the code's own formula
HIGH      src/discount.py               3 surviving mutants (boundary `>=` → `>` unnoticed)
MEDIUM    tests/integration/test_orders.py  fails under --random-order (shared session fixture)
LOW       tests/unit/test_parse.py:12   1.4s in tests/unit — real filesystem I/O
```

Save the report to `.agents_workspace/test-audits/<YYYY-MM-DD>.md`, so the findings that need a
decision outlive the session, and name the path in the reply. A subagent in report-only mode
returns the report instead, and its caller saves it.

### Report-only mode

Use it when the audit is delegated to a subagent, or the user asks for findings without fixes. A
subagent cannot ask the parent anything, so the report has to stand alone.

- Skip check 2 (it breaks source on purpose), never edit any file, and never install a package or
  change a lockfile or CI config.
- Keep the list to findings that let a suite pass on broken code or let a real failure go
  unnoticed, ranked worst-first, because a long tail buries the few fixes that matter.
- After the list, add: the commands run and their verdicts, including checks skipped and why (tool
  missing, timed out, not run); the zero-coverage files the diff touches; the 2–3 fixes worth making
  first, as concrete suggestions; and any bug found in source, reported and never fixed.

## Stop conditions

- The suite is already failing → report that and stop. An audit of a red suite is meaningless.
