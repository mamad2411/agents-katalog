---
name: planning-category-pointer
description: "Pointer to a library of 12 specialized Planning skills. Use when working on planning-related tasks."
risk: none
---

# Planning Capability Library 🎯

This is a **pointer skill**. The 12 specialized Planning skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **blueprint** — Turn a one-line objective into a step-by-step construction plan any coding agent can execute cold. Each step has a self-contained context brief — a fresh agent in a new session can pick up any step without reading prior steps.
- **concise-planning** — Use when a user asks for a plan for a coding task, to generate a clear, actionable, and atomic checklist.
- **decision-navigator** — Guide stuck or overwhelmed users through targeted branching questions until they reach concrete next steps.
- **idea-refine** — Refines raw ideas into sharp, actionable concepts through structured divergent and convergent thinking. Use when an idea is still vague, when you need to stress-test assumptions before committing to a plan, or when you want to expand options before converging on one.
- **idea-to-blueprint** — Turn a raw product, app, bot or feature idea into one evidence-backed build blueprint (researched stack, epics, Given/When/Then criteria, tests) that coding agents build one epic per session.
- **not-a-vibe-coder** — Turns vague prompts into 8 structured planning files for brand new projects. DO NOT use on existing codebases.
- **plan-writing** — Structured task planning with clear breakdowns, dependencies, and verification criteria. Use when implementing features, refactoring, or any multi-step work.
- **planning-and-task-breakdown** — Breaks work into ordered tasks. Use when you have a spec or clear requirements and need to break work into implementable tasks. Use when a task feels too large to start, when you need to estimate scope, or when parallel work is possible.
- **planning-with-files** — Work like Manus: Use persistent markdown files as your "working memory on disk."
- **spec-driven-development** — Creates specs before coding. Use when starting a new project, feature, or significant change and no specification exists yet. Use when requirements are unclear, ambiguous, or only exist as a vague idea.
- **track-management** — Use this skill when creating, managing, or working with Conductor tracks - the logical work units for features, bugs, and refactors. Applies to spec.md, plan.md, and track lifecycle operations.
- **writing-plans** — Use when you have a spec or requirements for a multi-step task, before touching code

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `read` to load its `SKILL.md` from the vault:
   `/home/melfiano/.config/opencode/skill-libraries/planning/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `/home/melfiano/.config/opencode/skill-libraries/planning`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
