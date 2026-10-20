---
name: publicist-us-local-seo
description: Use when improving search visibility for US earned media or configuring a publisher's Google News, local search, or Discover presence. Covers NewsArticle data, Publisher Center, and Core Web Vitals.
license: MIT
metadata:
  version: "0.1.0"
  author: "shy-tangerine"
---

# US local SEO / Google News optimization, US market

Use this guide to improve search visibility for US earned media. Pair it with `publicist-us` and `publicist-us-regional-media`.

---

## Why local SEO matters for PR

| Stat | Impact |
|---|---|
| **Google News referral** | 20-40% of news site traffic |
| **Google Discover** | 30%+ of mobile news consumption |
| **Local pack (map pack)** | 46% of searches have local intent |
| **Earned media half-life** | 2-3 days without SEO; weeks with |

For each placement, check whether the outlet can use the supplied headline, image, author, and structured data to improve search visibility.

---

## Google News and Publisher Center

### Publisher Center setup (one-time)
1. **Verify ownership** in Google Search Console
2. **Submit publication** in Publisher Center (`news.google.com/publisher`)
3. **Configure sections**. Top stories, Local, Business, Tech, etc.
4. **Set up feeds**. RSS/Atom for each section
5. **Configure branding**. Logo, favicon, publication name
6. **Set crawl frequency**. "As fast as possible"

Setup is complete when ownership, publication details, sections, feeds, branding, and crawl frequency are configured.

### Article-level requirements (must-have)
| Element | Requirement |
|---|---|
| **Headline** | < 110 chars, keyword-rich, no clickbait |
| **Date** | `datePublished` + `dateModified` (ISO 8601) |
| **Author** | `author` with `url` + `sameAs` (LinkedIn/Twitter) |
| **Publisher** | `publisher` with `name`, `logo`, `url` |
| **Images** | `image` array: 1200x630 min, 16:9, caption + credit |
| **Video** | `video` object with `contentUrl`, `embedUrl`, `duration` |
| **ArticleBody** | Full text in `articleBody` (not truncated) |
| **Section** | `articleSection` (e.g., "Business", "Technology") |
| **Tags** | `keywords` array (5-10 relevant tags) |

### Structured data (NewsArticle schema)
```json
{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "Exact headline from article",
  "datePublished": "2024-01-15T10:30:00-05:00",
  "dateModified": "2024-01-15T14:22:00-05:00",
  "author": [{
    "@type": "Person",
    "name": "Jane Reporter",
    "url": "https://outlet.com/author/jane-reporter",
    "sameAs": ["https://linkedin.com/in/janereporter", "https://twitter.com/janereporter"]
  }],
  "publisher": {
    "@type": "Organization",
    "name": "Outlet Name",
    "logo": {"@type": "ImageObject", "url": "https://outlet.com/logo.png"},
    "url": "https://outlet.com"
  },
  "image": ["https://outlet.com/img/hero-1200x630.jpg"],
  "video": {"@type": "VideoObject", "contentUrl": "https://outlet.com/video.mp4"},
  "articleSection": "Technology",
  "keywords": ["AI", "enterprise", "funding", "San Francisco"],
  "articleBody": "Full article text here..."
}
```

### Publisher Center feed requirements
| Feed Type | Format | Frequency | Fields |
|---|---|---|---|
| **RSS 2.0** | XML | Real-time | title, link, pubDate, description, media:content |
| **Atom 1.0** | XML | Real-time | title, link, updated, content, media:thumbnail |
| **Google News Sitemap** | XML | Daily | news:news, news:publication, news:title, news:publication_date |

---

## Local pack and Google Maps optimization

### Google Business Profile (GBP) for earned media
| Element | Optimization |
|---|---|
| **Name** | Exact business name (no keywords) |
| **Categories** | Primary + 9 secondary (specific) |
| **Description** | 750 chars, keyword-rich, local |
| **Photos** | 10+ high-res (exterior, interior, team, products) |
| **Posts** | Weekly: events, offers, news, COVID updates |
| **Q&A** | Pre-populate top 10 questions |
| **Reviews** | Respond to 100% within 24h |
| **Attributes** | All relevant (wifi, parking, accessibility) |

### Local link building via earned media
| Tactic | Execution |
|---|---|
| **NAP consistency** | Name, Address, Phone identical across all citations |
| **Local citations** | Chamber, BBB, local directories, .gov/.edu links |
| **Earned media links** | Ask outlets for dofollow link to GBP landing page |
| **Event schema** | `Event` markup for local events coverage |
| **Local news carousel** | `NewsArticle` + `areaServed` + `spatialCoverage` |

---

## Google Discover optimization

