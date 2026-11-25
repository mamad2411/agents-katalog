---
name: Learning Log
description: Capture corrections and preferences from this session so Claude doesn't repeat the same mistakes next time. Use at the end of any session where you had to redirect Claude or correct something. Adapts to Claude Code, claude.ai, and Cowork.
---

# /learning-log

This skill captures corrections from this session so the next session starts smarter.

When you correct Claude, when you say "not like that, like this," when a skill produces something off — those corrections get written into a running log. Next session, Claude reads the log and the correction is already applied.

---

## Which surface are you on?

**Claude Code**
You have file access. Append the new entry directly to `~/.claude/learning-log.md` (or the equivalent path the user uses). Keep the file sorted newest-first. Confirm with the user before saving.

**claude.ai chat**
You can't touch files. Generate the entry as a copy-ready block. Tell the user to paste it into their learning-log file and re-upload that file to the product Project.

**Cowork**
You have workspace access. Append to `learning-log.md` in the workspace if it exists, or create one at `project/learning-log.md` if not. Confirm before saving.

---

## How to use it

At the end of any session where Claude got something wrong, say:

> "Update the learning log with what you learned today."

Claude will draft a structured entry. Review it. Approve or edit. Then it gets saved (or you paste it in, on Chat).

---

## What gets logged

Worth logging:
- A correction you had to make more than once
- A preference Claude kept getting wrong
- A format or style rule that came up
- A decision Claude should remember

Not worth logging:
- One-off mistakes that won't come up again
- Anything already in your profile or project spec

---

## Log format

```
**Date:** [YYYY-MM-DD]
**Context:** [what you were working on]
**What happened:** [what Claude got wrong or what you corrected]
**The learning:** [the specific rule or preference going forward]
**Category:** [voice / design / build / product / process / other]
```

One entry per correction. Entries sort newest-first.

---

## Workflow layer (once you graduate)

When one product becomes three, the learning log moves to Notion (or Linear) the same way the spec does: a single "Learning log" page under the product hub, entries as bullet rows or subpages. Claude reads it at session start via MCP or a paste.

Same pattern. Different surface. The value is the same: each session inherits the corrections of every session before it.

---

## Entries

[Your entries go here — below this line in the saved file.]
