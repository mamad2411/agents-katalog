---
name: captcha-cloudflare-bypass
description: >
  Bypass Cloudflare protection, CAPTCHA challenges, and anti-bot systems on websites.
  Covers Cloudflare Turnstile, reCAPTCHA v2/v3/Enterprise, hCaptcha, Vercel Security
  Checkpoint, and generic JS challenges. Use when a website returns 403, shows CAPTCHA,
  displays "checking your browser", or blocks automated access.
  Triggers: cloudflare, captcha, antibot, 403 forbidden, turnstile, hcaptcha, recaptcha,
  challenge page, bot detection, WAF, "just a moment", "checking your browser", "verify you are human"
allowed-tools: '*'
---

# CAPTCHA & Cloudflare Bypass Skill

Bypass anti-bot protection on websites using a **tiered approach** — from simplest to most sophisticated.

## Quick Decision Tree

```
Site blocked?
├── 403 Forbidden / "Just a moment" / Cloudflare challenge
│   ├── Tier 1: curl_cffi with browser-grade TLS → TRY FIRST
│   ├── Tier 2: cloudscraper library → TRY SECOND
│   ├── Tier 3: CloakBrowser stealth → FOR JS-heavy sites
│   └── Tier 4: Playwright Chromium + wait → FALLBACK
├── CAPTCHA visible (reCAPTCHA / hCaptcha / Turnstile)
│   ├── Try bypassing via Tier 1-3 (many auto-solve)
│   ├── CloakBrowser humanize=True (reCAPTCHA v3 score 0.9)
│   └── 2Captcha / anti-captcha API → PROGRAMMATIC SOLVE
└── Vercel Security Checkpoint
    └── CloakBrowser + 20s wait → ONLY solution
```

---

## TIER 1: curl_cffi (Best for API endpoints)

**When:** You need JSON data from an API behind Cloudflare, or simple page fetches.
**Why:** curl_cffi mimics browser TLS fingerprints (JA3), bypasses most Cloudflare static checks without JavaScript execution.

```python
# pip install curl_cffi
from curl_cffi import requests

# impersonate="chrome" mimics real Chrome TLS fingerprint
response = requests.get(
    "https://protected-site.com/api/data",
    impersonate="chrome",
    headers={
        "Accept": "application/json",
        "Referer": "https://protected-site.com/",
    }
)
print(response.status_code)  # 200 (not 403)
data = response.json()
```

### Advanced curl_cffi Options

```python
# With cookies (persistent session)
session = requests.Session(impersonate="chrome")
session.headers.update({
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
})
r = session.get("https://protected-site.com")
# Cookies auto-persist across requests in same session

# With proxy
response = requests.get(
    "https://protected-site.com",
    impersonate="chrome",
    proxies={"https": "http://user:pass@proxy:port"},
)
```

---

## TIER 2: cloudscraper (JS challenge solver)

**When:** curl_cffi fails because Cloudflare sends a JS challenge page (not just 403).
**Why:** cloudscraper executes the Cloudflare challenge JavaScript and extracts the clearance cookie.

```python
# pip install cloudscraper
import cloudscraper

scraper = cloudscraper.create_scraper(
    browser={
        "browser": "chrome",
        "platform": "windows",
        "mobile": False,
    }
)

response = scraper.get("https://protected-site.com")
print(response.status_code)  # 200 after solving JS challenge
print(response.text[:200])
```

### cloudscraper Limitations
- ❌ Does NOT solve reCAPTCHA or hCaptcha (only JS math challenges)
- ❌ May fail on newer Cloudflare Turnstile (2024+)
- ✅ Works well on classic Cloudflare "Checking your browser" pages
- ✅ Auto-solves Cloudflare JS computational challenges

---

## TIER 3: CloakBrowser (Full stealth browser)

**When:** Site has Turnstile, reCAPTCHA, fingerprinting, or needs JavaScript rendering.
**Why:** 49 source-level C++ patches, real navigator properties, humanize behavior.

