---
name: add-mk-dump
version: 1.0.0
description: Creates a new monkey-brain dump session from the template and registers it in dump-index.md. Use when user runs /add-mk-dump or wants to start a new dump session.
user-invocable: true
---

# add-mk-dump

Creates a new dated session file and registers it so `/clean-mk-dump` can find it.

## Flow

1. Check `docs/monkey-brain/MONKEY_BRAIN_TEMPLATE.md` exists — if not, tell user to run `/init-mk-dump` first
2. Session directory: `docs/monkey-brain/dump-sessions/{yyyy}/{mm}/` — create if it doesn't exist
3. Run number: count files matching `{yyyy-mm-dd}-???-*.md` in today's directory + 1, zero-padded (`001`, `002`, …)
4. New filename: `{yyyy-mm-dd}-{run}-temp.md`
5. Copy template content into the new file exactly as-is
6. Update `docs/monkey-brain/dump-index.md`:
   - If missing or malformed, initialize it first (see `/init-mk-dump` for format)
   - Add row to Sessions table: `| {yyyy}/{mm}/{filename} | dumped |`
   - Set `latest:` to full path from project root
7. Tell user the file path; start from `## Emotional` and work through naturally; run `/clean-mk-dump` when done

Do NOT open the file or pre-fill any sections.
