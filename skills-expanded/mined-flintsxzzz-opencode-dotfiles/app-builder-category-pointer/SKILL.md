---
name: app-builder-category-pointer
description: "Pointer to a library of 4 specialized App Builder skills. Use when working on app-builder-related tasks."
risk: none
---

# App Builder Capability Library 🎯

This is a **pointer skill**. The 4 specialized App Builder skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **fastapi-templates** — Create production-ready FastAPI projects with async patterns, dependency injection, and comprehensive error handling. Use when building new FastAPI applications or setting up backend API projects.
- **frontend-mobile-development-component-scaffold** — You are a React component architecture expert specializing in scaffolding production-ready, accessible, and performant components. Generate complete component implementations with TypeScript, tests, s
- **javascript-typescript-typescript-scaffold** — You are a TypeScript project architecture expert specializing in scaffolding production-ready Node.js and frontend applications. Generate complete project structures with modern tooling (pnpm, Vite, N
- **templates** — Project scaffolding templates for new applications. Use when creating new projects from scratch. Contains 12 templates for various tech stacks.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/app-builder/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/app-builder`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