```python
# pip install cloakbrowser
from cloakbrowser import launch
import time

browser = launch(humanize=True)  # humanize for realistic mouse/typing
page = browser.new_page()

# Navigate with generous timeout
page.goto("https://protected-site.com", timeout=30000)

# CRITICAL: Wait for challenge to resolve (5-25 seconds depending on site)
time.sleep(15)

# Check if challenge passed
title = page.title()
if "just a moment" in title.lower() or "checking" in title.lower():
    time.sleep(10)  # Wait more

# Page content is now accessible
content = page.content()
print(f"Title: {title}")

# Take screenshot for verification
page.screenshot(path="/tmp/cloak_result.png")

browser.close()
```

### CloakBrowser Persistent Profile (keeps cookies)

```python
from cloakbrowser import launch_persistent_context

context = launch_persistent_context(
    user_data_dir="/tmp/bypass-profile",
    humanize=True
)
page = context.new_page()
page.goto("https://protected-site.com")
# Cookies saved for future visits
context.close()
```

### CloakBrowser with Proxy

```python
browser = launch(
    proxy="http://user:pass@proxy.example.com:8080",
    geoip=True,  # Auto-match timezone to proxy IP
    humanize=True
)
```

### ⚠️ PITFALL: CloakBrowser launch() Hangs

On some servers, `cloakbrowser.launch()` hangs indefinitely. **ALWAYS wrap in timeout:**

```bash
timeout 45 python3 my_cloak_script.py
```

If it hangs 3+ times, fall back to Playwright Chromium (Tier 4).

### ⚠️ PITFALL: Async/Sync Conflict

CloakBrowser uses **sync Playwright**. Don't call `launch()` inside `asyncio.run()`:

```python
# ❌ WRONG - crashes with "Sync API inside asyncio loop"
import asyncio
async def main():
    browser = launch()  # ERROR!
asyncio.run(main())

# ✅ CORRECT - use sync directly
browser = launch()
page = browser.new_page()
page.goto("https://site.com")
browser.close()

# ✅ OR connect to existing CDP for async
import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.connect_over_cdp("http://127.0.0.1:9222")
        page = browser.contexts[0].pages[0]
        await page.goto("https://site.com")
asyncio.run(main())
```

---

## TIER 4: Playwright Chromium + Hermes Browser Tools

**When:** CloakBrowser is too slow/unavailable, or you need accessibility snapshots.
**Why:** Built-in Hermes tools (`browser_navigate`, `browser_click`, etc.) handle element refs and interaction.

```bash
# Launch Chrome with CDP
/root/.cache/ms-playwright/chromium-*/chrome-linux*/chrome \
  --headless=new --no-sandbox --disable-gpu \
  --remote-debugging-port=9222 --disable-dev-shm-usage \
  --user-data-dir=/tmp/chrome-profile &

# Verify
curl -s http://127.0.0.1:9222/json/version
```

Then use Hermes tools:
1. `browser_navigate(url="https://protected-site.com")`
2. `browser_snapshot()` — check if CAPTCHA/challenge appears
3. Wait and retry snapshot if challenge page
4. `browser_vision()` — visually confirm if challenge passed

**Note:** Standard Playwright Chromium often fails Cloudflare/Turnstile. Use only when Tier 1-3 fail.

---

## TIER 5: CAPTCHA-Solving Services (Programmatic)

**When:** All browser approaches fail and CAPTCHA is required (reCAPTCHA v2 checkbox, hCaptcha).
**Why:** Paid services solve CAPTCHAs via human workers or AI.

### Option A: 2Captcha API

```python
import requests
import time

API_KEY = "YOUR_2CAPTCHA_API_KEY"

# Step 1: Submit CAPTCHA
resp = requests.post("http://2captcha.com/in.php", data={
    "key": API_KEY,
    "method": "userrecaptcha",
    "googlekey": "SITE_RECAPTCHA_KEY",  # From page source
    "pageurl": "https://protected-site.com/page",
    "invisible": 0,  # 1 for invisible reCAPTCHA
}).text
captcha_id = resp.split("|")[1]

# Step 2: Poll for solution
token = None
for _ in range(30):
    time.sleep(5)
    result = requests.get("http://2captcha.com/res.php", params={
        "key": API_KEY,
        "action": "get",
        "id": captcha_id,
    }).text
    if "CAPCHA_NOT_READY" not in result:
        token = result.split("|")[1]
        break

# Step 3: Inject token into page
if token:
    # Via browser_console or page.evaluate()
    js = f"""
    document.getElementById('g-recaptcha-response').innerHTML = '{token}';
    // Also try for enterprise
    if (typeof ___grecaptcha_cfg !== 'undefined') {{
        Object.keys(___grecaptcha_cfg.clients).forEach(key => {{
            Object.entries(___grecaptcha_cfg.clients[key]).forEach(([k, v]) => {{
                if (v && typeof v === 'object' && v.callback) {{
                    v.callback('{token}');
                }}
            }});
        }});
    }}
    """
```

