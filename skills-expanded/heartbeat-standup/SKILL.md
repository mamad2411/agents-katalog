---
name: heartbeat-standup
description: Scheduled daily standup for every Paperclip agent — each weekday evening, post shipped / in-progress / blocked / budget / tomorrow's plan as a formatted comment in the Paperclip ticket UI. Use on the daily standup heartbeat, or when asked to "post my standup", "daily update", "end-of-day report", or "what did you get done today". Don't use for escalating urgent blockers (delegation-protocol, the moment it happens) or budget warnings (budget-guardrails).
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Paperclip Workforce, Blueprint, Standup, Reporting, Heartbeat]
    related_skills: [ceo-operating-doctrine, delegation-protocol, budget-guardrails, researcher-persona, writer-persona]
    blueprint:
      schedule: "0 18 * * 1-5"
      prompt: "Post my daily standup"
---

# Heartbeat Standup

The 6 p.m. weekday ritual for every agent in the org, CEO included. One formatted comment that lets a human skim the whole team in two minutes: what shipped, what's moving, what's stuck, what it cost, what's next. The standard: every line traces to a ticket ID, every number is real, and "blocked" always names who unblocks it.

## When to Use

- The standup heartbeat fires (weekdays 18:00) — this is the default trigger.
- A human or the CEO asks for a daily update or end-of-day report.
- **Not for:** escalating an urgent blocker (do that the moment it happens via `delegation-protocol` — standup only *recaps* it), budget warnings (fire those immediately per `budget-guardrails`), or planning tomorrow's actual work (CEO's `ceo-operating-doctrine` heartbeat does that; your "tomorrow" section is intent, not assignment).

## Role Boundary

- **You own:** an honest, complete standup of your *own* tickets, posted on time in the right place.
- **You escalate:** nothing new via standup — blockers listed here must already have been raised on their tickets. If you discover an unraised blocker while writing the standup, raise it on its ticket first, then list it.
- **You never:** report another agent's work as your own, mark something "shipped" that wasn't accepted per its definition of done, or skip the budget line.

## Quick Reference

| Section | Rule |
|---|---|
| Shipped today | Only tickets accepted/closed today, with ticket IDs. Empty is a valid answer. |
| In progress | Ticket ID + one-line state + % or next milestone. No vague "working on it". |
| Blocked | Ticket ID + what's needed + **who** unblocks it + since when |
| Budget | Spent this month / cap / % — pulled fresh, not remembered |
| Tomorrow | Max 3 items, each tied to a ticket, in priority order |
| Where to post | Your standup thread/ticket in Paperclip so the CEO and humans see it in the ticket UI |

## Procedure

1. **Pull the facts** — list your tickets changed today (closed, commented, state-changed) and fetch fresh budget numbers per `budget-guardrails`. Success: every claim you're about to make has a ticket ID or a number behind it.
2. **Classify** — sort into shipped (accepted today), in progress (open with movement or planned movement), blocked (waiting on someone/something — confirm each blocker was already raised on its ticket; if not, raise it there now).
3. **Check ancestry** — for shipped and tomorrow items, note the project each ticket serves. If a ticket serves nothing, flag it in the standup ("orphan — needs a home or a close") rather than hiding it.
4. **Fill the template exactly** — no section skipped; use "None" rather than omitting. Keep the whole post skimmable: aim under 20 lines, plain markdown that renders in the Paperclip ticket UI (headers, dashes, no tables-in-tables, no images).
5. **Post** — as a comment on your standup ticket/thread. Success: it appears in the ticket UI, timestamped today.
6. **Cross-link** — if your budget is ≥80% or a blocker is >48h old, @-mention the CEO on those specific lines so the standup doubles as a nudge, not a surprise.

## Output Template

```
## Standup — {agent name} — {YYYY-MM-DD}

**Shipped today**
- {T-##} {title} — accepted ({project})
- None

**In progress**
- {T-##} {title} — {state, e.g. "draft v2 with editor, revision due tomorrow"}

**Blocked**
- {T-##} {what's needed} — waiting on {who} since {date}
- None

**Budget:** {spent} / {cap} ({%}) — {ok | ⚠ warning mode | ⛔ hard stop}

**Tomorrow (priority order)**
1. {T-##} {intent}
2. {T-##} {intent}
```

## Pitfalls

- **The optimistic "shipped"** — listing a draft delivered but not yet accepted as shipped; the CEO plans on top of work that bounces back. Recovery: shipped means accepted against the definition of done; move anything else to "In progress" with its true state, and correct yesterday's standup with a follow-up comment if you already misreported.
- **Blocker debut at standup** — a blocker appears in the standup that was never raised on its ticket, losing hours or a whole day. Recovery: raise it on the ticket immediately (with who unblocks it), then reference it in the standup; blockers are raised in real time, recapped at 18:00.
- **Stale budget line** — copying yesterday's number and drifting past 80% unnoticed. Recovery: the budget line must come from a fresh check at post time; if the fresh number crosses a threshold, trigger `budget-guardrails` warning behavior before posting.
- **The essay standup** — 60 lines nobody reads, burying the one blocked item that mattered. Recovery: enforce the template's shape — one line per item, max 3 tomorrow items; details live on the tickets, the standup links to them.

## Verification

- [ ] Posted to the standup thread/ticket, visible in the Paperclip ticket UI, dated today
- [ ] Every item carries a ticket ID; shipped items were actually accepted today
- [ ] Every blocker names who unblocks it and was already raised on its own ticket
- [ ] Budget line is freshly pulled; threshold crossings triggered `budget-guardrails` behavior
- [ ] All five sections present ("None" where empty); post is under ~20 lines
- [ ] CEO @-mentioned on any ≥80% budget or >48h blocker lines
