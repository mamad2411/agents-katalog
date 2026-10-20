---
name: copies-rule
description: >-
  Does a sample task. Use when a sample is needed.
---

# Sample

## When to use

When a sample is needed.

## Procedure

1. Read the sibling code.
2. Compare with `core.repository.diff`.
3. Do not add credentials, tokens, private keys or connection strings with embedded
   passwords to tracked files, including tests, fixtures, examples and evidence records.
   Reference secrets through the project's configured secret mechanism.

The rule core.security.no-secrets-in-source applies.
