---
name: browser-automation-security
description: Playwright browser automation for security testing, OSINT, web scraping,
  and penetration testing. Full browser automation with Chromium for JS-rendered pages,
  login automation, form interaction, screenshot capture, and network interception.
  Use as an alternative to web_extract for interactive/dynamic content.
version: 1.61.0
category: red-teaming
license: MIT
metadata:
  hermes_origin: import
tags:
- playwright
- browser
- automation
- headless
- scraping
- pentest
- chromium
related_skills:
- web-app-pentest
- client-auth-bypass
- security-orchestrator
---

# Playwright Browser Automation for Security

Use Playwright's Chromium browser as an alternative to `web_extract` for:
- **JavaScript-rendered pages**: SPAs, React, Vue, Angular apps
- **Login automation**: Auto-fill credentials, handle MFA flows
- **Dynamic content**: Infinite scroll, lazy loading, websocket data
- **Visual recon**: Screenshots, DOM snapshots, accessibility trees
- **Network interception**: Capture API calls, modify requests/responses
- **Form fuzzing**: Automated form discovery and parameter fuzzing

## Installation (Playwright 1.61+)

### Python (main — for execute_code / terminal scripts)

```bash
# Python package
pip3 install --upgrade playwright

# Install Chromium browser (headless shell)
python3 -m playwright install chromium

# Optional: install all browsers
python3 -m playwright install

# Verify
python3 -c "from playwright.sync_api import sync_playwright; print('OK')"
python3 -m playwright --version  # should show 1.61.x
```

### Node.js CLI — @playwright/cli (NEW 2026-06)

`microsoft/playwright-cli` repo has been re-released as `@playwright/cli` npm package,
purpose-built for AI coding agents with token-efficient CLI + SKILLS system:

```bash
# Install globally
npm install -g @playwright/cli@latest
playwright-cli --help

# Install built-in skills (for Claude Code, Copilot, Hermes, etc.)
playwright-cli install --skills
```

Key CLI commands:
```bash
playwright-cli open https://target.com --headed      # open page (headless by default)
playwright-cli type "text"                            # type into focused element
playwright-cli press Enter                            # press keys
playwright-cli click e42                              # click element by ref
playwright-cli screenshot                             # capture screenshot
playwright-cli snapshot                               # get page accessibility snapshot
playwright-cli --help                                  # full command list
```

CLI vs Python API:
- **CLI** (`playwright-cli`): token-efficient, stateless, ideal for quick agent actions
- **Python API** (`playwright`): full control, complex scripting, network interception, CDP
- **Both share the same browser** — use CLI for quick tasks, Python for complex workflows

## Quick Start Scripts

### Script 1: Browser Intel Gatherer

Load via execute_code (adjust path for your profile):
```python
exec(open(os.path.expanduser(
    "~/.hermes/skills/red-teaming/playwright-browser/scripts/browser_intel.py"
)).read())
```

### Script 2: Automated Login & Session Capture

```python
exec(open(os.path.expanduser(
    "~/.hermes/skills/red-teaming/playwright-browser/scripts/auth_automation.py"
)).read())
```

### Script 3: Form Fuzzer

(Same pattern — form_fuzzer is embedded in SKILL.md examples below)

## Core Playwright Patterns

### Basic Browser Intel (JS-rendered pages)

```python
from playwright.sync_api import sync_playwright

def browser_intel(url: str, screenshot: bool = True, 
                  extract_links: bool = True, extract_forms: bool = True,
                  wait_for_network: bool = True, timeout: int = 30000):
    """Gather intelligence from a URL using a real browser."""
    results = {}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            viewport={'width': 1920, 'height': 1080},
        )
        page = context.new_page()
        
        # Enable request/response logging
        network_requests = []
        page.on('request', lambda req: network_requests.append({
            'url': req.url, 'method': req.method,
            'resource_type': req.resource_type,
        }))
        
        page.goto(url, wait_until='networkidle' if wait_for_network else 'domcontentloaded',
                  timeout=timeout)
        
        # Get page content
        results['title'] = page.title()
        results['url'] = page.url
        results['content'] = page.content()
        
        # Extract links
        if extract_links:
            links = page.eval_on_selector_all('a[href]', 
                'els => els.map(el => ({href: el.href, text: el.textContent.trim()}))')
            results['links'] = links
        
        # Extract forms
        if extract_forms:
            forms = page.eval_on_selector_all('form',
                '''els => els.map(f => ({
                    action: f.action,
                    method: f.method,
                    inputs: [...f.querySelectorAll('input[name],select[name],textarea[name]')]
                        .map(i => ({name: i.name, type: i.type}))
                }))''')
            results['forms'] = forms
        
        # Network requests (API endpoints, third-party)
        results['network'] = network_requests[:100]  # limit
        
        # Screenshot
        if screenshot:
            results['screenshot_path'] = '/tmp/browser_intel.png'
            page.screenshot(path=results['screenshot_path'], full_page=True)
        
        # Cookies
        results['cookies'] = context.cookies()
        
        browser.close()
    
    return results
```

### Automated Login & Session Capture

