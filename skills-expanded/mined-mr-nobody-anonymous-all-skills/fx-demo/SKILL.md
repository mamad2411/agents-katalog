---
name: fx-demo
description: "A fixture skill that exists so the re-derived manifest has a component list to compare. Use only from tests/unit/self-consistency.test.mjs."
category: skill-governance
domain: skill-governance
subdomain: general
version: 1.0.0
license: Apache-2.0
risk: low
source:
  repository: "product-on-purpose/agent-skills-toolkit"
  commit: "333810d901"
  imported_at: "2026-09-20"
  license: "Apache-2.0"
platforms:
  - claude-code
  - cursor
  - codex
  - gemini
  - antigravity
  - copilot
---


# fx-demo

## Purpose
Give the self-consistency fixture one on-disk component, so the guard is exercised against a real tree
rather than only against strings.

## When to use
Never outside the test suite. This directory is a regression corpus, not a shipped skill.
