---
name: fixture-tool
description: Echo strings back from an in-process fixture model. Use when a
  loader test needs a minimal tool bundle with a tools.py.
license: MIT
compatibility: requires gap>=0.1
metadata: {category: testing, tags: [fixture, echo]}
gap:
  tools:
    - fixture-tool.echo: Echo a string back, uppercased.
---

# fixture-tool

A minimal tool bundle: one `@tool` function in `tools.py`, no canonical
scripts. Exists only for the loader test suite.

## When to use

- Never, outside of tests.
