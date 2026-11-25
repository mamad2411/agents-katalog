---
name: validate-with-code-review
description: Validate a PR diff against repository code standards, established practices, and simplification opportunities. Use during a validation cycle or when another skill needs a focused code review.
---

# Validate with code review

Read [the shared validation contract](../validate/validation-contract.md). The caller supplies `RUN_DIR` containing `context.json` and `changes.json`.

## Review the diff against its home

Read the complete three-dot diff from `context.json`, then inspect every changed file with enough surrounding code to understand its module. Find repository guidance before judging: `AGENTS.md`, `CONTRIBUTING*`, style/lint configuration, test conventions, architecture docs, and nearby analogous code. Repository rules override general preferences.

For every changed behavior, test these lenses: explicit standards, consistency with local patterns, unnecessary complexity or abstraction, duplicated logic, unclear names or boundaries, and code that can be deleted or made more direct without losing required behavior. Report only actionable regressions caused or exposed by the diff; leave formatting and mechanically enforced rules to tooling.

Write `code-review.json` atomically as the contract's finding array. Every finding needs a changed-line location, quoted evidence, impact, and a concrete simplification or correction. Prefer no finding to a speculative nit.

**Done when:** every changed file has been considered against all applicable repository guidance and lenses, and `code-review.json` is a valid JSON array with no duplicate concerns.
