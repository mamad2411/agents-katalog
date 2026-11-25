---
name: bypass-anything
description: Browser automation with anti-detection, human behavior simulation, Cloudflare bypass, and CAPTCHA solving. Use when you need to automate browser tasks like form submission, account registration, web scraping behind CF/CAPTCHA, brand monitoring, or any task requiring a real browser session that evades bot detection.
---

# Bypass Anything

Browser automation skill for Claude Code. Zero Puppeteer dependency. CDP WebSocket native.

## Architecture

```
Claude Code (commander)
  └── CDP WebSocket Engine (direct Chrome control)
      ├── stealth-inject.mjs    ← 11 anti-detection modules
      ├── human-behavior.mjs    ← Bezier mouse + typing rhythm + random scroll
      ├── cf-solver.mjs         ← FlareSolverr + CDP fallback
      ├── captcha-solver.mjs    ← Turnstile local + 3 paid API providers
      └── cdp-submit.mjs        ← Main engine (navigate, evaluate, screenshot)
```

## Quick Start

### 1. Install

```bash
cd bypass-anything && npm install
```

### 2. Launch Chrome with CDP

```bash
# macOS
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-bypass

# Windows
"C:\Program Files\Google\Chrome\Application\chrome.exe" \
  --remote-debugging-port=9222 --user-data-dir=C:\chrome-bypass

# Linux
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-bypass
```

### 3. Use from Claude Code

```
Navigate to https://example.com and fill the registration form with:
- Name: John Doe
- Email: john@example.com
```

Claude Code will use this skill to:
1. Connect to Chrome via CDP WebSocket
2. Inject 11 anti-detection modules
3. Navigate using Chrome's built-in HTTP (respects proxy settings)
4. Fill forms with human-like typing rhythm
5. Handle CAPTCHAs automatically if API key configured

## Core Modules

### Anti-Detection (stealth-inject.mjs)

11 modules injected via CDP `Page.addScriptToEvaluateOnNewDocument` (NOT `Runtime.evaluate`). This ensures stealth runs BEFORE any page JS. Using `Runtime.evaluate` was the #1 cause of CF Turnstile detection failures.

1. `navigator.webdriver` → returns `undefined`
2. Chrome runtime API → complete fake with `OnInstalledReason`, `PlatformArch`, etc.
3. Permissions API → fixes `notifications` query
4. iframe `contentWindow` → returns parent window instead of null
5. WebGL vendor/renderer → `Intel Inc.` / `Intel Iris OpenGL Engine`
6. `navigator.plugins` → Chrome PDF Plugin, PDF Viewer, Native Client
7. `navigator.languages` → `['en-US', 'en', 'zh-CN']`
8. Media codecs `canPlayType` → realistic responses
9. `sourceURL` leak → strips injection artifacts
10. `hardwareConcurrency` → 8 cores
11. `deviceMemory` → 8GB

### Human Behavior (human-behavior.mjs)

- **Mouse**: Cubic Bezier curves with 8-15 waypoints, velocity profile (smoothstep ease in-out), micro-tremor (1-3px jitter), Perlin noise timing
- **Click**: Move to target, pause 50-150ms, then press/release with 30-80ms gap
- **Typing**: CDP `Input.dispatchKeyEvent` keyDown/keyUp + DOM value update, 30-120ms per char, 10% chance of 200ms "thinking" pause
- **Scroll**: Variable speed, 3-7 steps

### CF Bypass (cf-solver.mjs)

Priority chain: FlareSolverr Docker → CDP takeover (with Page.addScriptToEvaluateOnNewDocument stealth)

- **FlareSolverr**: Headless Chrome solves CF challenge, returns clearance cookies. Deploy with `docker run -d -p 8191:8191 ghcr.io/flaresolverr/flaresolverr`
- **CDP takeover**: Reuse user's already-verified Chrome session. Stealth injected via `Page.addScriptToEvaluateOnNewDocument` before navigation. 99% success rate when browser has active CF clearance

