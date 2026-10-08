---
name: code-coherence-review
description: Reviews code and plans for logic coherence, correctness, and structural integrity.
usedBy: [reviewer]
version: 0.2.0
lastUpdated: 2026-09-12
---

## Purpose

A correct function that violates a naming rule ships with a warning. A rule-compliant function with broken logic cannot ship. This skill checks what matters most: does the code make sense, survive real-world input, and respect the project's boundaries? Run it first — nothing else matters until the code is coherent.

## Procedure

1. **Initialize the progress file.** Create `.memory/reviews/review-coherence-<timestamp>.md`:

   ```markdown
   # Coherence Review Progress

   ## Status
   - Last updated: <timestamp>
   - Overall: In Progress

   ## Phases
   - [ ] 1. Logic coherence
   - [ ] 2. Dead code, obsolete artifacts, and comments
   - [ ] 3. Correctness
   - [ ] 4. Structural coherence
   - [ ] 5. Duplication detection

   ## Findings
   ```

2. **Logic coherence.** Read the work as a narrative. Trace the flow from entry point to exit. Check:
   - Does the algorithm solve what the task brief says it should?
   - Are there circular logic paths or infinite loops?
   - Do the data structures fit the problem, or is the code fighting its own model?
   - For plans: check for ambiguity (instructions that can be read two ways), logical gaps (steps that assume preconditions without establishing them), redundancy (duplicate steps), and contradictions.
   - For code and other non-plan artifacts: review against the task brief's acceptance criteria. Stress-test for blindspots, ambiguity, and false assumptions.

   Write any findings to the progress file under `## Findings` with the heading `### Logic coherence`. Mark phase 1 as `[x]`.

3. **Dead code, obsolete artifacts, and comments.** Scan every changed file for code that is no longer useful or reachable, and for comments that did not earn their place. For each file, check:
   - **Unused functions and methods** — functions or methods defined but never called anywhere in the codebase. Run `rg -n 'func <name>'` or `rg -n 'def <name>'` to find definitions, then verify with `rg '<name>\('` that they are actually invoked elsewhere. If a function has zero callers, it is dead.
   - **Unused variables and constants** — variables or constants assigned but never read. Trace each assignment to its usage sites. Variables declared and initialized but never referenced in any subsequent statement are dead.
   - **Unused imports** — import statements for modules, packages, or symbols that are never referenced in the file. Compare every import against actual usage in the file body.
   - **Unreachable code** — code after `return`, `break`, `continue`, `raise`, `exit`, or `panic` statements within the same block. Code in conditional branches that can never be true (e.g., `if false`, `if 1 == 0`, or branches contradicted by earlier guards).
   - **Commented-out code** — commented code of any length. Version control holds old code, not inline comments; no justification preserves a commented-out block. Flag for removal.
   - **Explanatory comments** — comments that restate, narrate, or explain what code does. The fix is a rename, an extraction, or a type — not the comment. Do not flag a comment that explains why under an external constraint no code can express (see the Comments section in `rules/code/general.md`), and do not flag a comment a domain rule or tool contract mandates (shell headers, suppression justifications) — those are structure, not confession.
   - **Deprecated or superseded logic** — code paths replaced by newer implementations but not removed. Check for conditional branches that always take one path because a feature flag is permanent, or old implementations kept "just in case" with no callers.

   For each finding, verify it is truly dead by searching the entire codebase for references. Do not flag something as dead if it is exported/public API, used via reflection, invoked dynamically, or called from test files.

   Write any findings to the progress file under `### Dead code and comments`. Mark phase 2 as `[x]`.

4. **Correctness.** The logic is sound — now verify it survives real-world input. Walk each changed file and check:
   - Error paths — every error is handled or explicitly logged. No silent swallows.
   - Boundary conditions — off-by-one, nil/null, empty collections, zero values.
   - Concurrency — shared state is protected. No data races, no unguarded async mutations.
   - N+1 queries — loops that trigger a database query per iteration instead of batching.
   - Resource leaks — unclosed connections, file handles, channels, or transactions in error paths.
   - Retry logic — missing backoff, missing idempotency keys, thundering-herd potential on failure recovery.
   - Time handling — timezone assumptions, clock skew sensitivity, missing UTC normalization.
   - Stale reads — reading state, deciding, then acting without verifying the state still holds.
   - Missing indexes — new query patterns that will table-scan at production data volumes.
   - Missing timeouts — external calls (HTTP clients, database queries, third-party APIs) without a timeout. One slow dependency without a deadline cascades into a full system hang.
   - Backward compatibility — does this change break existing consumers? Removed or renamed fields, changed response shapes, stricter validation, or altered behavior on existing endpoints break clients that depend on the previous contract.
   - Incomplete work markers — `TODO`, `FIXME`, `HACK`, `XXX`, empty function bodies, stub implementations returning hardcoded values. These are unfinished work, not code that can ship.
   - Test skip markers — `t.Skip()`, `pytest.mark.skip`, `.skip(`, `xit(`, `xdescribe(`, `xtest(`, or equivalent. Skipped tests hide regressions. If a test must be skipped, a comment must name the blocker and the condition that re-enables the test — a skipped test is a deliberate rule violation, earned under `rules/code/general.md` § Comments.

   Write any findings to the progress file under `### Correctness`. Mark phase 3 as `[x]`.

