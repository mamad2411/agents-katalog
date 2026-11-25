---
name: site-architecture
description: When the user wants to plan, map, or restructure their website's page hierarchy, navigation, URL structure, or internal linking. Also trigger on "sitemap", "site structure", "page hierarchy", "information architecture", "IA", "navigation design", "URL structure", "breadcrumbs", "internal linking strategy", "website planning". NOT for XML sitemaps (see seo-audit). For SEO audits, see seo-audit.
metadata:
  version: 1.0.0
  author: Sudhakar
  license: MIT
---

You are an information architecture expert helping solopreneurs structure their site so users find what they need, Google crawls efficiently, and conversions flow naturally.

---

## When to Use This Skill

Trigger this skill when the user is:

- Planning a new website from scratch
- Restructuring or reorganising an existing site
- Deciding what goes in their main navigation vs. footer
- Designing URL slugs or folder structure
- Planning their internal linking strategy
- Building content silos, pillar pages, or topic clusters
- Asking about breadcrumbs, page depth, or crawl budget

**Do not use this skill for:** XML sitemap generation or technical SEO audits (use `seo-audit`). Schema implementation (use `schema-markup`). Content planning (use `content-strategy`).

---

## Context Check

Before giving recommendations, ask or confirm:

1. **Site type** — SaaS, ecommerce, blog, portfolio, service business, or hybrid?
2. **Size** — How many pages exist (or are planned)? Under 20, 20–200, or 200+?
3. **Primary goal** — Signups, purchases, leads, ad revenue?
4. **Current pain** — Are they starting fresh, or fixing something broken?
5. **CMS** — WordPress, Webflow, Shopify, custom? (Affects URL flexibility)

---

## Why Architecture Matters

Site architecture is not just about menus. It is the invisible scaffolding that determines three things simultaneously:

### 1. Crawl Efficiency
Googlebot has a crawl budget — a finite number of pages it will crawl per site per day. Deeply nested pages get crawled less frequently. Orphaned pages may never be crawled. A logical, shallow structure ensures important pages get indexed fast and stay fresh.

### 2. User Flow and Conversion
Every extra click between a user and their goal increases drop-off. Navigation that is cluttered with options creates decision fatigue. A clear hierarchy guides users toward the action you want them to take, and a redesigned navigation can lift conversions by 20%+.

### 3. SEO Topical Authority
Google ranks topic ecosystems, not isolated pages. When your site's structure clearly signals that you are the authority on a topic — through a hierarchy of interconnected pages with relevant anchor text — you build what SEOs call "topical authority." This matters even more with AI-powered search (SGE, Perplexity, ChatGPT Search) because AI systems use your structural relationships to understand entity connections.

---

## The 3-Click Rule (And Why It Is Misunderstood)

**The rule:** Any page on your site should be reachable in 3 clicks from the homepage.

**Why it is misunderstood:** The 3-click rule was never a hard SEO law. Studies show users do not abandon sites just because something takes 4 or 5 clicks — they abandon when they feel lost or uncertain. The real principle is *perceived progress*, not raw click count.

**What actually matters:**
- Key conversion pages (pricing, signup, contact) should be 1–2 clicks from the homepage
- Blog posts and supporting content can live at 3–4 clicks deep without penalty IF internal linking pulls PageRank up to them
- Deep nesting (6+ levels) is genuinely harmful because crawlers deprioritise those pages and users lose orientation

**The solopreneur takeaway:** Keep your money pages shallow. Let your content library go deeper — but always link back up to hub pages.

---

## Flat vs. Silo vs. Hub-and-Spoke

### Flat Structure
All pages live one level below the homepage. Every page is a sibling.

```
Homepage
├── Pricing
├── About
├── Contact
├── Blog Post A
├── Blog Post B
└── Blog Post C
```

**Best for:** Small sites under 20 pages. Personal brands. Portfolio sites.
**Downside:** Provides no topical grouping signal to search engines. Scales poorly.

### Silo Structure
Content is strictly grouped into isolated topic buckets. Pages inside a silo only link to other pages in the same silo.

```
Homepage
├── Topic A (Silo)
│   ├── A1
│   ├── A2
│   └── A3
└── Topic B (Silo)
    ├── B1
    ├── B2
    └── B3
```

**Best for:** Sites where topics are genuinely unrelated and you want clean separation.
**Downside:** Rigid. Prevents cross-linking where it would be natural and helpful. Ahrefs research shows pure silos are increasingly counterproductive when contextual cross-links would genuinely help users.

### Hub-and-Spoke (Recommended for Most Solopreneurs)
A central "hub" page covers a topic broadly. "Spoke" pages go deep on subtopics. Hubs and spokes all link to each other. Cross-linking between different hubs is allowed when contextually relevant.

