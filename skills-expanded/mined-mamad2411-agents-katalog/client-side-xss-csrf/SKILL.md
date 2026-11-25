---
name: client-side-xss-csrf
description: Client-side vulnerabilities — reflected/stored/DOM XSS, CSRF, and open redirect — with unique-marker confirmation, context-aware payloads, and dalfox/xsstrike delegation. Use when parameters are reflected into HTML/JS, when state-changing actions lack anti-CSRF tokens, or when redirect destinations come from input. OWASP A03/A01, WSTG-CLNT, CWE-79/352/601.
---

# XSS / CSRF / Open Redirect

`dr(){ docker run --rm detech/toolbox:latest "$@"; }`

## Cross-Site Scripting (XSS)
**Detect with a unique marker** so reflection is unambiguous and baseline-diffable:
- Inject `dtxr8z"><svg/onload=alert(1)>` and `dtxr8z'><img src=x onerror=alert(1)>`.
- **Confirm reflected:** the raw payload appears **unencoded** in an `text/html` response **and
  is absent from a benign baseline**. (Reflection unencoded = strong; execution needs a browser.)
- **Context matters** — tailor the break-out:
  | Context | Payload shape |
  |---|---|
  | HTML body | `"><svg onload=alert(1)>` |
  | Attribute | `" autofocus onfocus=alert(1) x="` |
  | JS string | `';alert(1);//` , `</script><svg onload=alert(1)>` |
  | URL/href | `javascript:alert(1)` |
  | JSON reflected to HTML | break out of the script/JSON context |
- **Stored XSS:** submit into persistent fields (profile, comment, filename, review), then load
  the page that renders it. **DOM XSS:** trace sources (`location`, `document.URL`,
  `postMessage`) → sinks (`innerHTML`, `eval`, `document.write`, `setAttribute`) in the JS.
- **WAF/ filter bypass:** case, encoding, `<svg>`, event handlers, `<iframe srcdoc>`, template
  literals, HTML-entity/JS-escape tricks (see `waf-detection-bypass`).
- **Impact PoC:** steal a cookie/token to your OOB listener, or perform an action as the victim
  — enough to prove impact, nothing destructive.
```bash
dr dalfox url "$U/search?q=FUZZ" --silence --format json     # after manual reflection signal
dr xsstrike -u "$U/search?q=test"
```

## CSRF
- Find state-changing actions (password/email change, transfer, role change, delete).
- Missing/weak protection: no anti-CSRF token, token not validated, token not tied to session,
  predictable token, `SameSite` not set, action accepts `GET`, or CORS is over-permissive.
- **PoC:** craft an auto-submitting form/`fetch` from an attacker origin; if it succeeds using
  the victim's cookies → CSRF. Also test **JSON CSRF** (`text/plain` content-type trick) and
  **method override**.

## Open Redirect
- Sinks: `redirect,url,next,return,returnUrl,dest,to,continue,r`.
- Payloads: `https://evil.example/`, `//evil.example`, `/\evil.example`, `https:evil.example`,
  `//evil.example/%2f..`, whitelist bypass `https://trusted.evil.example`, `@`-tricks.
- **Confirm:** response is a `30x` whose `Location` points off-site to your domain (do NOT
  follow redirects when testing). Chain into OAuth token theft / phishing / SSRF filter bypass.

## Confirmation discipline
- XSS: unique marker reflected unencoded, absent from baseline (or a real DOM sink hit).
- Open redirect: `Location` header off-site — header-based, not body text.
- CSRF: the action actually executes cross-origin with the victim's session.

## Analysis & recording
Record marker/payload, context, exact request+response (show the reflected/`Location`/executed
action), CWE (79 XSS / 352 CSRF / 601 redirect), OWASP **A03**/**A01**, CVSS, impact (session
theft, account actions, phishing), remediation (context-aware output encoding + CSP for XSS;
anti-CSRF tokens + `SameSite` for CSRF; allow-list redirects). Pass `validation-gates`.
