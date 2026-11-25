---
name: research-plan-implement
description: Research codebase first, then plan, then implement. Use when the user has an unclear or large task and wants research before planning and implementation.
---

# Research → Plan → Implement

This skill runs a **research-first** workflow for unclear or large tasks: research the codebase and docs, then plan, then implement.

## Steps

1. **Research**
   - Use the **explore** subagent (or main agent) to search the codebase and docs for the user’s goal.
   - Summarize: what exists, current patterns, what’s missing. Answer what the codebase already does and what would need to change.

2. **Plan**
   - Invoke the **planner** subagent with the research summary and the user’s goal.
   - Capture scope, numbered steps, dependencies, and notes. Do not write code yet.

3. **Implement**
   - Execute the plan step by step. Follow project rules (e.g. `@general-conventions`, `@api-conventions` when relevant).
   - If the user asked for “first N steps only,” implement only those and say what’s left for later.

4. **Verify (optional)**
   - Optionally invoke the **verifier** subagent to confirm the implementation matches the plan, tests pass, and nothing obvious is broken.
   - If the user did not ask for verification, you may skip this step and report completion.

## Notes

- If the user only asked for research, stop after step 1 and present the research summary.
- If the user only asked for research and plan, stop after step 2 and present the plan.
- Subagents used: explore (built-in), planner, verifier (optional). Written workflow: [examples/agent-frameworks/research-plan-implement.md](../../../examples/agent-frameworks/research-plan-implement.md).
