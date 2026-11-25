---
name: seo-audit
description: "Use when auditing or diagnosing SEO on a site: \"SEO audit\", \"technical SEO\", \"why am I not ranking\", \"on-page SEO\", \"meta tags review\", \"SEO health check\", or whether a page is ready to launch. NOT for building a site (`/founder-pipeline:web-site-creator`), writing page copy (`/founder-pipeline:blog-launch`), getting pages indexed (`/founder-pipeline:web-indexation`), ongoing AI-citation measurement, or local place-in-the-query ranking."
license: MIT
metadata:
  version: "2.0.0"
  author: "Alireza Rezvani (v1.0)"
  category: "marketing"
  updated: "2026-08-22"
---

# SEO Audit

Diagnose what is wrong with a page or a site, in priority order, with evidence. This skill
**grades what exists**. It does not build, deploy or index anything.

Reference convention used throughout: **in-skill references are bare paths**
(`references/seo-audit-reference.md`); **cross-skill references are rooted at the plugin**
(`${CLAUDE_PLUGIN_ROOT}/skills/ai-seo/references/content-patterns.md`). If a path in this file has
no `${CLAUDE_PLUGIN_ROOT}` prefix it lives inside this skill.

## Delegation

Read `references/delegation-table.md` before you start any fix, rewrite, keyword, indexation, schema, local-search or citation-measurement work the audit surfaces: it maps each concern to the skill or source that owns it. This skill owns diagnosis only.

## Modes

| Mode | Does | Cost |
|---|---|---|
| `audit <domain>` | Full site diagnosis: crawl-and-index, technical, on-page, content, authority | Free unless a paid rank-data provider is invoked — **state the plan cost before any paid call** |
| `page <url>` | One page. Runs the checker script, returns the four-layer score plus the Launch Gate | Free |
| `launch-check <url>` | Launch Gate only. Binary. Ship / do not ship | Free |
| `score` | Re-run `page` across a named set of URLs, comparison table | Free |

Default when the invocation is bare: `audit` on the domain in context.

## Initial assessment

Read `brand_context/` in the active workspace before asking anything. It carries the offer, the
ICP and the voice — do not re-ask for what is already written down.

Then establish three things, and **stop and ask** rather than guess at any of them. A confident
audit built on the wrong primary keyword is worse than no audit.

1. **Site context** — what kind of site, what the business goal for organic is, which pages are
   the revenue pages.
2. **Current state** — known issues, traffic baseline, recent migrations or redesigns.
3. **Scope** — whole site or named pages; full stack or one layer; is there GSC access.

## The score: four layers, renormalised

Report **one number plus its coverage**. Never a bare number.

| Layer | Weight | Asks |
|---|---|---|
| **Indexability** | 30 | Can a search engine and an AI crawler fetch it, and will they keep it? Canonical, `noindex`, crawler delivery |
| **On-page** | 25 | Is the page's own metadata doing its job? Title, description, H1, hierarchy, internal links out |
| **Extractability** | 25 | Can an answer be lifted off it without running JS and without reading markup? Visible date, price in text, FAQ answers present in the DOM, markdown twin |
| **Delivery** | 20 | How it is served. HTTPS, viewport, image alt coverage |

Four rules, and they are not negotiable:

- **An unmeasured check is never a zero.** It leaves the numerator and the denominator both. The
  score renormalises over what was actually measurable.
- **`coverage` prints beside the total, always** — `82/100 (coverage 71%)`. A high score at 40%
  coverage is a claim about a fifth of the page.
- **Any layer below 70 ships with a concrete fix**, not a number. "Extractability 58" is not a
  finding; "the price lives only in a JS-rendered widget, move it into the body copy" is.
- **Schema is reported, never scored.** So is word count. See Myths below for why.

## Run the checker

