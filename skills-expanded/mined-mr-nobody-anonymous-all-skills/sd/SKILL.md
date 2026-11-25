---
name: sd-skill
description: "Creates a thing and validates it. Use when the frontmatter status must be mirrored by the library.json entry for the mirroring test."
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


# sd-skill

## Purpose
A fixture skill whose frontmatter declares `metadata.status: deprecated` while its library.json entry says `active`, to exercise the S8 status-mirroring check.

## When to use
Only in the components-mirror unit test.
