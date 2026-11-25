---
name: nonprofit-board-packet
description: "Creates board meeting packets with agenda, financial summaries, program updates, and vote items for nonprofit governance."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Nonprofit Board Packet

## When to Use This Skill

Use this skill when you need to:
- Create a board meeting packet with agenda, financials, and program updates
- Prepare vote items and resolutions for board approval
- Build a standard board packet template for recurring meetings
- Present organizational performance data to a nonprofit board of directors

**DO NOT** use this skill for staff meeting agendas, advisory board updates, or investor presentations. This is for formal nonprofit board of directors governance packets.

---

## Core Principle

A BOARD PACKET MUST GIVE EVERY DIRECTOR THE INFORMATION THEY NEED TO MAKE INFORMED DECISIONS IN THE MEETING — NOT A MOMENT OF READING TIME SHOULD BE WASTED ON CONTENT THAT DOES NOT DRIVE A DECISION OR REQUIRE BOARD AWARENESS.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Meeting date and time** | "When is the board meeting?" | No default — must be provided |
| **Meeting type** | "Regular quarterly, annual, or special meeting?" | Regular quarterly |
| **Vote items** | "What decisions need board approval at this meeting?" | No votes — information only |
| **Financial period** | "What financial period should the summary cover?" | Previous quarter |
| **Key updates** | "What major program or organizational updates should the board know?" | No default — must be provided |
| **Distribution deadline** | "When should directors receive the packet?" | 7 days before the meeting |

**GATE: Confirm the brief and gather all data before building the packet.**

---

## Phase 2: Structure

### Board Packet Contents

```
1. Cover page — meeting date, time, location, call-in details
2. Agenda — timed agenda with item owners
3. Consent agenda — items for approval without discussion
4. Minutes from previous meeting — for approval
5. Executive Director report — narrative update (1-2 pages)
6. Financial summary — income statement, balance sheet, budget vs. actual
7. Program updates — key metrics and highlights per program
8. Committee reports — updates from active committees
9. Vote items — resolutions requiring board action
10. Appendix — supporting documents referenced in the packet
```

### Agenda Template

```
## Board Meeting Agenda
**Date:** [Date]  **Time:** [Time]  **Location:** [In-person / Zoom link]

| Time | Item | Type | Presenter |
|------|------|------|-----------|
| 0:00 | Call to order and roll call | Procedural | Board Chair |
| 0:05 | Approval of consent agenda | Vote | Board Chair |
| 0:10 | Executive Director report | Information | ED |
| 0:25 | Financial review | Information/Discussion | Treasurer |
| 0:40 | Program updates | Information | Program Director |
| 0:55 | [Vote item 1] | Vote | [Presenter] |
| 1:10 | [Vote item 2] | Vote | [Presenter] |
| 1:20 | Committee reports | Information | Committee Chairs |
| 1:35 | New business | Discussion | Board Chair |
| 1:45 | Adjournment | Procedural | Board Chair |
```

**GATE: Present the agenda for approval before building the full packet.**

---

## Phase 3: Write

### Executive Director Report

```
## Executive Director Report — [Period]

### Highlights
- [Top 3-5 achievements or milestones]

### Challenges
- [Key challenges and how they are being addressed]

### Key Metrics
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| [Metric 1] | [X] | [Y] | On track / Behind / Ahead |

### Looking Ahead
- [Priorities for next quarter]
- [Decisions or support needed from the board]
```

### Financial Summary

```
## Financial Summary — [Period]

### Income Statement (Budget vs. Actual)
| Category | Budget | Actual | Variance |
|----------|--------|--------|----------|
| Revenue | $[X] | $[Y] | +/- $[Z] |
| Expenses | $[X] | $[Y] | +/- $[Z] |
| Net | $[X] | $[Y] | +/- $[Z] |

### Cash Position
- Current cash on hand: $[X]
- Months of operating runway: [X] months
- Restricted funds: $[X]
- Unrestricted funds: $[X]

### Notable Items
- [Any significant variances with explanations]
- [Upcoming large expenses or revenue]
```

### Vote Item Format

```
## Resolution: [Title]
**Background:** [2-3 sentences explaining the context and why this needs board approval]
**Recommendation:** [What the staff or committee recommends]
**Financial impact:** [Cost or revenue implications]
**Motion:** "Resolved, that the Board of Directors approves [specific action]."
**Supporting documents:** [Reference to appendix items]
```

---

## Phase 4: Polish

### 1. Packet Checklist

```
- [ ] Cover page has all meeting logistics (date, time, location, dial-in)
- [ ] Agenda is timed and assigns presenters to each item
- [ ] Previous meeting minutes are included for approval
- [ ] Financial summary matches the reporting period
- [ ] All vote items include background, recommendation, and resolution language
- [ ] Packet is under 20 pages (excluding appendix)
- [ ] Distributed to all directors at least 7 days before the meeting
```

### 2. Consent Agenda Guide

Items appropriate for the consent agenda (approved without discussion):
- Previous meeting minutes
- Routine financial reports
- Committee reports with no action items
- Staff hiring/departures (informational)

Any director can request an item be removed from the consent agenda for discussion.

### 3. Post-Meeting Follow-Up

- Distribute draft minutes within 48 hours
- Send action items to responsible parties with deadlines
- File the approved packet in the organization's records
- Update the board portal with final documents

---

## Example 1: Quarterly Board Meeting Packet

```
Contents: Agenda, consent agenda, ED report, Q3 financials, 3 program updates, 1 vote item (approve annual budget), committee reports from governance and finance
Page count: 15 pages + 8-page appendix
Distribution: Sent via board portal 10 days before meeting
```

## Example 2: Annual Meeting Packet

```
Contents: Agenda, annual financial report, impact summary, board officer elections, strategic plan update, annual budget approval, auditor selection vote
Page count: 22 pages + annual report as appendix
Distribution: Sent 14 days before meeting
```

---

## Anti-Patterns

- **Information overload** — a 50-page packet guarantees that directors will not read it. Stay under 20 pages for the core packet.
- **No advance distribution** — handing out the packet at the meeting means unprepared directors making uninformed decisions.
- **Vague vote items** — "Approve the budget" without the budget attached is not actionable. Include all supporting data.
- **All information, no decisions** — board meetings are for governance decisions. If there is nothing to decide, the meeting may not be necessary.
- **Missing financial context** — numbers without budget comparison or narrative explanation are meaningless to non-financial directors.
- **No action items after the meeting** — decisions without assigned owners and deadlines do not get implemented.

---

## Recovery

- **Financial data is not ready:** Include preliminary figures with a note that final numbers will be distributed before the meeting. Never delay the full packet for one section.
- **No vote items this quarter:** Use the time for strategic discussion. Provide a discussion guide with questions for the board to consider.
- **Board members do not read the packet:** Shorten it. Add an executive summary page at the front with the 5 most important things they need to know.
- **First time creating a board packet:** Start with agenda, financials, and ED report. Add additional sections as the board governance matures.
