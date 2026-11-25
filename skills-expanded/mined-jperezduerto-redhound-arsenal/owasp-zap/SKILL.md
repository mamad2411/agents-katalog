---
name: owasp-zap
description: >
  Use and operate OWASP ZAP (Zed Attack Proxy) — the world's most widely used free web application
  security scanner. Use when performing web application penetration testing, running automated DAST
  scans, configuring a proxy for manual testing, handling authentication for scans, integrating
  security scanning into CI/CD pipelines, or comparing ZAP with Burp Suite. Covers installation,
  proxy setup, spider, active/passive scanning, Ajax Spider, authentication handling, ZAP API,
  Docker automation scripts (zap-baseline.py, zap-full-scan.py, zap-api-scan.py), scan policies,
  Zest scripting, and marketplace add-ons. GitHub: https://github.com/zaproxy/zaproxy (14.9k stars).
license: Apache-2.0
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/zaproxy/zaproxy
  language: Java
---

# owasp-zap Agent Skill

## When to Use This Skill

Use this skill when:
- Setting up ZAP as an intercepting proxy for manual web app testing
- Running automated baseline, full, or API scans against a target application
- Configuring authentication (form-based, script-based, token-based) for authenticated scans
- Integrating ZAP scans into GitHub Actions, Jenkins, or other CI/CD pipelines
- Using the ZAP REST API or Python client for programmatic control
- Writing Zest or JavaScript scripts to automate custom scan logic
- Comparing ZAP's capabilities against Burp Suite for tooling decisions

## What OWASP ZAP Does

ZAP (Zed Attack Proxy) is a Java-based DAST (Dynamic Application Security Testing) tool that intercepts browser traffic via proxy, spiders application content, and runs passive and active security checks against web applications. It serves both as a hands-on proxy for manual testers and as a fully automated scanner suitable for CI/CD pipelines. ZAP v2.17.0 is the current stable release, now maintained by Checkmarx.

## Installation

### Cross-Platform Installer (GUI + daemon)
```bash
# Download from https://www.zaproxy.org/download/
# Linux installer
chmod +x ZAP_2_17_0_unix.sh
./ZAP_2_17_0_unix.sh

# macOS — Homebrew
brew install --cask owasp-zap

# Windows — Chocolatey
choco install zaproxy
```

### Snap (Linux)
```bash
sudo snap install zaproxy --classic
zap.sh -daemon -host 0.0.0.0 -port 8080 -config api.key=your-api-key
```

### Docker (preferred for CI/CD)
```bash
# Stable image
docker pull ghcr.io/zaproxy/zaproxy:stable
# or: docker pull zaproxy/zap-stable

# Weekly (latest features)
docker pull ghcr.io/zaproxy/zaproxy:weekly

# Bare (minimal CI image — no GUI)
docker pull ghcr.io/zaproxy/zaproxy:bare
```

### Run ZAP Headless Daemon
```bash
zap.sh -daemon -host 127.0.0.1 -port 8080 \
  -config api.key=changeme \
  -config api.addrs.addr.name=.* \
  -config api.addrs.addr.enabled=true
```

## Core Concepts

### Scan Modes
| Mode | Description |
|---|---|
| **Passive Scan** | Analyzes proxied traffic — no new requests. Always-on. |
| **Spider** | Crawls links recursively from a start URL. Fast but misses JS-heavy apps. |
| **Ajax Spider** | Uses Selenium/browser to crawl JS-rendered pages (slower, more thorough). |
| **Active Scan** | Sends attack payloads (SQLi, XSS, etc.) against discovered URLs. |

### Proxy Configuration

ZAP listens on `127.0.0.1:8080` by default.

**Firefox (manual)**: Preferences → Network Settings → Manual Proxy → HTTP Proxy: `127.0.0.1`, Port: `8080`

**FoxyProxy browser extension** (recommended for quick toggle):
- Add entry: proxy `127.0.0.1:8080`
- Import ZAP CA cert: Tools → Options → Dynamic SSL Certificates → Save, then import into browser trust store.

