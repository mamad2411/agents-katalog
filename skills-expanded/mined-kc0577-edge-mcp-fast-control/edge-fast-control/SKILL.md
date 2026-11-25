---
name: edge-fast-control
description: Route Microsoft Edge browsing to the user's configured playwright_edge MCP connection and everyday signed-in Edge profile. Use whenever the user explicitly says Edge, Microsoft Edge, 日常 Edge, 常用 Edge, 打开 Edge, 使用/调用 Edge, asks to reuse Edge login/history/tabs/extensions, or requests browser automation that depends on their existing Edge session. Prefer one fast Playwright workflow and prohibit silent fallback to ChatGPT's built-in Edge, in-app Browser, Chrome, or Computer Use.
---

# Edge Fast Control

Control the user's everyday Microsoft Edge through the configured `playwright_edge` MCP server and Playwright Extension. Preserve the existing profile, login state, extensions, preferences, and unrelated tabs.

## Required route

1. Use `mcp__playwright_edge__browser_run_code_unsafe` as the default tool for a known multi-step workflow.
2. Use other `mcp__playwright_edge__browser_*` tools only for genuinely exploratory pages, recovery, dialogs, or visual verification after the extension connection page has been sanitized.
3. Never use any of these as an automatic substitute:
   - `agent.browsers.get("edge")` through `node_repl`
   - the ChatGPT in-app Browser
   - `chrome:control-chrome`
   - Computer Use
   - a temporary Playwright profile
4. Use a different route only when the user explicitly requests that route or explicitly approves fallback after `playwright_edge` cannot be recovered.

The word “Edge” refers to this Playwright MCP route, not merely any backend that happens to open an Edge window.

## Fast workflow

For deterministic tasks, send one complete function to `browser_run_code_unsafe`:

```text
navigate directly
→ wait for DOM or URL conditions
→ read candidate elements once
→ select and act inside the browser
→ verify final URL, title, or page state
→ return a structured result with phase timings
```

- Prefer direct target URLs when known.
- Use `locator.waitFor()` and `waitForURL()` instead of fixed sleeps.
- Do not use `waitForTimeout()` for ordinary page readiness.
- Avoid repeated snapshot/find/click/wait round trips.
- Omit screenshots unless visual evidence is required.
- Do not close unrelated tabs unless the user requests it.

## Connection and profile rules

- Connect through the installed Playwright Extension and its configured `PLAYWRIGHT_MCP_EXTENSION_TOKEN`.
- Treat the token as a secret. Never print, quote, log, or expose its value.
- Never list tabs while the active page may be the extension `connect.html` page; its URL query can contain connection credentials.
- For a connection check, use `browser_run_code_unsafe` to detect the extension page internally, navigate it to `about:blank`, and return only a sanitized status. Never return the original extension URL or query parameters.
- Do not pass `--user-data-dir` or `--isolated`; both can produce a profile different from the user's everyday Edge.
- Do not launch another Edge profile to make a failed connection appear successful.
- Verify success from the requested signed-in state or the existing Edge tabs, not merely from the executable name.

## Recovery

If a `playwright_edge` call reports `Transport closed` or the server is unavailable:

1. Run one secret-safe `mcp__playwright_edge__browser_run_code_unsafe` probe. If the active page is an extension `connect.html` page, navigate it to `about:blank` before returning; return only `connected`, `sanitizedExtensionPage`, and the safe final URL.
2. If it still fails, inspect the configured local `playwright_edge` server without revealing credentials.
3. Reconnect or start the localhost-only configured Playwright MCP extension server when safely possible, then retry the original task once.
4. If `playwright_edge` is absent from the task's tool list, stop and tell the user that this task did not load the MCP server. Ask them to restart Codex and confirm `playwright_edge` with `/mcp`.
5. Never hide the failure by switching to a built-in browser route.

## Completion standard

Report completion only after verifying the requested final page or state. Include the browser-internal duration when the task is a speed test. If recovery fails, name the failed `playwright_edge` route and the next concrete action; do not claim that Edge automation succeeded through another plugin.
