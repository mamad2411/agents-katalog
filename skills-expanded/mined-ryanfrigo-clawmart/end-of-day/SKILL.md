---
name: end-of-day
description: An evening wrap — what got done, what slipped, the loose ends, and tomorrow's top 3.
metadata: { "openclaw": { "emoji": "🌙" } }
---

# End of Day

Close the loop on the day. This skill reconciles what actually happened against what the morning brief said mattered, names what slipped and why, flags the loose ends still owed, and sets a clean top-3 for tomorrow — so you log off knowing nothing's lost.

## When to use (trigger phrases)

Use this skill when the user says:

- "wrap up my day" / "end of day" / "what did I get done?"
- "what did I miss today?"
- "set me up for tomorrow"
- Or run it on a schedule each evening (e.g. 18:00 on weekdays).

## How it works

1. **Gather the day's ledger** from the connected tools:
   - **Done** — tasks completed today (`things` logbook / `remindctl` completed, Todoist, Notion).
   - **Open / overdue** — tasks still pending, especially anything due today that didn't close.
   - **Meetings held** — today's calendar events that occurred, and any that likely produced action items.
   - **Loose ends** — emails/messages still needing a reply (reuse `inbox-triage` output if available, else a light scan of the day's unread direct messages).
   - **Tomorrow** — the next day's calendar and anything due tomorrow.
2. **Reconcile against the morning.** If a `daily-brief` ran, compare its "Needs you" list to what got handled. Explicitly mark each as done or carried forward — this is the accountability loop that makes the wrap worth reading.
3. **Compose the wrap** (below): Done → Slipped → Loose ends → Tomorrow. Keep it honest and short; a wrap that flatters is useless.
4. **Set tomorrow's top 3.** Choose by impact, not volume — pull from open/overdue tasks, tomorrow's meetings (and their prep), and today's slipped items. Exactly three. If more scream for attention, name the three and note "+N behind them."
5. **Optionally roll slipped tasks forward** — re-date today's incomplete items to tomorrow — only if the user has set `autoRollForward`; otherwise just list them and ask.
6. **Deliver** via the user's private channel at the scheduled evening time.

## Output

Example wrap:

```
🌙 End of day — Tue Mar 3

✅ DONE (5)
  • Sent Acme the redlined MSA (the day's big one — off your plate)
  • Approved Q3 budget
  • Design review held; decision: ship the new pricing page Thu
  • Unblocked Marcus on the API-key call
  • Shipped the launch checklist (was overdue)

⏳ SLIPPED (2)
  • Board prep — bumped by the Acme conflict; moved to tomorrow 09:00
  • Newsletter draft — didn't start; low urgency, carry forward

📨 LOOSE ENDS (owed replies)
  • Dana (investor) — thank-you + next-step note. Draft's in your inbox.
  • Priya — you said you'd confirm the hiring number by EOD; still open.

🎯 TOMORROW — top 3
  1. Board prep (09:00 meeting — prep first thing)
  2. Confirm the hiring number to Priya (you promised EOD, now overdue)
  3. Investor follow-up to Dana while it's warm
  First meeting: 09:00 Board prep. Then clear till 13:00 — good deep-work window.

Roll the 2 slipped tasks to tomorrow? [y/n]
```

## Notes

- **Requires task + calendar tools**, and benefits from the email/message tools for the loose-ends section. It reports on what those tools expose; it doesn't track work they can't see.
- **Pairs with `daily-brief`.** The reconcile step is far more useful when a morning brief exists to check against — install both for the full open-loop/close-loop cycle.
- **Schedule it** with OpenClaw `cron` for a consistent evening time; a wrap that arrives at a random hour gets ignored.
- **"Top 3" is a judgment call** — bias to what's high-impact or already promised (owed replies and slipped commitments outrank fresh nice-to-haves).
- **Doesn't auto-reschedule** meetings or tasks without opt-in. `autoRollForward` only re-dates *your* incomplete tasks; it never touches other people's calendars.
- **Honest by default.** If little got done, the wrap says so plainly and helps reset — it won't dress up a slow day.
