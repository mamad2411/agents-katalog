---
name: sci-paper-search
description: Search and download SCI papers from Web of Science, Wiley, IEEE, etc. using your everyday Chrome browser. Handles captcha/verification by letting you manually complete it in the browser window while the script auto-detects and resumes. Use when the user wants to search academic databases, download papers, or automate paper collection workflows.
allowed-tools: Bash(python:*), Bash(curl:*), Bash(powershell:*)
---

# SCI Paper Search & Download

Search academic databases and download papers through **your own Chrome browser** — not a headless bot. Websites see a real user, so login sessions, cookies, and institutional access all work. When verification/captcha appears, you handle it manually and the script auto-resumes.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Your Chrome (--remote-debugging-port=9222)              │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Tabs with your cookies, logins, sessions         │  │
│  └───────────────────────────────────────────────────┘  │
│                         ▲                                │
│                         │ CDP (WebSocket)                │
│                         ▼                                │
│  Python helper (cdp.py)                                  │
│  - new_tab(url) → open & navigate                       │
│  - tab.eval(js) → execute JS, get results               │
│  - tab.navigate(url) → navigate existing tab             │
│  - tab.info() → get title + URL                         │
└─────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Launch Chrome with Debug Port

First locate your Chrome executable. **Ask the user for the path to `chrome.exe` if you don't know it** — otherwise auto-detect it from the common install locations:

```powershell
$chrome = @(
  "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
  "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
  "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1

if (-not $chrome) { Write-Error "Chrome not found — ask the user for its path" }
```

Close all Chrome windows, then launch with the debug port:

```powershell
# Kill existing Chrome
powershell -Command "Get-Process chrome -ErrorAction SilentlyContinue | Stop-Process -Force"

# Launch with debug port
& $chrome `
  --remote-debugging-port=9222 `
  --remote-debugging-address=127.0.0.1 `
  --remote-allow-origins=* `
  --user-data-dir="$env:LOCALAPPDATA\Google\Chrome\User Data" `
  --no-first-run
```

> **NOTE:** If Chrome complains about the profile being locked, use a separate debug profile: `--user-data-dir="$env:LOCALAPPDATA\chrome-debug-profile"`. The first launch will be a fresh profile — log in to your sites once, and sessions will persist.

Verify the debug port is open:

```bash
curl -s http://127.0.0.1:9222/json/version
```

### 2. Use the CDP Helper

The `cdp.py` module (see [references/cdp.py](references/cdp.py)) provides a minimal interface:

```python
from cdp import new_tab, get_tab, list_tabs

tab = new_tab("https://www.webofscience.com/wos/alldb/basic-search")
result = tab.eval("document.title")
tab.navigate("https://doi.org/10.1002/adma.201300155")
title, url = tab.info()
```

### 3. Standard Workflow

The canonical pattern for any paper search:

```
1. Open search page → wait for user to handle login/captcha
2. Fill search form → click search
3. Wait for results → extract paper list
4. Click paper → find "Full text at publisher" → navigate to PDF
5. If verification appears → user handles it → script auto-resumes
6. Click download → save PDF
```

**Key principle:** Never use `input()` for pauses. Instead, **poll the page state** in a loop and auto-detect when the user has finished manual intervention:

```python
while True:
    time.sleep(3)
    title, url = tab.info()
    blocked = any(k in title.lower() for k in ["verify", "captcha", "sign in"])
    if not blocked and "target-site.com" in url:
        break
    print("  ... waiting for verification ...")
```

## Database-Specific Patterns

### Web of Science

**Search URL:** `https://www.webofscience.com/wos/alldb/basic-search`

> ⚠️ **IMPORTANT: WoS only supports ENGLISH search terms.** Chinese, Japanese, Korean, and other non-Latin scripts will produce garbled results or zero hits. Always translate the user's query into English before searching. For example: "石墨烯气凝胶" → "graphene aerogel", "碳纳米管" → "carbon nanotube", "钙钛矿太阳能电池" → "perovskite solar cells".

