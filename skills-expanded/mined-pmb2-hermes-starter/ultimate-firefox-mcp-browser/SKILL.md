---
name: ultimate-firefox-mcp-browser
version: 1.0.0
description: Default/primary browser for all Hermes automation — ultimate-firefox-mcp with human-like behavior, 22 stealth measures, and 2captcha auto-solving. Use for scraping, OSINT, and any browser task.
metadata:
  hermes:
    tags: [firefox, mcp, 2captcha, stealth, scraping, osint, automation, captcha]
    triggers:
      - use the browser
      - scrape a site
      - osint browsing
      - captcha solving
      - undetected browsing
      - cloudflare bypass
      - firefox automation
    related_skills:
      - firefox-stealth-ops
      - stealth-browser-setup
      - tor-camoufox-bridge
---

# Ultimate Firefox MCP Browser (Default Browser)

the operator's directive (July 20, 2026): ultimate-firefox-mcp is the DEFAULT/PRIMARY browser for ALL Hermes browser tasks. It must look like a human using the browser in every way. 2captcha handles Cloudflare/CAPTCHAs via coded waits.

## Browser Selection Order

1. **ultimate-firefox-mcp** (Tier 1) — all scraping, OSINT, automation. Human-like input + stealth.
2. **camoufox-enhanced** (Tier 2) — only if Tier 1 gets blocked by anti-bot.
3. **tor-browser-mcp** (Tier 3) — only when Tor anonymity is required.

Do NOT reach for Playwright/Chromium (`browser_*` native tools) first — that was the old default.

## Quick Start

```bash
export TWOCAPTCHA_API_KEY='<key>'   # enables auto-solving
bash ~/AppData/Local/hermes/scripts/start-ultimate-firefox-mcp.sh
```

```python
from firefox_browser_automation import FirefoxBrowserAutomation

automation = FirefoxBrowserAutomation(headless=False)
await automation.launch(port=9239)
result = await automation.navigate("https://example.com", wait_for_captcha=True, timeout=30)
html = await automation.get_content()
await automation.screenshot("out.png")
await automation.close()
```

CLI: `python ~/AppData/Local/hermes/scripts/firefox_browser_automation.py <url> [--headless] [--screenshot out.png] [--no-captcha]`

## 2captcha Integration Pattern

- Detect CAPTCHA markers in DOM: `g-recaptcha`, `h-captcha`, `cf-turnstile`, `challenge`.
- Extract site key via `document.querySelector('[data-sitekey]')` (reCAPTCHA) or `[data-hcaptcha-sitekey]` (hCaptcha).
- Submit to 2captcha (`pip install 2captcha-python`), poll for solution (5–30s — **code explicit waits**, don't tight-loop).
- Inject: set `[name="g-recaptcha-response"]` textarea value + override `grecaptcha.getResponse`, then submit form.
- Requires `TWOCAPTCHA_API_KEY` env var; without it, skip detection gracefully.
- Supports reCAPTCHA v2/v3, hCaptcha, Turnstile, FunCaptcha, GeeTest.

## Key Files

- Wrapper: `~/AppData/Local/hermes/scripts/firefox_browser_automation.py`
- Startup: `~/AppData/Local/hermes/scripts/start-ultimate-firefox-mcp.sh` (kills stale Firefox, launches with `--remote-debugging-port 9239` + the operator's main profile, starts MCP server)
- Config doc: `~/AppData/Local/hermes/ULTIMATE_FIREFOX_MCP_CONFIG.md`
- Server repo: `${USER_HOME}/ultimate-firefox-mcp`
- Profile: `~/AppData/Roaming/Mozilla/Firefox/Profiles/<profile-id>.default-release-1` (500+ saved logins — Google, ChatGPT, GitHub, Grok, Shopify, MetaMask, Namecheap)

## Pitfall: FastMCP + pydantic v2 rejects `typing` annotations

The server crashes at startup when tool handlers use `Dict`/`Optional`/`List` from `typing`:

```
pydantic.errors.PydanticUserError: `firefox_connectOutput` is not fully defined;
you should define `Dict`, then call `firefox_connectOutput.model_rebuild()`
```

The error names ONE symbol per run — bulk-fix, never iterate one at a time. Fixed July 20, 2026 in `ultimate_firefox_mcp/tools/__init__.py`:

```bash
sed -i 's/) -> Dict\[str, Any\]:/) -> dict:/g' tools/__init__.py
sed -i 's/Optional\[str\]/str | None/g; s/Optional\[int\]/int | None/g; s/Optional\[float\]/float | None/g; s/Optional\[bool\]/bool | None/g' tools/__init__.py
sed -i 's/Optional\[List\[Dict\[str, Any\]\]\]/list | None/g; s/Optional\[List\[str\]\]/list | None/g; s/Optional\[Dict\[str, Any\]\]/dict | None/g' tools/__init__.py
sed -i 's/List\[Dict\[str, Any\]\]/list/g; s/List\[str\]/list/g' tools/__init__.py
```

Verify: `python -c "from ultimate_firefox_mcp.main import create_mcp_server; create_mcp_server()"` → "All tools registered successfully".

**Rule for any FastMCP server on pydantic ≥2.10:** annotate handlers with `dict`, `list`, `str | None` — never `typing.Dict/Optional/List`.

## Pitfall: Headless needs `--disable-gpu`

Firefox crashes headless on this Windows machine without `--disable-gpu` (D3D11 compositor fails). The wrapper adds it automatically; add it manually for any custom launch.

## Pitfall: Zombie Firefox processes

`disconnect()` closes the WebSocket but NOT the firefox.exe process. Always `taskkill //F //IM firefox.exe` in cleanup, or zombies hold port 9239 and exhaust the ~5 BiDi session limit.

## ⚠️ Known Issue: Firefox 153+ Compatibility

Firefox 153 changed `--remote-debugging-port` to serve `httpd.js` (a basic HTTP file server) instead of the CDP/BiDi protocol. The Ultimate Firefox MCP auto-detection tries `ws://.../session` (BiDi) and `http://.../json/version` (CDP) — both return 404 on Firefox 153+.

**Diagnosis:** Firefox is running on port 9239 and the port is listening, but `curl http://127.0.0.1:9239/json/version` returns 404, and the MCP's `firefox_connect` returns `connected: false`.

**Workaround (geckodriver):** Use geckodriver (installed via npm) for WebDriver automation instead:

```bash
geckodriver --port 4444 --log fatal 2>&1 &
# Then use the WebDriver HTTP API at http://127.0.0.1:4444
```

```python
# Create a session
import requests
r = requests.post('http://127.0.0.1:4444/session', json={
    "capabilities": {"alwaysMatch": {"browserName": "firefox"}}
}, timeout=30)
session_id = r.json()['value']['sessionId']

# Navigate
requests.post(f'http://127.0.0.1:4444/session/{session_id}/url',
    json={'url': 'https://example.com'}, timeout=30)
```

**Permanent fix:** Patch the MCP launcher (`launcher.py`) to set `devtools.debugger.features.cdp = true` via `--set-pref` or `about:config` before connecting, or add a `--enable-cdp` flag to Firefox startup.

## Housekeeping Note

A flat stub of this skill also exists at `~/AppData/Local/hermes/skills/ultimate-firefox-mcp-browser.md` (written directly during the setup session, July 20, 2026). This categorized version is canonical; the flat stub can be removed by the curator.
