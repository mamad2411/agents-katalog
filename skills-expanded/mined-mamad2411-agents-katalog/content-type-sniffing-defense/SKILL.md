---
name: content-type-sniffing-defense
description: >
  Defend against MIME / content-type sniffing: enforce X-Content-Type-Options: nosniff,
  accurate Content-Type, safe user-upload serve paths, and polyglot body risks that
  browsers re-interpret as HTML/script. Use when hardening user content, static hosts,
  CDN origins, missing nosniff, wrong MIME on uploads, or MIME-confusion XSS on owned
  apps and authorized assessments.
---

# Content-Type Sniffing Defense

## Scope And Authorization

- **In scope:** owned apps, CDNs, object storage frontends; authorized header audits.
- **Out of scope:** uploading polyglots to third-party services without authorization.
- Prefer staging when changing MIME maps for large static corpora.
- Pair with CSP (`content-security-policy-design`) and upload validation practices.

## When To Use

- User-generated content is served from the same site or sibling CDN.
- Missing `X-Content-Type-Options: nosniff`.
- Downloads/previews with wrong or generic `Content-Type`.
- Tokens: nosniff, MIME sniffing, content-type, polyglot upload, MIME confusion.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full XSS methodology | `xss-cross-site-scripting` |
| CSP design | `content-security-policy-design` |
| R2/S3 public access | cloud storage skills |
| Cookie flags | `cookie-security-flags` |

## Threat Model

| Issue | Risk |
| --- | --- |
| Browser sniffs body as HTML | XSS on “image”/“text” upload |
| `text/plain` without nosniff | Historical XSS via sniff |
| Served as `application/octet-stream` inconsistently | UX vs safety trade-offs |
| Same-origin user content | Cookie-bearing XSS context |
| SVG as image | Scriptable SVG if served inline |

## Workflow

### 1. Confirm scope and success

1. Upload/serve paths, CDN behaviors, same-site vs separate domain for UGC.
2. Success: all relevant responses send `nosniff` + correct type; UGC cannot execute as script in app origin.
3. Prefer **separate cookie-less domain** for UGC when possible.

### 2. Inventory headers

```bash
curl -sI https://app.example.com/ | rg -i "content-type|x-content-type-options"
curl -sI https://cdn.example.com/user/abc.png | rg -i "content-type|x-content-type-options|content-disposition"
```

1. Map frameworks/static servers that might omit nosniff.
2. List upload allowed extensions and how MIME is chosen (client-claimed vs magic bytes).

### 3. Apply defenses

**Global header:**

```http
X-Content-Type-Options: nosniff
Content-Type: <authoritative type>
```

**nginx:**

```nginx
add_header X-Content-Type-Options "nosniff" always;
```

**UGC practices:**

| Control | Practice |
| --- | --- |
| Type | Detect from magic bytes; ignore client `Content-Type` alone |
| Disposition | `Content-Disposition: attachment` for untrusted files when download is enough |
| Domain | Serve UGC from `uploads.example.com` without session cookies |
| CSP | Restrict `script-src` even on UGC domain |
| SVG | Sanitize or serve as download only |
| HTML uploads | Deny or isolate |

### 4. Polyglot awareness

1. Files that are valid image **and** HTML/JS — nosniff + correct image type + no HTML execution context.
2. Never reflect upload filename into HTML without encoding.

### 5. Verify

```bash
# Every UGC URL class:
curl -sI "$URL" | rg -i "x-content-type-options: nosniff|content-type:"
# Browser lab: upload HTML-as-png attempts; ensure not executed as document
```

1. Automated tests assert nosniff on app and upload responses.
2. Check error pages and API JSON also send nosniff (cheap win).

### 6. Operate

1. CDN: ensure edge adds nosniff; origin truth for Content-Type.
2. Monitor XSS reports involving upload URLs.

### 7. Hand off

1. Document UGC domain and MIME allowlist.
2. Pair with CSP rollout for depth.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Header | nosniff everywhere HTML/UGC | Only on homepage |
| MIME | Magic-byte validated | Trust `image/png` from client |
| UGC host | Cookie-less sibling domain | Same origin as session |
| SVG | Sanitized/download | Inline raw SVG from users |
| Evidence | curl matrix | Assumed framework default |

## Output Checklist

- [ ] Response classes inventoried
- [ ] nosniff deployed consistently
- [ ] Content-Type authoritative and correct
- [ ] UGC isolation/disposition strategy set
- [ ] Upload MIME validation hardened
- [ ] Browser/lab verification done
- [ ] CDN/origin parity checked
- [ ] Residual polyglot risks noted

## Rules

- Owned systems only for enforcement.
- Prefer isolate UGC + nosniff + correct types over any single control.
- Evidence via headers and upload tests.
- Complements CSP/XSS skills; does not replace them.
