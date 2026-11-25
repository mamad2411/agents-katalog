---
name: followup-sequence
description: Generate and schedule a 4-touch follow-up cadence where each touch adds a new reason — and automatically stop the moment the prospect replies.
metadata: { "openclaw": { "emoji": "🔁" } }
---

# Follow-up Sequence

Most replies come after the first email, not on it. This skill builds a disciplined 4-touch cadence where every follow-up adds a *new* angle instead of guilt-tripping — and, critically, stops the instant the prospect replies or opts out.

## When to use (trigger phrases)

Use this skill when the user says:
- "set up follow-ups for <prospect>"
- "queue the cadence" / "sequence this lead"
- "what's my next follow-up to <name>?"
- "schedule 4 touches for <company>"
- (Handoff) right after `cold-open` drafts touch one.

## How it works

1. **Anchor on touch one.** Take the `cold-open` message as touch 1 (day 0). If it hasn't been sent, note that the cadence starts when it is.
2. **Design four touches, each with a distinct angle.** Never "just bumping this to the top of your inbox." Every touch must justify its own existence:
   - **Touch 1 — day 0:** the cold open (the observation + hypothesis + soft ask).
   - **Touch 2 — day +2 or +3:** a *new* angle. A different signal, a specific resource ("we wrote up how a team your size handled this"), or a sharper version of the value hypothesis. Reply in the same email thread.
   - **Touch 3 — day +5 to +7:** proof or a pattern. A concrete example of the outcome (no fabricated logos/case studies — use real ones or a specific mechanism), or a one-line "here's what week one looks like."
   - **Touch 4 — day +10 to +14:** the polite breakup / permission to close. "Sounds like this isn't a now problem — I'll close the loop unless you'd rather I check back next quarter." Breakups often get the highest reply rate because they hand back control.
3. **Respect timing rules.** Send during the prospect's business hours (use their timezone from the research card), skip weekends and obvious holidays, and never send two touches on the same day. Space follow-ups by working days, not calendar days.
4. **Thread correctly.** For email, all follow-ups reply within the same thread (same subject, `Re:`) so the prospect has context. For LinkedIn/DM, keep each touch even shorter.
5. **Register the stop conditions — this is the most important step.** The cadence must cancel all remaining touches on any of:
   - A reply from the prospect (hand off to `reply-triage`).
   - A hard bounce or "no longer at this company."
   - An unsubscribe / "remove me" / "not interested" (also suppress — see Notes).
   A bot that keeps sending after someone replies is the fastest way to burn a domain and a reputation.
6. **Persist the schedule.** Write each scheduled touch to `pipeline-log` with its send date and status (`scheduled` / `sent` / `canceled`). The daily run checks what's due today; that's how "scheduling" actually works without a dedicated sequencer.
7. **Cap the cadence.** Four touches, then stop and mark the prospect `nurture` (recheck in a quarter). Do not invent a fifth, sixth, seventh touch — that's harassment, not persistence.

## Output

The full sequence with dates, angles, and the stop rule. Example:

```
CADENCE — Dana Ruiz @ Acme (starts on send of touch 1)

Touch 1  Day 0    [cold-open]      Angle: hiring signal → ramp gap
Touch 2  Day +3   Tue 9:15a PT     Angle: resource — "AE ramp w/o an SDR"
Touch 3  Day +7   Mon 8:40a PT     Angle: mechanism — what week one looks like
Touch 4  Day +12  Thu 10:00a PT    Angle: breakup — permission to close

STOP on: any reply, bounce, or opt-out → cancel remaining, notify user.
State written to pipeline-log (status: scheduled).

Draft of Touch 2:
  (in-thread reply, no new subject)
  One more thought, Dana — the piece that usually bites new AEs isn't
  the calls, it's the 40 minutes of research before each one...
```

## Notes

- **Scheduling depends on your setup.** OpenClaw doesn't ship a native drip sequencer. This skill schedules by writing dated tasks to `pipeline-log`; a daily agent run (or a cron you configure) sends what's due. If you've connected a real sequencer or CRM, prefer that.
- **Stop-on-reply requires inbox access.** The stop condition only fires if the agent can see replies and bounces. Configure the same inbox the cold opens send from, and let `reply-triage` watch it.
- **Honor opt-outs immediately and permanently.** "Remove me," "unsubscribe," or "stop" must cancel the cadence *and* suppress the contact from all future outreach — same day. This is both basic decency and, in most jurisdictions, the law (CAN-SPAM, GDPR/PECR).
- **No fake urgency or fake proof.** Don't fabricate "only 2 spots left" or case studies that don't exist. The breakup email works because it's honest, not because it's a trick.
- **Volume discipline.** Spreading four touches per prospect over two weeks keeps daily send volume and spam risk manageable. Don't compress the cadence to hit someone five times in three days.
