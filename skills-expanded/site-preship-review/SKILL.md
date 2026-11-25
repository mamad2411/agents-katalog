---
name: site-preship-review
audience: chrono
description: Use before publishing or relaunching any website — six parallel single-dimension reviewers (design, mobile, states, user flows, launch prep, security & infra) that render and look at every page, then one or two fix passes. Includes launch-readiness and rendered-page checks.
---

# Site pre-ship review

Six reviewers, one dimension each, run in parallel against a frozen branch of the site. Each renders every page and
LOOKS at it; none edits. Then a single fix worker applies every BLOCKER and MAJOR plus the quick MINORs, and a second
fix pass takes whatever reviews landed late. Idea credited to an @voxyz_ai post (five subagents, twenty checks); this is
our own checklist, tuned by what actually broke.

## Packet shape (shared by all six)

- Point at a branch, never a working tree: `git worktree add --detach /private/tmp/site-review-$RANDOM <branch>` and
  serve with `python3 -m http.server`.
- Render with Python Playwright launching its **own** headless Chromium at 1440x900 and 390x844 (plus 360/320 for
  headers). Never attach to the operator's browser.
- Give the reviewer the product facts the copy must match (prices, limits, chains, tagline) and a read-only pointer to
  the code that is the source of truth for them.
- Deliverable: numbered findings for that dimension only (page + element + screenshot path + BLOCKER/MAJOR/MINOR +
  exact fix), then PASS/FAIL per checklist item. Screenshots go OUTSIDE the repo; a worker that commits them to the
  site repo gets its whole commit refused at integration.

## The six checklists

1. **Design** — one type scale and casing; consistent spacing grid; brand identical on every page; WCAG AA contrast and
   an obvious primary call to action on every page, mobile included.
2. **Mobile** (390 and 360) — no horizontal scroll (long addresses/code wrap inside their box); tap targets >= 44 px;
   menu opens, closes, every item works; body text >= 16 px, nothing clipped.
3. **States** — every form's empty/invalid/success/failure states, with the network request intercepted (never send a
   real message); 404; copy-button feedback, hover/focus/disabled, visible keyboard focus; no console errors; works
   with JS disabled or slow.
4. **User flows** — the five-second test, then Get Started → install → first action, checked against the real code;
   pricing → start; every internal link and anchor resolves; legal and support reachable from every footer.
5. **Launch prep** — unique title, description, canonical, og:* (1200x630 image that exists), twitter:card on every
   page; favicon, robots.txt, sitemap.xml; no placeholder/TODO/staging/testnet copy or internal paths/IDs; page weight
   and render-blocking assets.

6. **Security & infra** (added from a cited research pass) — secret scan of the
   BUILD OUTPUT and client bundles (`gitleaks dir <dist> --no-git`, grep `sk-`, `ghp_`, `AIza`, `service_role`,
   `NEXT_PUBLIC_`/`VITE_` leaks); security headers via `curl -sI -L` (HSTS, nosniff, frame-options, a CSP that works);
   all four host variants (http/https × apex/www) 301 once to the canonical HTTPS host and the cert SAN covers both;
   backend row-level security / unauthenticated access tested where a database backs the site.

Add to the existing five, all cheap and automatable: `npx @axe-core/cli <url> --tags wcag2a,wcag2aa` (design);
Playwright **WebKit** render plus `100dvh` checks (mobile); honeypot + burst-rate-limit probe on forms, custom 500
page (states); `npx linkinator <url> --recurse` and a cross-page fact-consistency check on prices/limits (flows);
`robots.txt` has no `Disallow: /`, no `X-Robots-Tag: noindex`, og:image is PNG/JPEG not SVG, Lighthouse LCP <= 2.5 s
and CLS <= 0.1, and a grep for AI boilerplate (`Lorem`, `John Doe`, `Company Name`, `555-01`) (launch prep). AI-built
sites specifically: hallucinated links, fake stats/testimonials, and facts that disagree between pages.

## Routing notes (measured)

- The Codex board lane could not launch Chromium in its sandbox (Mach port `Permission denied (1100)`); a reviewer
  there sees nothing. Route visual reviewers to lanes that rendered: Gemini (`accessibility-engineer`,
  `growth-and-search-analyst`, `vega`) and Claude (`frontend-engineer`). `frontend-engineer` has no Gemini adapter.
- Findings the operator owns (legal entity, release credentials) go to the operator as one question; everything else
  the fix pass just does.
- Legal/credential placeholders and launch-day copy (e.g. "testnet beta") are the usual BLOCKERs — tell the fix worker
  the launch-day facts explicitly.
