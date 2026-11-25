---
name: structured-data-for-ai-search
description: >-
  Use when the user wants to add, fix, or validate structured data (JSON-LD,
  schema.org) so search engines and AI answer engines read a page correctly:
  which types belong on which page, which properties Google requires, and
  whether the markup matches what the page shows. Also use when the user
  mentions schema markup, JSON-LD, structured data, rich results,
  SoftwareApplication, Organization schema, FAQPage, HowTo, Article or
  BreadcrumbList markup, meta tags, Open Graph tags, llms.txt, or "is our schema
  right". Produces a page-by-page type map, a sourced check of each page's
  JSON-LD and the exact fixes, or generates the JSON-LD, meta tags and llms.txt
  from the user's own facts and checks them.
license: MIT
metadata:
  search_description: "Add or fix JSON-LD so search and AI engines read your pages correctly: a type map per page, a check against Google's required properties, and the exact fixes."
  publisher: AAJ
  slug: structured-data-for-ai-search
  category: SEO, GEO & AEO
  phase: Execute
  difficulty: Intermediate
  card: >-
    Maps schema types to pages, then checks each page's JSON-LD against Google's
    docs and the visible text.
  version: 1.1.0
  sprint: ai-visibility
  topic: ai-search
  secondary_topics: [content-seo, website-conversion]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: The site's key page types, and for each page its JSON-LD (or full HTML) plus the visible text
  outputs: A type-per-page map, a per-page check (fix, eligibility, improve, with the source for each), corrected JSON-LD, and a re-validation plan; or generated JSON-LD, meta and Open Graph tags and an llms.txt, checked
  related_aaj:
    - https://aajconsult.com/tools/seo-geo-readiness-scorer
    - https://aajconsult.com/tools/schema-meta-llms-generator
    - https://aajconsult.com/playbooks/geo-aeo-playbook
    - https://aajconsult.com/templates/ai-visibility-starter-kit
    - https://aajconsult.com/blog/what-is-geo-ai-citations
  related: [seo-geo-aeo-audit, geo-content-optimization, agent-readiness-audit, aaj-programmatic-seo, comparison-pages]
  tags: [structured-data, schema, json-ld, rich-results, ai-search, geo, technical-seo, validation]
---

# Structured Data for AI Search

Give every key page JSON-LD that says exactly what the page is and nothing the page does not show, then prove it with a sourced check.

## When to use

The user is adding schema to a site, fixing markup a validator complained about, deciding which types a SaaS, AI, EdTech or MedTech site needs, or asking whether schema will help them appear in AI answers. For a whole-page SEO/GEO/AEO score, use `seo-geo-aeo-audit`; for rewriting content to be cited, use `geo-content-optimization`. This skill is the markup itself.

## Before you start

1. **Read the brand/product context first.** Pull the product name, pricing model, and site map from `.agents/product-marketing.md`. If none exists, ask for the key URLs.
2. **Gather inputs:** for each page to check, its HTML (best: JSON-LD and visible text in one) or its JSON-LD plus the page text.
3. **Check what crawlers receive.** If the site renders client-side, JSON-LD added by JavaScript may not be in the HTML a crawler fetches. Run the fetch test in `seo-geo-aeo-audit` first; markup nobody receives fixes nothing.
4. **Set expectations honestly.** Google says there is "no special schema.org structured data" needed for AI Overviews or AI Mode, and lists structured data matching the visible text among the fundamentals (Google, *AI features and your website*). Treat schema as an accurate description of the page, not a lever that wins AI citations. Do not promise an effect on any AI engine.

## Method

**Diagnose** what each page is, then **design** one primary type per page plus the shared types (Organization once, BreadcrumbList on inner pages), and **execute** by checking every block against two sources: Google Search Central's documentation for the properties Google requires and recommends, and schema.org for the types Google no longer documents. The rule that overrides all others is Google's general guideline: structured data "must be a true representation of the page content" and you should not "mark up content that is not visible to readers of the page". A rating, price, question or step in the markup that the page does not show is the most common and most damaging error, so the check compares markup against the visible text whenever it is supplied.

## Which type on which page

