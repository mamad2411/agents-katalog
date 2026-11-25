---
name: seo-audit
description: Audit a website's SEO health — from basic on-page hygiene (title, meta description, headings, canonical) to advanced technical, structured-data, social, and performance signals — given either a live homepage URL or a project's source code. Produces a prioritized Markdown report plus machine-readable JSON. Use this whenever the user asks to "audit SEO", "check SEO", "improve search ranking", "review meta tags / structured data / sitemap / robots.txt", "why isn't my site ranking", "make my site SEO-friendly", or shares a homepage URL or a web project and wants its search-engine readiness assessed — even if they don't say the word "SEO" explicitly.
---

# SEO Audit

Audit a website's search-engine readiness and produce a prioritized, actionable report.
There are two modes — pick based on what the user gives you:

- **URL mode** — the user gives a live URL (or just a domain). Run the bundled Python script;
  it fetches the page, crawls a few internal pages, scores everything, and writes the report.
- **Code mode** — you have the project's **source code** (running inside Claude Code / Cursor /
  an agent with repo access). Audit the source against the same checklist, citing real files,
  because many issues (sitemap generation, head/meta management, structured data, image alt)
  are best fixed at the source.

When both are available (e.g. a repo with a running dev server), do **both**: run the script
against the live/dev URL for ground truth, then map findings back to the source to recommend
fixes.

## Golden rules

1. **Measure, don't guess.** In URL mode, run the script and report what it actually found.
   In code mode, read the real files — never invent meta tags, schema, or config that isn't there.
2. **Prioritize ruthlessly.** Lead with the few changes that move the needle (indexability,
   titles, mobile, structured data), not an undifferentiated wall of nitpicks.
3. **Explain the why and the fix.** Every finding should tell the user what's wrong, why it
   matters for search, and the concrete change to make.
4. **Know the tool's limits.** The script does *static* analysis of server-rendered HTML. For
   JS-heavy SPAs it may under-count content/links — say so. It does not measure real Core Web
   Vitals; recommend PageSpeed Insights / Lighthouse for field data.

---

## URL mode — how to run

### Locate the script (important)

Run the script by its **real path**, not relative to the user's current directory — when this
skill triggers, the working directory is the user's project, not the skill folder. The script
self-locates its own helpers, so it works from any directory once you give it the right path.

- **Installed as a Claude Code plugin:** use the plugin root variable:
  `"${CLAUDE_PLUGIN_ROOT}/skills/seo-audit/scripts/seo_audit.py"`.
- **Installed as a personal/project skill or on Claude Desktop:** the `scripts/` folder sits
  next to this `SKILL.md`. Use that directory's absolute path (the one this file was loaded
  from), e.g. `<skill-dir>/scripts/seo_audit.py`.

In the commands below, `SEO=<that absolute path>/seo_audit.py`.

### Dependencies (optional, best-effort)

The engine has **no required dependencies** — it falls back to the Python standard library. But
`requests` + `BeautifulSoup` make parsing more robust, so before the first URL audit, try to
install them (ignore failure and proceed regardless):

```bash
pip install -r "<skill-dir>/requirements.txt" || true
python "$SEO" --self-check        # shows Python version + which backend is active
```

### Run the audit

```bash
python "$SEO" <url> [--crawl N] [--out DIR] [--json-only] [--md-only]
```

- `<url>` — homepage URL (scheme optional; `https://` is assumed).
- `--crawl N` — max pages to crawl, homepage included. Default **8**. Use `1` for homepage-only.
- `--out DIR` — output directory. Default `./seo-report`. Writes `report.md` and `report.json`.
- `--self-check` — print the runtime environment / active backend and exit (no URL needed).

Example:

```bash
python "$SEO" https://example.com --crawl 8 --out ./seo-report
```

**After it runs:** read `seo-report/report.md`, then present to the user:
1. **Check confidence first.** If the report shows a ⚠️ *Low confidence* banner (also in
   `report.json` under `confidence`), lead with that — the site likely blocked the bot or
   served a stripped/JS-rendered shell, so the score reflects what a bot saw, not real users.
   Recommend verifying in a browser / headless renderer before trusting the findings.
2. The **overall score + grade** and the per-category scores.
3. The **top priority fixes** (critical → warning → notice), each with the why and the fix.
4. Offer to go deeper on any category or, if you have the source, to apply the fixes.

The script prints which backend it used and a one-line summary to stderr; the full detail is
in the report files.

## What gets checked

