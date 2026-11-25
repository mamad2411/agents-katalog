---
name: scraperapi-seo-audit
description: >
  Run a comprehensive SEO audit using ScraperAPI's live SERP and scraping tools — no setup required.
  Use this skill whenever the user wants to: audit SEO for a website, understand why a page isn't
  ranking, check SEO health, analyze keyword rankings, compare against competitors in search results,
  find content gaps, review on-page signals (titles, meta, headings, schema), diagnose a traffic drop,
  check indexation, or get prioritized SEO recommendations. Also trigger when the user says things like
  "why am I not showing up on Google," "my traffic dropped," "how do I rank for X," "what's wrong
  with my SEO," "SEO check," or "SEO review." This skill works out of the box — it uses the
  ScraperAPI MCP tools already connected to this session, with no CLI or API key setup needed.

  Note: Transmits user-supplied queries, URLs, and content to ScraperAPI.
metadata:
  openclaw:
    requires:
      env:
        - SCRAPERAPI_API_KEY
    emoji: "📈"
    homepage: https://docs.scraperapi.com/
---

# ScraperAPI SEO Audit

Live SEO analysis powered by ScraperAPI's real-time SERP and scraping tools. No CLI installation or API key setup required — the tools are already connected. The approach is outside-in: start with what Google is actually showing, then scrape pages to explain why.

**You — Claude — execute the tool calls directly.** Do not generate code for the user or explain how they could run these calls themselves. Call the MCP tools, read the results, and report findings. The user wants an SEO audit, not instructions.

**Never fabricate findings.** Every finding must cite the exact tool call and output that supports it. If something can't be measured with these tools, say so and note the right external tool.

---

## MCP Tools Available

| Tool | What it returns |
|------|----------------|
| `mcp__ScraperAPIRemote__google_search` | Live structured SERP — organic rankings, featured snippets, People Also Ask, AI Overview presence, knowledge panels, sitelinks. Returns parsed JSON, not raw HTML. Supports geo-targeting via `countryCode` and `gl` parameters. |
| `mcp__ScraperAPIRemote__scrape` | Full page content with JS rendering — use `outputFormat: "markdown"` for content extraction and word count, `outputFormat: "html"` for schema markup, meta tags, and canonical inspection |
| `mcp__ScraperAPIRemote__google_news` | Brand and topic mention recency — useful for E-E-A-T and freshness signals |

### Render guidance for `scrape`
When calling `mcp__ScraperAPIRemote__scrape`, set `render=true` and `premium=true` for any page that requires JavaScript to display content — React/Next.js apps, SPAs, Webflow sites with client-side rendering. Use standard (no render flags) for static HTML: WordPress sites, GitHub, news articles. If the returned HTML has an empty `<head>` or missing body content, escalate to `render=true, premium=true` and retry.

---

## Core Workflow

For every SEO audit request:

1. **Probe for missing parameters** — Confirm URL, target keywords, geography, and scope before starting (see Parameter Probing below).
2. **Select mode** — Single-Page Audit (Mode A) or Site-Wide Audit (Mode B).
3. **Stage 1** — Indexation & SERP Snapshot.
4. **Stage 2** — Keyword Visibility + AI Overview Check.
5. **Stage 3** — On-Page Analysis.
6. **Stage 4** — Competitor Gap Analysis.
7. **Stage 5** — Brand & Freshness Signals.
8. **Calculate health grade** and write report using `references/report-template.md`.

## Data Collection Rules

- **Parallelize** — Within each stage, issue all tool calls in a single response turn. Never loop sequentially over pages or keywords.
- **Be efficient** — Mode A targets ~8–12 tool calls. Mode B targets ~20–30. If you need more, tell the user and ask how to prioritize.
- **Always geo-target** — Pass `countryCode` and `gl` to every `google_search` call for the user's target market. US is the default; always confirm geography before starting.
- **Handle render failures** — If a page returns empty or near-empty content, retry once with `render=true, premium=true`. Note the escalation in the report.
- **Cite every finding** — Include the exact query or URL. Users must be able to trace every claim back to a tool call.
- **Date-stamp every report** — Include "Audited: [date]" so users know how fresh the data is.

---

## Parameter Probing

Check the user's request for these four parameters. Ask all unclear parameters in one message — never one at a time. Infer what you can from context before asking.

| Parameter | Default if not specified | When to ask |
|-----------|--------------------------|-------------|
| **Site URL** | — | Always ask if not provided |
| **Target keywords** | Infer from homepage content after scraping | Confirm inferred keywords before proceeding |
| **Target market / geography** | United States | Always ask — a UK site's rankings on google.com tells you nothing useful |
| **Audit scope** | Mode B (site-wide) for bare domains; Mode A (single-page) for full URL paths | Ask only if genuinely ambiguous |

---

## Audit Modes

### 1. Single-Page Audit (Mode A)

**When to use**: User gave a specific URL, asked why a particular page isn't ranking, or has a narrow question about one page's SEO performance. ~8–12 tool calls.

