# Skill: Test-Driven Development

## Trigger
Load this skill whenever:
- Writing a new function, hook, component, or module
- Fixing a bug (the bug must have a test that reproduces it before the fix)
- Refactoring existing code
- Adding a new API endpoint or store action

## Type
**Rigid** — The RED → GREEN → REFACTOR cycle is non-negotiable. Never write implementation code before a failing test exists.

## Instructions

### Phase 1 — RED (Write a failing test)
1. Identify the smallest possible unit of behavior to implement.
2. Write a test that describes the expected behavior. The test must:
   - Have a descriptive name (`it('returns zero when no transactions exist', ...)`)
   - Test one thing only
   - Currently fail (you have not written the implementation yet)
3. Run the test. Confirm it fails with the expected error, not an import error or syntax error.
4. Do not proceed to Phase 2 until the test fails for the right reason.

### Phase 2 — GREEN (Make the test pass with minimal code)
5. Write the simplest possible implementation that makes the test pass.
6. Do not add logic the test does not require. Resist the urge to generalize.
7. Run the test. Confirm it passes.
8. Do not proceed to Phase 3 if any other tests are broken.

### Phase 3 — REFACTOR (Clean up without changing behavior)
9. Improve the implementation: extract duplication, rename variables, simplify logic.
10. Run the full test suite after every change. All tests must stay green.
11. Do not add new behavior during refactor. If you think of something new, write a new test first (return to Phase 1).

### Repeating the cycle
12. For each additional behavior, return to Phase 1. One cycle per behavior unit.

## Verification
- A failing test exists before any implementation is written.
- The test name describes behavior, not implementation details.
- After GREEN, no other tests are broken.
- After REFACTOR, the test suite is fully green and the code is cleaner than before.
- At no point was implementation written without a corresponding test.