### Option B: anti-captcha.com API

```python
import requests

resp = requests.post("https://api.anti-captcha.com/createTask", json={
    "clientKey": "YOUR_API_KEY",
    "task": {
        "type": "RecaptchaV2EnterpriseTaskProxyless",
        "websiteURL": "https://protected-site.com",
        "websiteKey": "SITE_RECAPTCHA_KEY",
        "apiDomain": "www.google.com",
    }
}).json()
task_id = resp["taskId"]
```

---

## Site-Specific Strategies

### Cloudflare Turnstile
- **curl_cffi** → Works for API endpoints (no JS needed)
- **CloakBrowser** → Passes automatically (Turnstile verified: PASS)
- **cloudscraper** → May fail on newer Turnstile versions

### Cloudflare "Under Attack Mode" (5-second challenge)
- **curl_cffi** → Usually works (Tier 1)
- **cloudscraper** → Designed for this (Tier 2)
- **CloakBrowser** → Always works (Tier 3)

### reCAPTCHA v2 (checkbox)
- **CloakBrowser humanize=True** → Score 0.9, but v2 checkbox may still show
- **Manual** → Human clicks the checkbox
- **2Captcha** → Programmatic solve (~$2-3/1000 solves)

### reCAPTCHA v3 (invisible)
- **CloakBrowser** → Score 0.9 ✅ (passes automatically)
- **curl_cffi** → Works if no JS challenge precedes it

### reCAPTCHA Enterprise
- **CloakBrowser** → Partial success, may still show challenge
- **2Captcha Enterprise** → `RecaptchaV2EnterpriseTaskProxyless` task type
- **Manual** → Most reliable for Enterprise

### hCaptcha
- **CloakBrowser** → Often passes
- **2Captcha** → `HCaptchaTaskProxyless` task type

### Vercel Security Checkpoint
- **Only CloakBrowser works** → `time.sleep(20)` after goto
- CDP/Playwright Chromium → Stuck forever
- `curl_cffi` / `cloudscraper` → Fails

### FunCaptcha / Arkose Labs (GitHub, EA, Roblox, etc.)
- **Structure:** Nested iframes — outer provider (e.g. `octocaptcha.com`) → Arkose Labs enforcement (`arkoselabs.com`) → `game-core-frame`
- **CDP inspection:** `Target.getTargets` reveals iframe tree with targetIds, but **cross-origin interaction is blocked**
- **CloakBrowser** → Unreliable. FunCaptcha specifically targets automation.
- **2Captcha** → `FunCaptchaTaskProxyless` task type. Requires `publicKey` (from page source `pk=` param) and `pageUrl`. ~$3-4/1000 solves.
- **Manual** → Most reliable. FunCaptcha visual/audio puzzle requires human.
- **GitHub specifically:** Uses `octocaptcha.com` as outer wrapper, `pk=747B83EC-2CA3-43AD-A7DF-701F286FBABA` as the Arkose public key. No known programmatic bypass.

> **Full GitHub signup workflow** (4-layer anti-bot): see `references/github-signup-workflow.md`

**Debugging FunCaptcha iframe structure via CDP:**
```javascript
// Get all targets (iframes show up as type="iframe")
Target.getTargets → look for:
//   1. octocaptcha.com (outer wrapper)
//   2. arkoselabs.com/v2/.../enforcement.*.html (inner enforcement)
//   3. game-core-frame (actual puzzle — nested inside #2)
// Cannot access game-core-frame content due to cross-origin policy
```

