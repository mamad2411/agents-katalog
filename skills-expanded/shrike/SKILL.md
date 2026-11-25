---
name: shrike
description: Debug a web app with Shrike's recordings. Use when a button, page or request in the user's web app misbehaves and Shrike is open with the shrike MCP tools connected.
---

# Debugging with Shrike

Shrike runs the user's app and records each click from the page to the database. Use its `shrike` MCP tools to see what really happened instead of guessing from the code.

1. Get the app running: `run_app` if it isn't, then `app_snapshot` to see the page.
2. Reproduce the problem. Ask the user to click it in Shrike, or do it yourself with `app_click`, `app_type` or `run_scenario`.
3. Read the trip: `list_trips` for the newest recordings, `get_action` for the one that broke, `get_event` and `get_logs` for detail. `focus_trip` shows the user the one you mean.
4. Find the cause in the code with `read_file` and `search_code`. Say which line and why, plainly.
5. Change code only with `propose_patch`. It waits until the user applies or rejects the change in Shrike. Never edit files yourself and never run shell commands to change them.
6. After the user applies it, run the same steps again (`run_scenario`) and `compare_actions` with the broken recording. Say whether it is fixed.

If the user rejects a patch, read their comments, then propose a revised one or ask what they'd prefer.
