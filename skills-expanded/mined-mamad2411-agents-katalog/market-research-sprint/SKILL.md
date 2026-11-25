---
name: market-research-sprint
description: Builds the full market picture in one run — size with the working shown, ranked segments and a beachhead call, trends with timing, channel shortlist, category rules, and whitespace — then writes it into marketing-brief.md. Use when entering a market, picking a beachhead, or replacing hunches with a defensible market view.
argument-hint: "[market or product + the decision this research must drive]"
---

# Market Research Sprint — the whole market picture in one run

Market research fails in two ways: it never gets done, or it becomes a six-week report nobody uses. This sprint does the whole job in one pass — sized, segmented, trend-checked, channel-mapped — with every number graded by confidence, and it ends written into the brief where the rest of the department will actually use it.

## Inputs
- The market or product, and the decision this research must drive: $ARGUMENTS
- From `marketing-brief.md` if present: the business (what is sold, at what price), any existing market numbers to verify rather than redo, and the ICP to anchor segmentation.

## Do this
Inside Claude Code, steps 2–7 can run in parallel via the market-research agents by name — market-sizer, segment-mapper, trend-tracker, channel-scout, category-analyst, whitespace-finder — with research-synthesiser handling step 8. The steps below are the full method either way.

1. Fix the research question. Name the decision this research must drive — enter or skip, which beachhead, how to price, where to distribute. Everything that follows is scoped to that decision.
2. **Size it bottom-up.** TAM, SAM, and SOM built from countable units (number of target businesses × plausible spend), every assumption written out and graded T1 sourced, T2 reasoned estimate, T3 guess. Sanity-check against one top-down source.
3. **Segment and score.** Cut the market two or three ways, score each segment on size, pain intensity, reachability, and willingness to pay, and call the beachhead candidate.
4. **Read the trends.** What is rising and falling — search interest, funding, hiring, community chatter. Separate trend from fad by naming the driver: structural drivers persist, fashionable ones fade.
5. **Map the channels.** Where these buyers already pool — communities, newsletters, events, platforms, voices they trust — with a first read on the cost of reaching them.
6. **Learn the category rules.** Table stakes versus differentiators, how buyers compare options, how mature the category is — worth competing in as-is, or worth reframing.
7. **Find the whitespace.** Cross-reference buyer complaints, gaps in competitor coverage, and emerging segments for ground worth owning.
8. Synthesise into one market brief: keep only decision-relevant findings, keep the confidence grades visible, and write it into **The market** section of `marketing-brief.md` (create the file from the plugin's example if it does not exist).

## Output
The market brief — sized market with the working shown, segment scorecard and beachhead call, three trends with timing windows, channel shortlist, category rules, whitespace list — written into `marketing-brief.md`. End with the three decisions this research should drive and the finding you are least confident in.

## Rules
- Never present a T3 as a finding. A guess wearing a percentage sign is still a guess — grade it and move on.
- Bottom-up beats top-down. A top-down number is a sanity check, never the headline.
- One beachhead. If two segments tie, pick the more reachable one and note the runner-up.
- Findings serve the named decision. Anything that does not move it gets one appendix line, not brief space.
- Date-stamp the section. Market numbers rot — a dated number can be refreshed, an undated one can only be doubted.
