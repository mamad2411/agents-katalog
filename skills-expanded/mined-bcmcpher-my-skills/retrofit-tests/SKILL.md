---
name: retrofit-tests
description: >
  Add comprehensive unit tests to an existing source file using a focused, iterative
  workflow: plan full coverage first using boundary value analysis, then implement one
  unit at a time — pausing between units to keep context lean. Use this skill when the
  user wants to add tests to existing code, improve test coverage, test a module already
  written, or says "write tests for X", "add test coverage", "test this function",
  "generate unit tests for this file", or "/retrofit-tests". If the code doesn't exist
  yet and tests should drive the design, suggest /tdd instead.
argument-hint: <source-file>
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Skill: retrofit-tests

Add well-structured unit tests to an existing source file. Plan coverage for the whole
file upfront, then implement one unit at a time — pausing between units to keep context
lean and attention sharp.

---

## Phase 1: Plan (first invocation for a file)

Check whether a TODO file already exists for this source file (see Naming below).
If one exists, skip directly to Phase 2.

### Step 1 — Detect language and load reference

Identify the language from the file extension and read the corresponding reference file
for framework-specific conventions (test runner, file naming, AI marker style, mocks):

| Extension | Reference file |
|---|---|
| `.py` | `${CLAUDE_PLUGIN_ROOT}/references/python.md` |
| `.js`, `.mjs`, `.cjs` | `${CLAUDE_PLUGIN_ROOT}/references/javascript.md` |
| `.ts`, `.tsx` | `${CLAUDE_PLUGIN_ROOT}/references/typescript.md` |
| `.r`, `.R` | `${CLAUDE_PLUGIN_ROOT}/references/r.md` |
| `.c`, `.cpp`, `.cc`, `.h`, `.hpp` | `${CLAUDE_PLUGIN_ROOT}/references/c_cpp.md` |
| `.rs` | `${CLAUDE_PLUGIN_ROOT}/references/rust.md` |

If the language isn't listed, apply generic TDD principles and use `# AI-Generated`
as the marker.

### Step 2 — Inventory testable units

Read the source file and list every testable unit. For each function or method, use
**boundary value analysis** to identify test cases. If a function is an orchestrator or
end-to-end pipeline (calls 3+ other functions, reads and writes files), note it in the
TODO as a candidate for an **integration test** rather than a unit test — unit mocking
of an orchestrator usually produces tests that are more brittle than useful.

- **Equivalence classes:** what inputs are valid vs. invalid? Group them.
- **Boundary values:** test at and around limits (0, 1, empty, single element,
  max value, min value)
- **Error states:** exceptions, invalid types, null/None inputs
- **External dependencies:** which units call out to filesystem, network, database,
  or other modules? These will need mocking.

### Step 3 — Write the TODO file

Create `<source-dir>/retrofit-tests-todo.md` with this format:

```markdown
# Test TODO: <source-file>
Language: <language>
Test file: <test-file-path>
Generated: <date>

## Units
- [ ] `function_name` — happy path; boundary: empty input; error: None raises TypeError
- [ ] `ClassName.method` — happy path; boundary: max value; mock: db.query
- [ ] `ClassName.__init__` — valid args; invalid args raise ValueError
```

### Step 4 — Offer plan review (optional)

Before starting Phase 2, offer: **"Would you like a subagent to review this test plan
as a staff engineer before we begin writing tests?"** A reviewer subagent checks for
coverage gaps, mocking strategy correctness, missing edge cases, and whether the
planned unit order respects dependencies.

If the user declines or doesn't respond, proceed immediately. The TODO file is already
a reviewable artifact — the review offer is most valuable for large source files with
complex dependency graphs.

### Step 5 — Begin

Tell the user "I've planned N units in `<todo-file>`. Starting unit 1 now..." then
proceed directly to Phase 2 without waiting.

---

## Phase 2: Execute (one unit per turn)

