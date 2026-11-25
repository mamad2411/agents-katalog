---
name: corpus-clean-b
description: "Use when verifying corpus discovery against a clean fixture pair."
version: 0.1.0
---

# corpus-clean-b

## Intent

Serves as the beta half of the clean corpus fixture pair.

## Inputs

The corpus root path handed over by the beta test.

## Preconditions

The beta fixture tree is checked out unchanged.

## Procedure

1. Stay deliberately unlike the alpha sibling in every sentence.
2. Provide beta-flavored prose for the discovery assertions.

## Output

An empty findings list for the beta fixture.

## Examples

Given the input `beta`, the expected output is `beta-lint-clean`.

## Anti-patterns

Copying alpha prose into the beta fixture.
