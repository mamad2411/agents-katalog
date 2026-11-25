---
name: cs-caller-space
description: "Calls both worker subagents using a whitespace-only-separated metadata.chain string. Use when delegating work to cs-worker-a and cs-worker-b without commas."
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

# cs-caller-space
Delegates to cs-worker-a and cs-worker-b. `metadata.chain` is declared as a
whitespace-only-separated string (no commas), proving S4 tolerates that separator too.
