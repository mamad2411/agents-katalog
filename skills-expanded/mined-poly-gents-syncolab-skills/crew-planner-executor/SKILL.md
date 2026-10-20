---
name: crew-planner-executor
description: "Split long, exploratory work into a planner phase (produce a concrete plan) and an executor phase (carry out the plan), with an explicit checkpoint between the two so the human can intervene cheaply."
---

# Planner / executor split (crewai-inspired)

Long tasks that mix exploration and execution fail differently than each phase alone. Separate them, with a planner that emits a concrete plan and an executor that carries it out.

## When to use

- A research-driven engineering task (figure out the approach, then ship).
- A multi-step automation build (design the flow, then build it).
- An audit-then-act task (find issues, then fix them).

## The phases

### Phase A — Planner

The planner agent:
1. Reads the user goal and constraints.
2. Surveys the existing system (code, docs, dashboards) for the relevant context.
3. Produces a plan with: numbered steps, estimated effort per step, owner per step (could be the same executor or different), and verification per step.
4. Posts the plan to the user (or to the manager under `crew-manager-pattern`) for explicit approval.
5. STOPS. Does not execute.

### Phase B — Executor

The executor (same or different agent):
1. Confirms the plan version they are executing.
2. Carries out each step in order, running `agent-status-pings`.
3. If reality diverges from the plan, STOPS and either updates the plan (small drift) or hands back to the planner (large drift) — never silently improvises a different plan.
4. Runs `production-validation` or `agent-self-check` at the end and reports done.

## The checkpoint

The handoff between A and B is the most valuable point in the loop. It is the cheapest place for the user to redirect work. Make the plan crisp, numbered, and short enough to read in 60 seconds.

## Anti-patterns

- Executor that quietly replans halfway through.
- Planner that never stops — keeps editing the plan after the user approved it.
- Skipping the user-approval step on plans larger than a few hours of work.
