---
name: frontend-security
description: Hardens browser code against XSS, token theft, CSRF, clickjacking and supply-chain attacks (safe DOM sinks, sanitization, strict CSP, Trusted Types, token storage, SRI, postMessage checks). Use when writing or reviewing frontend code that renders user content, handles auth tokens or cookies, adds third-party scripts, sets security headers or CSP, or uses innerHTML, dangerouslySetInnerHTML, v-html or bypassSecurityTrust. Not for server-side injection or authz checks (use security-audit).
license: MIT
---

# Frontend Security

Assume every string that reaches the DOM can contain an attacker's payload, and that anything shipped to the browser is public. Defend in layers: safe rendering first, sanitization where HTML is unavoidable, then a strict CSP to contain what slips through.

## When to use

- Rendering user-generated or third-party content (comments, markdown, rich text, URLs).
- Deciding where to store access or refresh tokens in a single-page app.
- Adding a Content Security Policy or other security headers.
- Adding third-party scripts (analytics, chat widgets, tag managers).
- Using `postMessage`, iframes, redirects after login, or `window.open`.

Not for: server-side injection, authorization checks and secrets management (see the **security-audit** skill); OAuth/OIDC flows (see **auth-implementation**).

## Workflow

1. **Find the sinks.** Search the codebase for the dangerous APIs in the table below. Each hit needs a reason it is safe or a fix.
2. **Trace the data** reaching each sink. If any part comes from a user, URL, storage, API response or `postMessage`, treat it as untrusted.
3. **Prefer safe rendering.** Use text bindings (`{value}`, `{{ value }}`, `textContent`) so the framework escapes output. Only fall back to HTML insertion when the feature truly needs markup.
4. **Sanitize unavoidable HTML** with a vetted library (for example DOMPurify) right before insertion, on the client, with a restrictive allowlist. Never write your own regex sanitizer.
5. **Validate URLs** before putting them in `href`, `src`, `action` or `location`: parse with `new URL()` and allow only `http:`, `https:` (and `mailto:` if needed). This blocks `javascript:` URLs.
6. **Contain with CSP.** Roll out a nonce- or hash-based policy in report-only mode first. Read [references/csp-rollout.md](references/csp-rollout.md) when adding or tightening a CSP.
7. **Check tokens, cookies and CSRF** using the tables below.
8. **Review third parties and the bundle** (SRI, public env vars, source maps, dependencies).
9. Before changing production headers or CSP enforcement, show the user the exact header and get confirmation: a wrong policy can break the whole site.

## Dangerous sinks

| Framework | Sink | Safe alternative |
| --- | --- | --- |
| DOM | `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write` | `textContent`, `createElement` + `append` |
| DOM | `eval`, `new Function`, `setTimeout("string")` | Pass functions, never strings |
| React | `dangerouslySetInnerHTML`; `href={userUrl}` | Render as children; validate URL scheme |
| Vue | `v-html`; `:href="userUrl"` | `{{ }}` interpolation; validate URL scheme |
| Angular | `bypassSecurityTrustHtml` / `Url` / `ResourceUrl` / `Script` / `Style` | Let Angular's built-in sanitizer handle `[innerHTML]`; don't bypass |
| Svelte | `{@html ...}` | Normal `{value}` bindings |
| jQuery | `.html()`, `$(userString)` | `.text()` |

Also check:

- **Server-rendered JSON in `<script>` tags.** A value containing `</script>` breaks out. Serialize with a library that escapes `<` (as `\u003c`), not plain string interpolation.
- **Markdown renderers.** Turn off raw HTML in the renderer or sanitize its output.
- **User-uploaded SVG.** It can carry script. Don't render it inline on your origin (see **file-storage-uploads**).

## Where to keep tokens

