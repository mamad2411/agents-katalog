---
name: landing
description: Landing page conversion specialist. Audits every section of a marketing or product landing page — hero, social proof, features, pricing, CTAs — for conversion friction, structural weakness, and performance issues. Fixes section order, CTA hierarchy, trust signals, and load time. Verifies every change at both desktop and mobile. Use when user wants to improve landing page conversions, audit a marketing page, or invokes /landing.
---

# /landing — Landing Page Conversion

Systematically finds and fixes every conversion killer on a landing page. Works above the fold first, then section by section, verifying visually at each step.

Conversion principles and section formulas: [CONVERSION.md](CONVERSION.md)

If a `DESIGN-BRIEF.md` exists in the project root: read it before starting. The brief's **Brand personality**, **Emotional goal**, and **Visual references** fields tell you the tone and visual register the landing page must hit. The **Defining screen** field tells you whether the landing page is the top priority.

---

## Phase 0 — Environment Setup

### 0a. Check / start dev server
```bash
curl -s --max-time 2 -o /dev/null -w "%{http_code}" http://localhost:3000
```
If not `200`, find and start the dev command, then wait:
```bash
until curl -s --max-time 2 http://localhost:3000 > /dev/null 2>&1; do sleep 1; done && echo "ready"
```

### 0b. Find the landing page
```bash
# App Router
find . -path "*/app/page.tsx" -not -path "*/node_modules/*"

# Pages Router
find . -path "*/pages/index.tsx" -not -path "*/node_modules/*"

# Marketing subdirectory
find . -name "page.tsx" -path "*/marketing/*" -o -name "page.tsx" -path "*/landing/*" | grep -v node_modules
```

Read the landing page file and any layout wrappers. Note every section component imported.

### 0c. Write the landing page scripts
Write both to the **project root** (needs node_modules). Deleted in Phase 4.

**`_landing_screenshot.mjs`** — full-page and above-fold screenshots:
```js
import { chromium } from '@playwright/test';
import { mkdirSync } from 'fs';

const get = (f) => { const i = process.argv.indexOf(f); return i !== -1 ? process.argv[i+1] : null; };
const url    = get('--url')    ?? 'http://localhost:3000';
const name   = get('--name')   ?? 'landing';
const width  = parseInt(get('--width')  ?? '1280');
const height = parseInt(get('--height') ?? '900');
const auth   = get('--auth');

mkdirSync('/tmp/landing', { recursive: true });

const browser = await chromium.launch();
const context = await browser.newContext({
  viewport: { width, height },
  ...(auth ? { storageState: auth } : {}),
});
const page = await context.newPage();
try {
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
} catch {
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
}

// Above-fold screenshot (viewport only — no scroll)
await page.screenshot({ path: `/tmp/landing/${name}-above-fold.png`, fullPage: false });

// Full-page screenshot
await page.screenshot({ path: `/tmp/landing/${name}-full.png`, fullPage: true });

await browser.close();
console.log(`above-fold: /tmp/landing/${name}-above-fold.png`);
console.log(`full-page:  /tmp/landing/${name}-full.png`);
```

