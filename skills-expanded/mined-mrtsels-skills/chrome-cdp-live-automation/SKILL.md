---
name: chrome-cdp-live-automation
description: Use when driving the user's real Chrome via CDP.
metadata:
  imported_from: hermes
---

# Chrome CDP Live Automation (chrome-devtools-mcp autoConnect)

Drive the user's **real, logged-in** Chrome (cookies/session intact) via CDP.
Preferred over temporary browser instances whenever the target site needs the
user's login state (CUSIS, PeopleSoft, enterprise portals, university systems).

## Setup

1. User opens `chrome://inspect/#remote-debugging` → clicks **Enable**.
   If stuck on "starting...": Cmd+Q Chrome fully, reopen, re-Enable.
   Success marker: `~/Library/Application Support/Google/Chrome/DevToolsActivePort`
   exists with port + ws path.
2. Register the MCP server (no Hermes restart needed):
   ```bash
   mcporter config add chrome-devtools --command npx --arg -y --arg chrome-devtools-mcp@latest --arg --autoConnect --scope home
   ```
3. User clicks Allow on the authorization prompt.
4. Start daemon: `mcporter daemon start` (first call may time out while npx
   boots the server — retry after a few seconds).

## Core usage

```bash
mcporter call chrome-devtools.list_pages          # pageId changes after reload/restart
mcporter call chrome-devtools.select_page pageId=2
mcporter call chrome-devtools.take_snapshot       # grep for uid=... textbox/button
mcporter call chrome-devtools.fill uid=1_4 value="user@example.com"
mcporter call chrome-devtools.click uid=1_6
```

### evaluate_script — the critical quirks

- **Must be a function declaration, NOT an IIFE.** Passing
  `(function(){ ... })()` fails with `Unexpected token ';'`. Strip the
  wrapper and pass the body as `function f() { ... }`.
- mcporter key=value syntax breaks on the `function` param (error -32602).
  Always use JSON:
  ```bash
  mcporter call chrome-devtools.evaluate_script --args '{"function": "function f(){return JSON.stringify({a:1});}"}'
  ```
- **`dialogAction` answers `window.prompt`/`confirm`/`alert`** while the script
  runs: pass a string as the prompt response, or `"accept"`/`"dismiss"`.
  Separate tool: `handle_dialog action=accept` (+ `promptText`).
- Loading a script that sets `location.href` (redirect) destroys the script
  context — everything after the redirect is lost. Re-paste the script on the
  new page (same as console-paste behavior).
- Use `JSON.stringify` inside the function and return it — output is JSON-safe.

### Inspecting state

`evaluate_script` returning `document.body.innerText` slices is the fastest
way to read PeopleSoft/SPA page state (titles, error dialogs, "Restricted"
messages). `getComputedStyle(el)` confirms real rendering vs inline style.

## Pitfalls

1. **autoConnect is WebSocket-ONLY, single client.** Chrome 136+ in
   autoConnect mode exposes no HTTP `/json` endpoint (Selenium's
   `debugger_address` fails with connection refused; direct WebSocket
   handshake gets HTTP 403 for non-official clients). Only the official
   chrome-devtools-mcp client can attach. Do NOT try Selenium/Playwright
   against an autoConnect'd Chrome — start a separate instance instead.
2. **One CDP client at a time.** If another tool holds the connection
   (e.g. a previous mcporter session), stop it first (`mcporter daemon stop`),
   else the new client cannot attach.
3. **NEVER open a second browser instance logged into the same account**
   while a live session exists. Sites like CUSIS detect multiple logins and
   **lock the ORIGINAL session** ("Restricted Multiple Login Error" page;
   enrollment actions prohibited). Recovery: fully quit Chrome (Cmd+Q),
   reopen, re-login — new session is clean. Always reuse the existing session
   (debug_port / autoConnect), never spawn a second logged-in instance to
   "test".
4. **setInterval in background tabs is throttled.** Nominal 10 ms interval
   measured at avg ~50 ms, max ~95 ms. Don't trust nominal polling rates for
   timed actions; pick an honest interval (50 ms is fine) and verify with
   `performance.now()` sampling.
