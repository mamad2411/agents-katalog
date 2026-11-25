---
name: clickup-today
description: "Use for 오늘 작업, Typora 일일 체크리스트, ClickUp 하위 작업 등재, local Markdown sheet refresh/publish/push; preserve local edits. For generic ClickUp tasks use clickup-cli; for calendars use Morgen."
---

# ClickUp Today

Use this skill only for daily Markdown sheets stored under `days/YYYY-MM-DD.md`. Read the relevant sheet before changing it; ask the user to save unsaved Typora edits first. Use the configured, authenticated `clickup-cli` for ClickUp operations, never direct API calls. For generic ClickUp tasks use the `clickup-cli` skill instead. For calendar events and Morgen tasks use `morgen`, not this tool.

Follow `README.md` for private `config.json` setup and installation. Never place list IDs, credentials, or task contents in tracked files. The user-installed command is `clickup-today`; direct invocation of `today.py` is also supported. Dates are local to the machine.

- `clickup-today refresh [--date YYYY-MM-DD] [--focus TASK_ID]`: read-only ClickUp sync into the sheet. Focus applies to refresh only. Linked checkboxes identify ClickUp tasks; unlinked handwritten items stay local. Preserve local checks, nested handwritten items, and notes; if a parent disappears, keep its handwritten items under the local-items heading.
- `clickup-today publish [--date YYYY-MM-DD]`: register unlinked checkboxes under their nearest linked parent. Match existing direct children by parent and name (including completed) before creating, verify each created task by re-reading it, and link it in the sheet. A checked item is still not completed remotely. After an uncertain create response, reconcile first; do not blindly retry.
- `clickup-today push [--date YYYY-MM-DD]`: only on an explicit request to change remote completion. Complete checked linked tasks using the configured list's real completion status, re-read each result, and refresh; never push an unlinked checkbox or reopen an unchecked task.

Do not equate same-titled linked and unlinked entries, or same-titled tasks under different parents. After remote changes, report the affected IDs, parent/list where relevant, and verified status. Never run `push` as part of `refresh` or `publish`.