**`_landing_audit.mjs`** — programmatic conversion checks:
```js
import { chromium } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'fs';

const get = (f) => { const i = process.argv.indexOf(f); return i !== -1 ? process.argv[i+1] : null; };
const url    = get('--url')    ?? 'http://localhost:3000';
const name   = get('--name')   ?? 'landing';
const width  = parseInt(get('--width')  ?? '1280');
const height = parseInt(get('--height') ?? '900');
const auth   = get('--auth');

mkdirSync('/tmp/landing', { recursive: true });

const browser = await chromium.launch();
const context = await browser.newContext({
  viewport: { width, height },
  ...(auth ? { storageState: auth } : {}),
});
const page = await context.newPage();
try {
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
} catch {
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
}

const audit = await page.evaluate((viewportHeight) => {
  const vp = viewportHeight;

  // ── CTA check ────────────────────────────────────────────────
  const allButtons  = [...document.querySelectorAll('a[href], button')];
  const aboveFoldEl = allButtons.filter(el => {
    const r = el.getBoundingClientRect();
    return r.top >= 0 && r.bottom <= vp && r.width > 0;
  });

  // Primary CTA detection: text match first, then fall back to visual prominence
  // (largest button by area, or highest contrast background vs page bg)
  const textMatchCTA = aboveFoldEl.find(el =>
    /sign up|get started|start|try|join|buy|get|download|book|request|build|ship|create|launch/i.test(el.textContent ?? '')
  );
  const prominentCTA = aboveFoldEl
    .filter(el => el.tagName === 'A' || el.tagName === 'BUTTON')
    .sort((a, b) => {
      const ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect();
      return (rb.width * rb.height) - (ra.width * ra.height); // largest area first
    })[0];
  const primaryCTA = textMatchCTA ?? prominentCTA ?? null;

  // ── Heading structure ─────────────────────────────────────────
  const h1s = [...document.querySelectorAll('h1')].map(el => el.textContent?.trim());
  const h2s = [...document.querySelectorAll('h2')].map(el => el.textContent?.trim());

  // ── Social proof above fold ───────────────────────────────────
  const socialProofKeywords = /\d[\d,]+\s*(users?|customers?|teams?|companies|reviews?|stars?)|trusted by|used by|\d+\s*%/i;
  const aboveFoldText = document.body.innerText.slice(0, 2000);
  const hasSocialProofAboveFold = socialProofKeywords.test(aboveFoldText);

  // ── Navigation link count ─────────────────────────────────────
  const navLinks = [...document.querySelectorAll('nav a, header a')].length;

  // ── Images ───────────────────────────────────────────────────
  const heroImg = document.querySelector('img, video');
  const heroImgSrc = heroImg?.getAttribute('src') ?? null;
  const heroImgLoading = heroImg?.getAttribute('loading') ?? null;

  // ── Page weight signals ───────────────────────────────────────
  const timing = performance.getEntriesByType('navigation')[0];
  const loadTime = timing ? Math.round(timing.loadEventEnd - timing.startTime) : null;
  const domContentLoaded = timing ? Math.round(timing.domContentLoadedEventEnd - timing.startTime) : null;

  // ── LCP candidate ─────────────────────────────────────────────
  const lcpEntries = performance.getEntriesByType('largest-contentful-paint');
  const lcp = lcpEntries.length ? Math.round(lcpEntries.at(-1).startTime) : null;

  // ── OG / social meta tags ─────────────────────────────────────
  const ogTitle       = document.querySelector('meta[property="og:title"]')?.getAttribute('content') ?? null;
  const ogDescription = document.querySelector('meta[property="og:description"]')?.getAttribute('content') ?? null;
  const ogImage       = document.querySelector('meta[property="og:image"]')?.getAttribute('content') ?? null;
  const twitterCard   = document.querySelector('meta[name="twitter:card"]')?.getAttribute('content') ?? null;
  const metaDesc      = document.querySelector('meta[name="description"]')?.getAttribute('content') ?? null;

  // ── Scroll-depth CTA coverage ─────────────────────────────────
  // Divide page into quartiles. Check each for a visible CTA.
  const pageHeight = document.documentElement.scrollHeight;
  const ctaEls = [...document.querySelectorAll('a[href], button')].filter(el => {
    const s = getComputedStyle(el);
    return s.display !== 'none' && s.visibility !== 'hidden' && el.getBoundingClientRect().width > 0;
  });
  const ctaQuartiles = [0.25, 0.5, 0.75, 1.0].map(pct => {
    const threshold = pageHeight * pct;
    return ctaEls.some(el => {
      const r = el.getBoundingClientRect();
      // getBoundingClientRect is relative to viewport; offset by scrollY gives absolute position
      const absTop = r.top + window.scrollY;
      return absTop <= threshold;
    });
  });
  // ctaQuartiles[i] === true means a CTA exists within the first (i+1)*25% of the page

  return {
    cta: {
      primaryCTAAboveFold:  !!primaryCTA,
      primaryCTAText:       primaryCTA?.textContent?.trim() ?? null,
      detectedBy:           textMatchCTA ? 'text-match' : (prominentCTA ? 'prominence' : 'none'),
      aboveFoldButtonCount: aboveFoldEl.length,
      ctaCoverageByQuartile: {
        top25pct: ctaQuartiles[0],
        top50pct: ctaQuartiles[1],
        top75pct: ctaQuartiles[2],
        top100pct: ctaQuartiles[3],
      },
    },
    headings: { h1s, h2s },
    socialProof: { hasSocialProofAboveFold },
    nav: { linkCount: navLinks },
    hero: { imgSrc: heroImgSrc, imgLoading: heroImgLoading },
    performance: { loadTime, domContentLoaded, lcp },
    meta: { ogTitle, ogDescription, ogImage, twitterCard, metaDesc },
  };
}, height);

writeFileSync(`/tmp/landing/${name}-audit.json`, JSON.stringify(audit, null, 2));
await browser.close();

console.log(JSON.stringify(audit, null, 2));
```