### AWS WAF (CAPTCHA)
- **CloakBrowser** → Usually passes with humanize=True
- **2Captcha** → `AWSCaptchaTask` task type

---

## Quick Helper Script: Smart Bypass

Save as `~/.hermes/scripts/smart_bypass.py`:

```python
#!/usr/bin/env python3
"""Smart anti-bot bypass — tries tiers 1→3 automatically."""
import sys
import time

def bypass_url(url: str, need_js: bool = False) -> dict:
    """Try to fetch a protected URL using progressive bypass tiers."""
    result = {"url": url, "tier": None, "status": None, "content": None}

    # TIER 1: curl_cffi
    try:
        from curl_cffi import requests as cf_requests
        r = cf_requests.get(url, impersonate="chrome", timeout=15, headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": url.rsplit("/", 1)[0] + "/",
        })
        if r.status_code == 200 and "challenge" not in r.text[:500].lower():
            result.update(tier="curl_cffi", status=200, content=r.text)
            return result
    except Exception as e:
        result["tier1_error"] = str(e)

    # TIER 2: cloudscraper
    try:
        import cloudscraper
        scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows"})
        r = scraper.get(url, timeout=20)
        if r.status_code == 200:
            result.update(tier="cloudscraper", status=200, content=r.text)
            return result
    except Exception as e:
        result["tier2_error"] = str(e)

    # TIER 3: CloakBrowser
    if not need_js:
        return result  # Skip browser if only API data needed

    try:
        from cloakbrowser import launch
        browser = launch(humanize=True)
        page = browser.new_page()
        page.goto(url, timeout=30000)
        time.sleep(15)
        content = page.content()
        title = page.title()
        browser.close()
        result.update(tier="cloakbrowser", status=200, content=content, title=title)
        return result
    except Exception as e:
        result["tier3_error"] = str(e)

    return result


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else None
    if not url:
        print("Usage: smart_bypass.py <url> [--js]")
        sys.exit(1)
    need_js = "--js" in sys.argv
    result = bypass_url(url, need_js=need_js)
    print(f"Tier: {result.get('tier', 'FAILED')}")
    print(f"Status: {result.get('status', 'N/A')}")
    if result.get("content"):
        print(f"Content length: {len(result['content'])} chars")
        print(f"Preview: {result['content'][:300]}")
    else:
        print(f"Errors: {result}")
```

---

## Pitfalls

1. **Don't hammer sites.** Rate limiting + IP bans. Space requests 5+ seconds apart.
2. **curl_cffi is the fastest path** — always try it first for API data.
3. **CloakBrowser launch() can hang** — always `timeout 45 python3 script.py`.
4. **Cloudflare cookies are temporary** — clearance cookie expires ~30 min. Re-solve if 403 returns.
5. **reCAPTCHA Enterprise ≠ reCAPTCHA v3** — Enterprise often requires human or paid solver.
6. **Proxy quality matters** — datacenter IPs get blocked faster than residential.
7. **Keep sessions alive** — `requests.Session()` / persistent profiles preserve cookies across requests.
8. **Check `response.text[:500]`** — if it contains "challenge", "captcha", "verify", the bypass failed.
9. **Don't mix sync/async Playwright** — CloakBrowser is sync-only. Use `connect_over_cdp` for async.
10. **2Captcha costs money** — ~$2-3 per 1000 reCAPTCHA solves, ~$3-4 for hCaptcha. Budget accordingly.

## Verification

After any bypass attempt, verify success:
```bash
# Check response doesn't contain challenge markers
python3 -c "
import sys
content = open(sys.argv[1]).read() if len(sys.argv) > 1 else ''
markers = ['challenge', 'captcha', 'just a moment', 'checking your browser', 'verify you are human', 'turnstile']
found = [m for m in markers if m in content.lower()[:1000]]
print('BLOCKED' if found else 'CLEAR')
print(f'Found: {found}' if found else '')
"
```

## Dependencies (pre-installed)

- `cloakbrowser` v0.3.29 ✅
- `curl_cffi` v0.15.0 ✅
- `cloudscraper` v1.2.71 ✅
- `playwright` v1.60.0 ✅
