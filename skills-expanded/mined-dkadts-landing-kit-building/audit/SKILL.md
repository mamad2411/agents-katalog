---
name: audit
description: Pre-ship checklist. Anti-AI-slop, hardcode, perf, a11y, SEO, security, contract, mobile, typography, and references-compliance checks. Report pass/fail. Blocks /deploy on any blocking failure.
---

# /audit

Final verifier before `/deploy`. Categories: **anti-slop** (what killed prior projects), **technique** (perf, a11y, SEO), **contract** (matches DESIGN-LOCK, brief, and the approved manifest).

## When to use

- After `/build` + `/mobile` (site assembled).
- Before `/deploy` (required gate).
- Regularly during development for sanity checks.

## Check categories

### A. Anti-AI-slop (DESIGN-LOCK enforcement)

Walk HTML/CSS/JS. Each check = pass / fail with file/line.

- [ ] **Emoji in HTML** — grep `[\u{1F300}-\u{1F9FF}]` in HTML. Fail if found (unless emoji is in the brand book).
- [ ] **More than one gradient** — grep `linear-gradient|radial-gradient|conic-gradient`. Fail if > 1 unique.
- [ ] **More than one radius** — grep all `border-radius:`. Everything must be `var(--radius)`. Fail on hardcode.
- [ ] **More than 2 font-weights** — grep `font-weight:`. Fail if > 2 unique values project-wide.
- [ ] **Center-align > 50%** — count sections with `text-align: center` vs total. Warning if > 50%.
- [ ] **More than 5 section types** — count unique `<section class="sec sec-...">`. Fail if > 5 (see DESIGN-LOCK §8).
- [ ] **Decorative icons** — visually check: icons purely for decoration? Warning.
- [ ] **Bounce/spring motion** — grep `cubic-bezier` for out-of-range values (>1 or <0). Fail if found and not allowed in DESIGN-LOCK.
- [ ] **Mixed icon libraries** — > 1 SVG sprite or > 1 icon font. Fail.
- [ ] **Pill everywhere** — if DESIGN-LOCK radius ≠ 999 but `border-radius: 999px` present — Fail.

### A2. Typography (English print-quality rules)

- [ ] **Hanging short words at line end** — grep the rendered HTML for space-separated short words at potential line breaks. Specifically: scan each text node for space-terminated sequences ending in words from the `/typography` canonical short-word list (`a`, `an`, `the`, `and`, `or`, `but`, `of`, `to`, `in`, `on`, `for`, `with`, `is`, `are`, `be`, `it`, `we`, `you`, etc.). If the space is a regular space (not `&nbsp;`) and the next word exists, this is a violation. Fail with line reference.
- [ ] **Dashes at line end** — grep for ` [-–—] ` (space, dash, space). If the space before the dash is a regular space (not `&nbsp;`), this is a violation. Fail.
- [ ] **Orphans in headings and paragraphs** — for each `<h1>`, `<h2>`, `<h3>`, `<p>`, `<li>`, `<blockquote>`, verify the last two words are joined by `&nbsp;`. Fail if a regular space separates the last two words of a text node.
- [ ] **Language contract** — if `<html lang="en">` is not set, and the copy is English, fail the language attribute check (also caught in D). Typography rules only apply to English.
- [ ] **`no-typo` opt-outs** — count elements with `class="no-typo"`. Warning if > 3 (user disabled typography on many blocks — worth reviewing).

### B. Hardcode (tokens.css enforcement)

- [ ] **Hex colors in CSS outside tokens.css** — grep `#[0-9a-f]{3,8}` in `site/css/*.css` except `tokens.css`. Fail.
- [ ] **rgb/rgba in CSS outside tokens.css and outside `var(--c-overlay)`** — grep `rgba?\(`. Fail on each.
- [ ] **Hardcoded px (except 1px border)** — grep `\d+px` except `1px solid`. Fail.
- [ ] **Hardcoded ms/s** — grep `\d+(ms|s)\b` in CSS outside tokens. Fail.
- [ ] **Hardcoded cubic-bezier** in CSS/JS outside tokens.css. Fail.
- [ ] **Inline styles** — grep `style="..."` in HTML. Fail.
- [ ] **!important** — grep. Fail (except `responsive.css` mobile parallax kill — allowed there).

### C. Perf

- [ ] **HTML size** — `wc -c index.html` — target ≤ 100KB post-build (without inline SVG).
- [ ] **Total CSS size** — sum all CSS — target ≤ 50KB.
- [ ] **Total JS size** — target ≤ 50KB (excluding external analytics).
- [ ] **Media sizes** — every `.webp` under 500KB (special cases aside); `.mp4` under 3MB.
- [ ] **Preload on hero** — `<link rel="preload" as="image" href="/media/hero.webp">` in head. Fail if missing.
- [ ] **font-display: swap** — on every @font-face. Fail.
- [ ] **loading="lazy"** on every img outside hero. Warning if missing.
- [ ] **decoding="async"** on every img. Warning if missing.
- [ ] **Cache headers** — vercel.json contains immutable for media. Fail if missing.

### D. A11y

