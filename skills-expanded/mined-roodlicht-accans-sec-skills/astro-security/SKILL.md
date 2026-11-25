---
name: astro-security
description: Astro security review — render-mode attack surface (SSG/SSR/hybrid), set:html and MDX content collections (XSS + author trust), API routes and middleware (auth, scope), adapter-specific runtime models (Cloudflare/Vercel/Netlify/Node), env-var hygiene (PUBLIC_ prefix), and Decap CMS pairing (OAuth backend, token storage, branch-based editorial workflow).
---

# Astro Security

## When to use

This skill is the Astro-specific layer on top of `secure-coding`. Astro mixes static-site generation, server-side rendering, and partial hydration in one codebase, which means the attack surface differs per page even within the same project. That mixed-mode reality is the single most underappreciated source of Astro security mistakes.

Triggers on:

- A question like "review our Astro app for security issues", "is this page SSG or SSR", "set:html on user input", "Astro API route auth", "Decap CMS hardening", "OAuth backend for Decap", "Astro middleware bypass".
- Presence of `astro.config.mjs`/`.ts`, `src/pages/`, `src/middleware.ts`, `src/content/` directories, `@astrojs/*` adapters, or `decap-cms`/`netlify-cms` admin-UI files.
- A PR touching `set:html`, `Astro.locals`, middleware, content-collection schemas, MDX components, or adapter config.
- Astro version bumps, especially around security advisories (check the `astro` GitHub security tab).
- A handoff from `security-review` or `api-security` when Astro is in the stack.

### When NOT (handoff)

- General TS/JS secure-coding (not Astro-specific) → `secure-coding`.
- OWASP API Top 10 as a conceptual framework → `api-security`. Here for the Astro-specific implementation of API routes.
- SAST tooling (eslint-plugin-security, Semgrep `p/javascript`) → `sast-orchestrator`.
- Dep vulns in `package.json` → `cve-triage`.
- Adapter-platform infrastructure (Cloudflare Workers KV access, Vercel project-config, Netlify env-vars) → platform-specific docs and `iac-security` where relevant.
- Secrets in `.env`, `.env.local`, or platform env-var stores → `secrets-scanner`.
- Decap CMS as a stand-alone topic outside Astro context (e.g. with Hugo, Gatsby, Eleventy) — this skill covers it because the Astro+Decap pairing is the most common production deployment.

## Approach

Six phases. Phase 1 (render-mode classification) is the foundation — without it you cannot reason about which security rules apply to a given page.

### 1. Render-mode classification → attack-surface map

Astro has three output modes, set in `astro.config.mjs`:

- **`output: 'static'`** (default, SSG). Pages render at build time. No server-side runtime at request time. The attack surface is the build pipeline (supply chain, secrets in environment, `[verify]`-marked CVEs in dependencies) — not the running site. Once deployed, pages are plain HTML.
- **`output: 'server'`** (full SSR). Every page renders per request. Auth, sessions, env vars, server-side data fetches — all live.
- **`output: 'hybrid'`** (mixed). Default to SSG, opt-in to SSR per page via `export const prerender = false`. Or default to SSR with `export const prerender = true` for pre-rendered routes.

**Reviewer rule**: for every page or route, identify its render mode FIRST. The `prerender` flag, the absence/presence of an adapter, and any per-page exports decide which security rules apply. A page that "looks" dynamic in the source can still be SSG (so dynamic data is frozen at build time, possibly leaked to the static HTML); a page that "looks" static can be SSR (so input-validation and auth become live concerns).

Common mistake: assuming hybrid means "the safe parts are static". The pages that use `Astro.request` or read cookies must be SSR. If they slip into SSG by default, they may bake build-time-only data (env vars, request-context defaults) into the static output and leak it.

### 2. Output sanitization and XSS

Astro auto-escapes content rendered via `{expression}` in templates. XSS arises where you opt out.

- **`set:html`** directive — Astro's equivalent of React's `dangerouslySetInnerHTML`. Renders raw HTML.
  ```astro
  <div set:html={userContent} />        <!-- XSS if userContent is user input -->
  <Fragment set:html={trustedHtml} />   <!-- same risk, no wrapping element -->
  ```
  Default rule: never on user-controlled input. If you need rich-text input, sanitize via DOMPurify (server-side) or an isomorphic sanitizer before assignment.
