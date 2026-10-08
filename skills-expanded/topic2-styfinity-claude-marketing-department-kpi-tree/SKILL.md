---
name: kpi-tree
description: Defines the north-star metric, breaks it into 3-5 drivers with owners and leading indicators, specs the one-page weekly dashboard, and names the single metric that matters right now. Use when reporting is a pile of numbers nobody acts on, or when the team cannot agree what winning looks like this quarter.
argument-hint: "[business goal + the numbers you currently track]"
---

# KPI Tree — the numbers that run the week

Most marketing dashboards are graveyards: forty metrics, no decisions. A KPI tree is the opposite — one north star that tracks value delivered, a handful of drivers that multiply into it, and a weekly page that says what to do differently on Monday. If a number cannot change a decision, it does not make the tree.

## Inputs
- The business goal and the numbers currently tracked, with baselines where known: $ARGUMENTS
- From `marketing-brief.md` if present: **Numbers that matter** (current north star and baselines), the offer and price (unit economics hang off them), and the primary channel.

## Do this
1. Pick the north star: the one number that best tracks value delivered to customers AND moves revenue when marketing does its job. Test every candidate against gaming — if the team maxed this number and revenue stayed flat, it is the wrong star. Follower counts and impressions only qualify if the model genuinely monetises attention.
2. Break the north star into 3–5 drivers, as arithmetic where possible — pipeline value = conversations × qualification rate × win rate × average deal, for instance. Arithmetic exposes which driver is actually the constraint.
3. Attach each driver to an activity the team actually runs, and to an owner. A driver nobody owns is a hope.
4. Mark each node leading or lagging, and pair every lagging number with the leading one that predicts it — revenue lags, conversations lead. Leading numbers run the week; lagging numbers judge the month.
5. Spec the weekly one-page dashboard, with the source written down per number. Anything unmeasurable today goes on an instrumentation list, not the dashboard:
   - North-star trend against target.
   - Each driver with this week's number, last week's, and the delta.
   - One experiment readout with its decision.
6. Name the ONE metric that matters right now: the driver furthest from target with the strongest link to money. One, not three — this is the number the week gets organised around. Inside Claude Code, the metrics-architect agent runs the deep version of this pass.
7. Update **Numbers that matter** in `marketing-brief.md` — north star, drivers with owners, baselines date-stamped, and the current one metric.

## Output
The KPI tree (north star, drivers with owners and their leading indicators), the weekly dashboard spec with sources, the instrumentation list, and the one metric that matters right now — saved into `marketing-brief.md`.

## Rules
- Baselines come from real data or get marked UNKNOWN. A tree grown from invented baselines produces confident nonsense.
- Every number on the dashboard must be able to change a Monday decision. If it cannot, cut it.
- Date-stamp every baseline and target. Undated numbers rot into folklore.
- If the one metric is hard to name, the tree is too big. Prune until it is obvious.
- The tree serves the constraint. When the constraint moves, re-run this skill — do not let last quarter's tree run this quarter's week.
