---
name: my-taste
description: "My taste (AI-First edition): apply your own design taste when asked about my taste, design feedback, does this look right, a polish pass or a design review. Kept current from your own agent sessions and notes when you say 'update my taste', or by the weekly taste update. Never reads email or chat apps."
---

# My taste

The person's own design taste as short rules, learned from what they typed to their agents and the notes they
keep. It starts empty and grows.

## How to use

Apply the rules below to design work, reviews and polish passes. They're evidence, not law: the current request
wins, and the person's latest word beats anything here. With no rules yet, say so and offer to update.

## Rules

### Design

_No rules yet._

### Look and feel

_No rules yet._

### How I review

_No rules yet._

## Update my taste

When the person says "update my taste", and for the weekly taste update. Read only their own agent sessions on
this computer and notes they point to; never email, chat apps, other people's files or anything online.

1. **Back up:** `node <this skill>/scripts/taste.mjs backup` copies this file into `backups/` here. Stop if it fails.
2. **Collect:** `node <this skill>/scripts/taste.mjs messages --days 7` prints what the person typed, newest
   first and trimmed, without agent briefs, automations or autopilot. Use `--since <date>` for longer.
3. **Find taste:** what they said about how things should look, read, move or work, above all corrections ("too
   busy", "left align it"), approvals and rejections. A rule needs two sightings, or one clear "always" or "never".
4. **Edit the rules** under the right heading, one line each, and change nothing else in this file:
   `- **<The rule, in general words>.** (seen <n> times, last <yyyy-mm-dd>)`. Merge duplicates, and when they
   changed their mind, the latest wins. No quotes, names, links or private details.
5. **Check:** `node <this skill>/scripts/taste.mjs check`. If it fails and you can't fix it,
   `taste.mjs restore` puts the backup back.
6. **Report, every time,** even when nothing changed: `node <this skill>/scripts/taste.mjs report --text "<what
   changed, or nothing new this week>"` adds it to `updates/<yyyy-mm-dd>.md` here. The weekly update also notes
   anything that blocked it there; it never asks questions.
