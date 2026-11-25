---
name: dashboard
description: Generate the visual dashboard for TenantFlow. Copies the fixed dashboard template to the workspace. The dashboard reads tasks.json and progress.log from disk and auto-refreshes every 5 seconds.
---

# Dashboard

Copies the dashboard template to `.claude/workspace/dashboard.html`.

## Workflow

1. **Copy the template** — copy `.claude/skills/dashboard/dashboard.html` to `.claude/workspace/dashboard.html`
2. **Do NOT regenerate the HTML from scratch** — always use the fixed template
3. **Instruct user**: "From `.claude/`, run `python -m http.server 8000`, then open `http://localhost:8000/workspace/dashboard.html`."

## How the dashboard works
- Reads `tasks.json` and `progress.log` via fetch (relative paths)
- Auto-refreshes every 5 seconds
- Shows: status counts (done, in progress, pending, blocked, failed), overall progress bar, milestone progress bars, task list with status badges, activity timeline from progress.log
- No generation needed — the same HTML file works for any project because it reads task data dynamically

## Important
- Serve from `.claude/`, not `.claude/workspace/`. The dashboard reads `progress.log` from its own folder and `tasks.json` from `../tasks.json`, and a server started inside `workspace/` can't reach the parent folder. Served from there, the dashboard stays on "Waiting for tasks.json...".
- The project's copy of the template is `.claude/skills/dashboard/dashboard.html`, taken from the team builder's `references/templates/dashboard.html`. Do not modify it per project.
