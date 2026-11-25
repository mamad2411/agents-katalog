---
name: skillui
description: Governed LeeWay adapter for SkillUI, a CLI that statically extracts design systems from websites, repositories, or local codebases and can generate Agent Skill artifacts.
metadata:
  source-type: tool-adapter
  canonical: amaancoderx/npxskillui
---
# SkillUI Adapter
Canonical source: `amaancoderx/npxskillui` on `main`.

SkillUI is an execution tool, not a canonical upstream `SKILL.md` pack. Use it when a task requires extracting colors, typography, spacing, components, animation patterns, or a reusable design-system skill from an existing site or codebase.

Execution contract:
1. Prefer an already-installed `skillui` executable; do not install packages without authorization.
2. Verify Node.js/runtime prerequisites before execution.
3. Default to static analysis. Use its Playwright-backed ultra mode only when browser execution is authorized and available.
4. Treat generated `SKILL.md`, screenshots, and design tokens as generated evidence, not proof of visual equivalence.
5. Validate the generated artifact against the source before promotion.

State: `REFERENCE_ADAPTER` until the tool is actually available and executed.
