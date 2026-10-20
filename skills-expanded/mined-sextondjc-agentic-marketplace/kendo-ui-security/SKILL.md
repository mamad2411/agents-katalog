---
name: kendo-ui-security
description: Use when reviewing Kendo UI implementations for XSS vulnerabilities in templates, CSRF exposure in DataSource transport, insecure Upload configurations, and known CVEs in Progress/Kendo dependencies.
---

# Kendo UI Security

## Specialization

Identify and remediate Kendo UI-specific security vulnerabilities covering XSS via template injection (`#= #` vs `#: #`), unsafe DataSource transport patterns, CSRF token absence in AJAX requests, insecure Upload handler configuration, Content Security Policy conflicts with inline Kendo UI scripts, and known CVEs in Kendo UI and its dependency chain — grounded in OWASP and official Kendo UI documentation.

## Trigger Conditions

- Reviewing code that passes user-controlled or server-supplied data to `#= #` (raw-output) template expressions.
- Auditing `kendo.template()` usage with dynamic HTML strings.
- Reviewing DataSource transport AJAX calls for CSRF token injection.
- Auditing Kendo UI Upload server handler for unrestricted file type acceptance.
- Assessing Kendo UI Editor (rich text) content sanitization before persistence.
- Evaluating CSP headers for compatibility with Kendo UI inline script patterns.
- Reviewing a Kendo UI version for known CVEs.
- A `kendo-ui-quality-gate` audit identifies a security finding.

## Scope Boundaries

In scope:

- XSS via Kendo UI template raw output (`#= data.field #`) with untrusted content.
- `kendo.template()` constructor injection via dynamic template strings.
- CSRF exposure in DataSource `transport.create`, `update`, `destroy` operations.
- Kendo UI Upload: file type whitelist enforcement, server-side validation obligations.
- Kendo UI Editor: output sanitization before storage and re-display.
- CSP compatibility: `unsafe-eval` requirement for `kendo.template()`, mitigation paths.
- Known CVEs: Kendo UI jQuery dependency CVEs (CVE-2019-11358, CVE-2020-11022/11023) and upstream npm package advisories.
- SSRF risk from DataSource URLs constructed from user input.

Out of scope:

- Server-side security controls for API endpoints.
- Authentication and session management.
- Network transport security beyond AJAX header configuration.
- Non-Kendo UI JavaScript security (use `jquery-security` or `web-frontend` skills).

## Inputs

- Code under review (file paths or snippets).
- Kendo UI version in use.
- DataSource endpoint trust model: server-controlled vs. user-supplied content.
- CSP policy in use (if defined).
- Upload handler server technology and configuration.

## Required Outputs

- XSS risk inventory: each template using `#= #` with untrusted content, classified by risk level.
- Remediation for each sink: switch to `#: #` (encoding), DOMPurify integration, or structured DOM construction.
- CSRF token strategy for all non-idempotent DataSource transport operations.
- Upload security checklist: MIME type validation, file extension whitelist, max size enforcement.
- Editor sanitization recommendation: server-side HTML sanitizer before storage.
- CSP compatibility finding: `unsafe-eval` requirement assessment and mitigation path.
- Kendo UI CVE assessment for the version in use.

## Vulnerability Catalog

### 1. XSS via Template Raw Output

Kendo UI templates use two output syntaxes:

| Syntax | Behavior | Use When |
|---|---|---|
| `#: data.field #` | HTML-encodes output | **Default for all user-supplied or server-supplied string content** |
| `#= data.field #` | Renders raw HTML — **XSS sink** | Only for trusted, application-controlled HTML fragments |

```javascript
// UNSAFE — user-controlled content rendered as raw HTML
var tmpl = kendo.template("<td>#= data.userInput #</td>");

// SAFE — HTML-encoded output
var tmpl = kendo.template("<td>#: data.userInput #</td>");

// SAFE — when HTML is required, sanitize first
var tmpl = kendo.template("<td>#= kendo.htmlEncode(data.userInput) #</td>");
```

### 2. Dynamic Template String Injection

Never construct template strings from user input:

```javascript
// UNSAFE — attacker controls template logic via field names
var tmpl = kendo.template("<td>#= data." + userField + " #</td>");

// SAFE — field names must come from a trusted, application-defined whitelist
var allowedFields = ["name", "email", "status"];
if (allowedFields.includes(fieldName)) {
    var tmpl = kendo.template("<td>#: data." + fieldName + " #</td>");
}
```

### 3. CSRF in DataSource Transport

```javascript
// SAFE — inject anti-forgery token in all mutating operations
var dataSource = new kendo.data.DataSource({
    transport: {
        create: {
            url: "/api/items",
            method: "POST",
            beforeSend: function(xhr) {
                xhr.setRequestHeader(
                    "X-CSRF-Token",
                    $("meta[name='csrf-token']").attr("content")
                );
            }
        }
        // repeat for update and destroy
    }
});
```

### 4. Upload Security

```javascript
// Client-side extension whitelist (advisory — always enforce server-side)
$("#upload").kendoUpload({
    validation: {
        allowedExtensions: [".pdf", ".docx", ".xlsx"],
        maxFileSize: 5242880 // 5 MB
    },
    // Server-side handler MUST enforce the same constraints independently
});
```

### 5. CSP Compatibility

`kendo.template()` uses `new Function()` internally, which requires `unsafe-eval` in the `script-src` CSP directive. Mitigation options:

- Use pre-compiled templates (Kendo UI template pre-compilation) to avoid runtime `new Function()`.
- Where `unsafe-eval` cannot be permitted, pre-compile all templates at build time.

### 6. Kendo UI CVE Assessment

| CVE | Affected Dependency | Severity | Remediation |
|---|---|---|---|
| CVE-2019-11358 | jQuery ≤ 3.3.1 | Medium | Upgrade jQuery ≥ 3.4.0 |
| CVE-2020-11022 | jQuery < 3.5.0 | Medium | Upgrade jQuery ≥ 3.5.0 |
| CVE-2020-11023 | jQuery < 3.5.0 | Medium | Upgrade jQuery ≥ 3.5.0 |

Run `npm audit` on each project to detect additional upstream advisories beyond this static list.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Classify one template as XSS-safe or unsafe | Template encoding decision documented with rationale |
| L2 Practical | Full template and CSRF audit for one feature area | All `#= #` sinks classified; CSRF tokens injected in mutating transport |
| L3 Hardening | Upload, Editor, and CSP audit complete | Upload whitelist enforced server-side; Editor sanitized; CSP `unsafe-eval` assessed |
| L4 Expert | Full CVE assessment + pre-compiled template pipeline | CVE inventory complete; pre-compilation eliminates `unsafe-eval` requirement |
