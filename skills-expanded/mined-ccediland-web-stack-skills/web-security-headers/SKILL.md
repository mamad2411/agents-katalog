---
name: web-security-headers
description: Set up a hash-based Content Security Policy and the full set of HTTP security headers for an Astro 7 site on Cloudflare Workers Static Assets. Use when adding or hardening CSP, HSTS, X-Frame-Options, frame-ancestors, Referrer-Policy, Permissions-Policy, COOP, COEP, or CORP, when deciding where each header belongs (native CSP meta element, Cloudflare _headers file, or middleware), when wiring script and style hashes, or when adding Subresource Integrity. Explains the per-page CSP delivery split (meta on static pages, header on SSR), why frame-ancestors and reporting directives need a real header, and the adapter limitation — it emits no static headers. Trigger on set up a hash-based CSP, add CSP to Astro, security headers on Cloudflare, _headers file, X-Frame-Options, clickjacking protection, or Astro Content Security Policy. Owns the CSP infrastructure — for one library's CSP recipe use motion-system (GSAP, Motion), webgl-atmosfera (shaders), signature-anim (Rive WASM), or seo-aeo-schema (JSON-LD).
---

# Web Security Headers for Astro on Cloudflare

> Deliver CSP plus the full HTTP security-header set for an Astro 7 site on Cloudflare Workers Static Assets. Astro's native CSP hashes scripts and styles per page; everything the meta element cannot carry, plus all transport and framing headers, lives in a hand-written public/_headers file.

## TL;DR
- Astro native CSP (security.csp) is hash-based and delivered per page automatically: a meta element on static pages, a Content-Security-Policy response header on server-rendered pages. It is not nonce-based.
- The Cloudflare adapter (@astrojs/cloudflare 14.2.1) does not support staticHeaders — gate re-verified 2026-08-17 against the adapter source; the decision stands — so on static pages the CSP stays a meta element. There is no built-in path to emit it as a real header on Cloudflare static output.
- The meta element cannot carry frame-ancestors, report-uri, report-to, or sandbox, and cannot be report-only. Clickjacking protection and reporting therefore require a real header in public/_headers.
- Put HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, and the Cross-Origin headers in public/_headers. That file applies only to static-asset responses, not to Worker (SSR) responses.
- Critical caveats, repeated under Limitations: keep COEP off by default (require-corp breaks cross-origin embeds such as WebGL textures and Rive), do not ship HSTS preload by default (it is effectively permanent), and do not put custom Cache-Control in _headers (unreliable on Workers assets, issue 13164).

## Reference materials — load when relevant

This SKILL.md is the verdict, the layer split, and the baseline. Load a reference only when its condition is met:

- references/csp-astro-native.md — load when configuring security.csp, adding external or CDN hashes, using the runtime CSP API, or hitting a CSP incompatibility.
- references/cloudflare-headers.md — load when writing or debugging the _headers file, configuring .assetsignore, or hitting the Cache-Control quirk.
- references/header-inventory.md — load for per-header recommended values, rationale, and caveats (HSTS, X-Frame-Options, Permissions-Policy, COOP, COEP, CORP, and the rest).
- references/middleware-ssr.md — load when any route is server-rendered and needs headers, or when a real CSP response header is required instead of the meta element.
- references/sri-and-verification.md — load when adding Subresource Integrity for cross-origin resources, or when verifying the deployed headers.

## Architecture — which layer emits which header

Two layers cooperate. Astro owns the CSP script-src and style-src hashing; Cloudflare _headers owns everything else, including the CSP directives the meta element silently drops. Server-rendered routes are a third surface, because _headers does not touch Worker responses.

| Header or directive | Where it goes | Why there |
|---|---|---|
| script-src, style-src (with hashes) | Astro security.csp; meta element on static pages, response header on SSR pages | Astro computes the per-page hashes; no other layer knows them |
| frame-ancestors, report-to, report-uri, sandbox | public/_headers | the meta element ignores these directives by spec |
| HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, COOP, COEP, CORP | public/_headers | transport, framing, and policy headers on static-asset responses |
| any header for a server-rendered or on-demand route | src/middleware.ts | _headers does not apply to Worker responses |

The reason the split is forced rather than chosen: on Cloudflare static output the adapter cannot hand Astro's computed CSP to a real header (no staticHeaders support in v13), so the meta element is the only native CSP carrier, and the meta element cannot express frame-ancestors or reporting. Those must come from _headers as a separate Content-Security-Policy header; the browser enforces the intersection of the meta policy and the header policy.

## Setup

