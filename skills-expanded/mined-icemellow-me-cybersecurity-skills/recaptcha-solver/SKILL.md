---
name: captcha-solver
description: Self-hosted CAPTCHA solving servers — reCAPTCHA v2 (CaptchaPlugin ONNX), Cloudflare Turnstile + JS challenges (Playwright), with 2captcha and FlareSolverr compatible APIs
version: 2.0
tags: [captcha, recaptcha, turnstile, cloudflare, bypass, automation, browser, playwright, 2captcha, flaresolverr]
---

# CAPTCHA Solver — Self-Hosted Solving Infrastructure

## Overview

Two self-hosted CAPTCHA solver servers running on the VPS, both exposing **2captcha-compatible APIs**. The Turnstile solver additionally provides a **FlareSolverr-compatible API** for drop-in replacement.

| Solver | Port | Method | Status |
|--------|------|--------|--------|
| **reCAPTCHA v2** | 8866 | CaptchaPlugin ONNX models + CDP | Working (extension deps) |
| **Turnstile/CF** | 8877 | Playwright browser automation | ✅ Fully working |

**GitHub repos** (private, `icemellow-me`):
- `recaptcha-v2-solver`
- `turnstile-solver`

---

## API Quick Reference

**API Key:** `8010000000ccojr5nrbg516w5jvw1wu9`

### 2captcha-compatible API (`/in.php` + `/res.php`)

**reCAPTCHA v2 (port 8866):**
```
POST /in.php  key=KEY&method=userrecaptcha&googlekey=SITE_KEY&pageurl=PAGE_URL
GET  /res.php?key=KEY&action=get&id=TASK_ID
→ OK|g-recaptcha-response-token
```

**Turnstile (port 8877):**
```
POST /in.php  key=KEY&method=turnstile&sitekey=SITE_KEY&pageurl=PAGE_URL
GET  /res.php?key=KEY&action=get&id=TASK_ID
→ OK|turnstile-token
```

**Cloudflare JS Challenge (port 8877):**
```
POST /in.php  key=KEY&method=challenge&pageurl=PAGE_URL
GET  /res.php?key=KEY&action=get&id=TASK_ID
→ OK|cf_clearance=VALUE;width=XXXX
```

### FlareSolverr-compatible API (port 8877 only)

```
POST /v1  {"cmd": "request.get", "url": "https://...", "maxTimeout": 60000}
→ {"status": "ok", "solution": {"cookies": [...], "userAgent": "...", "url": "..."}, "message": "..."}
```

---

## Turnstile Solver (Port 8877) — Working

Uses **Playwright** (not raw CDP) for reliable browser automation.

### Challenge Types Supported
- **Cloudflare JS Challenge** — waits for auto-resolution, returns `cf_clearance` cookie
- **Managed Challenge** — waits for auto-solve (clicks through if needed)
- **Interactive Turnstile** — finds widget, clicks checkbox, extracts token from hidden input
- **Invisible Turnstile** — waits for token injection by site JavaScript

### Technical Details
- Playwright `chromium` with `--no-sandbox`
- Each task gets an isolated browser context (separate cookies/storage)
- 60s overall per-task timeout with `asyncio.wait_for`
- Auto-detects challenge type via page content scanning
- Turnstile token extracted from multiple sources: `input[name=cf-turnstile-response]`, `textarea`, `window.turnstile._siteKey`, and JS evaluation
- CDP event listeners detect `cf_clearance` cookie for JS challenges

### Critical Implementation Details
- **Token extraction order matters** — check `input[name=cf-turnstile-response]` first (most reliable), then `textarea`, then window object, then DOM data attributes
- **Turnstile widget detection** — search for iframe with `/cdn-cgi/challenge-platform/` in src, or `[data-sitekey]` elements, or `div.cf-turnstile`
- **Widget click** — must click inside the Turnstile iframe's content frame, not the iframe element itself
- **CF challenge pages** — wait for `cf_clearance` cookie via CDP Network.dataReceived events, not just page load
- **Test keys** — Cloudflare test keys (`1x00000000000000000000AA`) always return `XXXX.DUMMY.TOKEN.XXXX` — this is expected, not a failure

### Known Working Sites
- `https://nowsecure.nl` — CF JS challenge, returns `cf_clearance` in ~4s ✅
- `https://demo.turnstile.workers.dev/` — Turnstile widget demo ✅

---

## reCAPTCHA v2 Solver (Port 8866)

Uses **CaptchaPlugin** ONNX neural network models + Chrome CDP.

### How It Works
1. Content scripts inject into reCAPTCHA frames
2. Each challenge image is **perceptually hashed** and looked up in SQLite cache
3. On cache miss, ONNX models classify tiles:
   - `models/type.onnx` — 100×100 input, 16 logits output (3×3 tile classification)
   - `models/grid.onnx` — 240×240 input, shape `(1, 11, 16)` (4×4 grid scoring)
4. Matching tiles clicked via content script

### Grid Model Indexing (Critical)
Shape: `(1, 11, 16)` → `logits[0][class_idx][grid_cell]`

```
type_to_index: bicycles=0, bridges=1, buses=2, cars=3, chimneys=4,
  motorcycles=5, mountains=6, palm_trees=7, stairs=8, taxis=9, tractors=10
```

