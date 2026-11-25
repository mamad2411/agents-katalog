---
name: meeting-notes-actions
description: Converts a raw meeting transcript or messy notes file into a locked-format output — decisions, action items with owner and due date, open questions, and a 5-line summary. Use when the user says "process this transcript", "extract action items", "what did we decide", "summarize this meeting", or drops a notes/transcript file. Don't use for deciding whether the meeting should exist (use calendar-concierge) or rolling actions into a weekly log (use weekly-review).
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Productivity, Meetings, Action-Items]
    related_skills: [calendar-concierge, weekly-review, email-triage]
---

# Meeting Notes → Actions

Takes the raw material of a meeting — a transcript, a wall of notes, a pasted chat — and returns exactly four things in a locked template: decisions, action items (owner + due date), open questions, and a 5-line summary. The standard: every action item traces to something actually said, every gap (missing owner, no date) is marked `UNASSIGNED`/`NO DATE` instead of invented.

## When to Use

- "Turn this transcript into action items", "what were the decisions", "process my meeting notes".
- After any recorded call, standup, or workshop where a file or paste exists.
- **Not for:** deciding whether the meeting should exist (use `calendar-concierge`) or rolling actions into a weekly log (use `weekly-review`).

## Quick Reference

| Action | Command / Call |
|---|---|
| Read the source | `read_file` the transcript/notes path (or use pasted text) |
| Size check | `wc -l "notes.txt"` / `wc -w "notes.txt"` |
| Find commitments | `grep -inE "i('|w)ll| will |action|todo|by (mon|tue|wed|thu|fri|next|end of)" "notes.txt"` |
| Find decisions | `grep -inE "decid|agree|we're going with|let's go with|approved" "notes.txt"` |
| Resolve dates | `date -v+3d "+%Y-%m-%d"` (macOS) / `date -d "+3 days" +%F` (Linux) |
| Save output | Write to `<source-name>-actions.md` next to the source (new file — overwrites nothing) |

## Procedure

1. **Precheck** — confirm the source exists and is readable (`wc -w` it). No file and no pasted text? Ask for one; never generate a summary of a meeting you haven't seen. Ask for the meeting date if it isn't in the file (needed to resolve "by Friday").
2. **First pass: decisions** — read fully; grep for decision language as a safety net. A decision is a resolved choice ("we're going with monthly pricing"), not a topic discussed. If it was debated but not closed, it's an open question.
3. **Second pass: actions** — extract every commitment. Each needs owner + task + due date. Owner unnamed → `UNASSIGNED`. No date stated → `NO DATE`. Relative dates ("by Friday") → resolve to ISO dates with `date`, anchored to the meeting date, and keep the original phrase in parentheses.
4. **Third pass: open questions** — unresolved threads, "let's take that offline", explicit parking-lot items.
5. **Summarize** — exactly 5 lines: (1) purpose/context, (2) headline outcome, (3) second key point, (4) main tension or risk, (5) what happens next.
6. **Deliver** — output the locked template below. Do not add, remove, or reorder sections. Offer to save as `<source-name>-actions.md`; write only as a new file, never overwriting the source.

## Output Template

Locked — sections, order, and headings must not change:

```
# {Meeting title} — {YYYY-MM-DD}

## Decisions
- D1: {decision} (context: {one clause})

## Action Items
| # | Owner | Action | Due |
|---|---|---|---|
| A1 | {Name or UNASSIGNED} | {verb-first task} | {YYYY-MM-DD ("by Friday") or NO DATE} |

## Open Questions
- Q1: {question} (raised by {name}, if known)

## Summary
1. {purpose/context}
2. {headline outcome}
3. {second key point}
4. {main tension or risk}
5. {what happens next}
```

Empty section? Keep the heading and write `None recorded.`

## Pitfalls

- **Inventing owners or due dates to make the table look complete** — the worst failure: someone gets chased for a task they never took. `UNASSIGNED` and `NO DATE` are correct outputs; flag them in your closing line as the meeting's follow-up debt.
- **Discussion mistaken for decision** — "we could try X" is not "we decided X." Test: would every attendee agree it was settled? If not, it's an open question.
- **Relative dates anchored to today instead of the meeting date** — a Monday transcript processed Thursday makes "by Wednesday" already wrong. Always anchor `date` math to the meeting date; if unknown, keep only the verbatim phrase and mark `NO DATE (relative: "by Wednesday")`.
- **Transcript too long / auto-captions garbled** — process in chunks and merge; for garbled names use `Speaker A/B` consistently rather than guessing real names. Note the quality caveat above the summary.
- **Summary sprawls past 5 lines** — the lock is the feature. Exactly five numbered lines; trim commentary, not content.

## Verification

- [ ] Output matches the locked template exactly — 4 sections, this order, table columns intact
- [ ] Every action item is traceable to a line in the source (spot-check 2–3 against the transcript)
- [ ] No invented owners or dates; gaps are marked UNASSIGNED / NO DATE
- [ ] Summary is exactly 5 lines
- [ ] Source file untouched; any saved output is a new `-actions.md` file
