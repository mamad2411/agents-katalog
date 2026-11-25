---
name: tasks-open-loop-weekly-reconciliation
description: Weekly SBDC open-loop sweep against CENTRAL-LEDGER.md — closes what the evidence proves is done, flags what is doubtful, and reports the rest
---

> **Schedule:** Weekly
> **Needs:** Gmail, Google Calendar, {{CRM}}, workspace files
> **Helper scripts (yours, not included):** learnings.py, ledger.py

# Weekly SBDC Open Loop Reconciliation

## Objective

Sweep the open items in `CENTRAL-LEDGER.md` against live Gmail and Calendar,
then **act on what you find**: close the items the evidence proves are done, flag
the ones that are doubtful, and report everything else.

**Scope: SBDC / UMD work only.** Do not touch FNX Pearl, Northfork, or personal
items — the ledger carries all four contexts and only the SBDC ones are yours.

### This task WRITES now. That is the point of it.

It used to be report-only. The 2026-08-19 audit's complaint was exact: *"detects
drift but can't fix it."* A sweep that produces a document {{USER}} has to read and
then act on is a second to-do list, and a second to-do list is the thing this
whole system exists to delete. So this task closes items itself.

Writing carries an obligation the old version did not have: **every close must
carry the evidence that justified it**, in the ledger line, permanently. A close
without recorded evidence is indistinguishable from a guess, and a guess in the
source of truth is worse than no sweep at all.

Wrong closes are recoverable — {{USER}} can uncheck the box in the door or reply
`reopen 14` to the Daily Central email — but only if he notices. Stay well inside
the evidence bar below.

---

## Step 0 — Durable learnings

```
cd /d "{{WORKSPACE_ROOT}}"
py {{WORKSPACE_ROOT}}/learnings.py list --skill tasks-open-loop-weekly-reconciliation
py {{WORKSPACE_ROOT}}/learnings.py list --grep ledger
```

Do not read `learnings.jsonl` whole — it exceeds the tool-result token cap and
truncates silently. If a learning contradicts anything below, the learning wins.

## Step 1 — Read the ledger

```
cd "{{WORKSPACE_ROOT}}"
py {{WORKSPACE_ROOT}}/ledger.py json
```

`CENTRAL-LEDGER.md` is the **source of truth**. `TASKS.md` and the Open Loops
table in `MEMORY.md` are stale snapshots — read them for context if you like, but
never reconcile *to* them and never edit them here.

## Step 2 — Gather evidence