- **MDX in content collections** — see phase 4. MDX includes JSX expressions and component instantiation; treating it as "just markdown" is wrong. MDX = code execution in the render context.
- **`client:*` directives** (`client:load`, `client:visible`, `client:idle`, `client:only`) ship JS to the browser. Review what is hydrated, especially client-side props that flow from server-side fetches — props are serialized into the page HTML and visible in the browser. Same trust-boundary discipline as the Next.js Server/Client Component boundary.
- **Markdown rendering** is safe by default: standard CommonMark / GFM is parsed and escaped. Custom remark/rehype plugins can reintroduce raw-HTML pass-through; review any `rehype-raw`-style plugin.
- **`<style>` and `<script>` element exceptions**: Astro's `is:inline` directive bypasses processing. Combined with templated content this can become an injection vector.

### 3. Server endpoints (API routes) and middleware

Two server-side primitives, both common attack-surface entry points.

**API routes** (`src/pages/api/*.ts`):

```ts
export async function POST({ request, locals }: APIContext) {
  const session = locals.session;             // set by middleware
  if (!session) return new Response("unauth", { status: 401 });

  const body = await request.json();
  const parsed = schema.safeParse(body);      // zod / valibot
  if (!parsed.success) return new Response("bad request", { status: 400 });

  // ... business logic with explicit ownership check
}
```

- Auth in the handler, not only in middleware (defense-in-depth).
- Input validation via zod/valibot. Trust nothing from `request.json()` or `request.formData()`.
- IDOR fix: compare resource ownership against the authenticated identity. Same `api-security` API1 BOLA discipline.

**Middleware** (`src/middleware.ts`):

- Runs before every matching request, can mutate `context.locals`, redirect, or rewrite.
- Useful for: setting auth context, security headers, redirects.
- **Not safe as the only auth gate**. The Next.js CVE-2025-29927 class of middleware-bypass bug taught this lesson the hard way: middleware logic on the server can be skipped under specific request shapes if the framework has a bug. Pages and API routes must independently verify auth from `Astro.locals`.
- Matchers: Astro middleware matches all requests by default; scoping is via early-return inside the middleware. Make sure the path-check is correct and not bypassable via URL-encoding.

### 4. Content collections, MDX, and the author-trust model

Content collections (`src/content/<collection>/*.{md,mdx,json,yaml}`) are typed content, validated via a `config.ts` schema. Two security considerations:

- **MDX = code execution at render**. MDX files can include JSX expressions, import components, and run logic. An author who can write MDX into the content collection has effectively code-execution rights in the rendering context. This is fine for internal-team authors. It is **not** fine for user-generated content (blog comments, user profiles, community posts) — those must be plain Markdown or sanitized HTML.
- **Schema validation does not sanitize content body**. The `z.object({...})` schema validates frontmatter; the body content is still arbitrary markdown/MDX. Schema is a type guard, not an XSS guard.

**Author-trust model checklist:**

- Who can commit to `src/content/`? In a Decap CMS setup (phase 6), this maps to "who has OAuth-authenticated edit access to the repo".
- Are MDX files limited to a content collection where only trusted authors write? If a user-facing collection allows MDX, that is a finding.
- Can imports inside MDX reach `src/components/*` or `src/lib/*`? If yes, the author-trust model extends to your entire `src/` tree — not just the markdown directory.

### 5. Adapter-specific runtime + env vars + headers

Astro is adapter-agnostic, but each adapter has different security ergonomics.

- **`@astrojs/node`** — runs as a regular Node server. Standard Node security context: process env vars, filesystem access, network egress. No platform sandbox.
- **`@astrojs/cloudflare`** — Cloudflare Workers runtime. Env vars are bound, not from `process.env`. KV / R2 / D1 / Durable Objects are accessed via bindings on `context.locals.runtime.env`. Smaller request body limits (~100MB), constrained CPU time, no Node API.
- **`@astrojs/vercel`** — edge runtime or serverless functions. Edge runtime is V8-isolate (no Node API), serverless is Node. Edge-vs-serverless choice matters for which APIs you can use; security model differs slightly (edge has stricter cold-start isolation).
- **`@astrojs/netlify`** — Netlify Functions or Edge Functions, similar to Vercel split.

