---
name: botkits-routine-healthcheck
description: >-
  Needs Grok Bot. Use when auditing Grok Bot routines for token waste, offering a fleet checkup
  after template import, deciding cadence, or running the standing
  routine-healthcheck wake.
compatibility: Needs Grok Bot (reads Grok Bot routines).
---
# Routine healthcheck

Audit every bot's scheduled and event routines for wasted wakes and noise, then propose fixes. Report only. Don't change another bot's routines until the user picks which fixes to apply.

## When

- The standing `routine-healthcheck` routine fires (default Monday morning).
- First run after import: offer once ("want a checkup of every bot's routines?") and run only on yes.
- The user asks for a routine audit, a token check, or cheaper wakes.
- Before you create a new standing routine.

After the first checkup, offer once to create the weekly `routine-healthcheck` routine if it doesn't exist. Don't re-ask on later runs.

## Collect

1. List every folder in `/home/box/agent-data/agents/`.
2. For each: the bot name from `profile.json`, then every `automations/*/automation.json`.
3. Per routine, note: cron or event, enabled or paused, runs per day (work it out from the cron), and whether the prompt says to stay silent when nothing changed.

## Flag

Each flag names the bot, the routine, the evidence, and a one-line fix.

- **Too often.** Anything denser than hourly (every 15 minutes is 96 wakes a day). Suggest hourly, a few fixed times, or weekday working hours. If it's watching Slack, GitHub, or mail, suggest an event trigger instead of a poll.
- **Talks when it has nothing.** No silence rule, or it sends filler like "(no change)". A message the user can't act on is noise, and noise trains people to ignore the real ones.
- **Heavy host.** A frequent routine on a bot whose chat is already long, so every wake drags that history along. Move it to a fresh, small bot.
- **Dead weight.** Paused for weeks, finished its job (a watch past its end date), or two bots doing the same job.
- **Never acted on.** If the user hasn't responded to or used a routine's output in weeks, propose pausing it.

## Report

One list, worst first: bot, routine, flag, fix, and estimated wakes saved per week. Add a total. No essay. If everything is fine on a scheduled run, say nothing.

Offer to apply fixes only after the user picks. When creating a new bot for a standing sweep, give it one routine at the slowest schedule that still works.

## Inspired by

- [Lauren Tan (@poteto), dr eggbot](https://x.ai/bot/marketplace/bots/dr-eggbot-v2) (marketplace template; no reuse license shown, so no text is copied). Does well: names a weekly token and waste audit that stays quiet and waits for the user to pick. Missing: the listing gives the schedule and intent but no flags, cost estimate, or report shape.
- [Google SRE Book, Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/). Does well: every page should be actionable, noisy alerts get ignored, and rarely used rules should be up for removal. Missing: about production alerting, not agent wakes or token cost.
- [Google SRE Book, Eliminating Toil](https://sre.google/sre-book/eliminating-toil/). Does well: defines repetitive, automatable work with no lasting value. Missing: no audit procedure for scheduled jobs.

## What this version adds

- Wakes-per-day math and a weekly savings total in the report.
- The "actionable or silent" test and a "never acted on" flag, taken from alerting practice.
- Event triggers suggested in place of polling.
