---
name: aim-browser
description: >
  Shared Co-Pilot Chromium CDP engine & CLI for AGY, Grok, and OpenCode:
  live aim-connect Browser split-pane streaming, multi-subagent tab isolation
  (--tab <lease>), <5ms zero-VLM self-healing Website Maps (--map-record /
  --map-click / --map-type), DOM/AX extraction, and human login handoff.
---

# `aim-browser` — Co-Pilot CDP Engine & Multi-Agent Playbook

Cross-platform Node.js Chromium CDP engine (`127.0.0.1:9222`) shared directly with the Operator's **`🌐 Browser`** split-pane inside `aim-connect`. Prefer one-verb skills (`aim-page-fetch`, `aim-google-ai`, `aim-google-web`, `aim-login-hold`, etc.) for single-shot lookups; use `aim-browser` whenever you need live interactive browsing, multi-tab subagent work, form automation, or recurring Website Maps.

> [!IMPORTANT]
> **WHY USE `aim-browser` IN CLI / TMUX SESSIONS**
> - Unlike `agy`'s `/browser` command (which requires an interactive desktop Chrome `v144+` allow-prompt and single-session lock), `aim-browser` runs natively on Linux, WSL2, and Windows 11 (`src/daemon.js`), streams live into the Operator's **`🌐 Browser`** split-pane with real-time `🤖` cursor HUD pills, and lets parallel subagents work simultaneously in isolated background tabs.

---

## 1. The 3 Mandatory Co-Pilot Rules

1. **Always Isolate Your Tab (`--tab <lease>`):**
   Pass `--tab <subagent-or-task-name>` (for example `--tab market-brief` or `--tab subagent-1`). Leased tabs run with `stealFocus: false` so parallel subagents **never** hijack the Operator's active tab or stomp each other, while emitting live cursor HUD events for your tab chip.
2. **Never `--stop` a Shared Session:**
   `--start` is idempotent. When your subagent finishes a temporary tab, clean up ONLY your tab via `--release-tab <lease>` — **never** run `--stop` unless the Operator explicitly asks to shut down the entire browser daemon.
3. **Human-in-the-Loop Login / 2FA Handoff (`🎮 Control ON`):**
   Never bypass or solve CAPTCHAs/2FA yourself. Leave the login page open on your `--tab <lease>`, tell the Operator to click your `🤖 <lease>` tab in **`🌐 Browser`**, toggle **`🎮 Control ON`** (or **`🔑 Type / 2FA`**), complete sign-in, and reply *"continue"* so you resume on the authenticated cookie session.

---

## 2. Invoking From Any Repository

Run directly from **any** working directory using `${AIM_BROWSER_ROOT:-$HOME/aim-browser}`:

```bash
BROWSER_CLI="${AIM_BROWSER_ROOT:-$HOME/aim-browser}/aim-browser.skill/scripts/run.js"

# 1. Start daemon (idempotent, stays minimized off Operator desktop) + open isolated tab + list elements:
node "$BROWSER_CLI" --start --tab agent-work --open "https://finance.yahoo.com" --elements

# 2. Type & click inside your leased tab without stealing focus from other tabs:
node "$BROWSER_CLI" --tab agent-work --type 0 "NVDA" --keypress enter --wait 1500 --content

# 3. Release & close only your leased tab when done:
node "$BROWSER_CLI" --release-tab agent-work
```

---

## 3. Zero-VLM Fast Path & Self-Healing Website Maps (`< 5ms`, `0` Vision Tokens)

95% of navigation and layout checks require **zero screenshots or vision models**:

1. **Fast DOM / Accessibility Readout (`< 5ms`):** Use `--elements` (numbered visible interactive elements with exact `(x, y)` coordinates), `--content`, or `--content-ax` instead of burning tokens on screenshots.
2. **Popup & Mobile Overflow Math:** Use `--check-occlusion <x> <y>` (`document.elementFromPoint`) to detect modal/cookie blockers and `--check-layout` to detect horizontal CSS overflow deterministically.
3. **Self-Healing Website Maps (`~/.cache/aim-browser/maps/<domain>.json`):**
   On recurring portals or `localhost` apps, record multi-anchor landmarks once so repeat visits run in `< 5ms` and automatically self-heal if CSS classes change:
   ```bash
   # Visit #1 — Record landmarks by element index or CSS selector:
   node "$BROWSER_CLI" --tab clerk --map-record searchInput 0 --map-record submitBtn "#search-btn"

   # Visits #2..N — Auto-heals drifted CSS via ARIA/text/heading anchors & dismisses blocking modals:
   node "$BROWSER_CLI" --tab clerk --url "https://portal.example.com" \
     --map-type searchInput "vasquez" \
     --map-click submitBtn
   ```

---

## 4. CLI Flag Reference (Executed Left → Right)

- **Lifecycle:** `--start` · `--start-minimized` · `--start-visible` · `--show` · `--minimize` · `--maximize` · `--check` · `--stop`
- **Multi-Tab & Subagent Leases:** `--tab <lease|new>` · `--actor <name>` · `--leases` · `--release-tab <lease>` · `--list` / `--tabs` · `--open <url>` · `--use <index>` · `--close [<index>]`
- **Navigate & Wait:** `--url <url>` · `--wait-ready` · `--wait-selector <css>` · `--wait <ms>` · `--scroll-to-bottom`
- **Discover & Layout Math:** `--elements` · `--content` · `--content-ax` · `--html` · `--check-occlusion <x> <y>` · `--check-layout` · `--screenshot <path>` (`--fullpage`)
- **Self-Healing Site Maps:** `--map-record <key> <selector|index>` · `--map-click <key>` · `--map-type <key> <text>` · `--map-show [<domain>]`
- **Interact:** `--click <css|index>` · `--tap <index>` · `--tapxy <x> <y>` · `--taptestid <id>` · `--type <index> <text>` · `--textbox <text>` · `--keytype <text>` · `--keypress <enter|tab|backspace|escape>` · `--keycombo ctrl+enter`
- **Advanced:** `--eval "<js>"` · `--frame <id|main>` · `--block-media` · `--spy <regex>` · `--dlpath <dir>` · `--upload <css> <file>` · `--resize <w> <h>`

## 5. Programmatic Node.js API

```javascript
import {
  AimBrowser,
  startDaemonAsync,
  acquireTabLease,
  recordLandmark,
  actOnLandmark,
} from 'aim-browser';
```
