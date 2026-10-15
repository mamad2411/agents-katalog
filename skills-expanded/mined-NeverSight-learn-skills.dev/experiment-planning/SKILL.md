---
name: experiment-planning
description: Use when an approved deep learning experiment design needs a concrete multi-step plan covering code changes, sanity checks, runs, and artifact capture
---

# Experiment Planning

Convert an approved experiment design into an execution plan that another researcher could follow without guessing.

## Output

Save the plan to `docs/experiments/plans/YYYY-MM-DD-<topic>.md`.

## Plan Structure

Start every plan with:

```markdown
# [Topic] Experiment Plan

**Goal:** [What hypothesis this plan tests]

**Baseline:** [Exact run, config, or checkpoint to compare against]

**Primary Metric:** [Metric and selection rule]

**Budget:** [GPUs, wall-clock, run count]

---
```

## Workflow

1. Map the files, configs, scripts, and launch commands involved.
2. Break the work into small steps:
   - code change
   - static or unit check
   - tiny sanity run
   - full run
   - result collection
3. For each step, include exact file paths and exact commands.
4. Define what artifacts must be saved: config, seed, commit, checkpoint, logs, metrics table.
5. Call out rollback criteria and stop conditions.
6. Hand execution to `experiment-execution`.

## Good Planning Rules

- Prefer one hypothesis per plan.
- Keep evaluation fixed unless the plan is specifically about evaluation.
- Include a "small-data / few-step sanity run" before expensive training.
- Separate infrastructure refactors from scientific questions whenever possible.
