---
name: reply-clear
description: Read replies to the Daily Central email and close (or reopen) the ledger items they name, via {{WORKSPACE_ROOT}}/reply_clear.py
---

> **Schedule:** Twice daily, 10:00 AM and 9:00 PM ET
> **Needs:** Gmail, workspace files
> **Helper scripts (yours, not included):** learnings.py, ledger.py, reply_clear.py

# Reply-to-clear — closing items by answering an email

**Schedule:** twice daily, **10:00 AM and 9:00 PM ET** (`America/New_York`).
**Reads:** replies to the "Daily Central" thread in {{YOUR_EMAIL}}.
**Writes:** `CENTRAL-LEDGER.md`, only through `{{WORKSPACE_ROOT}}/reply_clear.py`.

## Why this task exists

Every other way to close an item asks {{USER}} to **go** somewhere — the local
door needs `start-dashboard.bat` running, the cloud door needs a browser. This
one needs only the email already open in front of him. It is the fallback that
survives a dead server, a dead laptop, and a bad week. Treat it as load-bearing.

## The danger, stated plainly

A reply quotes the original email underneath it. That original contains **every
item number** and the literal string `done: 1, 15` in its hint line. Anything
that parses a whole reply body will close every item in that email, every single
morning, silently.

`{{WORKSPACE_ROOT}}/reply_clear.py` is built to make that impossible and is tested against real
Daily Central bodies in five quoting styles. **So do not parse the reply
yourself. Do not extract numbers yourself. Do not "help" by reading the body and
deciding what he meant.** Hand the raw body to the script and use what it returns.

---

## Step 0 — Durable learnings

```
cd /d "{{WORKSPACE_ROOT}}"
py {{WORKSPACE_ROOT}}/learnings.py list --skill reply-clear
py {{WORKSPACE_ROOT}}/learnings.py list --grep ledger
```

Do not read `learnings.jsonl` whole — it exceeds the tool-result token cap and
truncates silently. If a learning contradicts anything below, the learning wins.

## Step 1 — Find unprocessed replies

Gmail search:

```
subject:"Daily Central" newer_than:7d -label:"Spine Processed"
```

For each matching **thread**, the first message is the Daily Central email
itself. **Only messages after the first one are replies.** The original is also
from {{USER}} (he mails himself), so "from:me" does not distinguish them —
position in the thread does.

Skip any message that already carries the `Spine Processed` label. That label is
the only thing preventing an old reply from being re-applied on a later run,
which would re-close an item {{USER}} had deliberately reopened. If the label does
not exist yet, create it.

If there are no unprocessed replies, stop here and report "no replies". That is
the normal outcome most runs. Do not send anything.

## Step 2 — Apply each reply

For each reply, oldest first, write the **raw plain-text body** to a file and run:

```
cd "{{WORKSPACE_ROOT}}"
py {{WORKSPACE_ROOT}}/reply_clear.py apply --file reply.txt --json
```

Use `py`, not `python3`. Use the **plaintext** body, not the HTML one.

The script returns JSON with `closed`, `reopened`, `already_closed`,
`already_open`, `unknown`, `bare_numbers`, `ambiguous`, `refused`, and the new
`open`/`archived` counts. It is idempotent — re-running the same reply closes
nothing the second time.

**If it fails: retry exactly once.** If the second attempt also fails, do not
label the message processed (so the next run retries it), record the failure, and
continue to Step 4 with a failed heartbeat.

## Step 3 — Label, and answer only when he needs an answer

After a reply is applied, add the `Spine Processed` label to that message.

Then decide whether to reply to the thread:

- **Everything applied cleanly** (only `closed` and/or `reopened`) — **send
  nothing.** The ledger has it, and tomorrow's Daily Central shows the new
  counts. A confirmation email for a thing that worked is noise, and noise is
  what makes him stop reading the 6:55 email.
- **Anything in `refused`, `unknown`, `ambiguous`, or `bare_numbers`** — reply to
  that thread, to **{{YOUR_EMAIL}} only**, with the plain-text output of:

  ```
  py {{WORKSPACE_ROOT}}/reply_clear.py apply --file reply.txt
  ```

  (the human-readable `summarize()` form). Keep it to those lines and nothing
  else. This is the one case where silence would be a lie: he thinks he closed
  something and it did not close.

Never email anyone but {{USER}} from this task. Never send to a client.

## Step 4 — Stamp the heartbeat

```
cd "{{WORKSPACE_ROOT}}"
py {{WORKSPACE_ROOT}}/ledger.py beat reply-clear ok
```

or, if the run failed twice:

```
py {{WORKSPACE_ROOT}}/ledger.py beat reply-clear fail
```

One failure stays silent by design — that is the retry absorbing a blip. Two
consecutive failures promote it to the health line in the Daily Central email.

## Step 5 — Report

Report: how many replies were processed, what closed, what reopened, anything
refused or unknown, and whether a clarification reply was sent. Keep it short.

---

## Do not

- **Do not parse the reply yourself.** See "The danger" above. This is the single
  most important rule in this file.
- Do not edit `CENTRAL-LEDGER.md` by hand or with your own regex. `{{WORKSPACE_ROOT}}/ledger.py` and
  `{{WORKSPACE_ROOT}}/reply_clear.py` are the only writers.
- Do not act on a reply whose result is `refused`. The refusal means the quote
  boundary probably leaked; closing "just the ones that look right" is exactly
  the guess the refusal exists to prevent.
- Do not process a message that already has the `Spine Processed` label.
- Do not send a confirmation email on a clean run.
- Do not widen the Gmail search beyond the Daily Central subject. A close must
  come from a reply to that email, not from any message that happens to say
  "done".

## Known context

- Item numbers are permanent and never recycled, which is what makes "done: 1,
  15" safe to act on weeks later.
- `MAX_PER_REPLY` is 12. More than that in one reply closes nothing and returns a
  `refused` message — the Daily Central email lists at most 7 items, so a reply
  naming 19 means the parse leaked, not that he had a big day.
- {{USER}} can also write `reopen 17`, `undo 17`, or `oops 17` to move an item
  back to Open. `not done: 17` reads as a reopen, not a close.
- A reopened item is protected from automated re-closing by the `sweep` guard in
  `{{WORKSPACE_ROOT}}/ledger.py`, but **not** from this task — a reply is {{USER}} speaking, and he
  is allowed to change his mind about his own reopen.
