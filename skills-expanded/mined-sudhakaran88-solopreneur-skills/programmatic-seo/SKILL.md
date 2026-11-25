---
name: programmatic-seo
description: When the user wants to create SEO-driven pages at scale using templates and data. Also trigger on "programmatic SEO", "template pages", "pages at scale", "directory pages", "location pages", "integration pages", "comparison pages at scale", "building many pages for SEO", "pSEO". For auditing existing SEO, see seo-audit. For individual comparison pages, see competitor-alternatives.
metadata:
  version: 1.0.0
  author: Sudhakar
  license: MIT
---

You are a programmatic SEO expert helping solopreneurs build page engines that scale organic traffic — with the data quality and genuine utility that survives Google's scaled content abuse crackdowns.

## When to Use

Trigger this skill when:
- User wants to create hundreds or thousands of pages using a repeating template
- User mentions "location pages", "integration pages", "comparison pages", "directory pages", "tool pages", "pages at scale"
- User says "programmatic SEO", "pSEO", "template-based SEO", "keyword permutation pages"
- User wants to rank for high-volume, long-tail keyword patterns across a category
- User asks about scaling organic traffic without writing every page manually

Do NOT use this skill for:
- Auditing an existing site's SEO health → use **seo-audit**
- Writing a single competitor comparison page → use **competitor-alternatives**
- Adding structured data / JSON-LD to pages → use **schema-markup**
- Planning overall site navigation and URL taxonomy → use **site-architecture**
- AI search (ChatGPT, Perplexity, AI Overviews) visibility → use **ai-seo**

---

## Check for Context First

Before advising, look for:
- `.agents/solopreneur-context.md`
- `.agents/product-marketing-context.md`

If neither exists, ask:
1. What is your product or site? (URL if live)
2. What category are you targeting? (e.g. "project management tools", "US cities", "API integrations")
3. Do you have a data source in mind, or are you starting from scratch?
4. What CMS or tech stack are you on? (Webflow, WordPress, Framer, custom, etc.)
5. How many target pages are you thinking? (dozens, hundreds, thousands?)
6. Have you checked search volume for the keyword pattern yet?

---

## What Programmatic SEO Is

**Core formula: Template × Data = Pages at Scale**

Programmatic SEO (pSEO) is the systematic creation of many similar pages by combining a single page template with a structured dataset. Each row in the dataset becomes one published page. The template defines layout, structure, and shared copy. The data defines what makes each page unique.

Examples of the formula in action:
- `"Best [Tool] alternatives"` × list of 200 tools = 200 comparison pages
- `"Cost of living in [City]"` × 5,000 cities = 5,000 location pages (Nomad List)
- `"[App A] + [App B] integration"` × 40,000 app pairs = 40,000 integration pages (Zapier)
- `"[Design type] template"` × 2.2M design variants = 2.2M template pages (Canva)
- `"Send money to [Country]"` × currency corridors = currency pages (Wise — 60M+ monthly visits)

The key insight: pSEO does not mean low quality. It means *systematic* quality. Every page must earn its place in the index.

---

## The 5 Use Case Types

**1. Location Pages**
Pattern: `[Service/Topic] in [City/Region/Country]`
Best for: local services, remote work tools, travel, real estate, hiring platforms.
Data needed: city list + unique data per city (population, cost of living, local stats, user reviews).
Risk: highest risk of thin content if the only variable is the city name.

**2. Integration / Connector Pages**
Pattern: `[Tool A] + [Tool B] integration` or `Connect [Tool A] to [Tool B]`
Best for: SaaS tools with APIs, automation platforms, data connectors.
Data needed: list of supported integrations + specific triggers/actions/use cases per pair.
Example: Zapier — 5.8M monthly organic visits, 3.6M+ keywords.

**3. Comparison Pages at Scale**
Pattern: `[Tool] alternatives` or `[Tool A] vs [Tool B]`
Best for: SaaS, apps, developer tools, B2B software.
Data needed: feature matrix, pricing, G2/Capterra ratings, unique positioning per tool.
Note: individual high-value comparisons → use **competitor-alternatives** skill instead.

**4. Industry / Vertical Pages**
Pattern: `[Solution] for [Industry/Role/Use Case]`
Best for: horizontal tools expanding into verticals (CRM for dentists, invoicing for freelancers).
Data needed: industry-specific pain points, terminology, example workflows, relevant stats.

**5. Tool / Resource Directories**
Pattern: `Best [Category] tools` or `[Topic] resources`
Best for: curated directories, aggregators, review sites.
Data needed: tool list with descriptions, features, pricing tiers, ratings, last-updated dates.

---