- **Gmail** — `label:"Follow Up"`, plus targeted searches per open item (the
  person's address, the subject). Use the quoted display name; the label-ID form
  (`label:Label_4880014200443597663`) returns zero silently and always has.
  For each item, find the **last** message in the thread and note its direction
  (inbound vs from {{YOUR_EMAIL}}) and age.
- **Google Calendar** — the last 14 days. A session that actually happened is the
  strongest evidence a scheduling loop is closed.

Look back **14 days** for both. Any source that fails twice is survivable: note
it, carry on, and say so in the report.

## Step 3 — Classify every open item into exactly one bucket

**CLOSE** — act on it. Requires a **concrete, nameable artifact**:
- a reply from the other person that answers the open ask, or
- a calendar event that occurred and covers the item, or
- an outbound message from {{USER}} that delivers the thing that was owed, or
- a {{CRM}} postbox BCC confirming the session was logged.

**FLAG** — doubtful, needs {{USER}}. Anything where the evidence is suggestive but
not conclusive, or where the item may have been overtaken by events.

**LEAVE** — still genuinely open, or SBDC-adjacent but not yours to judge.

### Never close on any of these

- "It's old, so it's probably handled." Age is not evidence. The 2026-08-09 sweep
  established that this backlog is a **backlog, not drift** — in every confirmed
  item the last message was inbound and unanswered. Old means owed, not done.
- An OOO auto-reply. Four items already have one and none of them are closed.
- Silence from the other person.
- An outbound message that only *promises* the thing ("I'll send that over").
- Your own inference that {{USER}} "probably" did it offline.

### Hard limits

- **At most 5 closes per run.** If you believe more than 5 are done, close the 5
  best-evidenced, flag the rest, and say so in the report. A sweep that empties
  the ledger in one pass is far more likely to be wrong than right.
- **Never close an item carrying `flag:review`.** Those are waiting on {{USER}}'s
  judgment, not yours. As of this writing: L-015, L-017, L-019, L-025, L-033.
- **Never close an item carrying `reopened:`.** He already overruled a close on
  that item. `{{WORKSPACE_ROOT}}/ledger.py` enforces this for `--via sweep` and will print
  `SKIPPED ... reopened by hand`; do not try to route around it.

## Step 4 — Write

One command per item, through `{{WORKSPACE_ROOT}}/ledger.py`. Never hand-edit the file.

```
cd "{{WORKSPACE_ROOT}}"

py {{WORKSPACE_ROOT}}/ledger.py close L-014 --via sweep --evidence "Max replied 2026-07-28 answering the projections question"

py {{WORKSPACE_ROOT}}/ledger.py flag L-019 --why "Meeting held 8/12 but the deliverable it was about is not mentioned anywhere since"
```

- `--evidence` is **required** on every close. State the artifact and its date.
  "Appears resolved" is not evidence; "replied 2026-08-17 'Yes, I can do both'" is.
- Keep evidence to one line. It is written into the ledger line verbatim.
- Re-running a close is a no-op, so a retried run cannot double-close.

## Step 5 — Stamp the heartbeat

```
py {{WORKSPACE_ROOT}}/ledger.py beat weekly-sweep ok
```

or `py {{WORKSPACE_ROOT}}/ledger.py beat weekly-sweep fail` if the run failed. The health line in the
Daily Central email is driven entirely by these stamps — an unstamped success
looks exactly like a failure, and after two of those it shows up as a problem.

## Step 6 — Report

Save to `outputs/reconciliation-YYYY-MM-DD.md` in the repo, and report the same
summary back in chat.

```
# Weekly SBDC Open Loop Reconciliation — YYYY-MM-DD

## What I changed
| Item | Action | Evidence | New state |
|------|--------|----------|-----------|

## Executive Snapshot
- Closed this run:
- Flagged for your call:
- Still open:
- Highest-risk follow-up:
- Sources unreachable:

## Still Open — oldest first
| Item | Who | Age | Last message direction | Why it is still open |
|------|-----|-----|------------------------|----------------------|

## Flagged for {{USER}}
| Item | Why I did not decide | What would settle it |
|------|---------------------|----------------------|

## Missing — commitments with no ledger item
| Proposed item | Source evidence | Urgency |
|---------------|-----------------|---------|

## Questions for {{USER}}
- [Question] — why it matters
```

**Do not add missing items to the ledger yourself.** Propose them here. Adding is
how a sweep quietly inflates the open count with things {{USER}} never agreed to
own; closing is reversible in one tap, but a wrongly-added item is a new
obligation staring at him every morning.

---

## Do not

- Do not close anything without a named artifact and a date.
- Do not close more than 5 items in one run.
- Do not close a `flag:review` or `reopened:` item.
- Do not edit `CENTRAL-LEDGER.md`, `TASKS.md`, or `MEMORY.md` by hand or with your
  own regex. `{{WORKSPACE_ROOT}}/ledger.py` is the only writer.
- Do not send any email from this task.
- Do not reconcile to `MEMORY.md` or `TASKS.md` — both are stale by design now.
- Use `[not found — confirm]` rather than guessing, and prefer FLAG over CLOSE
  whenever you are weighing whether the evidence is good enough. The asymmetry is
  deliberate: a missed close costs him one tap, a wrong close costs him trust in
  the ledger.