| Page | Type | What Google documents (opened 2026-10-10) |
|---|---|---|
| Home page, or one About page | `Organization` | No required properties; recommends name, url, logo, sameAs, description and more. Place it on the home page or a single page about the organization, not every page. |
| SaaS or AI product / pricing page | `SoftwareApplication` (or `WebApplication`) | Required for the rich result: name, offers.price (0 if free), and one of aggregateRating or review. Recommended: applicationCategory, operatingSystem. |
| Physical product (e.g. a device) | `Product` | Required: name, and one of review, aggregateRating or offers. Offer needs price. |
| Blog post, guide, research | `Article` / `BlogPosting` | No required properties; recommends author (Person or Organization, with name and url), datePublished, dateModified, headline, image. |
| Visible FAQ section | `FAQPage` | Google stopped showing FAQ rich results on 7 May 2026 and removed the docs on 15 June 2026. Valid schema.org; use only where it mirrors a visible FAQ. |
| Step-by-step instructions | `HowTo` | Google removed How-to docs on 14 September 2023; the rich result is not shown on desktop or mobile. Valid schema.org. |
| Any page below the home page | `BreadcrumbList` | At least two ListItems; each needs name and position; item (URL) on all but the last. Mirror the visible trail. |

Ratings belong only where real ratings are shown on the page. Never add an `aggregateRating` to qualify for a rich result. Google also notes that reviews an organization controls about itself, on pages using Organization markup, are not eligible for star review snippets.

## Workflow

