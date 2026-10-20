---
name: arch-code-review
description: Review code and pull requests for defects, security, quality, and convention
  compliance. Covers PR review pipelines with confidence scoring, pre-commit self-verification,
  silent-failure and error-handling audits, type-design analysis, comment accuracy,
  and test coverage review. Use before committing, before opening a PR, or when asked
  to review existing changes.
---

# Code Review (composite skill)

Review code and pull requests. Composed from: code-review, requesting-code-review,
pr-code-reviewer, pr-code-simplifier, pr-test-analyzer, comment-analyzer,
silent-failure-hunter, type-design-analyzer.

## When to activate

- Review of a PR or a set of changes
- Pre-commit / pre-PR self-verification of new code
- User asks "does this look right?", "review my changes"
- Focused audits: error handling, type design, test coverage, comments

## A. PR review pipeline (structured)

1. **Eligibility**: skip if the change is closed/draft/automated/simple-and-obviously-fine.
2. **Conventions**: collect project instruction files (AGENTS.md/CLAUDE.md) in root and
   modified dirs; list paths.
3. **Summary**: produce a concise change summary.
4. **Parallel review passes** (independent lenses):
   - **Conventions**: audit changes against AGENTS.md/CLAUDE.md.
   - **Shallow bugs**: read only the diff; scan for large obvious bugs; ignore nitpicks.
   - **History**: `git blame` + history of modified code.
   - **Prior changes**: previous PRs that touched these files; their comments apply here?
   - **Comments**: ensure changes comply with guidance in code comments.
5. **Confidence scoring** (0–100):
   - 0: false positive / pre-existing.
   - 25: possible but unverified; stylistic unless in conventions.
   - 50: verified real but nitpick/rare.
   - 75: double-checked, likely hit in practice; impacts functionality or explicit convention.
   - 100: certain, frequent; evidence confirms.
6. **Filter**: report only issues scored ≥ 80.
7. **Re-check eligibility** (change may have moved).
8. **Report**: findings with file:line, why it matters, concrete fix; cite links.

### False-positive exclusions
Pre-existing issues; things that look like bugs but aren't; senior-level nitpicks;
what a linter/typechecker/CI catches; generic quality unless convention-required;
convention issues explicitly silenced in code (lint-ignore); intentional functionality
changes; real issues on lines the author didn't modify.

## B. Pre-commit self-verification

1. **Get the diff** of changes.
2. **Static security scan**: hardcoded secrets, shell injection, dangerous eval/exec,
   unsafe deserialization, SQL string formatting.
3. **Baseline tests and linting** (language-specific: pytest/npm test/cargo test/go test).
4. **Self-review checklist**: correctness, edge cases, error handling, naming,
   test coverage.
5. **Independent reviewer** pass (fresh perspective).

## C. Silent-failure & error-handling audit

1. **Identify all error handling code**: catch blocks, fallbacks, `Result`/`?`, error maps.
2. **Scrutinize each handler**: is the failure swallowed? logged? recoverable?
3. **Check for hidden failures**: silent catch, empty fallback, ignored `Err`, `unwrap`/panic
   in prod paths, default that masks the real cause.
4. **Error messages**: actionable? include context (what, where, how to fix)?
5. **Validate against project standards** for error propagation and observability.

Report each finding with confidence; focus on failures that suppress errors or hide
the real cause.

## D. Type-design analysis

Evaluate types for: **encapsulation** (fields hidden, invariants kept), **invariant
expression** (does the type forbid invalid states?), **usefulness** (does the type earn
its existence?), **enforcement** (is the invariant compiler-enforced, not just
convention?). Rate each dimension; give qualitative feedback and concrete refactors.

## E. Test coverage review (PR)

- Do tests cover the new functionality and edge cases?
- Are they meaningful (assert behavior) or just exercise code paths?
- Missing cases: error paths, boundary values, empty states, concurrency.
- Are tests brittle (implementation-coupled) or stable (behavior-coupled)?

## F. Comment-accuracy audit

- Comments match the code they describe?
- Docstrings complete and accurate?
- Comment rot / stale guidance flagged as debt?
- Changes comply with guidance embedded in comments?

## Output format

Start with what's being reviewed. For each high-confidence issue: description +
confidence, file:line, the convention rule or bug explanation, concrete fix.
Group by severity (Critical 90-100, Important 80-89). If no high-confidence issues,
confirm the code meets standards with a brief summary.

## Related skills
- `arch-code-architecture` — review architecture before code
- `arch-code-quality` — conventions and standards the review enforces
- `arch-refactoring` — when review surfaces simplification/modernization needs
