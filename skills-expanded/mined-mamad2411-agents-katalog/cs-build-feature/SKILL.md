---
name: cs-build-feature
description: >
  Interactive orchestrator that builds a feature from its CodeSpring plan. It
  interviews the user about what they're building, checks the feature has enough
  context (notes + Frontend/Backend PRDs) and a numbered task list, guides them
  to fill any gaps, then builds the Kanban tasks — optionally spawning up to 5
  parallel sub-agents — while guarding the shared systems it could break. Use
  when the user wants to build/implement a feature they planned in CodeSpring.
  Triggers, "build this feature", "implement my feature", "start building from
  CodeSpring", "let's build X", "work through my Kanban tasks".
allowed-tools: Bash(codespring:*) Bash(npx @codespring-app/cli:*)
metadata:
  author: codespring
  version: "0.1"
---

# Build a feature from its CodeSpring plan

A guided, interactive build. Do NOT jump straight to writing code — walk the user through readiness first, then build in a controlled way. This skill both reads the plan and (in the build phase) edits the codebase, so be deliberate.

Uses: `codespring` skill references (`task-workflow.md`, `prd-management.md`, `pitfalls.md`, `codespring-docs.md`), and the sibling skills `cs-build-create-prd` and `cs-build-create-tasks`.

## 0. Connect first
`codespring auth status` + `codespring status` (LOCAL project; print it).

## 1. Interview — what are we building?
Ask the user what feature they want to build. Then read what CodeSpring has and reflect it back in **3 simple bullet points**: "Here's what I think we're building — confirm or correct." Keep it plain-language.

## 2. Readiness check — is there enough context?
For the target feature, verify:
- A **how-it-works note** exists and is substantive.
- **Frontend and Backend PRDs** exist (`codespring prds` / `codespring prd <id>`).
- The Backend PRD actually covers the shared systems (routes, data model, auth/RLS, jobs/cron, storage, payments/credits, env vars) and a dependency map.

If context is missing:
- Offer to generate PRDs now via **`cs-build-create-prd`**, OR
- Tell the user to do it in the CodeSpring web app and walk them through it using `references/codespring-docs.md` (open the project → the feature's PRD bridge → add + generate the Frontend/Backend PRD). Then: "Come back and tell me when that's done," and re-check.

## 3. Tasks check — is there a plan to build?
Check the Kanban for numbered tasks on this feature (`codespring tasks --feature <id>`). If there are none, run **`cs-build-create-tasks`** first. Then point the user to the board: in CodeSpring, top-right toggle **Map / Kanban** → click **Kanban** to see the tasks (see `references/codespring-docs.md`).

## 4. Build mode — ask, don't assume
Ask the user two things:
1. **How do you want to build?**
   - **One task at a time** (more control, review between each), or
   - **Run for a while** (build a batch autonomously).
2. If autonomous: **how many parallel sub-agents?** (1–5; cap at 5). Then confirm which tasks each will take.

## 5. Choose the tasks + order
List the feature's `todo` tasks by number. Recommend which to do first — pick the set that gets to a **testable slice** soonest (foundations/backend before dependent UI). Ask the user which tasks to work on now.

## 6. Break-risk guard (important)
Ask: **"Are there any existing features you're worried this could break?"** If yes:
- Add explicit Kanban check tasks (via `cs-build-create-tasks` numbering) to verify those features still work after the build, and
- Tell every sub-agent, in its brief, not to modify the shared systems those features depend on (from the Backend PRD dependency map) without flagging it.

## 7. Build
- Move each task to in progress (`codespring task start <id>`), implement it, then `codespring task done <id>`.
- For parallel builds, spawn up to N sub-agents (max 5). Give each a self-contained brief: its task number + description, the reuse map, the "must not touch" list, and the break-risk guard. Assign independent (parallel-safe) tasks to different agents; keep dependent tasks sequential.
- Report progress against task numbers so the user can watch the board move.

## 8. Wrap up
Summarize what was built, which tasks are done, and what remains. Recommend running the app / tests to verify the testable slice. Suggest **`cs-build-resync-codebase`** once the feature is finalized, so CodeSpring reflects what was actually built.

## What good looks like
- The user confirmed a 3-bullet understanding before any code was written.
- Missing PRDs/tasks were filled (in-app or via the sibling skills) before building.
- The build ran at the control level the user chose (single-step or up to 5 agents), foundations first, with explicit guards so existing features weren't broken.
