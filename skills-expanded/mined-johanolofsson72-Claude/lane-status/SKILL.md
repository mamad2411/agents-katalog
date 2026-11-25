---
name: lane-status
description: "Is there anything for me to do on this project? Answers from the register's own state — your row, the other developer's row, what is unclaimed and runnable, what is held and why, which open questions hold a row, and who committed what this week. Triggers: anything for me to do, what should I work on, what should I do today, what is the other developer doing, where does the project stand, project status, lane status, finns det något för mig att göra, vad ska jag göra."
allowed-tools: Bash, Read, Grep
user-invocable: true
argument-hint: "[--owner NAME]"
---

# Lane status

Answers "is there anything for me to do on this project today?" without anyone having to ask
the other developer. Everything comes from files git already carries between machines.

## How to run it

**1. Run the status script.** It is the only source — never parse the register by hand, and
never guess who owns what:

```bash
bash scripts/lane-status.sh
```

The lane comes from `SPEC_OWNER` in `.claude/settings.local.json` (gitignored, per machine).
If it is unset on a multi-lane project the output says so, and setting it is the first fix —
without a lane there is no way to tell "my row" from "theirs". On a single-lane project the
report still works and simply has no other lane to describe.

**2. If the output says upstream is ahead: pull first, then answer.** An answer computed on a
stale base can hand out a row the other lane already claimed. `git pull --rebase`, re-run.

**3. Read the diagnosis before recommending a row.** A register row is a pointer; the reasoning
is in `specs/INDEX.pending.md` under the same heading. A row that looks small on the register
line can be three pieces of work.

**4. Answer in this order**, as briefly as it can be said:

1. **What to start now** — a recommendation, not a menu. If the developer has a row assigned,
   that is the answer, full stop. If they have none: the top unclaimed row whose dependencies
   are all ticked, with one sentence on why that one.
2. **What is waiting on somebody else** — the other lane's row, and which open questions hold
   an unticked row. That is what the developer should *not* start, and each is worth a line.
3. **What changed since last time** — only if the other lane has committed since this
   developer's own last commit. Otherwise skip it entirely.

## Claiming a row

If you recommend an unclaimed row: set the owner tag in the register (`— @name`, last on the
line), commit, push. The other lane then sees it at its next session start instead of starting
the same thing. A row that already has an owner is not yours to move —
`.claude/rules/spec-register.md`.

Keep the row under 300 bytes. If it is already at the ceiling, the diagnosis moves to
`specs/INDEX.pending.md` before the tag will fit.

## What not to do

- **Do not resolve "which spec is active" yourself.** `scripts/spec_active.py` owns that
  question and it is what the PreToolUse guards enforce. This skill answers a different one:
  what the other lane holds and what is free.
- **Do not read `## Register history` or `INDEX.history.md`.** Audit trail, never input.
- **Do not report a finding only in the chat.** If you find something while answering, it
  belongs in a file — which one is the table in `.claude/rules/lane-handoff.md`.