**Data gathering**:
```
# Stage 1: Indexation check (run in parallel)
mcp__ScraperAPIRemote__google_search  query="site:[domain]"  countryCode="[cc]"  gl="[cc]"
mcp__ScraperAPIRemote__google_search  query='"[Brand Name]"'

# Stage 2: Keyword visibility — one per target keyword (run in parallel)
mcp__ScraperAPIRemote__google_search  query="[target keyword 1]"  countryCode="[cc]"  gl="[cc]"
mcp__ScraperAPIRemote__google_search  query="[target keyword 2]"  countryCode="[cc]"  gl="[cc]"

# Stage 3: On-page analysis — target page + homepage (run in parallel)
mcp__ScraperAPIRemote__scrape  url="[target-page-url]"  outputFormat="html"
mcp__ScraperAPIRemote__scrape  url="[target-page-url]"  outputFormat="markdown"
mcp__ScraperAPIRemote__scrape  url="[homepage-url]"     outputFormat="html"

# Stage 4: Top 2 competitors surfaced in Stage 2 (run in parallel)
mcp__ScraperAPIRemote__scrape  url="[competitor-1-url]"  outputFormat="html"
mcp__ScraperAPIRemote__scrape  url="[competitor-2-url]"  outputFormat="html"

# Stage 5: Brand freshness signals
mcp__ScraperAPIRemote__google_news  query='"[Brand Name]"'
```

**Analysis**: Run all five Audit Stages below. Focus depth on the target page and its direct competitors.

**Output format**: Use `references/report-template.md`. Adapt section depth to single-page scope. Include health grade.

---

### 2. Site-Wide Audit (Mode B)

**When to use**: User gave a bare domain or said "audit my site." Samples homepage plus up to 7 key pages inferred from homepage navigation. ~20–30 tool calls.

**Data gathering**:
```
# Stage 1: Indexation check (run in parallel)
mcp__ScraperAPIRemote__google_search  query="site:[domain]"  countryCode="[cc]"  gl="[cc]"
mcp__ScraperAPIRemote__google_search  query='"[Brand Name]"'
mcp__ScraperAPIRemote__google_search  query="[Brand Name]"

# Stage 2: Keyword visibility (run in parallel, one per keyword)
mcp__ScraperAPIRemote__google_search  query="[target keyword 1]"  countryCode="[cc]"  gl="[cc]"
mcp__ScraperAPIRemote__google_search  query="[target keyword 2]"  countryCode="[cc]"  gl="[cc]"
mcp__ScraperAPIRemote__google_search  query="[target keyword 3]"  countryCode="[cc]"  gl="[cc]"

# Stage 3: On-page analysis — homepage + up to 7 key pages (run in parallel)
# Infer key pages from homepage navigation links
mcp__ScraperAPIRemote__scrape  url="[homepage-url]"   outputFormat="html"
mcp__ScraperAPIRemote__scrape  url="[page-2-url]"     outputFormat="html"
mcp__ScraperAPIRemote__scrape  url="[page-3-url]"     outputFormat="html"
# ... (up to 8 pages total)
# Follow with markdown for content depth assessment on highest-priority pages:
mcp__ScraperAPIRemote__scrape  url="[priority-page-url]"  outputFormat="markdown"

# Stage 4: Top 2–3 competitors per keyword (run in parallel)
mcp__ScraperAPIRemote__scrape  url="[competitor-1-url]"  outputFormat="html"
mcp__ScraperAPIRemote__scrape  url="[competitor-2-url]"  outputFormat="html"
mcp__ScraperAPIRemote__scrape  url="[competitor-3-url]"  outputFormat="html"

# Stage 5: Brand freshness signals
mcp__ScraperAPIRemote__google_news  query='"[Brand Name]"'
```

**Analysis**: Run all five Audit Stages below at full depth across all sampled pages.

**Output format**: Use `references/report-template.md`. Full section depth for all five stages. Include health grade.

---

## Audit Stages

These five stages apply to both modes. Run them in order; parallelize all calls within each stage.

### Stage 1 — Indexation & SERP Snapshot
**What it answers**: "Does Google know this site exists, and what does it see?"

Extract from `site:` results: approximate indexed page count, sitelinks presence, any unexpected URLs in the index (staging domains, UTM-parameterised URLs, duplicate content signals). From brand search: Knowledge Panel presence, branded SERP features.

Note: `site:` counts are Google's displayed estimate — approximate only. Precise coverage data requires Google Search Console. Always caveat this in findings.

Read `references/serp-playbook.md` for exact query patterns and extraction fields.

### Stage 2 — Keyword Visibility + AI Overview Check
**What it answers**: "Where does the site actually appear, and what is Google showing above it?"

For each target keyword, extract: organic position and ranking URL, title tag as shown in SERP, featured snippet (domain and format), People Also Ask questions (top 3–4), and **AI Overview presence** (Y/N — if Y, note which domains are cited as sources).

