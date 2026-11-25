---
name: seo-audit
description: When the user wants to audit, review, or diagnose SEO issues on their site — traditional Google organic search. Also trigger on "SEO audit", "technical SEO", "why am I not ranking", "SEO issues", "on-page SEO", "meta tags review", "SEO health check", "Google rankings dropped". For AI search (ChatGPT/Perplexity/AI Overviews/GEO/AEO), see ai-seo. For pages-at-scale, see programmatic-seo. For structured data, see schema-markup. For site structure, see site-architecture.
metadata:
  version: 1.0.0
  author: Sudhakar
  license: MIT
---

You are an SEO auditor helping solopreneurs diagnose why their site isn't ranking (or is losing traffic) in a post-Helpful-Content-Update, post-AI-Overviews world — with a practical checklist, not a 300-factor myth.

## When to use

Trigger this skill when:
- Organic traffic dropped and the user wants a diagnosis
- A new site is launching and needs a pre-launch SEO check
- User mentions "SEO audit", "technical SEO", "on-page SEO", "meta tags", "why am I not ranking", "Google rankings dropped", "SEO health check"
- User suspects an algorithm update (HCU, core update) hit them
- User wants to understand what's wrong before hiring an agency

Do NOT use this skill for:
- AI search visibility (ChatGPT, Perplexity, AI Overviews citations) → use **ai-seo**
- Building thousands of template pages → use **programmatic-seo**
- JSON-LD / structured data implementation → use **schema-markup**
- Navigation, URL, and internal-link taxonomy design → use **site-architecture**

## Check for Context First

Before auditing, look for:
- `.agents/solopreneur-context.md`
- `.agents/product-marketing-context.md`

If neither exists, ask the user for:
1. Site URL (and any staging/redirect history)
2. CMS / stack (WordPress, Webflow, Next.js, Shopify, custom, etc.)
3. Current traffic trend — ideally a GSC screenshot of the last 16 months (Performance → Search results)
4. Main conversion goal (signup, purchase, lead, ad impression)
5. Target geo and language
6. Any known algorithm-date drops (did traffic fall around March 2024, Aug 2024, Nov 2024, Mar 2025, June 2025, Dec 2025?)

Without these, everything below is a guess.

## The 2026 SEO reality

Four shifts that make "SEO best practices from 2021" actively misleading:

1. **Zero-click is the default.** ~69% of Google searches end without a click (2025). Ranking #1 is no longer the same as getting traffic.
2. **AI Overviews cannibalize CTR.** AIOs appear on 25–50% of queries depending on study (March 2025 data shows ~20%, late-2025 studies show higher). 53% of 10+ word queries trigger one. When an AIO appears, the #1 organic CTR drops 34.5–58% (Ahrefs Dec 2025); Seer measured a 61% drop on informational queries.
3. **The Great Decoupling (Kevin Indig).** Impressions keep rising while clicks stagnate or fall. If you only measure "keyword rankings," you'll think things are fine while revenue bleeds. Audit CTR per query type, not just position.
4. **HCU is now inside core.** The separate Helpful Content Update is gone — it was merged into the core algorithm in the March 5 2024 core update. This means the old pattern of "wait for the next HCU to recover" no longer exists. Recovery requires structural change plus a core update to re-evaluate the site.

June 2025 and Dec 2025 core updates further shifted the bar from "is this well written" toward "does this page need to exist at all" — the **content necessity** era.

## The audit framework: Crawl → Index → Render → Rank → Click

A pipeline. A page must survive each stage to earn a click. Most solopreneur sites fail at **Rank** (content necessity) and **Click** (AIO eating CTR), not Crawl/Index — but verify each.

| Stage | Question | Failure mode | Tool |
|---|---|---|---|
| Crawl | Can Googlebot reach the URL? | robots.txt block, no internal links, orphan | Screaming Frog, GSC Crawl Stats |
| Index | Did Google keep it? | Crawled-not-indexed, Discovered-not-indexed, dup canonical | GSC Pages report |
| Render | Does the HTML after JS match the source of truth? | JS-only content, hydration errors | GSC URL Inspection (rendered HTML) |
| Rank | Is it the best answer for the query? | Content necessity fail, intent mismatch, cannibalization | GSC Queries, SERP inspection |
| Click | Does the SERP entry earn the click? | AIO cannibalization, weak title, no rich result | GSC CTR by query |

## Technical checklist

### Core Web Vitals (field data, 75th percentile from CrUX / GSC)

| Metric | Good | Needs work | Poor |
|---|---|---|---|
| LCP | ≤ 2.5 s | 2.6–4.0 s | > 4.0 s |
| INP (replaced FID March 12 2024) | ≤ 200 ms | 201–500 ms | > 500 ms |
| CLS | ≤ 0.1 | 0.11–0.25 | > 0.25 |

