---
name: skill-name
description: <One or two sentences. State WHAT the skill does AND WHEN to use it. Be tight and boring, not clever — a precise description triggers reliably; a vague one under-triggers. Name the user phrases/contexts that should invoke it, e.g. "Use whenever the user mentions X, Y, or asks to Z, even if they don't say the word 'skill'.">
---
# skill-name

<Short framing: what problem this solves and the principle behind it.>

## Steps
1. ...
2. ...

## Notes
- Keep this file under ~500 lines. If it grows, split details into `references/` and point to them.
- Add `scripts/` for deterministic/repetitive work (they run without loading into context).
- Add `assets/` for templates/icons used in output.

<!-- Folder layout:
skill-name/
├── SKILL.md        (required)
├── scripts/        (optional — executable helpers)
├── references/     (optional — docs loaded on demand)
└── assets/         (optional — templates, etc.)
The skill is the authoring format; ship it to a team by bundling it in a plugin. -->
