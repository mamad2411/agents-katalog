---
name: auto-build-full
description: Orchestrates subagents to explore, plan, implement, verify, and review a feature end-to-end. Best fit for larger features or features requiring deeper hands-on verification.
---

# Auto Build Full

You are the **orchestrator**. Do not implement the feature yourself. Instead, spawn focused subagents, review their output between steps, and keep the workflow moving. Escalate to the user only when requirements are very ambiguous, access is blocked, or the workflow cannot proceed.

Formulate each subagent's Task prompt from the step instructions below, passing prior subagent output and absolute project paths as context.

## Workflow overview

```
Explore (A) → Plan (B) → [orchestrator reviews plan]
  → Implement (C…) → Verify (D) → Code Review (E)
  → [orchestrator makes reasonable fixes] → Final report
```

Track the feature number `<N>` from `docs/features/<N>_PLAN.md` throughout.

---

## Step 1 — Subagent A: Explore

Spawn an `explore` subagent. Pass the feature description and instruct it to:

1. Explore the codebase to understand current state relevant to the feature
2. Infer user intent; resolve ambiguities from code conventions and context when possible
3. Ask the user **only** if something is genuinely unclear and would materially change the implementation
4. Return a concise brief: relevant files/modules, existing patterns to follow, open questions (resolved or escalated), and recommended scope

Do not write a plan or code. Wait for A to finish before continuing.

If A escalates unanswered questions, ask the user, then re-run or resume A with answers.

---

## Step 2 — Subagent B: Plan

Spawn a subagent. It must **read and follow** the `plan-feature` skill.

Pass A's exploration brief and the original feature description. B writes `docs/features/<N>_PLAN.md`.

---

## Step 3 — Orchestrator reviews plan

Read the plan yourself. Adjust the plan file directly if needed:

- Ensure the plan matches the user's intent and fix any scope creep or contradictions to the user's description
- Look for any overengineering and opportunities for a simpler or more focused solution
- Ensure that the solution "makes sense" and is the most reasonable approach given the current code and user intent

Keep edits minimal. Do not rewrite the entire plan.

---

## Step 4 — Subagent C: Implement

### Small features (single phase or few files)

Spawn a subagent with the plan path and instruction to implement the **entire** plan.

### Large features (multiple phases)

1. Create `docs/features/<N>_PROGRESS.md` with a checklist of plan phases
2. Spawn subagent(s) per phase:
  - **Sequential** when phases depend on each other (e.g. data layer before UI/API)
  - **Parallel** subagents in one message when phases are independent (e.g. Phase 2A UI + Phase 2B API)

Update `_PROGRESS.md` after each subagent or wave completes. Each implementer gets: plan path, phase scope, exploration brief, and files already touched.

The implementer writes code only; no re-planning, no verify or review workflow. Match existing project conventions and keep scope to the plan.

Wait for all implementers to finish before continuing.

---

## Step 5 — Subagent D: Verify

Spawn a subagent to launch and validate the app:

1. Run lint and tests if the project has them; fix failures before proceeding
2. Start the dev server (`pnpm run dev` or project equivalent) in the background
3. Smoke-test key flows for the feature using built-in browser tooling (navigate, snapshot, exercise critical paths)
4. Fix issues found during verification
5. Return: commands run, pass/fail summary, fixes made, URLs tested

If browser tooling is unavailable, fall back to HTTP health checks and report the gap.

Stop the dev server when done unless the user would expect it running.

---

## Step 6 — Subagent E: Code Review

Spawn another subagent. This agent must **read and follow** the `code-review` skill to create an objective unbiased review. Do not convey "what was implemented" to this subagent. Simply give it the source plan and instruct it to use the code-review skill.

Pass the plan path. E should:

1. Review the implementation against the plan (bugs, data alignment, style, over-engineering)
2. Write `docs/features/<N>_REVIEW.md` documenting findings

This agent's sole responsibility is creating the review.

---

## Step 7 — Make reasonable fixes

Review the code-review output **yourself** and decide what issues are actually critical and require fixes. Then, make the fixes yourself.

Don't go overboard fixing every single thing - focus on the things that need fixing to bring the implementation to meet the user's expectations:

1. Fix issues worth fixing now: correctness bugs, data-alignment issues, and plan deviations
2. Defer large refactors unless critical; note deferred items in the review doc with reasoning
3. Run lint and tests if the project has them; fix failures introduced by the fixes

If fixes are substantial, re-run a lightweight verify pass (lint + targeted browser check).

---

## Step 8 — Final report

Tell the user:

- What was built (1–3 sentences)
- Plan and review doc paths (`<N>_PLAN.md`, `<N>_REVIEW.md`, `<N>_PROGRESS.md` if used)
- Notable deviations from the original description or plan
- Deferred review items and why
- How to run/test the feature locally

---

## Escalation rules

Escalate to the user when:

- Subagent A cannot resolve a blocking ambiguity
- Missing credentials, permissions, or external services
- Plan and feature description fundamentally conflict
- Verify cannot start the app after reasonable fixes
- A subagent fails twice on the same step

After escalation, incorporate the user's answer and resume from the failed step.