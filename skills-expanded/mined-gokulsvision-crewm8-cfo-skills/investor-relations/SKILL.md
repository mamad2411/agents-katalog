---
name: investor-relations
description: Manage investor communications — monthly/quarterly updates, board meeting preparation, investor portals, ad-hoc requests, and relationship nurturing. Use when the user asks about drafting an investor update, preparing for a board meeting, responding to investor questions, or managing investor communications.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, fundraising, investor-relations, board-meetings]
related_skills:
  - board-reporting
  - financial-statement-generation
  - fundraising-process-management
  - cash-monitoring
  - cap-table-management
  - data-room-management
inputs_required:
  - investor-and-board-member-list-with-contact-info
  - current-financials-from-financial-statement-generation-and-cash-monitoring
  - key-metrics-ARR-growth-churn-NRR-gross-margin-burn-multiple
  - company-updates-wins-challenges-asks-from-CEO
  - board-meeting-schedule-and-agenda-items
deliverables:
  - monthly-investor-update-email-ready
  - board-meeting-agenda-and-materials-timeline
  - investor-CRM-summary-and-sentiment-tracker
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Investor Relations

Manage ongoing communication with investors and the board — from regular updates to board meeting prep to ad-hoc requests. Goal: investors feel informed, engaged, and ready to help when you need them.

## Purpose

Investors are partners, not just check-writers — but only if they're kept informed. Inconsistent communication erodes trust and makes it harder to get help when you need it. This skill ensures investors receive regular, structured updates, board meetings are productive, and ad-hoc requests are handled promptly, so the company builds a reputation as a transparent, well-run organization.

## When to Use

- "Draft this month's investor update"
- "Prepare for the board meeting"
- "What should we tell investors about [X]?"
- "Create an investor portal / newsletter"
- "Respond to this investor question"
- "Annual shareholder meeting prep"

## Inputs Required

1. **Investor & board member list** — name, firm, contact info, board status, investment amount, relationship notes.
2. **Current financials** — from `financial-statement-generation` and `cash-monitoring`.
3. **Key metrics** — ARR, growth, churn, NRR, gross margin, burn multiple.
4. **Company updates** — wins, challenges, asks, strategic decisions from the CEO/leadership.
5. **Board meeting schedule** — dates, format (virtual/in-person), upcoming agenda items.

## Quick Reference

| Communication Type | Frequency | Format | Audience |
|---|---|---|---|
| Investor update | Monthly | Email (standard template) | All investors |
| Board meeting | Quarterly (or as scheduled) | Deck + meeting | Board members |
| Bad news | Within 48 hours | Email or call | All investors |
| Ad-hoc requests | Within 24 hours acknowledgment | Email or portal | Requester |
| **Best practice** | Consistency beats perfection | Send on fixed cadence | |

## Procedure

### 1. Monthly/Quarterly Investor Update

The standard format that investors actually read:

```
Subject: [Company Name] — April 2026 Update

Hi everyone,

TL;DR: [One sentence summary — the most important thing that happened.]

📈 Metrics (vs last month / last quarter):
- ARR: $1.45M (+15% MoM / +140% YoY)
- Customers: 142 (+12)
- Gross Margin: 79% (flat)
- Net Revenue Retention: 115%
- Cash: $2.8M (24 months runway)
- Burn: $92k (net burn this month)

🎉 Wins:
- Closed Acme Corp ($120k ARR, our largest deal ever)
- Launched AI feature — 40% of customers tried it in week 1
- Hired VP of Sales (ex-Figma)

⚠️ Challenges:
- Churn spiked to 3.2% this month (two SMB bankruptcies — likely not trend)
- Key eng hire declined offer — restarting search
- AWS bill growing faster than revenue — investigating optimization

🙏 Asks (how you can help):
- Intros to: VP Eng candidates, Series A leads at Benchmark/a16z
- Feedback on: new pricing page (link)
- Reference calls with: fintech CTOs for our enterprise deal

📅 Next board meeting: June 12 — materials by June 5

Thanks,
[CEO Name]
```

### 2. Board Meeting Preparation

**2 weeks before:**
- Send calendar invite with proposed agenda.
- Request agenda items from board members.

**1 week before:**
- Circulate board deck (see `board-reporting` skill for full format).
- Include: financial summary, metrics dashboard, strategic topics, voting items.

