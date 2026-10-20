---
name: launch-readiness-audit
description: Pre-launch audit for any website or web app — 35+ checks across mobile layout, links & navigation, SEO basics, content cleanup, UX feedback, security (API keys, admin routes, auth, database rules, input validation, rate limits, uploads, error leaks) and resilience (slow internet, payments & webhooks, break-it testing). Use before deploying, before handing a site to a client, after a big feature, or when the user says launch, go live, production-ready, pre-launch, audit, or "check everything".
---

# Launch Readiness Audit

Written for this agent-kit from Prashant's own pre-launch list. Checklist version (tick-boxes only): `.claude/checklists/launch-readiness.md`.

## How to run

1. **Classify the project first** — it decides which groups apply:
   - **Static / landing / portfolio** (no login, no DB): every item tagged [ALL] in the checklist — groups 1–4, 5.1–5.3, 6.1, 6.8, 6.9, 6.10, 7.1, 7.3 (27 + bonus).
   - **Web app with backend** (login, DB, APIs): all of the above + 5.4 and 6.2–6.7 (34 + bonus).
   - **Has payments**: everything, including 7.2 (35 + bonus).
2. Work group by group. For each item: check → fix → re-check. If a fix is outside the task scope or risky, list it instead of doing it.
3. Test against the running app (dev server or preview deploy), not just the code. Use `reticle-audit-my-app` / `reticle-test-error-states` if Reticle is set up, otherwise the browser.
4. Only test security on the user's own app and environments. Never run attack tools against third-party sites or production systems without explicit permission.
5. Finish with the report format at the bottom.

Related skills: `express-api-backend` + `owasp-security` (group 6 fixes), `llm-app-engineering` (AI endpoints: keys, rate limits, injection), `premium-interaction-craft` (states & feedback), `post-code-cleanup` (debug logs, dead code), `web-design-guidelines`, `checklist-design`, `reticle-*`.

---

## Group 1 — Mobile & layout  (applies: all)

**1.1 Remove horizontal scrolling / 1.2 Fix mobile overflow**
- Find the culprit in DevTools console:
  ```js
  [...document.querySelectorAll('*')].filter(e => e.getBoundingClientRect().right > document.documentElement.clientWidth + 1)
  ```
- Usual causes: fixed widths (`width: 1200px`, `w-[800px]`), `100vw` inside a page with a scrollbar, long words/URLs (fix: `overflow-wrap: anywhere`), images without `max-width: 100%`, negative margins, off-canvas menus/animations translated outside the viewport, wide tables/code blocks (wrap them in an `overflow-x: auto` container).
- Fix the cause. `overflow-x: hidden` on `body` is a last resort — it hides the bug and breaks `position: sticky`; if needed, prefer `overflow-x: clip` on the specific section.

**1.3 Add a mobile menu**
- Hamburger button is a real `<button>` with `aria-label`, `aria-expanded` and `aria-controls`.
- Menu: Esc closes, focus moves into it and back to the button on close, background scroll locked, closes on link click and on route change, tap targets ≥ 44px.

**1.4 Make every page mobile optimized / 1.5 Test mobile layouts**
- Check every route (not only home) at 360, 390, 414, 768 and 1024px, portrait and landscape, and on one real phone if possible.
- `<meta name="viewport" content="width=device-width, initial-scale=1">` present; zoom not disabled.
- Inputs use font-size ≥ 16px (stops iOS zoom-on-focus); fixed/sticky bars don't cover content or the on-screen keyboard; use `100dvh` instead of `100vh` for full-height sections.

## Group 2 — Links & navigation  (applies: all)

**2.1 Find broken links**
- Run against the running site: `npx linkinator http://localhost:3000 --recurse` (use the real port/preview URL). Fix every 404 / 5xx; also check anchor `#ids` exist.
- External links: working, `https`, and new-tab links use `rel="noopener noreferrer"`.

**2.2 Fix footer links**
- Every footer link goes somewhere real (no `href="#"`); social links point to the client's real profiles; legal pages exist.

**2.3 Remove unused navigation**
- No nav items for pages that don't exist or aren't ready. Nav is identical across pages; the current page is marked with `aria-current="page"`.

**2.4 Make the logo clickable**
- Logo is wrapped in a link to `/` with an accessible name (e.g. `aria-label="<Brand> home"` or logo `alt` text).

