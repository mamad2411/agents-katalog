---
name: channel-picker
description: Scores candidate channels on ICP presence, ability to execute, economics, and speed to signal, then commits to one primary channel plus support and lays out the 90-day plan with kill thresholds agreed up front. Use when marketing is spread across five half-run channels, or when picking where a new offer meets the market.
argument-hint: "[channels in play or under consideration + hours and budget available]"
---

# Channel Picker — one channel, properly, before any second

Channel diversification is where small marketing teams go to die. Every channel has a learning curve, a native content shape, and a feedback delay, and splitting effort across five means mastering none. This skill forces the honest scoring, commits to one primary, and — just as important — writes the not-doing list so the parked channels stop taxing attention.

## Inputs
- Channels currently running or under consideration, plus the real constraints (hours per week, budget, existing assets and skills): $ARGUMENTS
- From `marketing-brief.md` if present: the ICP and the avatar's watering holes (where buyers actually gather), the offer and price point (the economics hang off it), and any current channel numbers.

## Do this
1. Build the candidate list from evidence — the watering holes in the customer research, not the channels the team enjoys or the ones loudest this month. Inside Claude Code, channel-scout can map where buyers gather and channel-strategist can run the scoring.
2. Score each candidate 1–5 on four axes, with a line of reasoning per score:
   - **ICP presence** — are buyers there in buying mode, or just present?
   - **Ability to execute** — do the skills, assets, and hours to do this channel well actually exist in-house?
   - **Economics** — rough acquisition cost at realistic conversion rates against the offer's price, and the payback window.
   - **Speed to signal** — how fast the channel says yes or no. Slow-signal channels are expensive places to learn.
3. Sanity-check the maths on the top two: at this price, how many wins per month must the channel produce to pay back, and is that volume plausible there? Show the working.
4. Commit to one primary channel and at most two support channels. Support means it feeds or compounds the primary — content that arms outbound, for instance — not a second bet running in parallel.
5. Write the not-doing list. Every channel not picked gets named as deliberately parked, with the condition that would reopen it, so it stops leaking hours and guilt.
6. Lay out the 90 days: weeks 1–2 setup and first tests, weeks 3–6 volume and iteration, weeks 7–12 scale or kill. Define the numbers that mean "working" for each phase now — before any spend, not during week six.
7. Update **Channels & funnel** in `marketing-brief.md` with the primary channel and the reasoning behind it.

## Output
The scored channel table, the pick with its reasoning, the not-doing list with reopen conditions, and the 90-day plan with pre-agreed thresholds — the channel decision written into `marketing-brief.md`.

## Rules
- Score from evidence — the brief's watering holes, realistic conversion benchmarks, actual hours available. A channel scored on enthusiasm fails on schedule.
- One primary until it demonstrably works. A second channel is earned by the first one's numbers, never defaulted into.
- "The ICP is on it" is not enough. They must be reachable there in buying mode, at economics the offer can afford.
- Kill thresholds are set before week one. Deciding mid-flight is how dead channels run for a year.
