---
name: cs-caller-comma
description: "Calls both worker subagents using a comma-separated metadata.chain string. Use when delegating work to cs-worker-a and cs-worker-b."
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

# cs-caller-comma
Delegates to cs-worker-a and cs-worker-b. `metadata.chain` is declared as a comma-separated
string (the recommended shape), not a YAML list.
