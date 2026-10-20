---
name: jquery-security
description: Use when reviewing jQuery code for XSS vulnerabilities, unsafe HTML injection, insecure AJAX patterns, CSRF exposure, and Content Security Policy compliance.
---

# jQuery Security

## Specialization

Identify and remediate jQuery-specific security vulnerabilities covering XSS via `.html()`, `$.parseHTML()`, and `$(htmlString)` constructor injection; CSRF in AJAX requests; insecure JSONP usage; and CSP violations from jQuery's inline event model — grounded in OWASP and official jQuery security guidance.

## Trigger Conditions

- Reviewing code that passes user-controlled or server-supplied data to `.html()`, `.append()`, `.prepend()`, `.before()`, `.after()`, `.replaceWith()`, or `.wrap()`.
- Auditing `$()` constructor calls with dynamic HTML strings.
- Reviewing `$.parseHTML()` usage.
- Auditing AJAX calls for CSRF token handling.
- Reviewing JSONP usage for cross-origin data.
- Assessing jQuery version for known CVEs.
- Reviewing inline event handlers (`onclick="..."`) in jQuery-generated HTML for CSP compliance.
- A `jquery-quality-gate` audit identifies a security finding.

## Scope Boundaries

In scope:

- XSS via jQuery DOM manipulation methods with dynamic content.
- `$('<tag>', props)` constructor injection.
- `$.parseHTML()` context and `keepScripts` parameter risks.
- CSRF exposure in `$.ajax()` calls.
- JSONP security and deprecation.
- Known jQuery CVEs and version-specific vulnerabilities.
- CSP compatibility of jQuery patterns.

Out of scope:

- Server-side security controls.
- Authentication and session management.
- Network transport security beyond AJAX header configuration.

## Inputs

- Code under review (file paths or snippets).
- jQuery version in use.
- Endpoint trust model: server-controlled content vs. user-supplied content.
- CSP policy if defined.

## Required Outputs

- XSS risk inventory: each sink consuming dynamic content, with trust classification.
- Remediation for each sink: `.text()` substitution, DOMPurify integration, or structured DOM construction.
- CSRF token strategy for non-idempotent AJAX calls.
- JSONP replacement recommendation if JSONP is found.
- jQuery CVE assessment for the version in use.
- CSP compatibility finding if inline event handlers are generated.

## Vulnerability Catalog

### 1. XSS via .html() and Related Sinks

**Sinks that execute script content from strings:**

```javascript
// All of these are XSS sinks when content is user-controlled or server-supplied
$(el).html(userInput);
$(el).append('<div>' + userInput + '</div>');
$(el).prepend(userInput);
$(el).after(userInput);
$(el).before(userInput);
$(el).replaceWith(userInput);
$(el).wrap(userInput);
$('<div>' + userInput + '</div>').appendTo(el);
```

**Safe alternatives:**

```javascript
// Use .text() for plain text content — HTML-encodes automatically
$(el).text(userInput);

// Construct DOM structurally — never concatenate user data into HTML strings
$('<div>').addClass('item').text(userInput).appendTo(el);

// If HTML rendering of server content is required — sanitize first
import DOMPurify from 'dompurify';
$(el).html(DOMPurify.sanitize(serverHtml));
```

**Rule:** `.text()` is always safe for text content. `.html()` is only safe when content is a trusted static string or has passed through a sanitizer.

### 2. $() Constructor Injection

```javascript
// Vulnerable: if url comes from user input containing HTML
$(userInput).appendTo('#container');

// $() with a leading '<' interprets the string as HTML
// A value like '<img src=x onerror=alert(1)>' will execute
```

**Remediation:** Validate that the argument to `$()` is a selector string or a native element, not user input. Never pass user-controlled strings to `$()` unless they have been validated as a safe CSS selector.

### 3. $.parseHTML() Risks

```javascript
// Dangerous: keepScripts defaults to false in jQuery 3.x, but script tags
// embedded in attributes (onerror, onload) still execute in older versions
const nodes = $.parseHTML(userInput);
$(el).append(nodes);
```

**Remediation:**

```javascript
// Always sanitize before parsing when content is user-controlled
const clean = DOMPurify.sanitize(userInput);
const nodes = $.parseHTML(clean, document, false);
$(el).append(nodes);
```

In jQuery 3.5+, `$.parseHTML()` no longer executes scripts in the string by default, but attribute-based event handlers can still trigger in older environments. Treat all `$.parseHTML()` calls with dynamic content as requiring sanitization.

### 4. CSRF in AJAX

