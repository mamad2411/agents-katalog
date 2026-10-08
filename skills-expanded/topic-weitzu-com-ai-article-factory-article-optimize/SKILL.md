---
name: article-optimize
description: 'Use to make a correct article rank in search and get cited by AI answer engines — on-page SEO + GEO + structured data, all first-party, no external packs. SEO/GEO优化/meta描述/schema结构化数据/AI引用/citation/optimize/精选摘要/featured snippet'
version: "1.0.0"
license: Apache-2.0
homepage: "https://github.com/weitzu-com/ai-article-factory"
when_to_use: "Use as the article factory's P7 optimization stage, or standalone when content is already correct (passed QA) and needs to be tuned to (1) rank in Google/Bing for the target query and (2) be quoted by ChatGPT, Perplexity, Gemini, Claude, and Google AI Overviews. Triggers: SEO优化, GEO优化, 让AI引用, optimize this article, add schema, write meta description, win the featured snippet, AI citation, generative engine optimization. Do NOT use to fix factual errors or thin content — that is the QA gate's job."
argument-hint: "<article folder | draft.md> [target query] [Article|TechArticle] [--howto]"
metadata:
  author: weitzu-com
  tags: [seo, geo, structured-data, json-ld, schema, ai-citations, featured-snippet, meta-tags, internal-linking, on-page, optimize, SEO优化, GEO优化, 结构化数据, AI引用]
---

# Article Optimize (SEO + GEO + Structured Data)

The factory's **P7** stage, made first-party. You take an article that is already **correct** (P8 QA territory, not yours) and tune it so one piece does two jobs at once: **gets indexed and ranked** by search engines, and **gets quoted** by AI answer engines.

## First principle

> A single well-structured passage that fully answers one question — placed first, sourced, and entity-consistent — is the shared optimum for both a long-tail ranking and an AI citation. Optimize the passage, not the page chrome.

Everything below is **pure on-page logic**. No crawler, no keyword tool, no external skill pack is required — if those are connected the work gets sharper, but the stage runs standalone on the draft text alone.

## Guardrails (read first)

- **Right before optimized.** If the content is wrong, thin, or unsourced, stop and hand back to QA. Do not paper over weak content with markup.
- **Markup mirrors visible content.** Never put a claim, rating, FAQ answer, or step in JSON-LD that a reader cannot see on the page. Mismatched schema gets the page demoted, not promoted.
- **No invented facts.** The "exclusive information" and any statistic must already exist in the draft (sourced via the claim ledger `[C#]`). You restructure and surface; you never fabricate.
- **One edit, one reason.** Each change you make maps to a checklist item below so the human can review it.

## Workflow (8 steps)

Run in order. After each step, note what changed and why.

### 1. Lock the target
Identify the **primary query** (the one phrase the article must own) and 2–4 secondary/long-tail queries. Identify the **canonical entity** (brand / product / person / concept) and its one canonical name. If the entity name varies across the draft, normalize to one spelling everywhere — AI disambiguation depends on it.

### 2. SEO — on-page signals
Produce these artifacts (see the SEO checklist for pass bars):

