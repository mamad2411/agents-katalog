---
name: calendar-guard
description: Protect the calendar — flag conflicts and back-to-backs, propose reshuffles, and hold focus blocks.
metadata: { "openclaw": { "emoji": "🛡️" } }
---

# Calendar Guard

Your calendar is a budget, not a bulletin board. This skill audits the week ahead, catches the double-bookings and death-march back-to-backs before they happen, and defends real focus time — proposing concrete moves you approve with one word.

## When to use (trigger phrases)

Use this skill when the user says:

- "check my calendar" / "any conflicts this week?"
- "protect my focus time" / "hold some deep-work blocks"
- "is my day too packed?" / "fix my schedule"
- Or run it every morning as part of the `daily-brief`, and on Sunday for the week ahead.

## How it works

1. **Pull the horizon.** Read the next N days (default 7) from the configured calendar tool (`gcalcli agenda`, `icalBuddy eventsFrom:today to:+7`, or Google Calendar). Capture start/end, attendees, accepted/tentative status, and internal-vs-external.
2. **Run the audit** against the user's rules (from config):
   - **Hard conflicts** — any two events that overlap in time.
   - **Back-to-backs** — gap below the buffer (default 10 min) between meetings, especially before an important or external one where the user needs a beat to prep.
   - **Overload days** — more than `maxMeetingHours` (default 5h) booked, or zero unbroken gap ≥ 90 min.
   - **Boundary violations** — anything before working-hours start, during a protected lunch, or after hours.
   - **Unactioned invites** — tentative/unaccepted meetings that need a yes/no.
   - **No focus time** — days with no protected deep-work block.
3. **Prioritize what to keep.** When two things collide, rank by: external commitment > 1:1 with a direct report / manager > small group with a decision > large informational meeting > optional/FYI. The lowest-ranked one is the move/decline candidate.
4. **Propose specific changes** — not "you're busy," but "decline the 15:00 all-hands dry-run; move the Growth sync to Thu 11:00; that opens 14:00–15:30 for Acme prep." Respect fixed anchors (standups, external calls) and never propose moving an external meeting without flagging it as needing the other party's agreement.
5. **Hold focus blocks.** On lighter days, place `focusBlockTarget` (default 1 × 2h) blocks titled `Focus — protected`, scheduled in the user's real peak hours if configured. Creating these can be auto-approved via `autoHoldFocus`; everything else waits for a yes.
6. **Draft the messages** for any reschedule/decline so the user just sends them (hand off to `inbox-triage` conventions for tone).
7. **Report + apply.** Show the audit and the proposed changes; write to the calendar only what the user approves.

## Output

Example audit:

```
Week of Mar 3 — 18 meetings, 22h booked. 1 conflict, 3 back-to-backs, 0 focus blocks.

⚠️ CONFLICT
  Tue 14:00 — "Acme call" (external) ↔ "Board prep" (internal)
  → Keep Acme (external, revenue). Move Board prep to Tue 16:30 (open). Draft sent below.

🔁 BACK-TO-BACK (needs buffer)
  Mon 11:00 design review → 12:00 investor call, no gap.
  → Move investor call to 12:15 (15-min buffer to reset + skim notes).

🥵 OVERLOAD
  Thu — 6.5h of meetings, no gap over 40 min.
  → Suggest declining the 15:00 "roadmap FYI" (optional, recording exists).

🧘 FOCUS TIME
  No deep-work blocks this week.
  → Holding: Wed 09:00–11:00 and Fri 09:00–11:00 "Focus — protected".  [create? y/n]

Proposed writes: 1 move, 1 decline draft, 2 focus blocks. Apply which?
```

## Notes

- **Requires a calendar tool** with read (and, to apply changes, write) access — e.g. `gcalcli` for Google Calendar, `icalBuddy` for macOS Calendar.app (read-only), or another CLI you've wired to OpenClaw. Read-only tools still let it audit and draft; it just can't apply the writes itself.
- **Set your rules** in `openclaw.json.example`: `workingHours`, `bufferMinutes`, `maxMeetingHours`, `lunch`, `focusBlockTarget`, `peakHours`, `vipAttendees`.
- **Timezone matters** for every overlap and boundary check — configure it and confirm events render in the user's zone (watch for all-day and cross-TZ external invites).
- **Never silently moves an external meeting.** Those require the other side to agree; the skill drafts the ask and stops.
- **Only holds/creates on approval** unless `autoHoldFocus` is on, and even then it only *adds* focus blocks — it never deletes or moves existing events without a yes.
