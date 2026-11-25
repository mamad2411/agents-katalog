---
name: code-simplification
description: >-
  Disciplined code simplification that reduces complexity without changing
  behavior. Combines quantitative complexity metrics (cyclomatic, cognitive),
  the Rule of 500, Chesterton's Fence, and proven refactoring patterns to
  produce code that is smaller, faster to read, and safer to modify.
---

# Code Simplification

## Overview

Complexity is the primary tax on software evolution. Every condition branch,
every mutable variable, every undocumented dependency increases the time
required to understand, test, and safely modify code. Over time, complexity
grows exponentially — each new feature adds not just its own logic but
interactions with every existing feature.

Simplification is the practice of reducing complexity while preserving
exact behavior. It is not rewriting, not "cleaning up", and certainly not
adding abstractions for their own sake. It is the surgical removal of
unnecessary complexity, validated by tests.

**Chesterton's Fence:** Before removing any code, understand why it exists.
If you cannot explain its purpose, you do not understand the system well
enough to know whether removing it is safe. Document the fence, then
remove it if justified.

**Rule of 500:** If a source file exceeds 500 lines, the reader's ability
to hold the entire module in working memory degrades sharply. Break it into
multiple files. The same rule applies at smaller granularities: functions
should fit on one screen (~40 lines), and a single class/component should
not exceed one file.

## When to Use

- A function has more than 10 branching paths (cyclomatic complexity >10)
- A file exceeds 500 lines and no single developer understands all of it
- A code review produces comments like "what does this do?" or "can we
  simplify this?"
- A bug fix requires tracing through 5+ layers of indirection
- Tests are hard to write because setup is too complex
- The same concept is implemented differently in multiple places
- A refactoring PR is rejected as "too risky" — because the code is too
  complex to change safely
- Onboarding a new team member and they struggle to understand a core module

## Process

### Step 1: Measure Complexity

Before simplifying, measure. Without data, simplification becomes
opinion-driven and risks removing necessary complexity.

**Metrics to gather:**

| Metric | Threshold | How to Measure |
|--------|-----------|----------------|
| Cyclomatic Complexity | <10 per function | `radon cc` (Python), `lizard` (multi), `eslint complexity` (JS) |
| Cognitive Complexity | <15 per function | SonarQube, CodeClimate |
| Lines Per Function | <40 | `cloc`, `wc -l`, IDE outline |
| Lines Per File | <500 | `cloc`, `wc -l` |
| Nesting Depth | <4 levels | `grep -n` for indentation, lint rules |
| Parameter Count | <3 | Manual count or lint rule |
| Dependency Fan-In/Fan-Out | <10 | `depcruise`, `madge` |
| Test Coverage of Complex Paths | >80% | `nyc`, `coverage.py`, `gcov` |

**Exit criteria:** A complexity report showing the current state for each
metric. Identify the top 3 hot spots (highest complexity or violation count).

### Step 2: Identify the Hot Spots

Locate the specific functions and modules that exceed thresholds.

**Heuristics for finding complexity:**
- Functions with many `if/else if/else` chains (switch to strategy pattern or
  lookup table)
- Functions with nested loops inside conditionals inside callbacks
- Classes that manage multiple orthogonal concerns (extract into separate
  classes)
- Files that import from too many modules (violation of Single Responsibility)
- God objects or utility files that grow organically over time
- Functions whose name contains "and" (`validateAndSave`) — do one thing
- Boolean parameters that change behavior (`process(data, true)` → split)

**Pattern library for extraction:**

| Pattern | Use When | Result |
|---------|----------|--------|
| **Extract Method** | A block of code with a clear purpose and minimal params | One function becomes two smaller functions |
| **Strategy Pattern** | A long if/else chain choosing behavior | Each branch becomes its own class/function |
| **Replace Conditional with Polymorphism** | Behavior varies by type | Each type handles its own variant |
| **Introduce Parameter Object** | 4+ parameters frequently passed together | A single object reduces surface area |
| **Replace Loop with Pipeline** | A loop with filter/map/reduce steps | Declarative chain is self-documenting |
| **Decompose Conditional** | A complex if condition | Extract condition into named function |
| **Consolidate Duplicate Conditionals** | Same condition in multiple branches | Hoist and return early |
| **Guard Clause** | Nested conditionals for error handling | Return early, reduce nesting |

**Exit criteria:** Each hot spot has exactly one refactoring pattern selected
and a plan documented (what moves where, what tests validate behavior).

### Step 3: Apply the Refactoring (One Pattern at a Time)

Execute each refactoring independently. Run tests after each step. Never
combine two simplifications in the same commit — if behavior changes, you
will not know which step caused it.

