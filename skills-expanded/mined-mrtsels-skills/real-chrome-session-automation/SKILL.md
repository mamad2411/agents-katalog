---
name: real-chrome-session-automation
description: Use when automating user's real Chrome via CDP (mcporter).
metadata:
  imported_from: hermes
---

# Real Chrome Session Automation (mcporter + chrome-devtools-mcp)

Drive the user's **actual logged-in Chrome** through Chrome DevTools Protocol via
`chrome-devtools-mcp` (called with `mcporter`). Principle: for login-gated work
(CUSIS, PeopleSoft, enterprise SPAs), reuse the user's real session/cookies —
**never spawn a temp browser instance that re-logs-in the same account**.

## Setup (autoConnect, Chrome 144+)

Default Chrome profile rejects `--remote-debugging-port` (136+ security). Use
the inspect-page toggle instead:

1. User opens `chrome://inspect/#remote-debugging` → **Enable**.
   Success marker: `~/Library/Application Support/Google/Chrome/DevToolsActivePort`
   exists and contains `port` + `ws path` lines. If stuck on "starting...":
   Cmd+Q fully quit Chrome, reopen, re-Enable.
2. Register the server (survives Hermes restarts):
   ```bash
   mcporter config add chrome-devtools --command npx --arg -y \
     --arg chrome-devtools-mcp@latest --arg --autoConnect --scope home
   ```
3. User clicks **Allow** on the authorization prompt.
4. First call after registration is slow (npx cold start); retry with a longer
   timeout instead of assuming failure.
5. **`Could not find DevToolsActivePort` even though the file exists** (2026-08,
   macOS): Node 22+ resolves `localhost` to `::1` (IPv6) first, but Chrome's
   debug port listens only on `127.0.0.1` — the autoConnect ws connect fails
   and the MCP wraps the real cause into a misleading "Could not find
   DevToolsActivePort" error (the readFile/parse succeeded; the ws connect is
   what failed). Verify the resolution order:
   ```bash
   node -e "require('dns').lookup('localhost',{all:true},(e,a)=>console.log(JSON.stringify(a)))"
   # bad: [{"address":"::1","family":6},...]  →  good: 127.0.0.1 first
   ```
   Fix: restart the mcporter daemon with IPv4-first resolution (survives until
   the daemon is restarted without the env var):
   ```bash
   mcporter daemon stop
   NODE_OPTIONS=--dns-result-order=ipv4first mcporter daemon start
   ```
   Also: after the Auto 2FA popup closes, the MCP's selected-page state can get
   stuck ("The selected page has been closed" on every call, even list_pages) —
   restart the daemon the same way; the Chrome session/login survives.

### Chrome 151: default profile refuses `--remote-debugging-port` (profile-copy recipe)

2026-08-11 verified on this machine: launching Chrome with
`--remote-debugging-port=9222` (via `open -a` OR the binary directly) while
using the **default profile** prints

```
DevTools remote debugging requires a non-default data directory.
Specify this using --user-data-dir.
```

and the DevTools server **never starts** — no listener on 9222, no
DevToolsActivePort written (the file you see may be a stale leftover from a
previous run; it lies). The `chrome://inspect` Enable toggle also can't help
when Chrome isn't running at all.

**Working recipe (preserves extensions + cookies — Auto 2FA still works):**

1. Fully quit Chrome: `osascript -e 'tell application "Google Chrome" to quit'`
   (never killall — loses the tab session).
2. Copy the whole profile to a debug dir:
   ```bash
   ditto "$HOME/Library/Application Support/Google/Chrome" \
         "$HOME/Library/Application Support/Google/Chrome-Debug"
   rm -f "$HOME/Library/Application Support/Google/Chrome-Debug"/Singleton{Lock,Cookie,Socket} \
         "$HOME/Library/Application Support/Google/Chrome-Debug/DevToolsActivePort"
   ```
3. Launch the binary **directly** (arg passing via `open -a` proved
   unreliable — the flag appeared in ps but the server never bound):
   ```bash
   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
     --remote-debugging-port=9222 \
     --user-data-dir="$HOME/Library/Application Support/Google/Chrome-Debug"
   ```
