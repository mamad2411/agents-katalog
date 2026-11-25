---
name: codex-goal-control
description: Open and control the current Codex thread goal from any Codex thread. Use when the user asks to open the goal panel, manage goals without the CLI, set/pause/resume/complete/clear a thread goal, or make the local goal web app point at the current thread.
---

# Codex Goal Control

This skill is experimental. It depends on Codex goals and app-server goal methods, which may change across Codex versions. Use it as a local operator convenience, not as a stable production contract.

Prerequisite:

```toml
[features]
goals = true
```

Use the bundled goal panel helper as the canonical implementation. Do not infer the current thread from the browser page; claim the current Codex thread from the agent runtime first.

## Open The Goal Panel For This Thread

Run:

```bash
node "${CODEX_HOME:-$HOME/.codex}/skills/codex-goal-control/scripts/codex_goal_panel_open.js" --json
```

Return the `threadUrl` or `url` as the default panel link. The helper writes the current `CODEX_THREAD_ID` to the local claim file and ensures the localhost panel server is running.

If the user is in a new Codex thread, run this helper again. Do not reuse an old browser URL unless it already includes the intended `threadId`.

If the helper reports `server` as `started-unverified-sandbox`, the current sandbox could not verify the local listener. Check the returned `serverLogFile` if the panel does not load. If the server is not actually running, start it with approval because it must bind `127.0.0.1:43873`:

```bash
node "${CODEX_HOME:-$HOME/.codex}/skills/codex-goal-control/scripts/codex_goal_panel_server.js" --host 127.0.0.1 --port 43873
```

## Direct Goal Commands

Use these when the user asks to manage the current thread goal without opening the panel:

```bash
node "${CODEX_HOME:-$HOME/.codex}/skills/codex-goal-control/scripts/codex_goal.js" get
node "${CODEX_HOME:-$HOME/.codex}/skills/codex-goal-control/scripts/codex_goal.js" set "objective" --budget 3000
node "${CODEX_HOME:-$HOME/.codex}/skills/codex-goal-control/scripts/codex_goal.js" pause
node "${CODEX_HOME:-$HOME/.codex}/skills/codex-goal-control/scripts/codex_goal.js" resume
node "${CODEX_HOME:-$HOME/.codex}/skills/codex-goal-control/scripts/codex_goal.js" complete
node "${CODEX_HOME:-$HOME/.codex}/skills/codex-goal-control/scripts/codex_goal.js" clear
```

These commands default to `CODEX_THREAD_ID`. Only pass `--thread` when the user explicitly wants to target a different thread.

## Reporting Rule

Be explicit about proof:

- `thread_proven`: the Codex thread goal API returned the expected state for `CODEX_THREAD_ID`.
- `panel_proven`: the localhost panel API returned the expected state.
- `visual_proven`: the user or browser automation confirmed the visible browser render.

Do not call browser/panel evidence proof that the agent intrinsically received the goal. Use the thread goal API or the built-in goal state for that claim.