**Meeting structure (90 minutes):**

| Time | Item | Owner |
|---|---|---|
| 0-5 min | Approve prior minutes, consent agenda | CEO |
| 5-20 min | CEO update — state of the company | CEO |
| 20-35 min | Financial review & KPIs | CFO |
| 35-55 min | Strategic deep-dive (one topic per meeting) | CEO / Lead |
| 55-70 min | Discussion / decisions | All |
| 70-85 min | Forward calendar, action items | CEO |
| 85-90 min | Executive session (board only, no management) | Board |

**48 hours after:**
- Send minutes, action items, and next meeting date.

### 3. Ad-Hoc Investor Requests

When an investor asks for something:
1. Acknowledge within 24 hours (even if you don't have the answer yet).
2. Route to the right skill for data (financials, cap table, metrics).
3. Always provide context, not just raw data. "Here's our ARR trend. The dip in March was seasonality — we saw the same thing last year."
4. Track all outgoing data — investors talk to each other. Be consistent.

### 4. Investor CRM

Maintain a lightweight investor CRM:

| Investor | Firm | Board? | Last Touch | Notes | Warm Intros? |
|---|---|---|---|---|---|
| Sarah Chen | a16z | Yes | Apr 15 (board) | Very helpful on GTM strategy | Yes — portfolio companies |
| Mark Ruiz | XYZ Capital | No | Mar 28 (update) | Introduced us to 2 hires | Yes — SaaS founders |
| ... | ... | ... | ... | ... | ... |

### 5. Bad News Communication

Framework for delivering bad news to investors:
1. **Lead with the news** — don't bury it.
2. **What happened, why, and what we're doing about it.**
3. **Impact on metrics / runway.**
4. **What we need / what's changing.**
5. **Next update.**

Send bad news proactively. Investors hate surprises more than bad news.

## Output Format

- Monthly investor update (email-ready)
- Board meeting agenda and timeline
- Investor contact summary
- Action item tracker from last board meeting
- Investor sentiment / engagement score (crude: who opens, who replies, who's gone silent)

## Done Criteria

The skill is complete when:
1. Investor update is drafted in the standard email-ready format with metrics, wins, challenges, and asks
2. Board meeting preparation timeline is laid out with agenda and material deadlines
3. Ad-hoc investor requests are acknowledged and routed
4. Investor CRM is populated with contact info, last touch date, and relationship notes
5. Bad news communication framework is documented and ready to use

## Pitfalls

- **Sending updates irregularly**: a polished update sent every 3 months is worse than a simple update sent on the 5th of every month. Consistency builds trust.
- **Hiding bad news**: investors hate surprises more than they hate bad news. Bad news delivered within 48 hours gets help. Bad news discovered from another source gets distrust.
- **Asking generic questions**: "Can you help?" gets ignored. "Can you intro us to the CTO at Figma?" gets responses. Every update should have at least one concrete ask.
- **Using board meetings for status updates**: send the status deck ahead of time. Board meeting time should be used for strategic discussion and decisions, not reading slides.
- **Failing to track investor engagement**: some investors go silent after writing the check. Track who's engaged and who's not — don't spend energy chasing ghosts.

## Verification

Can you answer "when was the last update sent to investors and what did it contain?" from the investor CRM? Are upcoming board meeting dates and material deadlines on a timeline? Can bad news be communicated within 48 hours using the documented framework? If not, the investor relations program is incomplete.

## Example

**User prompt**: "Draft this month's investor update."
**What should happen**: Pull current financials and key metrics from linked skills, gather latest company wins/challenges/asks from the CEO, format into the standard investor update template (TL;DR, metrics table, wins, challenges, asks, next board meeting date), and produce an email-ready update.

**User prompt**: "Prepare for the board meeting."
**What should happen**: Build the board meeting timeline (2 weeks before: agenda out, 1 week before: board deck circulated, meeting day: structure per template, 48 hours after: minutes and action items), draft the financial review section of the board deck with metrics dashboard, and compile action items from the prior meeting.

## Linked Skills

- Board deck & financial analysis → `board-reporting`
- Financial statements → `financial-statement-generation`
- Fundraising timeline & strategy → `fundraising-process-management`
- Cash snapshot for updates → `cash-monitoring`
- Cap table for ownership questions → `cap-table-management`
- Data room for document sharing → `data-room-management`
