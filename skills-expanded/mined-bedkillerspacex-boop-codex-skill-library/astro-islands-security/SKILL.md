---
name: astro-islands-security
description: >
  Astro islands architecture security for owned sites: server vs client trust boundaries,
  partial hydration, props serialization, XSS via set:html/raw HTML, env exposure
  (PUBLIC_*), and API route auth. Use when reviewing Astro apps for client-boundary leaks
  or hardening islands — not for attacking third-party Astro sites.
---

# Astro Islands Security

## Scope And Authorization

- **In scope:** Astro projects you own or assess with authorization (static, SSR, hybrid).
- **Out of scope:** Unauthorized testing of external Astro deployments.
- Islands move code to the browser — treat props and hydrated components as public surface.
- Never put secrets in `PUBLIC_` env vars or client islands.
- Pair with `code-quality-standards`, `xss-cross-site-scripting` when HTML sinks appear.

## When To Use

- Choosing which components are islands (`client:load` / `visible` / `idle` / `only`).
- Reviewing props passed into React/Vue/Svelte islands for sensitive data.
- Hardening `set:html`, Markdown, or CMS-driven HTML.
- SSR/API routes (`src/pages/api`) authz and CSRF considerations.
- Preventing ship of service tokens via Vite-define or import.meta.env mistakes.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Deep XSS methodology | `xss-cross-site-scripting` |
| React component patterns | `react-component-patterns` |
| CSP header deployment | security headers / nginx skills |
| Generic secrets hygiene | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Boundary | Trust |
| --- | --- |
| `.astro` server render | Can use secrets, DB, private APIs (SSR) |
| Island (`client:*`) | Untrusted browser; all props visible |
| `import.meta.env.PUBLIC_*` | Exposed to client bundle |
| Server-only env | No `PUBLIC_` prefix; not imported by islands |
| Content collections / MD | Treat as untrusted if author not fully trusted |

## Island Directive Risk

| Directive | Security note |
| --- | --- |
| `client:load` | Immediate hydration; largest early JS surface |
| `client:visible` | Defers until viewport; still full client trust once loaded |
| `client:idle` | Same trust as other client directives |
| `client:only` | Skips SSR for component — still ships JS/props |
| none (static) | Prefer for pure content; least client attack surface |

## Workflow

### 1. Confirm scope and success criteria

1. Record output mode (static/server/hybrid), adapters, auth model, CMS sources.
2. Success: no secrets in client bundles; islands receive only public DTOs; HTML sinks sanitized; API routes enforce auth.
3. Inventory frameworks used in islands (React/Vue/Svelte/Solid).

### 2. Inventory islands and env

```bash
rg -n "client:(load|visible|idle|only|media)" src
rg -n "set:html|set:text" src
rg -n "PUBLIC_|import.meta.env" src
rg -n "src/pages/api" -g '*.ts' -g '*.js'
npm run build
# Inspect client assets for accidental secrets (careful redaction)
rg -n "API_KEY|SECRET|PRIVATE" dist || true
```

1. List each island entry component and its props interface.
2. Flag server modules imported from island code (bundle leakage risk).
3. Note third-party scripts in layouts.

### 3. Baseline

1. Save build output size and list of hydrated islands on critical pages.
2. Capture any existing CSP / security headers.
3. Sample CMS HTML for script tags.

### 4. Apply hardening

**Minimize islands**

1. Prefer static `.astro` for content; hydrate only interactive widgets.
2. Pass minimal props: IDs and display strings, not full user records or tokens.
3. Fetch private data inside SSR frontmatter; send derived public view models only.

**Safe HTML**

```astro
---
// Prefer components + set:text; if HTML required, sanitize server-side first
import { sanitize } from '../lib/sanitize';
const safe = sanitize(cmsHtml);
---
<article set:html={safe} />
```

1. Do not pass unsanitized CMS HTML into islands for `dangerouslySetInnerHTML` / `v-html`.
2. Markdown: use a hardened pipeline; disable raw HTML if authors untrusted.

**Env separation**

```ts
// server-only
const dbUrl = import.meta.env.DATABASE_URL;
// client-safe
const publicCdn = import.meta.env.PUBLIC_CDN_URL;
```

1. Never prefix secrets with `PUBLIC_`.
2. Avoid importing server modules from files that islands import.

**API routes**

```ts
// src/pages/api/profile.ts
import type { APIRoute } from 'astro';
export const GET: APIRoute = async ({ cookies, request }) => {
  const session = await requireSession(cookies, request);
  if (!session) return new Response('Unauthorized', { status: 401 });
  // return only authorized fields
  return Response.json({ name: session.publicName });
};
```

1. Same-origin cookie flags: `HttpOnly`, `Secure`, `SameSite`.
2. CSRF strategy for cookie-authenticated mutating routes.
3. Rate-limit auth and form endpoints when exposed.

**Headers (adapter/nginx)**

1. CSP with strict `script-src` (nonces/hashes if possible).
2. `X-Content-Type-Options`, `Referrer-Policy`, `Frame-Ancestors` as appropriate.

### 5. Verify with evidence

```bash
npm run build
rg -n "sk_live|BEGIN PRIVATE|DATABASE_URL" dist && echo FAIL || echo OK
# Authz
curl -i https://localhost:4321/api/profile
curl -i -H "Cookie: session=..." https://localhost:4321/api/profile
```

1. Browser DevTools: island props in HTML/JSON must not contain secrets.
2. XSS tests on CMS fields (authorized) — see XSS skill for methodology.
3. Confirm static pages that need no JS avoid unnecessary `client:*`.

### 6. Observe and harden

1. Monitor CSP reports if deployed.
2. Review new islands in PR checklist: props sensitivity + directive choice.
3. Dependency audit for island framework CVEs.

### 7. Hand off

1. Document island map and allowed prop types.
2. Env var table: server vs PUBLIC.
3. Link CSP/CDN owners.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Hydration | Few small islands | Entire page `client:load` |
| Props | Public DTO | Session token in prop |
| HTML | Sanitized set:html | Raw CMS HTML to island |
| Env | Secrets server-only | `PUBLIC_API_SECRET` |
| API | Session + authz checks | Open JSON with PII |
| Scope | Own site | Unauth third-party testing |

## Output Checklist

- [ ] Mode/adapter/auth model recorded
- [ ] Island inventory with directives
- [ ] Props reviewed for sensitive fields
- [ ] HTML sinks sanitized or removed
- [ ] Env PUBLIC_ vs secret separation verified
- [ ] API routes authn/z + cookie flags
- [ ] Build/dist secret scan clean
- [ ] CSP/headers considered
- [ ] `code-quality-standards` applied

## Rules

- Client islands are public code + public data surfaces.
- Never ship secrets via env PUBLIC_ or island props.
- Prefer static rendering; hydrate intentionally.
- Sanitize any HTML that crosses trust boundaries.
- Focus on Astro boundaries; deep XSS/CSRF methodology in dedicated skills.
