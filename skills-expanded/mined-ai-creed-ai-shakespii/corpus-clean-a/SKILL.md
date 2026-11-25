---
name: corpus-clean-a
description: "Use when verifying corpus discovery against a clean fixture pair."
version: 0.1.0
---

# corpus-clean-a

## Intent

Serves as the alpha half of the clean corpus fixture pair.

## Inputs

The corpus root path handed over by the alpha test.

## Preconditions

The alpha fixture tree is checked out unchanged.

## Procedure

1. Stay deliberately unlike the beta sibling in every sentence.
2. Provide alpha-flavored prose for the discovery assertions.

## Output

An empty findings list for the alpha fixture.

## Examples

Given the input `alpha`, the expected output is `alpha-lint-clean`.

## Anti-patterns

Copying beta prose into the alpha fixture.
