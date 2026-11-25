---
name: route-by-cost
description: Pick the right model for each job — route bulk and mechanical work to cheap models, exploration to fast mid models, and reserve the strongest model for judgment, taste, and final review. Escalate when the output misses the bar.
---

# Route by cost

Use when orchestrating work across models (subagents, workflow steps,
delegation): decide which model does which job, instead of running everything on
the most expensive one.

## The heuristic

Match each job to the cheapest model that clears the bar:

| Job | Route to |
|---|---|
| Clear-spec implementation, codemods, migrations, data/log analysis | cheapest capable model (a bulk model / Codex) |
| Repo exploration, readers, fact-checks, wiring/config verification | a small fast model |
| Tricky refactors, user-facing code, UI, copy, API design | a strong model |
| Orchestration, synthesis across agents, final review, hard judgment | your best model, used sparingly |

## Principles

- **Spend the scarce (best) model on judgment, not labor.** Its jobs: decide,
  synthesize, review, and the genuinely hard or taste-critical work. Everything
  else delegates down.
- **If you can fully specify the task, it doesn't need the best model.** Write
  the spec, hand it to a cheaper one.
- **Generate cheap, verify smart.** A cheap model produces the diff; a strong
  model reviews it — reviewing costs a fraction of generating.
- **Escalate on quality, not price.** If a cheap model's output misses the bar,
  rerun with a stronger one — don't ship mediocre to save cost. Cost is a
  tie-breaker, not the goal.
- **Anything user-facing** (UI, copy, API shape) must meet the taste bar — don't
  cheap out there.

## Subagents & workflows

- Don't let subagents or workflow steps silently inherit the orchestrator's
  model — pass a model explicitly per job.
- For parallel editing agents, isolate them (separate git worktrees) so their
  edits don't collide.
