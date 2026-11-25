---
name: findable
description: Autonomous SEO/GEO research and optimization skill — searches the web for best practices, applies safe improvements automatically, and documents sensitive changes in TODO SEO.md
when_to_use: when you want to improve a project's visibility in search engines and AI recommendations
version: 1.1.0
languages: all
---

# Findable

> Research deep. Apply safe. Document sensitive. Never stop.

---

## What it does

When invoked, Findable runs an autonomous loop:

1. Searches GitHub, GitLab, Google, forums, and docs for current SEO/GEO best practices
2. Reads the project to understand its stack and context
3. Applies **safe changes** immediately (new files, additions, metadata)
4. For **sensitive changes**, creates or updates `TODO SEO.md` with full details
5. Reports what was found, what was applied, what was queued
6. Repeats — keeps researching and improving until the user says to stop

---

## Search scope

Every research cycle covers:

- **SEO** — technical SEO, on-page optimization, structured data (JSON-LD), Core Web Vitals, sitemaps, robots.txt, canonical URLs
- **GEO** (Generative Engine Optimization) — how AI systems discover, crawl, and recommend content
- **llms.txt** — the emerging standard for AI-readable site context ([llmstxt.org](https://llmstxt.org))
- **AI visibility** — appearing in ChatGPT, Perplexity, Claude, Gemini, and other LLM recommendations
- **Rich results** — Open Graph, Twitter Cards, structured data, rich snippets
- **Crawlability** — robots.txt, sitemap.xml, internal linking, page speed

Sources to search: GitHub repos, GitLab projects, Google Search, Hacker News, dev.to, Reddit (r/SEO, r/webdev), Stack Overflow, official docs (Google Search Central, schema.org, llmstxt.org, web.dev)

### Community/social research — prefer last30days

For anything community- or sentiment-driven — what people are actually saying right now on Reddit, Hacker News, X, etc. about SEO/GEO/AI-visibility practices — invoke the `last30days` skill first if it's available. It aggregates and engagement-ranks real posts across Reddit, HN, X, YouTube, TikTok, and GitHub, which plain web search frequently fails at (queries like `site:reddit.com OR site:hn.algolia.com` often return nothing useful from web search alone).

### Blocked research — optional `web`/unblock skill

If a source comes back blocked, paywalled, or empty (403/429, CAPTCHA, thin/garbage result) and the `web` skill (aka "unblock") is installed, it may be invoked to push through via its fallback chain instead of just discarding that source. This is purely optional: never required, never installed on demand, never a reason to pause a cycle. If it isn't installed, or a query isn't worth the extra hop, just move on to the next query.

Priority order per cycle:
1. Try `last30days` for the community/sentiment angle of the current research question.
2. Regardless of whether it finds anything, still run the normal web search queries below — they cover official docs and general guides that `last30days` doesn't target.
3. If `last30days` isn't installed, skip straight to web search — don't block the cycle on it.
4. For a source that comes back blocked or empty, optionally try `web` if installed — otherwise skip it and keep going.

---

## Reading before touching

**Never modify a file without reading it first.**

For every file the skill might touch:
1. Read it completely
2. Understand the project stack and what the file does
3. Decide: safe change (apply) or sensitive change (document in TODO SEO.md)

---

## Safe changes — apply automatically

Apply without asking when the change is purely additive and cannot break existing behavior:

- Creating `robots.txt` (when it does not exist)
- Creating `sitemap.xml` (when it does not exist)
- Creating `llms.txt` (when it does not exist)
- Adding `<meta>` tags: title, description, `og:*`, `twitter:*`
- Adding JSON-LD structured data blocks
- Adding `<link rel="canonical">` tags
- Creating `humans.txt`
- Adding `alt` text to images that have none
- Creating documentation files: `SEO.md`, `FINDABLE.md`

---

## Sensitive changes — document in TODO SEO.md

For anything that modifies existing structure, configuration, or behavior — create or update `TODO SEO.md` in the project root.

Sensitive change examples:
- Changing URL structure or routing
- Modifying existing HTML structure or layout
- Changing navigation, menus, or link hierarchy
- Modifying build configs, server configs, `.htaccess`, `nginx.conf`
- Changing meta tags that were deliberately set
- Restructuring content or pages
- Editing an existing `robots.txt`, `sitemap.xml`, or `llms.txt` — the safe-change list above only covers creating these when absent; once one exists, treat any edit to it as sensitive
- Any change where the right answer depends on the specific stack

### TODO SEO.md format

```markdown
# TODO SEO

> Last updated: YYYY-MM-DD

## Pending Changes

### [Change title]
- **Source:** [URL of the best practice, repo, or article found]
- **What:** [Exactly what will be done]
- **Where:** [Which file(s) will be touched, with line numbers when possible]
- **Why:** [Why this improves SEO / GEO / AI visibility]
- **Risk:** [What could break or needs verification before applying]
- **Effort:** Low / Medium / High
```

---

## Research queries

Use web search with queries like:

```
SEO best practices site:github.com
llms.txt specification
GEO generative engine optimization guide
how LLMs crawl and recommend websites
structured data JSON-LD best practices schema.org
robots.txt best practices
sitemap.xml optimization tips
Core Web Vitals optimization
Open Graph meta tags complete guide
AI visibility SEO recommendations site:reddit.com OR site:hn.algolia.com
technical SEO checklist site:dev.to
```

Add the current year to a query only when freshness genuinely matters (e.g. "Core Web Vitals thresholds 2026") — a hardcoded year goes stale the moment the calendar turns and biases results toward outdated pages.

---

## Research loop

After each cycle:
1. If `last30days` is available, use it first for the community/sentiment angle — then search the web regardless of what it turns up
2. If a search comes back blocked or empty, optionally invoke `web` (if installed) to try harder — skip this step entirely if `web` isn't installed or it's not worth the hop
3. Read the project state (files, stack, existing SEO setup)
4. Apply safe changes or add to `TODO SEO.md`
5. Report: what was searched, what was found (with URLs), what was applied, what was queued
6. Repeat

Stop when one of these is true:
- The user says to stop
- There is nothing left to find or apply (all known improvements are either done or in `TODO SEO.md`)
- Context is running out

If context fills before finishing, update `TODO SEO.md` with current state. A new session can resume by reading `TODO SEO.md`.

---

## Reporting format

After each cycle, output:

```
## Findable — Cycle N

**Searched:** [queries used]
**Found:** [source URLs with one-line summary each]
**Applied:** [files created or changed, with reason]
**Queued in TODO SEO.md:** [changes documented, not yet applied]
**Next:** [what the next cycle will focus on]
```

---

## Compatibility

Works in any project with web presence:
- Static sites (HTML, Jekyll, Hugo, Eleventy, Astro)
- Next.js, Nuxt, SvelteKit, Remix
- Backend apps with HTML output (Rails, Django, Laravel, Express)
- Documentation sites (Docusaurus, VitePress, GitBook)
- Any project that needs to be found
