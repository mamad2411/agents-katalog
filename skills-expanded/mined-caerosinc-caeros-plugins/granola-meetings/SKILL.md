---
name: granola-meetings
description: Find, read, and summarize Granola meetings — last meeting, date ranges, meetings with a person, folder views, action-item sweeps, and meeting prep. Use for any "which meetings / what happened / what's outstanding" request once the granola core skill has routed here.
---

# Granola meetings

Recipes over `list_meetings` + `get_meetings` (+ `list_meeting_folders` on
paid plans). Read [granola] first for auth and tool basics.

## Last meeting

1. `list_meetings` for the most recent meetings (narrow by date if the tool
   accepts a range; otherwise take the newest result).
2. `get_meetings` on the top id.
3. Answer from summarized notes; mention attendees and date so the user can
   confirm it is the meeting they meant. Offer the transcript (paid) if they
   want exact wording.

## Meetings in a window ("this week", "yesterday", "July")

1. Resolve the user's phrase to concrete dates in their timezone first.
2. `list_meetings` filtered to that range.
3. For summaries across several meetings, fetch them in ONE `get_meetings`
   call with all ids, then synthesize: one line per meeting (title, date,
   attendees, outcome), then themes across them.

## Meetings with a person

`list_meetings` filtered by attendee. Names can be ambiguous — if several
people match or results look thin, ask which person or try their email.

## Action items and follow-ups

Action items live inside the notes returned by `get_meetings` — there is no
separate action-item tool. Sweep: list the window, get the notes, extract
items marked as action items / next steps / owners, and group by owner.
Attribute each item to its meeting so the user can trace it.

## Meeting prep ("prep me for my next call with X")

1. Past context: meetings with X (above) — decisions, open items, promises.
2. Open questions: anything left unresolved in the latest notes.
3. Present as a short brief: relationship recap, open threads, suggested
   agenda. `query_granola_meetings` can shortcut step 1 for broad context.

## Folders (paid)

`list_meeting_folders` to enumerate, then `list_meetings` filtered by folder.
On free plans skip folders silently and filter by date/attendee instead.