4. Chrome 151 does **NOT** write DevToolsActivePort into the custom profile
   dir, and mcporter reads the **default** path. Fetch the ws path over HTTP
   and hand-write the file where mcporter looks:
   ```bash
   WS=$(curl -s http://127.0.0.1:9222/json/version | python3 -c "import json,sys;print(json.load(sys.stdin)['webSocketDebuggerUrl'])")
   printf '9222\n%s\n' "${WS#ws://127.0.0.1:9222}" \
     > "$HOME/Library/Application Support/Google/Chrome/DevToolsActivePort"
   ```
   (`webSocketDebuggerUrl` = `ws://127.0.0.1:9222/devtools/browser/<uuid>` —
   strip the `ws://...` prefix; the file format is `port` + newline + ws path.)
5. `mcporter call chrome-devtools.list_pages` — reconnects with "page ids have
   changed", re-select pages.

Always verify the server is actually up with
`curl -s http://127.0.0.1:9222/json/version` (curl fails = server not started)
before blaming mcporter's "Could not find DevToolsActivePort".

## Core workflow

```bash
mcporter call chrome-devtools.list_pages        # page ids change after ANY Chrome restart
mcporter call chrome-devtools.select_page pageId=2
mcporter call chrome-devtools.take_snapshot     # accessibility tree w/ uid= refs
mcporter call chrome-devtools.fill uid=1_4 value="..."
mcporter call chrome-devtools.click uid=1_6
mcporter call chrome-devtools.evaluate_script --args '{"function": "function f(){...}"}'
```

## evaluate_script — the 3 gotchas

1. **Must pass a function declaration, not an IIFE.** An IIFE string
   (`(function(){...})();`) fails with `Unexpected token ';'`. Strip the
   wrapper: `body[len('(function () {'):-len('})();')]` → wrap as
   `function runX() { <inner> }`.
2. **mcporter key=value syntax can't express the `function` arg** (errors
   -32602) — always use `--args '{"function": "..."}'` JSON form.
3. **Dialogs**: pass `dialogAction` to `evaluate_script` — `"accept"`,
   `"dismiss"`, or a **string = the response for `window.prompt`**. Use it to
   auto-answer prompt() dialogs (e.g. feed a target time to a countdown
   script). Alternative: `chrome-devtools.handle_dialog action=accept
   promptText=...`.

**Page navigation destroys the script context.** If the script does
`location.href = ...` (URL-redirect logic), the running script dies on the new
page — re-paste/re-run on the destination page. This is normal, not a bug.

## Chrome 151+ autoConnect constraints

- The autoConnect debug channel is **WebSocket-only**: no HTTP `/json/version`
  endpoint. Selenium `debugger_address` attach fails with
  `ERR_CONNECTION_REFUSED`; raw `websockets` handshake gets **HTTP 403**.
  chrome-devtools-mcp is the only client that works — don't burn time on
  Selenium/Playwright attaching to an autoConnect Chrome.
- **Single CDP client at a time.** mcporter holds the connection; stop the
  daemon (`mcporter daemon stop`) to release it, or other clients (and a second
  mcporter call) get connection-refused.
- After Chrome restart: debug setting persists, DevToolsActivePort regenerates
  with a new ws path, page ids change, and mcporter auto-reconnects (with a
  "page ids have changed" note) — re-list pages and re-select.

## Extension popups & chrome-extension:// pages

Opening an installed extension's popup/options page (e.g. Auto 2FA) via CDP:

1. **Enumerate installed extensions**: `new_page url="chrome://extensions/" background=true`
   (background tab — does not touch the user's active tab), then `take_snapshot`.
   With Developer mode on, each card shows `ID: <32-hex>` as StaticText.
   Alternative: grep 32-hex IDs from
   `~/Library/Application Support/Google/Chrome/Default/Preferences`.
2. **Find the popup entry**: read
   `~/Library/Application Support/Google/Chrome/Default/Extensions/<id>/<version>/manifest.json`
   → `action.default_popup` (MV3) gives the path (e.g. `popup.html`).
3. **Open it — in a NEW tab, never on the active page**: `new_page url="chrome-extension://<id>/popup.html"`.
   - `new_page` creates the extension page as the selected tab (confirmed via `take_snapshot`), even though `list_pages` may show it under a stale title or omit it — trust `take_snapshot`, not the page list.
   - **NEVER `navigate_page` the currently-active tab to a chrome-extension:// URL while that tab holds in-flight state (e.g. a Duo auth prompt).** It destroys the auth flow and the user will (rightly) call this out. `navigate_page` only if the selected page is disposable (e.g. a scratch chrome://extensions tab).
   - There is NO `navigate` tool — the correct name is `navigate_page`.
4. **Why not the real popup**: CDP cannot click the browser toolbar icon (that's
   browser UI, not page DOM). Loading popup.html renders identical content and
   wakes the MV3 service worker — functionally equivalent for extracting the
   popup's data (2FA codes, device lists, "Try Again" state).
5. **Poll state, then close**: after `new_page`, the extension page is the
   **selected** tab — poll with `take_snapshot` directly at ~2s intervals until
   the expected state text appears (e.g. `StaticText "Logged in!"`). Note:
   chrome-extension pages are **omitted from `list_pages`**, so there is NO page
   id for `select_page`/`close_page` — close the tab with
   `evaluate_script` running `window.close()` (works when the popup is the
   selected page; response will say "The selected page has been closed"), then
   `list_pages` + `select_page` to restore the original tab. If the popup shows
   a "no pending login" state (e.g. "No logins found!"), the push hadn't
   arrived or timed out — return to the auth page, click "重试"/retry, and poll
   again.

Pitfall: `take_snapshot` output is large and gets truncated — extension-card
snapshots carry base64 icon data and can be 30K+ chars. Pass `filePath=` to
save the full snapshot, then grep for `heading "..." level="3"`,
`button "On|Off"`, and `ID: <hex>` lines instead of reading the raw dump.

### Extension ID: permanent vs ephemeral (verify before hardcoding)

Extension IDs are NOT always stable — check the manifest before hardcoding one
in a skill/script:

- **Web Store install** (manifest has `key` + `update_url` =
  `https://clients2.google.com/service/update2/crx`): ID is **permanent**,
  derived from the publisher's public key. Safe to hardcode.
- **Load unpacked WITHOUT `key` in manifest** (e.g. a fresh `npm run build`
  artifact): Chrome generates a **random ID per load** — hardcoding it breaks
  after any reinstall. Must re-discover the ID.

Verify ID derivation (works for any manifest with `key`):
```bash
python3 -c "
import json, base64, hashlib
m = json.load(open('$HOME/Library/Application Support/Google/Chrome/Default/Extensions/<id>/<ver>/manifest.json'))
key = base64.b64decode(m['key'])
chars = 'abcdefghijklmnop'
digest = hashlib.sha256(key).digest()[:16]
print(''.join(chars[(b>>4)&0xF] + chars[b&0xF] for b in digest))  # == <id> when key present
"
```
Re-discover IDs from `chrome://extensions/` snapshot or
`~/Library/Application Support/Google/Chrome/Default/Preferences`.

## ⚠️ Session-lock safety rule (critical)

Systems that lock sessions (CUSIS, PeopleSoft, bank portals) detect a second
login from the same account and **restrict the ORIGINAL session** — e.g. CUSIS
shows "Restricted Multiple Login Error" and prohibits further enrollment
actions in the first window. Causes: launching a second Chrome instance
(Selenium/temp profile) logged into the same account.

- NEVER re-login the same account in a second browser/instance while the user's
  session is live.
- If testing Python/Selenium tooling against a logged-in service: reuse the
  existing session (debug_port attach) or schedule the test when the user can
  re-login — do NOT open a second instance with the same credentials.
- Recovery: fully quit Chrome (Cmd+Q), reopen, re-login in the single window.

## Timing: measure, don't guess

Before tuning sleeps in injected scripts, measure real DOM latency:
checkbox→click can be ~2ms; page loads <1.5s. Then set conservative margins
(click gap ~200ms, page load poll 300ms intervals instead of fixed sleeps).
Poll for element appearance rather than fixed `setTimeout` when the wait is
bounded by page load.

## Verifying injected-script behavior (validated pattern)

1. **Read the script's own log overlay** back through evaluate_script:
   ```js
   // in page: overlay element with id "log-overlay" (or similar), lines appended
   function check() {
     var ov = document.getElementById("log-overlay");
     return JSON.stringify(ov ? ov.innerText.split("\n").slice(-6) : "NO OVERLAY");
   }
   ```
   Confirms the script ran without re-reading its source.
2. **Verify UI geometry** for bottom-pinned overlays (user prefers log bars
   pinned to the bottom of the viewport):
   ```js
   function geo() {
     var r = document.getElementById("log-overlay").getBoundingClientRect();
     return JSON.stringify({ bottom: Math.round(r.bottom), vh: window.innerHeight });
   }
   // bottom === vh  → flush against viewport bottom
   ```
3. **Feed time/prompt values to countdown scripts** via `dialogAction` string
   (e.g. a future HH:MM:SS) — then confirm the waiting loop logs
   ("Waiting..." spam) and the deadline click fires exactly on time.
4. **Watch for silent-failure bugs in injected scripts**: an Enroll/Validate
   click without element-existence check + try/catch prints "success" even when
   nothing was clicked. Wrap clicks and log the real error.
5. **Scripts that redirect destroy their own context** — re-inject on the
   destination page before testing the rest of the flow.

## Validating "step X is unnecessary" — confirm the auth actually happened

Before concluding a step is optional (e.g. "login worked without opening the
popup"), verify the auth transaction **actually exercised the flow**:

- **Compare transaction IDs across attempts.** In Duo, the auth page URL is
  `duosecurity.com/prompt/<TXID>?authkey=...`. If a "successful" retry shows the
  **same TXID** as the earlier attempt, Duo short-circuited with an
  already-approved session — the flow never ran 2FA, so it proves nothing about
  whether a step is needed.
- **Check the page actually reached the waiting state** ("等待批准…" /
  "正在等待批准") rather than jumping straight to the destination.
- Real lesson (2026-08): a reused TXID was wrongly taken as evidence that the
  Auto 2FA popup needn't be opened — the user corrected it. Only fresh-TXID
  attempts count as evidence.
- **Sanctioned test ground (user directive)**: repeated Duo-flow testing happens
  ONLY at `https://duo.itsc.cuhk.edu.hk/` (device-management portal). Do not
  use other sites to iterate on Duo behavior.
- **Loop-back pattern enables repeat tests without logout** (verified 5/5,
  2026-08): at the device-management portal, checkbox + "Go to Enroll/Manage
  Devices" triggers a fresh 2FA, and after approval the page **returns to the
  same portal page** — ready to trigger again immediately. Never Logout to
  "reset" for another round: Logout clears the ADFS session and forces a full
  credential re-login, which is both slower and outside the sanctioned test
  ground.

## Injected-script copy: STE100 English (user preference)

The user wants script UI/log messages in Simplified Technical English
(ASD-STE100) style — see the `simplified-technical-english` skill:
active voice, short sentences, consistent terms, no "will"/"e.g."/etc.
Not Chinese/colloquial ("Reg緊！" → "The script clicks the Enroll button.").
Keep log strings English even when the user chats in Chinese.

## References

- `references/cusis-course-csv-extraction.md` — CUSIS View My Classes → 课程 CSV
  提取（innerText 解析、多时段配对、验收流程），供日历导入。
- `references/cdp-connection-notes.md` — exact error signatures + recovery for
  the 151 autoConnect / Selenium / WebSocket failure paths.
- `references/approval-mode-allow-dialog.md` — why the per-connection Allow
  dialog appears (approval mode is BY DESIGN), and the verified
  `--remote-debugging-port` precedence path (skips the dialog but loses real
  session state on a custom profile; default dir is refused by Chrome 136+).
