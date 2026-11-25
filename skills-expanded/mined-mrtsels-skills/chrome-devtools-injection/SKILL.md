---
name: chrome-devtools-injection
description: 注入JS脚本到用户真实Chrome时使用（cdp注入、对话框、验证、单会话红线）。
metadata:
  imported_from: hermes
---

# Chrome DevTools Script Injection (live browser)

Run console scripts (e.g. shopping-cart helpers, form automators) inside the
user's real, already-logged-in Chrome. The scripts themselves never handle
login — the agent's job is: right page → inject → handle dialogs → verify.

## Prerequisites (fresh machine)

```bash
npm install -g mcporter
mcporter config add chrome-devtools --command npx --arg -y --arg chrome-devtools-mcp@latest --arg --autoConnect --scope home
```
- User Chrome must have remote debugging on: `chrome://inspect/#remote-debugging` → **Enable**
  (success marker: `~/Library/Application Support/Google/Chrome/DevToolsActivePort`
  exists with port + ws path; if stuck "starting...": Cmd+Q quit Chrome fully, reopen).
- First `mcporter call` may time out 10–30s while npx downloads the server — retry.

## Core injection pattern

```bash
mcporter call chrome-devtools.list_pages          # find the target tab
mcporter call chrome-devtools.select_page pageId=N
mcporter call chrome-devtools.evaluate_script --args '{"function": "function f(){return document.title;}"}'
```

### Pitfall 1 — IIFE must become a function declaration
Scripts are usually written as `(function(){ ... })();`. Passing that straight to
`evaluate_script` throws `Unexpected token ';'`. Strip the IIFE wrapper and pass a
function body (the MCP tool calls it):
```python
import json, os, subprocess, shlex
js = open(os.path.expanduser('~/path/to/script.js')).read()
body = js.strip()
inner = body[len('(function () {'):-len('})();')]
fn = 'function runScript() {' + inner + '\n}'
cmd = "mcporter call chrome-devtools.evaluate_script --args " + shlex.quote(json.dumps({"function": fn}))
subprocess.run(cmd, shell=True, check=True)
```
Use `os.path.expanduser('~/...')` — never hardcode `/Users/<name>/` paths (breaks portability, leaks identity in shared/repo docs).

### Pitfall 2 — key=value flags fail; use --args JSON
`mcporter call chrome-devtools.evaluate_script function=...` errors -32602.
Always pass `--args '{"function": "...", "dialogAction": "..."}'`.

### Pitfall 3 — dialogs
`dialogAction` as a string = the return value of `window.prompt` (e.g. a target
datetime). For scripts with `confirm`, use `handle_dialog action=accept|dismiss`.
A stale prompt can survive a page reload and block every later snapshot call —
dismiss it (`handle_dialog action=dismiss`) before continuing.

`evaluate_script` returning `undefined` is normal — scripts act via DOM side effects.

## Log overlay pattern (shared, single-line)

- **One shared overlay id** across related scripts (e.g. `#log-overlay`). Two
  scripts with different ids (`log-overlay` vs `validate-log-overlay`) stack two
  fixed-bottom overlays on the same page — user sees them overlap.
- Render a single line: `overlay.innerText = message` (replace, don't append).
- Apply styles (textAlign etc.) OUTSIDE the create-if-missing block so a reused
  overlay from a previous run also gets the new style.
- Style: fixed, `bottom: 0`, full width, `zIndex` high, STE100-style English
  messages (active voice, short sentences) when the user asks for clean logs.

## Navigation / page-state pitfalls

- **Jump destroys script context**: if a script redirects via `location.href`, the
  injected context dies — re-inject on the new page. Scripts should detect "am I
  on the right page" and ask before jumping.
- **SPA vs classic URL**: PeopleSoft-style apps render components under one base
  URL (`NUI_FRAMEWORK`) — decide page identity by `document.title` + DOM presence
  (e.g. `.ps-checkbox` count), NOT by URL substring.
- **Empty state has no buttons**: if the cart/table is empty, the action buttons
  don't exist. Tell the user to populate data first; don't run the script.

## Verify, don't just report "injected"

1. Read the overlay: `document.getElementById("log-overlay").innerText`.
2. For timed clicks, confirm the page reacted (success msg OR the expected
   "not open yet" rejection — rejection = click worked, timing policy said no).
3. Precise request-time check (user asks "actual vs target"):
   ```js
   var ns = performance.timeOrigin;
   performance.getEntriesByType("resource")
     .filter(e => e.initiatorType === "xmlhttprequest")
     .slice(-1).map(e => new Date(ns + e.startTime).toISOString())
   ```
   See `references/timing-verification.md` for measured numbers.

## SINGLE-SESSION RULE (hard)

**Never open a second browser instance logged into the same account.** PeopleSoft/
CUSIS detects concurrent logins and locks the ORIGINAL session with
"Restricted Multiple Login Error" — the user's real session stops being able to
enroll. This happened in production testing: a Selenium instance logged into CUSIS
simultaneously with the user's Chrome → user's cart page became a restriction page.
Recovery: quit Chrome entirely (Cmd+Q via osascript, never `killall`) → reopen →
re-login (one session only). Any test of logged-in flows reuses the existing
session; duplicate-instance logins are a red line.

## Publishing derived scripts

- If a script derives from an upstream repo that has **no LICENSE** (check
  `https://api.github.com/repos/<owner>/<repo>` → `license` field; GitHub API
  returns `None`), upstream is All-Rights-Reserved by default. Add a **Credits
  section** in the README naming the source repo + list your specific changes.
- Fully original files: state "原创实现，无外部代码引用".

## macOS gotchas

- **Case-insensitive filesystem**: `mkdir cusis-auto-reg` when `CUSIS-Auto-Reg`
  already exists silently targets the SAME directory (APFS default). To create a
  genuinely separate repo dir, use a different name (e.g. `cusis-auto`). Verify
  with `ls` that the dir really is new; `git remote -v` shows what repo you're in.
- **Check before mv**: when moving files, confirm source and destination are
  distinct dirs first (same-name-different-case is a real collision trap).

## References

- `references/timing-verification.md` — measured NTP offset, poll/buffer tuning, Performance API recipe.