### CAPTCHA Solver (captcha-solver.mjs)

- **Turnstile**: Local in-page token capture (free, no external dependency)
- **reCAPTCHA v2/v3, hCaptcha, image**: Paid API providers (2Captcha, CapSolver, Anti-Captcha)
- Auto-degradation: Turnstile local → paid API → report failure

### CDP Engine (cdp-submit.mjs)

Main entry point. Connects to Chrome via WebSocket, injects stealth via `Page.addScriptToEvaluateOnNewDocument`, navigates pages, fills forms, takes screenshots. Auto-detects and waits for CF challenges to resolve.

```javascript
import { connect, navigate, getPageInfo, fillField, clickElement, takeScreenshot } from './scripts/cdp-submit.mjs';
```

## Configuration

### config.json

- `cdp`: Chrome path, port, viewport
- `captcha`: Provider and API key env var names
- `cf_bypass`: FlareSolverr URL and retry settings
- `proxy`: Optional HTTP proxy
- `stealth`: Module list

### Environment Variables

```bash
# CAPTCHA API keys (set one or more)
export CAPTCHA_2CAPTCHA_KEY="your_key"
export CAPTCHA_CAPSOLVER_KEY="your_key"
export CAPTCHA_ANTICAPTCHA_KEY="your_key"
export CAPTCHA_PROVIDER="2captcha"  # default provider

# Optional
export PROXY_HOST="127.0.0.1"
export PROXY_PORT="7892"
```

## Usage Scenarios

### Brand Monitoring
Navigate to competitor/mention pages, capture screenshots, extract text. Anti-detection ensures no blocks.

### Backlink Automation
Submit to directories, forums, Web 2.0 platforms. Human behavior simulation passes anti-spam checks (Akismet, Antispam Bee). One link per root domain per brand.

### Account Registration
Automated form filling with human-like typing. Handles Turnstile automatically. For reCAPTCHA/hCaptcha, set up API key.

### Web Scraping Behind Protection
CF-protected sites: CDP takeover bypasses without triggering challenge. If challenge triggers, FlareSolverr solves it.

### Reverse Proxy Testing
Navigate through proxy, verify response, capture headers. CDP respects Chrome's proxy settings (unlike Puppeteer's Node.js HTTP layer).

## Anti-Spam Countermeasures

| System | Bypass | Method |
|--------|--------|--------|
| Akismet | Yes | Clean email + ISP proxy + URL in author field only |
| Antispam Bee | Yes | `typeHuman()` triggers keyboard events |
| WPantispam Protect | Config-dependent | Plain text + URL field |
| CleanTalk | No | 403 block, skip site |
| hCaptcha Enterprise | No | Server-side stripping, skip site |
| Jetpack Highlander | No | Cross-origin iframe, skip site |

## Limitations (Current Version)

- No Canvas/Audio/Font fingerprint protection yet
- No residential IP rotation
- CAPTCHA (non-Turnstile) requires paid API key
- Single Chrome profile per session (no multi-tab isolation)
- No cookie/session persistence across restarts
- Interactive Turnstile challenges (forced by sitekey 3x...FF) may require user click; managed/invisible mode auto-passes
- `challenges.cloudflare.com` may be blocked in some regions (China); test with `curl -s https://challenges.cloudflare.com/turnstile/v0/api.js`

## Roadmap

- [ ] Residential IP rotation (Bright Data / IPRoyal integration)
- [ ] Canvas fingerprint randomization
- [ ] AudioContext fingerprint noise
- [ ] Font enumeration protection
- [ ] Multi-profile parallel sessions
- [ ] Cookie jar persistence (save/load sessions)
- [ ] Playwright MCP bridge for complex interactions
- [ ] Visual CAPTCHA classification (local ML model)
- [ ] Smart form field detection (label-based, not selector-based)
- [ ] Auto-login with credential vault