```python
def auto_login(url: str, username: str, password: str,
               username_selector: str = None, password_selector: str = None,
               submit_selector: str = None, login_url: str = None):
    """Automatically log in and capture session cookies/tokens."""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # Navigate to login page
        target = login_url or url
        page.goto(target, wait_until='networkidle')
        
        # Auto-detect login form if selectors not provided
        if not username_selector:
            # Common username field selectors
            for sel in ['input[name="username"]', 'input[name="email"]', 
                        'input[type="email"]', 'input[name="user"]',
                        '#username', '#email', '#login', '#user']:
                if page.locator(sel).count() > 0:
                    username_selector = sel
                    break
        
        if not password_selector:
            for sel in ['input[name="password"]', 'input[type="password"]', '#password']:
                if page.locator(sel).count() > 0:
                    password_selector = sel
                    break
        
        if not submit_selector:
            for sel in ['button[type="submit"]', 'input[type="submit"]', 
                        'button:has-text("Login")', 'button:has-text("Sign in")',
                        'button:has-text("登入")', 'button:has-text("登录")']:
                if page.locator(sel).count() > 0:
                    submit_selector = sel
                    break
        
        # Fill credentials
        page.fill(username_selector, username)
        page.fill(password_selector, password)
        
        # Click submit and wait for navigation
        with page.expect_navigation(wait_until='networkidle'):
            page.click(submit_selector)
        
        # Check if login succeeded
        current_url = page.url
        
        # Capture session data
        cookies = context.cookies()
        localStorage = page.evaluate('() => JSON.stringify(localStorage)')
        sessionStorage = page.evaluate('() => JSON.stringify(sessionStorage)')
        
        browser.close()
        
        return {
            'success': 'login' not in current_url.lower(),
            'final_url': current_url,
            'cookies': cookies,
            'localStorage': localStorage,
            'sessionStorage': sessionStorage,
        }
```

### Network Interception & API Discovery

```python
def intercept_network(url: str) -> dict:
    """Intercept all network requests to discover APIs, auth tokens, etc."""
    api_calls = []
    auth_headers = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # Intercept requests
        def handle_request(request):
            api_calls.append({
                'url': request.url,
                'method': request.method,
                'headers': dict(request.headers),
                'post_data': request.post_data,
            })
        
        # Intercept responses
        def handle_response(response):
            headers = dict(response.headers)
            # Look for auth tokens in response headers
            for key in ['authorization', 'x-auth-token', 'x-api-key', 'set-cookie', 'bearer']:
                if key in {k.lower() for k in headers}:
                    auth_headers.append({
                        'url': response.url,
                        'status': response.status,
                        'header': key,
                        'value': headers.get(key, headers.get(key.title(), '')),
                    })
        
        page.on('request', handle_request)
        page.on('response', handle_response)
        
        page.goto(url, wait_until='networkidle', timeout=30000)
        browser.close()
    
    # Filter API calls
    api_endpoints = [r for r in api_calls if 
        any(x in r['url'] for x in ['/api/', '/graphql', '/rest/', '/v1/', '/v2/'])]
    
    return {
        'all_requests': api_calls,
        'api_endpoints': api_endpoints,
        'auth_headers': auth_headers,
    }
```

### Form Fuzzer — Test for XSS/SQLi via Browser

```python
def fuzz_forms(target_url: str, form_selector: str = 'form') -> dict:
    """Automatically discover and fuzz forms on a page."""
    
    XSS_PAYLOADS = [
        '<img src=x onerror=alert(1)>',
        '"><img src=x onerror=alert(1)>',
        "'-alert(1)-'",
        '<svg/onload=alert(1)>',
    ]
    
    SQLI_PAYLOADS = [
        "'",
        "1' OR '1'='1",
        "1' AND 1=1--",
        "1' AND SLEEP(2)--",
    ]
    
    results = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        page.goto(target_url, wait_until='networkidle')
        
        # Find all forms
        form_count = page.locator(form_selector).count()
        
        for i in range(form_count):
            form = page.locator(form_selector).nth(i)
            
            # Get form inputs
            inputs = form.locator('input[name], textarea[name], select[name]')
            input_count = inputs.count()
            
            form_info = {
                'form_index': i,
                'action': form.get_attribute('action') or '',
                'method': form.get_attribute('method') or 'get',
                'findings': [],
            }
            
            for j in range(input_count):
                inp = inputs.nth(j)
                name = inp.get_attribute('name') or ''
                inp_type = inp.get_attribute('type') or 'text'
                
                if inp_type in ('submit', 'button', 'image', 'hidden', 'checkbox', 'radio'):
                    continue
                
                # Test with XSS payloads
                for payload in XSS_PAYLOADS[:2]:
                    try:
                        inp.fill(payload)
                        # Check for reflected XSS in page
                        content = page.content()
                        if payload in content:
                            form_info['findings'].append({
                                'type': 'potential_xss',
                                'field': name,
                                'payload': payload,
                                'evidence': 'payload reflected in page',
                            })
                    except:
                        pass
                
                # Reset and test with SQLi payloads
                try:
                    inp.fill(SQLI_PAYLOADS[1])  # OR 1=1
                except:
                    pass
            
            if form_info['findings']:
                results.append(form_info)
        
        browser.close()
    
    return results
```