**Env vars**:

- `PUBLIC_*` prefix exposes the variable to the **client bundle**. Anything with `PUBLIC_` is essentially public — treat it that way.
- Server-only env vars must NOT carry the `PUBLIC_` prefix.
- `astro:env` (Astro 5+, opt-in) provides a typed schema for env access. Use it where available; it catches accidental client/server mismatches at build time.
- Audit: grep for `PUBLIC_` in your code. Anything with `KEY`, `SECRET`, `TOKEN`, `API`, `PASSWORD` after `PUBLIC_` is a finding.

**Security headers**:

- Astro 5+ has experimental CSP integration (`experimental.csp`). Where available, prefer it over hand-rolled middleware-set CSP.
- Without built-in CSP: set headers via the adapter's response handler or via middleware for SSR pages. Static pages get headers from the host (Cloudflare Pages, Vercel, Netlify all support per-route headers config).
- HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy — same baseline as any modern web app.
- CSP with `unsafe-inline` defeats most of the point. Use nonces or hashes; Astro's CSP integration supports nonce flow.

### 6. Decap CMS (formerly Netlify CMS)

Decap is the most common CMS pairing for Astro: git-based, content stored as files in the repo, edited via a JS admin UI. Specific security implications:

**OAuth backend**:

- Decap admin UI authenticates via OAuth against a git provider (GitHub, GitLab, Bitbucket).
- The OAuth flow needs a backend exchange (the OAuth client_secret can't sit in the browser). Common implementations: a self-hosted Cloudflare Worker / Netlify Function / Vercel Function that handles the `/api/decap-auth/*` exchange. Netlify Identity (the historical default) was deprecated.
- **OAuth scope minimization**: the registered OAuth app should request only the scopes Decap needs (`repo` for GitHub if private; `public_repo` if public; nothing more). Audit the OAuth app's scope on the provider side.
- **Repo restriction**: configure the OAuth app to be restricted to the specific repo. On GitHub: a GitHub App scoped to one repo is preferable over a classic OAuth app with broad access.

**Token storage and XSS impact**:

- Decap stores the OAuth access token in `localStorage` after login. This is by design (the SPA needs it for git-API calls).
- **Consequence**: XSS on the admin UI = token theft = full repo write access until token expires.
- **Mitigation**: strict CSP on the admin UI (`/admin/`), no `unsafe-inline` in the admin route, treat the admin UI as a trust boundary distinct from the public site. If your CSP on the public site needs to be relaxed for any reason, the admin UI's CSP must be tightened independently.
- Token lifetime: GitHub OAuth tokens don't expire by default. Consider rotating the OAuth app credentials periodically; revoke immediately if XSS is found.

**Editorial workflow**:

- `publish_mode: editorial_workflow` puts content edits into a draft branch, with PR review before merge.
- This is effectively a PR-as-content-gate — review of content goes through the same review path as code.
- Without editorial workflow, every save is a direct commit to `main`. For multi-author setups or anything customer-facing, editorial workflow is the right default.

**Authorization model**:

- Decap has **no native role system**. Authorization is entirely the git provider's repo permissions: who has commit access to the repo can edit. There is no "editor-only, can't touch settings" tier.
- Implication: an editor account is, from the git-provider perspective, a write-access account. Treat editors with the same vetting as developers.
- For finer-grained control, use GitHub branch protection + CODEOWNERS + required reviews on `main`. Editorial-workflow PRs go to feature branches; CODEOWNERS gates merging to main.

**Media library**:

- Uploaded media goes into the repo as files, committed via the OAuth-authenticated user.
- Large or binary uploads inflate the repo. Consider an external media backend (Cloudinary, ImageKit, custom S3) for production.
- File-type validation is done client-side in Decap; the git API will accept anything. Validate again in CI (e.g. a workflow that scans new files in the editorial-workflow branch).

### Verification-loop

Layer 1: render mode identified per page (SSG / SSR / hybrid)?, all `set:html` reviewed for user-input source?, MDX scope contained to trusted authors?, API routes have auth + input validation?, middleware not the only auth gate?, env vars audited for accidental `PUBLIC_` prefix?, Decap OAuth scope minimized + admin-UI CSP tightened?

Layer 2: Astro version up to date (check `astro` GitHub security advisories, `[verify]` markers on any specific CVE claims), adapter version current, Decap CMS version current, claims about OAuth scope behavior verified against the actual GitHub/GitLab OAuth app config (not assumed).

## Output

```
Astro security review — <app>
Astro: <x.y.z> | Adapter: <node | cloudflare | vercel | netlify>
CMS: <Decap | other | none>

Render-mode map:
  output:                <static | server | hybrid>
  Per-page prerender exports: <list of explicit overrides>
  Pages with auth/sessions:   <should be SSR; verify>

Output sanitization:
  set:html occurrences:       <N, locations, source-of-input per occurrence>
  MDX collections:            <which, author scope>
  client:* directives:        <which, hydrated props review>

Server endpoints:
  src/pages/api/* count:      N
  Auth check per handler:     <yes for all | gaps on ...>
  Input validation:           <zod/valibot/... | none>

Middleware:
  src/middleware.ts present:  <yes/no>
  Auth in middleware only:    <FINDING if yes>
  Headers set in middleware:  <list>

Content collections:
  Collections defined:        <list, MDX-allowed yes/no per collection>
  Author-trust model:         <internal-team | broader>

Adapter + env vars:
  Adapter:                    <name + version>
  PUBLIC_* vars:               <list, review for accidental exposure>
  astro:env in use:            <yes/no>
  Security headers:            <CSP, HSTS, etc. — present, nonce-based>

Decap CMS (if applicable):
  OAuth backend:               <self-hosted worker | Netlify Identity (deprecated) | other>
  OAuth scope:                 <minimum repo scope | over-permissive — FINDING>
  GitHub App vs OAuth app:     <App | classic OAuth app — FINDING if classic on private repo>
  Editorial workflow:          <enabled | disabled>
  Admin UI CSP:                <strict | inherits public CSP — FINDING if same as public>
  Media backend:               <git-stored | external>

Version check:
  Astro security advisories:   <within N days | check>
  Decap CMS version:           <date of last update>
  cve-triage handoff:          <N deps with vulns>

Findings (severity-sorted, follow security-review format)
Verification-loop: ...
```

## References

- **Astro security overview** — [https://docs.astro.build/en/guides/security/](https://docs.astro.build/en/guides/security/). Official Astro security guidance.
- **Astro CSP integration** — [https://docs.astro.build/en/reference/experimental-flags/csp/](https://docs.astro.build/en/reference/experimental-flags/csp/). Built-in CSP from Astro 5+.
- **Astro middleware** — [https://docs.astro.build/en/guides/middleware/](https://docs.astro.build/en/guides/middleware/).
- **Astro content collections** — [https://docs.astro.build/en/guides/content-collections/](https://docs.astro.build/en/guides/content-collections/). MDX vs Markdown distinction.
- **Astro endpoints** — [https://docs.astro.build/en/guides/endpoints/](https://docs.astro.build/en/guides/endpoints/). Server endpoints (API routes) reference.
- **Astro security advisories** — [https://github.com/withastro/astro/security/advisories](https://github.com/withastro/astro/security/advisories). Primary CVE source.
- **Decap CMS docs** — [https://decapcms.org/docs/](https://decapcms.org/docs/). Backend, OAuth, editorial workflow.
- **Decap CMS GitHub** — [https://github.com/decaporg/decap-cms](https://github.com/decaporg/decap-cms). Source + advisories.
- **GitHub OAuth app vs GitHub App** — [https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/differences-between-github-apps-and-oauth-apps](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/differences-between-github-apps-and-oauth-apps). For Decap backend choice.
- **OWASP Top 10 2021** — [https://owasp.org/Top10/](https://owasp.org/Top10/).
- **CSP Reference** — [https://content-security-policy.com/](https://content-security-policy.com/). Per-directive guide.
- **MDN Security Headers** — [https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers).

## Categories

- appsec