Seven categories, scored 0–100 each and rolled into an overall weighted score. Full detail,
including exact thresholds and rationale, is in `references/checklist.md` and
`references/thresholds.md` — read those when the user wants depth or asks "why".

| Category | Highlights |
|---|---|
| **Crawlability & Indexing** | HTTPS, HTTP status, redirect chains, `noindex`/`X-Robots-Tag`, canonical, `robots.txt`, XML sitemap |
| **On-Page** | title, meta description, single H1 + heading order, `html lang`, image `alt`, URL hygiene |
| **Technical** | mobile viewport, charset, favicon, hreflang, compression, caching, HTTP/2+, HSTS |
| **Structured Data & Social** | JSON-LD / schema.org, Open Graph, Twitter Cards |
| **Content** | thin content, duplicate titles/descriptions across the crawl, broken internal links |
| **Keywords & Topics** | apparent focus keyword, presence in title & H1, consistency across title·H1·meta·URL·body, keyword-stuffing, descriptive anchor text |
| **Performance** | HTML weight, render-blocking resources, image dimensions & lazy-loading (static heuristics) |

---

## Code mode — auditing source

When you have the repository, audit the source against the same seven categories. The
framework-specific guidance — where titles/meta live, how sitemaps and robots are generated,
how to add JSON-LD, common pitfalls in Next.js / React (Vite/CRA) / Astro / Nuxt / plain HTML
/ WordPress — is in **`references/code-audit.md`**. Read it, detect the stack, then walk the
source and produce findings that **cite real files** (e.g. `app/layout.tsx:14`).

If there's a runnable dev server, also run URL mode against it (`http://localhost:PORT`) and
reconcile the two: the live run shows symptoms, the source shows where to fix them.

## Reporting

In URL mode the script writes the report for you. In code mode (or when summarizing), follow
the structure in `assets/report-template.md`: overall grade → executive summary → top fixes →
per-category findings with severity, the problem, why it matters, and the fix.

Keep severities consistent with the engine: 🔴 critical (blocks indexing/ranking), 🟠 warning
(real problem), 🟡 notice (minor/improvement), 🟢 pass, ℹ️ info (context).

### Keyword & topic suggestions

The **Keywords & Topics** category measures what the page *already* signals; turn that into
forward-looking suggestions. After the audit, read the **Detected keyword profile** finding
(`keyword-profile` in `report.json`, under `findings[].evidence`) — it lists the apparent focus
term, the top terms, and the top phrases. From that profile plus the page's content:

1. **Confirm the target.** State the page's apparent primary keyword and search intent
   (informational / commercial / navigational). If it doesn't match what the page *should* rank
   for, that mismatch is the headline recommendation.
2. **Suggest keywords to implement.** Propose a short list (≈5–10) of related terms the page is
   *not* yet targeting — semantic variants, long-tail and question forms, and adjacent subtopics
   the copy implies but doesn't cover.
3. **Say where each goes.** For every suggestion, name the slot: title, H1, a new H2 section,
   body copy, image `alt`, or internal anchor text.

Be explicit that these are **content-derived** suggestions, **not** validated against real
search volume or difficulty — see *Limits* for how to confirm demand.

## Limits & optional extensions

- **Bot-blocking / cloaking:** some sites (e.g. Amazon, sites behind aggressive WAFs) serve a
  stripped page or a challenge to non-browser clients. The engine detects this and marks the
  audit **low confidence** with reasons — honor that signal and don't over-trust the score.
- **JS-rendered sites:** static HTML may miss client-rendered content/links (also surfaced via
  low confidence). Note it, and verify in a browser or with a headless renderer if accuracy matters.
- **Core Web Vitals:** not measured here. Recommend PageSpeed Insights or Lighthouse; the
  PageSpeed Insights API (free key) can be wired in as an optional extension.
- **Keyword suggestions are content-derived.** The Keywords & Topics category and any suggested
  keywords come from the page's own text — there is **no search-volume or difficulty data**.
  Validate demand and competition with Google Search Console (your own queries/impressions) or a
  keyword tool (Keyword Planner, Ahrefs, Semrush) before committing to new targets. Wiring one of
  those in is an optional, key-requiring extension, deliberately outside the self-contained core.
- **Large sites:** the crawler is intentionally small and polite. For full-site crawls, raise
  `--crawl` deliberately and mind the target's load.

## Reference files

- `references/checklist.md` — the complete basic→advanced SEO checklist.
- `references/thresholds.md` — exact thresholds (lengths, counts) and the reasoning.
- `references/code-audit.md` — per-framework source-auditing guide.
- `assets/report-template.md` — report skeleton for code-mode / manual reports.