### Screenshot Capture & Visual Diffing

```python
def capture_state(url: str, output_path: str = None) -> dict:
    """Capture screenshots and DOM state."""
    output = output_path or '/tmp/browser_capture.png'
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        
        page.goto(url, wait_until='networkidle', timeout=30000)
        
        # Full page screenshot
        page.screenshot(path=output, full_page=True)
        
        # Also capture viewport-only
        viewport_path = output.replace('.png', '_viewport.png')
        page.screenshot(path=viewport_path, full_page=False)
        
        # Accessibility tree (useful for understanding page structure)
        accessibility = page.accessibility.snapshot()
        
        # Console logs
        console_logs = []
        page.on('console', lambda msg: console_logs.append(f'[{msg.type}] {msg.text}'))
        
        browser.close()
    
    return {
        'full_screenshot': output,
        'viewport_screenshot': viewport_path,
        'title': page.title(),
        'accessibility_tree': accessibility,
        'console_logs': console_logs,
    }
```

## Script Template for execute_code

When using Playwright in execute_code, use this pattern:

```python
# Note: execute_code runs in a sandbox without the playwright package
# Use terminal() to run playwright scripts instead

from hermes_tools import terminal

# Write the script to a temp file and execute it
script = '''
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com")
    print(page.title())
    browser.close()
'''

write_file('/tmp/playwright_script.py', script)
result = terminal('python3 /tmp/playwright_script.py')
```

## Integration with Other Skills

### Chain: Playwright → pentesting
```
1. Use playwright to login and capture session cookies
2. Pass cookies to web-app-pentest for authenticated scanning
3. Use form_fuzzer to discover injection points
```

### Chain: Playwright → OSINT
```
1. Use browser_intel to capture JS-rendered content
2. Use network interception to discover hidden API endpoints
3. Pass findings to parallel-intel for deeper research
```

### Chain: Playwright → Client-side auth bypass
```
1. Use Playwright to load the packed JavaScript
2. Extract auth functions dynamically
3. Use client-side-auth-bypass to reverse the encoding
```

### Chain: Playwright → Monitoring Dashboard Capture
```
1. Use auto_login to authenticate into the target web app
2. Navigate to authenticated dashboard (e.g., /monitor/)
3. page.wait_for_timeout(3000) — let HLS/WebSocket feeds initialize
4. page.screenshot(full_page=True) — capture full dashboard with live feeds
5. Optional: page.eval_on_selector_all to extract all camera names/states
```

### HLS Video State Verification

After loading a monitoring page with HLS video players, check video states in JS:
```python
video_states = page.eval_on_selector_all('video',
    'els => els.map(v => ({'
    '  src: v.getAttribute("data-src"),'
    '  readyState: v.readyState,     # 4 = HAVE_ENOUGH_DATA = live'
    '  paused: v.paused,             # false = actively playing'
    '  duration: v.duration          # seconds of buffer'
    '}))'
)
```
`readyState=4` + `paused=false` confirms live camera feeds are accessible.

## JavaScript Injection for Hidden/JS-Dependent Forms

When radio buttons or form elements are hidden by CSS (Playwright reports "element is not visible"), use `page.evaluate()` to set form values directly and submit via `fetch()`:

```python
# Set hidden form fields via JS
page.evaluate('''(data) => {
    document.querySelector('#hidden_field_id').value = data.value;
    return document.querySelector('#csrf_token').value;
}''', {'value': 'payload_here'})

# Submit via fetch() with X-CSRFToken header (Flask-WTF AJAX pattern)
resp = page.evaluate('''(data) => {
    return fetch('/endpoint/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': data.csrf
        },
        body: new URLSearchParams({
            'csrf_token': data.csrf,
            'hidden_field': data.value,
            'name': data.payload
        }).toString()
    }).then(r => r.text());
}''', {'csrf': csrf_token, 'value': vid, 'payload': injection_payload})
```

This bypasses visibility checks, click interception, and complex UI flows. Use when:
- Radio buttons are `display:none` or hidden by parent containers
- Forms rely on JavaScript to populate hidden fields before submission
- The UI requires multi-step interactions that are timing-dependent

## Pitfalls