**Install ZAP CA certificate** (required for HTTPS interception):
```bash
# Export cert from ZAP GUI: Tools → Options → Network → Server Certificates → Save
# Or from API:
curl "http://localhost:8080/OTHER/core/other/rootcert/?apikey=changeme" -o zap-ca.cer

# Import into Firefox (about:preferences → Certificates → Import)
# Import into system store (Linux)
sudo cp zap-ca.cer /usr/local/share/ca-certificates/zap-ca.crt
sudo update-ca-certificates
```

## CLI and Docker Automation Scripts

### zap-baseline.py — Passive-Only Scan (CI-safe)
Runs spider (1 minute default) + passive scan. No active attacks. Safe for production pipelines.
```bash
# Basic baseline scan
docker run --rm -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t https://target.example.com

# With HTML report
docker run --rm -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t https://target.example.com -r baseline-report.html

# Fail on WARN or higher
docker run --rm -t ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t https://target.example.com -l WARN

# Ignore specific rules (by ID)
docker run --rm -t ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t https://target.example.com -c zap-baseline.conf

# Extended spider time (minutes)
docker run --rm -t ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t https://target.example.com -m 5

# Key flags
# -t  Target URL
# -r  HTML report file (in /zap/wrk/ when using Docker volume)
# -J  JSON report file
# -x  XML report file
# -w  MARKDOWN report file
# -l  Minimum alert level: PASS | WARN | FAIL (default WARN)
# -c  Configuration file (alert overrides)
# -m  Spider minutes (default 1)
# -a  Include Ajax Spider
# -d  Debug mode
```

### zap-full-scan.py — Spider + Active Scan
Full attack scan including active checks. Not safe for production without explicit authorization.
```bash
# Basic full scan
docker run --rm -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable \
  zap-full-scan.py -t https://target.example.com -r full-report.html

# With Ajax Spider enabled
docker run --rm -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable \
  zap-full-scan.py -t https://target.example.com -r full-report.html -a

# Fail build on FAIL-level alerts
docker run --rm -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable \
  zap-full-scan.py -t https://target.example.com -r full-report.html -I

# Custom scan policy
docker run --rm -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable \
  zap-full-scan.py -t https://target.example.com -r full.html --hook=/zap/wrk/myhooks.py
```

### zap-api-scan.py — API Scanning (OpenAPI / GraphQL / SOAP)
```bash
# OpenAPI spec from URL
docker run --rm -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py -t https://api.example.com/openapi.json -f openapi -r api-report.html

# OpenAPI spec from local file
docker run --rm -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py -t /zap/wrk/openapi.json -f openapi -r api-report.html

# GraphQL
docker run --rm -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py -t https://api.example.com/graphql -f graphql -r api-report.html

# SOAP WSDL
docker run --rm -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py -t https://api.example.com/service?wsdl -f soap -r api-report.html

# Key flags: -t (target), -f (format: openapi|soap|graphql), -r (report)
```

## ZAP REST API

ZAP exposes a REST API on the proxy port. All action calls require `apikey`.

### Python Client
```bash
pip install python-owasp-zap-v2.4
```

```python
from zapv2 import ZAPv2
import time

zap = ZAPv2(apikey='changeme', proxies={
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
})

target = 'https://target.example.com'

# Spider
print('Starting spider...')
scan_id = zap.spider.scan(target, maxchildren=None, recurse=True)
while int(zap.spider.status(scan_id)) < 100:
    print(f'  Spider progress: {zap.spider.status(scan_id)}%')
    time.sleep(2)

# Ajax Spider
zap.ajaxSpider.scan(target)
while zap.ajaxSpider.status == 'running':
    time.sleep(3)

# Active Scan
print('Starting active scan...')
ascan_id = zap.ascan.scan(target, recurse=True, inscopeonly=True)
while int(zap.ascan.status(ascan_id)) < 100:
    print(f'  Active scan progress: {zap.ascan.status(ascan_id)}%')
    time.sleep(5)

# Get alerts
alerts = zap.core.alerts(baseurl=target, start=0, count=200)
for alert in alerts:
    print(f"[{alert['risk']}] {alert['alert']} @ {alert['url']}")

# Generate report
html_report = zap.core.htmlreport()
with open('zap-report.html', 'w') as f:
    f.write(html_report)
```