The deterministic layer is a script. **Run it before writing a single finding** — this skill's
findings are evidence-led or they are opinions.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/seo-audit/scripts/seo_checker.py" --url <url> --json
python3 "${CLAUDE_PLUGIN_ROOT}/skills/seo-audit/scripts/seo_checker.py" --url <url> --keyword "<primary keyword>" --json
python3 "${CLAUDE_PLUGIN_ROOT}/skills/seo-audit/scripts/seo_checker.py" --file page.html --json
```

Pass `--keyword` whenever the primary keyword is known: it turns on the Gate's title / H1 / URL /
first-100-words placement check. Without it that Gate item reports as not tested, not as a pass.

It emits one stable shape, which `page`, `launch-check` and `score` all read:

```json
{ "overall": 0, "coverage": 0, "confidence": "high|medium|low",
  "layers": { "indexability": {"score": 0, "weight": 30, "measured": [], "unmeasured": [], "failing": []} },
  "checks": { "<id>": {"status": "pass|fail|warn|unmeasured|report", "note": "", "score": 0} },
  "gate":   { "pass": true, "blockers": [] } }
```

Checks it runs: `canonical`, `noindex`, `crawler_fetch` (fetches as GPTBot **and** Googlebot,
asserts 200 and no placeholder string in the served HTML), `title`, `meta_description`, `h1`,
`heading_hierarchy`, `internal_links`, `visible_date` (English plus one worked non-English
locale — see `DATE_PATTERNS` in the script and add your market's date forms there),
`price_number`, `schema_only_faq`, `md_twin`, `https`, `viewport_meta`, `image_alt_text`. Reported
but never scored: `word_count`, `schema_types_present`, `keyword_placement`.

**What the script cannot do is yours.** It has no opinion on whether the page answers the query,
whether the proof is real, or whether the primary keyword was the right one. Grade those by hand
and say which is which.

## Audit framework

Full checklist: `references/seo-audit-reference.md`. The priority order is inlined here because it
is the thing that gets used on every run and a pointer alone makes this section hollow:

1. **Crawlability and indexation** — can it be found and kept? robots.txt, sitemap, canonicals,
   stray `noindex`, redirect chains, soft 404s. Nothing below this matters if this fails.
2. **Technical foundations** — Core Web Vitals (LCP < 2.5s, INP < 200ms, CLS < 0.1), HTTPS,
   mobile, server-rendered content.
3. **On-page** — title, description, one H1, heading hierarchy, keyword placement, internal links.
4. **Content quality** — does it deserve to rank? Intent match, E-E-A-T, original data or
   first-hand experience, named sources.
5. **Authority and links** — referring domains, anchor profile, brand mentions.

Work top-down. Report bottom-up findings only after the layer above them is clean, and say so when
you are skipping ahead.

## Money page checklist

Build skills cover how a page is *made*. None of them covers the shape of the *offer* on it. Grade
every revenue page against this — it is where most commercial sites actually lose.

- [ ] **One service per page.** Never two combined. This is the single most common failure on a
      service site, and it defeats the primary-keyword model before anything else is attempted.
- [ ] **Two-second rule.** What you do, where you do it, and what to do next are all visible
      without scrolling and without reading a paragraph.
- [ ] **Plain headline, not clever.** The H1 names the service. Wordplay goes in the sub-head or
      nowhere.
- [ ] **Price is answered on the page.** A number, a band, a "from", or an explicit reason there
      isn't one. Silence is the most-asked question left unanswered.
- [ ] **CTA above the fold, mid-page and at the end.** Same action, three chances.
- [ ] **Real photos.** Stock imagery on a service page reads as a page about a service rather than
      a page from a business.
- [ ] **FAQ capped at 5 questions** on a transactional page. More is a content page wearing a
      money page's clothes.
- [ ] **Three or more internal links out** to related services and proof pages.
- [ ] **No word-count target.** Answer the query completely and stop.

## The answer capsule

The canonical rule lives in **`${CLAUDE_PLUGIN_ROOT}/skills/ai-seo/references/aeo-patterns.md`** and is stated
in exactly one place. Do not restate it with different numbers here or anywhere else — grade
against it:

> **40–60 words total, first sentence self-contained at ≤25 words.** No hyperlinks inside the
> capsule.

Grade each question-shaped heading on the page against that, and report the ones that bury their
answer below a warm-up paragraph.

## AEO and the AI-era layer

Two different things. Keep them apart in the report.

- **AEO** — position 0, People Also Asked, voice. The surface is **Google's classic SERP**,
  measured in GSC and SERP-feature data. Patterns and the honest ceiling:
  `${CLAUDE_PLUGIN_ROOT}/skills/ai-seo/references/aeo-patterns.md`.
- **AI citation** — being quoted by ChatGPT, Perplexity, AI Overviews. Different game, different
  evidence, and this skill does not restate it. The evidence base lives in
  `${CLAUDE_PLUGIN_ROOT}/skills/web-site-creator/phases/5-seo.md` §5.4 and in
  `/founder-pipeline:ai-seo`. **Cite those, never re-derive them** — a second copy of an evidence
  base drifts within a month.

The one bridge worth stating in an audit: pages that held featured snippets before AI Overviews
rolled out tend to appear in AI Overviews. Structuring for the snippet is not wasted work. It is
also not the same as optimising for citation.

## Location pages

A place in the query changes the job, and this skill does not do that job. Local search wants
service×city validation, name/address/phone (NAP) consistency, `LocalBusiness` schema and a
claimed business profile — none of which is graded here.
**`/founder-pipeline:web-listings`** owns directories and the canonical NAP values; the rest is a
separate local-SEO pass you run yourself. Do not grade a location page here beyond the generic
on-page layer, and never recommend more locality mentions — if density warns, the fix is fewer.

## Launch Gate

**Binary. Separate from the score. Never traded against it.** A page can score 100 and fail the
Gate — the demo run in the checker script does exactly that, deliberately (100/100, Gate FAIL on
thin content).

This is the auditor's mirror of `/founder-pipeline:web-site-creator`'s GATE 5, for sites you did
not build. `launch-check <url>` runs it alone.

| # | Blocker |
|---|---|
| 1 | `noindex` anywhere in the **built** HTML (not the source) |
| 2 | Missing or off-host canonical |
| 3 | Not exactly one H1 |
| 4 | Missing title or missing meta description |
| 5 | Not served over HTTPS |
| 6 | Non-200, or placeholder text, when fetched as GPTBot or Googlebot |
| 7 | Thin page — under 150 words. The only surviving word-count threshold |
| 8 | Fewer than 3 internal links out |
| 9 | Primary keyword missing from title, H1, URL or first 100 words (needs `--keyword`) |

Not automatable, so check by hand and say you did: LCP under 2.5s, WebP/AVIF only, title and
description unique **across the site**, no broken links, 301s in place for anything moved.

## Myths this skill does not chase

Read `references/myths.md` when a client or finding raises word count, outbound links, schema, AI-written content, slug order or keyword density.

## Output format

**Executive summary** — 3–5 bullets. Overall score with coverage, Gate pass/fail, top three
issues, the quickest win.

**Findings**, grouped by layer, each in this format and never without evidence:

- **Issue** — what is wrong
- **Impact** — High / Medium / Low, and on what (indexation, ranking, extraction, conversion)
- **Evidence** — the check id and its output, the URL, or the tool and date.
  `[source: <provider> <tool>, <date>]` for anything from a rank-data provider
- **Fix** — specific enough to hand to someone else
- **Priority** — 1–5

**Prioritised action plan** — always the final section. Critical (blocking indexation) → high
impact → quick wins (under 15 minutes) → long-term.

Write for a technically-aware non-specialist. "The title is weak" is useless. "The title is 83
chars, above the length band where Google rewrites almost every title it sees [Zyppy title-rewrite
study, ~80k titles]" is not.

## Tools

Read `references/tools.md` when you need real rank, SERP, on-page or backlink data (state the plan cost before any paid call) or the free tool list.

## References

- `references/seo-audit-reference.md` — the full graded checklist behind the Audit Framework
- `references/review-stars-rich-snippets.md` — earning the ⭐ rating under a result: eligible
  `Product`/`AggregateRating` schema, the visible-rating rule, the self-serving `LocalBusiness`
  trap, honest `ratingCount` vs `reviewCount`, GSC validate, then queue via
  `/founder-pipeline:web-indexation`
- `${CLAUDE_PLUGIN_ROOT}/skills/ai-seo/references/aeo-patterns.md` — the canonical answer-capsule
  rule, the snippet-type map, and what AEO will not do
- `${CLAUDE_PLUGIN_ROOT}/skills/web-site-creator/phases/5-seo.md` — the canonical build rules and
  the AI-era evidence base. Cite it; never re-derive it

## Proactive triggers

Surface these without being asked:

1. **Traffic drop mentioned** — frame an audit scope immediately, starting at indexation.
2. **Migration or redesign, planned or recent** — flag the pre/post audit and the 301 map before
   anything else.
3. **"Why isn't my page ranking?"** — run `page <url>` first. The Gate answers it about a third of
   the time before any keyword work starts.
4. **Keyword gaps surfacing in a `/founder-pipeline:web-keyword` session** — offer an audit to validate the
   opportunity is real before pages get built against it.
5. **New site or product launch** — offer `launch-check` on the money pages. Free, binary, and
   catches the expensive mistakes.
6. **Testimonials or ratings on a page but no stars in search** — run the review-stars playbook at
   `references/review-stars-rich-snippets.md`.
7. **Any "live", "real-time" or counter widget on a page** — run `crawler_fetch` before grading.
   AI crawlers execute zero JavaScript, so a placeholder is what they index.

## Task-specific questions

1. Which pages and keywords actually matter?
2. Is there Search Console access?
3. Any recent changes, migrations or redesigns?
4. Who are the top organic competitors?
5. What is the current organic baseline?

## Related skills

Read `references/related-skills.md` when deciding which skill takes over after the audit (web-site-creator, web-keyword, ai-seo, web-indexation, humanize, blog-launch) and for the two adjacent jobs not shipped here.

## Learnings

Durable findings from real audits. **Read this section before auditing** — these are patterns
already paid for; do not re-derive them.

**Who writes here:** the `/founder-pipeline:founder` pipeline's `P4.S4-SourceGap` step (competitor
shipped-HTML teardown) after every stream, and any manual audit that finds something durable.

**Where the write actually lands.** Plugin files are read-only in most installs, so `P4.S4` writes
its dated lines wherever this skill's local overrides live for you — a `SKILL.local.md` beside this
file, or your own learnings store. This section stays as the shipped seed and as the spec for what
a good entry looks like: same heading, same write rules, same one-or-two-line shape. Read both when
you audit; the seed below is not the whole record once the pipeline has run a few times.

**Write rules (enforced — a bad entry is worse than none):**
- **Generalise or don't write it.** *"B2B service pages in this market consistently ship `Service`
  + `BreadcrumbList` but never `FAQPage`"* is a learning. *"That one competitor's pricing page has
  no canonical"* is a stream fact — it stays in that stream's step file.
- One or two lines, carrying **date · page type · territory/vertical · the action it implies**.
- No entry that merely restates the Audit Framework or the checklists above.
- Contradicts an existing entry? Update that entry with the newer evidence rather than appending.

### Entries

Read `references/learnings-entries.md` before auditing (the dated seed entries) and when adding a new entry, to match the shape of the existing ones.

## Output artifacts

| Artifact | Format | Description |
|---|---|---|
| Executive summary | Markdown bullets | Score + coverage, Gate verdict, top 3 issues, quickest win |
| Four-layer scorecard | Table | Per-layer score, weight, measured/unmeasured counts, failing check ids |
| Launch Gate verdict | Pass/fail + blocker list | Binary. Reported separately from the score, always |
| Findings | Table per layer | Issue / Impact / Evidence / Fix / Priority |
| Money page grade | Checklist | Per revenue page, with the offer-shape failures called out first |
| Prioritised action plan | Numbered list | Critical → high impact → quick wins → long-term |
| Keyword cannibalisation map | Table | Pages competing for one term, with the canonical or redirect call |
| Raw checker JSON | JSON | The `seo_checker.py` output, kept so a later run can diff against it |
