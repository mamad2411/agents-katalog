---
name: ultraviewer-computer-use
description: >
  Operate an authorized remote Windows computer through the ultraviewer-mcp server
  (UltraViewer-compatible, headless). Use when the user asks to connect to an UltraViewer
  ID, look at or control a remote PC they gave you an UltraViewer ID and password for, or
  set up ultraviewer-mcp.
metadata:
  homepage: https://github.com/abhalala/ultraviewer-mcp
---

# UltraViewer computer use

`ultraviewer-mcp` is a stdio MCP server. It connects to one remote computer at a time using that computer's UltraViewer ID and current password, then exposes screenshots and mouse and keyboard input as tools.

## Rules

- Only connect to a computer the user owns or is authorized to access, with an ID and password the user gave you in this conversation. Never reuse a password from an earlier conversation.
- Never ask the user for the password in plain chat if your client offers a secret-input tool; use it.
- Before any destructive action on the remote machine (deleting files, uninstalling, changing accounts or security settings, sending messages or payments), stop and confirm with the user.
- Call `disconnect` when the task is done or the user stops responding.

## Setup check

1. Confirm the `ultraviewer` MCP server is configured. If not, point the user to the README: build with `cargo build --release`, then register the binary as a stdio server, for example `claude mcp add ultraviewer -- /absolute/path/to/ultraviewer-mcp`.
2. Call `session_status` to confirm the server responds.

## Control loop

1. `connect` with `partner_id` and `password`.
2. `session_status`: check `Remote allows control`. If `no`, you can only watch; tell the user.
3. `screenshot` (default `max_width` 1280). Read the screen before acting.
4. Act with coordinates taken from the most recent screenshot:
   - `click` `{x, y, button?, count?}`
   - `move_mouse` `{x, y}`
   - `drag` `{from_x, from_y, to_x, to_y, button?}`
   - `scroll` `{direction: up|down, amount?, x?, y?}`
   - `type_text` `{text}` (newline presses Enter, tab presses Tab)
   - `press_keys` `{keys, repeat?}`, for example `ctrl+c`, `alt+tab`, `win+r`, `enter`; separate chords with spaces
   - `remote_action` `{action: ctrl_alt_delete|lock_screen}`
5. Take a new `screenshot` after each action that changes the screen, and confirm the result before the next step. Coordinates from an older screenshot may be wrong after a resize or a window move.
6. `disconnect`.

## Troubleshooting

- "screen dictionary ... not found": see Setup check step 2.
- "larger than this viewer supports": ask the user to pick a single monitor in UltraViewer on the remote computer or lower its resolution, then reconnect.
- Timeout while connecting: the ID or password is wrong, the password has rotated, or the remote UltraViewer is offline. Ask the user for the current password.
