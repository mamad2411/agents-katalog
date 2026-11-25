---
name: create-unit-tests
description: "Write unit tests for branch changes (or a scoped target) following best practices. Args: [<file-path | directory | module>]"
argument-hint: "[<file-path | directory | module>]"
---

<!-- Note: $ARGUMENTS is substituted by Claude commands only. In Copilot,
     the user must include their argument inline in the prompt; the skill
     body sees the literal text "$ARGUMENTS" unsubstituted. -->

## Arguments

`[<file-path | directory | module>]`

- Optional. Scopes test generation to a specific target; default is the branch diff vs `main`/`master`.
- **Examples**: `/create-unit-tests`, `/create-unit-tests src/payments/`

> Copilot CLI note: `$ARGUMENTS` does not substitute in skills; include the argument inline in your prompt.

# Create Unit Tests

Act as or delegate to the test automation role to write unit tests for the resolved scope.

## Scope

Default: diff between this branch and the base branch (`main`/`master`), narrowed to changed functions only. If provided, scope to: $ARGUMENTS (a file path, a directory, or a module name).

**Hard rule**: never touch files outside the resolved scope. If `$ARGUMENTS` is empty AND the branch diff is also empty, stop and report: "No changes detected; nothing to test. Pass an explicit target if you want to scope this run manually."

## How to write each test

Follow these practices for every test you generate:

1. **Structure (AAA)**: Arrange -> Act -> Assert, with a blank line between sections. One logical assertion per test.
2. **Naming**: descriptive: `should_<expected>_when_<condition>` or `given_<state>_when_<action>_then_<outcome>`. The name alone should explain the intent.
3. **FIRST**:
   - **F**ast: no real network, DB, filesystem, or sleep.
   - **I**ndependent: no ordering dependencies, no shared mutable state.
   - **R**epeatable: no `time.now`, no unseeded random, no env-dependent values.
   - **S**elf-validating: pass/fail via assertions, not `print` or manual inspection.
   - **T**imely: written alongside or before the production code, not as an afterthought.
4. **Mock only at boundaries**: external services, filesystem, network, clock, randomness. Do NOT mock the system under test (SUT) or its internal helpers.
5. **Test behavior, not implementation**: assert on public outputs, return values, and observable state; never on private method calls or internal data structures.
6. **Coverage per changed function**:
   - Happy path (the documented/obvious case)
   - At least one error path
   - Boundaries: 0, 1, max, negative
   - Nullish / empty inputs
   - Collections: empty, single element, ordering
   - Target: **>=80% branch coverage** on the scoped target. (Threshold chosen because below 80% typically leaves entire `catch`/error branches untested, the largest source of regressions in this repo's prior bugs. Lower it explicitly with a project-level coverage config if the codebase has a different baseline.)
7. **Match the repo's existing test style**: framework, file location, imports, fixture pattern, assertion library. Mirror what is already there; do not introduce a new style.

## Anti-patterns to avoid

- `sleep`, `setTimeout`, or any timing-based wait as test coordination
- Shared mutable state between tests (module-level vars, global fixtures without teardown)
- Near-duplicate tests: parameterise when two tests differ only by input
- Testing framework / stdlib behavior (trust the platform)
- Reaching into private implementation: if you have to, the abstraction is the problem; flag it, do not test around it
- Flakiness treated as a "retry the test" problem: flakiness is a bug
- **Mutation sanity check**: for each test, ask "if the production code it covers were broken, would this test fail?" If not, the assertion is wrong.

## Scope safety rules

These override everything else in this command:

- **Never** create or modify tests outside the resolved scope.
- **Never** refactor production code to add test seams. If the SUT is hard to test, add it to the **Blocked** section and stop; do not touch production code.
- **Never** install new dependencies, change test framework config, or modify CI config without stopping to ask first.
- **Only** write to the project's existing test directory convention: detect it (`tests/`, `__tests__/`, `*.test.ts`, `*_test.py`, `spec/`, etc.). Do not invent a new location.

## Output format

For each test file created or modified:

- **Path** (relative to repo root)
- **Functions covered**: list of target functions/methods
- **Tests added**: count and one-line rationale

**Blocked** (only if non-empty): anything that could not be tested safely: SUT needs refactor, missing fixture, ambiguous behavior, scope-safety tripwire. One line per item with reason.

### Verdict

- Functions targeted: N
- Tests written: N
- Estimated branch coverage on scoped target: %
- Blocked items: N

### Next steps

End with a one-line pointer:

> Run `/check-tests <same scope>` to verify coverage and spot any remaining gaps.

## Rules

- Match the project's existing test framework, file layout, assertion library, and naming exactly; do not introduce a new style.
- When in doubt, stop and ask rather than refactor production code or widen scope.
- Report only what you did. No trailing summary, no "next steps" beyond the one-line pointer above, no advice the user did not ask for.
