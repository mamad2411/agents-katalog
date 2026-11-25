---
name: things
description: Add and manage actionable items in Things (macOS) via URL scheme. Add to-dos, projects, update tasks, show lists, search. Use when user asks to add tasks to Things, create to-dos, Things integration, or /things.
---

# Things Skill

Add and manage actionable items in Things 3 for Mac using the Things URL Scheme. Requires macOS with Things 3.

## Usage

```bash
python3 _scripts/things.py add "Buy milk"
python3 _scripts/things.py add "Call dentist" --when tomorrow --tags Errand
python3 _scripts/things.py project "Vacation" --area Family --todos "Book flights" "Pack bags"
python3 _scripts/things.py show   # Show Today
python3 _scripts/things.py search "meeting"
```

## Add Options

- `--when`, `-w` — today, tomorrow, evening, anytime, someday, or date (e.g. 2026-02-25)
- `--list`, `-l` — Project or area name
- `--notes`, `-n` — Notes
- `--tags`, `-t` — Comma-separated tags
- `--deadline`, `-d` — Deadline date

## Update (requires `THINGS_AUTH_TOKEN` in `.env`)

Get token from Things → Settings → General → Things URLs → Manage.

```bash
python3 _scripts/things.py update <todo-id> --when today
python3 _scripts/things.py update <todo-id> --completed true
```

## Output

Opens Things app via URL scheme. No file output.
