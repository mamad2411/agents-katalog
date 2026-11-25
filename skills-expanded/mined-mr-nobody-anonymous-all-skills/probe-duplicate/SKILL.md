---
name: probe-duplicate
description: "PROBE FIXTURE side B. Two plugins ship a skill with this exact directory name and this exact skill name. Invoke it and read which side answers - that is the whole experiment."
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


# Probe duplicate, side B

When invoked, state exactly: **"I am side B."** and stop.

Do nothing else. The only information this skill carries is which copy of it the runtime resolved.
