---
name: validate-by-challenge
description: Challenge code-review and security-review findings independently for evidence, scope, and severity before a validation report is published. Use during a validation cycle or when another skill needs findings pressure-tested.
---

# Validate by challenge

Read [the shared validation contract](../validate/validation-contract.md). The caller supplies `RUN_DIR` and exactly one `source`: `code` or `security`. Challenge only that source. Do not read the other reviewer's artifacts.

## Challenge code findings

When `source` is `code`: read `code-review.json` and the diff and repository context named in `context.json`. For each finding, independently seek counterevidence: an applicable project rule, an intentional local pattern, existing abstraction constraints, unchanged pre-existing behavior, a test that proves the concern false, or a smaller accurate scope. Write one verdict per finding to `challenge-code-review.json`: `upheld`, `dismissed`, or `reframed`. A reframe supplies a corrected finding with the same ID.

**Done when:** every code finding has exactly one evidence-based verdict.

## Challenge security findings

When `source` is `security`: read `security-review.json` and the same diff/context. Explicitly test attacker reachability, required privileges, existing controls, realistic impact, and severity. Write one verdict per finding to `challenge-security-review.json`.

**Done when:** every security finding has exactly one evidence-based verdict, and no new findings were introduced.
