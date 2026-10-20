---
name: frontend-feature-audit
description: "Use when auditing a frontend for feature completeness."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [qa, audit, frontend, completeness, nextjs, mock-data, dead-links, placeholder]
    triggers: [audit, feature-completeness, frontend-audit, placeholder, mock-data, phantom-route, dead-link, unimplemented, static-content, qa-matrix]
    related_skills: [web-app-qa, dogfood, gstack-qa]
---

# Frontend Feature Completeness Audit

Audit a web frontend for **unimplemented features** — mock data masquerading as real, phantom routes, dead links, fake flows, static placeholders — and deliver a route/workflow QA matrix with file:line evidence. Read-only investigation; do not edit files during the audit.

Distinct from `web-app-qa` (post-fix end-to-end verification): this is the pre-launch/pre-handoff **"what's actually implemented?"** sweep. The two pair well — audit first, then verify fixes in a real browser.

## When to Use

- Asked to "audit feature completeness", "check what's actually implemented", "find placeholders/stubs", or "create a QA matrix"
- Before demoing, shipping, or selling a site — catch fake features before they embarrass
- When a site looks polished but the DB/API returns empty (hardcoded UI hiding missing backend)
- Next.js App Router, Astro, or any framework with file-based routing + a route-protection/middleware layer

## Methodology (7 steps)

### 1. Route inventory
```bash
find app components lib -type f \( -name "*.tsx" -o -name "*.ts" \) | grep -v node_modules | sort
```
Note dynamic segments (`[slug]`, `[[...slug]]`), API routes, `not-found.tsx`. This is the ground truth of real routes.

### 2. Placeholder / mock-data scan
```bash
grep -rniE "TODO|FIXME|mock|Mock|placeholder|coming soon|would come from|Add more|Simulate API call|not implemented|under construction" app components lib --include="*.tsx" --include="*.ts"
```
Filter false positives (Tailwind `placeholder:` classes, `placeholder="..."` input props). Real signals:
- `// TODO: Implement actual ...` + hardcoded values (`rating: 4.5`, `badge: undefined`)
- `// Simulate API call` + `setTimeout` in submit handlers
- `const mockBook = {...}` / `// Mock data - would come from database`
- Hardcoded arrays with `// Add more posts...`

### 3. Three-way cross-check: nav hrefs ↔ route files ↔ auth config
```bash
grep -rn "href=" components/*nav*.tsx components/footer.tsx | grep -oE '"/[^"]*"' | sort -u
find app -maxdepth 2 -name "page.tsx" | sort
cat lib/utils/protected-routes.ts   # or middleware.ts
```
Three failure classes:
- **Phantom routes**: linked in nav or protected-route config with no page file → 404 for logged-in users (anonymous users only see the 307→login).
- **Auth-gated publics**: apps where unknown routes default to `requiresAuth=true`. Public-by-intent paths (`/endings/*`, `/tag/*`, `/book/*/rewrites`, `/story/*`) missing from `PUBLIC_ROUTES` get bounced to login for anonymous visitors. This is the sneakiest one — the site looks fine logged-in, but public content is walled.
- **Dead mock links**: hardcoded homepage showcase/testimonial data with fake authors → profile links 404, story links redirect into the auth wall.

### 4. Live probe — NEVER trust `-L`
```bash
# Pass 1: real status + redirect target, NO -L
curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" -m 20 "https://site$path"
# Pass 2: Location header for 3xx
curl -s -o /dev/null -m 20 -D - "https://site$path" | grep -iE "^HTTP|^location"
```
**Pitfall:** an early pass with `curl -L` reported 200 for protected routes — `-L` follows the 307→login and the login page returns 200, masking the auth wall. Always probe without `-L` first; `redirect_url`/`Location: /login?redirect=...` is the auth-wall signal.

### 5. Fake-flow detection (client components)
Grep for `Simulate`, `setTimeout`, `toast.success` inside submit handlers. Common patterns:
- Contest entry / contact forms: `await new Promise(r => setTimeout(r, 2000))` then success toast — nothing persisted.
- Account deletion: `// TODO: Implement account deletion` with success toast + `router.push("/login")` — nothing deleted.
- "Request Data Export" buttons with no `onClick` handler at all (dead button).

### 6. Browser pass (console / network / a11y)
Browser fallback ladder when the default backend is unavailable:
1. `browser_navigate` (CDP) — may fail with connection refused.
2. playwright-mcp `browser_navigate` — may fail "Browser is already in use ... use --isolated".
3. chrome-devtools-mcp `list_pages` → `navigate_page` on an already-attached Chrome — most reliable fallback.

Collect per page:
- Console errors — React minified #422/#425 = rules-of-hooks violation (conditional hook call); `[issue] A form field element should have an id or name attribute` = a11y.
- Network failures — 500s on `/_next/image?url=https://m.media-amazon.com/...` = remote host blocks Next's image proxy; 307 on `/icon.ico` = middleware matcher excludes `favicon.ico` but not `icon.ico`.
- A11y snapshot — missing labels, unlabeled buttons, empty states.

### 7. Deliverable — route/workflow QA matrix
| Route / Flow | Live status | Evidence | Root cause (file:line) |
|---|---|---|---|
| `/endings` | 500 `__next_error__` | curl + browser | SSR crash in list page |
| `/library` | 307→login (anon), 404 (authed) | curl; no route files | nav link w/o page file |

Plus a **"what works" list** (verified-clean routes so the reader knows what NOT to touch) and severity-ranked fix priorities (P0/P1/P2). Lead the report with outcomes; the parent agent's context is precious.

## Pitfalls

- **`curl -L` masks 307→login as 200** — probe without `-L` first, always.
- **Windows host, `search_files` fails on `E:\` drive-letter paths** ("cannot find the path") — fall back to terminal `grep -rniE ... /e/path --include="*.tsx"` with MSYS-style paths.
- **`curl -o /tmp/foo` may fail on MSYS** — `/tmp` doesn't resolve; write probe bodies to `~/`.
- **Hardcoded stats on homepages** (10K+ users, 4.9 rating) with an empty API are marketing placeholders — flag as fake data and note the numbers are fabricated.
- **"200 on protected route" is often the login page after redirect** — verify content identity when status codes look wrong (compare body against known pages).

## Support files

- `references/bookends-audit-worked-example.md` — full worked example: BookEnds (bookends.your-domain.example, Aug 2026) audit with every confirmed finding and file:line ref.