Read the TODO file. Find the first unchecked item (`- [ ]`). If all items are checked,
tell the user all units are covered and stop.

### Step 1 — Load minimal source context

Use Grep or a targeted Read (with line offset and limit) to load just the function or
class body for the current unit. Avoid re-reading the entire file.

### Step 2 — Identify dependencies and check the test file

Note any external dependencies in this unit (filesystem, network, database, other
modules). These must be mocked — do not let tests reach real external systems.
See the language reference for mock patterns.

If a test file already exists, read it briefly to understand the existing structure
and confirm you won't duplicate anything. **Never modify or delete existing tests.**

### Step 3 — Red: Write one failing test

Write a test that exercises a boundary condition or error state — something the
implementation must handle but that is easy to get wrong. Use AAA structure:

```
# Arrange — set up inputs, mocks, and fixtures
# Act     — call the unit under test
# Assert  — verify the output or side effect
```

Run it with the test runner. **Confirm it actually fails.**

> A test never seen failing cannot be trusted to catch future regressions. The red
> step is proof that the test is a real guard, not a tautology.

### Step 4 — Green: Write the passing tests

Write tests for the happy path, then the remaining boundary cases and error states
from the TODO item. Run all new tests and confirm they pass.

### Step 5 — Refactor: Clean up the new tests

With all new tests green, review them for quality:

**FIRST check:**
- **F**ast — runs in milliseconds?
- **I**ndependent — shares no mutable state with other tests?
- **R**epeatable — same result every run?
- **S**elf-validating — clear pass/fail assertion?

**Clarity check:**
- Are test names clear statements of behavior?
- Is the AAA structure obvious in each test?
- Any duplication that could be extracted to a fixture?

Make any cleanup edits, then re-run to confirm still green.

### Step 6 — Mark done and pause

Update the TODO: change `- [ ]` to `- [x]` for the completed unit.

Report:
- Which unit is done
- How many tests were written (pass/fail breakdown)
- What's next in the TODO

Then ask: **"Ready to continue with the next unit?"**

This pause is intentional. Starting the next unit in the same context carries over
source and test snippets no longer needed. The user can reply "yes/continue" or
invoke `/retrofit-tests` again to start fresh with only the TODO loaded.

---

## Naming conventions

**TODO file:** `<source-dir>/retrofit-tests-todo.md`
- `src/utils.py` → `src/retrofit-tests-todo.md`

**Test file:** Follow language conventions from the reference file.
- Python default: `tests/test_<module>.py` (or `test_<module>.py` alongside source)
- If a test file already exists, append to it. Never delete existing tests.

---

## Marking AI-generated tests

Mark every test you write so humans can quickly audit AI-generated coverage.
Each language has a preferred style — see the reference file. The generic fallback is
a `# AI-Generated` comment directly above the test function.

Never apply AI-generated markers to tests that already exist in the file.

---

## Core constraints

- **Never modify or delete existing tests** — only append.
- **Never change source code** to make tests pass. If a test fails due to a source bug,
  note it in a comment and mark the test as `xfail` (or language equivalent). Move on.
- **If a test reveals a bug in the source**, mark the test with a `# BUG: <description>`
  comment and add a TODO item. Never fix source bugs during retrofit — that is a
  separate task.
- **If a unit has no testable seam** (no parameters, direct I/O, global state, no
  dependency injection), document it in the TODO as "requires refactoring for
  testability" and skip — do not attempt to test it as-is.
- **Mock all external dependencies** — unit tests must not reach real external systems.
- **One unit per turn** — the pause between units is intentional.
- **Always run tests** to confirm red, then green, then still green after refactor.
- **Load only what you need** — targeted reads, not full-file loads during execution.
- After all TODO items are checked, suggest running the project's coverage tool
  (e.g., `pytest --cov=<module>`, `jest --coverage`) and report the resulting
  line/branch coverage.
