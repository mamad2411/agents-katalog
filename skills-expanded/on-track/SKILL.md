---
name: on-track
description: "Use this skill when the user wants to know whether they are on pace for what they are working toward — each savings goal against its deadline, and financial independence or retirement against their plan — and what to change if they are behind. Use it for 'am I on track', 'will I hit my house deposit', 'when can I retire', 'how far am I from FI', even if they never say 'goal'. Not for whether one purchase fits (can-i-afford-it), not for how the investments performed (investment-checkup)."
---

Check progress toward the user's goals and financial independence. Read-only. Describe
trajectories from their own numbers — never what to buy or sell.

## Gotchas

- get_goals already computes each goal's remaining, months left, required monthly amount and
  pace status. Quote them; do not recompute.
- get_goal_allocation says whether free cash funds every goal at once. A shortfall lands on a
  goal — name which.
- simulate_retirement is the ONE retirement answer (the Outlook's own engine): odds, safe-to-
  retire age, extra saving. get_fire_projection gives only the FIRE number and progress toward
  it (pass get_net_worth's total in current_nw_base) — never quote a second verdict beside the
  simulation. If a figure is missing (age, spending in retirement), ask instead of guessing.
- The FI plan can carry life events and extra income streams (get_plan_baseline). Name them, so
  the user knows what the projection assumes.
- A lever is a re-run with an override, never an estimate.

## Steps

1. Load the tools: get_goals, get_goal_allocation, simulate_retirement, get_fire_projection, get_plan_baseline.
2. **Goals** — get_goals, then get_goal_allocation. Behind or past due first, then ahead, then on
   track; one line each.
3. **Financial independence** — get_net_worth, get_fire_projection, get_plan_baseline: the FI
   number and progress; then simulate_retirement (no arguments) for the odds and the age.
4. **If behind** — one or two levers with real numbers: simulate_retirement with only the lever
   changed (saving or retireAge), naming it as a what-if; for a goal, the monthly amount needed
   against what is set aside now.
5. No goals and no plan yet: say so plainly and offer to set one up with create_goal, and ask before
   creating it.
