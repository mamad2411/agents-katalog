---
name: browser-control
description: Drive a real Chrome or Edge browser through the browser-ref MCP server — navigate, read pages, click by ref, fill forms, take screenshots. Use whenever a task needs a live logged-in browser, JavaScript-rendered content, or multi-step interaction (login, checkout, dashboards) that plain HTTP fetching cannot handle.
license: Apache-2.0
---

# Browser control

The `browser-ref` MCP server drives a real, persistent browser. Pages are read as **semantic snapshots**: interactive elements get stable `[eN]` ids, and you act by id instead of guessing CSS selectors.

## Setup

This skill needs the `browser-ref` MCP server. It runs over stdio and uses the Chrome or Edge already installed — no browser download, no API key.

```json
{
  "mcpServers": {
    "browser-ref": {
      "command": "npx",
      "args": ["-y", "browser-ref-mcp"]
    }
  }
}
```

Verify with `npx -y browser-ref-mcp --version`, or call `browser_get_info` once the server is connected. Source: <https://github.com/zy2755/browser-ref-mcp> · npm: `browser-ref-mcp`.

## The core loop

1. `browser_navigate` — returns the page plus a snapshot already attached.
2. Read the snapshot. Each interactive element looks like `[e12] button "Sign in"`.
3. `browser_click` / `browser_type` / `browser_select_option` with `ref: "e12"`.
4. Every action returns a fresh snapshot — read it rather than re-snapshotting blindly.

## Rules

**Never guess a CSS selector.** If the element you want is not in the snapshot, either call `browser_snapshot` with `filter: "interactive"` (fewer tokens, just actionable nodes) or `rootRef` to narrow into one subtree. Selectors are an escape hatch, not the default.

**Refs die on navigation.** After `browser_navigate`, a click that navigates, or a tab switch, every `eN` from the previous snapshot is stale. Use the snapshot that came back with the result.

**A click result of "ref could not be resolved" is not a dead end.** The server already walked cssPath → `getByRole` exact → fuzzy → `getByText`. When it reports failure, the element usually no longer exists or moved into a new frame — take a fresh snapshot before retrying. Do not retry the same ref.

**Wait for conditions, not for time.** `browser_wait` accepts `text`, `selector`, `url`, and `idle` (network quiet). Prefer text or idle over `timeMs`; fixed sleeps are the main cause of flaky automation.

**If a tool call fails with a connection error,** call `browser_get_info` first. It reports health, tab list, restart count and the last error without launching anything. The browser is normally relaunched automatically on the next action and open tabs are restored — you just need to re-snapshot.

## Reading pages efficiently

- `browser_snapshot` with `filter: "interactive"` when you only need to act.
- `browser_evaluate` for structured extraction: return JSON, for example `() => [...document.querySelectorAll('article h2')].map(h => h.textContent)`. Far cheaper than snapshotting a long list.
- `browser_screenshot` when layout or visual state matters (charts, canvas, CSS bugs). Use `ref` to capture a single element.

## Browser lifecycle

Headed by default — the user can watch and take over. Tabs and logins persist in a dedicated profile across restarts, so a first-time login survives.

- `BROWSER_MCP_CDP_URL` — attach to a browser the user already has open on a debug port instead of launching a new one.
- `BROWSER_MCP_HEADLESS` — no visible window; use only when the user does not need to watch.
- `BROWSER_MCP_PROFILE` — alternate profile directory.

`browser_close` ends the browser but keeps the profile, so logins are not lost.

## Do not

- Do not try to solve CAPTCHAs, 2FA prompts, or payment confirmation. Dialogs are auto-accepted by default; anything requiring a human decision must be handed back to the user with a screenshot.
- Do not paste cookies, tokens, or page data containing credentials into replies.
- Do not run two automation tasks against the same profile at once — they will fight over the same browser.
