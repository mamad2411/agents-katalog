---
name: stealth-browser-setup
description: Configure and maintain Camofox + CloakBrowser stealth browser backend for Hermes Agent browser_* tools.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [stealth, browser, anti-detection, captcha, firefox, chromium]
    triggers: [stealth browser, anti-detection browsing, setup stealth browser, Camofox, CloakBrowser, bypass captcha]
    related_skills: [firefox-stealth-automation, captcha-bypass-browsers]
---

# Stealth Browser Setup for Hermes

Hermes `browser_*` tools (browser_navigate, browser_snapshot, etc.) normally use agent-browser with a vanilla Chromium that websites can detect. This skill configures a stealth backend using.

## Architecture

```
browser_* tools
  ├── CAMOFOX_URL set?  →  Camofox REST API → Camoufox (Firefox fork, C++ fingerprint spoofing)
  └── fallback           →  agent-browser → CloakBrowser (stealth Chromium, anti-bot patches)
```

## Layer 1: Camofox (Primary)

Camofox wraps Camoufox, a Firefox fork with C++ fingerprint spoofing that passes all browser detection tests.

### Start Camofox
```bash
cd ${MY_REPOS}/camofox-browser
MSYS_NO_PATHCONV=1 node server.js &
```

Waits ~7 seconds to download Camoufox on first run, then exposes REST API on port 9377.

### Health Check
```bash
curl -s http://localhost:9377/health
```

Returns: `{"ok":true,"engine":"camoufox","browserConnected":true,"browserRunning":true,...}`

### Verify Browsing
```bash
# Create a tab and navigate
curl -s -X POST http://localhost:9377/tabs \
  -H "Content-Type: application/json" \
  -d '{"userId":"hermes","sessionKey":"test","url":"https://example.com"}'

# Get snapshot
curl -s "http://localhost:9377/tabs/{tabId}/snapshot?userId=hermes"
```

## Layer 2: CloakBrowser (Fallback)

CloakBrowser is a custom Chromium build with stealth patches at:
`C:\\Users\\<you>\\.cloakbrowser\\chromium-146.0.7680.177.5\\chrome.exe`

Agent-browser picks it up via `AGENT_BROWSER_EXECUTABLE_PATH` env var set in .env.

### CDP Mode (for Zillow / tough sites)

