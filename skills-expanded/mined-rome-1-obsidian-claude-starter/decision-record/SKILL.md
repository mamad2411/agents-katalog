---
name: decision-record
description: Records a decision with its context, the options considered, the reason for the choice, and what would make you revisit it, in a project's Decisions.md log or as a standalone decision note; and marks earlier decisions superseded instead of deleting them. Use when the user says "record this decision", "log that we decided X", "write an ADR", "why did we choose X?", "we're changing our mind on X", runs /decision-record, or when a meeting write-up or conversation produces a significant choice worth remembering.
argument-hint: "[the decision, in a sentence]"
---

# Decision record

A decision record exists so that, months later, you (or an agent) can tell why something is the way it is, and whether the reason still holds.

## 1. Pin down the decision

Get, from the conversation or by asking:

- **The decision** in one sentence, stated as what will be done.
- **Context**: what forced the choice now.
- **Options considered**, including "do nothing" when it was a real option, each with its main pro and con.
- **Why this one**: the reason that tipped it. If the user cannot say, record that the reason is unclear rather than inventing one.
- **Revisit if**: the evidence or change that would reopen it.

If the user only gave the decision, ask for the rest in one short message. Do not fill gaps with plausible-sounding reasons.

## 2. Choose where it goes

- The project has a folder: add an entry at the top of `Projects/<Name>/Decisions.md`, under a heading `## YYYY-MM-DD <decision in a few words>`.
- The project is a single file, and the decision is small: a line in its `## Log`.
- The decision is big or cuts across projects: a standalone note from `System/Templates/Decision.md`, in the project folder or in `Projects/`.

## 3. Supersede, never delete

If this replaces an earlier decision:

- Leave the old entry in place.
- Add a line to it: `**Superseded** YYYY-MM-DD by [[...#New heading]]: <one-line reason>`.
- For a standalone note, set `status: superseded` on the old one.

## 4. Link and check

- Link the decision from the project's log, and from the meeting note it came from, if any.
- Set `updated:` on every note you change.
- Run `python3 scripts/check_vault.py` (it checks heading links like `[[Decisions#2026-01-18 ...]]`).
