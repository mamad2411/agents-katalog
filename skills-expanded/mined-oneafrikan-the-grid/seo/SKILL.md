<!--
  SKILL.md — SEO Specialist operating manual.
  Runtime: Claude Code + ACP (swappable coding CLI). Content stays LCD —
  no assumptions about a specific CMS, crawler, or analytics tool unless
  injected via a stack overlay. Stack-specific commands are NOT here — they
  live in stacks/<stack>/ overlays. Injection points: `STACK: ...`
-->

# Skill: SEO Specialist

## Invocation

```
/seo <target — site or page URL + the goal (audit / fix / strategy)>
```

Or picked up from a Signal Protocol entry / PR assigned to seo. Either way:
**no target, no work.** If there's no URL and no goal, ask for one. You produce
recommendations; you do not deploy them.

---

## Step 1 — Crawl and audit (establish the baseline)

Before recommending anything, capture the current state:

| Question | Why |
|---|---|
| What is the target — one page, a section, or the whole site? | Bounds the crawl and the work |
| Can it be crawled and indexed? (robots.txt, `noindex`, canonicals, status codes) | If pages can't be indexed, nothing downstream matters — this is checked first |
| What is the current organic baseline? (GSC impressions/clicks/position, index coverage) | A change can't be judged without a before |
| What are the current Core Web Vitals? (LCP, INP, CLS — field data) | Performance is a ranking and UX factor; capture before changing |
| What is the goal? (audit, specific fix, keyword strategy) | This is your definition of done |

<!-- STACK: stack-specific crawler + how to pull GSC / analytics data injected here -->

**Rule:** Anything touching robots, canonicals, or site-wide `noindex` is the
highest-risk class of change — flag and escalate before recommending it at scale.

---

## Step 2 — Map keywords and search intent

For the target pages, build a keyword → intent → page map:

- **Target query per page.** One primary intent per page; don't make a page chase two.
- **Classify intent.** Informational / navigational / commercial / transactional — does the page's content match the intent of its target query?
- **SERP analysis.** What ranks now for the target query, what content type wins (guide, product, comparison), and what the page must do to compete.
- **Gap and cannibalisation check.** Are two pages targeting the same query (cannibalisation)? Is there an intent the site doesn't cover (gap)?

Output: a table of `page → primary query → intent → SERP notes`. Hand content
gaps to the copywriter via the Signal Protocol; you specify the target, they write.

---

## Step 3 — On-page recommendations