- [ ] **Alt on every img** — grep `<img` without `alt=`. Fail per instance.
- [ ] **Aria-label on textless buttons** — burger, close, prev/next carousel. Fail.
- [ ] **Label on every input** — not just placeholder. Fail.
- [ ] **Contrast text/background** — run WCAG formula; ≥ 4.5:1 (AA). Fail.
- [ ] **Keyboard navigation** — every interactive element reachable via Tab. Manual check.
- [ ] **Focus visible** — CSS `:focus-visible` defined. Warning if missing.
- [ ] **prefers-reduced-motion** — @media rule present. Fail if missing and animations exist.
- [ ] **Skip-link** — `<a href="#main">Skip to content</a>` first in body. Warning.
- [ ] **Lang attribute** — `<html lang="en">` or other. Fail if missing.

### E. SEO

- [ ] **Title** — not "TBD", not empty, ≤ 60 chars. Fail.
- [ ] **Meta description** — not empty, 120–160 chars. Fail.
- [ ] **OG tags** — og:title, og:description, og:image, og:url. Fail on missing.
- [ ] **OG image** — 1200×630, ≤ 300KB. Fail.
- [ ] **Twitter card** — `<meta name="twitter:card" content="summary_large_image">`. Warning.
- [ ] **Canonical** — `<link rel="canonical" href="https://...">`. Warning.
- [ ] **Robots** — if /thank-you exists — must be noindex. Warning.
- [ ] **Sitemap.xml** — exists. Warning.
- [ ] **One H1 per page** — grep `<h1`. Fail if > 1.

### F. Security

- [ ] **Vercel headers** — X-Frame-Options, X-Content-Type-Options, Referrer-Policy set. Fail if missing.
- [ ] **HTTPS-only links** — grep `http://` in HTML. Fail per instance (except localhost, mailto:, tel:).
- [ ] **External links rel** — every `<a target="_blank">` has `rel="noopener noreferrer"`. Fail.
- [ ] **No inline event handlers** — grep `onclick=|onload=` in HTML. Fail.
- [ ] **No secrets** — grep `api_key|secret|password|token=` in HTML/JS. Fail.
- [ ] **Secret storage documented** — verify `site/_deploy-log.md` or `brief/06-technical.md` names where sensitive keys live (Vercel env / GCP Secret Manager / other). Warning if undocumented.

### G. Contract (matches brief)

- [ ] Every section from `brief/copy-analysis.md` → structure present? Fail on omission.
- [ ] Every interactive block from `brief/07-interactive.md [x]` implemented? Fail on omission.
- [ ] CTA button matches `brief/03-goals.md`? Fail.
- [ ] Contacts in footer from `brief/01-business.md` → contacts? Fail.
- [ ] Analytics IDs from `brief/06-technical.md` wired? Fail.
- [ ] Privacy Policy page exists if applicable (see `brief/blocks/legal-privacy.md`)? Fail.

### H. Mobile

- [ ] Viewport meta present. Fail.
- [ ] Emulate 375×667, 390×844, 414×896 — visual smoke test. Warning on any breakage.
- [ ] Cache-bust `?v=N` on every CSS/JS link. Fail.
- [ ] Tap-target size ≥ 44px on every interactive. Fail.
- [ ] `site/_mobile-check-report.md` exists and its verdict is OK (produced by `/mobile` Step 7). Fail if missing or FAIL verdict.

### I. References compliance (approved-manifest enforcement)

- [ ] **Manifest exists** — `references/approved-manifest.md` present. Fail if missing.
- [ ] **All items checked** — every `[ ]` in the manifest must be `[x]` by the end of `/build`. For each unchecked item, fail with a citation showing which reference source expected it.
- [ ] **Manifest not empty (advisory)** — if the manifest has zero items even though `references/` had files, warning: probably a `/refs` skip.
- [ ] **Removed items logged** — any item that was in the manifest historically but is now absent must have a corresponding decision-log entry in `DESIGN.md` explaining why. Fail on silent drops (compare against git history if available; otherwise warn).

## Report format

`site/_audit-report.md`:

```markdown
# Audit report — 2026-08-08 15:30

## Summary
- ✅ Passed:      56
- ⚠️ Warnings:    3
- ❌ Failed:      2

## ❌ Blocking fails (must fix before /deploy)

1. **B — Hardcoded hex** — site/css/hero.css:23 `#0A0A0A` not in tokens.css
2. **I — References compliance** — approved-manifest item unmet:
   `[ ] motif: horizontal thin rule between sections  ← ref: mood/aesop`
   Expected in: sections separator layer. Not found.

## ⚠️ Warnings (non-blocking, discuss)

1. **A — Center-align** — 3 of 5 sections centered — risk of flatness. Keep?
2. **D — Focus visible** — :focus-visible not defined in CSS
3. **E — Sitemap.xml** — missing

## ✅ Passed
- 56 checks passed. Full list in _audit-full.md.

## Verdict
❌ /deploy blocked. Fix fails and rerun /audit.
```

## Rules of behavior

- **Do not "improve" found problems automatically.** Report to user, let them decide.
- **Fail = strict.** Warning = soft.
- **Always cite file/line.** Without it, the user wastes time searching.
- **Deep check once per project.** Quick check for frequent runs — modified sections only.

## What NOT to do

- Do not run `/deploy` if there are fails.
- Do not rewrite code for the user (dev feedback loop).
- Do not skip a category — always run all of A through I.

## Next

- Fix fails → rerun `/audit`.
- Everything pass → `/deploy`.