### Key API Endpoints (curl)
```bash
BASE="http://localhost:8080"
KEY="changeme"

# Spider
curl "$BASE/JSON/spider/action/scan/?apikey=$KEY&url=https://target.com"
curl "$BASE/JSON/spider/view/status/?apikey=$KEY&scanId=0"

# Active scan
curl "$BASE/JSON/ascan/action/scan/?apikey=$KEY&url=https://target.com&recurse=true"
curl "$BASE/JSON/ascan/view/status/?apikey=$KEY&scanId=0"

# Get alerts
curl "$BASE/JSON/core/view/alerts/?apikey=$KEY&baseurl=https://target.com"

# HTML report
curl "$BASE/OTHER/core/other/htmlreport/?apikey=$KEY" -o report.html

# Shutdown ZAP
curl "$BASE/JSON/core/action/shutdown/?apikey=$KEY"
```

## Authentication Handling

### Form-Based Authentication
1. In GUI: Sites panel → right-click context → Properties
2. Authentication → Form-Based Authentication
3. Set Login URL, Username Field, Password Field
4. Set Logged-in/Logged-out indicators (regex on response body)
5. Add user: Context → Users → Add

### Script-Based Authentication (for complex flows — OAuth, MFA bypass, custom tokens)
```javascript
// Zest script: Authentication.zst
// Or JavaScript via BSH/GraalVM engine
function authenticate(helper, paramsValues, credentials) {
    var req = helper.prepareMessage();
    req.setRequestHeader("Content-Type", "application/json");
    req.setRequestBody(JSON.stringify({
        username: credentials.getParam("Username"),
        password: credentials.getParam("Password")
    }));
    helper.sendAndReceive(req);
    return req;
}
function getRequiredParamsNames() { return ["Username", "Password"]; }
function getOptionalParamsNames() { return []; }
function getCredentialsParamsNames() { return ["Username", "Password"]; }
```

### JWT / Token Injection via Replacer
- Tools → Options → Replacer → Add Rule
- Match Type: Request Header, Match String: `Authorization:`
- Replacement: `Authorization: Bearer <your-jwt>`
- Applies to all proxied requests automatically

### Session Management
- Context → Session Management → HTTP Session Management (cookie-based)
- Or use Cookie-Based with `Replacer` to inject session cookies
- For SPAs: Script-Based Session Management

## Scan Policies

Scan policies control which active scan rules run and at what strength/threshold.
```
GUI: Analyze → Scan Policy Manager → Add

Key settings per rule:
  Threshold: OFF | DEFAULT | LOW | MEDIUM | HIGH
  Strength:  DEFAULT | LOW | MEDIUM | HIGH | INSANE
```

Common policy tuning:
- Disable noisy rules: SQL Injection (time-based), Path Traversal for high false-positive environments
- Enable rule 90034 (Cloud Metadata Exposure) for cloud targets
- Set strength=INSANE only for dedicated lab environments (very slow)

## HUD (Heads Up Display)

ZAP's HUD overlays security data directly in the browser.
```bash
# Enable HUD via CLI
zap.sh -daemon -port 8080 -config hud.enabled=true
# Or via GUI: Tools → Options → HUD → Enable HUD when using ZAP's browser
```
HUD shows alerts inline per page element, allows toggling active scanning from the browser.

## Scripting

### Zest Scripts (GUI-native recording format)
- Record via ZAP GUI: Scripts → Zest Script → Record
- Edit conditionals, assertions, and transformations
- Run as authentication script, active scan rule, or standalone

### JavaScript Active Scan Rules
```javascript
// Custom active scan rule — check for debug header exposure
function scan(as, msg, param, value) {
    var newMsg = msg.cloneRequest();
    newMsg.getRequestHeader().setHeader("X-Debug", "true");
    as.sendAndReceive(newMsg);
    if (newMsg.getResponseBody().toString().contains("DEBUG_MODE")) {
        as.raiseAlert(2, 1, "Debug Mode Enabled", "...", param, value, "", "", "", newMsg);
    }
}
```

## CI/CD Integration

