---
name: mission-skill
description: "Use when verifying anatomy alias overrides against a fixture skill."
version: 0.1.0
---

# mission-skill

## Mission

States its purpose under a heading only a config override can accept.

## Inputs

The config fixture path handed over by the alias test.

## Preconditions

The alias fixture tree is checked out unchanged.

## Procedure

1. Lint once without a config to observe the CT06 warning.
2. Lint again with the intent-alias override to observe silence.

## Output

One CT06 warning by default; none under the alias override.

## Examples

Given the input `mission`, the expected output is `one CT06 warning`.

## Anti-patterns

Renaming the Mission heading back to Intent.
