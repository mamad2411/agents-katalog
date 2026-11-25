---
name: catalyst-tracker
description: "This skill should be used when the user asks '最近有什么催化剂', '这周有什么重要事件', '财报什么时候出', or during daily morning checks. Maintains a forward-looking catalyst calendar (earnings, conferences, policy events) linked to the stocks you track, consolidated in a catalysts-calendar.md file."
version: 1.0.0
---

# Catalyst Tracker

Maintains a forward-looking calendar of events that could trigger stock re-pricing.

## When to Use

- During daily research — check what catalysts are approaching
- When building a trade thesis — identify timing
- Periodic self-check — review if the catalyst calendar is up to date

## Catalyst Types

1. **Company-specific**: Earnings reports, product launches, customer wins, management changes
2. **Industry events**: Conferences (GTC, CES, MWC), trade shows, industry data releases
3. **Policy/Regulatory**: Government policy announcements, regulatory changes
4. **Macro**: Interest rate decisions, economic data releases, market sentiment shifts

## Catalyst File

Maintain a consolidated calendar in `catalysts-calendar.md` (in your research notes directory). If you keep a per-stock research-state file, also note each stock's upcoming catalysts there.

```markdown
# 催化剂日历

## 本周 ({date range})
- {date}: {event} → 影响标的: {stocks} | 预期影响: {brief}

## 下周
- ...

## 本月后续
- ...

## 远期 (1-3个月)
- ...
```

## Workflow

### Daily Check (part of a morning routine)
1. Read catalysts-calendar.md
2. Flag any catalyst happening today or tomorrow
3. Surface it in your morning briefing / trade planning

### Weekly Update
1. Search for new upcoming events via WebSearch
2. Remove passed catalysts
3. Add newly discovered catalysts
4. Link each catalyst to the affected stocks in your notes

## Rules

1. **Every catalyst must have a specific date** (or at least month/quarter)
2. **Every catalyst must link to at least one stock** — unlinked events are noise
3. **Assess probability and impact** — not all catalysts are equal
4. **Remove passed catalysts promptly** — stale calendars are worse than no calendar
