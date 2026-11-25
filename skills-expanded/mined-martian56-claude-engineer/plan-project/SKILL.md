---
name: plan-project
description: Use after the project brief is agreed, to produce a phased, multi-file implementation plan with a hard human sign-off gate, before any build work begins. Establishes the decision log and durable state files.
---

# Plan Project

**Announce at start:** "I'm using claude-engineer:plan-project to produce the phased plan."

## Iron Law
**NO BUILD WORK BEFORE THE USER SIGNS OFF ON THE PLAN.** Violating the letter is violating the spirit.

## Procedure (create a task per step)
1. **Decompose with `superpowers:writing-plans`** - turn the agreed brief into bite-sized, testable tasks; map the file structure first; right-size tasks; bake in DRY/YAGNI/TDD.
2. **Impose the customer-experience-first phase order.** Default phases:
   - **Phase 0 - Conventions & scaffold** (`project-conventions`, `monorepo-and-tooling`, `docker-dev-environment`).
   - **Phase 1 - Design system** (`design-system`: DESIGN.md is the source of truth).
   - **Phase 2 - Frontend shells & components** (`frontend-development`, on-token, WCAG AA).
   - **Phase 3 - Backend APIs & data** (`backend-development`).
   - **Phase 4 - Integration & end-to-end flows.**
   - **Phase 5 - Quality, CI/CD, finish** (`testing-and-quality`, `ci-cd-pipeline`).
3. **Write the plan as multiple files** under `docs/plan/` - `00-overview.md` plus one file per phase (`01-design-system.md`, `02-frontend.md`, …), each with goals, tasks, file targets, and the per-phase "definition of done" (the four quality gates).
4. **Record a decision log** at `docs/plan/decisions.md` (every non-obvious choice + why).
5. **Initialize durable state** via `claude-engineer:project-memory` (creates `.claude-engineer/memory.md`, `progress.md`, `current-phase.txt`).
6. **HARD SIGN-OFF GATE.** Present the plan and explicitly ask the user to approve. Do not proceed to `claude-engineer:execute-build` until they do.

## Quality bar baked into every phase's "done"
Tests + coverage · Playwright E2E with zero console errors · WCAG AA · strict types + lint clean.
(See `claude-engineer:testing-and-quality`.)

## Red flags - STOP
- About to scaffold/build code while still "planning" → stop; finish the plan and get sign-off.
- A phase has no concrete "definition of done" → add the four gates.
- The plan lives in one giant file → split into `docs/plan/*` so it survives and stays scannable.
