---
name: mem
description: Quick memory capture for fleeting thoughts without context switching. Use when user says "mem", "remember", "capture this", or /mem.
---

# Mem Skill - Quick Memory Capture

Capture fleeting thoughts, ideas, and notes instantly without context switching.

## Usage

```bash
python3 _scripts/mem_capture.py "Your thought here"
```

With custom title & destination:
```bash
python3 _scripts/mem_capture.py "Your content" --title "Great Idea" --dest "00 - Inbox"
```

## Defaults

- **Destination**: `00 - Inbox/`
- **Title**: `Memory - HH:MM`
- **Tags**: `#type/fleeting`, `#source/mem-skill`

## Output

Timestamped note in your vault with YAML frontmatter.
