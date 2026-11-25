---
name: journal
description: >-
  Use when the user wants to work with their daily note — view today's entry,
  add a log, do a daily review, or capture quick thoughts. Covers all daily
  note workflows.
---

# Daily Journal

Work with today's daily note in the Obsidian vault.

## Default Action (no arguments)

1. Call `obsidian_get_daily_note` to retrieve today's note
2. Summarize key tasks, events, or entries
3. Ask if the user wants to add anything

## Quick Capture (with arguments)

If the user provides text after `/journal`, log it:

1. Call `obsidian_append_daily_log` with heading "Notes" and the user's text
2. Confirm what was logged

## Common Headings

When logging entries, use these standard headings:
- **Work Log** — tasks, progress, accomplishments
- **Notes** — general thoughts and observations
- **Ideas** — creative ideas and inspirations
- **Meetings** — meeting notes and action items

## Weekly Review

If the user asks for a "weekly review":
1. List recent daily notes via `obsidian_list_notes` (subfolder "Daily Notes")
2. Read each day's note
3. Summarize themes, accomplishments, and open items