5. **Inline styles on reused elements.** If the script reuses an overlay/div
   created by a previous run, `if (!el) { create + set styles }` skips style
   updates. Re-apply styles unconditionally after the guard.
6. Reload/navigation resets pageIds and the selected page — re-call
   `list_pages` and `select_page` after any navigation.
7. **`list_pages` hides `chrome-extension://` pages** (extension popups,
   options). The popup tab IS reachable — after `new_page` it becomes the
   selected page and `take_snapshot` reads it — but it has no pageId you can
   `close_page`. Close it via `evaluate_script`:
   `function f(){window.close(); return "closed";}` (works when the popup is
   the selected page). Note the closing popup makes the connection report
   "The selected page has been closed" for the next 1-2 calls — re-run
   `list_pages`/`select_page` until a real page is selected.
8. **`navigate_page` replaces the CURRENT selected page.** If you need a
   second page (extension popup, settings, another site) while a live page
   matters (auth flow in progress), use `new_page` — never navigate the
   working page away. Navigating a Duo/SSO auth page mid-flow destroys the
   auth session. New page = `mcporter call chrome-devtools.new_page url="..."`
   (background=true opens without stealing focus).
9. **State check before acting** — when an automation step only matters in
   some states, read `location.href`/`document.body.innerText` first and skip
   if not applicable. E.g. an SSO 2FA helper must check the current URL is
   still the auth page (`duosecurity.com`) before opening the code-generator
   popup: session cookies ("remember me") can auto-pass auth, so the popup
   would open to nothing ("No logins found!").

## Fixed-DOM-id JS clicks (vs uid clicks)

`click uid=...` uses the accessibility snapshot's dynamic uid, which changes
every snapshot. For pages with stable element ids, one `evaluate_script` can
replace the whole click sequence and is id-agnostic:

```bash
mcporter call chrome-devtools.evaluate_script --args '{"function": "function f(){var c=document.getElementById(\"chkPresentation\"); if(c && !c.checked){c.checked=true;} if(typeof persuedPresentation===\"function\"){persuedPresentation();} var b=document.getElementById(\"btnManageDevices\"); if(b){b.disabled=false; b.style.filter=\"none\"; b.click();} return \"triggered\";}"}'
```

Pattern: check element exists → set state → enable if disabled → `.click()`.
This defeats `<input type="button">` + inline-onclick cases where synthetic
mouse events never fire the handler. Verify by reading `location.href` after
(triggering actions navigate away; if URL didn't change the click failed —
retry or fall back to manual uid clicks).

## Daemon recovery (sticky "selected page closed")

If `list_pages` returns only `The selected page has been closed` repeatedly
(the selected page died and the connection is stuck), recover with:
```bash
mcporter daemon stop && sleep 2 && mcporter daemon start && sleep 3
mcporter call chrome-devtools.list_pages
```
Do NOT burn time on `select_page` retries first — the daemon restart clears
the stale selected-page state in one step.

## Timed clicks (auto-registration style)

Design rule: **click must fire AFTER the target time, never before.**
- Measure the local clock offset vs an authoritative source:
  `sntp -sS time.apple.com` (NTP, sub-ms precision; repeat 3× and take the
  max offset as the design value). Note: transparent proxies hijack NTP DNS
  to reserved ranges (198.18.x.x) — offsets are still readable and valid.
- Buffer must satisfy: `buffer > |clock offset| + poll lag + margin`.
- Pattern: poll every N ms checking `target <= new Date()`, then wait
  `buffer` ms before clicking. With a ~70 ms offset: 50 ms poll + 80 ms
  buffer → click lands 80–130 ms late, never early.
- Cross-check the server's own time via the HTTP `Date` header
  (`curl -sI https://host/`) — but it is SECOND-granularity only (±500 ms),
  use it only for coarse confirmation, NTP for the real number.

## Launching Chrome with remote debugging (Chrome 151+)

**Chrome 151+ refuses `--remote-debugging-port` on the DEFAULT profile.** Even
with the flag passed, the process runs but the port never listens and no
DevToolsActivePort file is written; the browser's stderr shows:

```
DevTools remote debugging requires a non-default data directory. Specify this using --user-data-dir.
```

The `chrome://inspect → Enable` flow still works, but for scripted launches
(Chrome fully closed, need debugging from boot) the working recipe is:

```bash
# 1. Quit Chrome (AppleScript preserves tabs), remove stale port file
osascript -e 'tell application "Google Chrome" to quit'
rm -f "$HOME/Library/Application Support/Google/Chrome/DevToolsActivePort"

# 2. Copy profile to a new dir (keeps extensions + login state, ~350MB)
ditto "$HOME/Library/Application Support/Google/Chrome" \
      "$HOME/Library/Application Support/Google/Chrome-Debug"

# 3. Clean singleton locks in the copy
rm -f "$HOME/Library/Application Support/Google/Chrome-Debug/"{SingletonLock,SingletonCookie,SingletonSocket,DevToolsActivePort}

# 4. Launch via terminal background (NOT `open`, NOT trailing &) with BOTH flags
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/Library/Application Support/Google/Chrome-Debug"

# 5. mcporter only reads DevToolsActivePort at the DEFAULT profile path,
#    and the debug instance may not write one — construct it manually:
WS=$(curl -s http://127.0.0.1:9222/json/version | python3 -c "import json,sys; print(json.load(sys.stdin)['webSocketDebuggerUrl'])")
printf '9222\n%s\n' "${WS#ws://127.0.0.1:9222}" > "$HOME/Library/Application Support/Google/Chrome/DevToolsActivePort"
mcporter call chrome-devtools.list_pages   # then it connects
```

Diagnosis order when mcporter says "Could not find DevToolsActivePort":
1. `curl -s http://127.0.0.1:9222/json/version` — if this fails, the port
   isn't listening at all (don't trust a stale DevToolsActivePort file: it
   survives from a previous session even when Chrome is closed).
2. Check the browser process stderr for the "non-default data directory"
   message.
3. Note: a fresh `ditto` copy of the profile reuses the same browser UUID in
   /json/version — that is normal, not a stale file.

## Reading PeopleSoft NUI page data (buttons invisible to querySelector)

PeopleSoft NUI (CUSIS 2026+) renders interactive course blocks as
`DIV.ps_box-group psc_layout` with an `A.ps-link` header — **`querySelectorAll("button")`
returns 0** even though the accessibility snapshot shows buttons. Don't fight
the DOM; parse `document.body.innerText` line structure instead:

- Course header: `^([A-Z]{2,6} \d{4}) (.+)$` (e.g. `CHLT 1002 University Chinese II`)
- Component line: `^\(\s*(\d+)\s*\)\s*(.*?)\s*-\s*(\w+)\s*$`
  (e.g. `( 10068 ) HL - LEC`; some rows have empty section: `( 4884 ) - - LEC`)
- After a component: date lists (`9/10, 9/17, ...` or `2026/09/07 - 2026/11/30`),
  `Days: X` / `Times: Y` lines, and room lines — **paired by order** (a LEC
  with Tue+Thu slots emits two date lists + two day/time pairs + two rooms;
  keep them index-aligned when expanding).
- Extract via mcporter `evaluate_script` returning `document.body.innerText`
  (JSON-encoded), then parse in Python. Never trust course names by guessing —
  read the actual page text.

## Log overlay pattern (user preference for CUSIS scripts)

Bottom-anchored, single-line, centered, ms-precision timestamps, STE100
English (active voice, short sentences — see `simplified-technical-english`
skill). Example message style: "The script clicks the Enroll button." /
"Waiting for the registration time. Current time: 12:24:11.863".
User iterated left → right → center; center is the settled choice.

## References

- `references/measured-timings.md` — real measurements from a CUSIS auto-reg
  session (clock offsets per NTP source, setInterval throttle, click latency).
- `references/cusis-timetable-to-calendar.md` — CUSIS View My Classes → CSV →
  Google Calendar pipeline: NUI text extraction, per-date event expansion
  (not RRULE), bulk create/verify/delete with google-workspace skill, the
  `calendar list --max 25` truncation pitfall, and the user's event-format
  convention (title=course code, description=course name, location=room).