- **Title tag**: contains the primary query + an information-gain hook (a number, year, outcome, or angle the SERP doesn't already have). ≤ 60 Latin chars / ≤ 30 CJK chars. Do not duplicate the H1 verbatim if a sharper title wins more clicks.
- **H1**: one per page, contains the primary query, reads naturally.
- **Meta description**: ≤ 155 chars (≤ 80 for CJK), front-loads the answer, ends with a reason to click. Never keyword-stuff.
- **Slug**: short, hyphenated, lowercase, primary keyword, no stop-word filler, no dates that will rot.
- **Internal links**: **≥ 2** contextual links to related articles, descriptive anchors (no "click here"), exact-match anchors kept to 10–20% of the article's anchor mix.
- **Image alt text**: every image gets descriptive alt; the cover/lead image alt includes the primary query naturally.
- **Heading structure**: H2/H3 in a logical hierarchy, no skipped levels.

### 3. GEO — make every section AI-citable
- **Every H2/H3 is an independently answerable question** that resolves in the first 40–60 words after the heading. A reader (or model) landing only on that block must get a complete answer with no "as discussed above."
- **Structure the citables**: definitions as standalone 25–50-word blocks (`**[Term]** is [category] that [function], [key trait].`); comparisons as tables ending in "Choose A if… / Choose B if…"; data as `According to [Source] ([date]), [stat]` with the implication; processes as numbered action-verb steps.
- **Entity consistency**: same canonical name everywhere; add one disambiguation line if the entity collides with a common term.
- **≥ 1 exclusive datum**: surface at least one piece of first-hand experience, original data, named case study, or expert quote already in the draft — this is the single biggest lever for being cited over a competitor.
- **FAQ from real queries**: 3–6 questions phrased the way users actually search (mine People-Also-Ask wording, support questions, the secondary queries from step 1 — not invented filler). Each answer 40–120 words, answer-first.

### 4. Win the featured snippet
For the primary query, decide the snippet format and build the matching block **immediately under the relevant H2 (first instance wins)**:

| Query shape | Snippet format | Block to build |
|-------------|----------------|----------------|
| "what is / what does" | Paragraph | 40–60-word self-contained answer, keyword in first 5 words |
| "how to / steps to" | Ordered list | 5–8 steps, each ≤ 20 words, action verb first |
| "types of / best / signs of" | Unordered list | 5–8 parallel items, short phrasing |
| "X vs Y / pricing" | Table | 3–6 rows, 3–5 cols, short cells, comparison dimension in header |

Move setup/context/commentary **below** the answer block, never above it.

### 5. Structured data
Generate JSON-LD and place it in one `<script type="application/ld+json">` block (combined array if multiple types). Templates: `references/schema-templates.md`.

- **Always**: `Article` (or `TechArticle` for developer/technical how-it-works content) — `headline`, `description`, `image`, `datePublished`, `dateModified` (ISO 8601), `author` (named Person), `publisher`, `mainEntityOfPage` (canonical URL).
- **If the page has a visible FAQ section**: add `FAQPage` — every `Question`/`acceptedAnswer` must match visible text verbatim.
- **If the page is a how-to** (`--howto` or step-based content): add `HowTo` — `name`, `step[]` with positions and per-step anchor URLs; `totalTime`/`supply`/`tool` only when visible.
- Use `aggregateRating`/`review` **only** when visible, verifiable reviews back the exact numbers — otherwise omit.

### 6. Validate the markup (self-contained, no tooling needed)
Run this static check before declaring done:
- [ ] Parses as JSON (no trailing commas, balanced braces/brackets, double quotes only).
- [ ] `@context` is `https://schema.org`; every object has an `@type`.
- [ ] All required fields for the chosen type are present and non-placeholder (no `[…]` left).
- [ ] Dates are ISO 8601; URLs are absolute and canonical.
- [ ] Every schema value appears in the visible content (FAQ answers, steps, headline match).
- [ ] If a live validator is available, also confirm with `validator.schema.org` / Google Rich Results Test — but the static check above is the gate.

### 7. Score (SEO and GEO, 0–10 each)
Self-assess against the rubrics below. **If either score is < 8, list the specific changes that would raise it** and apply the cheap ones before finishing.

### 8. Hand off
Report: artifacts produced (title/meta/slug/alt/links/FAQ/JSON-LD), before/after SEO and GEO scores, snippet format targeted, the one exclusive datum surfaced, and any open improvement items.

## SEO scoring rubric (0–10)

Score 1 point each (cap 10):
1. Title has primary query **and** an information-gain hook, within length.
2. H1 present, single, contains primary query.
3. Meta description ≤ 155 chars, answer-first, has a click reason.
4. Slug clean, keyword-bearing, no rot-prone dates.
5. ≥ 2 contextual internal links with descriptive anchors.
6. Every image has descriptive alt; lead image alt carries the query.
7. Heading hierarchy logical, no skipped levels.
8. Primary query placed in first 100 words naturally (no stuffing).
9. Secondary/long-tail queries each owned by a section.
10. A featured-snippet block exists in the correct format under its H2.

## GEO scoring rubric (0–10)

Score 1 point each (cap 10):
1. Every H2/H3 answers its question in the first 40–60 words.
2. ≥ 3 standalone, quotable definitions (25–50 words).
3. ≥ 1 comparison or data point structured as table/`According to…` with a date.
4. ≥ 1 exclusive datum (first-hand data, named case, expert quote).
5. Canonical entity name consistent throughout; disambiguation present if needed.
6. FAQ covers real user-query phrasing (≥ 3), answer-first.
7. Short paragraphs (2–4 sentences), scannable hierarchy.
8. External citations to authoritative, dated sources.
9. Author credentials / byline visible.
10. Valid `FAQPage` (and `HowTo` if applicable) markup mirrors visible content.

> A score of 8–9 ships. 10 is rare and not required. Below 8 on either axis is an open loop, not a pass.

## References

- `references/schema-templates.md` — copy-ready JSON-LD for `Article`, `TechArticle`, `FAQPage`, `HowTo`, with shared rules and a combined-array example.

---
*Distilled from the SEO/GEO Claude skill packs (aaron-he-zhu/seo-geo-claude-skills, inhouseseo/superseo-skills, Apache-2.0); original concise reimplementation.*
