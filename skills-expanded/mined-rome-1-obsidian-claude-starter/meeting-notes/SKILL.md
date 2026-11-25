---
name: meeting-notes
description: Turns rough meeting notes, a transcript, or a spoken recap into a structured meeting note in Meetings/, then updates the linked people and project notes and lists the action items. Also preps for an upcoming meeting by pulling the relevant people, project and past-meeting context. Use when the user pastes meeting notes or a transcript, says "write up this meeting", "log my call with X", "notes from today's sync", "prep me for my meeting with X", or runs /meeting-notes.
argument-hint: "[paste notes, or 'prep <person or topic>']"
---

# Meeting notes

Two modes: **write-up** (after a meeting) and **prep** (before one).
If the user says "prep", go to the prep section.

## Write-up

### 1. Gather

- Take the raw notes or transcript the user gave you. If none, ask them to paste or dictate.
- Ask only for what you cannot infer: the date (default today), and the project if it is unclear.

### 2. Resolve the people and the project

- For each attendee, look for `People/<First-Last>.md` (Grep the name; names in notes are often first names only).
- Link those that exist. For people without a note, write the plain name and ask whether to create notes for any of them. Do not create person notes unasked.
- Find the project note the meeting belongs to, if any.

### 3. Write the note

Create `Meetings/YYYY-MM-DD-Topic.md` from `System/Templates/Meeting.md`.

- **Context**: one or two sentences on why the meeting happened.
- **Key points**: what was learned or discussed that matters later. Not a transcript.
- **Decisions**: each one a line. Note who made it if that matters.
- **Action items**: `- [ ] Who: what, by when`. If an owner or date was not stated, write "owner?" or "date?" rather than guessing.
- Keep quotes only when the exact wording matters, and mark them as quotes.

### 4. Update linked notes

- Each tracked attendee: a dated line under `## Interactions` linking the meeting; update `last_contact`; update `next_action` if the meeting changed it.
- The project: a line in its `## Log` (or `Current-State.md`), and the user's own action items as `- [ ]` under `## Next actions`.
- Significant decisions: offer to record them with the `decision-record` skill.
- Set `updated:` on every note you change.

### 5. Report

Show the action items, the notes you changed (as links), and any open questions (unknown owners, people without notes).
Run `python3 scripts/check_vault.py`.

## Prep

1. Find the person notes, the project notes and the last two or three meetings with the same people or project.
2. Write a short brief in the chat, not a file, unless asked:
   who they are and what they care about, what was said or promised last time, open action items on both sides, and two or three things worth raising.
3. Offer to create the meeting note now with the context section filled in, so notes can go straight into it.