**Usage:**
```bash
# Desktop
node _landing_screenshot.mjs --url http://localhost:3000 --name home-desktop
node _landing_audit.mjs --url http://localhost:3000 --name home-desktop

# Mobile
node _landing_screenshot.mjs --url http://localhost:3000 --name home-mobile --width 375 --height 812
node _landing_audit.mjs --url http://localhost:3000 --name home-mobile --width 375 --height 812
```

**After every screenshot: use the `Read` tool on both images (above-fold and full-page).**

---

## Phase 1 — Landing Page Audit

### 1a. Run the programmatic audit
```bash
node _landing_audit.mjs --url http://localhost:3000 --name desktop
node _landing_audit.mjs --url http://localhost:3000 --name mobile --width 375 --height 812
```
Read both JSON reports. Flag any of these immediately:
- `primaryCTAAboveFold: false` — **critical**: visitor can't act without scrolling
- `detectedBy: "none"` — **critical**: no interactive element found above fold at all
- `h1s.length > 1` — **major**: two h1s compete for attention
- `h1s.length === 0` — **critical**: no clear headline
- `hasSocialProofAboveFold: false` — **major**: trust not established before CTA
- `lcp > 2500` — **major**: page loads too slowly (Google's "good" threshold)
- `navLinks > 5` — **moderate**: nav distracts from the single goal
- `ogTitle: null` — **major**: social shares show no title (kills click-through from social)
- `ogImage: null` — **major**: social shares show no preview image
- `ogDescription: null` — **moderate**: social shares show no description
- `ctaCoverageByQuartile.top75pct: false` — **major**: a visitor who reads 75% of the page has no CTA in reach
- `ctaCoverageByQuartile.top100pct: false` — **critical**: no final CTA before footer

### 1b. Screenshot the landing page
```bash
node _landing_screenshot.mjs --url http://localhost:3000 --name desktop
node _landing_screenshot.mjs --url http://localhost:3000 --name mobile --width 375 --height 812
```
**Read all 4 images** (desktop above-fold, desktop full, mobile above-fold, mobile full).

Apply the **5-second test** to the above-fold screenshot: look at it for 5 seconds, then answer:
1. What is this product?
2. Who is it for?
3. What do I do next?

If any answer is unclear → the above-fold has a critical problem.

### 1c. Read the page structure
Read the landing page file and all imported section components. Map the actual section order:

```
[ ] Hero / above fold
[ ] Social proof / logos
[ ] Problem / pain
[ ] Solution / how it works
[ ] Features / benefits
[ ] Testimonials
[ ] Pricing
[ ] FAQ
[ ] Final CTA
[ ] Footer
```

For each section, note:
- What heading it uses (h2, h3)
- What the primary CTA text is (if any)
- Whether it matches [CONVERSION.md](CONVERSION.md) formula

### 1d. Check performance signals
```bash
# Bundle size signals
find . -name "*.js" -path "*/_next/static/chunks/*" -not -path "*/node_modules/*" \
  | xargs wc -c 2>/dev/null | sort -rn | head -10

# Images without optimization
grep -rn "<img" . --include="*.tsx" -not -path "*/node_modules/*" | grep -v "next/image\|Image from"

# Unoptimized hero image (loading=lazy above fold is a performance bug)
grep -rn "loading.*lazy" . --include="*.tsx" --include="*.html" -not -path "*/node_modules/*" | head -10
```

LCP target: < 2.5s. Flag anything that delays it:
- Hero image not using `<Image>` (Next.js) or `loading="eager"` / `fetchpriority="high"`
- Large JS bundles blocking render
- Web fonts without `display=swap`

Present the full audit findings before continuing.

---

## Phase 2 — Priority Ranking

Score each issue:

| Issue | Points |
|-------|--------|
| No primary CTA above the fold | +5 |
| 5-second test fails (unclear value prop) | +5 |
| LCP > 2.5s | +4 |
| No h1 or two competing h1s | +4 |
| Social proof absent from above fold | +3 |
| Hero image lazy-loaded (blocks LCP) | +3 |
| Navigation has >5 links (distraction) | +3 |
| Section order wrong (pricing before proof) | +2 |
| Multiple primary CTAs competing | +2 |
| CTA copy is generic ("Submit", "Learn more") | +2 |
| Missing trust signals (no logos, no reviews) | +2 |
| Testimonials anonymous or missing names | +1 |
| FAQ missing | +1 |
| No final CTA before footer | +1 |

Work highest score first. Ask user to confirm before Phase 3.

---

## Phase 3 — Recursive Fix Loop

Work through issues in ranked order. Maximum **3 iterations per section**.

### 3a. Screenshot before
Take above-fold and full-page screenshots for the current section's context.
**Read both.** Describe what the conversion problem looks like in the rendered UI.

### 3b. Analyse
Read the section component file. Apply rules from [CONVERSION.md](CONVERSION.md). Categorise:

- **Critical** — blocks conversion entirely (no CTA, page doesn't load)
- **Major** — measurably hurts conversion (wrong section order, no social proof above fold)
- **Minor** — optimisation (better CTA copy, stronger headline)

### 3c. Fix

Apply fixes automatically — no permission needed:

**Above fold:**
```
Value proposition: headline must answer "what is it + who is it for" in one sentence.
  Bad:  "The Future of Work"
  Good: "Project management for remote engineering teams"

CTA: must be visible without scrolling. Move it up, or shorten content above it.
CTA copy: verb-first + benefit (from /copy PRINCIPLES.md rules).
Social proof: add one number or logo row immediately below the CTA.
  Format: "Trusted by 10,000+ developers at [Logo] [Logo] [Logo]"
```

**Section order:**
```
Correct order (from CONVERSION.md):
  1. Hero — value prop + CTA
  2. Social proof — logos or numbers (trust, immediately after CTA)
  3. Problem — "you know this pain"
  4. Solution — "here's the better way"
  5. Features — the specifics
  6. Testimonials — social proof with names and faces
  7. Pricing — after they're sold on value
  8. FAQ — handles objections
  9. Final CTA — close again
```

**Navigation:**
```
Landing pages should have minimal nav. For dedicated landing pages:
  Remove nav entirely, or collapse to logo + single CTA
  Never link away to docs, blog, or other pages from a conversion landing page
  Nav links = exits. Every exit is a lost conversion.
```

**Performance:**
```tsx
// Hero image — eager load, high priority (never lazy above fold)
<Image
  src="/hero.png"
  alt="..."
  priority          // Next.js: adds fetchpriority="high" + preload
  loading="eager"   // belt-and-suspenders
/>

// Web font — add to <head>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preload" as="font" href="/fonts/inter.woff2" type="font/woff2" crossOrigin="anonymous" />
```

**OG / social meta tags (in Next.js App Router):**
```tsx
// app/layout.tsx or app/page.tsx
export const metadata: Metadata = {
  title:       'Ship UI in minutes, not days — ParticleUI',
  description: '200+ production-ready components. Copy, paste, done.',
  openGraph: {
    title:       'Ship UI in minutes, not days',
    description: '200+ production-ready components. Copy, paste, done.',
    images: [{ url: '/og-image.png', width: 1200, height: 630 }],
    type: 'website',
  },
  twitter: {
    card:        'summary_large_image',
    title:       'Ship UI in minutes, not days',
    description: '200+ production-ready components. Copy, paste, done.',
    images:      ['/og-image.png'],
  },
};
```

**OG image rules:**
- 1200×630px minimum (Twitter requires ≥600px wide)
- Shows the product UI, not just a logo on a solid color
- Text is readable at thumbnail size (48px+ font size)
- Contrasting background (white text on dark, or dark text on light)
- Save as PNG or JPG under 5MB

**Trust signals:**
```
Security: "256-bit SSL", "SOC 2 certified", "GDPR compliant"
Guarantees: "30-day money-back guarantee", "No credit card required"
Reviews: star rating + count ("4.9 stars · 2,400 reviews")
Named testimonials: name + title + company + photo (anonymous = 60% less credible)
```

### 3d. Screenshot after
```bash
sleep 3  # hot reload
node _landing_screenshot.mjs --url http://localhost:3000 --name desktop-after
node _landing_screenshot.mjs --url http://localhost:3000 --name mobile-after --width 375 --height 812
node _landing_audit.mjs --url http://localhost:3000 --name desktop-after
```
**Read all images and the new audit JSON.**

Apply the 5-second test again to the above-fold screenshot. Is the value prop clear now?

Verify:
1. Primary CTA visible above fold on desktop?
2. Primary CTA visible above fold on mobile (375px)?
3. `primaryCTAAboveFold: true` in audit JSON?
4. Social proof present before the first scroll?
5. LCP improved if performance fixes were applied?

If any fail: go back to 3c (increment iteration, max 3).

### 3e. Conversion checklist
Before marking the landing page done:

- [ ] 5-second test passes — value prop clear in above-fold screenshot without reading
- [ ] One h1 that answers "what + who"
- [ ] Primary CTA above the fold on desktop (1280px)
- [ ] Primary CTA above the fold on mobile (375px)
- [ ] CTA copy is verb-first + benefit (not "Submit" or "Learn more")
- [ ] Social proof (number or logo row) visible above fold or immediately after CTA
- [ ] Section order: hero → proof → problem → solution → features → testimonials → pricing → FAQ → final CTA
- [ ] No more than one primary CTA per section (secondary CTAs should be visually subordinate)
- [ ] Testimonials have name, title, company (not anonymous)
- [ ] Hero image loads eagerly with priority (not lazy)
- [ ] LCP < 2.5s (from audit JSON)
- [ ] Navigation minimal — no links that lead users away from conversion goal
- [ ] Trust signals present (security badge, guarantee, or review count)
- [ ] Final CTA before footer repeats the above-fold CTA offer
- [ ] `ctaCoverageByQuartile.top75pct: true` — CTA within reach at 75% scroll
- [ ] `ctaCoverageByQuartile.top100pct: true` — CTA within reach at bottom of page
- [ ] `og:title` set — matches the hero headline, ≤60 characters
- [ ] `og:description` set — one sentence value prop, ≤155 characters
- [ ] `og:image` set — 1200×630px, shows the product or key visual (not the logo alone)
- [ ] `twitter:card` set to `summary_large_image`
- [ ] `meta[name="description"]` set — same as og:description or variant
- [ ] Mobile layout: CTA not hidden below fold, text not truncated, tap targets ≥44px

Any fail → go back to 3c. After iteration 3: flag and advance.

---

## Phase 4 — Cleanup & Report

Delete temp scripts:
```bash
rm -f _landing_screenshot.mjs _landing_audit.mjs
```

Final report:

```
5-second test: pass / fail
Primary CTA above fold (desktop): ✓ / ✗
Primary CTA above fold (mobile):  ✓ / ✗
LCP: Xms (target <2500ms)
Social proof above fold: ✓ / ✗
Section order correct: ✓ / ✗
```

| Issue | Severity | Fixed | Iterations |
|-------|----------|-------|------------|
| ...   | ...      | ✓ / ⚠ | ...       |

List all flagged issues at the bottom.

---

## Rules

1. **Above fold first, always.** Nothing matters if visitors don't see the value before they scroll.
2. **5-second test is the pass/fail.** If a stranger can't identify the product and the next step in 5 seconds, it's broken.
3. **One primary CTA per viewport.** Multiple primary CTAs cancel each other out.
4. **Social proof before scroll.** Trust must be established before asking for action.
5. **Section order is the sales argument.** You wouldn't quote a price before demonstrating value.
6. **Navigation is the enemy of conversion.** Every link out is a lost conversion on a dedicated landing page.
7. **Performance is conversion.** A 1-second delay costs ~7% conversions. LCP is the metric.
8. **Mobile is primary.** Most landing page traffic is mobile. Fix mobile first, then verify desktop.
9. **Max 3 iterations.** Flag and move on.
10. **Never change logic, routing, or data fetching.** Only content, order, copy, and visual treatment.

---

See [CONVERSION.md](CONVERSION.md) for section formulas, CTA patterns, social proof templates, and trust signal hierarchy.
