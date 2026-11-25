---
name: corpus-good
description: "Use when verifying that one broken skill does not abort the corpus run."
version: 0.1.0
---

# corpus-good

## Intent

Serves as the healthy neighbor of a deliberately broken fixture skill.

## Inputs

The corpus root path handed over by the broken-skill test.

## Preconditions

The broken fixture tree is checked out unchanged.

## Procedure

1. Lint cleanly while the neighbor fails to parse.
2. Prove the corpus loop isolates per-skill failures.

## Output

An empty findings list for the good fixture.

## Examples

Given the input `good`, the expected output is `good-lint-clean`.

## Anti-patterns

Fixing the broken neighbor; it is broken by design.
