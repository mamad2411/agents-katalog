---
name: kpi-analysis
description: Turn weekly KPI exports (Excel/CSV) into a trend summary with week-over-week change, vs target, anomaly flags, top movers and manager narrative. Use when the user asks to analyse KPIs, explain weekly metrics, spot anomalies, or write KPI commentary.
---

# Weekly KPI Analysis & Commentary

## Inputs
- CSV/Excel export in long format: week, metric, value, target (optional)
- Wide exports (one column per metric or per week): reshape to long first (see `references/analysis-rules.md`)
- Optional: context notes (peak season, system outage, new customer go-live) to explain movements

Several files: combine into one long table. If two sources give different values for the same metric and week, keep the most recent export and flag the conflict under Needs input.

## Defaults (ask vs assume)
| Setting | Default if not stated | Options |
|---|---|---|
| Period | Latest week in the data vs previous week | Any week; multi-week trend |
| Trailing window | 4 weeks | 3–12 |
| Anomaly thresholds | abs z over 2, or abs WoW over 20% | User thresholds |
| Direction | Higher is better, except metrics named dwell, delay, cost, error, rejection, backlog, TAT | User list |
| Audience | Manager | Manager · Leadership · Ops team |

Ask one question only if direction (higher vs lower is better) is unclear for a metric that is flagged. Otherwise assume and state it.

## Steps
1. Load the data; confirm columns, weeks covered, metrics, and gaps (missing weeks, non-numeric values).
2. Run `python scripts/kpi_summary.py FILE --lower-better m1,m2` (add `--all` for full history). Use its numbers and flags as-is; never compute by hand.
3. Classify each metric: On target · Missed target · Anomaly · Insufficient history, using `references/analysis-rules.md`.
4. Pick top movers from the script output; for each, give the likely driver only if the input or context notes support it, else "Driver: TBD".
5. Write the narrative: 3–5 sentences, outcome first, worst issue next, one ask or action.
6. Fill `templates/kpi-commentary-template.md`. See `templates/example-commentary.md` (fake data, from `templates/sample-kpi.csv`).
7. Run the self-check and fix before returning.

## Format
Use `templates/kpi-commentary-template.md`: Headline, KPI table (from script), Flags & top movers, Narrative, Actions, Data notes.

## Rules
- **Branding only on request:** use plain, neutral formatting by default. Apply a company or brand design skill (colours, fonts, logo, templates) only when the user names that skill or brand in the request; never pick one automatically.
- Never invent values, targets, causes or drivers. Write TBD and list under Needs input.
- Keep metric names, week labels and units exactly as in the input.
- Quote numbers from the script output; round only for the narrative (1 decimal for %).
- Say "better/worse", not just "up/down"; respect metric direction.
- A flag is a prompt to investigate, not a conclusion: write "check" not "caused by" unless evidence is given.
- Narrative ≤ 120 words for Manager, ≤ 60 for Leadership.
- Show "n/a" for missing target or history; never fill with zero.

## Self-check
- [ ] Every number in the narrative matches the script output
- [ ] Direction correct for each metric (lower-better list stated)
- [ ] Every flagged metric appears in Flags with a next step
- [ ] Drivers only from input evidence, otherwise TBD
- [ ] Data gaps and script notes copied into Data notes
- [ ] Narrative within word limit

## Output
Return the commentary from `templates/kpi-commentary-template.md`, then an **Assumptions & Needs input** block (defaults, direction assumptions, missing targets, data gaps, TBD drivers).

After edits to this skill, rerun `evals/test-cases.md`.
