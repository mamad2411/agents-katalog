---
name: kill-switches
description: The canonical list of kill switches every [YOUR_FIRM] sales-harness agent checks at the top of every loop tick and immediately before every send. Use when running the Prospector, Composer, or Cadence skills, or any time before drafting/sending outbound — to confirm no global pause, opt-out, send-cap, or reply-rate floor is active.
cowork:
  category: automation
  icon: Flag
---

# Kill Switches

A kill switch is a condition that, when active, **stops an agent from acting**. They are not warnings. They are not soft signals. They are hard stops.

## Files in this skill

- `triggers.md` — the exact triggers and their effects. Read at the top of every agent loop and immediately before every send.

## The rule

Every agent — Prospector, Composer, Cadence — calls into this skill before doing any work, and again before any send. If any trigger is active, the agent reports it, logs to the prospect MD file (or to a global log), and exits cleanly.

## Why this is its own skill, not inside `compliance`

Compliance checks gate content (banned phrases, suppression, CAN-SPAM). Kill switches gate behavior (campaign auto-pause, per-rep send caps, the global pause flag, error-rate thresholds). They look similar but apply at different points: compliance is per-draft, kill switches are per-tick.

Keeping them separate makes it harder to accidentally remove a kill switch when editing compliance, and easier to add new ones without touching compliance.

## Authoring new kill switches

A new trigger goes into `triggers.md`. Every agent already imports this skill, so once the trigger is in the file, all three agents check it.