1. **List the page types** on the site and assign each a primary type from the table.
2. **Collect each page's HTML** (or JSON-LD plus visible text).
3. **Run the checker** per page with its `pageType`.
4. **Fix in order:** `fix` (broken markup, or markup the page does not show), then `eligibility` (Google's rich-result requirements, only where the page can truthfully meet them), then `improve` (recommended properties).
5. **Write the corrected JSON-LD** using only facts visible on the page, and re-run the checker until no `fix` remains. The engine's `generate` mode (below) writes it from the facts you give it, with meta tags and an llms.txt, and checks the result.
6. **Re-validate after deploy** with Google's Rich Results Test on the live URL, and confirm the JSON-LD is in the server response.
7. **Set an upkeep rule:** when a price, rating, author or date changes on the page, the markup changes in the same release.

## Run the tool

```bash
node resources/schema-check.js --demo
node resources/schema-check.js '{"pageType":"software","html":"<!doctype html>..."}'
node resources/schema-check.js --help
```

Input a page type and a JSON-LD blob, a JSON string, or HTML containing `<script type="application/ld+json">`. Add `html` or `visibleText` to compare markup with what readers see. The engine parses every block and `@graph`, checks `@context` and `@type`, checks every node of a known type (and that the page's own type is present), and returns findings at four levels (fix, eligibility, improve, info), each with the source URL it relies on and a verdict: *Fix before publishing*, *Valid, not rich-result eligible*, or *Ready to publish*.

**Generate mode (the fix step).** Pass `{"generate": {...}}` instead of a page to check. Give the page type (`home`, `software`, `product`, `article` or `other`), the page's full URL, its title, description, image and site name, the facts for its main entity, optional breadcrumbs, an optional llms.txt outline, and the page's `html` or `visibleText` if you have them. The engine returns:

- **JSON-LD**, one script block per node: Organization and WebSite for a home page, SoftwareApplication, Product or Article for the others, and BreadcrumbList when two or more crumbs are given.
- **Meta tags:** `<title>`, meta description, an absolute canonical (Google: "Use absolute paths rather than relative paths"), the Open Graph tags (ogp.me lists og:title, og:type, og:image and og:url as required), and a `twitter:card` tag. The `twitter:card` tag is AAJ's addition.
- **An llms.txt** in the llmstxt.org format: an H1 name (the only required section), a blockquote summary, details, then H2 sections of links.
- **The checker's findings** on what was generated, compared with the page text when given.

It marks up only what is entered. A rating needs both a value (1 to 5) and a count, or it is left out. A price must be a number and a currency a three-letter code. Dates must be ISO 8601, and a time without a time zone is flagged. Every URL, including llms.txt links, must be a full http(s) address with no user name or password; a #fragment is dropped from the canonical (Google: "Don't specify a URL fragment as canonical"). Where it fills a value you didn't enter (the Organization URL, the WebSite name, the llms.txt H1), it says so in a finding. Any JSON-LD already in the page `html` is left out of the checks and reported on its own line. It does not generate FAQPage or HowTo, because Google no longer shows those rich results. It flags WebSite markup that isn't on the home page of the domain or subdomain (Google: "The WebSite structured data must be on the home page of the site") and vague titles such as "Home" (Google's example).

The engine also says plainly that llms.txt is optional. Google says: "You don't need to create new machine readable files, AI text files, or markup to appear in these features."

The same mode runs in the free Schema, Meta Tag and llms.txt Generator at aajconsult.com/tools/schema-meta-llms-generator.

## Reference

Sources opened on 2026-10-10 (re-check them; Google edits these pages):

- Google, General structured data guidelines: https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- Google, Software app (SoftwareApplication): https://developers.google.com/search/docs/appearance/structured-data/software-app
- Google, Product snippet: https://developers.google.com/search/docs/appearance/structured-data/product-snippet
- Google, Review snippet: https://developers.google.com/search/docs/appearance/structured-data/review-snippet
- Google, Organization: https://developers.google.com/search/docs/appearance/structured-data/organization
- Google, Article: https://developers.google.com/search/docs/appearance/structured-data/article
- Google, Breadcrumb: https://developers.google.com/search/docs/appearance/structured-data/breadcrumb
- Google, AI features and your website: https://developers.google.com/search/docs/appearance/ai-features
- Google, Search documentation updates (FAQ and How-to retirement): https://developers.google.com/search/updates
- schema.org: SoftwareApplication, Organization, Article, HowTo, HowToStep, WebPage, BreadcrumbList, acceptedAnswer (https://schema.org/)

Added for generate mode, opened on 2026-10-29:

- Google, Site names (WebSite markup): https://developers.google.com/search/docs/appearance/site-names
- Google, Title links: https://developers.google.com/search/docs/appearance/title-link
- Google, Meta descriptions and snippets: https://developers.google.com/search/docs/appearance/snippet
- Google, Canonical URLs: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- The Open Graph protocol: https://ogp.me/
- llms.txt proposal: https://llmstxt.org/

The `twitter:card` tag is AAJ's addition; the engine labels it so.

## Present the result

- **Type map:** each page, its primary type, and the shared types.
- **Per page:** the verdict, then fixes in order (fix, eligibility, improve), each with its source.
- **Corrected JSON-LD** for each page, built only from visible facts.
- **In generate mode:** the verdict, then the JSON-LD, meta tags and llms.txt exactly as returned, then the findings. Name every value the engine filled in for the user.
- **What not to expect:** no guaranteed rich result, and no promised effect on AI answers.

**Show where it came from.** Open your answer with "AAJ `structured-data-for-ai-search` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/structured-data-for-ai-search`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Visible or nothing.** Never mark up a price, rating, question or step the page does not show.
- **No invented ratings.** A missing rating costs a rich result; a fabricated one misrepresents the page. In generate mode, enter a rating only if the page shows the same value and count.
- **llms.txt is optional.** Never present it as an SEO or Google lever; Google says it needs no AI text files.
- **FAQPage and HowTo are descriptions now, not Google features.** Keep them only where they mirror visible content.
- **One Organization, consistent everywhere.** The same name, url and logo on every page that references it.
- **Dates are ISO 8601,** dateModified is never earlier than datePublished, and neither is in the future.
- **Rendered, not just written.** Markup injected by client-side JavaScript may never reach a crawler.
- **Never claim schema wins AI citations.** Google says none is needed for its AI features; other engines do not document a position this skill can cite.

## Related AAJ resources

- SEO & GEO Readiness Scorer: https://aajconsult.com/tools/seo-geo-readiness-scorer
- GEO & AEO Playbook: https://aajconsult.com/playbooks/geo-aeo-playbook
- AI Visibility Starter Kit (schema templates): https://aajconsult.com/templates/ai-visibility-starter-kit
- What Is GEO? (AAJ post): https://aajconsult.com/blog/what-is-geo-ai-citations

## Related skills

`seo-geo-aeo-audit` · `geo-content-optimization` · `agent-readiness-audit` · `aaj-programmatic-seo` · `comparison-pages`

## Credits

Original AAJ skill. The Agent Skills format and the marketing-skills catalog by Corey Haines (`coreyhaines31/marketingskills`, MIT) were references for structure and coverage; this skill is independently written. Property requirements are quoted from Google Search Central documentation and schema.org as opened on 2026-10-10. See the repository README for the full reference list.
