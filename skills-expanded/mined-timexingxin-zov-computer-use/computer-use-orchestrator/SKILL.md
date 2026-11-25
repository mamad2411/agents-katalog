---
name: computer-use-orchestrator
description: "Controls native desktop and cross-app tasks on macOS and Windows with semantic targeting, background-first operation, observed effects, and recovery. Use for native GUI, dialogs, canvas, or mixed web/desktop flows. Pure API/CLI/file tasks do not need this skill."
---

# Computer Use Orchestrator (macOS & Windows Background-First GUI Routing)

This skill orchestrates native desktop automation on **macOS** and **Windows** across Model Context Protocol (MCP) Computer Use backends while enforcing strict focus safety, single-writer ownership, and verifiable state transitions.

## 1. Routing Priority

1. **Direct API / MCP / CLI / Filesystem First**: Whenever a task can be completed cleanly via native files, CLI tools, or dedicated APIs, use them instead of GUI automation.
2. **Structured Browser Tools for Web DOM**: Delegate web page navigation, DOM scraping, and web form interaction to structured browser tools (e.g., Playwright MCP or Chrome DevTools MCP). Never operate web pages via blind desktop coordinate clicking when DOM tools exist.
3. **Semantic Tree First for Native Desktop GUI**: Route native macOS and Windows desktop tasks to **Zov Computer Use** (`zov-cua`, read `zov-computer-use`). Inspect health and permission readiness first (`request_access` / `list_apps`), without triggering unnecessary prompts during read-only checks.
4. **Fallback Backends**: If a specific capability is unavailable in the primary server, fall back to other explicitly configured desktop backends (such as `cua-driver` or `macos-mcp`) according to their live tool schemas.
5. **Visual Coordinate Fallback**: Use window-scoped screenshots (`PrintWindow` on Windows, `screencapture -l` on macOS) and coordinate actions **only** when the Accessibility / UI Automation tree does not expose the target control (e.g., custom canvas or self-drawn widgets). Physical cursor movement, foreground window activation, or global hotkeys require explicit user authorization—never silently steal focus from the user's active window.

## 2. Closed-Loop State Discipline

- **Pin Target Identity**: Establish the exact `app_ref` (`pid`, `bundle_id`, `name`) and `window_id` before dispatching actions. Do not assume the frontmost window belongs to the current task.
- **Re-Observe After Every Mutation**: Respect `state_id` and element handle lifecycles (`h_*`), or pass `return_state="compact"` for single-roundtrip atomic updates. Never chain multiple blind coordinate clicks from stale memory.
- **Verify Real Outcomes**: An `action_receipt` (`ok: true`) only confirms dispatch, not application-level completion. Verify field values, window states, or exported files directly after mutating actions.
- **Targeted Recovery**:
  - `stale_handle` / expired `state_id` → re-observe via `get_app_state` and select a fresh handle.
  - `foreground_required` → target is occluded or requires foreground focus for raw keystrokes; prefer semantic `set_value` / `click` (`strategy="a11y"`), or request user authorization before activating the window.
  - `permission_denied` → report the exact OS requirement (macOS `Accessibility` / `Screen Recording`, or Windows UIPI Administrator elevation mismatch) and stop the GUI branch cleanly.
  - Transient UI/IO delay → wait briefly and re-observe once; never loop across multiple GUI backends blindly.
- **Clean Up Owned Resources Only**: Close or remove only temporary windows/files created by the current task. Never terminate or restart user-owned applications.

## 3. Primary Backend Capability Profile

| Backend | Primary Characteristics & Operational Boundaries |
| --- | --- |
| `zov-cua` (**Zov Computer Use**) | Dual-native MCP server (`@zov/mcp-server`): compiled Swift `ApplicationServices` + `CoreGraphics` (`macos-ax-helper`) on **macOS 13+** and compiled C# UI Automation + Win32 `PrintWindow`/`SendInput` (`windows-uia-helper.exe`) on **Windows 10/11**. Provides stable semantic handles (`h_*`), compact/diff tree compression, atomic `return_state="compact"`, TOCTOU identity checks, password redaction, and background-safe `click`/`set_value`/`perform_action` with zero external binary dependencies. |

## 4. Single-Writer & Main-Agent Serialization

- **Single Writer per Window**: At any moment, at most one controller/agent may write to a target application or window. Before switching backends, confirm prior action completion and acquire a fresh `state_id` from the new backend. Never pass `state_id`, handles, or raster coordinates across different MCP servers.
- **Main-Agent GUI Ownership**: `zov-cua` enforces a cooperative subagent guard (`_meta["com.zov/request-context"].runtime_scope === "subagent"` → `SUBAGENT_COMPUTER_USE_UNAVAILABLE`). Keep GUI mutations serialized on the main agent; delegate only non-GUI file/research subtasks to subagents. Never strip metadata to bypass runtime guards.

## 5. Safe Background Window Closing

1. Before closing any window, verify task ownership (`app_ref`, `window_id`, document path) and unsaved state; save and verify file output first if modified.
2. When the close button (`AXCloseButton` on macOS or TitleBar `"Close"` / `"关闭"` button on Windows) is exposed in the semantic tree, re-observe the target window and trigger `left_click` / `click` with `strategy="a11y"` rather than sending global `cmd+w` / `alt+f4`.
3. After dispatch, call `list_windows` to confirm the target `window_id` has exited while other user windows remain intact. If a save prompt appears, pause and re-observe instead of repeating close commands.

## 6. Kill-Switch & Post-Stop Recovery

- `stop_computer_control` acts as a session-level kill switch, not a temporary window lock release. Once invoked (`"Computer control was stopped ... Start a new session"`), all subsequent calls on the same MCP session (both mutating and observation tools, except `get_capabilities`, `wait`, and `stop_computer_control`) fail closed and tracked held mouse inputs are released.
- Do not loop `request_access` or mutate runtime directories to bypass a stopped session. Resume only in a newly authorized MCP session after confirming prior actions have settled, and never automatically replay the halted action.
