---
name: intake-project
description: Use at the very start of a new project to turn a rough idea or a draft brief into a refined, agreed project brief. Looks for a user-written draft; refines it by questioning if present, or runs an interactive intake interview to create it if absent.
---

# Intake Project

**Announce at start:** "I'm using claude-engineer:intake-project to pin down what we're building."

Goal: a **refined, mutually-agreed brief** that the planning stage can turn into a phased plan.

## Procedure (create a task per step)
1. **Find the brief.** Look for `_private/initial-plan-draft.md`.
   - **Present** → read it, then **grill** the user to fill gaps (see checklist below). Don't accept vagueness.
   - **Absent** → run an interactive intake interview, then WRITE their answers into `_private/initial-plan-draft.md`.
2. **Run the requirements/design dialogue** via `superpowers:brainstorming`. Do not skip - it is the discovery engine and the hard gate against premature building.
3. **Resolve the stack decisions** that the plan needs (defaults are opinionated; confirm only the genuinely open ones):
   - Frontend: **React (Vite SPA) vs Next.js** - choose per the project type (see `claude-engineer:frontend-development`).
   - JS package manager: **Bun vs pnpm**.
   - Anything project-specific (auth model, external integrations, data shapes).
4. **Capture the brief** to `_private/initial-plan-draft.md`: problem & users, core features (MoSCoW), the agreed stack choices, non-goals, constraints, any reference products/designs, success criteria.
5. **Hand off** to `claude-engineer:plan-project`.

## Intake checklist - the brief is not done until these are answered
- Who are the users and what is the one job-to-be-done?
- The 3 - 7 core features for v1, and explicit non-goals.
- React vs Next.js (and why); any second frontend?
- Design direction / brand / reference products (feeds the DESIGN.md in `claude-engineer:design-system`).
- Data model sketch and the key entities.
- Auth & roles? External services/APIs? Background jobs?
- Definition of success for v1.

## Red flags - STOP and keep grilling
- "Let's just start coding." → No. Build is plan-gated.
- Features described as adjectives ("modern", "fast") with no concrete behavior.
- Stack chosen by habit without matching the project type.
- The user and you picture different products. Reflect the brief back until it matches.
