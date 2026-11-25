---
name: meeting-booker
description: When a prospect says yes, offer real open times in their timezone, confirm, and drop a calendar hold with an agenda and video link — then log it.
metadata: { "openclaw": { "emoji": "📅" } }
---

# Meeting Booker

The point of everything upstream is a booked call. This skill closes the loop: it reads your actual calendar, offers concrete times in the prospect's timezone, confirms, and creates a clean calendar event — without double-booking you or making the prospect do timezone math.

## When to use (trigger phrases)

Use this skill when the user says:
- "book a call with <name>"
- "they said yes — find a time"
- "offer <prospect> some slots"
- "confirm the meeting with <company> and send the invite"
- (Handoff) when `reply-triage` classifies a reply as interested.

## How it works

1. **Confirm intent before touching the calendar.** Only start when the prospect has actually agreed to meet (from `reply-triage`). Don't push a meeting on a lukewarm "maybe."
2. **Determine the prospect's timezone.** Use the timezone from the research card, or infer from their location; when unsure, ask or offer times in their business hours and label the zone explicitly. Never send a bare "3pm" — always "3:00pm ET."
3. **Read real availability.** Check the user's connected calendar for genuinely open slots. Respect: working hours, a buffer between meetings (default 10–15 min), no back-to-backs if avoidable, and any focus blocks `calendar-guard`-style holds. Don't offer a slot you can't actually keep.
4. **Offer 2–3 specific slots, not a link dump.** Concrete options convert better than "here's my Calendly, pick anything." Propose a sensible duration (25 or 50 min — leave the buffer), spread across two days, in the prospect's timezone. Example: "Does Thu 10:00am or Fri 9:30am ET work? Happy to hold 25 min."
5. **On confirmation, create the event.** Once they pick, create a calendar event with:
   - A clear title: `Acme × <yourco> — intro (25m)`.
   - Both attendees invited.
   - A one-line agenda in the description (why you're meeting, what you'll cover) so it's not a mystery invite.
   - A video link (your configured conferencing default) or a note that you'll dial their number.
6. **Send a short confirmation.** Restate the date/time in *both* timezones, the duration, and the join link. Ask them to accept the invite.
7. **Log it.** Update `pipeline-log`: stage → `meeting booked`, the meeting datetime, and next step (`run meeting-prep` or `show up`).
8. **Handle the edges.** Reschedule requests: re-offer promptly, don't guilt. No-shows: wait ~10 min, send one gracious "missed you — want to grab another time?" and re-offer once. Cancellations: release the hold, mark `nurture` or `closed` per the reason.

## Output

The slot offer, then the confirmation + created event. Example:

```
OFFER (to prospect):
  Great — happy to keep it quick. Does Thursday 10:00am or Friday
  9:30am ET work for 25 minutes? I'll send an invite with a Meet link.

--- after they pick Thursday ---

EVENT CREATED:
  Title:   Acme × Northwind — intro (25m)
  When:    Thu Jul 9, 10:00–10:25am ET  (7:00am PT for you)
  Where:   Google Meet (link in invite)
  Invited: dana@acme.com, you
  Agenda:  Quick intro; where research-heavy outbound is slowing the
           new AEs; whether it's worth a deeper look.

CONFIRMATION (to prospect):
  Sent an invite for Thu Jul 9, 10:00am ET (25 min) with a Meet link —
  accept when you get a sec and I'll see you then.

Pipeline-log: stage engaged → meeting booked; next step "meeting-prep",
  due Wed Jul 8.
```

## Notes

- **Requires calendar read/write access.** Connect Google Calendar (or your provider) in OpenClaw. Without write access, the skill can propose times but you'll create the event manually.
- **Confirm before creating external invites** — at least until you trust it. An event fires emails to the prospect; a wrong time or a double-book is a bad first impression. Have the agent show you the event before sending, or restrict it to holds on your own calendar with a manual send.
- **Configure your conferencing default** (Google Meet, Zoom, phone). If none is set, the agent will say "I'll send a link" and you'll need to add it.
- **Timezone bugs are the classic failure.** Always state both zones in the confirmation; it catches errors before the prospect does. Watch DST transitions.
- **Don't over-automate no-shows.** One polite re-offer is fine; chasing a no-show three times reads as desperation. After one miss with no response, mark `nurture` and move on.
