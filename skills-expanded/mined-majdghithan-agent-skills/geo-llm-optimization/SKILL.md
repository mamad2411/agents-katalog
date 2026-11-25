---
name: geo-llm-optimization
description: Generative Engine Optimization (GEO) - make a website citable and recommended INSIDE AI-assistant answers (ChatGPT, Claude, Perplexity, Gemini), not just ranked on Google. Use when the user wants to be found now that people ask AI directly, wants to be a source LLMs pull from, or asks about llms.txt, AI crawler access, JSON-LD/structured data for AI, or "SEO for AI". Covers letting AI crawlers in, extractable content, structured data, authority/E-E-A-T signals, and llms.txt - with concrete implementation.
---

# GEO - Generative Engine Optimization

More and more people skip Google and ask ChatGPT/Claude/Perplexity/Gemini directly. When they do, there is no results page - one synthesized answer. If your content isn't *inside* that answer, you don't exist for that person: no impression, no click, nothing. GEO is how you get into the answer.

**SEO vs GEO:** SEO optimizes so a search engine *ranks* your page and you win a click. GEO optimizes so an AI assistant *cites or recommends you inside its answer* - you win a mention. They share most fundamentals; the target differs. SEO is not dead - do the shared fundamentals well and you play both games with one codebase.

## The five things GEO actually asks (in priority order)

### 1. Let the AI crawlers in (the #1 thing people get backwards)
AI assistants read the web through their own bots. If `robots.txt` blocks them, you've opted out of every AI answer on purpose. Allow them:
```
# robots.txt - allow AI crawlers explicitly (or just Allow: / for User-agent: *)
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended        # Gemini / Vertex training + grounding
Allow: /

Sitemap: https://example.com/sitemap.xml
```
Verify you are not accidentally blocking them at the CDN/WAF layer (Cloudflare "block AI bots" toggles, etc.).

### 2. Be extractable - LLMs lift *claims*
Models pull discrete claims out of your text. Make them easy to lift verbatim:
- Clear, descriptive headings; a direct **definition** near the top of each section.
- Short declarative sentences with **real numbers and sources** ("cut p95 from 800ms to 120ms").
- Answer the actual question plainly instead of burying it under vague prose - the page that says the thing directly gets quoted; the wall of fluff gets skipped.

### 3. Give machines structure (JSON-LD + semantic HTML)
Structured data tells both Google and the models exactly what the page is, who wrote it, and when. Use real `Article`/`BlogPosting`, `WebSite`, and `Person`/`Organization` types - and a `@graph` linking author to site:
```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "…",
  "datePublished": "2026-07-28",
  "author": {
    "@type": "Person",
    "name": "Your Name",
    "jobTitle": "…",
    "sameAs": ["https://www.linkedin.com/in/you", "https://github.com/you"]
  },
  "publisher": { "@type": "Organization", "name": "…" }
}
```
Add a clean `sitemap.xml`, canonical URLs, and OG/Twitter meta. **Do not fake schema** (e.g. a `FAQPage` for Q&As that aren't really on the page) - fabricated structured data is a liability, not a GEO win.

### 4. Build authority / E-E-A-T signals
Models weight sources they can trust: a **named author with a real bio** and `sameAs` links to real profiles (LinkedIn, GitHub), and being *talked about elsewhere*. A large share of GEO is won **off your own site** - in what the rest of the web says about you. Get cited, guest-post, answer where your audience already asks.

### 5. Ship an `llms.txt`
An emerging convention ([llmstxt.org](https://llmstxt.org)): a plain-text/markdown file at your root that points AI crawlers at your best, cleanest content - like a `sitemap.xml` written for models. Generate it from your content:
```
# Example Site
> One-line description of what this site is and who it's for.

## Articles
- [Article title](https://example.com/blog/slug): one-line summary.
- [Another](https://example.com/blog/slug2): one-line summary.

## About
- [Author on LinkedIn](https://www.linkedin.com/in/you)
- [Author on GitHub](https://github.com/you)
```
On Next.js, serve it from a route (e.g. `app/llms.txt/route.ts`) generated from your posts, with ISR so it stays current.

## Implementation checklist
- [ ] `robots.txt` allows GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended (and CDN/WAF isn't blocking them)
- [ ] Every page: canonical URL, semantic headings, a plain-language answer up top
- [ ] Per-page JSON-LD (`Article`/`BlogPosting`) + site-level `WebSite` + `Person`/`Organization` `@graph`
- [ ] Author has a real bio and `sameAs` profile links
- [ ] `sitemap.xml` + OG/Twitter meta present
- [ ] `llms.txt` at root, generated from real content, kept current
- [ ] No fabricated structured data (no fake FAQPage)
- [ ] A plan for off-site mentions/citations (the part you can't do on your own domain)

## Note on non-English
AI answers in under-served languages have far less competition. A deep, well-structured article in a language with little quality web content becomes a default source models reach for - a durable GEO moat.

## Sources
[llms.txt spec](https://llmstxt.org) · [OpenAI GPTBot docs](https://platform.openai.com/docs/bots) · [Google-Extended](https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers) · [schema.org BlogPosting](https://schema.org/BlogPosting)
