---
name: cua_desktop_operator_skill
description: Windows desktop operation skill for MCP-capable AI agents. Use when the task requires observing the current desktop, launching or focusing apps, clicking or typing in Windows GUI apps, using reusable desktop macros, or running an observe-plan-act-verify loop through the local desktop-operator MCP server.
---

# CUA Desktop Operator Skill

Use this skill when the user wants desktop control on Windows through a local MCP server.

## What this skill expects

- A local Python runtime with the desktop operator dependencies installed.
- The `desktop-operator` MCP server available over stdio.
- The agent can inspect screenshot artifacts returned by `desktop_observe`.
- Temporary artifacts should be cleaned after task success unless the user asked to keep them.

If the current client does not expose the `desktop_*` MCP tools yet:

1. Read `references/mcp-client-setup.md`.
2. If the client is Codex, Claude Code, Cursor, or OpenCode, configure the local MCP server before attempting the desktop task.
3. If the client is something else, stop and ask the user to add the MCP server manually, then send them the config snippet from `references/mcp-client-setup.md`.
4. After configuration, reload the client if needed and verify that `desktop-operator` is visible before starting the task.

If the runtime is not ready:

1. Run `scripts/setup_runtime.ps1`.
2. Run `scripts/start_mcp_server.ps1`.

## Core workflow

Use this loop for almost every GUI task:

1. Call `desktop_observe`.
2. Inspect the screenshot, active window, visible windows, and optional cropped window image.
3. Choose the smallest next step.
4. Prefer the highest-signal tool that fits:
   - `desktop_focus_window` before keyboard input
   - `desktop_click_relative` before absolute clicks
   - `desktop_uia_*` when a stable control is visible in UIA
   - `desktop_run_macro` when the action pattern is reusable
5. After each mutating action, call `desktop_observe` or `desktop_validate_state`.
6. Repeat until the success condition is visible.
7. If the task is complete and the user did not ask to keep screenshots, logs, or debug traces, call `desktop_cleanup_artifacts`.

## Tool selection order

Use tools in this order unless the task clearly needs something else:

1. `desktop_observe`
2. `desktop_find_window` or `desktop_list_windows`
3. `desktop_focus_window`
4. `desktop_run_macro` for stable repeated flows
5. `desktop_click_relative` / `desktop_uia_click`
6. `desktop_paste_text` for Chinese or mixed-language text
7. `desktop_type_text` only for short plain text
8. `desktop_validate_state`

## Action policy

- Keep actions small and reversible.
- Prefer one to three tool calls before observing again.
- Use `desktop_wait` when the UI is loading instead of stacking blind clicks.
- Use `match_index` whenever multiple similar windows exist.
- Use `desktop_run_macro` with `macro_id="__catalog__"` to inspect the built-in macro catalog.
- Clean temporary artifacts after successful completion unless the user explicitly asked to retain them.

## Safety policy

- Do not run destructive OS actions unless the user explicitly asked for them.
- Validate focus before typing or pressing submit keys.
- If a click misses once, re-observe before trying again.
- If UIA lookup is slow or empty, return to screenshot-driven interaction.

## References

- MCP tool details: `references/mcp-tool-catalog.md`
- MCP client setup: `references/mcp-client-setup.md`
- Interaction patterns: `references/interaction-patterns.md`
- Macro catalog: `references/macro-catalog.md`
- Failure recovery: `references/failure-recovery.md`
- Cross-agent notes: `references/compatibility.md`
