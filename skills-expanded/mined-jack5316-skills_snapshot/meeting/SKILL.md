---
name: meeting
description: Structure notes and action items from meeting conversations into Obsidian meeting notes. Use when user asks to process meeting notes, structure a conversation, extract action items, or /meeting.
---

# Meeting Notes Skill

Takes raw meeting notes or conversation transcripts and structures them into the vault's Meeting Note format: Attendees, Agenda, Notes, Decisions Made, Action Items, Follow Up.

## Usage

```bash
python3 _scripts/meeting_notes.py PATH [--title "Meeting Name"] [--output PATH]
```

- **PATH**: Path to the meeting notes file (relative to vault root or absolute). Supports raw transcripts, bullet notes, or unstructured conversation text.
- `--title`: Meeting name for the output note (default: derived from filename)
- `--output`: Custom output path (default: `Sources/Meeting - {title} - {date}.md`)

## Agent workflow

When user says "/meeting" or "structure these meeting notes" and points to a file:

1. Resolve the file path (vault-relative or absolute)
2. Run: `python3 _scripts/meeting_notes.py "path/to/notes.md"`
3. If meeting name is known: add `--title "Meeting Name"`
4. Confirm capture with the saved path

## Output

Structured note with:

- **Attendees** — Participants identified from the conversation
- **Agenda** — Topics discussed (inferred if not explicit)
- **Notes** — Key discussion points, summarized
- **Decisions Made** — Explicit decisions and outcomes
- **Action Items** — Tasks with `- [ ]` checkboxes and assignees when identifiable
- **Follow Up** — Suggested next steps or items to process into project notes

Uses `[[wikilinks]]` for Obsidian interconnection. No YAML frontmatter in output.
