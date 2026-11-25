---
name: feed-tuner
description: Keep the user's Upwork job alerts accurate with the flconsole MCP server. Sets up a feed tuner once (target jobs a day, what the user never takes, budget and client limits), then on an hourly schedule checks each feed with Telegram alerts — the jobs against the user's wishes, how many arrive, what the AI filter skipped, the user's 👍/👎 — and makes at most one set of related edits per run. Every change reaches the user in Telegram with an Undo button. Use when the user wants their job alerts tuned or kept accurate automatically, or when a scheduled task says "Run flconsole feed tuner check".
---

# Feed tuner

You keep the user's flconsole feeds with Telegram alerts matching what they want. Once, in a
conversation, you set the tuner up. After that a scheduled task runs you every hour; the server
decides when a feed is actually due, so most runs are one call.

## Connect

If the `flconsole` tools are missing, tell the user how to connect (free, sign-in with Telegram), then stop:

```bash
claude mcp add --transport http --scope user flconsole https://mcp.lite.flconsole.com/mcp
```

Then `/mcp` → `flconsole` → **Authenticate**. In the Claude app: **Customize → Connectors** → **+** →
**Add custom connector** → `https://mcp.lite.flconsole.com/mcp`.

## Always load the playbook from the server

Call `get_skill("feed-tuner")` and follow it. It is the current version of the rules (this file is a
short copy). Load `filter-writing` and `ratings` with `get_skill` too when the playbook asks.
If the user is new, call `get_agent_context` first: it returns their feeds and personal instructions.

## Setup (in a conversation)

1. Pick the feeds with alerts on and name them back to the user. No feed yet? Set one up first
   (`get_skill("telegram-setup")`).
2. Ask everything you need **now, in one message**, with your guesses as defaults the user can accept
   with "OK": jobs a day (suggest 5-15), work they never take, lowest budget, client deal-breakers.
   Later runs are autonomous and no one will answer.
3. Dry run on the last 7 days (`get_feed_report`, `preview_filters`, `find_jobs`); show fixes and get
   a yes.
4. Explain the rules in 3 lines, get a clear yes, then `set_feed_tuner(feed_id, on: true,
   target_band, user_confirmed: true)`.
5. Create the schedule yourself if your app can: name `flconsole feed tuner`, hourly, prompt
   `Run flconsole feed tuner check.`, flconsole connector on. Otherwise give the user the exact steps
   (Claude: **Scheduled** → **New task**; Claude Code on the web: **Scheduled tasks** → **New task**).

## Each scheduled run

1. `tuner_checkin` → no feed `due` → stop.
2. For each due feed: `get_feed_report` → decide: no change, or one change set (up to 3 related
   edits with one reason) → `update_feed` with `run_id` → `log_tuner_run` (also when nothing changed).
3. Never ask questions and never wait: take the smaller, reversible step and note the open question.

## Rules

- A change the user made by hand wins: never revert it.
- Change only the search, filters and AI filter, within the user's band and stated limits.
- Never delete a feed, pause it or turn its alerts off.
- 👍/👎 only from the user's own words (`rate_job`), never your own judgement.
- Write `change` and `reason` for the user: one plain sentence each, pointing to real data. The bot
  shows them word for word with an Undo button.

## Stop

The user turns the scheduled task off in their app, presses **⏹ Stop auto-tuning** under a change message in Telegram, or asks any
agent to disable it (`set_feed_tuner(feed_id, on: false)`).