- **Headless detection**: Some sites detect headless browsers via navigator.webdriver. Use `args=['--disable-blink-features=AutomationControlled']`
- **Browser fingerprinting**: Sites may block based on fingerprint — use stealth plugins
- **Memory usage**: Each browser instance uses ~200-500MB RAM — close browsers after use
- **Timeout handling**: JS-heavy SPAs may need longer `wait_until='networkidle'` timeouts
- **Certificate errors**: Set `ignore_https_errors=True` for testing internal/self-signed sites
- **Resource blocking**: Block images/fonts for faster scraping: `page.route('**/*.{png,jpg,jpeg,gif,svg,css,font,woff,woff2}', lambda route: route.abort())`
- **Hidden form elements**: When `Locator.click` fails with "element is not visible", don't waste time forcing visibility — use `page.evaluate()` to set values and `fetch()` to submit. See JS Injection section above
- **Flask CSRF in AJAX**: Flask-WTF expects `X-CSRFToken` header for AJAX POSTs. Include it alongside the form-body `csrf_token` field
- **Context exhaustion in password loops**: NEVER create/destroy `browser.new_context()` inside a tight password-brute-force loop. Each context spawns a separate browser profile and the Node.js process accumulates file descriptors, eventually crashing with `EPIPE` or `write EPIPE`. Instead: (a) create ONE context, reuse it for all password attempts, clearing cookies between tries with `context.clear_cookies()`, or (b) use `requests.Session()` for form-based login brute force (100x faster) and reserve Playwright only for JS-rendered SPAs where requests can't work.
- **EPIPE crash in password loops**: Creating and destroying `browser.new_context()` inside a per-password loop (e.g., brute-forcing a login form) causes a Node.js EPIPE error after ~10-20 iterations. The Playwright pipe transport breaks under rapid context churn. **Fix**: Create ONE context and reuse it for all password attempts — clear cookies and reload the page per attempt. Use `context.clear_cookies()` and `page.goto()` rather than creating new contexts. If the site's login state persists across page reloads via localStorage/sessionStorage, use `context.storage_state()` to save and restore clean state. For more than ~30 attempts, switch to `requests` + form POST instead — Playwright is too slow for large-scale brute force.
- **macOS `timeout` command**: macOS (zsh) does not support bash's `/dev/tcp` for port scanning. Use Python's `socket` module instead: `socket.socket().connect_ex((ip, port))`.
- **Element UI / Vue SPAs**: Modern Chinese surveillance/DVR dashboards often use Element UI (class `el-input__inner`). Inputs typically lack `name`/`id` attributes — use placeholder-based selectors: `page.locator('input[placeholder="User Name"]')`, `page.locator('input[placeholder="Password"]')`. Buttons similarly: `page.locator('button:has-text("Log In")')`. After clicking, SPA routing (hash-based or pushState) means `page.expect_navigation()` often times out — use `page.wait_for_timeout(5000)` then check `page.url` instead.
- **SPA login that stays on the same URL**: When the page appears to stay on `/login` after clicking submit, the login may have failed silently (wrong credentials) rather than the button not working. Check `page.content()` for error toasts/messages from the JS framework.
- **`context.request.get()` also blocked by Cloudflare**: When a site is behind Cloudflare, even the browser's `context.request.get()` method returns Cloudflare challenge pages (403, ~6KB HTML). It uses a different TLS stack than the page context. For Cloudflare-protected downloads, use `page.goto()` with the download URL to trigger a native browser download, or use JavaScript `fetch()` inside `page.evaluate()`.

- **CTFd API calls via browser context**: When CTFd is behind Cloudflare, `curl` with a valid session cookie or token header still gets blocked by Cloudflare's TLS fingerprinting. Only requests through the real browser's TLS stack pass. For flag submission, either use Playwright to fill the flag input on the challenge page and click submit, or navigate to the API URL directly in a new browser tab via `page.goto()`.

- **Cloudflare Turnstile bypass via Real Chrome**: Playwright's bundled Chromium is detected by Cloudflare Turnstile even with `playwright-stealth`. Use real Google Chrome via `channel="chrome"` — it passes Turnstile automatically in ~5-10 seconds:
  ```python
  context = p.chromium.launch_persistent_context(
      user_data_dir="/tmp/profile",
      channel="chrome",   # use real Chrome, not Playwright's bundled one
      headless=False,     # headed works most reliably
      args=["--disable-blink-features=AutomationControlled"],
  )
  ```
  Bundled Chromium + stealth never passes; real Chrome always passes.

- **NEVER kill the user's Chrome**: Do not use `pkill -f "Google Chrome"`. If a profile is in use, create a profile with a different path (e.g., `/tmp/profile2`) instead of force-closing the user's browser.
- **Node 25 llhttp dylib mismatch (macOS)**: Homebrew's `node` (v25) was compiled against `libllhttp.9.3.dylib` but `brew reinstall llhttp` installs `9.4.2`, causing `Abort trap: 6` on `node --version`. Use Node 24 instead: `export PATH="$HOME/homebrew/opt/node@24/bin:$PATH"`. Node 24 works for all `npm install -g` operations including `@playwright/cli` and `@playwright/test`. See `references/playwright-cli.md` for details.

---

## Advanced Security Testing Patterns (2025-2026)

### 1. Playwright 1.50+ New Features for Security Testing

**HAR Tracing (v1.60+):** First-class HAR recording integrated into tracing for network debugging.

```python
# Record HAR + trace together
await context.tracing.start(screenshots=True, snapshots=True)
await context.tracing.start_har("trace.har", url_filter="**/api/**")
page.goto("https://target.com")
await context.tracing.stop(path="trace.zip")
await context.tracing.stop_har()
# Open with: playwright show-trace trace.zip
```

**APIRequestContext (v1.16+):** Standalone API testing without browser — share auth state with browser context.

