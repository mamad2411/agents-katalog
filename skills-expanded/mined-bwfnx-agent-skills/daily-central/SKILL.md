---
name: daily-central
description: Build and send the 6:55 AM ET "Daily Central" email from CENTRAL-LEDGER.md plus today's Calendar and the Gmail Follow Up sweep, then stamp the heartbeat
---

> **Schedule:** 6:55 AM ET "Daily Central" email
> **Needs:** Gmail, Google Calendar, workspace files
> **Helper scripts (yours, not included):** daily_central.py, learnings.py, ledger.py

# Daily Central — the 6:55 AM push

**Schedule:** every day, 6:55 AM ET (`America/New_York`). Seven days, not weekdays.
**Recipient:** {{YOUR_EMAIL}} ({{USER}}, to himself).

> **This task sends email, and that is intentional.** The standing "draft-only, no
> automatic sending" rule in `EXPORT-README.md` exists to protect *clients* from
> an agent emailing them unreviewed. This email goes to {{USER}} and nobody else.
> Never add another recipient. Never send anything to a client from this task.

## The one rule that outranks everything else

**THE EMAIL ALWAYS SENDS.** Quiet day, broken connector, empty ledger, partial
failure — it still goes out, saying what it could and could not do. A push that
silently skips a day teaches {{USER}} to stop looking at it, and once that habit
breaks the whole spine is dead. If you reach Step 5 and are not certain an email
was sent, send a bare one with whatever you have.

---

## Step 0 — Durable learnings (do this first, before any connector)

```
cd /d "{{WORKSPACE_ROOT}}"
py {{WORKSPACE_ROOT}}/learnings.py list --skill daily-central
py {{WORKSPACE_ROOT}}/learnings.py list --grep ledger
```

Do **not** read `learnings.jsonl` whole — it exceeds the tool-result token cap and
truncates silently. Query it. If a learning contradicts anything below, the
learning wins.

## Step 1 — Gather today's live context

Everything in this step is best-effort. **Any failure here is survivable** — note
it and carry on. Do not retry more than once per source.

1. **Google Calendar** — today's events for {{YOUR_EMAIL}}. Keep title, start
   time, location/notes. Skip all-day informational blocks.
2. **Gmail** — `label:"Follow Up"`. Use the quoted display name; the label-ID form
   (`label:Label_4880014200443597663`) returns zero silently and always has.
   For each thread, find the **last** message. Keep it only if that message is
   **inbound** (not from {{YOUR_EMAIL}}) and is **3 or more days old** — that is
   what "the ball is in {{USER}}'s court" means here. Record who, subject, and age
   in days.

Write what you got to `extras.json` in the repo root:

```json
{
  "calendar":  [{"title": "...", "when": "10:15", "note": "..."}],
  "followups": [{"who": "...", "subject": "...", "days": 5}],
  "unreachable": [],
  "door_url": "http://localhost:8765/sbdc-home.html"
}
```

**If a source failed both attempts, add its name to `unreachable`** (e.g.
`["Gmail"]`) and leave that array empty. The email will print "couldn't reach
Gmail today" in the health line, which is the honest outcome and the whole point
of having a health line.

## Step 2 — Build the email

Via the Windows PowerShell MCP tool (`mcp__Windows-MCP__PowerShell`):

```
cd "{{WORKSPACE_ROOT}}"
py {{WORKSPACE_ROOT}}/daily_central.py build --extras extras.json --out daily-central.html
```

Use `py`, not `python3` — `python3` is not on PATH on this machine.

The builder is deterministic and makes no network calls. It owns the selection
rules, the health line, and the rendering; you own only the connector data above.
It prints a JSON summary (subject, counts, health) and writes the HTML body.

**If this command fails: retry it exactly once.** If the second attempt also
fails, skip to Step 5 and send a plain-text email with the subject
`☀️ Daily Central — <Day Mon D>` and a body saying the builder failed and the
ledger could not be read. Do not silently produce nothing.

## Step 3 — Send it

Send via Gmail to **{{YOUR_EMAIL}}** only:

- **Subject:** exactly the `subject` from the builder's JSON. Same shape every
  single day — that consistency is what makes it a recognizable ritual object
  rather than inbox noise. Do not embellish it, do not add counts, do not vary it
  on quiet days.
- **Body:** the HTML from `daily-central.html`.
- **From:** the usual account. Same sender every day.

Send it. Do not create a draft.

## Step 4 — Stamp the heartbeat

Only after a confirmed successful send:

```
cd "{{WORKSPACE_ROOT}}"
py {{WORKSPACE_ROOT}}/daily_central.py sent
```

This writes `daily-central` into the ledger's Heartbeats table with a fresh
timestamp and resets its consecutive-failure counter to 0. **If you skip this,
tomorrow's email will correctly report that Daily Central has not run** — the
health line is driven entirely by these stamps, so an unstamped success looks
exactly like a failure.

If the send itself failed twice, instead run:

```
py {{WORKSPACE_ROOT}}/ledger.py beat daily-central fail
```

Two consecutive failures is what promotes it to the health line. One failure
stays silent by design — that is the auto-retry absorbing a transient blip.

## Step 5 — Report

Report back: whether the email sent, the subject line used, how many items were
selected, the health line, and anything in `unreachable`. Keep it short.

---

## Do not

- Do not edit `CENTRAL-LEDGER.md` by hand or with your own regex. It is parsed and
  written **only** through `{{WORKSPACE_ROOT}}/ledger.py`. Hand-rolled edits are how the line grammar
  drifts and items get silently dropped.
- Do not close, reword, or reorder ledger items. This task **reads** the ledger.
  Closing is the door's job (Phase 3) and the reply-fallback's job (Phase 4).
- Do not skip the send because there is nothing to report. See the rule at the top.
- Do not change the subject format. Ever.
- Do not email anyone except {{YOUR_EMAIL}}.

## Known context

- `CENTRAL-LEDGER.md` lives at the **repo root**, which is deliberately not a
  Netlify publish dir — the four publish dirs are `personal/`, `sbdc-advising/`,
  `northfork-farm/`, `fnx-pearl-consulting/`. It carries client names, so never
  move it into one of those.
- `door_url` currently points at the local dashboard (`start-dashboard.bat` must
  be running for the link to resolve). Phase 3b replaces it with a published
  Artifact URL that works from {{USER}}'s phone. Until then the link is
  desk-only — that is a known, accepted limitation, not a bug to work around.
- The numbers shown next to items (`[1]`, `[15]`) are the ledger's permanent
  item ids. They are never recycled, which is what makes the reply fallback
  ("done: 1, 15") safe.