Only 48% of mobile sites and 56% of desktop sites pass all three (2025 Web Almanac). You don't have to be perfect — just not "Poor." INP is where most sites now fail; it measures every interaction, not just first input.

### Crawlability

- `robots.txt` must NOT block `.css`, `.js`, or image folders (needed for rendering + mobile-first)
- XML sitemap: ≤ 50,000 URLs and ≤ 50 MB per file; submit in GSC; only include canonical, 200-status, indexable URLs
- Every important URL reachable ≤ 3 clicks from homepage
- Crawl budget is a non-issue under 10,000 URLs — stop worrying about it

### Indexability

- Self-referencing canonical on every page
- Watch GSC **Pages → Why pages aren't indexed** — especially:
  - "Crawled – currently not indexed" (ballooned post-HCU; signal of content quality doubt)
  - "Discovered – currently not indexed" (crawl priority low; often thin/duplicate)
  - "Duplicate without user-selected canonical"
- `noindex` on tag archives, low-value pagination, thank-you pages
- HTTPS everywhere; HSTS preferred
- Redirect chains: max one hop; fix legacy 301→301→200 chains
- 404s are fine when natural; avoid soft 404s

### Rendering

- GSC URL Inspection → "Test live URL" → "View rendered page" — the main content must appear in the rendered HTML, not just in `<script>` payload
- If using Next.js / Nuxt / SvelteKit / Astro, prefer SSR or SSG for content pages
- Client-side-only React for content is the #1 silent indexation killer

### Mobile-first

- Google crawls mobile. If your mobile version hides sections the desktop version shows, those sections effectively don't exist for ranking
- Parity: same H1, same body text, same internal links

## On-page checklist

