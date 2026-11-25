---
name: daily-note-generator
description: "Generates daily notes for wiki-llm with summary, tasks, focus, token usage, and model tracking"
version: 1.1.0
author: Yasuui
category: note-taking
tags: [daily, wiki-llm, tracking, automation]
license: MIT
platforms: [linux, macos, windows]
tested: schema-only
tested_note: Frontmatter and docs validated; no runtime execution.
requires:
  - "Hermes Agent v0.13.0+"
---

# Daily Note Generator Skill

This skill creates standardized daily notes for the wiki-llm system to track progress, token usage, models used, and tasks completed.

## When to Use

- Starting a daily work session and need a structured note template
- Tracking token usage, models, and tasks over time
- Maintaining a daily journal in wiki-llm format

## Prerequisites

- Hermes Agent v0.13.0+
- A wiki-llm vault or daily notes directory configured

## Steps

### 1. Generate Date

Uses current date in YYYY-MM-DD format.

### 2. Create Note File

Creates a markdown file in the configured daily notes directory:

```bash
DAILY_DIR="${DAILY_NOTES_DIR:-$HOME/projects/wiki-llm/wiki/daily}"
mkdir -p "$DAILY_DIR"
```

### 3. Apply Template

Uses the daily note template with placeholders for:
- Date and metadata
- Summary section
- Tasks completed checklist
- Focus areas
- Metrics and usage tracking
- Issues and resolutions
- Plans for tomorrow
- Notes and observations

### 4. Verify

```bash
ls -la "$DAILY_DIR/$(date +%Y-%m-%d).md"
```

## Configuration

Override the daily notes directory with environment variable `DAILY_NOTES_DIR` or set in your profile's `config.yaml`.

Default template location: `$DAILY_NOTES_DIR/template.md`

## Pitfalls

- If `DAILY_NOTES_DIR` is not set, defaults to a wiki-llm vault path — verify it exists
- Template must exist before first run; create one if missing
- Daily note files are not auto-committed to git (manual step if versioning is desired)

## License

MIT — see repository LICENSE file.