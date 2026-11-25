---
name: weekly-review
description: Run the founder's weekly business review — pull the week's numbers, compare against the running baseline, surface what changed and what needs a decision. Use when the founder says "weekly review", "how did the week go", "run the numbers", or at the first session of a new week.
---

# Weekly Review

Turns "how did the week go?" into a five-minute, decision-ready briefing. Output is one dated markdown report plus updated pending tasks — not a data dump.

## When to use / when NOT to use

- Use for the recurring weekly check-in, or when the founder asks how the business is doing.
- Do NOT use for deep-dive analysis of one channel (do that as a normal task) or for anything that changes live systems — this skill is read-only.

## Inputs

- Last week's report: the newest `memory/status/weekly-review-*.md` (the baseline).
- The business's number sources, as defined in `memory/RULES.md` §Review — e.g. for Kiln & Co: booking counts from the class system, shop orders, newsletter growth, social reach. Credentials come from the git-ignored credentials folder, read at runtime.
- `memory/status/PENDING-TASKS.md` (open loops to re-check).

## Steps

1. **Load the baseline.** Read the newest previous review. No baseline = say so and create the first one; never invent a comparison.
2. **Pull this week's numbers** from each defined source. Record the number you actually saw, with its source — never an estimate presented as a reading.
3. **Compare and rank.** For each metric: this week, last week, delta. Rank the report by decision-relevance, not by source order — the biggest mover leads.
4. **Sweep the open loops.** Anything in PENDING-TASKS now due, unblocked, or stale gets a line.
5. **Draft the decision list.** At most 3 items phrased as decisions the founder can make in one sentence ("extend early-bird a week: yes/no?").
6. **Verify before reporting:** re-open the written report file; check every number in it against the value pulled in step 2; check the date math on every deadline.

## Output

`memory/status/weekly-review-YYYY-MM-DD.md` — first line date-stamped, then: **TL;DR (3 bullets) → metric table with deltas → open-loop sweep → decision list.** In chat, lead with the TL;DR and the decision list; the file holds the detail.

## Guardrails

- Read-only: no live-system writes, no sends, no schedule changes from inside this skill.
- Numbers without a named source don't go in the report.
- If a number looks implausibly good or bad, say so and check the source twice before reporting it (suspiciously clean results are broken verification until explained).
