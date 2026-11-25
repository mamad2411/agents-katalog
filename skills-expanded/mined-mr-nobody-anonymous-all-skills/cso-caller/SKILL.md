---
name: cso-caller
description: "Declares it invokes cso-worker as a STRING, which the chain contract does not permit. Use to exercise the S4 migration-cap ceiling (ADR 0041) for a string-shaped orphan when rules.S4 is overridden to error."
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

# cso-caller
Steps.
