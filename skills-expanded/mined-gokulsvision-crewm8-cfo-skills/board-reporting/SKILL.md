---
name: board-reporting
description: Prepares board meeting materials including executive summary, financial review, KPI dashboards, variance analysis, strategic commentary, and action tracking. Use when the user mentions board deck preparation, board meeting materials, financial review for the board, or asks about what to present to the board.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, board-reporting, board-deck, executive-summary, variance-analysis]
related_skills: [financial-statement-generation, monthly-close-process, budget-creation-management, forecast-accuracy-tracking]
inputs_required: [financial-statements-from-financial-statement-generation, cash-position-and-runway, budget-vs-actual-comparison, forecast-accuracy-data, department-head-updates, prior-board-minutes, cap-table-and-fundraising-status]
deliverables: [complete-board-deck, executive-summary, supporting-appendix-financials, pre-read-email, post-meeting-minutes-template]
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Board Reporting

Prepare comprehensive board meeting materials. From the financial review to the strategic narrative, produce clear, honest, and decision-ready board decks. Goal: the board leaves the meeting informed, aligned, and knowing exactly how they can help.

## Purpose

Board meetings are the company's most important recurring governance event. Poor board decks — too long, too vague, too optimistic — waste the board's time and erode trust. This skill produces a concise, honest, decision-oriented board package that covers the financial review, KPI dashboards, variance analysis, strategic narrative, and clear asks. The board leaves knowing exactly where the company stands and how they can help.

## When to Use

- "Prepare for the board meeting"
- "Create the board deck"
- "Financial review for the board"
- "Board meeting agenda and materials"
- "Summarize this quarter for the board"
- "What should we present to the board?"

## Inputs Required

- Financial statements from `financial-statement-generation` (P&L, balance sheet, cash flow)
- Cash position and runway
- Budget-vs-actual comparison from `budget-creation-management`
- Forecast accuracy data from `forecast-accuracy-tracking`
- Department head updates (key wins, challenges, hiring progress)
- Prior board meeting minutes and outstanding action items
- Cap table and fundraising status

## Quick Reference

| Slide | Content | Purpose |
|-------|---------|---------|
| Executive Summary | TL;DR: ARR, cash, burn, key wins/challenges, 3 asks | Busy board members read this |
| Financial Review | P&L with % of revenue, budget vs actual, variance | Did we hit plan? |
| KPI Dashboard | ARR growth, NRR, churn, CAC payback, burn multiple | Trends and health signals |
| Cash & Runway | Cash position, burn rate, zero-cash date | How long can we operate? |
| Strategic Deep-Dive | One topic — roadmap, GTM, expansion | Board input needed |
| Forward Look | Priorities, milestones, asks | What's next |

## Procedure

1. Collect data from: `financial-statement-generation`, department heads, and prior meeting materials.
2. Build each slide with clear narratives. Every number should have a "so what?"
3. Draft the executive summary LAST (once you understand the full picture).
4. Circulate the deck 5-7 days before the board meeting.
5. After the meeting: send minutes, action items, and updated materials within 48 hours.

### Slide 1: Executive Summary (1 slide)

The "TL;DR" for the busiest people in the room:

```
Q2 2026 — Executive Summary

ARR: $4.1M (+28% QoQ, +95% YoY)           Cash: $8.2M (20 months runway)
NRR: 112%                                    Burn: $340k/mo (net)
Gross Margin: 81%                            Headcount: 42 (+5 this quarter)

Key Wins:
  - Closed 3 enterprise logos ($200k+ ACV each)
  - Launched v2 platform — 80% adoption in week 1
  - Hired VP Engineering (starting June 1)

Key Challenges:
  - SMB churn ticked up to 3.5% (monitoring)
  - Sales cycle for mid-market stretching from 45 to 60 days

3 Asks of the Board Today:
  1. Approve Q3 budget (+15% investment in S&M)
  2. Intros to Series B leads at [Firm A] and [Firm B]
  3. Feedback on international expansion timing
```

### Slide 2-3: Financial Review

P&L summary (quarterly), with % of revenue:

| ($ in 000s) | Q2 2026 Actual | Q2 2026 Plan | Variance % | Q1 2026 | QoQ % |
|---|---|---|---|---|---|
| Revenue | $1,100 | $1,050 | +5% | $860 | +28% |
| COGS | $209 | $200 | +5% | $168 | +24% |
| Gross Profit | $891 | $850 | +5% | $692 | +29% |
| Gross Margin % | 81% | 81% | — | 80% | +1pp |
| OpEx (total) | $1,245 | $1,200 | +4% | $1,020 | +22% |
| R&D | $498 | $480 | +4% | $420 | +19% |
| S&M | $435 | $420 | +4% | $350 | +24% |
| G&A | $312 | $300 | +4% | $250 | +25% |
| Net Income (Loss) | ($354) | ($350) | −1% | ($328) | +8% |

### Slide 4: Key Metrics Dashboard

