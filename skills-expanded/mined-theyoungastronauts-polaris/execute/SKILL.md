---
name: execute
description: "Execute one phase of an implementation plan — plan mode, implement, test, summarize; leaves changes uncommitted for the reviewer."
disable-model-invocation: true
---

# Execute a Phase

You are executing a phase of an implementation plan. Follow these steps exactly.

## 1. Find the Plan

Look for `plan.md` in the current directory, then `../plan.md`. If not found, ask the user where it is.

## 2. Identify the Phase

If the user specified a phase number, use that. Otherwise, review the plan and ask which phase to execute. Show a brief summary of each phase so the user can pick.

## 3. Plan the Implementation

**If a `/autopilot` or `/orchestrator` lead spawned you against a pre-approved plan.md, skip plan mode** — the approved plan is your approval. Explore the codebase as needed and go straight to implementation.

**In an interactive session, enter plan mode before writing any code.** Read through the phase tasks, explore the existing codebase, and present a concrete implementation plan:

- Which files you'll create or modify
- What approach you'll take for each task
- What order you'll work in
- Any decisions or trade-offs the user should weigh in on

The user can adjust the approach, reorder tasks, or flag concerns before any code is written. Only exit plan mode and start implementing after the user approves.

## 4. Implement

Work through each task in the phase sequentially:

- Read existing code before modifying anything
- Write tests alongside implementation, not after
- **Do not commit.** Leave all changes staged/unstaged. The verifier will commit after the phase passes verification.
- Stay within the phase scope — if you find work that belongs in another phase, note it but don't do it

If something in the plan doesn't make sense after seeing the actual code, stop and flag it rather than blindly following.

## 5. Integration Summary (if applicable)

If this phase produces or changes API endpoints, generate an integration summary at `docs/integration/[feature].md` covering endpoints, request/response shapes, auth, and error codes.

## 6. Wrap Up

When the phase is complete, provide a summary:

- What was implemented
- Files changed (list them)
- Any deviations from the plan and why
- Any concerns or notes for the next phase

Suggest running `/verify` in a new session as the next step.
