---
name: auto-build
description: Orchestrates three subagents to plan, implement, and review-fix a feature end-to-end. Best fit for building general-purpose features.
---

# Auto Build

You are the **orchestrator**. Do not implement the feature yourself. Instead, spawn three focused subagents, review their output between steps, and keep the workflow moving. Escalate to the user only when requirements are very ambiguous, access is blocked, or the workflow cannot proceed.

Formulate each subagent's Task prompt from the step instructions below, passing prior subagent output and absolute project paths as context.

## Workflow overview

```
Plan (A) → [orchestrator reviews plan]
  → Implement (B) → Review + Fix (C) → Final report
```

Track the feature number `<N>` from `docs/features/<N>_PLAN.md` throughout.

---

## Step 1 — Subagent A: Plan

Spawn a `generalPurpose` subagent. It must **read and follow** the `plan-feature` skill.

Pass the original feature description and instruct it to:

1. Explore the codebase as needed to research relevant files and patterns
2. Resolve ambiguities from code conventions when possible; ask the user **only** if something is genuinely unclear and would materially change the implementation
3. Write `docs/features/<N>_PLAN.md`

Do not implement code. Wait for A to finish before continuing.

If A escalates unanswered questions, ask the user, then re-run or resume A with answers.

---

## Step 2 — Orchestrator reviews plan

Read the plan yourself. Adjust the plan file directly if needed:

- Ensure the plan matches the user's intent and fix any scope creep or contradictions to the user's description
- Look for any overengineering and opportunities for a simpler or more focused solution
- Ensure that the solution "makes sense" and is the most reasonable approach given the current code and user intent

Keep edits minimal. Do not rewrite the entire plan.

---

## Step 3 — Subagent B: Implement

Spawn a subagent with the plan path and instruction to implement the **entire** plan.

The implementer writes code only; no re-planning, no full review workflow. Match existing project conventions and keep scope to the plan.

For large multi-phase plans, you may spawn parallel or sequential implementers per phase, but default to a single implementer unless phases are clearly independent or dependent.

Wait for B to finish before continuing.

---

## Step 4 — Subagent C: Code Review

Spawn another subagent. This agent must **read and follow** the `code-review` skill to create an objective unbiased review. Do not convey "what was implemented" to this subagent. Simply give it the source plan and instruct it to use the code-review skill.

Pass the plan path. C should:

1. Review the implementation against the plan (bugs, data alignment, style, over-engineering)
2. Write `docs/features/<N>_REVIEW.md` documenting findings

This agent's sole responsibility is creating the review.

---

## Step 5 — Make reasonable fixes

Review the code-review output **yourself** and decide what issues are actually critical and require fixes. Then, make the fixes yourself.

Don't go overboard fixing every single thing - focus on the things that need fixing to bring the implementation to meet the user's expectations:

1. Fix issues worth fixing now: correctness bugs, data-alignment issues, and plan deviations
2. Defer large refactors unless critical; note deferred items in the review doc with reasoning
3. Run lint and tests if the project has them; fix failures introduced by the fixes

---

## Step 6 — Final report

Tell the user:

- What was built (1–3 sentences)
- Plan and review doc paths (`<N>_PLAN.md`, `<N>_REVIEW.md`)
- Notable deviations from the original description or plan
- Deferred review items and why
- How to run/test the feature locally

---

## Escalation rules

Escalate to the user when:

- Subagent A cannot resolve a blocking ambiguity
- Missing credentials, permissions, or external services
- Plan and feature description fundamentally conflict
- A subagent fails twice on the same step

After escalation, incorporate the user's answer and resume from the failed step.