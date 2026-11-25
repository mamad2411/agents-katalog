---
name: daily-brief
description: Assemble a tight morning brief across email, calendar, messages, and tasks — what matters, what's due, what to say no to.
metadata: { "openclaw": { "emoji": "🌅" } }
---

# Daily Brief

A single scannable morning brief that pulls from your inbox, calendar, messages, and task list, then tells you the shape of your day — not a data dump. A busy operator should read it in 60 seconds and know exactly what needs them.

## When to use (trigger phrases)

Use this skill when the user says:

- "give me my morning brief" / "what's my day look like?"
- "daily brief" / "brief me"
- "what do I need to handle today?"
- Or run it automatically on a schedule (see Notes — OpenClaw `cron`).

## How it works

1. **Resolve the window.** "Today" = the user's local day (respect their timezone from config). If run before 6am, include anything since last night's `end-of-day` wrap.
2. **Gather in parallel** from whatever tools are connected:
   - **Calendar** — today's events via the configured calendar tool (`gcalcli agenda`, `icalBuddy eventsToday`, or Google Calendar). Note start times, attendees, join links, and any event with a description that implies prep.
   - **Email** — high-signal unread since last brief. Reuse the `inbox-triage` rubric if that skill is installed; otherwise pull the last ~18h of unread and keep only messages where the user is a direct recipient with an ask or a deadline.
   - **Messages** — unread DMs and @mentions from the message tools you have (`slack`, `imsg`, `discord`). Ignore channel noise; keep direct and mentioned only.
   - **Tasks** — items due today or overdue from the task tool (`things today` + `things upcoming`, `remindctl today` + `remindctl overdue`, Todoist, or Notion).
   - **Optional** — weather / commute if a `weather` tool is configured and the user has an in-person first meeting.
3. **Synthesize, don't dump.** Collapse everything into five short sections (below). The skill's value is judgment: what to surface and what to drop.
4. **Rank "Needs you" ruthlessly.** Cap it at 5 items ordered by impact. Impact ≈ (blocks someone else) > (external/money/legal) > (time-sensitive today) > (owed reply to a VIP). If there are more than 5, keep the top 5 and add a `+N more` line — never pad.
5. **Compute "Say no to."** Flag meetings/asks the user should decline or defer today: optional meetings that collide with a hard deadline, back-to-backs with no prep time before an important call, or new asks that aren't this week's priority. Give a one-line reason each.
6. **Deliver** via the user's preferred channel — reply inline in OpenClaw, or push to a private Slack DM / iMessage thread if configured. Keep the whole thing under ~250 words.

## Output

A structured brief. Example:

```
Good morning. Heavy meeting day (4h booked), one hard conflict at 2pm,
and the Acme contract reply is the thing that actually moves today.

📅 Today
  09:30  1:1 with Priya (30m) — she flagged the hiring plan; skim her doc first
  11:00  Design review (60m)
  14:00  ⚠️ CONFLICT: Acme call ↔ Board prep — both 14:00. Pick one.
  16:00  Investor intro w/ Dana Lee (external) — see meeting-prep one-pager
  Evening clear.

✅ Needs you (4)
  1. Reply to Acme (Sarah) — she's waiting on the redlined MSA to sign this week.
     Draft ready in inbox-triage. → send today
  2. Approve the Q3 budget in email from Finance — blocks the team's spend.
  3. Decide the 2pm conflict: Acme call vs Board prep.
  4. Respond to Marcus (Slack DM) — he's blocked on your API-key decision.

📌 Due today
  - Ship the launch checklist (overdue 1 day)
  - Send Dana the deck before the 4pm

🚫 Say no to
  - "Quick sync?" from Growth (11:30) — collides with design review; offer Thu.
  - Optional all-hands dry-run (15:00) — you have the Acme/Board crunch.

👀 FYI
  - Stripe payout cleared. Newsletter draft is in your read-later.
```

## Notes

- **Depends on the tools you've connected.** The brief is only as complete as the OpenClaw skills you have configured for email, calendar, messages, and tasks (e.g. `himalaya`, a calendar CLI, `slack`/`imsg`, `things`/`remindctl`). Missing a source? The brief simply omits that section rather than guessing.
- **Schedule it.** Wire this to OpenClaw's `cron` tool with a `systemEvent` at, say, 06:45 on weekdays so the brief lands before you're up. The skill itself just assembles; the schedule is yours to set.
- **Timezone is load-bearing.** Set the user's timezone in config; "today" and every time in the brief must render in it.
- **Tune the threshold.** The 5-item "Needs you" cap and what counts as "urgent" are personal — expose a `vipSenders` list and a `maxNeedsYou` in `openclaw.json.example` and honor them.
- **Privacy.** A brief can contain sensitive names, deals, and health items. Deliver only to a private channel the user controls; never a shared room. Draft replies live in `inbox-triage`; this skill points to them but does not send anything.
- **No fabrication.** If a source returns nothing, say "inbox clear" — never invent an item to look busy.
