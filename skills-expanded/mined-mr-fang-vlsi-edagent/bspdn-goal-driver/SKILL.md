---
name: bspdn-goal-driver
description: Drive BSPDN objective optimization toward target outcomes (about 8% dynamic-power reduction without area/timing regression, or 5%+ frequency uplift with non-worse power/area) using gated experiments and evidence tracking.
---

# BSPDN Goal Driver

## When to use

Use this skill when the user asks to push objective/performance toward explicit PPA goals, not just run exploratory experiments.

## Knowledge And Tool Interaction

1. Read the latest route/STA/PPA evidence and milestone history before proposing the next campaign.
2. If the task needs shared KB/tool lookup before campaign planning, delegate that retrieval step to `eda-context-accessor`.
3. Write every milestone decision back into durable evidence artifacts so later optimization rounds inherit the exact gate history.

## Outputs

1. `bspdn_goal_progress.summary.md`
2. `bspdn_goal_progress.detail.tsv`
3. campaign plan (`goal_campaign_plan.md`)
4. evidence-backed milestone decision note (`M0/M1/.../M4`).

## Hard rules

1. No promotion claim without execution-contract PASS.
2. Goal-B frequency claim must come from period sweep, not WNS proxy alone.
3. Record exact selector/route-hint config for each compared run.

## Operational References

1. Load `references/goal-contract.md` when deciding whether the task is targeting power goal A, frequency goal B, or both.
2. Load `references/milestone-policy.md` when deciding current milestone, promotion readiness, or whether a campaign should advance.
3. Load `references/campaign-workflow.md` when building the goal tracker, selecting testcase tier, or running the gated A/B campaign.
4. Load `references/reporting-policy.md` when deciding whether a user-facing milestone report or PDF summary is justified.