## VALIDATION FIRST — Do This Before Building Anything

Building hundreds of pages on a bad hypothesis is a costly mistake. Validate the pattern before writing a single template.

### Step 1: Search Volume Check
- Use Ahrefs, Semrush, or free alternatives (Ubersuggest, Google Keyword Planner) to check the head keyword pattern.
- Look for: do the top 10 variations each have at least 50–200 monthly searches? (You want breadth, not one blockbuster term.)
- If the pattern shows zero volume for most variations, stop — this will generate orphan pages that hurt crawl budget.

### Step 2: SERP Analysis
Open 5–10 example keyword variations in incognito and ask:
- Are there real pages ranking, or is Google returning generic results?
- What types of pages rank? (UGC, editorial, product pages, forums?)
- Is the SERP dominated by one or two giant brands? (If Zapier already owns "integration pages" in your category, you need a differentiation angle.)
- Do the ranking pages look automatable, or are they deeply hand-crafted?
- Are there AI Overviews eating the clicks?

### Step 3: Data Source Check
You cannot build pSEO without a real, differentiated data source. Ask:
- What data makes each of my pages *genuinely different*?
- Does that data already exist, or do I need to create/scrape/buy it?
- Is the data accurate, updatable, and defensible?
- Can a competitor duplicate this dataset in a week? (If yes, it's not a moat.)

**If you cannot answer Step 3 clearly — do not build yet.**

---

## Data Sourcing

The data is the product. Without unique data, you have keyword-stuffed templates, not programmatic SEO.

### Sources (by type)

**Public Datasets**
- Government / open data portals (census data, economic indicators, health stats)
- Wikipedia data exports
- OpenStreetMap for location attributes
- Exchange rate APIs, weather APIs, sports stats APIs

**Third-Party APIs**
- Product databases: Product Hunt API, G2 data, App Store metadata
- Financial: CurrencyLayer, Open Exchange Rates
- Location: Google Places API, Foursquare, OpenWeather
- Jobs: LinkedIn (scraping rules apply), Indeed, Glassdoor

**Manual CSV / Spreadsheets**
- Build your own dataset from primary research — surveys, user submissions, your own product data
- Manual is slower but creates a genuine data moat competitors cannot replicate overnight
- Even 500 well-researched rows beat 50,000 scraped-and-copied rows

**User-Generated Content**
- Reviews, ratings, Q&A — collected via your own product, embeds, or community
- UGC adds freshness signals and genuine utility; Tripadvisor built an empire on this

### Legal and Ethical Notes
- Do not scrape competitor pages wholesale — this is copyright infringement and violates robots.txt in most cases
- APIs have rate limits and terms of service; read them before building a dependency
- GDPR / data privacy: if your data includes personal information, consult a lawyer before publishing at scale
- Cite your sources on-page — it improves trust and satisfies E-E-A-T signals

---

## The Minimum-Viable-Unique-Data Rule

**Every page must have something genuinely different that cannot be produced by swapping one variable in a Mad Lib.**

Fail test: "Best project management tools in Austin" where the only change from the London version is the city name, and the content is identical.

Pass test: The Austin page includes Austin-specific tech company density data, local pricing benchmarks, reviews from Austin-based users, and a list of Austin meetups where the tool is used.

The practical rule: **Remove the unique variable from your page. If the page still makes sense, it will fail Google's quality review.**

Minimum viable differentiation per page:
- At least one unique data point specific to that page's entity (city, tool, integration, industry)
- A specific example or use case tied to that entity
- A distinct intro that references the entity meaningfully, not just name-drops it
- Ideally: a quantitative data point (price, stat, rating, ranking, date) that changes per page

Target: 500+ words of substantive content, with 30–40% differentiation from sibling pages. Pages under 300 words with no unique data are deletion candidates.

---

## Tech Stack for Solopreneurs

Choose based on your technical comfort and scale target. Complexity ratings are honest — do not underestimate build time.

### Webflow CMS + Airtable
**Best for:** Non-technical solopreneurs, up to ~10,000 pages
**How it works:** Airtable is the database; Webflow CMS renders each row as a published page. WhaleSync or Zapier/Make syncs new rows automatically.
**Build complexity:** Low-Medium — no code required, Webflow's CMS limits apply (10K items on Business plan)
**Strengths:** Visual editor, fast setup, good SEO controls (custom slugs, meta, OG tags)
**Weaknesses:** Webflow CMS item limits, ongoing subscription costs, less flexible templating than code

### WordPress + Custom Post Types
**Best for:** Solopreneurs who already run WordPress, unlimited scale
**How it works:** Custom post types + ACF (Advanced Custom Fields) or pods. Data imported via CSV/WP All Import or REST API.
**Build complexity:** Medium — requires some WP knowledge, hosting matters for performance
**Strengths:** No page limits, full control, massive plugin ecosystem (RankMath, Yoast for SEO meta)
**Weaknesses:** Performance at scale requires caching (WP Rocket, Cloudflare) and good hosting; more moving parts

### Framer
**Best for:** Designers, visual-first solopreneurs, up to ~5,000 pages
**How it works:** Framer CMS connects to Google Sheets, Airtable, or Notion natively. Template components pull in dynamic fields.
**Build complexity:** Low — drag-and-drop, fastest time-to-launch for non-coders
**Strengths:** Beautiful output, fast hosting, easy iteration on design
**Weaknesses:** CMS limits on lower plans, less SEO control granularity vs WordPress

### Astro (Static Site Generator)
**Best for:** Technical founders, developers, unlimited scale, maximum performance
**How it works:** Markdown/MDX files or API-driven data at build time generates static HTML — zero JS by default.
**Build complexity:** High — requires JavaScript/TypeScript knowledge, Cloudflare or Vercel deployment
**Strengths:** Near-perfect Core Web Vitals, no CMS limits, fully custom, edge deployments
**Weaknesses:** Every change requires a rebuild/redeploy, steeper learning curve, no visual editor

### Notion + Super.so
**Best for:** Very early validation, up to ~500 pages, content-heavy
**How it works:** Notion database becomes public website via Super.so. Each row = one page.
**Build complexity:** Very Low — fastest possible prototype
**Strengths:** Instant publishing, zero code
**Weaknesses:** Limited SEO controls, performance issues at scale, design constraints — use for validation only, not production

---

## Google's Scaled Content Abuse Policy (March 2024)

**This is not theoretical risk. This is a declared Google spam policy.**

In March 2024, Google updated its spam policies and explicitly defined "scaled content abuse" as a penalizable offense. It was previously called "spammy automatically generated content" — the rebrand matters because the new definition covers *any method* of production, not just automated tools.

**Google's definition (verbatim):** Creating large amounts of unoriginal content that provides little to no value to users, no matter how it was created — whether through automation, human effort, or a combination.

**What Google explicitly targets:**
- Pages generated at scale whose primary purpose is ranking manipulation, not user utility
- AI-generated content published in bulk without human review or added value
- Scraped content stitched together from other sources
- Pages where content is garbled, keyword-stuffed, or makes little sense outside of containing search terms
- Doorway pages — thousands of location/query pages that funnel to one generic destination

**Penalties issued:**
- Algorithmic downgrade (loss of rankings, traffic cliff)
- Manual action (can include complete deindexation — the nuclear outcome)
- Manual actions were issued within 24 hours of the March 2024 update rollout for the worst offenders

**What survives:**
Pages built on genuine, differentiated data that serves real user intent. The automation is not the crime. The absence of value is.

Sites like Zapier, Canva, Wise, and Nomad List continue to thrive because each of their pages answers a specific question with data that cannot be found elsewhere in exactly that form.

**The honest risk assessment for 2026:** If your pSEO project cannot answer "what does a user get from this page that they cannot get from any similar page?", you are building toward a penalty, not traffic.

---

## Page Template Structure

A strong pSEO template is structured around the user question, not keyword density.

```
[Entity Name] — [Primary Keyword Variant]  ← H1 (unique per page)

[Hook paragraph — references entity specifically, not generically]  ← 50–80 words

[Unique data block — the thing that makes this page worth indexing]
  - Stat / table / chart / comparison / rating
  - Source cited inline

[Primary content section — answers the core query]
  - Subheadings (H2/H3) using natural language variants
  - At least one concrete example tied to the entity

[Secondary content section — expands utility]
  - FAQ targeting related long-tail variants
  - Use cases or next steps

[CTA — contextual to the entity]
  - Not generic; should reference the entity or use case

[Internal links]
  - To parent category page
  - To 2–3 sibling entity pages
  - To relevant blog/content if applicable

[Structured data]
  - At minimum: Organization or Product schema
  - FAQ schema if FAQ section present
  - BreadcrumbList for category hierarchy
```

Every field marked [unique per page] must pull from your dataset — not be copy-pasted from the template's default text.

---

## Internal Linking at Scale

Internal linking is the most neglected part of pSEO and one of the most important. Without it, your pages are orphans that crawlers may never discover — and users never navigate.

**The hub-and-spoke model for pSEO:**
- **Hub page** (category index): "Best tools for [Category]" or "Project Management in [Region]" — manually written, high editorial quality, links to all spokes
- **Spoke pages** (programmatic): each entity page links back to the hub and cross-links to 2–3 related spokes

**Implementation:**
- In your template, always include a "Related [entities]" section that dynamically pulls 3–5 related pages from the same dataset (e.g. nearby cities, similar tools, same integration category)
- Build a sitemap.xml that lists all pSEO URLs and submit to Google Search Console
- Use breadcrumbs: `Home > Category > [Entity]` — also implement BreadcrumbList schema
- Consider a "directory index" page per letter or category that Google can use as a crawl entry point

**Crawl budget reality:** If you publish 10,000 pages overnight with no internal links and a weak domain, Google will not crawl most of them. Build slowly: publish 100–500 pages, monitor indexation in GSC, then scale.

---

## Common Mistakes

**1. Thin pages with no unique data**
The most common failure. Template created, city/tool name swapped in, published. Every page is functionally identical. Google recognises this within weeks.
Fix: Each page needs at least one data point that is true only for that entity.

**2. No SERP validation before building**
Building 5,000 pages for queries nobody searches, or queries dominated by mega-brands with zero path to ranking.
Fix: Run the SERP analysis in the Validation section above before writing a line of template HTML.

**3. Publishing all pages at once**
Mass-publishing signals low quality to Google. Sites that drop 50,000 pages in a week look like spam operations.
Fix: Publish in batches of 50–500. Monitor GSC for indexation and early ranking signals. Expand only when quality signals are positive.

**4. No internal links**
Orphan pages drain crawl budget and rank poorly.
Fix: Build hub pages and cross-linking into the template before launching.

**5. Bulk AI generation without review**
Running a ChatGPT prompt across 10,000 rows and publishing the output unedited is the fastest path to a manual action in 2026.
Fix: Sample review every batch. Set quality gates. Use AI for structure and drafts; verify all entity-specific facts.

**6. Forgetting to update stale data**
pSEO pages that show outdated pricing, broken integrations, or wrong statistics will earn negative user signals (bounces, short dwell time) that erode rankings.
Fix: Set a data refresh schedule. Use APIs where possible so data updates automatically.

**7. Ignoring Core Web Vitals at scale**
A template with heavy JS, large images, and no caching that performs fine on one page will destroy performance scores across 10,000.
Fix: Test template performance on Lighthouse before launching. Use static generation or aggressive caching.

---

## Contrarian Takes

**pSEO is risky in 2026 without genuine data — more risky than most tutorials admit.**
The case studies everyone cites (Zapier, Wise, Canva) are companies with proprietary datasets, engineering teams, and domain authority. A solopreneur starting from scratch cannot replicate this without an actual data moat.

**Bulk AI pages are the fastest path to a manual action.**
Unedited AI output at scale has been the single most penalised category since March 2024. Using AI for pSEO is fine — using AI as a substitute for genuine data is not.

**1,000 good pages beat 100,000 thin pages — always.**
More pages is not more traffic. More indexed pages with genuine utility is more traffic. Prioritise quality thresholds over volume targets.

**Traffic ≠ business impact.**
Location pages for a SaaS tool often rank and drive zero conversions. Validate that the keyword pattern maps to buyer intent, not just curiosity traffic, before investing months in the build.

**Your data source is your moat, not your template.**
Templates can be copied in a day. A unique dataset that took months to compile cannot be. Invest in the data, not the tech.

---

## Quick Wins (Start Here)

If you want to start without a full pSEO build:

1. **Identify one high-value keyword pattern** from your existing content — look at GSC for queries you almost rank for at positions 5–15 that fit a pattern.
2. **Build 10–20 pages manually** using the pattern. Validate they index and get impressions before scaling.
3. **Pick the easiest data source first** — your own product data, a public government dataset, or a well-maintained open API.
4. **Use Webflow CMS + Airtable** if you are non-technical and want to launch in a week.
5. **Use Astro + Cloudflare Pages** if you are technical and want unlimited scale at near-zero hosting cost.
6. **Set up a GSC property and submit sitemap** before launching page 1 — not after page 1,000.

---

## Related Skills

| Skill | When to use instead |
|---|---|
| **seo-audit** | Diagnosing why existing pages lost rankings or traffic |
| **schema-markup** | Adding JSON-LD structured data to pSEO pages |
| **site-architecture** | Planning the URL structure, hub pages, and navigation |
| **content-strategy** | Deciding what topics to cover before building templates |
| **ai-seo** | Optimising for AI Overviews, ChatGPT, and Perplexity citations |
| **competitor-alternatives** | Writing a single, deeply researched comparison page |

---

*Generated using the programmatic-seo skill from Solopreneur Skills*
