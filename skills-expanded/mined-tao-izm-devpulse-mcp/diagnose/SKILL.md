---
name: diagnose
description: Diagnose why the user's local dev environment is broken (dev server won't start or crashed, port already in use, errors in logs, merge conflicts, missing dependencies) using the devpulse MCP tools. Use when the user says something is broken, not working, or asks "what's wrong" with their app or dev server.
---

# Diagnose the dev environment

1. Call the devpulse `get_session_snapshot` tool before asking the user anything. Pass `cwd` only if the user is working in a different directory from the current project.
2. Read `diagnosis` first: `health`, `primary_issue`, `suggested_action` and `confidence`.
3. If `recent_errors` shows errors and you need the full picture, call `get_recent_errors` (it returns stack traces and more entries).
4. For a port conflict, tell the user which process holds the port (name, pid, directory) and offer to stop it or change the dev server's port. Do not kill a process without the user's confirmation.
5. After a fix, restart guidance or a change, call `get_running_services` to confirm the dev server is back up.

Report back in this order: what's wrong (one sentence), the evidence (the specific error, port or file), then the fix you propose or made. If `health` is `unknown`, say what devpulse couldn't determine instead of guessing.