```javascript
// Missing CSRF protection on state-mutating requests
$.ajax({ url: '/api/delete', method: 'POST', data: { id: 123 } });

// Correct: inject CSRF token in beforeSend
$.ajax({
  url: '/api/delete',
  method: 'POST',
  data: { id: 123 },
  beforeSend: function(xhr) {
    xhr.setRequestHeader('X-CSRF-Token', getCsrfToken());
  }
});

// Or set globally via ajaxSetup for all non-GET requests
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
      xhr.setRequestHeader('X-CSRF-Token', getCsrfToken());
    }
  }
});
```

- Never embed CSRF tokens in query strings — use headers.
- Server must verify the token for all non-idempotent requests.

### 5. JSONP

JSONP executes arbitrary JavaScript returned from a remote server. It is inherently unsafe if the server is untrusted or compromised.

**Remediation:**

- Replace JSONP with CORS-enabled JSON endpoints.
- If JSONP must be retained: restrict to trusted, controlled servers; validate the callback parameter name server-side.
- jQuery 3.x still supports JSONP via `dataType: 'jsonp'` — mark all such usages for replacement.

### 6. Known jQuery CVEs

| CVE | jQuery Versions Affected | Description | Fix |
|---|---|---|---|
| CVE-2019-11358 | < 3.4.0 | Prototype pollution via `$.extend(true, ...)` with `__proto__` key | Upgrade to ≥ 3.4.0 |
| CVE-2020-11022 | < 3.5.0 | XSS via `<script>` in HTML passed to DOM manipulation methods | Upgrade to ≥ 3.5.0 |
| CVE-2020-11023 | < 3.5.0 | XSS via `<option>` element in HTML passed to DOM manipulation methods | Upgrade to ≥ 3.5.0 |

**Rule:** Projects must run jQuery ≥ 3.5.0. Any older version must be escalated as a critical finding.

### 7. CSP Compatibility

jQuery-generated inline handlers (e.g., `.on('click', handler)` which jQuery wires without inline attributes) are CSP-compatible. However:

- Avoid calling `.attr('onclick', fn)` or injecting `onclick="..."` into HTML strings — these violate `script-src 'unsafe-inline'` restrictions.
- Avoid `$.globalEval()` — it executes a string as script, incompatible with strict CSP.
- Avoid `$.getScript()` pointing to untrusted sources — it executes fetched script without integrity checks.

## Security Review Workflow

1. Inventory all jQuery DOM manipulation calls; classify each by content source (static / server-trusted / user-controlled).
2. Flag every user-controlled sink; apply `.text()` or DOMPurify remediation.
3. Audit `$()` constructor calls for non-selector string arguments.
4. Audit all `$.parseHTML()` calls; verify sanitization precedes parsing.
5. Audit all non-GET `$.ajax()` calls for CSRF token injection.
6. Audit all `dataType: 'jsonp'` usages; recommend CORS replacement.
7. Check jQuery version against CVE table; flag if < 3.5.0 as critical.
8. Audit for `$.globalEval()`, `$.getScript()` to untrusted origins, and `.attr('onclick', ...)` patterns.
9. Emit findings with severity (Critical / High / Medium) and explicit remediation steps.

## Severity Classification

| Finding | Severity |
|---|---|
| jQuery version with known CVE | Critical |
| `.html(userInput)` without sanitizer | Critical |
| `$(userInput)` constructor with dynamic HTML | Critical |
| CSRF missing on POST/PUT/DELETE | High |
| JSONP to untrusted host | High |
| `$.parseHTML(userInput)` without sanitization | High |
| `$.globalEval()` usage | High |
| `.attr('onclick', ...)` in CSP-restricted environment | Medium |

## Done Criteria

- No unsanitized user input reaches a jQuery HTML sink.
- All non-GET AJAX calls inject a CSRF token.
- jQuery version is ≥ 3.5.0.
- No JSONP to untrusted origins.
- `$.globalEval()` is absent.
- Every finding has a severity and explicit remediation.

## References

- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [OWASP CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
- [jQuery Security Advisories](https://blog.jquery.com/tag/security/)
- [CVE-2020-11022](https://nvd.nist.gov/vuln/detail/CVE-2020-11022)
- [CVE-2020-11023](https://nvd.nist.gov/vuln/detail/CVE-2020-11023)
- [CVE-2019-11358](https://nvd.nist.gov/vuln/detail/CVE-2019-11358)
- [DOMPurify](https://github.com/cure53/DOMPurify)
- [jQuery API: .html()](https://api.jquery.com/html/)
- [jQuery API: $.parseHTML()](https://api.jquery.com/jquery.parsehtml/)
- [MDN: Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