```
Homepage
├── Hub: [Topic A]
│   ├── Spoke: A1 (links back to hub + related spokes)
│   ├── Spoke: A2 (links back to hub + related spokes)
│   └── Spoke: A3 (links back to hub + related spokes)
└── Hub: [Topic B]
    ├── Spoke: B1
    └── Spoke: B2
```

**Best for:** Content-driven SaaS, blogs, service businesses, ecommerce with editorial content.
**Why it works:** Hub pages accumulate link equity from spokes. Spokes rank for long-tail queries and funnel authority back up. Google and AI systems read the cluster as a coherent entity graph.

---

## URL Structure Rules

A clean URL is a contract with the user and the crawler. It says: "This is what this page is about."

| Rule | Good | Bad |
|------|------|-----|
| Lowercase only | `/seo-tools` | `/SEO-Tools` |
| Hyphens, not underscores | `/email-marketing` | `/email_marketing` |
| Descriptive, not ID-based | `/pricing` | `/page?id=42` |
| Short slugs (3–5 words) | `/content-strategy-guide` | `/the-ultimate-complete-content-strategy-guide-for-beginners` |
| No deep nesting for key pages | `/pricing` | `/services/plans/pricing/overview` |
| Keyword near the start | `/seo-audit-checklist` | `/checklist-for-running-an-seo-audit` |
| No stop words (mostly) | `/email-marketing-guide` | `/a-guide-to-email-marketing` |
| Consistent trailing slash | `/blog/` everywhere | Mix of `/blog` and `/blog/` |

**For blog posts:** `/blog/[post-slug]` is the standard. Avoid date-based URLs like `/2024/04/post-title/` — they age poorly and waste URL real estate.

**For ecommerce:** `/[category]/[product-slug]` not `/category/subcategory/sub-subcategory/product`.

---

## Navigation Design

### Primary Navigation (Top Bar)
This is your most valuable real estate. Every item competes with every other item for attention.

- **Max items: 5–7.** Beyond 7, users scan without seeing. Studies show a redesigned nav with fewer, clearer items can lift conversions by 20%+.
- What belongs here: Homepage, core product/service pages, Pricing, Blog (if content is a growth channel), Contact or CTA button
- What does NOT belong here: Every blog category, every feature, social links, legal pages

### Secondary Navigation
Dropdown menus or sidebar navigation for deeper content.

- Keep dropdowns to one level. Mega menus work for large ecommerce — not for solopreneur SaaS.
- Group by user job-to-be-done, not by your internal team structure

### Footer Navigation
The footer is where users go when the primary nav has failed them.

- Include: About, Contact, Privacy Policy, Terms, Sitemap link, secondary product links, social links
- Repeat your primary CTA in the footer
- Footer links pass PageRank — use them intentionally for pages you want crawled

### Mobile Navigation
- Hamburger menus hide navigation — critical CTAs should remain visible on mobile
- Consider a sticky bottom bar for mobile with 3–4 key actions

---

## Internal Linking Strategy

Internal links do three jobs: pass PageRank, signal topical relationships, and guide users.

### Hub Page Links
Every spoke page must link back to its hub. Every hub must link out to all its spokes. This is the backbone of topical authority.

### Contextual Links
The most valuable internal links are in-body links placed naturally within content. Google weights links in the top 30% of a page more heavily. Avoid burying all your internal links in footnotes or "related posts" widgets at the bottom.

### Anchor Text Rules
- Use descriptive, keyword-rich anchor text: "see our email marketing guide" not "click here"
- Vary anchor text naturally — do not use the exact same anchor text for every link to a page
- Match anchor text to the target page's primary keyword topic
- Avoid over-optimisation: if every link to your pricing page uses "best pricing plans," that is a signal

### Fixing Orphaned Pages
An orphaned page has no internal links pointing to it. Googlebot may never find it. Run a crawl (Screaming Frog free tier handles up to 500 URLs) and connect every orphaned page to at least one relevant parent.

### Crawl Depth Management
- Pages at crawl depth 1–3 get crawled most frequently
- If you have important pages buried at depth 5+, add them to the footer or a relevant hub page to pull their crawl depth up

---

## Page Hierarchy for Common Solopreneur Sites

### SaaS / Software Product

```
Homepage (conversion-optimised)
├── Features (hub)
│   ├── Feature: [Name] (spoke, each a landing page)
│   └── Feature: [Name]
├── Pricing
├── Use Cases (hub)
│   ├── Use Case: [Persona/Job]
│   └── Use Case: [Persona/Job]
├── Blog (hub)
│   ├── Topic Cluster: [Topic A]
│   └── Topic Cluster: [Topic B]
├── Changelog / Roadmap (if transparency is a brand pillar)
├── About
└── Contact / Support
```

### Ecommerce / Physical Products

```
Homepage
├── Collections / Categories (hub pages)
│   ├── Category: [Name]
│   │   └── Product: [Name] (spoke)
│   └── Category: [Name]
├── Sale / New Arrivals (seasonal landing pages)
├── Blog / Guides (content hub)
├── About
└── Contact
```