### 1. Enable Astro native CSP

Turn on hashing and set the non-script, non-style directives. Do not list script-src or style-src here; configure those through scriptDirective and styleDirective (see references/csp-astro-native.md). Do not add unsafe-inline; Astro rejects it once hashes are present.

```js
// astro.config.mjs
import { defineConfig } from 'astro/config';
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
  adapter: cloudflare(),
  security: {
    csp: {
      algorithm: 'SHA-256',
      directives: [
        "default-src 'self'",
        "img-src 'self' data:",
        "font-src 'self'",
        "connect-src 'self'",
        "base-uri 'none'",
        "form-action 'self'",
        "object-src 'none'",
      ],
    },
  },
});
```

### 2. Write public/_headers

This carries every header the meta element cannot, plus the frame-ancestors directive for clickjacking. Place the file at public/_headers (extension-less); Cloudflare parses it and applies it to static-asset responses.

```
/*
  Strict-Transport-Security: max-age=63072000; includeSubDomains
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), camera=(), microphone=(), payment=(), usb=(), magnetometer=()
  Cross-Origin-Opener-Policy: same-origin
  Cross-Origin-Resource-Policy: same-origin
  Content-Security-Policy: frame-ancestors 'none'
```

Tune the values against references/header-inventory.md before shipping; the defaults above suit a mostly-static marketing or content site. Do not add Cache-Control here.

### 3. Server-rendered routes only

If any route is on-demand (SSR), public/_headers will not cover its response. Set its headers in src/middleware.ts, and emit a real Content-Security-Policy header there if that route needs one. See references/middleware-ssr.md.

### 4. Subresource Integrity, optional

Astro has no native SRI. For a mostly same-origin site it adds little; add it only for cross-origin resources, either by hand or with the small build-time hash script. See references/sri-and-verification.md. (@kindspells/astro-shield is retired from this stack — unmaintained, peer range stops at astro 4.)

### 5. Verify

CSP cannot be tested in astro dev. Build and preview, then check the live response.

- Run astro build, then astro preview (or deploy), and load a page.
- Inspect headers with a request tool (for example curl with the head flag) and a headers scanner.
- Open the browser console and confirm no CSP violations from your own scripts or styles.

## Gotchas

- CSP is inert in astro dev because of the Vite dev server. Always validate with build plus preview.
- The Cloudflare adapter does not support staticHeaders as of 14.2.1 (review-gate re-checked 2026-08-17: NOT triggered; the feature ships in the node, netlify, and vercel adapters only). Re-check on each adapter minor; if it lands, you can move CSP to a real header and drop the meta element.
- The ClientRouter view-transition component and Shiki inline styles conflict with native CSP. Use Prism for code highlighting, and test the router path explicitly.
- Do not put Cache-Control in _headers; it is unreliable on Workers assets (issue 13164, wontfix). The adapter already sets immutable Cache-Control for hashed _astro assets — but watch issue 16692 (that injection reported missing in some adapter configs): confirm the header on a deployed _astro asset.
- COEP require-corp breaks cross-origin embeds (WebGL textures, Rive files, third-party fonts) unless each resource sends CORP. Keep COEP off unless every cross-origin resource is CORP-clean.
- HSTS preload is effectively permanent and can lock out subdomains. Do not ship preload by default; prefer enabling HSTS zone-wide in the Cloudflare dashboard to avoid a duplicate header.
- Cloudflare's Add security headers Managed Transform omits CSP and Permissions-Policy by design. Avoid setting the same header in both _headers and a dashboard transform.

## Limitations and out-of-scope

- This skill does NOT cover application-layer auth, CORS policy design for APIs, WAF, rate limiting, bot management, cookie flags (SameSite, Secure, HttpOnly), or the report-collection backend; it only shows how to declare report-to.
- Performance caching strategy (Cache-Control) is out of scope and belongs to a performance or CI skill. Only the cache-quirk warning lives here.
- Astro native CSP is hash-only; it does not support nonces. A nonce requires a server-rendered route and a real response header.
- This targets Cloudflare Workers Static Assets with @astrojs/cloudflare 14.2.1 and Astro 7.2.2. The _headers format also applies to legacy Cloudflare Pages. Verify behavior on deploy; the Cache-Control quirk (issue 13164) is wontfix.
- Version pins are current as of 2026-08-17. Re-verify staticHeaders support and the security.csp API shape on Astro or adapter upgrades. The 6-to-7 major left security.csp intact (additive only — 7.1.0 added an optional kind option for script-src-elem/-attr and style-src-elem/-attr).
