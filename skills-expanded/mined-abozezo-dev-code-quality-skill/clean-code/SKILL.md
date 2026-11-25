---
name: clean-code
description: |
  Removes dead code and unused imports, reduces duplication and complexity, and improves modular architecture
  while preserving intended behavior. Use for focused cleanup, refactoring, maintainability, or architecture work.
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
---

# Clean Code

Use this skill to make a targeted codebase easier to understand, test, and maintain without introducing unrelated rewrites.

## Scope

- Remove unused imports, variables, parameters, unreachable branches, commented-out code, obsolete helpers, and duplicate constants.
- Find and reuse existing helpers, validation, formatting, mapping, and shared abstractions before adding equivalents.
- Replace deep nesting and long conditional trees with guard clauses, early returns, and small single-purpose functions.
- Improve data flow with descriptive names, clear signatures, typed structures where available, and minimal parameters.
- Review module boundaries so responsibilities are cohesive and cross-cutting concerns are shared deliberately.

## Workflow

1. Inspect the requested area and search the workspace for existing utilities and equivalent logic.
2. Identify behavior-preserving cleanup opportunities; prioritize correctness and security over maintainability, performance, and style.
3. Make focused changes only. Avoid speculative rewrites and architectural churn without a concrete benefit.
4. Run the repository's relevant formatter, linter, type checks, and tests. Use the **code-verification** skill when a fuller verification pass is needed.
5. Confirm that behavior is preserved, dead code is gone, control flow is clearer, duplication is reduced, and the result remains testable.

## Guardrails

- Do not keep unused code "just in case"; version control preserves history.
- Do not convert error handling into silent failures. Keep failures explicit and actionable.
- Do not replace a well-scoped cleanup with a broad style-only rewrite.
- For security-sensitive changes, invoke **security-review**. For browser-facing changes, invoke **runtime-devtools-audit**.

## Reference

Read [the universal code-cleaning guide](reference/code-cleaning-universal.md) for language-agnostic rules, priorities, and refactoring patterns.