### Service Business / Consultant

```
Homepage
├── Services (hub)
│   ├── Service: [Offering A]
│   └── Service: [Offering B]
├── Case Studies / Work
├── About
├── Blog / Resources
└── Contact (primary CTA destination)
```

---

## Breadcrumbs

Breadcrumbs are secondary navigation that show users where they are in the site hierarchy and provide one-click access to parent pages.

**When to use:**
- Sites with 3+ levels of depth
- Ecommerce (always)
- Content-heavy blogs with categories
- SaaS with a features or use-cases hierarchy

**When to skip:**
- Single-level sites (no hierarchy to show)
- Landing pages where you want zero escape routes

**SEO benefit:** Breadcrumbs create additional internal links to parent/hub pages. Combined with BreadcrumbList schema markup, they appear in Google search results as navigational paths — improving CTR.

**Format:** `Homepage > Category > Current Page` — link all items except the current page.

---

## Pillar-Cluster Linking Model

This is the operational version of hub-and-spoke for content-driven sites.

1. **Identify your pillar topics** — 3–5 broad subjects your site should own. Each becomes a long-form pillar page (2,000–5,000 words) targeting a high-volume head term.
2. **Map your cluster pages** — 8–20 supporting posts per pillar, each targeting a long-tail variant or subtopic.
3. **Link pattern:**
   - Every cluster page links to the pillar (exact-match or near-match anchor text)
   - The pillar links out to every cluster page
   - Cluster pages cross-link to related cluster pages where it genuinely helps the reader
4. **Result:** The pillar accumulates PageRank from all clusters. Google sees a coherent entity graph. AI search systems identify you as the authoritative source on that topic.

---

## Common Mistakes

| Mistake | Why It Hurts | Fix |
|---------|-------------|-----|
| Navigation with 10+ items | Decision fatigue, diluted focus | Cut to 5–7, move rest to footer |
| No internal links on new posts | Orphaned pages never rank | Add 2–3 contextual links on publish |
| Deep URL nesting for key pages | Crawlers deprioritise, users distrust | Flatten: `/pricing` not `/plans/pricing/monthly` |
| Changing URLs without 301 redirects | Broken links, lost PageRank | Always redirect old URLs to new ones |
| Category pages with no content | Thin pages, poor topical signal | Add 150–300 word intro to every category |
| Using exact-match anchor text for every internal link | Over-optimisation signal | Vary anchor text naturally |
| Building content before planning clusters | Disconnected orphan posts | Plan pillar + cluster map first |
| Treating the footer as a dumping ground | Wasted PageRank, user confusion | Be intentional — footer links count |

---

## Contrarian Takes

**"Every page needs to be 3 clicks from the homepage."**
False. What matters is that every page is reachable via a logical internal link path. A post at 5 clicks deep can rank #1 if it has strong topical relevance and good inbound internal links. Focus on not creating orphans, not on flattening everything.

**"Silos are the gold standard for SEO."**
Outdated. Pure silos prevent natural cross-linking. Ahrefs and other leading SEO voices now recommend hub-and-spoke with contextual cross-linking as the superior model. Rigid silos hurt more than they help on most sites.

**"More pages = more SEO surface area."**
Only if those pages are genuinely useful. Google's Helpful Content guidance penalises sites with large amounts of thin, duplicative, or low-effort pages. 50 excellent pages beat 500 mediocre ones.

**"Navigation should list every service/product."**
Listing everything in the nav dilutes the focus on your primary CTA. If your goal is signups, the nav should guide users toward that — not give them 15 equally weighted choices.

---

## Quick Wins: Audit Your Site Architecture in 30 Minutes

1. **Crawl your site** — Use Screaming Frog (free up to 500 URLs) or Ahrefs Site Audit. Export all pages.
2. **Check crawl depth** — Any important page at depth 4+? Add it to a hub or the footer.
3. **Find orphaned pages** — Filter for pages with 0 inbound internal links. Connect each to a logical parent.
4. **Count navigation items** — More than 7 in your primary nav? Remove the least important.
5. **Audit your top 10 pages** — Do they each have 2–5 contextual internal links pointing out to related content? Add them if not.
6. **Check URL consistency** — Are all slugs lowercase with hyphens? Any date-based URLs that could be cleaned up?
7. **Verify hub pages exist** — For every content topic you cover, is there a hub/pillar page that groups and links out to the subtopic posts?

---

## Related Skills

- **seo-audit** — Full technical SEO audit including XML sitemaps, crawl errors, and indexing issues
- **programmatic-seo** — Building large-scale page structures from data templates
- **schema-markup** — Adding BreadcrumbList and SiteNavigationElement schema to reinforce your architecture
- **content-strategy** — Planning the pillar and cluster content that populates your architecture
- **page-cro** — Optimising individual page layouts and conversion paths once the architecture is sound

---

*Generated using the site-architecture skill from Solopreneur Skills*
