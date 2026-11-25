---
name: inbox-zero-sprint
description: Runs a timeboxed 25-minute inbox batch protocol — sort by sender value, apply the 2-minute rule, batch replies as drafts, park and schedule the rest — ending with a hard count report. Use when the user says "inbox zero", "help me clear my inbox", "email sprint", "my inbox is out of control", or wants a focused email session. Don't use for ongoing daily triage rules — use email-triage — or for customer support queues — use customer-support-inbox.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Productivity, Email, Timeboxing, Focus]
    related_skills: [email-triage, customer-support-inbox, calendar-concierge]
---

# Inbox Zero Sprint

A 25-minute, clock-driven assault on an overflowing inbox. Not a filing philosophy — a sprint protocol: sort by who's asking, kill the 2-minute items, batch-draft the real replies, park everything that deserves a scheduled slot, and finish with numbers. The rails: **every reply is a draft the user sends**, nothing is ever deleted, and when the 25 minutes end, the sprint ends — a truthful count beats a fake zero.

## When to Use

- The inbox has piled up (travel, launch week, avoidance) and the user wants one focused session.
- "Email sprint", "let's clear this out", "inbox zero session".
- Recurring use is fine — many users run this as a Friday-afternoon ritual — but each run is its own 25-minute box.
- **Not for:** the standing daily triage pass — use `email-triage`. Not for customer support severity queues — use `customer-support-inbox`. Not a filing/labeling system redesign.

## Quick Reference

| Action | Command / Call |
|---|---|
| Start the clock | `date +%H:%M:%S` — note it; the sprint ends 25 min later, checked at each phase gate |
| Load the inbox | connected email tool: list unread/inbox (read + draft only — no send, no delete) |
| Sender-value tiers | T1 clients & money · T2 team & partners · T3 known humans · T4 machines (newsletters, notifications) |
| Phase budget | Sort 5 min · 2-minute kills 8 min · Batch drafts 8 min · Park + schedule 4 min |
| Park list | `parked-email.md` — thread, why parked, scheduled slot |
| End math | `python3 -c "print({start_count} - {handled} - {parked})"` — must equal what's left |
| 2-minute rule | if a reply takes under 2 minutes to draft, draft it now; the moment it balloons, park it |
| Follow-up sprint | if >15 items remain, propose a second 25-minute slot tomorrow — don't extend today's |

## Procedure

1. **Precheck** — confirm the email tool is connected with draft capability; record the starting unread/inbox count and the start time. Announce the contract: 25 minutes, drafts only, nothing sent, nothing deleted, archive only with the user's OK.
2. **Sort (≤5 min)** — sweep the pile into the four sender-value tiers. T4 machines get bulk treatment immediately: newsletters and notifications are marked-read/archived *as a batch, with one confirmation* ("42 automated messages → archive all? y/n"). Never unsubscribe or delete on the user's behalf.
3. **2-minute kills (≤8 min)** — walk T1→T3 items answerable in under 2 minutes each: one-line confirmations, yes/no answers, quick forwards. Draft each (don't send), mark the thread handled. If an item balloons past 2 minutes, stop mid-thought and move it to the batch pile — the rule is the rule.
4. **Batch drafts (≤8 min)** — the substantial replies, highest sender-value first. Full drafts in the user's voice, saved to the drafts folder with the thread. Anything needing research, a decision, or more than ~5 minutes of writing is not drafted now — it's parked.
5. **Park + schedule (≤4 min)** — every remaining real item goes to `parked-email.md`: thread subject, sender, why parked (needs decision / needs research / waiting-on), and a proposed calendar slot. Offer to create the time blocks via the calendar tool — create events only on explicit confirmation.
6. **Count report** — stop at 25 minutes even if items remain. Compute the arithmetic, deliver the template, and remind the user their only job now: review the drafts folder and hit send.

## Output Template

```
# Inbox Sprint — {date}, {start}–{end} (25:00)

Start: {N} in inbox
├─ 🗑️ Bulk-archived machines: {n} (with your OK)
├─ ⚡ 2-minute drafts: {n}
├─ ✍️ Batch reply drafts: {n}
├─ 📌 Parked + scheduled: {n} → parked-email.md
└─ 📥 Remaining untouched: {n}
Check: {N} − {archived} − {drafted} − {parked} = {remaining} ✓

**Your move:** {n} drafts waiting in the drafts folder — review and send.
**Parked slots proposed:** {slot} for {item} ...
Nothing was sent or deleted during this sprint.
```

## Pitfalls

- **Sprint dissolves into one 25-minute email** — a single T1 thread eats the box. Recovery: the phase gates exist for this; at each `date` check, if a phase is over budget, park the current item mid-draft and advance. Depth goes in the parked slot, not the sprint.
- **Agent sends "obviously safe" replies** — even a one-line "confirmed, see you Tuesday" can be wrong (wrong Tuesday). Recovery: the drafts-only rail has zero exceptions; if a send happened, tell the user immediately and exactly what went out.
- **Bulk archive swallows a human** — a real person's mail sat in a newsletter-looking thread and got archived in the T4 sweep. Recovery: before the bulk action, list sender names, not just the count; anything with a personal name gets pulled out of the batch. Archive is recoverable — which is why delete is never used.
- **Fake zero** — items quietly archived without drafting or parking to make the number pretty. Recovery: the count arithmetic in the report must balance; any item not drafted, parked, or confirm-archived is "remaining", and that's fine.
- **Parked list becomes a graveyard** — parking without a scheduled slot is procrastination with a filename. Recovery: every park entry gets a proposed calendar slot in the same breath; unscheduled parks block the report's "done" line.

## Verification

- [ ] Sprint duration honored: end time − start time ≤ ~25 min, phases gated by real `date` checks
- [ ] Zero sends, zero deletes in the transcript; bulk archive had an explicit user yes with senders listed
- [ ] Count arithmetic balances (python3 check shown in the report)
- [ ] All parked items exist in `parked-email.md` with a proposed slot each
- [ ] Drafts folder holds every drafted reply, matching the report's draft count
- [ ] If items remain, a follow-up sprint slot was proposed rather than silently overrunning
- [ ] Report delivered even though the inbox isn't at literal zero — truthful count over fake zero
