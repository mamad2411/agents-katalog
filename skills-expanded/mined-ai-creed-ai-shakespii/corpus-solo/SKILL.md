---
name: corpus-solo
description: "Use when verifying that corpus discovery reports skipped directories."
version: 0.1.0
---

# corpus-solo

## Intent

Serves as the only real skill in the skipped-directory fixture root.

## Inputs

The corpus root path handed over by the skip test.

## Preconditions

The skip fixture tree is checked out unchanged.

## Procedure

1. Sit beside a non-skill directory and a stray file.
2. Remain the only discovered skill in this root.

## Output

An empty findings list for the solo fixture.

## Examples

Given the input `solo`, the expected output is `solo-lint-clean`.

## Anti-patterns

Adding a SKILL.md to the notes directory.
