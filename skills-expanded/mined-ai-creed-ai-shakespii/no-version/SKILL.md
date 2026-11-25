---
name: no-version-skill
description: "Use when verifying config overrides against a version-less fixture skill."
---

# no-version-skill

## Intent

Carries exactly one default-profile finding: the missing version error.

## Inputs

The config fixture path handed over by the test.

## Preconditions

The config fixture tree is checked out unchanged.

## Procedure

1. Lint once without a config to observe the FM05 error.
2. Lint again with each override fixture to observe the change.

## Output

One FM05 finding by default; fewer under overrides.

## Examples

Given the input `no-version`, the expected output is `one FM05 error`.

## Anti-patterns

Adding a version field; the missing field is the fixture's point.
