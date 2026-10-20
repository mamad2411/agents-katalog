---
name: angular-security-basics
description: >
  Angular client security: template encoding defaults, DomSanitizer, bypassSecurityTrust*
  review, HttpClient XSRF/CSRF, and auth interceptors. Use when reviewing Angular XSS sinks,
  innerHTML bindings, DomSanitizer bypass, HttpClient withCredentials, XSRF-TOKEN, HTTP
  interceptors for Bearer/cookie auth, or hardening org-owned Angular SPAs — authorized only.
---

# Angular Security Basics

## Scope And Authorization

- **In scope:** Angular applications you own or are authorized to assess.
- **Out of scope:** Attacking third-party Angular sites without permission.
- Prefer staging for CSP/XSRF experiments.
- Pair with `code-quality-standards` and `typescript-style-and-eslint`.

## When To Use

- SPA XSS review (templates, `innerHTML`, sanitizer bypass).
- Cookie-session CSRF/XSRF configuration with HttpClient.
- Auth interceptors (Bearer tokens vs cookies).
- Router open-redirect / URL handling review.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Angular Signals migration | `angular-signals-basics` |
| SSR hydration issues | `angular-ssr-hydration` |
| Generic XSS methodology | `xss-cross-site-scripting` |
| API JWT abuse testing | `api-auth-and-jwt-abuse` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Templates | Interpolation encodes HTML; prefer `{{ }}` over binding raw HTML |
| `[innerHTML]` | Sanitized by default; still avoid untrusted HTML |
| `bypassSecurityTrust*` | Audit every call; require code-owner justification |
| DomSanitizer | Do not “sanitize” by bypassing |
| HttpClient XSRF | Cookie `XSRF-TOKEN` + header for mutating cookie auth |
| Interceptors | Attach auth; never log tokens |
| Router | Validate returnUrl allowlist |

## Workflow

### 1. Confirm scope and success criteria

1. Record Angular version, auth mode (JWT in memory vs cookies), API origins.
2. Success: no unjustified bypasses; XSRF correct for cookie auth; interceptors safe; CSP considered.
3. Inventory third-party libs that write HTML.

### 2. Hunt XSS sinks

```bash
rg -n "bypassSecurityTrust|innerHTML|DomSanitizer|document\.write|element\.html" src/
rg -n "\\[innerHTML\\]|\\[href\\]|domSanitizer" src/
```

| Pattern | Risk |
| --- | --- |
| `bypassSecurityTrustHtml(user)` | XSS |
| Resource URL bypass for iframe | Open redirect / script |
| Binding untrusted URL to `script src` | XSS |

```typescript
// Bad
this.html = this.sanitizer.bypassSecurityTrustHtml(this.userProvided);
// Better: plain text, markdown with vetted sanitizer, or server-side safe HTML allowlist
```

### 3. HttpClient CSRF/XSRF (cookie sessions)

```typescript
// AppConfig providers (Angular modern APIs) or HttpClientXsrfModule
// Ensure:
// - Server sets readable XSRF cookie for app origin
// - Mutating requests include X-XSRF-TOKEN (default header name)
// - withCredentials if cross-subdomain cookies needed (careful)
```

1. JWT in `Authorization` header from memory: CSRF less relevant; XSS becomes token theft risk.
2. Do not store long-lived tokens in `localStorage` without XSS defense-in-depth.

### 4. Auth interceptors

```typescript
// Sketch
intercept(req, next) {
  const token = this.auth.getToken();
  const authReq = token
    ? req.clone({ setHeaders: { Authorization: `Bearer ${token}` } })
    : req;
  return next.handle(authReq);
}
```

1. Skip attaching tokens to absolute third-party URLs.
2. Handle 401 refresh without infinite loops.
3. Pair with server authz always.

### 5. Router / redirects

```typescript
// Bad: this.router.navigateByUrl(queryParams.returnUrl)
// Better: allowlist relative paths only
```

### 6. Verify

```bash
ng test
ng build --configuration production
npm audit --omit=dev
# Manual: inject <script> in profile fields; ensure not executed
# Manual: CSRF — cookie session POST without token rejected
```

### 7. Hand off

1. Document remaining bypasses with owners.
2. Prefer Trusted Types / CSP where org supports.
3. Security unit tests for sanitizer helpers.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| HTML | Text binding | Bypass sanitizer for convenience |
| Tokens | Memory + short TTL / BFF cookies | Forever token in localStorage |
| CSRF | XSRF for cookie auth | Cookie auth with no CSRF defense |
| Redirects | Relative allowlist | Open `returnUrl=//evil` |

## Output Checklist

- [ ] Angular version and auth mode recorded
- [ ] bypassSecurityTrust* audited
- [ ] innerHTML usage justified
- [ ] XSRF/cookie or JWT threat model applied
- [ ] Interceptors don’t leak tokens to third parties
- [ ] Router redirects allowlisted
- [ ] Tests/build green; manual XSS/CSRF checks
- [ ] `code-quality-standards` applied

## Rules

- Owned apps only.
- Angular encoding is not a substitute for safe HTML policies.
- Never bypass sanitizer without threat review.
- Server-side authz remains mandatory.
- Redact tokens in logs and error reports.