**Fielded search (Topic + Publication Name):**

```python
tab = new_tab("https://www.webofscience.com/wos/alldb/basic-search")
time.sleep(5)

tab.eval("document.querySelector('#onetrust-accept-btn-handler')?.click()")

# Fill the topic input via the Angular setter, or Angular won't register the value
tab.eval("""
    var inp = document.querySelector('#search-option-0');
    inp.focus();
    var setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
    setter.call(inp, 'graphene aerogel');
    inp.dispatchEvent(new Event('input', {bubbles: true}));
    inp.dispatchEvent(new Event('change', {bubbles: true}));
""")

tab.eval("""
    Array.from(document.querySelectorAll('button'))
        .find(b => b.textContent.trim().includes('Add row')).click();
""")
time.sleep(2)

# Switch row 2 to "Publication/Source Titles" — use the wos-select button, not mat-select
tab.eval("""
    var buttons = document.querySelectorAll(
        'wos-select.wos-select-search-field button[role="combobox"]');
    if (buttons.length >= 2) buttons[1].click();  // [0]=row1, [1]=row2
""")
time.sleep(2)
tab.eval("""
    var options = document.querySelectorAll(
        'mat-option, [role="option"], .mdc-list-item, .mat-mdc-option');
    for (var i = 0; i < options.length; i++) {
        if (options[i].textContent.includes('Publication')
            && options[i].textContent.includes('Source')) {
            options[i].click(); break;
        }
    }
""")
time.sleep(1)

tab.eval("""
    var inp = document.querySelector('#search-option-1');
    inp.focus();
    var setter = Object.getOwnPropertyDescriptor(
        HTMLInputElement.prototype, 'value').set;
    setter.call(inp, 'Advanced Materials');
    inp.dispatchEvent(new Event('input', {bubbles: true}));
    inp.dispatchEvent(new Event('change', {bubbles: true}));
""")

tab.eval('document.querySelector("button.search").click()')
```

**WoS uses VIRTUAL SCROLLING** — only the first 1–2 result records are actually rendered. The rest are `loading-cover` placeholders. **Always scroll to load before extracting:**

```python
# Scroll progressively to trigger rendering
for i in range(15):
    tab.eval(f'window.scrollTo(0, document.body.scrollHeight * {(i+1)/18})')
    time.sleep(0.7)
time.sleep(2)

# Now extract ONLY fully-rendered records
records = tab.eval("""
    document.querySelectorAll(
        'app-record.Summary-record-view:not(.loading-cover)')
""")
```

**WoS result selectors:**
- Rendered records: `app-record.Summary-record-view:not(.loading-cover)`
- Unrendered placeholders: `app-record.loading-cover` — skip these
- Title links: `a[href*="WOS:"]` (e.g., `WOS:001385113600001`)
- Page info: title contains `– N –` where N = total count

**Extracted text contains Material Design icon noise.** Strip these when displaying:
`arrow_drop_down`, `more_horiz`, `expand_more`, `get_app`, `open_in_new`.

**Known redirect:** WoS → `webofscience.clarivate.cn` (China mirror). This is normal.

### Wiley Online Library

**DOI pattern:** `https://doi.org/10.1002/adma.201300155`

Wiley uses **Cloudflare** verification. When the CDP script hits Cloudflare:
1. Script detects "安全验证" / "verifying you" / "请稍候…" in page
2. Script prints: "Verification needed — please complete in browser"
3. Script polls every 3s until verification passes
4. After Cloudflare passes, the ePDF reader loads (or PDF starts downloading)

**Wiley ePDF page:**
- Accept cookies first: find button with "全部接受" or "Accept all"
- Download button: Material icon `get_app` inside a button/link
- The download link pattern: `a` with text "get_app" → `href` = `/doi/pdfdirect/DOI?download=true`

**Direct PDF download (skip ePDF reader):**

Navigate straight to the PDF instead of going through the ePDF reader:

```python
doi = '10.1002/adma.202417462'
pdf_url = f'https://advanced.onlinelibrary.wiley.com/doi/pdfdirect/{doi}?download=true'
tab.navigate(pdf_url)  # may still trigger Cloudflare first
```

This pattern works for all Wiley journals (Advanced Materials, Advanced Functional Materials, Small, Angewandte Chemie, etc.) — replace the subdomain accordingly (`advanced.onlinelibrary.wiley.com` → the appropriate journal subdomain, or use `onlinelibrary.wiley.com`).

### Google Scholar

Google Scholar aggressively blocks automated access. **Always navigate via a search URL** rather than filling the form:

```python
tab = new_tab(
    'https://scholar.google.com/scholar?q=Characterization+and+Electrochemical+Performance+of+Graphene')
time.sleep(4)
```

When blocked, Google redirects to `/sorry/...` — detect this via URL, not just page text:

```python
blocked = '/sorry/' in url.lower() or 'captcha' in url.lower()
```

If blocked, tell the user to complete the CAPTCHA in Chrome and poll for unblock (URL no longer contains `/sorry/`).

**Results:** `.gs_ri` for each result. PDF links often appear as `[PDF]` links.

## Verification / Captcha Handling

### Detection Pattern

```python
def page_blocked(tab):
    """Check if page is blocked by verification — check BOTH text and URL"""
    title, url = tab.info()
    # URL-based detection (most reliable)
    if any(k in url.lower() for k in ['/sorry/', 'captcha', 'recaptcha', 'challenge']):
        return True
    if title == '请稍候…':  # Chinese Cloudflare intermediary page
        return True
    # Text-based detection
    return tab.eval("""
        (function() {
            var text = document.body ? document.body.innerText : '';
            return text.includes("verify you're human") ||
                   text.includes("not a robot") ||
                   text.includes("安全验证") ||
                   text.includes("正在进行安全验证") ||
                   text.includes("Ray ID") ||           // Cloudflare
                   !!document.querySelector('iframe[src*="captcha"]') ||
                   !!document.querySelector('.g-recaptcha') ||
                   !!document.querySelector('#challenge-stage');
        })()
    """)
```

### Auto-Resume After Manual Verification

```python
def wait_for_unblock(tab, target_url_fragment=""):
    """Poll until user completes verification"""
    print("  [WAIT] Manual verification needed — check the Chrome window!")
    while True:
        time.sleep(3)
        if not page_blocked(tab):
            title, url = tab.info()
            if target_url_fragment in url.lower():
                print(f"  [OK] Verification passed! Continuing...")
                return
            print(f"  [INFO] Current: {title}")
```

**Important:** Cloudflare sometimes shows a page that says "verifying" but never displays the interactive checkbox. If this happens, **refresh the page** (`tab.eval('location.reload()')`) to retrigger the challenge.

## Chrome Lifecycle Management

### Starting Chrome

```powershell
# $chrome = path to chrome.exe (see Quick Start for auto-detection)
Get-Process chrome -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep 2
Start-Process $chrome -ArgumentList `
  '--remote-debugging-port=9222',
  '--remote-debugging-address=127.0.0.1',
  '--remote-allow-origins=*',
  "--user-data-dir=$env:LOCALAPPDATA\chrome-debug-profile",
  '--no-first-run'
```

### Chrome Crashed? Restart It

If Chrome disconnects (port 9222 unreachable):

```bash
# Check if Chrome is running
tasklist | grep -i chrome
```

```powershell
# If dead, restart (same $chrome path as above)
Start-Process $chrome -ArgumentList `
  '--remote-debugging-port=9222',
  '--remote-debugging-address=127.0.0.1',
  '--remote-allow-origins=*',
  "--user-data-dir=$env:LOCALAPPDATA\chrome-debug-profile",
  '--no-first-run'
```

```bash
# Verify
curl -s http://127.0.0.1:9222/json/version
```

### Tab IDs Change After Restart