**2.5 Make the phone number clickable / 2.6 Make the email clickable**
- `<a href="tel:+91XXXXXXXXXX">` in international format (no spaces in the `href`), `<a href="mailto:name@domain.com">`.
- For local-business clients also consider a WhatsApp link: `https://wa.me/91XXXXXXXXXX` (digits only, country code, no `+`).

## Group 3 — SEO & identity basics  (applies: all)

**3.1 Add a favicon** — `favicon.ico` (or SVG) + 180×180 `apple-touch-icon` + web manifest icons 192/512 if it's a PWA. In Next.js App Router, placing `app/icon.png` / `app/favicon.ico` / `app/apple-icon.png` is enough.

**3.2 Fix page titles** — unique per page, "Page – Brand" pattern, ~50–60 characters. Next.js: `metadata` / `generateMetadata` with a `title.template` in the root layout.

**3.3 Add meta descriptions** — unique per page, ~150–160 characters, written for humans. Add Open Graph (`og:title`, `og:description`, `og:image` 1200×630) and canonical URL at the same time.

**3.4 Add a custom 404 page** — branded, explains what happened, links home and to key pages, and returns a real **404 status** (Next.js: `app/not-found.tsx`; SPA hosts: configure the host's 404 fallback). Also a friendly error page for 500s (`app/error.tsx`).

**3.5 Fix the copyright year** — render `© {new Date().getFullYear()} Brand`. Note: on fully static builds the year freezes at build time — either rebuild yearly, or render the year on the client.

## Group 4 — Content cleanup  (applies: all)

**4.1 Remove placeholder text** — search the code: `lorem|ipsum|placeholder|TODO|FIXME|coming soon|example\.com|John Doe|123-456|xxx`. Also placeholder images (unsplash/placehold.co/picsum), dummy prices, fake testimonials.

**4.2 Remove test data** — seed/mock users, test products/orders, `test@test.com` accounts, mock API responses left in production code paths, test-mode keys in production env.

**4.3 Compress images**
- Convert to AVIF/WebP, resize to the largest size actually displayed (×2 for retina), keep most images < 200KB and the hero < ~300KB.
- Next.js: use `next/image` (automatic formats/sizes). Otherwise: `sharp` script or Squoosh. Always set `width`/`height` (or `aspect-ratio`), `loading="lazy"` below the fold, and never lazy-load the LCP image.
- Strip EXIF/GPS metadata from user photos.

## Group 5 — UX feedback & broken interactions  (applies: all; APIs = backend apps)

**5.1 Fix broken buttons** — click every button and link on every page (or `reticle-audit-my-app`). A button must do something visible, have a disabled/loading state if async, and never be a `div` with `onClick`.

**5.2 Add success messages** — every form/action confirms what happened ("Message sent — we'll reply within 24 hours"), clears or keeps the form sensibly, and is announced to screen readers (`aria-live="polite"` / `role="status"`).

**5.3 Add error messages** — inline, next to the field, specific ("Enter a 10-digit mobile number"), say how to fix it, keep the user's input, `aria-describedby` links error to field.

**5.4 Handle API errors**
- Every `fetch`/API call handles: network failure, timeout, 4xx, 5xx, empty data, and non-JSON responses.
- UI shows a friendly message + retry, never a blank screen or infinite spinner. React: an error boundary per major section. Use `AbortController` timeouts for slow calls.

## Group 6 — Security  (applies: backend apps; 6.1/6.9/6.10 apply to all)

**6.1 Hide API keys**
- Secret keys live only on the server (env vars). Anything prefixed `NEXT_PUBLIC_` / `VITE_` / `REACT_APP_` is shipped to the browser — never put secrets there.
- `.env*` is in `.gitignore`; provide `.env.example` without values. Scan for leaks: `npx @secretlint/quick-start "**/*"` (no setup needed) or `gitleaks` on the repo, and search the built JS for `sk_`, `key=`, `secret`.
- If a key was ever committed or exposed: **rotate it** — deleting the commit is not enough.

**6.2 Protect admin routes / 6.3 Check authentication & permissions**
- Every protected page AND every API route checks the session on the **server** (middleware + inside the handler). Hiding a button in the UI is not protection.
- Authorization per resource: user A must not read/edit user B's data by changing an id in the URL or request (IDOR). Test it with two accounts.
- Roles checked server-side; admin actions logged. Sessions: httpOnly + Secure + SameSite cookies, logout invalidates, password reset tokens expire.

**6.4 Secure database rules**
- Supabase: Row Level Security ON for every table with policies; `service_role` key only on the server.
- Firebase: Security Rules are not left in test mode (`allow read, write: if true`); test with the Rules emulator.
- MongoDB/SQL: app uses a least-privilege DB user, DB not publicly reachable (IP allowlist / private network), backups on, no raw query string concatenation.

**6.5 Validate user inputs**
- Validate on the server with a schema (e.g. `zod`) for body, query, params and headers — client validation is only UX.
- Parameterized queries / ORM; sanitize any HTML that is rendered (no `dangerouslySetInnerHTML` with user content); limit lengths and payload size.

**6.6 Add API rate limits**
- Especially: login, signup, OTP, password reset, contact forms, AI/LLM endpoints, anything that costs money or sends email/SMS.
- Express: `express-rate-limit`. Serverless/Next.js: `@upstash/ratelimit` (Redis) or the host's firewall rules. Return 429 with a friendly message.

**6.7 Test file uploads**
- Check type by content (magic bytes, e.g. `file-type`), not just extension; allowlist types; max size limit on server; rename files (random names); store in object storage (S3/R2/Cloudinary/Supabase Storage), not the app folder; serve private files via signed URLs; block SVG/HTML uploads unless sanitized.
- Test: huge file, wrong type renamed to `.jpg`, empty file, many files at once, special characters in filename.

**6.8 Remove debug logs** — no `console.log` of tokens, user data or API responses; remove `debugger`; keep only intentional server logs (and never log passwords/tokens). `post-code-cleanup` covers this.

**6.9 Hide sensitive errors** — production responses never show stack traces, SQL errors, file paths or env values. Return a generic message + an error id; log the details server-side (Sentry or host logs). Framework debug/dev mode off in production.

**6.10 Security headers & HTTPS** — HTTPS only, HSTS, CSP, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `frame-ancestors` (Express: `helmet`; Next.js/Vercel: `headers()` in config). `npm audit --omit=dev` has no high/critical issues.

## Group 7 — Resilience & money flows

**7.1 Test slow internet**  (applies: all)
- Chrome DevTools → Network → throttling "Slow 4G" / "3G", and "Offline". Also CPU 4× slowdown.
- Check: skeletons/spinners appear, buttons can't be double-submitted, timeouts show a retry, nothing jumps around (CLS), fonts/images degrade gracefully, the page is usable before JS finishes.

**7.2 Test payments & webhooks**  (applies: apps with payments)
- Use test mode keys + the provider's test cards/UPI (Razorpay, Stripe…). Test success, failure, cancel, and closing the tab mid-payment.
- **Never trust the client** for payment success: confirm via server-side verification / webhook.
- Webhooks: verify the signature (Stripe: `stripe.webhooks.constructEvent` with the RAW body; Razorpay: HMAC SHA256 with the webhook secret), respond 2xx fast, make handlers idempotent (same event twice = one order), handle out-of-order events, log every event.
- Local testing: Stripe CLI `stripe listen --forward-to localhost:3000/api/webhooks`; for Razorpay use a tunnel (e.g. ngrok/cloudflared) to your local endpoint.
- Amounts come from the server (price lookup), never from the request body.

**7.3 Try to break your app (security & abuse testing)**  (applies: all, depth depends on app)
- Manual: tamper with ids in URLs/requests (IDOR), submit forms empty / huge / with `<script>alert(1)</script>` / `' OR 1=1 --` / `{"$ne": null}`, replay requests, double-click submit, open two tabs, use back button after logout, call APIs directly without the UI, remove the auth cookie.
- Automated (own app only): `npm audit`, OWASP ZAP baseline scan against a staging URL, Lighthouse Best Practices.
- Check the OWASP Top 10 categories as a mental checklist (broken access control, injection, auth failures, security misconfiguration, vulnerable components…).

---

## Report format

```
Launch readiness — <project> (<type: static | backend app | payments>)
✅ Passed: <n>/<applicable>
❌ Fixed during audit: <item — what was wrong — fix>
⚠️ Needs your decision: <item — why>
⏭ Not applicable: <items + reason>
Tools run: linkinator, secretlint, npm audit, Lighthouse, …
Tested on: <viewports / devices / network profiles>
```