### TYPE_INDEX Map
```
bicycles=0, motorcycles=1, boats=2, chimneys=3, palm_trees=4,
stairs=5, taxis=6, tractors=7, buses=8, bridges=9, cars=10, mountains=11
```

### Chrome Extension Loading Pitfalls (Chrome 148–149+)

⚠️ **These are the main blockers for the reCAPTCHA solver.**

1. **`--load-extension` is unreliable.** Extension may appear to load (ONNX init appears in stderr) but content scripts do NOT inject into reCAPTCHA iframes.
2. **`Extensions.loadUnpacked` via CDP** loads the extension but content scripts don't inject retroactively. MV3 content scripts need Chrome to register match patterns BEFORE page load.
3. **`chrome.runtime.reload()` kills the service worker.** After reload, SW target disappears and does NOT restart.
4. **`Page.reload` does NOT re-inject content scripts** — even with `ignoreCache: True`.
5. **Best approach: Playwright `launch_persistent_context`** — handles MV3 registration differently than raw Chrome CLI.

### Xvfb Setup (Required for Headed Chrome)

```bash
Xvfb :100 -screen 0 1920x1080x24 &
export DISPLAY=:100
```

---

## Server Startup Commands

```bash
# Xvfb (background, persistent)
Xvfb :100 -screen 0 1920x1080x24 &

# Chrome for reCAPTCHA (CDP on 9333)
DISPLAY=:100 google-chrome-stable \
  --remote-debugging-port=9333 --no-first-run \
  --disable-gpu --no-sandbox \
  --user-data-dir=/tmp/captcha-solver-chrome &

# reCAPTCHA solver server (port 8866, CDP 9333)
DISPLAY=:100 python3 -u /opt/captchaplugin/solver-server.py \
  --api-key KEY --port 8866 &

# Turnstile solver server (port 8877)
DISPLAY=:100 python3 -u /opt/turnstile-solver/solver-server.py \
  --api-key KEY --port 8877 &
```

---

## Docker Networking — Critical Pitfall

The solver servers run inside a Docker container. Their ports are only accessible from outside if:

1. **Docker port mapping** is in the `docker run` command (e.g., `-p 8866:8866 -p 8877:8877`)
2. **AWS EC2 security group** allows inbound TCP on those ports
3. **The NAT rule targets the correct container IP**

### Common Issue: NAT Routes to Wrong Container

```
# NAT rule says:  8866 → 172.17.0.2:8866
# But solver is in:  172.17.0.4
# Result: docker-proxy listens but connection resets (ECONNRESET)
```

**Diagnosis from host:**
```bash
# Check NAT rules
sudo iptables -t nat -L -n | grep -E '8866|8877'

# Check container IPs
docker inspect --format '{{.Name}} {{.NetworkSettings.IPAddress}}' $(docker ps -q)

# If IP mismatch, stop competing containers or recreate with correct IP
docker stop hermes2 hermes-abc57f8b
docker restart hermes
```

**Symptom:** `curl 127.0.0.1:8866` returns `Connection reset by peer` but server works fine from inside the container.

**No NET_ADMIN capability** — `iptables` inside the container returns `Permission denied` even as root. Port forwarding must be done from the host side.

### Quick Tunnel Alternative

If Docker port mapping is blocked, use `cloudflared` for instant public URLs:

```bash
# Install
curl -sL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 \
  -o /usr/local/bin/cloudflared && chmod +x /usr/local/bin/cloudflared

# Expose port 8877 (quick tunnel, no account needed)
cloudflared tunnel --url http://localhost:8877
# → https://random-words.trycloudflare.com
```

⚠️ Quick tunnel URLs change on every restart. For persistent URLs, use a named Cloudflare tunnel.

---

## CaptchaPlugin Account & Resources

- **Website:** https://captchaplugin.com
- **GitHub:** https://github.com/CaptchaRaptor/captchaplugin
- **API docs:** https://captchaplugin.com/api.php
- **Keys page:** https://captchaplugin.com/keys.php
- **WS endpoint:** `wss://ws.captcharaptor.com`
- **Auth token:** `CSGOSECRET1111!!WOWRAPTOR` (hardcoded in offscreen.js)

### WS Addon Installation
Copy WS addon files ON TOP of the `extension/` directory:
```
ws-addon/ws/background_ws.js      → extension/ws/background_ws.js
ws-addon/ws/offscreen.html        → extension/ws/offscreen.html
ws-addon/ws/offscreen.js          → extension/ws/offscreen.js
ws-addon/ws/recaptcha_frame_watch.js → extension/ws/recaptcha_frame_watch.js
ws-addon/manifest.json            → extension/manifest.json  (OVERWRITES base)
```

---

## Token Injection (Post-Solve)

```javascript
// reCAPTCHA token injection
document.querySelector('textarea[name="g-recaptcha-response"]').value = 'TOKEN';
___grecaptcha_cfg.clients[0].callback.callback('TOKEN');

// Turnstile token injection (if needed)
document.querySelector('input[name="cf-turnstile-response"]').value = 'TOKEN';
```

---

## Skill Support Files

- `references/vps-solver-debugging.md` — Chrome 149 extension loading debugging transcript
- `references/docker-networking.md` — Docker port mapping, NAT rules, container IP mismatches
- `references/docker-deployment-on-vps.md` — Probe-first workflow for installing/running solvers in a remote Docker container (probe paths, common failures, full deployment sequence)
- `templates/solver-server.py` — 2captcha-compatible API server template