After Chrome restart, all previous tab IDs are invalid. Use `list_tabs()` or `get_tab()` with the new ID from `requests.get(f"{CDP}/json")`.

## Advanced Patterns

See [references/advanced_patterns.md](references/advanced_patterns.md) for:
- Multi-dimensional deep search (6-8 dimensions × 5 pages)
- IF database matching with journal verification
- Multi-strategy PDF download (browser trigger, requests with cookies, XHR base64)
- State persistence for long download sessions
- Publisher-specific URL construction (Wiley, Cell Press, generic DOI)
- WoS metadata parsing from unstructured fullText

## Helper Module Reference

The CDP helper lives at `references/cdp.py`. Copy it to your working directory and import:

```python
from cdp import new_tab, get_tab, Tab, list_tabs
```

Key methods on `Tab`:
- `tab.eval(js)` — Evaluate JavaScript, return result value
- `tab.navigate(url)` — Navigate to URL
- `tab.info()` — Get (title, url) tuple
- `tab.ws` — Raw WebSocket connection
- `tab.close()` — Close WebSocket

New tabs are created without `--remote-allow-origins=*` set on Chrome, WebSocket connections will be rejected with HTTP 403. Always include this flag.

## Common Pitfalls

1. **`requests.put()` for new tabs, not `requests.get()`** — CDP `/json/new` only accepts PUT
2. **WebSocket origin rejection** — Need `--remote-allow-origins=*` Chrome flag
3. **GBK encoding on Windows** — Set `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` before printing. Also write extracted text to files instead of printing when dealing with special characters
4. **`input()` in non-interactive shells** — Use polling loops instead
5. **Chrome profile lock** — Either use a separate `--user-data-dir` or kill all Chrome processes first
6. **Material Design buttons** — Dispatch `mousedown` + `mouseup` + `click` events if simple `.click()` doesn't work
7. **WoS gateway URL** — Needs `DestApp` parameter; prefer clicking "Full text at publisher" links directly, or use DOI-based navigation
8. **SPA page detection** — WoS is a Single Page App; URL may not change immediately after navigation. Use page title and body text to determine state
9. ⚠️ **WoS requires ENGLISH search terms** — Chinese/Japanese/Korean characters are not supported by WoS search. Always translate non-English queries to English before searching. The search will appear to work (no error), but the query text will be garbled (e.g., "石墨烯" → "ʯīϩ") and return zero meaningful results
10. ⚠️ **WoS uses VIRTUAL SCROLLING** — Only 1–2 records are rendered initially. Scroll the page to load more before extraction. Select only `:not(.loading-cover)` records
11. ⚠️ **`tab.eval()` can return `None`** — CDP WebSocket may time out or the expression may fail silently. Always guard against `None` before comparing/iterating: `count = tab.eval(...) or 0`
12. **WoS field type dropdown** — Use `wos-select.wos-select-search-field button[role="combobox"]`, NOT `mat-select` directly. The `mat-select` is the Angular wrapper; the actual click target is the inner button
13. **Incomplete full record page** — The "Full text at publisher" link may not always be present. Fall back to DOI extraction from page text: regex `10\.\d{4,}\/[^\s]+`, then navigate to `https://doi.org/<DOI>`
14. **Extracted text contains Material Design icon names** — Filter out `arrow_drop_down`, `more_horiz`, `expand_more`, `get_app`, `open_in_new` from displayed results

## Sample Session

A complete session searching for graphene papers in Wiley's Advanced Materials journal:

```
>>> WoS Search: "graphene" in Topic + "Advanced Materials" in Publication Name
    3,244 results found

>>> Paper: "Wet Chemical Synthesis of Graphene"
    Eigler et al., Advanced Materials, 2013
    DOI: 10.1002/adma.201300155

>>> Full text → Wiley ePDF page → Cloudflare verification
    User completes verification → PDF (3.8 MB) loads

>>> Click download → PDF saved to Chrome's download directory
    Done.
```