```python
# API-first auth, then browser session
api = await request.new_context(base_url="https://api.target.com", extra_http_headers={"Authorization": f"Bearer {token}"})
resp = await api.get("/v1/user/profile")
assert resp.ok
# Inject token into browser
context = await browser.new_context(storage_state={"origins": [{"origin": "https://target.com", "localStorage": [{"name": "auth_token", "value": token}]}]})
```

**Route Interception Enhancements (v1.48+):** `route.abort()`, `route.fulfill()`, `route.continue_()` with regex/glob matching.

```python
# Block tracking, modify responses, inject faults
await page.route("**/*.{png,jpg,css,woff2}", lambda r: r.abort())
await page.route("**/api/**", lambda r: r.fulfill(status=200, json={"injected": True}))
await page.route("**/graphql", lambda r: r.continue_(
    post_data=r.request.post_data.replace('"query"', '"query","debug":true')
))
```

**Tracing.startHar() / WebStorage API (v1.60+):** HAR as first-class trace API; `page.local_storage` / `page.session_storage` for direct storage manipulation.

```python
# Direct storage manipulation without JS evaluation
await page.local_storage.set_item("bypass_2fa", "true")
await page.session_storage.set_item("admin_mode", "1")
```

**Browser.bind() + connect_over_cdp() (v1.59+):** Share browser sessions across processes/agents via named pipe or WebSocket.

```python
# Server: bind browser for remote agents
server_info = await browser.bind("sec-session", host="0.0.0.0", port=9222)
# Client (Playwright CLI or another script): connect
browser = await chromium.connect_over_cdp(server_info["endpoint"])
```

---

### 2. Headless Detection Bypass — Stealth Mode & page.add_init_script

**playwright-stealth** (Python) / **playwright-extra** + stealth plugin (Node) — patches 15+ fingerprint vectors.

```python
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-features=IsolateOrigins,site-per-process",
            "--disable-dev-shm-usage",
            "--disable-accelerated-2d-canvas",
            "--no-first-run",
            "--no-zygote",
        ],
    )
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        screen={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        locale="en-US",
        timezone_id="America/New_York",
        extra_http_headers={
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
        },
    )
    page = context.new_page()
    stealth_sync(page)  # Patches navigator.webdriver, plugins, chrome.runtime, permissions
    page.goto("https://target.com")
```

**Manual `page.add_init_script` for custom patches (runs before any page JS):**

```python
# Override canvas/WebGL fingerprint before page loads
await page.add_init_script("""
    // Canvas fingerprint noise
    const origToDataURL = HTMLCanvasElement.prototype.toDataURL;
    HTMLCanvasElement.prototype.toDataURL = function(type) {
        const ctx = this.getContext('2d');
        ctx.fillStyle = 'rgba(' + Math.random()*255 + ',' + Math.random()*255 + ',' + Math.random()*255 + ',0.01)';
        ctx.fillRect(0, 0, 1, 1);
        return origToDataURL.apply(this, arguments);
    };
    // WebGL renderer spoof
    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(p) {
        if (p === 37445) return 'Intel Inc.';  // UNMASKED_VENDOR_WEBGL
        if (p === 37446) return 'Intel Iris OpenGL Engine';  // UNMASKED_RENDERER_WEBGL
        return getParameter.apply(this, arguments);
    };
""")
```

**Persistent profile for cookie/localStorage survival across runs:**

```python
context = await p.chromium.launch_persistent_context(
    user_data_dir="./browser_profile",
    headless=True,
    args=["--disable-blink-features=AutomationControlled"],
)
```

---

### 3. Chrome DevTools Protocol (CDP) Security Features

**CDP Domains for security testing:** `Network`, `Security`, `Page`, `Runtime`, `Audits`.

```python
# Connect via CDP for low-level control
cdp = await page.context.new_cdp_session(page)
# Enable security domain
await cdp.send("Security.enable")
# Override certificate errors
await cdp.send("Security.setOverrideCertificateErrors", {"override": True})
# Get certificate details
cert = await cdp.send("Security.getCertificate", {"origin": "https://target.com"})
# TLS/SSL details
security_state = await cdp.send("Security.getVisibleSecurityState")
# JA3/JA4 fingerprint (requires mitmproxy or custom TLS client)
# Network domain: intercept before request sent
await cdp.send("Network.enable")
await cdp.send("Network.setRequestInterception", {"patterns": [{"urlPattern": "*", "resourceType": "Document", "interceptionStage": "Request"}]})
```

**Key CDP events:** `Security.certificateError`, `Security.securityStateChanged`, `Network.requestWillBeSent`, `Network.responseReceived`.

---

### 4. Mobile Browser Emulation for Security Testing (iOS Safari / Android Chrome)

**Built-in device descriptors (Playwright 1.50+):**

```python
from playwright.sync_api import sync_playwright

# iPhone 15 Pro (iOS Safari via WebKit)
with sync_playwright() as p:
    iphone = p.devices["iPhone 15 Pro"]
    context = p.webkit.launch_persistent_context(
        user_data_dir="./iphone_profile",
        headless=True,
        **iphone,
        locale="en-US",
        timezone_id="America/Los_Angeles",
    )
    page = context.pages[0] or context.new_page()
    page.goto("https://target.com")

# Pixel 8 (Android Chrome via Chromium)
pixel = p.devices["Pixel 8"]
context = p.chromium.launch_persistent_context(
    user_data_dir="./pixel_profile",
    headless=True,
    **pixel,
    args=["--disable-blink-features=AutomationControlled"],
)
```

