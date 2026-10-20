---
name: framework-nextjs
description: Next.js security review — validate build-manifest exposure, API route misconfiguration, server-side SSR data leaks, image-proxy SSRF surface, middleware bypass vectors, and ISR/rewrite/redirect hardening with docs-first read-only checks and no SSRF exploitation or admin impersonation.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# Next.js security — configuration and surface review

Use this skill to review Next.js application security posture on authorized in-scope targets. Validate build-manifest and source-map exposure, API route authentication, getServerSideProps SSR data leaks, image-proxy SSRF surface, middleware bypass vectors, `next.config.js` misconfiguration, ISR/rewrite abuse, and CSP header posture. All tests are read-only and low-rate. Never exploit image-proxy SSRF for internal-network access, forge middleware headers for authorization bypass, or deploy payload-based SSR injection — those behaviors are prohibited unless separately approved for destructive validation.

## Required inputs

- Written scope covering the Next.js application hosts, API route paths, `_next/` static paths, image-proxy endpoints, and allowed review methods. Explicit confirmation that SSRF exploitation, middleware-bypass header forging, SSR injection, and admin-route impersonation are prohibited unless separately approved.
- Next.js version from: build manifest `/_next/static/.../_buildManifest.js`, `next.config.js` content (if provided locally), `x-powered-by` header, or framework-specific response signatures.
- Official Next.js documentation for the detected version — prefer nextjs.org/docs.
- Valid authorization cache for the target application.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview.
5. `pentest_agent_execute_tool` for read-only execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — version detection and framework fingerprinting

1. Detect Next.js from response indicators: `__NEXT_DATA__` JSON embedded in page HTML, `/_next/static/` paths for chunk files, `__next` prefixed CSS/JS assets, and `x-powered-by: Next.js` header (if not suppressed). The `__next` build ID in URLs changes with each deployment.
2. Extract the build ID from page source: search for `"buildId":"..."` in the `__NEXT_DATA__` script tag. This build ID is not a version number but can be used to correlate deployments.
3. Identify rendering mode from page behavior: SSR pages include `__NEXT_DATA__` with full page props, SSG pages have `__N_SSG` markers, and ISR pages include `__N_SSG` with cache-control headers. CSR-only pages have minimal `__NEXT_DATA__` and load data client-side.
4. Document version evidence and note any uncertainty. If the application uses an outdated Next.js major version (below 13 for App Router security features, below 12 for middleware), flag immediately.

### Phase 2 — build manifest and source-map exposure

1. Probe for the build manifest: Next.js generates a client-side build manifest that lists all page routes, including those behind authentication. Find the manifest path in the initial page source (look for `/_next/static/` followed by a hash and `_buildManifest.js`). If discoverable, extract the route list.
2. If the build manifest lists admin pages, internal dashboards, or debug routes that are not linked from the public UI, flag as an information-disclosure finding. The route names alone may reveal internal application structure.
3. Check for source-map exposure: probe `/_next/static/chunks/pages/[page]-[hash].js.map` for key pages. Source maps contain original TypeScript/JSX source code with comments, API endpoint constructions, and possibly hardcoded secrets. Exposure is a high finding.
4. Check for `.map` files in robots.txt disallowed paths — attackers ignore robots.txt, so `Disallow` is not a security control. If source maps exist but are disallowed in robots.txt, they are still exposed and accessible.
5. Do not download source maps that may contain secrets. Record exposure, note file paths, and recommend removing `.map` files from production deployments.

### Phase 3 — API route authentication and method confusion

1. Identify API routes from the build manifest, page-source route references, and common Next.js patterns (`/api/*`). Next.js API routes are serverless functions deployed alongside pages.
2. Test API routes without authentication: probe `/api/user`, `/api/admin`, `/api/users`, `/api/config`, `/api/env`, `/api/debug`, and `/api/health` without cookies or authorization headers. Next.js API routes have no built-in authentication — each route handler must implement its own checks.
3. Test method confusion on API routes: send `DELETE /api/users/1`, `PUT /api/config`, or `PATCH /api/settings` without authentication. If the route handler only checks auth on `GET` but not on other HTTP methods, unauthorized mutation is possible.
4. Test for server-side environment variable leakage: Next.js public environment variables (prefixed with `NEXT_PUBLIC_`) are inlined at build time and visible in client-side JavaScript. Check whether sensitive variables lack the prefix and therefore are server-only — probe the page source for JSON objects containing `"NEXT_PUBLIC_"` keys and verify no private keys or secrets are prefixed incorrectly.
5. Do not attempt destructive API calls (DELETE user data, modify configuration, or trigger state changes).

