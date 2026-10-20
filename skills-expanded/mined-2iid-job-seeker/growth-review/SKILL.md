---
name: growth-review
description: The growth counterpart of /sprint-review — a periodic ritual that reads the funnel metrics, judges the running growth experiments (keep / kill / double-down), logs them, and turns learnings into backlog issues. Trigger words — growth review, growth check, funnel review, growth experiments, marketing review, what's working.
---
# /growth-review — run growth like sprints: hypothesis → measure → decide

**Use when:** periodically after launch (e.g. weekly). **Owner:** `growth-strategist`. Mirrors `/sprint-review`,
but for growth bets instead of build work.

## Procedure
1. **Read the metrics** — the `## Metrics (AARRR)` table in `docs/growth/gtm-plan.md` names, per stage, the
   metric and the **instrument** it is read from. Go to those instruments and read the **current values**; the
   plan holds the definitions, never the numbers. Then name the **weakest stage**.
   If the table has empty Instrument cells, or no numbers can be read, say
   `funnel: unavailable — <which stage, which instrument>` and **do not name a weakest stage**. A weakest stage
   chosen from no data is the vanity metric this playbook's own guardrail forbids.
2. **Judge each running experiment** — against its up-front metric + decision rule: **keep · kill · double-down**.
3. **Log it** — append one block per experiment to `docs/growth/growth-log.md`, shaped by
   `docs/_templates/growth-log.md`: hypothesis → what was done → metric (before → after) → decision → next.
4. **Turn learnings into work — and make the rows the linter accepts.** File each next experiment and each
   product change as a row in `scripts/kanban/issues.csv`. The header has **13 columns** and every one is
   positional; a row that is short, or whose title contains a comma, shifts every later field and silently
   mis-files the sprint. Concretely:
   - fill **all 13** columns in header order — read the header, do not guess it;
   - **no comma in the title** ("Price test — 2 weeks", never "Price test, 2 weeks");
   - `agent` must be an **existing persona** from `agents/README.md` — `growth-strategist` for an experiment,
     `content-marketer` for content, the surface's engineer for a product change;
   - `status` is `backlog`, and `sprint` is the sprint you intend `/next` to pick it up in — **the ACTIVE one
     or the next one**, never a sprint number nobody has opened;
   - `deps` names issue ids that exist, or is empty.

   Then **run the check** — this step is not done until it passes:
   ```bash
   bash scripts/kanban/lint-kanban.sh     # must exit 0
   ```
   **This is what closes the loop.** Rows the linter rejects do not reach the board, and rows filed into a
   sprint `/next` is not reading are invisible to it — in both cases growth has written a document, not work.
5. **Pick the next bet** — one primary experiment for the next period, attacking the weakest funnel stage.

## Guardrails
One metric + one decision rule per experiment, set BEFORE running it. Kill losers fast; don't fall in love with a
channel. Retention issues outrank new-acquisition ideas. No vanity metrics.

## Done when
Countable — the previous wording was satisfied by a verbatim copy of the template with nothing decided and
nothing filed:
- `docs/growth/growth-log.md` gained **exactly one dated block per running experiment**, each with a non-empty
  **Decision** of `keep` / `kill` / `double-down` and the **weakest stage** it attacked.
- `grep -c '<fill:' docs/growth/growth-log.md` prints `0`.
- `bash scripts/kanban/lint-kanban.sh` exits **0** over a backlog carrying **at least one new row per `keep` or
  `double-down`** — or the block states, in one line, why no work follows.
- The next bet is named, and it attacks the weakest stage from step 1 (or step 1 recorded
  `funnel: unavailable` and this says so).
- `/next` can see the new rows: their `sprint` is the ACTIVE sprint or the next one in
  `docs/planning/sprint-plan.md`.