| Option | XSS can steal it? | Notes |
| --- | --- | --- |
| `localStorage` / `sessionStorage` | **Yes**, any script on the page can read it | Avoid for access or refresh tokens |
| JS memory only | Harder (lost on reload) | OK for short-lived access tokens; refresh through an HttpOnly cookie |
| `HttpOnly; Secure; SameSite` cookie | No (script can't read it) | Needs CSRF protection |
| Backend-for-frontend (BFF) | No: tokens stay on the server | Recommended for SPAs handling sensitive data |

An XSS bug can still *use* a cookie session by making requests from the page. HttpOnly limits theft, not abuse, so preventing XSS still comes first.

## Cookies and CSRF

- Set session cookies as `HttpOnly; Secure; SameSite=Lax` (or `Strict`) with `Path=/`. Prefer the `__Host-` name prefix, which requires `Secure`, `Path=/` and no `Domain`.
- `SameSite` stops cross-*site* requests, but sibling subdomains count as the same site. If any subdomain can host untrusted content, also use CSRF tokens.
- For state-changing requests with cookie auth, use one of: a synchronizer token, a double-submit token, or a required custom header (which forces a CORS preflight). Also check the `Origin` header on the server.
- Never perform state changes on `GET`.

## Other browser attack surfaces

| Risk | Control |
| --- | --- |
| Clickjacking | `Content-Security-Policy: frame-ancestors 'none'` (or `'self'`); `X-Frame-Options: DENY` for old browsers |
| `postMessage` | Receiver checks `event.origin` against an exact allowlist and validates the message shape; sender passes an explicit `targetOrigin`, never `"*"` with sensitive data |
| Open redirect (`?next=`) | Allow only relative paths: resolve with `new URL(next, location.origin)` and require the same origin; reject `//host` and `/\host` |
| `window.open` to untrusted URLs | Pass `noopener` (third argument) so the new page can't control yours |
| Third-party scripts | Each one runs with full page access. Load only what you need; use Subresource Integrity (`integrity="sha384-..." crossorigin="anonymous"`) for fixed-version files on CDNs |
| Prototype pollution | Don't deep-merge untrusted JSON into objects; use `Object.create(null)` or `Map` for user-keyed data |

## Trusted Types

`Content-Security-Policy: require-trusted-types-for 'script'` makes the browser reject raw strings at DOM XSS sinks. Code must pass objects created by a named policy (for example a policy that calls DOMPurify). It is Baseline since early 2026 (Chromium, Firefox and Safari); older browsers ignore it, so check your support matrix. Roll it out in report-only mode like the rest of the CSP.

## The bundle is public

- Anything in client code is readable: API keys, feature flags, internal URLs, comments.
- Only variables with the framework's public prefix reach the browser (`NEXT_PUBLIC_`, `VITE_`, `PUBLIC_` in SvelteKit and Astro, `REACT_APP_` in Create React App). Never put a secret behind one of those prefixes.
- Don't serve source maps publicly in production unless you have decided the source is public. Upload them privately to your error tracker instead.
- Client-side checks (hidden buttons, route guards) are UX, not security. The server must enforce every permission.

## Dependency supply chain

- Commit the lockfile and install with `npm ci` (or `pnpm install --frozen-lockfile`, `yarn install --immutable`) in CI.
- Run the ecosystem's audit in CI and review new dependencies before adding them: maintainers, download history, install scripts, and name typos.
- Consider `--ignore-scripts` for installs where packages don't need lifecycle scripts.
- See the **dependency-upgrades** skill for upgrade workflow.

## Anti-patterns

- **"We sanitize on the server, so innerHTML is fine."** Server sanitization is tied to one output context. Sanitize at the sink, for that context.
- **Regex or blocklist sanitizers.** Browsers parse HTML in surprising ways. Use a maintained library.
- **CSP with `'unsafe-inline'` and `'unsafe-eval'` in `script-src`.** It gives almost no XSS protection.
- **Allowlisting whole CDNs in `script-src`.** Public CDNs host scripts that can be abused to bypass the policy. Use nonces with `'strict-dynamic'` instead.
- **Tokens in `localStorage` "because cookies are hard".**
- **Hiding admin features in the UI without server checks.**

## Done when

- Every dangerous sink found has either been replaced or has sanitization and a comment explaining why it is safe.
- URLs from untrusted sources are scheme-validated before use.
- Tokens are not in web storage; cookie sessions have CSRF protection.
- A CSP is at least running in report-only mode with reports being collected, and `frame-ancestors` is set.
- No secrets in client bundles; source maps are not public unless intended.

## References

- [references/csp-rollout.md](references/csp-rollout.md): read when adding, tightening or debugging a Content Security Policy.