### Phase 4 — getServerSideProps and SSR data leaks

1. Inspect the `__NEXT_DATA__` JSON embedded in SSR page responses. This object contains `props.pageProps` — the data passed from `getServerSideProps` or `getStaticProps`. Verify that no sensitive server-side data (internal IDs, user roles, email addresses, API keys, or database connection details) is serialized into client-visible props.
2. Test whether `getServerSideProps` accepts user-controlled parameters that influence server-side fetch URLs. Submit URL-like values in query parameters (e.g., `?source=`, `?url=`, `?preview=`, `?slug=`) and observe whether the server makes requests to those values. If the server follows user-supplied URLs, an SSRF vector exists in `getServerSideProps`.
3. Test preview mode endpoints: Next.js preview mode (`/api/preview`) allows bypassing SSG and rendering pages on-demand. If exposed without authentication, an attacker can view draft content, trigger expensive SSR renders, or enumerate preview-only pages.
4. Do not attempt to exploit SSR SSRF to access internal services. Record the vector, note the parameter, and stop.

### Phase 5 — image proxy and rewrites SSRF surface

1. Probe the Next.js image optimization endpoint: `/_next/image?url=<URL>&w=128&q=75`. This endpoint fetches and optimizes images from allowed domains defined in `next.config.js` (`images.domains` or `images.remotePatterns`). Test with an external image URL to confirm the proxy is functional.
2. Test for SSRF via the image proxy: submit internal URLs (`http://localhost`, `http://127.0.0.1`, `http://169.254.169.254/latest/meta-data/`, `http://[::1]`) as the `url` parameter. If the `remotePatterns` or `domains` configuration is missing or permits localhost, the image proxy may fetch from internal services.
3. Test for file-protocol access: submit `file:///etc/passwd` as the `url` parameter. If the image optimizer processes `file://` URLs, it can read local files — a critical finding.
4. Check `next.config.js` rewrites and redirects: if the application uses `rewrites()` to proxy API requests, test whether the rewrite target accepts user-controlled path segments. A rewrite like `source: '/api/:path*', destination: 'https://backend/:path*'` is safe, but `destination: 'https://' + process.env.BACKEND + '/:path*'` with user-controlled segments could be manipulated.
5. Do not exploit image-proxy SSRF to enumerate internal networks. Record the vector, note which internal hosts are reachable, and stop.

### Phase 6 — middleware bypass and header manipulation

1. Test middleware-protected routes: Next.js middleware (Edge) runs before request handling and can redirect, rewrite, or add headers. Test protected routes with commonly abused headers: `x-forwarded-host`, `x-forwarded-proto`, `x-forwarded-for`, and `x-middleware-subrequest`.
2. Test path-traversal bypass on middleware: if middleware protects `/admin`, try `/admin/../admin`, `/admin/.`, `/admin%2f`, `/Admin`, or `/ADMIN` (case-sensitivity depends on filesystem).
3. Test trailing-slash bypass: if middleware matches `/admin`, try `/admin/` or vice versa. Next.js middleware `matcher` config may not account for both variants.
4. Test host-header injection: middleware that checks `request.headers.get('host')` can be bypassed if the application also trusts `x-forwarded-host` and a reverse proxy passes it through.
5. Do not attempt to forge middleware subrequest headers (`x-middleware-subrequest`) for full authorization bypass. Record the bypass vector, note the specific header and path, and stop.

## Decision points