**Custom mobile context (fine-grained control):**

```python
context = browser.new_context(
    **p.devices["iPhone 13"],
    # Override specific properties
    geolocation={"latitude": 37.7749, "longitude": -122.4194},
    permissions=["geolocation"],
    color_scheme="dark",
    is_mobile=True,
    has_touch=True,
    java_script_enabled=True,
)
```

**Security-relevant mobile vectors to test:**
- Touch event handling (no hover)
- Viewport meta tag behavior
- iOS Safari WebKit quirks (no WebRTC in some versions, different CSP)
- Android Chrome intent:// scheme handling
- PWA install prompts / service worker behavior
- Biometric auth (WebAuthn) on mobile

---

### 5. Authenticated SPA Crawling — Session Export/Import

**Storage state (cookies + localStorage + sessionStorage) — full session persistence:**

```python
# After login, save full state
storage = await context.storage_state(path="session.json")
# Later: restore in new context
context = await browser.new_context(storage_state="session.json")
# Or load selectively
import json
state = json.load(open("session.json"))
context = await browser.new_context(storage_state=state)
```

**Cookie-only export for `curl` / `requests` (Netscape format):**

```python
def cookies_to_netscape(cookies):
    lines = ["# Netscape HTTP Cookie File"]
    for c in cookies:
        lines.append(f"{c['domain']}\tTRUE\t{c['path']}\t{'TRUE' if c['secure'] else 'FALSE'}\t{int(c.get('expires', 0))}\t{c['name']}\t{c['value']}")
    return "\n".join(lines)

cookies = context.cookies()
with open("cookies.txt", "w") as f:
    f.write(cookies_to_netscape(cookies))
# Use: curl -b cookies.txt https://target.com/api/...
```

**API-first authentication (fast) + browser session injection:**

```python
# 1. Login via API (requests/httpx — 100x faster than browser)
import httpx
resp = httpx.post("https://api.target.com/auth/login", json={"user": "x", "pass": "y"})
token = resp.json()["access_token"]

# 2. Inject into browser context
context = await browser.new_context(
    storage_state={
        "origins": [{
            "origin": "https://target.com",
            "localStorage": [{"name": "access_token", "value": token}]
        }]
    }
)
```

---

### 6. WebSocket Interception & Fuzzing

**Playwright 1.48+ native WebSocket routing (`page.route_websocket` / `context.route_websocket`):**

```python
# Intercept and log all WebSocket traffic
ws_messages = []

async def on_ws(route):
    ws = await route.connect_to_server()
    # Log client -> server
    ws.on("message", lambda msg: ws_messages.append(("client->server", msg)))
    # Log server -> client
    ws.on("message", lambda msg: ws_messages.append(("server->client", msg)))
    # Forward
    route.continue_()

await page.route_websocket("wss://target.com/**", on_ws)
```

**Fuzzing WebSocket messages (modify in transit):**

```python
async def fuzz_ws(route):
    ws = await route.connect_to_server()
    # Hook client messages: mutate before forwarding
    ws.on("message", async (msg) => {
        if (typeof msg === "string") {
            try {
                const data = JSON.parse(msg);
                // Inject fuzz payloads
                if (data.user_input) data.user_input = "' OR 1=1--";
                if (data.id) data.id = "../../etc/passwd";
                await ws.send(JSON.stringify(data));
                return;  # Don't forward original
            } catch {}
        }
        await ws.send(msg);  # Forward unchanged
    })
    # Hook server messages: inspect for data leaks
    ws.on("message", (msg) => {
        if (msg.includes("password") || msg.includes("token")) {
            console.log("[LEAK]", msg);
        }
    });

await page.route_websocket("wss://api.target.com/ws", fuzz_ws)
```

**WebSocket vulnerability checks (CSWSH, auth bypass, message tampering):**

```python
# 1. Cross-Site WebSocket Hijacking — test if origin not validated
# Connect from different origin (via page.evaluate fetch to ws://)
# 2. Auth token in WS handshake — intercept upgrade request
# 3. Message replay — capture and re-send sensitive frames
# 4. Binary frame fuzzing — send malformed binary data
```

---

### 7. CTFd / CTF Platform Automation Patterns

**CTFd API + browser automation hybrid (login via API, browse challenges via browser):**

```python
import httpx
from playwright.sync_api import sync_playwright

# 1. API login to get session
resp = httpx.post("https://ctf.target.com/login", data={"name": "user", "password": "pass"})
session_cookie = resp.cookies.get("session")

# 2. Browser with pre-authenticated session
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    context.add_cookies([{"name": "session", "value": session_cookie, "domain": "ctf.target.com", "path": "/"}])
    page = context.new_page()
    page.goto("https://ctf.target.com/challenges")
    # Auto-submit flags
    challenges = page.locator(".challenge-row").all()
    for ch in challenges:
        ch.click()
        flag_input = page.locator("input[name=flag]")
        flag_input.fill("FLAG{...}")
        page.click("button:has-text('Submit')")
```