For sites that block even Camoufox (e.g. Zillow's PerimeterX), launch
CloakBrowser with remote debugging and route Hermes browser tools through CDP:

```bash
# CRITICAL: must include --remote-allow-origins=* for WebSocket to work
\"${USER_HOME}/.cloakbrowser/chromium-146.0.7680.177.5/chrome.exe\" \
  --remote-debugging-port=9222 \
  --remote-allow-origins=* \      # ← REQUIRED for Chrome 146+
  --no-first-run \
  --no-default-browser-check \
  --disable-blink-features=AutomationControlled \
  --user-data-dir=\"${USER_HOME}/.cloakbrowser-profile\"
```

Without `--remote-allow-origins=*`, the WebSocket connection fails with
403 Forbidden: "Rejected an incoming WebSocket connection from the origin."

Set `BROWSER_CDP_URL=ws://127.0.0.1:9222/devtools/browser/{uuid}` in .env
to route all Hermes browser_* tools through this CDP endpoint.
This bypasses both Camoufox AND agent-browser, connecting directly to
the CloakBrowser engine.

## Layer 3: Stealth Browser Args

`AGENT_BROWSER_ARGS=--disable-blink-features=AutomationControlled,...`

Disables Chrome automation flags that sites detect.

## Configuration

All env vars are in `~/AppData/Local/hermes/.env`:

```
CAMOFOX_URL=http://localhost:9377
AGENT_BROWSER_EXECUTABLE_PATH=${USER_HOME}/.cloakbrowser/chromium-146.0.7680.177.5/chrome.exe
AGENT_BROWSER_ARGS=--disable-blink-features=AutomationControlled,--disable-features=ChromeWhatsNewUI,--no-first-run,--no-default-browser-check,--disable-sync
```

## Startup Script

`~/AppData/Local/hermes/scripts/start-stealth-browser.sh` - starts Camofox and verifies env.

### Quick Start
```bash
bash ~/AppData/Local/hermes/scripts/start-stealth-browser.sh
```

## Camofox API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | /health | Health check |
| POST | /tabs | Create tab (with userId, sessionKey, url) |
| POST | /tabs/{tabId}/navigate | Navigate to URL |
| GET | /tabs/{tabId}/snapshot | Accessibility snapshot with refs |
| POST | /tabs/{tabId}/click | Click element by ref/selector |
| POST | /tabs/{tabId}/type | Type text |
| POST | /tabs/{tabId}/press | Press key |
| POST | /tabs/{tabId}/scroll | Scroll page |
| POST | /tabs/{tabId}/evaluate | Run JavaScript |
| GET | /tabs/{tabId}/screenshot | Screenshot |
| DELETE | /tabs/{tabId} | Close tab |
| DELETE | /sessions/{userId} | Destroy session |

## Camofox Configuration

Config file: `camofox.config.json` in Camofox directory.

Plugins available:
- persistence: saves session profiles across restarts
- youtube: yt-dlp integration
- vnc: VNC server (disabled by default)

## Firefox Profile & Cookie Sync

### Profiles Available

| Name | Path | Purpose |
|------|------|---------|
| Pauls | `~/AppData/Roaming/Mozilla/Firefox/Profiles/<profile-id>.default-release-1` | Main Firefox with all accounts |
| hermes-mcp | `~/AppData/Local/hermes/firefox-profile` | Hermes MCP Firefox |
| pim-esr | `~/AppData/Local/hermes/firefox-profile-esr` | PIM ESR profile |

### Cookie Import to Stealth Browser

All 578 Firefox cookies are imported into Camoufox (`session: the operator`) so the stealth browser has the same logged-in accounts as Firefox:

- Google/Gmail
- ChatGPT / OpenAI
- GitHub
- Grok (x.ai)
- Shopify (kennyresell.com)
- MetaMask
- Namecheap
- And all other accounts

### How It Works

1. Extracts cookies from `cookies.sqlite` (Firefox stores in plain text)
2. Converts expiry from milliseconds to seconds
3. Imports via Camofox REST API: `POST /sessions/{userId}/cookies`
4. Auto-refreshed every 6 hours via cron `refresh-firefox-cookies`

### Manual Import
```bash
python ~/AppData/Local/hermes/scripts/import-firefox-cookies.py
```

You can verify accounts work by creating a tab in Camoufox and checking for login indicators.

### Firefox CDP Bridge (Alternative)
The Firefox BrowserProvider plugin at `plugins/browser/firefox/` creates a CDP↔BiDi bridge. To use it:
1. Launch Firefox with remote debugging:
   ```bash
   "C:/Program Files/Mozilla Firefox/firefox.exe" --remote-debugging-port 9222
   ```
2. Set `browser.cdp_url: ws://127.0.0.1:9222` in config.yaml
3. Or set `browser.cloud_provider: firefox` to use the bridge plugin

## Zillow / PerimeterX Workaround

Camoufox (Firefox fork) gets blocked by Zillow's PerimeterX anti-bot system. The page returns "Access to this page has been denied". Workaround:

### Option A: CloakBrowser via CDP (Recommended)
Launch CloakBrowser with remote debugging, then route browser tools through it:

```bash
# Start CloakBrowser with CDP
"${USER_HOME}/.cloakbrowser/chromium-146.0.7680.177.5/chrome.exe" \
  --remote-debugging-port=9222 \
  --no-first-run --no-default-browser-check \
  --disable-blink-features=AutomationControlled \
  --user-data-dir="${USER_HOME}/.cloakbrowser-profile"

# Verify
curl http://127.0.0.1:9222/json/version

# Set BROWSER_CDP_URL in .env so Hermes routes through it:
BROWSER_CDP_URL=ws://127.0.0.1:9222/devtools/browser/{uuid}
```

When `BROWSER_CDP_URL` is set, Hermes `browser_*` tools connect directly to the CDP endpoint, bypassing both Camoufox and agent-browser entirely.

### Option B: Firefox CDP Bridge
Launch Firefox with remote debugging and connect via the browser_tool CDP override. Firefox is less aggressively fingerprinted than Chromium for Zillow.

### Option C: Chrome DevTools MCP
The `chrome-devtools-mcp` MCP server (already configured) connects to Chrome DevTools protocol. Use its tools (`mcp_chrome_devtools_mcp_*`) for manual browsing of tough sites.

## CloakBrowser CDP Auto-Launch

For persistent CloakBrowser availability, add to the startup script:
```bash
BROWSER_CDP_URL=$(curl -s http://127.0.0.1:9222/json/version 2>/dev/null | python -c "import sys,json;print(json.load(sys.stdin).get('webSocketDebuggerUrl',''))" 2>/dev/null)
if [ -n "$BROWSER_CDP_URL" ]; then
  echo "BROWSER_CDP_URL=$BROWSER_CDP_URL" >> ~/AppData/Local/hermes/.env
fi
```

## Cookies from Firefox (for logged-in sessions)

All 578 Firefox cookies are imported into Camoufox session `the operator`. Cron `refresh-firefox-cookies` runs every 6 hours.

## Browser Selection Guide

| Site | Best Engine | Reason |
|------|-------------|--------|
| General browsing | Camoufox (default) | Best anti-detection |
| County assessor (leepa.org) | Camoufox | Works, no bot blocking |
| Clerk of Courts | Camoufox | ASP.NET, no JS complexity |
| FOSS OSINT / Google phone search | Camofox | Passes Google bot detection, unlike Chromium. See twenty-crm-administration references/phone-number-update-pattern.md |
| Google sites | Camoufox (with cookie import) | Uses Firefox cookies |
| FOSS OSINT / Google phone search | Camofox | Passes Google bot detection. Rate-limited after ~10 rapid queries. See twenty-crm-administration references/phone-number-update-pattern.md |
| Free people search (TruePeopleSearch) | NOT RECOMMENDED | Blocked by DataDome even in Camofox. Use Google search instead (indexes the same data) |
| ChatGPT / OpenAI | Camoufox (with cookie import) | Uses Firefox cookies |
| Tax collector (leetc.com) | Camoufox | Works fine |

## Troubleshooting

1. **Camofox won't start**: Check port 9377 isn't in use (`netstat -ano | grep 9377`)
2. **agent-browser can't find CloakBrowser**: Verify `AGENT_BROWSER_EXECUTABLE_PATH` points to the actual chrome.exe
3. **Firefox won't launch**: Camofox downloads Camoufox ~300MB on first run, needs ~30s
4. **Browser tools still detected**: Enable VNC in camofox.config.json or add more proxy args
5. **Zillow blocks Camoufox**: Switch to CloakBrowser CDP (see above)
6. **Google login blocks Chrome DevTools MCP**: The `mcp_chrome_devtools_mcp_*` tools use Playwright Chromium. Google's sign-in detects this as an insecure browser and refuses login with "This browser or app may not be secure." **Fix:** Use Camofox (Camoufox) instead — its Firefox-based spoofing passes Google's check. See Browser Selection Guide entry for Google sites.
7. **Google session cookies may expire in Camoufox**: Even with the 6-hour cookie refresh cron, Google sessions can expire if the account password changes or 2FA re-authenticates. The user will see accounts listed as "Signed out" on the account chooser page. **Fix:** Log in fresh through Camofox once, or copy session cookies from the main Firefox profile. See references/firefox-cookie-import.md.
8. **Camofox `/evaluate` returns plain string, not JSON:** The evaluate endpoint's `result` field is a plain string for simple expressions. Do NOT `json.loads()` the result:
   ```python
   # Correct for string results:
   resp = json.loads(urllib.request.urlopen(req).read())
   value = resp.get('result')  # "document.title" → e.g."Gmail" (plain)
   ```
   For complex expressions (objects/arrays), the result IS a JSON string that must be parsed.
9. **Camofox tab 404 after session expiry:** A Camofox tab can go stale (HTTP 404) if the tab was reaped by the browser or the session timed out. Always wrap snapshot/click in a try/except that handles 404 by creating a fresh tab. This is especially common after long idle periods (user walks away mid-auth).
10. **Watchdog script timeout == cron script timeout:** The stealth-browser-watchdog cron job (no_agent) has a default 120s script execution timeout. The watchdog script's internal `subprocess.run(timeout=120)` was also 120s — meaning the script always got killed by the cron timeout before its internal timeout could fire cleanly. **Fix:** Set the script's internal timeout to 90s or lower to leave buffer for Python startup overhead. If the script still times out, Camofox itself is failing to start (check Camofox health directly, not the watchdog wrapper).
