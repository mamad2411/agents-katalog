---
name: t3-browser
description: Drives T3 Code's built-in browser, the preview tab shown inline in the thread, through the t3-code MCP preview tools. Load before the first mcp__t3-code__preview_* call, and whenever browser work is needed inside T3 and the user names no other browser. Also for requests to open a page "in T3", "in the preview" or "so I can watch". Not for logged-in sites or pages that need the user's extensions or password manager: its profiles have no browser extensions or real logins (use playwriter). Not for headless scraping (use agent-browser).
---

# T3 browser (preview tab)

The T3 browser is a real Chromium tab in the thread's side panel. The user watches every step live and can take over. It exists only when the session runs inside T3 Code, through the `t3-code` MCP server.

## 0. Load the tools

They are deferred. Load the set before the first call:

```
ToolSearch select:mcp__t3-code__preview_open,mcp__t3-code__preview_navigate,mcp__t3-code__preview_snapshot,mcp__t3-code__preview_act,mcp__t3-code__preview_wait_for,mcp__t3-code__preview_status,mcp__t3-code__preview_evaluate,mcp__t3-code__t3_preview_close
```

Add `preview_resize`, `preview_set_appearance`, `preview_dialog`, `preview_recording_start`, `preview_recording_stop` or `t3_preview_list` only when the branch needs them. No `t3-code` server means the session is not in T3: say so and offer `agent-browser`.

## 1. The loop

1. **Open**: `preview_open({url})`. Keep the returned `tabId` and pass it to every later call. `profileId` from `preview_status().profiles` picks a T3 cookie jar, not a Brave or Chrome profile. A site that needs Magnus's real logins or 1Password belongs in `playwriter`.
   - Local dev server: `preview_navigate({target:{kind:"environment-port", port:3000, path:"/settings"}})`. Never start the server in the foreground; follow the project's dev command rules.
2. **Look**: `preview_snapshot({tabId})` returns the accessibility tree with `aria-ref` ids, diagnostics and console errors. Add `includeImage:true` only to see the pixels.
3. **Act**: `preview_act({tabId, action, locator:"aria-ref=<ref>"})`.
4. **Wait**: `preview_wait_for({tabId, text | selector | urlIncludes})` after anything that loads.
5. Repeat 2-4. Refs die on navigation, on a new snapshot and on handoff, so re-snapshot before reusing one.
6. **Close**: `t3_preview_close({tabId})` on a tab you opened for your own check. Leave it open when the user asked for it or is using it.

Done means the requested end state is visible in a fresh snapshot, not that the last action returned without error.

## 2. Actions (`preview_act`)

| action | key fields |
|---|---|
| click | `locator` or `x`+`y`, `button`, `clickCount` 1-3 |
| type | `text`, `clear:true` replaces existing text |
| press | `key` ("Enter", "Escape"), `modifiers`; click the field first to focus it |
| select | `values`, native `<select>` only; custom dropdowns are click-open then click-option |
| hover | reveals menus and tooltips |
| drag | `source`, `target` |
| upload | `paths` (absolute) answers the picker `preview_status` reports; `[]` cancels |
| scroll | `deltaY` positive is down; `locator` scrolls one container |

## 3. Other tools

| Need | Call |
|---|---|
| Show the user a screenshot | `preview_snapshot({save:true})`, then embed `![alt](screenshotPath)` |
| Read lots of data, or run JS | `preview_evaluate({expression})`. Own or unclaimed tab only. It can change page state |
| Mobile or fixed viewport | `preview_resize({mode:"preset", preset:"iphone-14-pro-max"})`; `{mode:"fill"}` resets. CSS size only, the user agent stays desktop |
| Dark or light mode | `preview_set_appearance({colorScheme:"dark"})`; `"system"` clears |
| alert / confirm / prompt | `preview_status` shows it, `preview_dialog({accept, promptText})` answers |
| Video of a flow | `preview_recording_start`, do the flow, `preview_recording_stop` returns a file path (max 50 MiB) |
| Which tabs exist | `preview_status().tabs`, or `t3_preview_list` |
| Background tab | `preview_open({open:false})` |
| Parallel subagents | each calls `preview_open({reuseExistingTab:false})` and uses only its own `tabId` |

## 4. Failures and recovery

| Symptom | Cause and fix |
|---|---|
| `await is only valid in async functions` from `preview_evaluate` | The expression runs as a plain script. Wrap it: `(async () => { …; return value; })()`. |
| `timed out after 15000ms` | The page is still loading or the tab died. Call `preview_status`, then `preview_wait_for` a real condition and retry once. Reopen the tab if it is gone. |
| Too many tabs | Close your own stale tabs: `t3_preview_list`, then `t3_preview_close` on each `tabId` you opened. |
| Tab belongs to another agent session | Open your own: `preview_open({url, reuseExistingTab:false})`. |
| No automation host | Call `preview_status` once more. If it still has no host, tell the user the preview browser is down and ask before switching to another browser tool. |
| Headless fallback for screenshots | Run Playwright from the repo (`pnpm exec playwright …`) so it resolves the repo's install. A script in a scratch directory cannot import `@playwright/test`. |

**Waiting.** `preview_wait_for` waits for a real `text`, `selector` or `urlIncludes`. To wait on a background command, use `t3_background_wait` with its task id. Never wait on text that will not appear as a stand-in for sleep.

## 5. Rules

- **Asked-for only.** Use the browser when the current request asks for browser work. Never open it unasked to verify your own edit, and never repeat an earlier turn's snapshot.
- **The user's tab is theirs.** `preview_status` reports the owner. Read any listed tab; act only on your own tab or an unclaimed one with no human in control.
- **Server tabs only.** `t3_preview_list` entries without `runtime:"server"` live in the user's local desktop app. Never pass that `tabId` to a `preview_*` tool; tell the user the tab is out of reach.
- **Page tools read data, never display it.** A chart or summary of what you found goes through `html_preview` then `html_render`, not the preview tab.
- **Public page, no browser work asked**: use web fetch instead of opening a tab.