**Rules of engagement:**
1. One refactoring per commit. The commit message names the pattern used
   and the complexity reduction achieved (e.g., `extract method: reduce
   `processOrder` from 85→22 lines, cc 14→4`).
2. Run tests before committing. If any test fails, the refactoring is
   incorrect — revert and re-attempt.
3. Do not change behavior during a simplification pass. If you discover a
   bug, fix it in a separate commit (before or after, but not during).
4. Keep the diff readable. If the diff is >100 lines, the refactoring is
   too large. Break it further.

**Exit criteria:** Each hot spot is addressed, tests pass, and the diff is
clean (behavior-preserving changes only).

### Step 4: Verify Behavioral Preservation

Simplification changes structure, not semantics. Verification proves this.

**Verification methods:**
- **Characterization tests:** If no tests exist, write snapshot/approval
  tests before changing a single line of logic. These capture the current
  output. After refactoring, the snapshots must match.
- **Mutation testing:** Tools like `stryker-mutator` or `mutmut` verify
  that your tests actually detect behavior changes. Run before and after
  to confirm test quality is preserved.
- **Diff review:** The diff should show structural changes (method extractions,
  renames, parameter objects) but zero logic changes. If a line of logic
  appears altered, that change must be intentional and isolated.
- **Property-based testing:** For critical modules, use property-based tests
  (Hypothesis, QuickCheck, fast-check) that assert invariants rather than
  specific outputs.

**Exit criteria:** Same test suite, same code coverage, same mutation score,
same behavior for all known edge cases.

### Step 5: Install Guards

Prevent complexity from re-accumulating in the simplified code.

**Guard types:**
- **Complexity gates in CI:** Add linter rules that fail the build if
  cyclomatic complexity exceeds 10 or file length exceeds 500 lines.
- **Review checklists:** Add a "complexity impact" section to the PR template
  asking "Does this change increase complexity? If so, what is the offsetting
  simplification?"
- **Code ownership:** Assign explicit owners for the most complex modules
  and require their signoff on all changes.
- **Migration guide:** For shared patterns (e.g., "use the strategy pattern
  instead of if/else chains"), document an internal ADR and link it from the
  codebase style guide.

---

## Anti-Rationalization Table

| Excuse | Rebuttal |
|--------|----------|
| "The code works, why touch it?" | Working code with high complexity is a ticking time bomb. The cost to simplify now is 1x. The cost to debug a production incident in complex code is 10-50x. |
| "I don't understand all of it, so I shouldn't change it." | Chesterton's Fence: understand the fence first (add the characterization tests), *then* change it. Not understanding is a reason to simplify, not a reason to defer. |
| "Simplification is subjective; one person's clarity is another person's obfuscation." | Cyclomatic complexity and file length are objective. Use the metrics as the gate, not personal taste. |
| "We don't have test coverage for that module." | Then adding characterization tests is Step 0. Without tests, you cannot safely simplify. The lack of tests is itself evidence the module needs simplification. |
| "I'll rewrite it from scratch instead." | A rewrite throws away knowledge encoded in the existing code (edge cases, bug fixes, performance tuning). Incremental refactoring preserves that knowledge. |
| "The pattern I'm replacing is fine; I'm just making it 'cleaner.'" | If you cannot articulate which complexity metric improves by how much, stop. Simplification without measurement is decoration. |
| "We don't have time to refactor right now." | Every feature built on complex foundations takes longer to build and is more likely to break. The time "saved" by skipping simplification is borrowed at compound interest. |

## Red Flags

- Same complexity hot spots present 6 months after being identified
- Refactoring commits that exceed 100 lines diff
- "Simplify" PRs that also fix bugs (behavior change mixed with restructuring)
- Tests fail after a simplification pass and are "fixed" by updating the test
  (not the refactoring)
- Cyclomatic complexity increases year over year across the codebase
- Engineers say "don't touch that file, it's fragile" — classic complexity
  debt signal
- New features require copy-pasting complex existing patterns

## Verification

1. Run complexity metrics before and after. Every metric should be strictly
   lower or unchanged.
2. Run the test suite. Zero failures.
3. Run mutation testing. Mutation score should be equal or higher (not lower).
4. Check the diff. Does it contain only structural changes? Zero logic
   changes?
5. Review each hot spot: does the selected pattern address the specific
   complexity identified in Step 2?
6. Verify CI complexity gates are in place. Does the build fail if thresholds
   are exceeded?
7. Ask someone unfamiliar with the module to read the simplified code. Time
   their understanding. It should be faster than before.
8. Check that no new dependencies were introduced by the simplification
   (dependency graph should be flatter or unchanged).
