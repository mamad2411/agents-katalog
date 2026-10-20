---

name: captcha-bypass-browsers
description: >-
  Captcha-bypass browsers installed: CloakBrowser (drop-in Playwright stealth Chromium)
  and camofox-browser (Firefox anti-detect REST API server). Setup and usage.
version: 1.0.0
license: MIT
author: Hermes Agent
metadata:
  hermes:
    tags: [captcha, browser-stealth, cloakbrowser, camofox, anti-detection]
    triggers: [captcha-bypass, cloakbrowser, camofox, hcaptcha, bot-detection]
    related_skills: [stealth-browser-setup, firefox-stealth-automation]
prerequisites:
  commands: [node, python]
---
# Captcha-Bypass Browsers — Setup & Usage Guide

## Critical Distinction: Two Browser Contexts

This infrastructure has **two independent browser stacks**. Confusing them wastes time.

| Stack | Engine | Controlled By | Session | Login State |
|-------|--------|--------------|---------|-------------|
| **Chrome DevTools MCP** | the operator's real Chrome | `mcp_chrome_devtools_*` tools | the operator's browsing session | ✅ the operator's accounts |
| **CloakBrowser** | Stealth Chromium (C++ patched) | Playwright Python scripts | Fresh incognito each run | ❌ Not logged in |

**Which to use:**
- Chrome DevTools for **navigating the operator's logged-in sessions** (Discord, GitHub, etc.)
- CloakBrowser for **bypassing captcha** (form submissions on public or token-authenticated pages)

## Interacting with React SPAs — Two Different Evaluation Contexts

This is the most important practical finding from the Discord bot creation work. Playwright's `page.evaluate()` and Chrome DevTools MCP's `evaluate_script` run in **different JavaScript worlds**:

| Mechanism | World | React event handlers? | localStorage access? |
|-----------|-------|----------------------|---------------------|
| Playwright `page.evaluate()` | Isolated world | ❌ Not attached | ❌ Not accessible |
| Chrome DevTools MCP `evaluate_script` | **Page's main world** | ✅ Fully bound | ✅ Accessible |
| Playwright `element.click()` | Actionability-checked | ❌ Blocked by overlays | N/A |
| Chrome DevTools MCP `click(uid)` | Protocol-level real click | ✅ Works | N/A |

**Practical consequences:**
- **Chrome DevTools MCP's `evaluate_script`** can call `cb.click()` on a React checkbox and React **will** process the state change. This is because the script runs in the page's main execution context where React's event delegation is listening.
- **Playwright's `page.evaluate(fn)`** calling `cb.click()` on the same checkbox **will NOT** trigger React's onChange in many cases. The event fires in the isolated world and doesn't reach React's synthetic event system at the document root.
- **Playwright's `element.dispatch_event("click")`** triggers Playwright's actionability checks (pointer_events, visibility, etc.) that can fail on patched browsers like CloakBrowser.

**For React form interactions, prefer these patterns:**

1. **Native property setter (value/checked)** — bypasses React state tracking entirely, then dispatches change events:
   ```javascript
   // Value setter for text inputs
   const ns = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
   ns.call(input, 'new text');
   input.dispatchEvent(new Event('input', {bubbles: true}));
   input.dispatchEvent(new Event('change', {bubbles: true}));

   // Checked setter for checkboxes
   const cs = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'checked').set;
   cs.call(checkbox, true);
   checkbox.dispatchEvent(new Event('change', {bubbles: true}));
   ```

2. **PointerEvent chain** — simulates real user interaction that React listens for:
   ```javascript
   element.dispatchEvent(new PointerEvent('pointerdown', {bubbles: true, cancelable: true}));
   element.dispatchEvent(new PointerEvent('pointerup', {bubbles: true, cancelable: true}));
   element.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}));
   ```

