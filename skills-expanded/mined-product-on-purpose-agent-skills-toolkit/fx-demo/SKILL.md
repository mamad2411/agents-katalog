---
name: fx-demo
description: A fixture skill that exists so the re-derived manifest has a component list to compare. Use only from tests/unit/self-consistency.test.mjs.
metadata:
  version: 0.1.0
  tier: universal
---

# fx-demo

## Purpose
Give the self-consistency fixture one on-disk component, so the guard is exercised against a real tree
rather than only against strings.

## When to use
Never outside the test suite. This directory is a regression corpus, not a shipped skill.
