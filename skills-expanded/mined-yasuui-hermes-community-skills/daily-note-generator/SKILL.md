---
name: daily-note-generator
description: Generates daily notes for wiki-llm with summary, tasks, focus, token usage, and model tracking
version: 1.0.0
author: Chief
tags: [daily, wiki-llm, tracking, automation]
---

# Daily Note Generator Skill

This skill creates standardized daily notes for the wiki-llm system to track progress, token usage, models used, and tasks completed.

## Usage

Run this skill to generate a daily note template for the current date.

## Steps

1. **Generate Date**: Uses current date in YYYY-MM-DD format
2. **Create Note File**: Creates a markdown file in `/Users/agentos/projects/wiki-llm/wiki/daily/`
3. **Apply Template**: Uses the daily note template with placeholders
4. **Open for Editing**: Opens the file in the default editor for manual filling

## Template Structure

The daily note includes:
- Date and metadata
- Summary section
- Tasks completed checklist
- Focus areas
- Metrics and usage tracking
- Issues and resolutions
- Plans for tomorrow
- Notes and observations

## Configuration

The skill uses the daily note template located at:
`/Users/agentos/projects/wiki-llm/wiki/daily/template.md`

## Output

Daily notes are saved to:
`/Users/agentos/projects/wiki-llm/wiki/daily/YYYY-MM-DD.md`

## Example

To generate today's daily note:
```bash
hermes skill run daily-note-generator
```

This will create/open the file for today's date in the daily notes directory.