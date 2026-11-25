---
name: ui-page-errors
description: "Error and status pages: not found, server error, forbidden, expired links, offline, maintenance and rate limiting, each with the right HTTP status, what happened in plain words, and ways forward. Read before building a 404, 500 or any error page."
---

# Error and status pages

The generated 404 is a giant number, an astronaut, "Oops! Looks like you're
lost in space" and one "Go home" button, served with status 200 so search
engines index it; the 500 is a stack trace or a blank white page. An error
page has three jobs: say what happened in plain words, keep the person
oriented and give them ways forward, and tell machines the truth with the
right status. The measures are in `ui-layout`; errors inside a working
screen (a failed block, a failed save) are `frontend-errors`.

## 1. The pages at a glance

| Page | Status | It says | Ways forward |
|---|---|---|---|
| Not found | 404 (410 when removed on purpose) | No page here, or it moved | Search, home, main sections |
| Server error | 500 | Something failed on our side | Try again, status page, a reference for support |
| Bad gateway, timeout | 502, 504 | The site is not answering right now | Try again in a minute, status page |
| Maintenance | 503 with `Retry-After` | What is down, and until when | Status page, when to come back |
| Forbidden | 403 | You are signed in but cannot see this, and why | Who can grant access, Request access, switch account |
| Signed out | 401 from the API; a sign-in page for people | Sign in to continue | Sign in, then back to this page |
| Expired or used link | 410 or 400 | This link expired or was used, and why | Send a new link, sign in |
| Rate limited | 429 with `Retry-After` | Too many attempts, and when to retry | Wait, or another way (reset password) |
| Offline | none (service worker) | You are offline, and what still works | Retry, which also happens by itself |

## 2. The skeleton

```
│ [the site's header and navigation, as on every page]                      │
│                                                                           │
│   Error 404                                          a small label        │
│   Page not found                                     (h1) the state       │
│   There is no page at /pricing/teams. It may have moved.                  │
│   [ Search the site .......................... ] [ Search ]               │
│   Pricing · Documentation · Contact                  real main sections   │
│                                                                           │
│ [the site's footer]                                                       │
```

- Keep the site's header and footer: people who land on an error from a
  search or an old link can still go anywhere. Inside an application the
  shell (sidebar, top bar) stays, and the error fills the content area.
- The message sits in the page's content column, left-aligned with the rest
  of the site (or centred as one short block when the page holds nothing
  else), 480 to 640px wide, 64 to 96px below the header. Not a full-screen
  splash.
- The `h1` names the state in words ("Page not found"); the number is a
  small label or left out. The document title says the same: "Page not
  found · [Site]".
- An illustration is optional and small (under about 200px), from the
  site's own world, and never pushes the ways forward out of view.

## 3. Not found (404)

- Show the address that was asked for, and say it does not exist or has
  moved, without blaming whoever typed it.
- The site's own search, links to home and the 3 to 5 main sections, and a
  "Did you mean /pricing?" link when the site can find a close match.
- Status 404 from the server for every unknown path. A single-page app that
  answers every path with `index.html` and 200 makes soft 404s that search
  engines index. Frameworks: Next.js `notFound()` and `app/not-found.tsx`;
  SvelteKit `error(404)` and `+error.svelte`; Nuxt
  `createError({ statusCode: 404 })` and `error.vue`; Astro
  `src/pages/404.astro`; Laravel `resources/views/errors/404.blade.php`;
  Django `404.html` (with `DEBUG = False`).
- Moved content answers 301 to its new address (keep a redirect map);
  content removed for good can answer 410.
- Never redirect every 404 to the home page: it hides the problem from
  people and crawlers alike.
- Log 404s with their referrer to find the broken links you own.

## 4. Server errors and maintenance (500, 502, 503, 504)

- Apologise once, plainly: "Something went wrong on our side. Try again in
  a moment." No jokes here.
- A "Try again" button that reloads, the status page if there is one, and a
  support route with a reference the user can copy (the request or error id
  from the logs or the error tracker): "Reference: 7f3a2c9e".
