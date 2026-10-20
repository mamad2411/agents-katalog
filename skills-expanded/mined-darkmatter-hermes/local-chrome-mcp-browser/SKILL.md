---
name: local-chrome-mcp-browser
description: Use when driving open Chrome/Dia tabs via local MCP bridges.
---

# Local Chrome / Dia MCP browser

Drive tabs in Cooper's **already running** browser (often **Dia** with TRDR/HL open) through local MCP, not a fresh headless profile.

## Prefer this over

- Launching a new Chromium via `agent-browser` / puppeteer when the user says the app is **already open** and hands an MCP config
- Pro `computer_use` alone when a browser MCP can read DOM/JS (use CUA only as fallback for AX/vision or when MCP is stuck)

## Two local servers (do not confuse)

| Server | How it runs | Typical URL / launch | Owns |
|--------|-------------|----------------------|------|
| **chrome-mcp-bridge** (`mcp-chrome-bridge`) | Native-messaging host spawned by the browser extension | `http://127.0.0.1:12306/mcp` (Chrome) or **`:12307/mcp` (Dia)** | Extension tabs in that browser |
| **chrome-devtools-mcp** | stdio MCP (`npx -y chrome-devtools-mcp@latest`) | Needs real CDP: `--browserUrl=http://127.0.0.1:PORT` where `GET /json/version` works | CDP-attached Chrome |

User paste shape for DevTools MCP:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

On this machine `npx` can fail on npm overrides — prefer the installed binary:

```bash
node ~/.npm/_npx/*/node_modules/chrome-devtools-mcp/build/src/bin/chrome-devtools-mcp.js \
  --browserUrl=http://127.0.0.1:9222 --no-usage-statistics
```

**CDP check first:**

```bash
curl -sS -m 2 http://127.0.0.1:9222/json/version
# must return webSocketDebuggerUrl — bare LISTEN on 9222 with HTTP 404 is NOT enough
```

If `/json/version` 404s, do **not** thrash chrome-devtools-mcp — use chrome-mcp-bridge instead (or ask user to enable remote debugging properly).

## chrome-mcp-bridge workflow (proven)

1. **Discover listener**
   ```bash
   lsof -nP -iTCP:12306,12307 -sTCP:LISTEN
   # Dia child of Dia PID → often 12307; Chrome → 12306
   ```
2. **One Streamable HTTP client per process** (Python):
   ```python
   from mcp import ClientSession
   from mcp.client.streamable_http import streamablehttp_client

   async with streamablehttp_client("http://127.0.0.1:12307/mcp") as (read, write, get_session_id):
       async with ClientSession(read, write) as session:
           await session.initialize()
           # ALL tool calls in this same session — do not reconnect mid-task
   ```
3. **Core tools** (from `chrome-mcp-shared` / list_tools):
   - `get_windows_and_tabs` → find TRDR/HL tabIds by **title** (`XMR/USDT … TRDR`, `HYPE/USDC … TRDR`)
   - `chrome_switch_tab` `{ tabId }`
   - `chrome_get_web_content` `{ tabId, textContent: true }`
   - `chrome_read_page` `{ tabId }` (a11y tree; good for TradingView chrome)
   - `chrome_javascript` `{ tabId, code }` — code runs in an **async function body**; use `return {…}` (not IIFE-only)
   - `chrome_screenshot` — may save under `~/Downloads/screenshot_*.png` (path in result)
   - `chrome_navigate` `{ url }` — opens/activates; watch it may focus a different existing tab with same origin

4. **JS extract pattern** (keep one session):
   ```js
   const body = (document.body && document.body.innerText) || "";
   const lines = body.split(/\n+/).map(s => s.trim()).filter(Boolean);
   return { title: document.title, url: location.href, sample: lines.slice(0, 250), bodyHead: body.slice(0, 15000) };
   ```

## Singleton transport pitfall (critical)

chrome-mcp-bridge attaches **one** MCP `Server` transport. Symptoms:

- `Already connected to a transport. Call close() before connecting…`
- HTTP 500 on `POST /mcp` after a prior client died uncleanly
- First call works, reconnect fails

**Fix:** kill **only** that bridge PID (extension respawns it):

```bash
PID=$(lsof -nP -iTCP:12307 -sTCP:LISTEN -t | head -1)
kill "$PID"
# wait until LISTEN returns, then single new client
```

Do **not** open a second client "to retry" while the first session is half-open. Prefer **one long-lived session** that dumps every symbol before exit.

`Session termination failed: 400` on context exit is noisy but usually harmless if work already finished.

## TRDR / trading console specifics

- Console URL shape: `https://trdr.io/console/<workspace>/<layout>`
- Multiple symbols may share the **same console URL** with different tab **titles** — always key off title (`XMR/USDT`, `HYPE/USDC`), not URL alone.
- Heavy TradingView UIs: `chrome_get_web_content` + title + primary market strip is often enough; chart OHLC may appear in a11y (`O/H/L/C` static texts) or screenshot.
- Inactive TRDR tabs can return a **shell-only** body (Watch List headers). If so: switch tab → wait 3–6s → re-fetch; avoid `chrome_navigate` to the same console URL (can jump you to another symbol's tab).
- Fallback for chart vision: `computer_use` capture on the **Dia** window (title contains TRDR / pair).

## Hyperliquid supplement

When browser DOM is thin, HL info API fills mark/oracle/funding/OI/volume:

```bash
curl -sS https://api.hyperliquid.xyz/info \
  -H 'content-type: application/json' \
  -d '{"type":"metaAndAssetCtxs"}'
# candles:
# {"type":"candleSnapshot","req":{"coin":"XMR","interval":"4h","startTime":...,"endTime":...}}
```

## Analysis output shape (Cooper)

Concise trading memo, not a tool diary:

1. Tape table (price, 24h, venue)
2. Per-asset structure (levels, book/depth, funding/OI if perp)
3. Cross-asset / book context only if visible and relevant
4. Actionable playbook (bias, add zone, trigger, invalidation)
5. Brief tooling note only if something blocked the path

## Pitfalls

- Assuming user MCP URL port without `lsof` (12306 vs 12307)
- Reconnecting Streamable HTTP after every tool call
- Treating LISTEN on 9222 as CDP-ready without `/json/version`
- `npx chrome-devtools-mcp` under broken npm overrides — use direct node path
- Clicking market list via AX indices with zero bounds (Dia) — prefer MCP tab switch / JS
- Writing secrets or vault addresses into skills; vault names in UI are fine as session context only

## Support files

- `references/bridge-and-trdr.md` — ports, one-shot Python client, TRDR tab identity, HL tape API
- `scripts/probe_bridge.sh` — listeners + `/json/version` + MCP initialize smoke

## Related

- `agent-browser` — separate CLI/CDP automation, not the extension bridge
- `hl-funding-analysis` — deeper HL funding harvest screener
- `computer-use` — desktop fallback when MCP cannot see the window
