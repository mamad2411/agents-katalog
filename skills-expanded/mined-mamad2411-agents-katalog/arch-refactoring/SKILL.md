---
name: arch-refactoring
description: Refactor, simplify, and modernize existing or legacy code safely. Covers
  legacy analysis, simplification, version-uplift migration, behavioral pinning with
  tests, business-rule extraction, and scaffolding new structure. Use before rewrites,
  for code-simplification tasks, when migrating a stack or module, or when improving
  maintainability without changing behavior.
---

# Refactoring & Modernization (composite skill)

Refactor, simplify, and modernize code safely. Composed from: code-simplifier,
legacy-analyst, version-delta-analyst, uplift-migrator, test-engineer,
business-rules-extractor, scaffolder.

## When to activate

- Simplify/refactor existing code for clarity and maintainability
- Migrate a module, project, or stack version
- Understand and modernize legacy code
- Extract business rules into testable specifications
- Scaffold a new structure around an approved architecture

## Core principle: pin behavior before you touch code

**Never rewrite before characterization.** Refactoring is provable only when the old
behavior is pinned. Write tests that capture current behavior first (characterization
tests), then refactor, then prove the diff didn't change behavior.

## A. Legacy analysis (understand before acting)

- **Structural map**: modules, dependencies, entry points, dead code.
- **Behavioral understanding**: what the system actually does, not what docs claim.
- **Dependency graph**: who depends on what; identify seams.
- **Dead-code detection**: unused exports/functions/classes.
- Output: a map of the system with seams marked for change.

## B. Business-rule extraction

Separate "what the business requires" from "how the old code happened to implement it":
- Mine domain logic, calculations, validations, policies from legacy code.
- Write them as **Given/When/Then** specifications (testable).
- These become the acceptance criteria for the rewrite/refactor.

## C. Characterization / contract / equivalence tests

Before any rewrite:
- **Characterization**: pin current behavior as-is (even if it's a bug — document it).
- **Contract**: pin external interfaces (I/O, error behavior).
- **Equivalence**: prove old and new behave identically on a test corpus.

## D. Simplification (code-simplifier)

Focus on recently modified code unless told otherwise. Preserve functionality while
improving:
- Clarity: names, structure, flow.
- Consistency: conventions, patterns.
- Maintainability: reduce duplication, extract meaningful helpers.
- Remove: ceremonial code, unnecessary abstractions (one impl, no second use),
  dead branches.
Don't over-refactor: only touch what earns its change; keep diffs minimal and reviewable.

## E. Version-uplift migration (same stack)

- **Identify breaking changes** between the two versions (e.g. .NET 4.8→8, Java 8→17,
  Spring Boot 2→3) that actually bite THIS codebase.
- Drive the ecosystem's migration tooling.
- **One module at a time**: migrate a pilot unit first, write a playbook, then apply to
  the rest.
- **Minimal diff**: preserve code, tweak what the version requires — not a rewrite.
- **Prove it**: run that unit's real build after migration.
- Flag "same-stack" bumps that are really rewrites (Python 2→3 str/bytes, AngularJS→Angular)
  — those need full rewrite flow, not minimal-diff.

## F. Scaffolding new structure

Once architecture is approved and spec exists:
- Project skeleton, domain model, API stubs.
- Executable acceptance tests (from the Given/When/Then specs).
- Write access scoped to the new service directory only.

## Safety rules

1. **Pin behavior first** — never refactor without characterization/contract tests.
2. **One module at a time** — no cross-cutting rewrites in one pass.
3. **Minimal diff** — every change should be explainable and reviewable.
4. **Real build/run proof** after each migrated unit.
5. **Refuse to migrate without a playbook** (for uplift) — no proven playbook, no migration.
6. **Mask secrets in findings** (`'Pr0d****'` + file:line) when quoting code.

## Output

- **Before**: characterization tests green (baseline).
- **During**: per-module migration/refactor with build proof.
- **After**: equivalence/contract tests green; summary of what changed and why.

## Related skills
- `arch-code-architecture` — target architecture for the refactor
- `arch-code-quality` — conventions the result must follow
- `arch-code-review` — review the refactored result
