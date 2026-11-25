---
name: warn-only
description: "Use when testing warning-only exit code behavior."
version: 0.1.0
author: somebody
---
# warn-only

## Intent

Control fixture: exactly one warning (FM01 unknown field), exit 0.

## Inputs

None — the fixture is static.

## Preconditions

None — no external dependencies.

## Procedure

1. Lint this directory and expect one warning.

## Output

A findings list with a single FM01 warning.

## Examples

Given the input `shakespii lint tests/fixtures/warn-only`, the expected output is one warning and exit code 0.

## Anti-patterns

Adding a second unknown field — the CLI test locks the count at one.