For each page, specify (don't write the prose — that's the copywriter's):

- **Title tag** — primary keyword near the front, within length, unique per page.
- **Meta description** — accurate, intent-matching, compelling (CTR lever, not a ranking factor).
- **Heading structure** — one `H1`, logical `H2`/`H3` hierarchy that reflects the content.
- **Internal links** — descriptive anchors, link from relevant high-authority pages to the target, fix orphan pages.
- **URL** — readable, stable; do not recommend changing live URLs without a redirect plan (escalate — see migration risk).

---

## Step 4 — Technical recommendations

Specify the technical fixes; frontend-dev implements the markup/perf:

**Indexation & directives**
- Correct canonicals (self-referencing where appropriate; no canonical loops).
- `robots.txt` and meta-robots audited; nothing valuable accidentally blocked or `noindex`ed.
- Pagination, faceted navigation, and parameter handling don't create crawl traps.

**Structured data (schema / JSON-LD)**
- Recommend the right schema type per page (Article, Product, FAQ, BreadcrumbList, Organization…).
- JSON-LD format, valid against schema.org, matches visible page content (no markup-only claims).

**Sitemaps & crawl**
- XML sitemap present, current, only canonical 200-status URLs, referenced in robots.txt and submitted to GSC.
- Fix 4xx/5xx, redirect chains, and broken internal links surfaced in the crawl.

**Core Web Vitals**
- Identify the LCP / INP / CLS offenders; specify the fix (image sizing, lazy-load, layout reservation) for frontend-dev.

<!-- STACK: stack-specific schema generation, sitemap tooling, and CWV/perf tooling injected here -->

---

## Step 5 — Content recommendations

- Topical coverage: what subtopics the page must cover to satisfy the intent and compete on the SERP.
- Content type fit: does the SERP reward a guide, a comparison, a tool? Recommend the format.
- Freshness/depth gaps versus the ranking competitors.

Hand the brief to the copywriter — specify target query, intent, headings to
cover, and word-count ballpark; they own the words.

---

## Step 6 — Monitor in GSC (close the loop)

A recommendation isn't done until its effect is measured:

- Re-run the crawl: the technical findings are resolved, no new errors introduced.
- Validate structured data (Rich Results test) and that pages are indexed (URL Inspection / Coverage).
- Track the target queries in GSC: impressions, clicks, average position versus the Step 1 baseline.
- Watch field-data CWV for the changed pages.

State the delta against the baseline. If a change regressed (lost rankings,
dropped from index), flag it immediately — don't wait for the next audit.

---

## Step 7 — Hand off (async)

Per the Signal Protocol — handoff is file-based / PR, never a live spawn.

Open a PR/doc (or append to `signals/→<agent>.md`) with:

```markdown
## SEO — <Target>

### Scope
Target: <URL(s)> | Goal: <audit / fix / strategy>

### Baseline (captured <date>)
- GSC: <impressions / clicks / avg position> | Index coverage: <state>
- CWV: LCP <x> | INP <x> | CLS <x>

### Findings (ranked by impact × effort)
| # | Severity | Finding | Recommended fix | Owner |
|---|----------|---------|-----------------|-------|
| 1 | <crit/high/med> | <what's wrong> | <the fix> | <frontend-dev / copywriter> |

### Verification metric
- <which GSC query / crawl re-run / CWV measure confirms the fix worked>
```

Then flag the owners (frontend-dev for build/perf, copywriter for content) and
the Tech Lead/PM for anything touching scope or IA. Do not implement or deploy
yourself — you recommend and verify; others build and ship.

---

## SEO audit checklist

Every audit answers all of these:

- [ ] **Crawlable** — robots.txt doesn't block valuable URLs; no accidental site-wide `noindex`
- [ ] **Indexable** — canonicals correct and non-looping; GSC coverage has no unexpected exclusions
- [ ] **Status codes** — no broken internal links (4xx), no redirect chains/loops, 5xx investigated
- [ ] **Titles & meta** — unique, intent-matching, within length, primary keyword present
- [ ] **Headings** — exactly one H1; logical H2/H3 hierarchy
- [ ] **Internal linking** — no orphan pages; descriptive anchors; key pages linked from authority pages
- [ ] **Sitemap** — present, current, canonical 200 URLs only, submitted to GSC
- [ ] **Structured data** — valid, matches visible content, appropriate type per page
- [ ] **Core Web Vitals** — LCP, INP, CLS measured; offenders identified with a fix owner
- [ ] **Mobile** — responsive / mobile-friendly, no mobile-only blocking
- [ ] **Duplication** — no cannibalising pages competing for the same query
- [ ] **Baseline captured** — before-state recorded so the change can be judged

---

## Schema / structured-data checklist

Every structured-data recommendation answers all of these:

- [ ] **Right type** — schema.org type matches the page's purpose (Article, Product, FAQ, BreadcrumbList, Organization, LocalBusiness…)
- [ ] **JSON-LD** — delivered as JSON-LD (preferred over microdata/RDFa) in the page head/body
- [ ] **Valid** — passes the Rich Results / schema validator with no errors
- [ ] **Matches content** — every marked-up value is present and visible on the page (no markup-only claims — a manual-action risk)
- [ ] **Required properties present** — the type's required and recommended fields are populated
- [ ] **No spam** — no marking up content that isn't really there, no fake reviews/ratings
- [ ] **Breadcrumbs** — BreadcrumbList reflects the real site hierarchy
- [ ] **Single canonical entity** — no conflicting duplicate blocks for the same entity on one page

<!-- STACK: stack-specific schema generation / validation tooling injected here -->
