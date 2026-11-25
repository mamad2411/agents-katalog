---
name: mes-project-onboarding
description: Use when an AI agent starts work in the AI-MES Copilot repository, needs to understand project structure, split a broad request into safe tasks, locate relevant documents, or choose the right MES-specific skill before coding.
---

# MES Project Onboarding

## Purpose

Use this first for broad requests such as "继续开发 MES", "实现某个模块", "检查项目", or "规划下一步". The goal is to gather context and narrow the task before editing code.

## Workflow

1. Check repository state with `git status --short --branch`.
2. Read `README.md`, `CONTRIBUTING.md`, and the relevant guides under `docs/`; locate other maintained documents with `rg --files -g "*.md"`.
3. Read `COLLABORATION.md`, `docs/FEATURES.md`, and the actual controller, domain service, schema or migration needed for the task. The current business scene is dimmable desk lamps L100/L200.
4. Identify target module, table prefix, API prefix, and frontend area.
5. Choose the next skill:
   - backend CRUD: `mes-backend-resource`
   - production, inventory, quality, traceability flow: `mes-backend-business-flow`
   - API mismatch: `mes-api-contract-sync`
   - entity/schema work: `mes-mysql-schema-check`
   - PC frontend: `mes-pc-frontend-page`
   - historical WeChat mini program, only when explicitly in scope: `mes-wechat-miniprogram`
   - integration, debug, test, review, progress: matching skill by name
6. If the user request is broad, split it into one deliverable that can be verified in the current turn.

## Task Slicing Rule

Prefer one small vertical slice:

- one module, table group, or screen;
- one API set, not every module at once;
- one failing test/build issue, not a general cleanup.

## Must Not

- Do not generate controllers, pages, or SQL before reading related files.
- Do not move or normalize unrelated documentation while implementing a feature.
- Do not mark a module complete without a verification result.