**AI Overview is the first finding to report per keyword.** A site ranking #1 below a full-viewport AI Overview is in a fundamentally different position than one ranking #1 on a clean SERP. Never report a ranking position without its AI Overview context.

If the site ranks outside position 10, search pages 2–3 (`start: 10`, `start: 20`) before classifying as "not ranking." Extract the top 3 organic competitors per keyword (excluding Wikipedia/Reddit unless they consistently outrank the target) — these feed Stage 4.

Read `references/serp-playbook.md` for extraction fields and geo-targeting parameters.

### Stage 3 — On-Page Analysis
**What it answers**: "What signals is Google reading from these pages?"

Scrape each target page with `outputFormat: "html"` for precise signal extraction, then `outputFormat: "markdown"` for content depth. For each page extract and evaluate: title tag (present, keyword-included, 50–60 chars, unique across site), meta description (present, compelling, 150–160 chars), H1 (exactly one, includes keyword, matches intent), H2/H3 hierarchy (logical, covers subtopics competitors rank for), schema markup types (`<script type="application/ld+json">`), internal links, image alt text, approximate word count.

Read `references/page-analysis.md` for the full extraction checklist.

### Stage 4 — Competitor Gap Analysis
**What it answers**: "What are the top-ranking pages doing that this site isn't?"

Take the top 2–3 competitors from Stage 2 per keyword. Scrape them with the same checklist from Stage 3. Compare: schema types in use, H2 topic coverage, content depth (word count), SERP features owned (featured snippet, PAA). Flag patterns appearing across all top-ranking pages — these are the highest-signal gaps, because they reflect what Google has repeatedly rewarded for this intent.

### Stage 5 — Brand & Freshness Signals
**What it answers**: "Does Google have reason to trust this site?"

Run `google_news` for the brand name (last 3 months). Note mention count and source quality. Check homepage for author bios, about page, expertise signals, and last-modified dates visible in page content.

Note: backlink authority cannot be measured with these tools. If the audit finds strong on-page SEO with poor rankings, flag backlinks as a likely limiting factor with Ahrefs/Semrush as the recommended tool.

---

## Health Grade

Calculate after completing all five stages. Grade is based on finding severity across Stages 1–4.

| Grade | Criteria |
|-------|----------|
| **A** | 0 critical findings, ≤ 2 high-priority issues |
| **B** | 0 critical, 3–5 high-priority issues |
| **C** | 1–2 critical findings, or 6–10 high-priority |
| **D** | 3–5 critical findings, or > 10 high-priority |
| **F** | > 5 critical findings, or indexation blocked |

**Critical findings** (each counts toward grade): `noindex` on a key page, title tags missing across the site, no schema on content pages, blocked by robots.txt.
**High-priority findings** (each counts toward grade): title length violations, duplicate titles, missing meta descriptions, no H1, zero internal linking, image alt text missing at scale.

Include the grade prominently in the executive summary.

---

## Audit Mode Selection Guide

| User says... | Mode |
|---|---|
| "Audit my site" / "Check my SEO" / bare domain provided | Site-Wide (Mode B) |
| "Why isn't [specific page] ranking" / full URL path provided | Single-Page (Mode A) |
| "My traffic dropped" / "What's wrong with my SEO" | Site-Wide (Mode B) |
| "How do I rank for [keyword]" | Single-Page (Mode A) — target the most relevant page |
| "Why am I not showing up on Google" | Site-Wide (Mode B) |
| "SEO check on my homepage" / "review my /pricing page" | Single-Page (Mode A) |

---

## Output Quality Standards

1. **Cite every finding.** Include the exact query or URL that surfaced each issue. "Title tag is missing" must name the page URL and the tool call that confirmed it.
2. **Report AI Overview context with every keyword ranking.** Position alone is incomplete. Always state whether an AI Overview is present, and if so, which domains it cites.
3. **Geo-target every SERP call.** A ranking result without the correct country context is misleading. Note the target market in the report header.
4. **Separate measurement from inference.** "The SERP shows..." for tool output. "This suggests..." for interpretation. Never present inferences as direct findings.
5. **Make recommendations specific.** "Change the title tag on /pricing from X to Y" — not "improve title tags." Every recommendation names the page and the exact change.
6. **Lead with executive summary and health grade.** Many users only read the top. The first section must state the grade, the 3 most important issues, and the single highest-impact action.
7. **Out-of-scope factors belong in Out-of-Scope Notes.** Flag with the right external tool: Core Web Vitals (field data) → PageSpeed Insights / Search Console; Crawl errors / coverage → Search Console > Coverage; Backlink profile → Ahrefs, Semrush, or Moz; Click-through rates → Search Console > Performance; Manual penalties → Search Console > Manual Actions.
8. **Don't exceed call budgets.** Mode A: ~8–12 calls. Mode B: ~20–30. If more are needed, tell the user and ask how to prioritize.
