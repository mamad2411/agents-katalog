---
name: inverse
description: Inverse thinking — compute reversely for problems, decisions, actions, and confusions. Inspired by linear algebra's inverse matrix and Charlie Munger's "invert, always invert." Use when you want to flip a problem, reverse a decision, undo an action, or dissolve confusion.
---

# Inverse Skill

Apply inverse thinking (Munger's "invert, always invert") to problems, decisions, actions, and confusions.

## Usage

```bash
python3 _scripts/inverse.py problem "I can't find time to exercise"
python3 _scripts/inverse.py decision "Should I quit my job?"
python3 _scripts/inverse.py action "I'm going to start a side project"
python3 _scripts/inverse.py confusion "I don't know what career path to take"
```

## Options

- `type` — One of `problem`, `decision`, `action`, `confusion` (required)
- `input_text` — The text to invert (required)
- `--from-path PATH` — Vault note with additional context
- `--title TEXT` — Custom output filename
- `--save` — Save to vault

## Output

`Atlas/Inverse - [Topic].md` (with YAML frontmatter)