- **Escalate on source-map exposure**: `.js.map` files accessible with original source code → high, especially if API keys or internal logic are visible.
- **Escalate on build-manifest route disclosure**: admin/internal route names visible that are not linked publicly → medium as pure information disclosure; high if combined with missing auth on those routes.
- **Escalate on API route missing authentication**: `/api/admin` or `/api/env` accessible without credentials → critical.
- **Escalate on image-proxy SSRF confirmed**: `/_next/image?url=http://169.254.169.254/` returns metadata → critical.
- **Escalate on image-proxy file-protocol access**: `/_next/image?url=file:///etc/passwd` returns file contents → critical.
- **Escalate on getServerSideProps SSRF**: user-controlled URL parameter triggers server-side fetch → high.
- **Escalate on middleware bypass confirmed**: authenticated-only route accessible via header manipulation → high.
- **Escalate on preview-mode exposed without auth**: `/api/preview` allows enabling preview → high.
- **Downgrade on NEXT_PUBLIC_ variable prefix misuse**: informative if the variable is not a secret — but flag any secret-like value.

## Prohibited behavior

- Exploiting image-proxy SSRF for internal network scanning or cloud-metadata extraction.
- Exploiting getServerSideProps SSRF for internal-service access.
- Forging `x-middleware-subrequest` headers for authorization bypass on live production routes.
- Accessing `file://` paths beyond the initial probe to confirm the vector exists.
- Deploying SSRF payloads, RCE attempts, or file-read chains.
- Testing credential endpoints, login forms, or password-reset flows.
- Running directory brute-force or wordlist scans against the application.
- Downloading source maps that contain secrets or proprietary logic.

## Stop conditions

- Image proxy confirms SSRF with internal/cloud-metadata access → stop, critical finding.
- Image proxy confirms file-protocol access → stop, critical finding.
- API route exposes environment variables or sensitive data without authentication → stop, critical finding.
- Source maps contain hardcoded secrets → stop, high finding, recommend secret rotation.
- getServerSideProps SSRF confirmed → stop, high finding, do not exploit further.
- Middleware bypass confirmed on production → stop, high finding.
- Evidence contains secrets or PII → redact immediately and store only minimal proof refs.

## Evidence — Next.js security matrix

For each target, record:

```text
Target: <URL> | Next.js version: <detected | estimated>

Build and source exposure:
  Build manifest exposed: <yes — path | no>
  Source maps exposed: <yes — page paths | no>
  Admin/internal routes disclosed: <yes — route names | none>
  NEXT_PUBLIC_ secrets: <found — variable names | none>

API route security:
  API routes discovered: <count>
  API routes missing auth: <yes — endpoints | all require auth>
  Method confusion possible: <yes — methods | no>

SSR data leaks:
  __NEXT_DATA__ sensitive props: <yes — field types | no>
  getServerSideProps SSRF vector: <yes — parameter | no>
  Preview mode exposed: <yes — /api/preview accessible | no>

Image proxy and rewrites:
  Image proxy SSRF to localhost: <yes — reachable hosts | blocked>
  Image proxy file:// access: <yes | blocked>
  Rewrite destination controllable: <yes — param | no>

Middleware:
  Middleware-protected routes: <list>
  Bypass via x-forwarded-* headers: <yes — header | no>
  Bypass via path manipulation: <yes — technique | no>
  Bypass via host header: <yes | no>

Overall risk: <critical | high | medium | low>
```

Never store: source-map contents, build-manifest JS with embedded secrets, image-proxy responses from internal services, `__NEXT_DATA__` containing PII or credentials, or bypass header values that reveal internal routing.

## Report handoff

1. `pentest_agent_record_finding` for: exposed source maps, build-manifest route disclosure, API routes missing auth, method-confusion vectors, SSR data leaks, getServerSideProps SSRF, image-proxy SSRF, image-proxy file-protocol access, middleware bypass, preview-mode exposure, and NEXT_PUBLIC_ prefix misuse.
2. Reference the Next.js security matrix.
3. Recommend: remove `.map` files from production builds (`productionBrowserSourceMaps: false` in `next.config.js`); authenticate all API routes — avoid relying on client-side checks; review `__NEXT_DATA__` for sensitive props and use server-side redaction before serialization; configure `images.remotePatterns` restrictively with explicit protocol, hostname, and pathname patterns; avoid passing user-controlled values directly into server-side fetch URLs in `getServerSideProps`; protect `/api/preview` with a secret token; test middleware matchers with encoded variants and path-traversal payloads; set `poweredByHeader: false` to remove the `x-powered-by` header; and upgrade to a supported Next.js version.
