---
name: planning-category-pointer
description: "Pointer to a library of 7 specialized Planning skills. Use when working on planning-related tasks."
risk: none
---

# Planning Capability Library 🎯

This is a **pointer skill**. The 7 specialized Planning skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **blueprint** — Turn a one-line objective into a step-by-step construction plan any coding agent can execute cold. Each step has a self-contained context brief — a fresh agent in a new session can pick up any step without reading prior steps.
- **concise-planning** — Use when a user asks for a plan for a coding task, to generate a clear, actionable, and atomic checklist.
- **decision-navigator** — Guide stuck or overwhelmed users through targeted branching questions until they reach concrete next steps.
- **plan-writing** — Structured task planning with clear breakdowns, dependencies, and verification criteria. Use when implementing features, refactoring, or any multi-step work.
- **planning-with-files** — Work like Manus: Use persistent markdown files as your "working memory on disk."
- **track-management** — Use this skill when creating, managing, or working with Conductor tracks - the logical work units for features, bugs, and refactors. Applies to spec.md, plan.md, and track lifecycle operations.
- **writing-plans** — Use when you have a spec or requirements for a multi-step task, before touching code

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/planning/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/planning`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