| Metric | Current Q | Prior Q | QoQ Trend | Target | Status |
|---|---|---|---|---|---|
| ARR Growth Rate | 28% QoQ | 25% | ↑ | >20% | 🟢 |
| Net Revenue Retention | 112% | 108% | ↑ | >110% | 🟢 |
| Logo Churn (monthly) | 2.5% | 2.0% | ↑ | <2% | 🟡 |
| CAC Payback (months) | 13 | 12 | ↑ | <12 | 🟡 |
| LTV / CAC | 4.5x | 5.0x | ↓ | >3x | 🟢 |
| Gross Margin | 81% | 80% | ↑ | >80% | 🟢 |
| Burn Multiple | 1.6x | 1.4x | ↑ | <1.5x | 🟡 |
| Magic Number | 1.1x | 1.0x | ↑ | >1.0x | 🟢 |
| Rule of 40 | 17 | 20 | ↓ | >40 | 🔴 |

### Slide 5: Cash & Runway

```
Cash Position:
  Start of Q2:  $8,720k
  End of Q2:    $8,200k
  Net Burn Q2:  $520k → ~$173k/month (vs $165k plan)

Runway: 20 months at current burn
Zero Cash Date: March 2028 (no changes)

Cash Waterfall:
  $8,720k → +$3,300k revenue booked − $2,090k OpEx − $310k capex/other − $1,420k working capital = $8,200k
```

### Slide 6-7: Strategic Deep-Dive

One strategic topic per board meeting. Examples:
- Product roadmap review
- Go-to-market strategy
- International expansion plan
- Fundraising strategy
- Competitive landscape shift
- Org structure / key hires

Structure: Context → Options considered → Recommendation → Key decisions needed.

### Slide 8: Headcount & Hiring

| Department | Q1 End | Hired | Departed | Q2 End | Plan |
|---|---|---|---|---|---|
| Engineering | 18 | +3 | −1 | 20 | 20 |
| Product / Design | 5 | +1 | 0 | 6 | 6 |
| Sales | 7 | +2 | 0 | 9 | 9 |
| Marketing | 3 | +1 | 0 | 4 | 4 |
| G&A | 4 | +1 | −1 | 4 | 5 |

### Slide 9: Forward Look & Asks

- Next quarter's priorities (3-5 bullets)
- Key milestones the team is driving toward
- Specific asks of the board (intros, approvals, advice)
- Upcoming key dates (next board meeting, fundraising timeline)

## Output Format

- Complete board deck (Markdown/text format, ready for slide creation)
- Executive summary (can stand alone as an email)
- Supporting appendix: detailed financials, pipeline data, cap table
- Pre-read email introducing the materials
- Post-meeting minutes template

## Done Criteria

The skill is complete when:
1. Executive summary captures the quarter's story in under one page with key metrics, wins, challenges, and 3 clear asks.
2. Financial review shows actual vs plan with variance analysis and explanations.
3. KPI dashboard shows trend direction and status indicators (green/yellow/red).
4. Cash and runway position is clearly stated with zero-cash date.
5. One strategic deep-dive topic is prepared with context, options, and recommendation.
6. Deck is ready to circulate 5-7 days before the board meeting.

## Pitfalls

- **Sugarcoating bad news or burying it in the appendix**: boards lose trust the moment they discover a problem you didn't surface directly. Lead with challenges, then explain the plan.
- **Packing the deck with 50 slides of raw data**: a board deck is a decision-making tool, not a data dump. If a slide doesn't drive a conversation or decision, cut it.
- **Presenting financials without budget/plan comparison**: actuals in isolation are meaningless. Every board member will ask "versus what?" — answer it before they do.
- **Waiting until the night before to send materials**: sending the deck less than 48 hours before the meeting guarantees board members arrive unprepared. Circulate 5-7 days ahead.
- **Failing to follow up on action items**: the best board deck is worthless if action items from the last meeting went unaddressed. Track and report on every commitment made.

### Heuristics

- **Board meetings are for strategy, not status**: send the financial review ahead of time. Spend meeting time on decisions.
- **Bad news first, honestly**: boards can smell spin. Lead with the real challenges.
- **Every slide should have a clear "so what?"**: if you can't explain why a slide matters in one sentence, cut it.
- **Three asks per meeting, max**: more than that and nothing gets done.
- **The CEO presents, the CFO supports**: the board deck reflects the CEO's voice. The CFO ensures the numbers are right and the narrative is consistent.

### Edge Cases

- **Crisis board meetings** (cash crunch, co-founder conflict, major customer loss): shorter deck, focused entirely on the problem, options, and decision needed.
- **First board meeting for a new investor**: include appendices with company history, cap table evolution, and product roadmap. They need context.
- **Board members who don't engage**: if a board member consistently doesn't read materials or contribute, flag to the CEO. Bad board members are worse than no board members.

## Verification

Can you answer "What are the three most important things the board needs to know right now?" in one sentence? Is bad news surfaced early and honestly? Is every slide either driving a decision or providing essential context? If not, the deck isn't ready.

## Example

1. "Prepare the Q2 2026 board deck — financial review, KPI dashboard, cash runway, and three strategic asks."
2. "We're facing a cash crunch and need an emergency board meeting. Build a crisis deck focused on the problem, options, and the urgent decision we need."
3. "A new investor just joined our board. Create supplemental materials covering company history and cap table evolution as appendices to the regular board deck."

## Linked Skills

- Financial statements → `financial-statement-generation`
- Close the books → `monthly-close-process`
- Budget comparison → `budget-creation-management`
- Forecast accuracy context → `forecast-accuracy-tracking`
