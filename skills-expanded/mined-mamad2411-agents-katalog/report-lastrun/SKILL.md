---
name: report-lastrun
description: "EXPRESS: a plain-language report of the last monitoring run for a NON-TECHNICAL reader — when it ran, a brief overview of what happened, expanding on any important issues or warnings, plus recent-run context. Read-only."
lane: coding
allowed-tools: Read, Glob, Grep, Bash
---

# report-lastrun (Rhetoric / Express)

Answers one question in language a non-technical person can act on: **"What did the
watchman find the last time it checked my machine — and is anything wrong?"** It leads
with *when* the last run happened and a *brief* plain-language overview of what it did,
then **expands on the important issues and warnings** so the reader understands what
needs attention. Strictly read-only — it changes nothing and sends no mail (that is
`send-report`).

This is the body of the `/watchman status` mode and of the `watchman status` launcher.
It is the gentler, more human counterpart to `report-status`: where `report-status`
inventories the whole journal for an operator, `report-lastrun` tells a person what just
happened and what (if anything) they should worry about.

> **PRIME DIRECTIVE (outranks everything below).** Do nothing destructive. If any action
> would delete or overwrite a file or directory, modify a database in any way, sever access
> (firewall/SSH/auth), or stop/remove a service or package — STOP, WARN the operator in plain
> language why it is destructive, and ASK for explicit per-action permission before proceeding.
> In the unattended loop there is no one to ask, so the action does not happen: record it and
> surface it instead. The only non-destructive database operation is routine create-or-update
> through lib/journal.sh. This rule has no exceptions and no mode that overrides it.

## When to use

`/watchman status` (typed live), and `watchman status` from the shell (which launches a
read-only session already running this). On demand only — never part of the loop.

<!-- origin: watchman | version: 1.0 | modifiable: true -->
## Workflow

1. **Preflight.** Run every claude-watchman function through the dispatcher —
   `bash lib/wm <function> [args…]` — which sources the libs under bash internally; never
   `source lib/…` directly (dontAsk refuses a dot-source). Initialize with
   `bash lib/wm journal_init`. Read **only** through `lib/journal.sh` (via `bash lib/wm`);
   never touch `findings.db` directly.

2. **Find the last run.** `bash lib/wm journal_recent_runs 5` returns the most recent runs
   newest-first as `id|kind|started_at|finished_at|summary`. The top row is the last run;
   its `summary` (written by `correlate-findings`: counts of new / regressed / cleared) is
   the account of *what happened that run*. Also call `bash lib/wm schedule_ledger_summary`
   — if headless (cron/systemd) runs exist it reports their most-recent timestamp, count,
   and any errors; if none, it says so (the visible tmux `/loop` shows cost live instead).
   - **No runs recorded yet** (empty `journal_recent_runs` output): say plainly that the
     watchman has not completed a full monitoring pass yet, suggest running `/watchman loop`
     (or `watchman audit`) once, and stop after the overview — there is nothing to expand on.

3. **Brief overview — lead with this.** In two or three short sentences, in plain language:
   - **When** the last run happened — convert the timestamp to a friendly form ("yesterday
     evening", "about 3 hours ago", with the date/time in parentheses). Note whether it was
     an attended loop or a scheduled headless run.
   - **The headline status.** Pull `bash lib/wm journal_count_open` and
     `bash lib/wm journal_count_regressed`. Open with a one-line verdict a non-expert
     grasps instantly — e.g. *"✅ Your system looks healthy — nothing needs your attention."*
     or *"⚠️ A few things need a look — none urgent."* or *"🚨 Something important came back
     and needs attention."* Regressed findings (problems that were fixed but have reappeared)
     are the loudest signal — never bury them.

4. **Expand on the important issues and warnings.** Call `bash lib/wm journal_important_open`
   — it returns the findings worth explaining (everything **regressed**, plus **high/critical**
   severity) WITH their `detail` and `remediation`, regressed first. For each, write a short,
   jargon-free entry:
   - **What it is** — name the problem in everyday words; define any unavoidable technical
     term in the same breath.
   - **Why it matters to them** — the real-world consequence (what an attacker could do, what
     could break, what could be lost), not the mechanism.
   - **What to do** — the suggested fix in plain terms, and **who runs it**: remind the reader
     that applying a fix is done with `watchman fix` (this report is read-only and changes
     nothing). If a finding is `manual` tier, say it needs a person's judgement.
   If `journal_important_open` is empty, say so warmly ("Nothing serious is open right now")
   and give just a one-line count of any low/info items rather than listing them.

5. **Recent-run context (short).** From the `journal_recent_runs` rows, note the trend in a
   sentence — are things getting better (fewer open each run), holding steady, or worsening?
   Mention any scheduled run that errored (from the ledger summary) since a failed headless
   pass means the machine may not have been checked when expected.

6. **Layout for a non-technical reader.** Clear, plainly-titled sections (a "Bottom line"
   first, then "What needs attention", then "Recent history"). Short sentences. No command
   dumps, no raw table output, no severity codes without translation. Friendly but honest —
   do not soften a real warning into vagueness. End with a single "What to do next" line.

7. **Change nothing.** Output text only — suitable for the terminal and for reading aloud to
   someone non-technical. Make no edits, run no fixes, send no mail.
<!-- /origin -->

## Grounding

- `lib/journal.sh` — `journal_recent_runs`, `journal_important_open`, `journal_count_open`,
  `journal_count_regressed` (all read-only, reached via `bash lib/wm <function>`).
- `lib/schedule.sh` — `schedule_ledger_summary` (headless run cost/recency, via `bash lib/wm`).
- `skills/logic/correlate-findings` — writes the per-run `summary` this report reads.
- `report-status` — the fuller, operator-facing journal summary; `send-report` — email.