**Automated challenge enumeration + flag submission:**

```python
async def ctf_automation(ctfd_url, username, password, flags_dict):
    """flags_dict = {challenge_id: 'FLAG{...}'}"""
    async with httpx.AsyncClient() as client:
        await client.post(f"{ctfd_url}/login", data={"name": username, "password": password})
        challenges = (await client.get(f"{ctfd_url}/api/v1/challenges")).json()["data"]
        for ch in challenges:
            if str(ch["id"]) in flags_dict:
                await client.post(f"{ctfd_url}/api/v1/challenges/attempt", json={
                    "challenge_id": ch["id"],
                    "submission": flags_dict[str(ch["id"])]
                })
```

**Real CTF patterns (extracted from 2024-2025 events):**
- **Scoreboard scraping**: Poll `/api/v1/scoreboard` for real-time ranking
- **Challenge file download**: Use `page.route("**/files/**")` to capture challenge binaries
- **Containerized challenge access**: Some CTFs expose challenge ports via subdomains — enumerate via certificate transparency logs
- **Multi-user team coordination**: Use shared `storage_state` across browser instances

---

### 8. Proxy / CDP Integration with Burp Suite / mitmproxy

**Playwright → mitmproxy → Burp Suite chain (recommended for HTTPS):**

```bash
# Terminal 1: mitmproxy as upstream proxy to Burp
mitmproxy --mode upstream:https://127.0.0.1:8080 --ssl-insecure

# Terminal 2: Burp Suite listening on 8080 (Proxy → Options → Proxy Listeners)

# Terminal 3: Playwright script
python3 playwright_script.py
```

```python
# Playwright: route through mitmproxy (port 8080)
browser = p.chromium.launch(
    proxy={"server": "http://127.0.0.1:8080"},
    args=["--ignore-certificate-errors", "--ignore-certificate-errors-spki-list"]
)
context = browser.new_context(ignore_https_errors=True)
```

**mitmproxy addons for security testing (save as `mitm_addon.py`):**

```python
# mitmproxy addon: JWT tagging, JA3 logging, SSL pinning bypass hooks
from mitmproxy import http, ctx

def request(flow: http.HTTPFlow) -> None:
    # Tag requests with JWT in Authorization header
    auth = flow.request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        flow.request.headers["X-JWT-Tagged"] = "true"

def tls_clienthello(data):
    # Log JA3 fingerprint
    ctx.log.info(f"JA3: {data.ja3}")
```

Run: `mitmproxy -s mitm_addon.py --mode upstream:https://127.0.0.1:8080`

**Browserless + Playwright (cloud browsers with stealth + residential proxies):**

```python
from playwright.sync_api import sync_playwright

BROWSERLESS_WS = "wss://chrome.browserless.io/playwright/chromium?token=YOUR_TOKEN&stealth=true&proxy=residential"

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(BROWSERLESS_WS)
    context = browser.contexts[0] if browser.contexts else browser.new_context()
    page = context.pages[0] if context.pages else context.new_page()
    page.goto("https://target.com")
```

---

### 9. Canvas/WebGL Fingerprinting for Browser De-anonymization

**Capture fingerprint for profiling / comparison:**

```python
async def capture_fingerprint(page):
    fp = await page.evaluate("""() => {
        const canvas = document.createElement('canvas');
        canvas.width = 200; canvas.height = 50;
        const ctx = canvas.getContext('2d');
        ctx.textBaseline = 'top';
        ctx.font = '14px Arial';
        ctx.fillStyle = '#f60';
        ctx.fillRect(10, 10, 100, 40);
        ctx.fillStyle = '#069';
        ctx.fillText('Fingerprint 🎭', 20, 15);
        const canvasHash = canvas.toDataURL();
        
        const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
        const webgl = gl ? {
            vendor: gl.getParameter(gl.VENDOR),
            renderer: gl.getParameter(gl.RENDERER),
            unmaskedVendor: gl.getParameter(37445),  // UNMASKED_VENDOR_WEBGL
            unmaskedRenderer: gl.getParameter(37446), // UNMASKED_RENDERER_WEBGL
            version: gl.getParameter(gl.VERSION),
            shadingLanguageVersion: gl.getParameter(gl.SHADING_LANGUAGE_VERSION),
            extensions: gl.getSupportedExtensions(),
        } : null;
        
        return {
            canvasHash,
            webgl,
            screen: {width: screen.width, height: screen.height, colorDepth: screen.colorDepth, pixelRatio: window.devicePixelRatio},
            navigator: {userAgent: navigator.userAgent, platform: navigator.platform, hardwareConcurrency: navigator.hardwareConcurrency, deviceMemory: navigator.deviceMemory, languages: navigator.languages},
            plugins: Array.from(navigator.plugins).map(p => p.name),
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        };
    }""")
    return fp
```

**Fingerprint comparison / de-anonymization:**

