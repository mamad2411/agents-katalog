---
name: minimal-pass
description: "Use when verifying the shakespii seed rules against a known-clean fixture skill."
version: 0.1.0
---

# minimal-pass

## Intent

Provides a known-clean control fixture for the seed rule set.

## Inputs

None — the fixture is static.

## Preconditions

None — no external dependencies.

## Procedure

1. Run the linter against this directory.
2. Expect zero findings.

## Output

An empty findings list.

## Examples

Given the input `shakespii lint tests/fixtures/minimal-pass`, the expected output is `✔ 0 problems` and exit code 0.

## Anti-patterns

Editing this fixture without updating the engine control test.