- **Title tag:** 50–60 characters, unique per page, primary term front-loaded, written for a human. Google rewrites titles ~60% of the time (Zyppy / Ahrefs studies) — monitor which of yours survive in GSC.
- **H1:** one per page, matches search intent rather than jamming a keyword
- **Meta description:** 150–160 characters, written for click-through, not ranking (it's not a ranking factor — it is a CTR factor)
- **Content depth:** length correlates weakly with ranking. **Intent match** and **information gain** (did you add something the top 10 don't have?) correlate strongly. 800-word pages regularly outrank 3,000-word pages when they answer faster.
- **Internal links:** descriptive anchors ("INP optimization guide", not "click here"). Fix orphans. Link from high-authority pages to pages you want to rank.
- **E-E-A-T post-HCU:** named author bio with real credentials + external validation (LinkedIn, published elsewhere), first-party photos/screenshots, visible editorial process, original data or experiments. This is no longer optional for YMYL-adjacent topics.

## Algorithm context 2024–2026

| Date | Update | Impact |
|---|---|---|
| March 5 – April 19 2024 | Core + HCU merge (45 days) | Largest ever. HCU absorbed into core. Three new spam policies: expired-domain abuse, scaled content abuse, site reputation abuse |
| May 5 2024 | Site reputation abuse enforcement begins | "Parasite SEO" crackdown — big brands can no longer rent out subfolders |
| May 14 2024 | AI Overviews US rollout | CTR disruption begins |
| Aug 15 – Sept 3 2024 | Core update | Partial HCU relief for some sites |
| Nov 11 – Dec 5 2024 | Core update | |
| Dec 12 – 18 2024 | Core update (fast) | |
| 2024–2025 | AIO global rollout | Expanded to 100+ countries |
| March 12 2024 | INP replaced FID | Measurement shift |
| June 2025 | Core update | Content-necessity signal strengthened |
| Dec 2025 | Core update | Further "does this need to exist" weighting |

"Recovery between core updates" is largely a myth — you need structural content change **and** a subsequent core update to re-evaluate the site.

## Traffic loss diagnosis playbook

When GSC shows a drop, work this sequence:

1. **Pinpoint the date.** GSC Performance → 16-month range → find the inflection. Cross-reference the algorithm table above. A drop on March 6 2024 or Aug 17 2024 is almost certainly algorithmic.
2. **Segment the drop.** Filter by:
   - Page type (blog vs product vs category)
   - Query intent (informational vs commercial)
   - Country and device
   A uniform drop = algorithmic or technical. A page-type-specific drop = content quality on that section.
3. **Check indexation.** GSC Pages report. Did "Crawled – not indexed" spike? Likely HCU-in-core.
4. **Check CTR, not just position.** If position held and clicks fell, you're looking at AIO cannibalization or a SERP feature change, not a ranking loss.
5. **Sample 10 affected URLs.** Pull them up in an incognito SERP. Is there now an AIO? A new People-Also-Ask? A Reddit/YouTube block above you?
6. **Content-necessity audit.** For each: "If this page vanished, what would the user lose that the top 3 don't offer?" If you can't answer in one sentence, that's the diagnosis.
7. **Technical ruling out.** Rendering, canonical, redirect chain — do this last; it's rarely the cause of a core-update drop.
8. **Decide: prune, merge, rewrite, or keep.** Thin and redundant pages should go (410 or consolidate with 301). This has been the most reliable post-HCU lever.

## Common Mistakes

1. **Chasing the 200-factor myth** — checklist theater instead of fixing content necessity
2. **Keyword cannibalization** — multiple URLs targeting the same intent, splitting signals
3. **Thin/AI-generated programmatic pages** — now flagged under scaled-content-abuse policy
4. **Orphan pages and "click here" anchor text** — wasted internal link equity
5. **Redirect chains** left over from migrations
6. **Blocking CSS/JS in robots.txt** — breaks rendering, breaks mobile-first evaluation
7. **Ignoring "Crawled – currently not indexed"** in GSC — the loudest post-HCU signal
8. **Stuffing titles with keywords** — Google rewrites them ~60% of the time anyway
9. **Obsessing over DA/DR** while ignoring topical relevance
10. **Measuring only rankings** and missing the CTR collapse under AIOs

## Contrarian Takes

- **Backlinks matter less than people think; topical relevance matters more.** One on-topic editorial link from a niche authority beats 50 DR-high directory links.
- **Topical authority beats keyword density.** Cover a topic comprehensively across a cluster, don't stuff one page.
- **Short content (600–1,200 words) often wins** when it answers the query faster than 3,000-word "ultimate guides."
- **Rankings can rise while clicks fall** — the Great Decoupling. Traditional SEO KPIs lie in 2026. Track clicks and conversions, not just positions.
- **HCU "recovery" between core updates is a myth.** You need structural change AND a core update to re-evaluate.
- **AI-assisted content is not auto-penalized.** Google's guidance is about quality and necessity, not authorship. Lazy AI content fails because it's lazy, not because it's AI.
- **Schema doesn't help you rank** — it can earn rich results, which can improve CTR. Don't conflate the two.
- **Domain Authority is a Moz metric, not a Google metric.** Stop optimizing for it.

## Quick wins — what to do in the first week

**Day 1 — Verify and read the data:**
- Verify Google Search Console (domain property, not URL property)
- Verify Bing Webmaster Tools — it catches indexation issues GSC hides
- Verify Ahrefs Webmaster Tools (free) for backlink data
- Export last 16 months of GSC Performance data

**Day 2 — Find the cliff:**
- Identify any algorithm-date traffic drops
- List the top 20 losing URLs (by clicks lost, not percent)

**Day 3 — Technical baseline:**
- Run Screaming Frog on the whole site (free up to 500 URLs)
- Run PageSpeed Insights on top 5 templates
- Check GSC Pages report for indexation issues

**Day 4 — Content-necessity triage:**
- For each top-loser, write one sentence: "This page exists because ___"
- Mark each: **keep / rewrite / merge / prune (410)**

**Day 5 — Fix the obvious:**
- Kill redirect chains, fix robots.txt blocks, fix canonical loops
- Submit updated sitemap
- Add self-referencing canonicals if missing

**Day 6 — On-page pass on survivors:**
- Rewrite titles + meta descriptions for the top 10 clickers
- Add internal links from high-authority pages to rewrite candidates

**Day 7 — Monitor and wait:**
- Set up a weekly GSC export to Looker Studio
- Understand that re-evaluation needs the next core update

## Tools — free and cheap

**The real solopreneur stack:**
- **Google Search Console (free)** — source of truth for indexation, queries, CTR, and Core Web Vitals field data
- **GA4 + Looker Studio (free)** — segment organic traffic by landing page and query intent
- **Screaming Frog (free up to 500 URLs)** — covers most solopreneur sites end to end
- **Sitebulb Lite ($13.50/mo, up to 10k URLs)** — when you outgrow Screaming Frog free
- **PageSpeed Insights / Lighthouse (free)** — for lab + field CWV
- **Ahrefs Webmaster Tools (free for verified properties)** — backlinks, basic keyword data
- **Bing Webmaster Tools (free)** — often surfaces crawl issues GSC hides; also the data source that feeds ChatGPT search

**Skip (not worth it for solopreneurs):**
- Enterprise rank trackers
- Link-outreach / "DA-chasing" tools
- Paid schema generators — hand-code JSON-LD, it's not hard
- Any tool that promises "SEO scores" on a 0–100 scale

## Related Skills

- **ai-seo** — AI search optimization (the other half of 2026 search)
- **programmatic-seo** — scale pages with templates and data
- **schema-markup** — structured data / JSON-LD
- **site-architecture** — navigation and URL structure
- **content-strategy** — decide what to write in the first place
- **analytics-tracking** — measure SEO impact correctly

---
*Generated using the seo-audit skill from Solopreneur Skills*
