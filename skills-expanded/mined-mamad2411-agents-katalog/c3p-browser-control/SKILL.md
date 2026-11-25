---
name: c3p-browser-control
description: Browser automation via the official Claude Chrome extension. Controls Chrome tabs, navigation, page reading, form filling, screenshots, console logs, and network requests through the installed extension's native-host socket bridge.
when-to-use: When the user asks you to interact with Chrome — browse websites, fill forms, take screenshots, read page content, or automate browser workflows. Invoke this skill before using any c3p-browser-control MCP tools.
---

# Chrome Browser Control

You have a browser automation MCP server (`c3p-browser-control`) that controls Chrome through the official Claude browser extension.

## Getting Started

Every session **must** start with `tabs_context_mcp` (with `createIfEmpty: true`) before any other browser tool. Other tools fail with `No MCP tab group exists` or `No tab available` until the tab group exists.

1. **Call `tabs_context_mcp` first** with `{ "createIfEmpty": true }`. Capture the returned `tabId` and `tabGroupId`.
2. **Reuse that `tabId`** in every subsequent `navigate`, `get_page_text`, `read_page`, etc. Do not omit `tabId` — the native bridge requires it.
3. **Create additional tabs** with `tabs_create_mcp` only if the workflow needs multiple tabs; otherwise reuse the tab from step 1.

When batching with `browser_batch`, every inner call that targets a tab still needs `tabId` in its args — `browser_batch` does not auto-fill it.

Inner `name` in `browser_batch` must be a top-level tool name from the list below — never an inner action enum. To wait, use `{ "name": "computer", "input": { "action": "wait", "duration": 2, "tabId": ... } }`, not `{ "name": "wait", ... }`. Same for `screenshot`, `scroll`, `key`, `type`, etc. — they are all `computer` actions. Pass the bare tool name without any server prefix.

## Available Tools

All tools are prefixed with the MCP server name in your tool list. Core tools (shown without prefix):

- `tabs_context_mcp` — get tab group context (call first)
- `tabs_create_mcp` — create a new tab
- `navigate` — go to a URL or forward/back
- `read_page` — accessibility tree of page elements
- `get_page_text` — extract plain text content
- `find` — find elements by natural language description
- `form_input` — set form values by element reference
- `computer` — mouse clicks, keyboard input, screenshots, scrolling
- `javascript_tool` — execute JS in page context
- `resize_window` — resize browser window
- `read_console_messages` — read browser console (always provide a filter pattern)
- `read_network_requests` — read HTTP requests (filter by URL pattern)
- `browser_batch` — batch multiple tool calls in one round trip
- `shortcuts_list` / `shortcuts_execute` — list and run extension shortcuts
- `gif_creator` — record and export browser actions as GIF
- `upload_image` — upload images to file inputs

## Important Rules

- **First navigation to a new domain must be a direct `navigate` call, NOT wrapped in `browser_batch`.** The Claude extension's batch implementation swallows `permission_required` events into a plain error string, so the permission popup never appears when navigating inside a batch. Always do an unwrapped `navigate` first; once the domain is authorized, follow-up actions (`read_page`, `computer`, `find`, etc.) on the same domain can be batched safely.
- **Click/hover by `ref`, not by guessed coordinates.** `read_page` returns element reference IDs like `[ref_5]` but no pixel positions. `computer` accepts `ref` for `left_click`, `right_click`, `double_click`, `triple_click`, `hover`, and `scroll_to`. Use it — coordinates picked without a screenshot are almost always wrong. Only fall back to `coordinate` after `screenshot` makes the target visually obvious. (c3p auto-prepends a screenshot before every click/hover to force a fresh composited frame; without it, CDP clicks on hidden MCP tabs silently no-op.)
- **Do not use `alert()`, `confirm()`, or `prompt()`** in JavaScript — they block the browser and cannot be dismissed through automation.
- **The user may see extension permission prompts** in Chrome. These are shown by the official extension and cannot be bypassed.
- **If permission is denied**, surface the denial to the user and do not retry or attempt workarounds.
- **Stop after 2–3 failed attempts** and explain what failed rather than retrying indefinitely.
- **Tab IDs are required** for most tools. Always get them from `tabs_context_mcp` first.
- **Use `browser_batch`** when you can predict a sequence of actions to reduce round trips.

## Diagnostics

Use `c3p_browser_status` to check connectivity — it reports the socket path, whether the native host is reachable, and current configuration.