### GitHub Actions
```yaml
name: ZAP Baseline Scan
on: [push]
jobs:
  zap_scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.12.0
        with:
          target: 'https://staging.example.com'
          rules_file_name: '.zap/rules.tsv'
          cmd_options: '-a'

      - name: ZAP Full Scan
        uses: zaproxy/action-full-scan@v0.10.0
        with:
          target: 'https://staging.example.com'

      - name: ZAP API Scan
        uses: zaproxy/action-api-scan@v0.7.0
        with:
          target: 'https://api.example.com/openapi.json'
          format: openapi
```

### Automation Framework (YAML-based, advanced control)
```yaml
# zap.yaml
env:
  contexts:
    - name: "Target Context"
      urls: ["https://target.example.com"]
      includePaths: ["https://target.example.com.*"]
      authentication:
        method: "form"
        parameters:
          loginPageUrl: "https://target.example.com/login"
          loginRequestData: "username={%username%}&password={%password%}"
        verification:
          method: "response"
          loggedInRegex: "\\QLogout\\E"
      users:
        - name: "test-user"
          credentials:
            username: "testuser"
            password: "testpass"
jobs:
  - type: spider
    parameters:
      context: "Target Context"
      user: "test-user"
      maxDuration: 2
  - type: activeScan
    parameters:
      context: "Target Context"
      user: "test-user"
  - type: report
    parameters:
      template: "traditional-html"
      reportFile: "/zap/wrk/report.html"
```
```bash
docker run -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable \
  zap.sh -cmd -autorun /zap/wrk/zap.yaml
```

## Marketplace Add-ons

Install via GUI: Help → Check for Updates, or Tools → Marketplace.

| Add-on | Purpose |
|---|---|
| Ajax Spider | JS-heavy app crawling via browser |
| Active Scan Rules (Alpha/Beta) | Additional experimental checks |
| GraphQL Support | Import and scan GraphQL schemas |
| OpenAPI Support | Import Swagger/OAS specs |
| Retire.js | Detect vulnerable JS libraries |
| Token Generator | Fuzzing with generated tokens |
| Wappalyzer | Technology fingerprinting |
| FuzzDB Files | Extended fuzzing wordlists |

## ZAP vs Burp Suite

| Feature | ZAP | Burp Suite |
|---|---|---|
| Cost | Free, open source | Community free; Pro ~$449/yr |
| CI/CD automation | Native Docker scripts, GitHub Actions | Enterprise only; unofficial scripts |
| REST API | Full REST API built-in | REST API in Pro+ |
| Ajax Spider | Built-in | Built-in (Crawler) |
| Extensibility | Java/Zest/JS/Python scripts | BApp Store (Java/Python extensions) |
| Active scan coverage | Good | Excellent (more rules) |
| Manual testing UX | Functional | Superior (Repeater, Collaborator, etc.) |
| Authenticated scanning | Supported (complex config) | Simpler session handling |
| Best for | CI/CD, OSS, API scanning | Manual testing, enterprise |

## Troubleshooting

**HTTPS interception fails / SSL errors**
→ Import ZAP CA cert into browser trust store. Export: `curl "http://localhost:8080/OTHER/core/other/rootcert/?apikey=KEY" -o zap.cer`

**Spider misses most pages (SPA)**
→ Enable Ajax Spider. Set browser to Firefox/Chrome in Ajax Spider options. Increase max duration.

**Active scan too slow**
→ Reduce thread count, narrow scope to specific URL tree, use a targeted scan policy disabling time-based SQLi rules.

**API returns 403 Forbidden**
→ API key mismatch. Verify `-config api.key=<key>` matches what you pass as `apikey=` parameter. Check `api.addrs` config if not on localhost.

**ZAP daemon crashes on startup**
→ Java version issue. ZAP requires Java 11+. Check: `java -version`. Use `JAVA_HOME` to point to correct JDK.

**False positives in CI/CD**
→ Create a `.zap/rules.tsv` file to set specific rules to IGNORE:
```tsv
10021	IGNORE	(X-Content-Type-Options)
10027	IGNORE	(Info Disclosure)
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [Why Your Penetration Test Report Is Useless (And What to Ask For Instead)](https://redhound.us/pentest-report)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