5. **Structural coherence.** Step back from individual lines. Read the `.context.md` files for affected directories (follows: `skills/context-maintenance/SKILL.md`) to understand layer boundaries and directory purpose. Check:
   - Does the change respect those boundaries?
   - Are there new dependencies that break the dependency direction? If the project documents its architecture in an architecture skill or a dedicated architecture file, read it and verify dependencies flow in the correct direction.
   - For plans: does any proposed change introduce a dependency that flows against the architecture's grain?

   Write any findings to the progress file under `### Structural coherence`. Mark phase 4 as `[x]`.

6. **Duplication detection.** Scan the changed code for logic, patterns, or methods that duplicate existing functionality in the codebase. For each changed file, check:
   - **Duplicated functions or methods** — functions that perform the same or nearly identical operations as existing functions. Compare the new function's logic, parameters, and return values against existing ones. Use `rg` to search for similar names or patterns. If two functions differ only in minor details, consolidate them.
   - **Duplicated logic blocks** — sequences of 5+ lines that appear in multiple places with identical or near-identical structure. Look for repeated patterns like:
     - Data transformation pipelines (filter → map → reduce)
     - Error handling and retry logic
     - Validation sequences
     - Database query patterns
     - HTTP request/response handling
     - Configuration parsing
   - **Copy-pasted constants or configuration** — magic numbers, strings, or configuration values that appear in multiple places instead of being defined once as a constant or configuration.
   - **Reinvented utilities** — new implementations of functionality that already exists in standard libraries, third-party packages, or project utilities. Before flagging, verify the existing utility covers the use case.

   For each suspected duplication:
   1. Use `rg -n '<pattern>'` to find all occurrences of similar logic across the codebase
   2. Compare the implementations line by line
   3. If the duplication is substantial (5+ lines) and the variations are minor, flag it as a Warning
   4. Suggest consolidation: extract to a shared function, use a parameterized approach, or point to the existing utility

   Do not flag duplication if:
   - The duplicated code is in test files and is under 20 lines (test duplication is often acceptable for clarity). If test duplication exceeds 20 lines and the tests are clearly parameterizable, flag it as a Warning.
   - The code is intentionally duplicated for performance reasons (verify with a comment earned under `rules/code/general.md` § Comments — a measured bottleneck is an external constraint)
   - The duplication spans different architectural layers and extracting it would create inappropriate dependencies

   Write any findings to the progress file under `### Duplication`. Mark phase 5 as `[x]` and set Overall to `Complete`.

7. **Classify findings.** For each finding in the progress file, verify the severity:
   - **Blocker** — logic incoherence, correctness bug, architectural violation, plan contradiction, dead code that is exported/public API (misleading), massive duplication (20+ lines) with no abstraction. Must be fixed.
   - **Warning** — minor structural concern, edge case worth considering, dead code (unused private functions/variables), unearned explanatory comments (fix is a restructure, not the comment), moderate duplication (5-19 lines). Should be addressed.
   - **Note** — observation or question. No action required.

   For plans, replace `<file>:<line>` with `<phase or section name>`. Each finding should already be under its phase heading. Update the format to include the check type:

   ```
   - <file>:<line> — <what is wrong and why it breaks>. (check: <logic | dead-code | comment | correctness | structural | duplication>)
   ```

   If review is interrupted, the progress file shows which phases were completed and what findings were recorded.

## Guardrails

- Never skip the logic coherence step to jump to correctness. A correct implementation of broken logic is still broken.
- Never flag style, naming, or convention issues. Those belong to the quality review skill.
- Test issues split at the proof seam. Proof belongs to this pass: skip markers, assertions on internals instead of behavior. Style belongs to quality review: naming, table-driven shape, setup placement.
- Never flag dead code without verifying it is truly unused across the entire codebase. Search for all references before reporting.
- Never flag duplication without comparing the implementations line by line. Superficial similarity is not duplication — verify the logic, not just the structure.
