---
name: download-attribute-security
description: >
  Assess and harden HTML download attribute usage, Content-Disposition filenames,
  content-type sniffing on file responses, and XSS or path risks via user-facing downloads.
  Use when reviewing <a download>, attachment/inline disposition, filename injection,
  user-content CDN/download endpoints, or sandboxing served files under authorized
  application security work.
---

# Download Attribute Security

## Scope And Authorization

- **In scope:** Web apps and file-delivery endpoints you own or may test under authorization.
- **Out of scope:** Using download tricks to malware-distribute; unauthorized testing.
- Prefer safe content types and `Content-Disposition: attachment` for untrusted files.
- Redact signed URL tokens in reports.
- Pair with `xss-cross-site-scripting`, `path-traversal-lfi`, storage skills, and `code-quality-standards`.

## When To Use

- Implementing user file download/export features.
- Reviewing `<a download="filename">` with cross-origin or user-controlled names.
- Hardening `Content-Disposition` filename parameters against injection.
- Preventing HTML/JS uploaded files from executing as active content when opened.
- Safari/Chrome differences for `download` attribute and CORS.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Stored XSS general | `xss-cross-site-scripting` |
| Path traversal on read | `path-traversal-lfi` |
| Desktop autoupdate packages | `desktop-autoupdate-security` |
| CSP/headers broadly | security header skills |
| Code quality baseline | `code-quality-standards` |

## Surfaces

| Surface | Risk |
| --- | --- |
| `<a download>` | Filename hint; cross-origin limits; may ignore without CORS |
| `Content-Disposition: attachment; filename=` | Header injection / unexpected names |
| `filename*` (RFC 5987) | Encoding issues |
| `Content-Type` | Sniffing → XSS if `text/html` inline |
| User uploads served same-site | Active content execution |
| Signed URLs | Token leakage via referrers |

## Workflow

### 1. Confirm scope and success criteria

1. File types allowed, storage, CDN, download UX.
2. Success: untrusted files download as attachments with safe types; filenames sanitized; no header injection; XSS via file open mitigated.
3. Browser matrix for critical UX.

### 2. Inventory download paths

```bash
rg -n "Content-Disposition|download=|File\\(|SendFile|attachment" -g '*.{cs,js,ts,py,go,java,html}'
```

1. Map user-controlled filename inputs.
2. Note whether files served from app origin or cookie-less cookie domain/CDN.

### 3. Harden response headers

```http
Content-Type: application/pdf
Content-Disposition: attachment; filename="report.pdf"; filename*=UTF-8''report.pdf
X-Content-Type-Options: nosniff
```

1. Prefer **attachment** over **inline** for untrusted content.
2. Force safe MIME for uploads (do not trust client Content-Type alone).
3. `X-Content-Type-Options: nosniff` to reduce sniffing.
4. Consider separate file domain without session cookies.

### 4. Filename sanitization

```python
import re
def safe_filename(name: str) -> str:
    name = name.replace("\\", "_").replace("/", "_").replace("\"", "")
    name = re.sub(r"[\r\n]", "", name)
    name = name[:128] or "download"
    return name
```

1. Strip CR/LF to prevent header injection.
2. Do not pass raw user strings into header formatting without encoding.
3. HTML `download` attribute value: similarly sanitize; do not put paths.

### 5. HTML `download` attribute notes

```html
<a href="/files/123" download="report.pdf">Download</a>
```

1. Same-origin: browser may honor filename.
2. Cross-origin: often requires CORS and may ignore `download`—do not rely for security.
3. Security must be enforced by **server headers**, not only the attribute.

### 6. Active content and XSS

1. Block serving user HTML/JS/SVG as `text/html` or image/svg+xml inline on cookie origin.
2. Re-encode or sandbox previews.
3. For SVG/HTML previews use strict CSP + sandbox iframe.
4. Malware scanning for uploads when threat model requires.

### 7. Verify and hand off

```bash
curl -sI 'https://app.example/files/123' | rg -i 'content-type|content-disposition|nosniff'
# Try filename with quotes/newlines in staging — must not split headers
```

1. Manual: download path executes as file not app page.
2. Document CDN cache rules for Content-Disposition.
3. Apply `code-quality-standards` to download handlers.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Disposition | attachment + safe type | inline HTML upload |
| Filename | Sanitized, no CR/LF | Raw user string in header |
| Origin | Cookie-less file host | Session cookies on UGC domain |
| Attribute | UX only | Trusted as security boundary |
| Sniff | nosniff | Guess text/html |
| Tokens | Short-lived signed URL | Token in Referer to third party |

## Output Checklist

- [ ] Download endpoints inventoried
- [ ] Content-Type and Disposition hardened
- [ ] Filenames sanitized (header + attribute)
- [ ] nosniff set
- [ ] Untrusted active content not inline on session origin
- [ ] Header injection tests pass
- [ ] CORS/download attribute behavior documented
- [ ] Signed URL leakage considered
- [ ] CDN behavior verified
- [ ] Residual risk noted

## Rules

- Server headers enforce download safety; `download` attribute is UX.
- Never trust user filename or content-type raw.
- Separate origins for UGC when practical.
- Authorized testing only.
- Focus on download/disposition/filename security.
