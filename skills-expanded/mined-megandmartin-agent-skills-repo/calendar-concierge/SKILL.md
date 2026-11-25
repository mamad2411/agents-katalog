---
name: calendar-concierge
description: Audits a week of calendar for meeting debt — no-agenda invites, default 30-minute-plus blocks, back-to-back chains — and proposes declines or shortens with polite draft messages. Use when the user says "audit my calendar", "protect my focus time", "too many meetings", "clean up my week", or "which meetings can I skip". Don't use for processing what happened in a meeting (use meeting-notes-actions) or a same-morning schedule glance (use morning-brief).
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Productivity, Calendar, Focus-Time]
    related_skills: [email-triage, meeting-notes-actions, morning-brief]
---

# Calendar Concierge

Audits one week of calendar, names the meeting debt out loud, and hands the user ready-to-send decline/shorten messages plus reclaimed focus blocks. The standard: every flagged meeting has a stated reason and a polite draft; the agent never declines, cancels, or edits an event itself without an explicit per-change confirmation.

## When to Use

- "Audit my week", "I have no focus time", "which of these meetings actually need me".
- Sunday/Monday planning: reshape the week before it starts.
- **Not for:** processing what happened *in* a meeting (use `meeting-notes-actions`) or a same-morning schedule glance (use `morning-brief`).

## Quick Reference

| Action | Command / Call |
|---|---|
| Pull the week | Connected calendar tool: list events, Mon–Fri of target week |
| Compute gaps | `python3` stdlib (`datetime`): sort events, find free blocks ≥ 90 min |
| Flag debt | Apply the three debt checks below to every meeting |
| Draft messages | Write decline/shorten drafts inline — drafts only |
| Apply changes | Calendar tool: decline/update — only after explicit "yes" per change |

## Meeting Debt Checks

1. **No agenda** — description empty or contentless ("sync", "catch up") with 3+ attendees.
2. **Default-length** — 30 or 60 min blocks whose stated purpose fits in less (status updates, quick decisions). Propose 15/25/50.
3. **Back-to-back chain** — 3+ consecutive meetings with <15 min between. Propose shortening the middle ones or moving one to async.

Also score each meeting: **Keep** (user is owner/decision-maker), **Shorten**, **Make async** (status could be a message), **Decline** (user is optional and the agenda doesn't need them).

## Procedure

1. **Precheck** — confirm a calendar tool is connected by listing one event. If not, ask the user to paste their week as text and continue in manual mode; never invent a schedule.
2. **Pull** — list Mon–Fri events for the target week (default: current week; next week if run on Fri–Sun). Capture title, start/end, attendee count, organizer, description.
3. **Audit** — run the three debt checks on every meeting; assign Keep / Shorten / Make async / Decline with a one-line reason. Compute total meeting hours and the largest uninterrupted free block per day (python3 `datetime` arithmetic — no mental math on times).
4. **Reclaim** — identify 2–3 concrete focus blocks (≥90 min) that the proposed changes would open, tied to the user's stated priorities if known.
5. **Draft** — for each Decline/Shorten, write a 1–2 sentence polite message (template below). Warm, no fake excuses, offers an alternative (async update, shorter slot, notes afterward).
6. **Deliver** — output the audit table + drafts. State plainly: "Nothing has been changed yet."
7. **Confirm & apply** — user picks changes; restate each ("Decline 'Vendor sync' Thu 14:00 and send this message — confirm?") and apply one at a time via the calendar tool only on explicit yes. Log what was changed.

## Output Template

```
# Calendar Audit — week of {Mon date}

**Load:** {X}h meetings / {Y}h workweek · Largest daily focus block: {list}

| Day/Time | Meeting | Attendees | Debt flags | Verdict | Why |
|---|---|---|---|---|---|

## Proposed changes ({n})
1. {Meeting} → {Decline/Shorten to 25m/Async}
   Draft: "{polite message}"

## Focus time reclaimed if applied: {Z}h
- {Day HH:MM–HH:MM} → suggested use: {priority}

Nothing has been changed yet — tell me which numbers to apply.
```

## Pitfalls

- **Agent declines or edits events during the "audit"** — the audit is strictly read-only. If any write happened before confirmation, report it immediately and offer to re-accept/restore the event.
- **Timezone drift makes back-to-back detection wrong** — normalize every event to the calendar's own timezone before computing gaps in python3; a "gap" that's really an overlap in another TZ produces embarrassing advice.
- **Flagging the user's own recurring 1:1s or their boss's meeting as Decline** — organizer and power dynamics matter. When the user reports to the organizer, cap the verdict at Shorten and say why in the reason column.
- **Recurring events counted once but flagged weekly** — a bad recurring meeting is the highest-value fix. Mark recurrences explicitly ("weekly — saves {X}h/month") so the user sees the compounding win.

## Verification

- [ ] Output matches the template; every meeting in the week appears exactly once with a verdict
- [ ] Meeting-hour math and gap calculations were done with python3 datetime, not estimated
- [ ] Every Decline/Shorten has a polite draft message attached
- [ ] Zero calendar writes before explicit per-change confirmation; applied changes are logged
- [ ] Reclaimed-hours figure equals the sum of the proposed changes
