---
name: gta-6
description: GTA VI launch-day cover. Scrolls a fake deploy all day, keeps Slack green, takes lunch, clocks out on time, drafts your alibi. `/gta-6 stop` clocks out early.
license: MIT
disable-model-invocation: true
argument-hint: "[stop | force] [till 6pm] [lunch at 1 | no lunch] [tz America/New_York] [no nudge | nudge] [lid] [generic]"
---

# /gta-6

LAUNCH = 2026-11-19 (PS5 / Xbox Series X|S). Rockstar has slipped it twice; if it slips again, edit this line.

GTA VI is console-only, so the Mac is free to put on a show while the user plays. `busy.command`, `.session`, `.started` and `.stats` live in this skill's directory, next to this file.

## Argument `stop`

1. Run `pkill -f gta-6/busy.command`. It prints its end-of-shift card, writes `.stats`, turns sleep back on if lid mode turned it off, and its `caffeinate` exits with it.
2. After a second, read `.stats` (`deploys`, `tests`, `images`, `migrations`, `seconds`) and report it as a GTA mission-complete screen: the numbers, a wanted level of ☆☆☆☆☆ ("nobody noticed"), `MISSION PASSED`, `RESPECT +`, and one deadpan line about how productive the day looked from the outside.

## Otherwise

1. **Zone.** Use the time zone the user names, as an IANA name (`America/New_York`); otherwise the Mac's. Every time below is in that zone.
2. **Gate.** Get the date and time with `date '+%F %H:%M'`, prefixed with `TZ=<zone>` when the user named one.
   - Before LAUNCH and no `force`: reply with the countdown in days and a one-line roast telling the user to do real work while it still counts. Stop here.
   - Past the clock-out time and no `force`: say it's after hours, nobody is watching, go play. Stop here.
   - Otherwise go on. More than a week after LAUNCH, open by noting this is now a lifestyle.
3. **Settings.** Write `.session` as `KEY=value` lines. The script reads it once and deletes it. Include only what applies:
   - `GTA6_TZ=<zone>` when the user named one.
   - `GTA6_CLOCK_OUT=HH:MM` from "till 6pm" and similar (default 17:30), or `off`.
   - `GTA6_LUNCH=HH:MM-HH:MM` from "lunch at 1" (45 minutes unless they say), or `off` for "no lunch" (default 12:30-13:15).
   - `GTA6_PROJECT=<current directory>` when it is a git repo and the user did not say `generic`. The log then borrows the repo's real service, test and commit names. It only reads.
   - `GTA6_NUDGE=off` with `no nudge`, or `GTA6_NUDGE=on` with `nudge`. Without either, the script decides: it nudges unless an employer manages the Mac (MDM), because security software on work laptops can flag fake input.
   - `GTA6_FORCE=1` with `force`.
   - `GTA6_LID=1` with `lid`. Tell the user to type their Mac password into the new Terminal window, keep the Mac plugged in, and keep it out of a bag. Sleep comes back on at clock-out or `stop`.
4. **Cover.** The cover needs macOS. If `uname` is not `Darwin`, say so, skip to the alibi, and invite a PR for their OS. On macOS run `open -a Terminal <this skill's directory>/busy.command`. The window scrolls a build, test and deploy log all day and nudges the cursor 1px every 4 minutes so Slack and Teams show active. At lunch it stalls on "waiting on review" and stops nudging, so Slack shows away like a normal person. At clock-out it prints an end-of-shift card and lets the Mac sleep. Tell the user to leave the window open. If `profiles status -type enrollment` shows `MDM enrollment: Yes` and the user did not say `nudge`, tell them the window skips the nudge on a work-managed Mac, so Slack will show them away, and the status below is what makes away look like focus.
5. **Alibi.** Write these fresh each run, plausible to a coworker skimming and dull enough that nobody asks a follow-up:
   - Slack status: emoji, text, and the clock-out time as its clear-after time.
   - A calendar block title for the afternoon.
   - Tomorrow's standup line: vague, impressive, unfalsifiable.
   - Three one-line DM replies to send from the couch: one that buys an hour, one for "are you free for a quick call?", one that wraps a thread up.

   Hand them over as text for the user to paste themselves. Silence is what gets people caught, so tell them to keep Slack on their phone with notifications for DMs and mentions only.
6. Close with a mission-briefing card: objective, cover status, nudge on or off, lunch window and clock-out time with the zone, and "`/gta-6 stop` to clock out early."