3. **Chrome DevTools MCP evaluate_script** (for the operator's logged-in Chrome sessions) — use `cb.click()` directly, it just works because the world is shared:
   ```javascript
   // This works inside Chrome DevTools MCP's evaluate_script:
   document.querySelector('[type="checkbox"]')?.click();
   ```

**Troubleshooting checklist when a React form won't submit:**
1. Check if the Create/Submit button is disabled by reading `aria-disabled` or `classList`
2. Check if a modal overlay is covering the button (`document.elementFromPoint(x, y)`)
3. Try `element.click()` (native DOM, no Playwright actionability check) via evaluate
4. Try PointerEvent chain if `click()` doesn't work
5. Force-enable then click: `button.disabled = false; button.click()`
6. For checkbox/input state, always use native property setter, never `checked = true` assignment

## Discord Bot Token Automation — Lessons Learned

Discord has three independent defenses against automated bot creation, and confusing the two browser stacks wasted significant time in the initial attempt:

**hCaptcha JS API (window.hcaptcha):** On pages where hCaptcha is rendered (including Discord's Developer Portal), the `window.hcaptcha` object provides direct control: `execute()` to trigger challenges, `getResponse()` to check solve state, `close()` to dismiss. See `references/hcaptcha-js-api.md`.

1. **hCaptcha (browser)** — CloakBrowser bypasses this; regular Chrome triggers it
2. **React SPA form submission** — Chrome DevTools MCP `evaluate_script` runs in page's main world where React handlers bind; Playwright `page.evaluate()` runs in isolated world where they don't
3. **MFA / password** — Must ask the operator to enter his password for token resets
4. **"Missing Access"** — account-level rate limit after ~1-2 app creations

**The one that worked:** Hybrid approach using Chrome DevTools MCP + the operator's MFA entry. Full details in `references/discord-bot-creation.md`.

**The two-world problem (PLAYWRIGHT vs DEVTOOLS MCP evaluate):**

| Context | React events? | localStorage? | location |
|---------|--------------|---------------|----------|
| Playwright `page.evaluate()` | ❌ Not bound | ❌ Not accessible | Isolated world |
| Chrome DevTools MCP `evaluate_script` | ✅ Bound | ✅ Accessible | Page main world |
| Chrome DevTools MCP `click(uid)` | ✅ Works | N/A | Protocol-level |

When `cb.click()` doesn't trigger React's onChange, use the **native property setter** pattern:
```javascript
const ns = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'checked').set;
ns.call(checkbox, true);
checkbox.dispatchEvent(new Event('change', {bubbles: true}));
```

## 1. CloakBrowser (Chromium-based, C++ stealth)

**Repo:** CloakHQ/CloakBrowser (23.6k ★)
**Installation:** `pip install cloakbrowser` ✅ already done
**Status:** Installed v0.3.31, verified working — stealth PASS (no HeadlessChrome leak)

**Usage in async Python:**
```python
from cloakbrowser import launch_async  # NOT just 'launch' (that's sync)

browser = await launch_async(headless=True, humanize=True)
page = await browser.new_page()
await page.goto('https://example.com')
await browser.close()
```

**Discord bot creation scripts:**  
- `~/cloak_bots5.py` — latest attempt, handles React dialog + checkbox via PointerEvent chain  
- `~/test_bot.py` — minimal single-bot test (created this session)  
- `~/cloak_bots.py` — original (broken — React overlay check fails)  

**Reality check on Discord bot token automation:**  
CloakBrowser bypasses hCaptcha visually (dialog opens cleanly), but Discord's React SPA form submission is brittle. Several layers of defense exist — see `references/discord-bot-creation.md` for the full analysis of what works and what doesn't.

## 2. camofox-browser (Firefox-based, anti-detection server)

**Repo:** jo-inc/camofox-browser (6.3k ★)
**Installation:** Cloned to `${MY_REPOS}\Documents\github\camofox-browser`
**Start:** `node server.js` (REST API on port 9377)
**Status:** Server running, Camoufox engine connected

**MCP Server:** Wrapper at `mcp_server.py` in the repo directory
**Hermes Config:** Added under `mcp_servers.camofox-browser` in config.yaml

**Tools available through MCP:**
- `camofox_status`, `camofox_start`, `camofox_stop`
- `camofox_navigate`, `camofox_snapshot`, `camofox_click`, `camofox_type`
- `camofox_scroll`, `camofox_screenshot`, `camofox_list_tabs`, `camofox_close_tab`

**First-run:** Downloads Camoufox binary (~300MB) automatically on first `/start`

## Key Difference
- **CloakBrowser** = Chromium drop-in replacement for Playwright scripts (best for existing Playwright automation)
- **camofox-browser** = REST API server with anti-detection Firefox (best for agent-based browsing via API/MCP)
