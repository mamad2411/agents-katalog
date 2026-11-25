---
name: personal-workbench-explorer
description: Explicit-only discovery skill that analyzes the current task context and proposes 3-5 valuable personal or professional workbench ideas, comparing value, usage frequency, build difficulty, data risk, and maintenance cost. Run only when the user explicitly types $personal-workbench-explorer, /personal-workbench-explorer, or names this skill. Never invoke implicitly for general productivity advice, brainstorming, or ordinary workbench questions.
---

# Personal Workbench Explorer

Help the user discover what durable system is worth building. Stay within context actually available in the current task; never claim access to unavailable cross-task history.

## Explore

1. Verify explicit invocation. If invocation is not explicit, do not run this workflow.
2. Read [discovery-workflow.md](references/discovery-workflow.md).
3. Extract repeated activities, recurring friction, handoffs, scattered information, decisions, and data that should persist.
4. Ask at most three high-value questions at a time. Prefer questions that separate candidate directions rather than collect exhaustive specifications.
5. Generate 3-5 distinct candidate workbenches. Avoid cosmetic variants of the same idea.
6. Score each candidate on value, frequency, implementation difficulty, data risk, and maintenance cost. Explain scores in the user's language level.
7. Recommend a direction only when evidence supports it; otherwise identify the next experiment or observation needed.
8. Produce a complete a structured discovery brief using [brief-template.md](references/brief-template.md).
9. Stop after the brief. Do not invoke or simulate `personal-workbench-builder`; tell the user they may explicitly invoke it with the chosen direction.

## Guardrails

- Do not invent job duties, tools, data, or pain points absent from the current task.
- Distinguish observed facts, user statements, and hypotheses.
- Prefer recurring, connected workflows with persistent state over one-off automations or ordinary websites.
- Surface sensitive-data and ongoing-maintenance implications early.
- Keep all candidates unless the user rejects them; ranking is comparison, not silent elimination.


