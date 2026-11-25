---
name: chrome-debugging
description: Debug and visually inspect a running website in Chrome through the EZ Chrome MCP tools. Use for live React, Svelte, or other browser apps, console logs, screenshots, and tab inspection.
---

# Chrome Debugging

Use this skill when you need to inspect a running website in Chrome from Cursor.

## Workflow

1. Call `overview` first and choose the tab ID that matches the site you are debugging.
2. Call `logs` before using `eval`; the compact activity timeline often explains the failure without mutating the page.
3. Call `screenshot` when you need to inspect the live GUI, compare rendered state, or check for overlapping elements.
4. Always pass `afterLogId` to `logs` or `eval` when you have a recent raw log ID from the tab; this keeps responses small while preserving the anchor log.
5. Use `log_detail` when a specific HTTP request row needs full captured headers, request body, or response body. The `logs` output intentionally keeps HTTP rows compact.
6. Prefer small eval scripts that read state or call one page function at a time.
7. Treat `eval` as potentially destructive: it can click buttons, mutate storage, send requests, navigate, and change app state.

When debugging asynchronous UI behavior, pass a small `waitMs` to `eval` so the tool waits until observed activity is quiet before returning.

## HTTP Request Details

The `logs` tool shows HTTP requests as compact request/response summary rows with correlation IDs. It does not render request headers, response headers, request bodies, response bodies, or body sizes.

Use `log_detail` with the raw activity/log ID from a request row to inspect the full captured JSON detail. If the detail is too large for the response, pass `absolute_path` to write the full uncompressed JSON to a file.

## Log Navigation

Use raw log IDs to avoid replaying large browser activity buffers into context.

- Start with `logs` using the default limit.
- For follow-up `logs` and `eval` calls, pass `afterLogId` with the latest visible raw log ID from the previous response whenever possible.
- `afterLogId` is inclusive: the anchor log ID you pass should appear again, followed by newer activity.
- To inspect older history, pass `beforeLogId` with the first raw log ID currently visible.
- Grouped rows may display an ID span such as `abc123..z9x8w7`; use either raw log ID from the span when paging.
- If a cursor is no longer retained, call `logs` without cursors to re-anchor on the current retained window.

## Example Usage

When working on a React or Svelte application, use the ezChrome MCP server to test your live application instead of reasoning only from source code.

1. Start the app with the project command, for example `just dev` when available.
2. Use `open-tab` to open the local app URL if a tab is not already available.
3. Use `overview` to get the tab ID.
4. Use `logs` to check console output, runtime errors, navigations, and compact XHR/fetch activity.
5. Use `screenshot` to inspect the rendered GUI. For example, capture a screenshot after changing layout code to check whether buttons, menus, modals, or form fields overlap.
6. Use `log_detail` for full HTTP request/response headers and bodies when a compact request row is relevant.
7. Use `eval` only when needed for precise DOM state, such as reading `document.querySelector('[data-testid="submit"]').getBoundingClientRect()`.
