<!-- agent-notes: { ctx: "strict TDD implementation workflow", deps: [docs/adrs/0002-tdd-workflow.md], state: active, last: "tara@2026-02-12" } -->
Implement the following using strict TDD: $ARGUMENTS

Follow this cycle for each piece of behavior:

1. **Red** — Write a failing test that describes the desired behavior. Run the test suite to confirm it fails.
2. **Green** — Write the minimum code to make the test pass. Run the test suite to confirm it passes.
3. **Refactor** — Clean up the implementation while keeping all tests green. Run the test suite after refactoring.

Commit after each green-refactor cycle with a conventional commit message.

Do not write implementation code without a failing test first.

For items sized M or larger, Tara must be invoked as a standalone agent for the Red phase (not inlined by Sato). See `docs/adrs/0002-tdd-workflow.md`.

## Tracking Artifact

After all TDD cycles are complete and tests pass, produce `docs/tracking/YYYY-MM-DD-<topic>-implementation.md` summarizing what was built, test results (pass count, coverage if available), and any deviations from the plan. Use the standard tracking format from `docs/process/tracking-protocol.md`. Set **Prior Phase** to the most recent plan artifact for this topic (if any).
