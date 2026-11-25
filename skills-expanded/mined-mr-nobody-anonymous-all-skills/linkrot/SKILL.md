---
name: linkrot
description: "Converts a meeting transcript into a decision log. Use when the user asks to extract decisions, action items, or owners from a transcript."
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


# linkrot

Steps the agent follows. See [the missing reference](missing.md) - a deliberately dangling
relative link so U6 (reference-links) fires an error in this fixture; the sibling
`askit.config.json` waives it with a file-scoped suppression, which must match in
component scope (ADR 0034, resolve profiles in component scope).
