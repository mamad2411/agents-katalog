---
name: budget-and-stop-condition-audit
description: >-
  Check that an agent loop has ceilings that actually bind — per-target, token
  and action — and that hitting one returns an incomplete result rather than a
  summary of what it managed. Use when reviewing loop termination, retries, or
  an agent that runs unattended.
allowed-tools: Read, Grep, Glob
---

# The ceiling that binds first is the only one that matters

A loop usually has several budgets and only one of them ever fires. Which one
fires, and how early, is the design; the rest are decoration. The second half
matters more: what the loop **returns** when it stops. A run that halts and
reports its partial work as an answer has converted a budget into a quality
problem.

## When to use this

Any agentic loop, particularly one that retries, and any agent that runs on a
schedule with nobody watching.

## Procedure

**1 — Enumerate every ceiling.** Steps, tokens, wall clock, cost, actions,
per-target attempts. For each, where it is checked and what it does on breach.

**2 — Order them by when they bind.** Run a task that consumes all resources
and record which fires first. A per-target ceiling usually binds long before a
token budget, which means the token budget was never the control.

**3 — Test the breach path.** The result must carry an explicit incomplete
flag. Check what a caller does with it: a loop that returns `complete: False`
into a pipeline that ignores the field has the same outcome as no budget.

**4 — Check the ceiling is not resettable by the agent.** A budget the loop can
extend on its own behalf — by starting a sub-task, spawning a child, or
retrying at a new target — is advisory.

**5 — Derive the numbers from observation.** State the p95 of a legitimate run
and set each ceiling above it. A round number either strangles real work or
never fires.

## Example

**Input** — the fixture committed at the top of [`scripts/budget_and_stop_condition_audit.py`](scripts/budget_and_stop_condition_audit.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
steps taken : 6
stopped by  : per_target (reports-db)
complete    : False   <- visible in the output, not silent

ceiling           limit     used
tokens            50000    10800
seconds              60      2.4
actions              20        6
```

The run continues past this. `test_skills.py` executes the script on every
build, **with no model configured** — so what CI proves is that it runs and
refuses legibly, not that it prints these lines. The output above is a recorded
run against a real model, and nothing re-diffs it: a model's answer is not
reproducible, and this repository does not claim otherwise anywhere it can be
checked.

## Output contract

```json
{
  "ceilings": [{"name": "str", "value": 0, "checked_at": "str", "binds_at_step": 0}],
  "first_to_bind": "str",
  "breach": {"returns_incomplete": true, "caller_respects_flag": false},
  "agent_resettable": ["str"],
  "basis": {"p95_legitimate_run": {"steps": 0, "tokens": 0}}
}
```

## Failure modes

- **Listing budgets without ordering them.** Only the first one exists.
- **Returning partial work as an answer.** The flag is the control; the number
  is the trigger.
- **A ceiling the agent can reset by spawning.** Count the whole tree.
