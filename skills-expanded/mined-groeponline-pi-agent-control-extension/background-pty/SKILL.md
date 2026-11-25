---
name: background-pty
description: "Manage persistent, long-running terminal sessions via tmux/dtach integration. Use for detached workflows, async jobs, or sessions that must survive disconnects. Examples: \"run in background\", \"detached session\", \"long running task\", \"tmux session\", \"persistent terminal\""
---
# Background PTY

Use this atom to manage terminal sessions that must persist beyond the life of a single LLM tool call or agent session.

## Mechanics

1.  **Launch**: Use `tctl launch --background` (wraps `tmux new-session -d` or `dtach -n`).
2.  **Attach**: Use `tctl attach -s <session-id>` to view the current state.
3.  **Read**: Use `tctl snapshot -s <session-id>` to get a text capture without attaching.
4.  **Send**: Use `tctl type -s <session-id> "cmd\n"` to inject commands.

## Workflow

1.  **Start a long task** (e.g., a complex build or server):
    ```bash
    ./bin/tctl launch "npm run build" -s build-session --background
    ```
2.  **Periodically check status**:
    ```bash
    ./bin/tctl -s build-session snapshot
    ```
3.  **Finalize**:
    ```bash
    ./bin/tctl -s build-session close
    ```

## Persistence Rules

- Session IDs must be unique per `RUN_ID`.
- Always close background sessions when finished to avoid resource leaks.
- Prefer `snapshot` over `attach` for programmatic monitoring.
