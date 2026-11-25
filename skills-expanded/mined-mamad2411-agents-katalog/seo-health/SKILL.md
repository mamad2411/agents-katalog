---
name: seo-health
description: "Technical SEO monitoring. Weekly PageSpeed audits, Core Web Vitals tracking, crawl health checks, image optimization, and mobile usability. Catches problems before they tank your rankings."
metadata:
  openclaw:
    version: "1.0"
    author: "Matt Berman"
    emoji: "🏥"
    homepage: https://bigplayers.co
    user-invocable: true
    category: "seo"
    requires:
      env: []
      tools: ["curl", "jq"]
    optional_env:
      - PAGESPEED_API_KEY
---

# SEO Health — Technical SEO Monitoring

Rankings don't just depend on content and links. If your site is slow, broken, or has technical issues, Google will rank your competitors instead. This skill catches problems before they cost you traffic.

Three scripts. Run weekly. Takes 5 minutes.

---

## Scripts

### 1. `health-speed.sh` — PageSpeed + Core Web Vitals

Checks your site's performance using Google's PageSpeed Insights API (free, no key required for basic usage).

**Usage:**
```bash
bash skills/seo-health/scripts/health-speed.sh <url> [--mobile] [--desktop] [--both]
```

**What it checks:**
- **LCP** (Largest Contentful Paint) — should be < 2.5s
- **INP** (Interaction to Next Paint) — should be < 200ms
- **CLS** (Cumulative Layout Shift) — should be < 0.1
- **FCP** (First Contentful Paint) — should be < 1.8s
- **TTFB** (Time to First Byte) — should be < 800ms
- **Speed Index** — should be < 3.4s
- Overall performance score (0-100)

**Outputs:**
- Current scores vs thresholds (PASS/FAIL for each metric)
- Top 5 opportunities to improve (with estimated time savings)
- Comparison to previous run (if snapshot exists)
- Mobile vs desktop breakdown

**Runs against:** Google PageSpeed Insights API (free tier: 25,000 queries/day with API key, rate-limited without)

### 2. `health-crawl.sh` — Crawl Health Audit

Checks your site for common technical SEO issues.

**Usage:**
```bash
bash skills/seo-health/scripts/health-crawl.sh <domain> [--sitemap URL] [--limit 50]
```

**What it checks:**
- **Broken internal links** (404s within your site)
- **Redirect chains** (301 → 301 → 301 = slow)
- **Missing meta tags** (title, description, canonical)
- **Duplicate titles/descriptions** across pages
- **Missing alt text** on images
- **Non-HTTPS resources** (mixed content)
- **Orphan pages** (in sitemap but no internal links pointing to them)
- **robots.txt** validation
- **Sitemap** accessibility and format

**Outputs:**
- Issue count by severity (critical, warning, info)
- Specific URLs with each issue
- Fix suggestions for each type

### 3. `health-images.sh` — Image Optimization Audit

Checks images across your top pages for SEO and performance issues.

**Usage:**
```bash
bash skills/seo-health/scripts/health-images.sh <domain> [--pages 10]
```

**What it checks:**
- **Oversized images** (> 200KB without compression)
- **Wrong format** (should be WebP or AVIF, not PNG/BMP)
- **Missing alt text** (bad for SEO and accessibility)
- **Missing dimensions** (width/height attributes — causes CLS)
- **Lazy loading** (below-fold images should have loading="lazy")
- **Responsive images** (srcset for different screen sizes)

**Outputs:**
- Per-page image report
- Total potential size savings
- Priority fixes (biggest images first)

---

## Weekly Health Check Workflow

```
Monday:  health-speed.sh --both     → Check Core Web Vitals
         health-crawl.sh            → Find broken links and tech issues
         health-images.sh           → Flag image optimization opportunities
```

Run all three in one go. The agent reads the output, prioritizes fixes, and adds them to your task list.

---

## Snapshots and Trending

Each script saves a snapshot to `workspace/seo/health/`:
- `speed-YYYY-MM-DD.json` — PageSpeed scores over time
- `crawl-YYYY-MM-DD.json` — Issue counts over time
- `images-YYYY-MM-DD.json` — Image audit results

The agent compares to previous snapshots and flags:
- "LCP got 400ms worse since last week"
- "3 new broken links appeared"
- "You added 12 images without alt text this month"

Trending data is how you catch regressions early.

---

## Thresholds

| Metric | Good | Needs Work | Poor |
|--------|------|-----------|------|
| LCP | < 2.5s | 2.5-4.0s | > 4.0s |
| INP | < 200ms | 200-500ms | > 500ms |
| CLS | < 0.1 | 0.1-0.25 | > 0.25 |
| FCP | < 1.8s | 1.8-3.0s | > 3.0s |
| TTFB | < 800ms | 800-1800ms | > 1800ms |
| Performance Score | 90+ | 50-89 | < 50 |

---

## How This Connects to the Loop

SEO Agent finds keywords. SEO Forge writes content. SEO Links gets backlinks. SEO Health makes sure the technical foundation doesn't undermine all that work.

A page with perfect content and strong backlinks will still rank poorly if it takes 6 seconds to load or has broken internal links. This skill is the foundation everything else sits on.