```python
import hashlib
def normalize_fp(fp):
    # Stable subset for comparison
    stable = {
        "canvas": fp["canvasHash"][:100],  # Prefix
        "webgl_vendor": fp["webgl"]["unmaskedVendor"] if fp["webgl"] else None,
        "webgl_renderer": fp["webgl"]["unmaskedRenderer"] if fp["webgl"] else None,
        "screen": fp["screen"],
        "nav_hw": {k: fp["navigator"][k] for k in ["hardwareConcurrency", "deviceMemory"]},
        "timezone": fp["timezone"],
    }
    return hashlib.sha256(str(stable).encode()).hexdigest()[:16]

# Cluster sessions by fingerprint
fingerprints = {}
for session_id, fp in all_sessions.items():
    fp_hash = normalize_fp(fp)
    fingerprints.setdefault(fp_hash, []).append(session_id)
# fingerprints with >1 session = likely same user/bot
```

**playwright-with-fingerprints (bablosoft) — real device fingerprint rotation:**

```bash
pip install playwright-with-fingerprints
```

```python
from playwright_with_fingerprints import PlaywrightWithFingerprints

async with PlaywrightWithFingerprints() as pw:
    browser = await pw.chromium.launch(headless=True)
    # Each new_context gets a unique real-device fingerprint
    context = await browser.new_context(fingerprint="random")
    page = await context.new_page()
    await page.goto("https://target.com")
```

---

### 10. Playwright über TCP/IP / Browserless / Remote Playwright

**connect_over_cdp() — connect to remote Chrome/CDP endpoint:**

```python
# Local Chrome with remote debugging
# chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-profile
browser = await chromium.connect_over_cdp("http://localhost:9222")
```

**Browser.bind() (v1.59+) — expose local browser for remote agents:**

```python
# Server side: launch and bind
server_info = await browser.bind("pentest-session", host="0.0.0.0", port=9222)
print(f"Endpoint: {server_info['endpoint']}")  # ws://0.0.0.0:9222/...
# Client side: connect
browser = await chromium.connect_over_cdp(server_info["endpoint"])
```

**Browserless.io — managed cloud browsers via CDP WebSocket:**

```python
BROWSERLESS = "wss://chrome.browserless.io/playwright/chromium?token=TOKEN&stealth=true&proxy=residential&blockAds=true"
browser = await chromium.connect_over_cdp(BROWSERLESS)
# Features: auto stealth, residential proxies, CAPTCHA solving, session recording
```

**playwright-cli attach (v1.59+) — CLI access to bound browsers:**

```bash
# List bound sessions
playwright-cli show
# Attach to named session
playwright-cli attach pentest-session
# Snapshot current state
playwright-cli -s pentest-session snapshot
```

**Docker / Kubernetes deployment (headless-shell for CI):**

```dockerfile
# Use Chrome for Testing headless-shell (Playwright 1.57+)
FROM mcr.microsoft.com/playwright:v1.60-jammy
WORKDIR /app
COPY . .
CMD ["python", "scraper.py"]
```

```yaml
# Kubernetes: Playwright as sidecar
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: playwright
    image: mcr.microsoft.com/playwright:v1.60-jammy
    command: ["sleep", "infinity"]
    ports:
    - containerPort: 9222
  - name: app
    image: myapp
    env:
    - name: PLAYWRIGHT_CDP_ENDPOINT
      value: "ws://localhost:9222"
```

---

### Quick Reference: Security Testing Checklist

| Area | Key APIs / Tools | Version |
|------|------------------|---------|
| **CLI (agent)** | `playwright-cli open/type/click/screenshot/snapshot` | @playwright/cli 1.61+ |
| Network interception | `page.route()`, `page.route_websocket()`, `context.route()` | 1.16+ |
| API testing | `request.new_context()`, `api.post()`, shared auth | 1.16+ |
| Tracing/HAR | `context.tracing.start()`, `context.tracing.start_har()` | 1.12+ / 1.60+ |
| Stealth | `playwright-stealth`, `page.add_init_script()`, persistent context | 3rd party |
| Mobile emulation | `p.devices["iPhone 15 Pro"]`, `p.devices["Pixel 8"]` | Built-in |
| Session persistence | `context.storage_state()`, `launch_persistent_context()` | 1.10+ |
| CDP | `page.context.new_cdp_session()`, `browser.connect_over_cdp()` | 1.8+ |
| Remote | `browser.bind()`, Browserless, `playwright-cli attach` | 1.59+ |
| Fingerprinting | Canvas/WebGL `page.evaluate()`, `playwright-with-fingerprints` | Custom |
| Proxy chain | `proxy={"server": "http://..."}`, mitmproxy upstream to Burp | Built-in |

## References

- `references/cloudflare-turnstile-bypass.md` — Cloudflare Turnstile bypass via real Chrome CDP (Playwright bundled Chromium fails, real Chrome passes)
- `references/chatgpt-web-relay.md` — ChatGPT Web Relay MCP server (Playwright + CDP, zero-API-quota ChatGPT access)
- `references/playwright-cli.md` — `@playwright/cli` (microsoft/playwright-cli) agent-optimized CLI: installation, commands, config schema, env vars, built-in skills, Node 25 llhttp pitfall