### Discover ranking factors
| Factor | Weight | Optimization |
|---|---|---|
| **E-E-A-T** | High | Author bios, credentials, contact, corrections policy |
| **Content freshness** | High | Publish within 24h of event; update `dateModified` |
| **Visual appeal** | High | 1200px+ hero, 16:9, alt text, captions |
| **Mobile UX** | High | Core Web Vitals passing, no intrusive interstitials |
| **Topic authority** | Medium | Consistent coverage of niche |
| **User engagement** | Medium | CTR, dwell time, scroll depth |

### Discover-optimized article template
```html
<article>
  <header>
    <h1>Headline with keyword + emotional hook (< 110 chars)</h1>
    <div class="byline">
      By <a href="/author/jane" rel="author">Jane Reporter</a>
      <time datetime="2024-01-15T10:30:00-05:00">Jan 15, 2024</time>
    </div>
  </header>
  <figure>
    <img src="hero-1200x630.jpg" alt="Descriptive alt text" width="1200" height="630">
    <figcaption>Caption with context</figcaption>
  </figure>
  <div class="article-body">
    <p>Lead paragraph with who/what/where/when/why in 25 words.</p>
    <!-- Full article with H2/H3 subheads, bullet points, short paragraphs -->
  </div>
  <footer>
    <div class="tags">Tag1, Tag2, Tag3</div>
    <div class="share">Social buttons</div>
  </footer>
</article>
```

---

## Core Web Vitals (CWV) for news sites

### Thresholds (Google standards)
| Metric | Good | Needs Improvement | Poor |
|---|---|---|---|
| **LCP** (Largest Contentful Paint) | ≤ 2.5s | 2.5-4.0s | > 4.0s |
| **INP** (Interaction to Next Paint) | ≤ 200ms | 200-500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | ≤ 0.1 | 0.1-0.25 | > 0.25 |

### News-specific CWV fixes
| Issue | Fix |
|---|---|
| **Hero image LCP** | Preload hero, use WebP/AVIF, proper dimensions |
| **Ad/layout shift CLS** | Reserve ad slots, `aspect-ratio` boxes |
| **Third-party scripts INP** | Defer non-critical, `partytown`, `isPartytown` |
| **Font loading** | `font-display: swap`, preload key fonts |

---

## Earned media SEO checklist (per placement)

### Pre-publication (pitch to outlet)
- [ ] Provide **canonical URL** for your site's version
- [ ] Request **dofollow link** to your canonical page
- [ ] Provide **structured data** (JSON-LD) for their CMS
- [ ] Supply **hero image** (1200x630, WebP, alt text)
- [ ] Provide **author bio** with schema markup
- [ ] Request **canonical tag** pointing to your URL

### Post-publication (within 24h)
- [ ] In Google Search Console, inspect the URL and request indexing.
- [ ] Submit the URL to the Google News Publisher Center feed.
- [ ] Share on **owned social** (triggers Discover)
- [ ] Add **internal links** from your site to placement
- [ ] In Search Console, monitor the Performance report's News tab.

### Ongoing (weekly)
- [ ] In Search Console, monitor Performance with the News search type selected.
- [ ] Track **Discover impressions** (if eligible)
- [ ] In Search Console's Experience section, monitor Core Web Vitals.
- [ ] Update **evergreen placements** with fresh data/links

---

## Tools & monitoring

| Tool | Purpose | Cost |
|---|---|---|
| **Google Search Console** | Indexing, CWV, News performance | Free |
| **Google Publisher Center** | News feed management | Free |
| **Google Business Profile** | Local pack | Free |
| **Schema Markup Validator** | Structured data testing | Free |
| **Rich Results Test** | Rich snippet preview | Free |
| **PageSpeed Insights** | CWV debugging | Free |
| **Screaming Frog** | Technical SEO audit | £149/yr |
| **Ahrefs / Semrush** | Keyword tracking, backlinks | $99-499/mo |

---

## Earned media SEO KPI dashboard

| KPI | Target | Frequency |
|---|---|---|
| **News impressions (GSC)** | +20% MoM | Weekly |
| **News CTR** | > 2% | Weekly |
| **Discover impressions** | +15% MoM | Weekly |
| **Local pack visibility** | Top 3 for 10+ keywords | Monthly |
| **CWV passing rate** | 100% pages | Weekly |
| **Indexed earned media URLs** | 100% within 24h | Daily |
| **Referral traffic from earned** | +10% QoQ | Monthly |

---

## References
- `https://developers.google.com/search/docs/appearance/structured-data/article`
- `https://news.google.com/publisher`, Publisher Center
- `https://developers.google.com/search/docs/appearance/google-news`
- `https://support.google.com/news/publisher-center/answer/7428893`, Feed specs
- `https://web.dev/vitals/`, Core Web Vitals
- `https://www.google.com/business/`, Google Business Profile
- `wiki/public-relations/us-outreach-workflow.md`

## What this skill does not do
- It does not implement SEO changes, configure a CMS, or guarantee rankings.
- It has no MCP or CLI tools; it is a reference.
