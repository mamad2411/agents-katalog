---
name: corpus-clone-b
description: "Use when verifying near-clone detection against a fixture pair."
version: 0.1.0
---

# corpus-clone-b

## Intent

Provides one half of a deliberately duplicated fixture pair.

## Inputs

A corpus root path supplied by the near-clone test.

## Preconditions

The clone fixture tree is checked out unchanged.

## Procedure

1. Repeat the shared fixture prose verbatim.
2. Keep both siblings byte-identical below the title.
3. Trigger near-clone detection by construction.
4. Trigger duplicate-block detection by construction.

## Output

An empty findings list for the clone fixture.

## Examples

Given the input `clone`, the expected output is `clone-lint-clean`.

## Anti-patterns

Letting the siblings drift apart.