- Never a stack trace, SQL, file paths, versions or internal host names:
  those go to the logs (`backend-errors`).
- The page must not depend on what failed: static HTML with inline CSS, no
  database call, no app bundle. Frameworks keep one (Next.js
  `app/global-error.tsx`, SvelteKit `src/error.html`, Rails
  `public/500.html`), and the proxy or CDN serves one when the app is down
  (nginx `error_page 502 503 504 /50x.html;`, Cloudflare custom error
  pages).
- Maintenance is a 503 with `Retry-After`, the expected end in the reader's
  time zone ("Back by 14:00 WIB"), what is affected, and the status page;
  planned work is announced in a banner beforehand. A short 503 keeps
  search rankings; a maintenance page served with 200 does not.

## 5. Forbidden and signed out (403, 401)

- Signed out: send people to sign in with a return address
  (`/sign-in?next=/invoices/42`, checked to be a path on this site) and
  bring them back after.
- Signed in without access: say what the page belongs to and what is
  needed ("This project belongs to the Finance workspace. Ask an owner for
  access."), name who can grant it when the user may know, offer "Request
  access" if the request reaches someone, and "Switch account" for people
  signed in with the wrong one.
- When admitting that a record exists would leak something (a private
  project), answer 404 instead (`backend-api`, section 2).

## 6. Expired and invalid links

- Reset links, email confirmations, invites, magic links and download links
  expire or get used. Say which and why ("Reset links last an hour, to keep
  your account safe"), and put the fix on the same page: "Send a new link",
  with the email filled in when it is known; "This invite was already
  accepted. Sign in".
- A 4xx status (410 for expired, 400 for malformed), `noindex`, and never a
  bare "Invalid token".

## 7. Rate limited and offline

- 429: "Too many attempts. Try again in 30 seconds", with the time from
  `Retry-After` counting down, and the other way when there is one ("Reset
  your password"). No scolding.
- Offline, for an installable app: the service worker precaches an offline
  page and serves it when a navigation fails (Workbox's `offlineFallback`
  recipe). It says the connection is gone, what still works (cached pages,
  drafts saved on the device), and retries when the `online` event fires.
  Inside the app, an offline banner rather than a page (`frontend-errors`).

## 8. Words and tone

- Plain and kind: what happened, whose side it is on, what to do now
  (`writing`). A joke only on a 404, and only if it does not replace the
  information.
- No "Oops" or "Uh-oh", no blame ("You typed the wrong address"), no dead
  ends: every error page offers at least two ways forward.
- No automatic redirect with a countdown; people read at their own pace
  (WCAG 2.2.1).
- Error pages are translated like every other page (`i18n`), the static 500
  included.

## 9. Phone and SEO

- On a phone: the same content in one column, the search full width, the
  links as a list with 44px targets, the header's menu still working.
- The right status on every error page, sent by the server and never cached
  by the CDN as a 200; `noindex` on error pages; error URLs never in the
  sitemap, moved pages out of it once they redirect.

## Check it

```sh
curl -s -o /dev/null -w "%{http_code}\n" https://example.test/no-such-page  # 404
curl -s -o /dev/null -w "%{http_code}\n" https://example.test/old-pricing   # 301
curl -sI https://example.test/ | grep -iE "^HTTP|^retry-after"              # 503 and Retry-After in maintenance
```

- Stop the app (or its database) and load a page: the static 500 or 503
  page appears, styled, without the app.
- `preview` at 360, 768 and 1440px on the 404: header and footer present,
  no dead links, the search works.
- An expired reset link offers a new one; a 403 names who can help; the
  offline page appears with the network off in DevTools.
- `ui_check` for "Oops", giant numbers and stock illustrations.

## Avoid

Soft 404s served with 200; every 404 redirected home; a giant number as the
only message; "Oops"; blaming the visitor; stack traces or internal names;
a 500 page that needs the database; no header or footer; a single "Go home"
button; jokes on server errors; redirect countdowns; maintenance served as
200; expired links that say only "Invalid token".
