---
name: tdd
description: >
  Write new functions, classes, or modules using strict test-first TDD: define the
  contract, write one failing test, implement only enough code to pass, refactor, then
  repeat. Tests drive the design — the implementation follows the tests. Use this skill
  when starting from a spec or requirement, designing a new API through tests, or when
  the user says "write this test-first", "do TDD", "drive this with tests", or "/tdd".
  If the target code already exists, suggest /retrofit-tests instead.
argument-hint: <description or spec of what to implement>
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Skill: tdd

Write new code test-first using the Red → Green → Refactor cycle. Tests define and
constrain the implementation. The goal is to write only as much code as the tests demand.

---

## Phase 0: Check for existing implementation

Before anything else:

- If the target source file or function already exists, stop and recommend
  `/retrofit-tests` instead — this skill is for code that doesn't exist yet.
- If a test file already exists for the target, read it to understand naming conventions
  and existing behaviors. You will only ever append to it — never modify existing tests.

---

## Phase 1: Define the contract

Before writing any code, establish what the unit must do:

- What is the function or class signature?
- What does it return for valid inputs?
- What errors or exceptions should it raise for invalid inputs?
- What external dependencies does it need (filesystem, network, database, other modules)?

If the user provided a spec, extract these from it. If anything is unclear, ask one
focused question before proceeding.

Write the contract as a comment block at the top of the new test file:

```python
# Contract: parse_config(path: str) -> dict
# - Returns a dict of key-value pairs from a .ini-style config file
# - Raises FileNotFoundError if path does not exist
# - Raises ValueError if the file is malformed
# - Dependency: accepts a file-like object for easy mocking in tests
```

This documents intent and becomes the checklist for Phase 2.

---

## Phase 2: Red → Green → Refactor (one behavior at a time)

If the function has only 1–2 obvious behaviors with no ambiguous edge cases, the user
may reply **"fast"** to skip the per-behavior confirmation pauses and complete all
behaviors in one turn.

**Load the language reference first.** Identify the language from the target file
extension, then read `${CLAUDE_PLUGIN_ROOT}/references/<lang>.md` for test runner
commands, file naming conventions, AI-generated marker style, and mock patterns.

| Extension | Reference file |
|---|---|
| `.py` | `${CLAUDE_PLUGIN_ROOT}/references/python.md` |
| `.js`, `.mjs`, `.cjs` | `${CLAUDE_PLUGIN_ROOT}/references/javascript.md` |
| `.ts`, `.tsx` | `${CLAUDE_PLUGIN_ROOT}/references/typescript.md` |
| `.r`, `.R` | `${CLAUDE_PLUGIN_ROOT}/references/r.md` |
| `.c`, `.cpp`, `.cc`, `.h`, `.hpp` | `${CLAUDE_PLUGIN_ROOT}/references/c_cpp.md` |
| `.rs` | `${CLAUDE_PLUGIN_ROOT}/references/rust.md` |

Repeat this cycle for each behavior in the contract:

### Step 1 — Red: Write one failing test

Pick the next behavior from the contract. For functions with many input variants
(validation, type coercion, numeric ranges), consider a parametrized test table rather
than separate test functions — check the language reference for the framework's
parametrize syntax (e.g., `@pytest.mark.parametrize` in Python).

If C/C++, check the language reference (`${CLAUDE_PLUGIN_ROOT}/references/c_cpp.md`)
for the preferred test framework (Catch2 vs googletest) before writing the first test.

Write a single test for it using AAA structure:

```
# Arrange — set up inputs, mocks, and fixtures
# Act     — call the unit under test
# Assert  — verify the output or side effect
```

Mock all external dependencies. Do not let tests reach real filesystems, networks,
databases, or other modules. See the language reference for mock patterns.

Run the test. **Confirm it fails for the right reason** — a missing implementation,
not a syntax error or import failure. If it fails for the wrong reason, fix the test
setup before moving on.

> A test never seen failing cannot be trusted to catch future regressions. The red
> step is proof that the test is a real guard, not a tautology.

### Step 2 — Green: Write the minimum implementation

Write only enough code to make the failing test pass. Resist anticipating future tests.
If the simplest passing implementation is a hardcoded return value, write that — the
next test will force generalization.

Run all tests. Confirm:
- The new test passes
- All previously passing tests still pass

If a prior test breaks, fix the implementation (not the test) before continuing.

### Step 3 — Refactor

With all tests green, review the new test and the new source. Prefer inline setup for
single-use test data. Extract a fixture only when the same setup block appears in 3+
tests — shared fixtures create coupling that makes individual test failures harder to
diagnose.

**Test quality — FIRST check:**
- **F**ast — runs in milliseconds?
- **I**ndependent — shares no mutable state with other tests?
- **R**epeatable — same result every run, no randomness or network?
- **S**elf-validating — asserts a clear pass/fail?

**Clarity check:**
- Is the test name a clear statement of behavior (reads like a sentence)?
- Is the AAA structure obvious — could you identify the three sections at a glance?
- Is there duplication with another test that could be extracted?

Make any cleanup edits, then re-run all tests to confirm still green.

Once tests are green and the refactor is done, **offer a commit** for this behavior:
suggest a short message in the form `test: add [behavior name] — red/green/refactor`.
Keep it optional — the user may prefer to batch behaviors — but surface it as the
natural cadence. Each committed behavior is independently revertable if a later
behavior breaks something unexpected.

### Step 4 — Pause and report

Report:
- Which behavior was just implemented
- Total test count and how many are new
- What the next behavior in the contract is

Then ask: **"Ready to continue with the next behavior?"**

This pause is intentional. Each new behavior should start with only the contract and
the current state in context — not accumulated source snippets from prior iterations.
The user can reply "yes" or invoke `/tdd` again to start fresh with a clean context.

---

## Core constraints

- **Never modify or delete existing tests** — read any existing test file to understand
  its structure and conventions, then only append. Existing tests document prior
  behaviors that must not be disturbed.
- **Never write more than the test demands** — minimal implementation only.
- **Never write two tests without an implementation step between them.**
- **Always run tests** to confirm red, then green, then still green after refactor.
- **Mock all external dependencies** — unit tests must not reach real external systems.
- **One behavior per turn** — the pause is intentional.
- **Mark all new tests** with the AI-generated marker for the language (see reference).
- For algorithmic or data-transformation functions with many valid input shapes, consider
  property-based testing (Hypothesis for Python, proptest for Rust) as a complement to
  example tests — check the language reference for availability.
