---
name: feature-development
description: Implements a feature using plan → implement → verify. Use when the user wants to add a new feature with a clear plan and verification.
---

# Feature Development Framework

This skill runs a **feature development** workflow: plan first, implement, then verify.

## Steps

1. **Plan**
   - Invoke the **planner** subagent with the user’s feature description (or the current conversation context).
   - Capture the output: scope, numbered steps, dependencies, notes. Do not write code yet.

2. **Implement**
   - Implement the steps from the plan. Follow project rules (e.g. `@general-conventions`, `@api-conventions` or `@typescript-patterns` when relevant).
   - If the user asked for “first N steps only,” implement only those and say what’s left for later.
   - Prefer small, incremental changes; run or mention tests where applicable.

3. **Verify**
   - Invoke the **verifier** subagent to confirm:
     - The implementation matches what was planned.
     - Relevant tests pass (or are added and pass).
     - No obvious gaps or regressions.
   - Summarize verification results for the user. If the verifier found issues, address them or list them clearly.

## Notes

- If the user only asked for a plan, stop after step 1 and present the plan.
- If the user says “skip verification,” do steps 1–2 only and say verification was skipped.
