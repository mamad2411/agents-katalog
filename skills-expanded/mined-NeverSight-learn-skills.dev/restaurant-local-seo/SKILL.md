---
name: restaurant-local-seo
description: Local SEO audit — "best [cuisine] near me" targeting, Google Business Profile optimization, NAP consistency, citation building, restaurant schema markup
version: 1.0.0
author: AI Restaurant Team
tags: [restaurant, local-seo, google-business-profile, schema, citations]
command: /restaurant local-seo <name>
output: RESTAURANT-SEO-[Name].md
---

# Local SEO Audit & Strategy

You audit a restaurant's local SEO performance — focusing on how it ranks for "best [cuisine] near me," map pack visibility, GBP optimization, NAP consistency across the citation web, and Restaurant schema markup. Then produce a prioritized 90-day local SEO roadmap.

**DISCLAIMER: AI-generated SEO audit. Local search ranking is influenced by many factors including review velocity, proximity, and Google's evolving algorithm.**

---

## When to use

- `/restaurant local-seo <name>` — full local SEO audit
- "rank for best [cuisine] near me"
- "how do I show up in Google maps"

---

## The 3 Pillars of Local SEO for Restaurants

1. **Relevance** — Does Google understand what you serve and where?
2. **Distance** — How close is the searcher to the restaurant?
3. **Prominence** — How well-known/reviewed/cited is the business?

You can only control #1 and #3.

---

## Execution Pipeline

### Step 1: Capture Current Rankings

Run searches and note position:

```
WebSearch("best [cuisine] in [city]")
WebSearch("best [cuisine] [neighborhood] [city]")
WebSearch("[cuisine] near me [city]")
WebSearch("[cuisine] restaurants [zip code]")
WebSearch("[cuisine] delivery [city]")
WebSearch("[specific dish] [city]")
```

For each search, capture:
- Map pack position (1, 2, 3, or not in map pack)
- Organic position
- Total competitors in the map pack
- Featured rich snippets / "people also ask"

### Step 2: Audit GBP for SEO

Critical SEO elements on GBP:
- **Primary category:** Restaurant ✓ — must match
- **Secondary categories:** "Italian Restaurant", "Pizza Restaurant", "Catering" — up to 4 more
- **Business description:** Front-load with primary keyword
- **Services:** Listed for "Dine-in", "Takeout", "Delivery", "Catering"
- **Attributes:** All applicable
- **Posts:** 1+ per week with target keywords naturally placed
- **Q&A:** Pre-seed with FAQs containing target keywords
- **Reviews:** Total count, recency, response rate (all SEO signals)
- **Photos:** Geo-tagged photos help relevance
- **Products:** Top menu items as products with names/descriptions/prices

### Step 3: NAP & Citation Audit

Check NAP consistency across 25+ key directories. Inconsistencies dilute local SEO authority.

**Tier 1 (highest authority):**
- Google Business Profile
- Apple Maps / Apple Business Connect
- Yelp
- Facebook
- TripAdvisor
- Bing Places
- Foursquare

**Tier 2 (food-specific):**
- OpenTable / Resy / Tock
- Zomato
- Restaurant.com / Allmenus
- Eater (in markets where it covers)
- The Infatuation

**Tier 3 (general / industry):**
- Better Business Bureau
- Yellow Pages
- Chamber of Commerce
- Local newspaper business directory
- Industry associations (state restaurant association)

### Step 4: Website Schema Audit

For restaurants, Google needs structured data to power rich results:
- **Restaurant schema** (name, address, phone, cuisine, price range, hours)
- **Menu schema** (each menu item as MenuItem with name, description, price)
- **Review schema** (aggregateRating from your reviews)
- **LocalBusiness schema** (additional local signals)
- **Event schema** (for live music nights, wine dinners, etc.)
- **FAQPage schema** (for FAQ section)

Check schema with Google's Rich Results Test.

### Step 5: Content / On-Site Audit

Pages a restaurant website should have for local SEO:
- Homepage (target: "[cuisine] restaurant [city]")
- Menu page (target: "[cuisine] menu [city]")
- About page (target: "[cuisine] restaurant [neighborhood]" — long tail)
- Reservations page (target: "[cuisine] reservations [city]")
- Catering page (target: "[cuisine] catering [city]")
- Private events page (target: "private dining [city]")
- Specific dish pages (for signature items)
- Location page (target: "[cuisine] restaurant near [landmark]")

### Step 6: Competitor SEO Comparison

For top 3 ranking competitors, capture:
- Domain Authority (rough estimate via Moz Bar / Ahrefs Free)
- Backlink count
- Review count + rating
- Years on Google (older = stronger)
- Mentions in press / blogs

---

## Output Template

Save to `RESTAURANT-SEO-[Name].md`:

```markdown
# Local SEO Audit: [NAME]

> **Generated:** [DATE] | **SEO Score:** [X]/100

**DISCLAIMER: AI-generated local SEO audit.**

## Current Rankings

| Query | Map Pack Position | Organic Position |
|-------|-------------------|-------------------|
| "best [cuisine] in [city]" | [3 / Not in pack] | [Page 1 #7] |
| "best [cuisine] near me" | ... | ... |
| "[cuisine] [neighborhood]" | ... | ... |
| "[cuisine] delivery [city]" | ... | ... |
| "[signature dish] [city]" | ... | ... |

**Map Pack Visibility Rate:** [X / Y queries] = [X]%

## SEO Score Breakdown

| Pillar | Score | Notes |
|--------|-------|-------|
| GBP Optimization | X/25 | ... |
| Reviews & Prominence | X/25 | ... |
| NAP & Citations | X/20 | ... |
| Schema Markup | X/15 | ... |
| On-Site Content | X/15 | ... |
| **Total** | **X/100** | |

## Google Business Profile Optimization

### Strong
- ...

### Weak
| Element | Current | Target | Fix |
|---------|---------|--------|-----|
| Secondary categories | 1 (Restaurant) | 4-5 | Add "Italian Restaurant", "Pizza Restaurant", "Catering", "Wine Bar" |
| Description | Generic | Keyword-rich | Rewrite with "Italian restaurant in [neighborhood] serving [signature dishes]" |
| Posts (last 30 days) | 0 | 4+ | Set up weekly posting cadence |
| Q&A answered | 60% | 100% | Answer the 3 open questions today |
| Geo-tagged photos | 0% | 100% | Reupload photos with GPS metadata |
| Products | 0 | 10+ | Add top 10 menu items as products |

## NAP Consistency Audit

| Directory | Name | Address | Phone | Status |
|-----------|------|---------|-------|--------|
| Google | ... | ... | ... | Reference |
| Apple Maps | ... | ... | ... | Match / Mismatch |
| Yelp | ... | ... | ... | ... |
| Facebook | ... | ... | ... | ... |
| TripAdvisor | ... | ... | ... | ... |
| Bing Places | ... | ... | ... | ... |
| Foursquare | ... | ... | ... | Not listed — ADD |
| OpenTable | ... | ... | ... | ... |
| Yellow Pages | ... | ... | ... | ... |

**Missing citations (add these):** [List directories restaurant isn't on yet]
**Inconsistent citations (fix these):** [Specific platform + what to fix]

## Schema Markup Audit

| Schema Type | Currently On Site? | Recommended |
|-------------|---------------------|-------------|
| Restaurant | No | YES — homepage |
| Menu / MenuItem | No | YES — menu page |
| AggregateRating | No | YES — homepage |
| LocalBusiness | No | YES — contact/footer |
| FAQPage | No | YES — if FAQ exists |
| Event | No | If hosting events |
| OpeningHoursSpecification | No | YES — embedded in Restaurant schema |

### Ready-to-Use Restaurant Schema (paste into website <head>)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Restaurant",
  "name": "[Restaurant Name]",
  "image": "[URL to hero photo]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[Address]",
    "addressLocality": "[City]",
    "addressRegion": "[State]",
    "postalCode": "[ZIP]",
    "addressCountry": "US"
  },
  "telephone": "[Phone]",
  "url": "[Website]",
  "servesCuisine": "[Cuisine]",
  "priceRange": "[$$]",
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday"],
      "opens": "11:00",
      "closes": "22:00"
    }
  ],
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "[X.X]",
    "reviewCount": "[N]"
  },
  "hasMenu": "[URL to menu]",
  "acceptsReservations": "True"
}
</script>
```

## Competitor SEO Comparison

| Restaurant | Map Pack Avg Position | Review Count | Domain Authority |
|------------|----------------------|--------------|-------------------|
| [Subject] | 5 | 287 | 12 |
| Competitor A | 1 | 1,247 | 22 |
| Competitor B | 2 | 892 | 18 |
| Competitor C | 3 | 540 | 15 |

**Gap to #1:** ~960 more reviews + 10+ Domain Authority points. **Closest win:** outranking #3 with consistent review velocity + new citations.

## Target Keyword Map

| Page | Primary Keyword | Secondary Keywords | Search Volume (est) |
|------|-----------------|---------------------|---------------------|
| Homepage | [cuisine] restaurant [city] | best [cuisine] [city], [cuisine] near me | 1,000+/mo |
| Menu | [cuisine] menu [city] | [signature dish] [city] | 200/mo |
| About | family-owned [cuisine] [city] | authentic [cuisine] [city] | 100/mo |
| Catering | [cuisine] catering [city] | [cuisine] catering [neighborhood] | 150/mo |
| Reservations | [cuisine] reservations [city] | book [cuisine] [city] | 75/mo |

## 90-Day Action Plan

### Days 1-30 — Foundation
1. **Week 1:** Fix all NAP inconsistencies across Tier 1 directories
2. **Week 1:** Add Restaurant + LocalBusiness schema to website
3. **Week 2:** Add 4 secondary categories to GBP, rewrite description
4. **Week 2:** Add top 10 menu items as Products on GBP
5. **Week 3:** Submit to 10 missing Tier 2 citations
6. **Week 4:** Set up weekly GBP posting cadence

### Days 31-60 — Velocity
1. **Review velocity push:** Train staff to ask every happy guest for a Google review — target 8-12 new reviews/week
2. **Content:** Publish 4 dedicated dish pages (one per signature item)
3. **Links:** Reach out to 3 local food bloggers / press for coverage
4. **Photos:** Add 15 geo-tagged photos per month

### Days 61-90 — Prominence
1. **Press strategy:** Pitch local food editors — anniversary, new chef, new dish launch
2. **Partnerships:** 2-3 cross-promotions with non-competing local businesses
3. **Events / experiences:** Wine dinner, cooking class — generates press + UGC
4. **Reputation defense:** Set up monitoring for new reviews / mentions

## Expected Outcomes

| Metric | Baseline | 90-Day Target |
|--------|----------|---------------|
| Map pack appearances (5 queries) | X% | X+30% |
| Google reviews | X | +60-100 |
| Organic website traffic | X | +25-40% |
| Phone calls from GBP | X | +30% |
| Direction requests from GBP | X | +30% |

**DISCLAIMER: AI-generated SEO audit. Local search results depend on many factors including searcher proximity. Results will vary.**
```

---

## Quality Standards

- Audit covers all 6 pillars (rankings, GBP, NAP, schema, content, competitors)
- Schema code is copy-paste ready
- 90-day plan is granular and prioritized
- Every recommendation tied to a search query or ranking factor

**DISCLAIMER: For educational/research purposes only.**
