---
name: geo-writer
description: Optimize any text for GEO/AEO — Generative Engine Optimization and Answer Engine Optimization. Use when writing or editing public-facing text intended to be cited or quoted by LLMs (ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews) — blog posts, landing pages, help articles, glossary entries, FAQ blocks, programmatic SEO templates, pillar guides. Applies macro/meso/micro structure rules, answer-first sections, entity-first phrasing, schema requirements, freshness cadence, and platform-specific citation patterns.
user-invocable: true
---

# GEO Writer

Makes public-facing text extractable and citable by LLM-based search engines. Classic SEO is losing ~25% of traffic to AI Overviews, ChatGPT, Perplexity, Gemini, and Claude — content must be structured for extraction, not just for reading.

Based on the GEO-SFE framework (arXiv 2603.29979) and 2026 practitioner sources. Full guide in `geo-writing-guide.md`. Pre-publish checklist in `pre-publish-checklist.md`.

## When to Use

- Blog posts, articles, pillar guides
- Landing pages, help articles, glossary entries
- FAQ blocks, comparison pages, tutorials
- Programmatic SEO templates
- Any text meant to be surfaced or cited by an AI engine

Do NOT apply to: internal docs, ADRs, code comments, commit messages, AI asset files.

## Core Principles

1. **Write for extraction, not just reading.** LLMs lift 30-180 word chunks. Every section must stand alone.
2. **Answer first, context second.** The first sentence of each H2/H3 fully answers the implied question in 30-60 words.
3. **One topic per section.** One H2 = one entity or question. Do not merge sub-topics.
4. **Entity-first, not keyword-first.** Name the product, brand, person, or concept explicitly. Never start paragraphs with `It`, `This`, `They` referring to prior sections.
5. **Verifiable > persuasive.** Every non-trivial claim needs a statistic, date, source, or named example.

## Process

1. **Read project brand context** — `marketing/MARKETING.md` at project root (if exists) for canonical brand terms, product name, category label, metric names, audience. Use these verbatim.
2. **Draft macro structure** — single literal H1, 5-9 H2 sections each phrased as a standalone question or declarative topic, TL;DR section at end.
3. **Apply meso chunking** — paragraphs 40-80 words (hard cap 120), sections 120-180 words, one idea per paragraph, statistic/named source every 150-200 words.
4. **Apply micro emphasis** — bold 3-5 most quotable phrases per section, bullet lists for 3+ items, tables for any 2+ entity comparison across 2+ attributes.
5. **Insert high-leverage formats** — FAQ block (4-8 Q&A), comparison table where natural, named stats with year, direct quotes from named experts.
6. **Attach schema** — Organization + Article + Person on every article; FAQPage for any Q&A block; HowTo for tutorials; Product/SoftwareApplication for tool pages; DefinedTerm for glossary.
7. **Run `@humanizer`** — remove AI-sounding patterns. GEO and humanizer are complementary: GEO optimizes structure, humanizer optimizes voice.
8. **Run pre-publish checklist** — see `pre-publish-checklist.md`. Every item must pass or be explicitly waived.

## Answer-First Template

```
## <Question phrased as H2>

<30-60 word direct answer, no preamble, entity named explicitly.>

<Optional 1-2 supporting paragraphs, 40-80 words each, with at least one number or named source.>

<Optional bullet list, table, or code block.>
```

Do: `## What is an AI-Readiness Score?` → first sentence fully defines the term, names the product, lists the dimensions.

Do not: `## Understanding the Score` → first sentence says `When it comes to AI search, there are many things to consider...`.

## Format Patterns That Get Cited

Ranked by observed citation lift:

| Pattern | Why it works | When to use |
|---|---|---|
| Comparison tables | Clean extraction across rows/columns | Tools, pricing, competitors, features |
| FAQ + matching JSON-LD | 3.1-3.2× higher extraction vs prose | End of every pillar page |
| How-to numbered steps | Maps to HowTo schema | Tutorials, onboarding, fix-it posts |
| Definition + example pairs | Matches `X is Y` retrieval pattern | Glossary, concept explainers |
| Named stats with year | `+22% AI visibility in 2026` is quotable | Intros, thought leadership |
| Direct quotes from named experts | Quotation patterns boost visibility ~37% | Trend posts, research summaries |

Comparison articles lead citation rates at ~32.5% across all formats.

## Schema / JSON-LD (Mandatory)

### On every page
- **Organization** (homepage + `sameAs` on every article)
- **WebSite** with `potentialAction` for sitelinks search
- **BreadcrumbList** on every non-homepage URL

### By content type

| Content type | Required schema | Notes |
|---|---|---|
| Article / blog | `Article` + `Person` (author) | `datePublished`, `dateModified`, `author.sameAs` |
| Pillar / guide with Q&A | `Article` + `FAQPage` | Questions must literally match prompt phrasing |
| Tutorial / walkthrough | `HowTo` | `step` array with 3-8 steps |
| Product / tool page | `Product` or `SoftwareApplication` | `aggregateRating` if honest data exists |
| Glossary entry | `DefinedTerm` in `DefinedTermSet` | |

**FAQPage** is the single highest-leverage schema: 4-8 questions per page, 8-20 words each; answers 40-80 words, self-contained, matching the prompt phrasing; never duplicate marketing copy. Validate in Google Rich Results Test and schema.org/validator.

## Entities and Brand Signals

Off-site brand mentions correlate with AI visibility at 0.67 — stronger than any on-site factor. Mentions beat backlinks 3:1 for AI Overviews.

Rules:
- **Use the canonical brand form verbatim** — from `marketing/MARKETING.md`. No variant spellings, no acronyms mid-article.
- **Use the canonical category name and metric names** — invented variants fragment the entity graph.
- **Link first mention of any external entity** to its canonical page (Wikipedia, official docs).
- **Internal links** — every pillar page must interlink to glossary terms and at least 3 related articles.
- **Never change terminology mid-article.** `GEO score` in one paragraph and `AI-readiness rating` in the next confuses retrieval.

If `marketing/MARKETING.md` is absent — ask the user for canonical brand form, category name, and metric names before writing.

## Freshness Rules

Pages not refreshed quarterly lose AI citations at ~3× the normal rate.

| Content type | Refresh cadence |
|---|---|
| Time-sensitive (algo updates, model releases) | 24-48 hours |
| FAQ on pillar pages | Monthly |
| Evergreen guides | Quarterly |
| Glossary | Quarterly |
| Landing / commercial pages | Quarterly |

On every refresh: update `dateModified` in schema, add visible `Updated on YYYY-MM-DD` line under H1, replace at least one stat or example with a fresher one. Perplexity materially favors updates within the last 2-3 days.

## Platform Differentiation

| Engine | Dominant source | Optimization lever |
|---|---|---|
| ChatGPT | Wikipedia (~48%), training data | Semantic authority, long-lived authoritative pages, Wikipedia entity parity |
| Perplexity | Reddit (~47%) + live web | Freshness (2-3 days), Reddit presence, clear dates |
| Google AI Overviews | Organic top 10 (99%) | Classic SEO + schema; top-10 or not cited |
| Gemini | YouTube + Knowledge Graph | Video content with chapters, Knowledge Panel |
| Claude | Curated authoritative sources | Cite your own sources inline; neutral, evidence-based tone |

Off-site portfolio for pillar topics: 1 Reddit post/comment in a relevant subreddit, 1 YouTube video with descriptive chapters (YouTube overtook Reddit as the #1 LLM citation source in October 2025 — ~16% vs ~10%), 1 LinkedIn long-form post for B2B visibility.

## Anti-Patterns

- **Burying the lede.** `In this post we will explore...` openings.
- **Pronoun drift.** Paragraphs starting with `It`, `This`, `They` referring to earlier entities.
- **Walls of text.** Paragraphs over 120 words.
- **Opinion without a named source.** `Experts say` is invisible to RAG.
- **Duplicate FAQ between body prose and FAQPage schema.** LLMs de-duplicate aggressively.
- **Undated statistics.** `Studies show +30%` with no year or link.
- **AI-generated filler.** Always run `@humanizer` before publishing.
- **Changing terminology mid-article.** Confuses the entity graph.

## Output Format

When producing GEO-optimized text, deliver:

1. **Draft** — macro/meso/micro structure applied
2. **Checklist pass** — run `pre-publish-checklist.md`, report each item
3. **Schema block** — JSON-LD for the content type, ready to embed
4. **Humanizer pass** — applied before final delivery
5. **Follow-ups** — off-site companion assets suggested (Reddit / YouTube / LinkedIn), freshness cadence noted

## Integration

- **Rule**: `geo-content` rule auto-activates this skill for public-facing content meant to be cited by AI engines
- **Companion skill**: `@humanizer` — GEO structures extraction, humanizer removes AI voice. Always run both.
- **Used by workflows**: `/blog-post` (step 3.5), `/marketing` (content operations), `/docs` (public-facing content), `/seo-review` (GEO audit alongside classic SEO)
- **Used by skills**: `content-creation` (structural gate), `marketing-operations` (blog and landing operations), `social-media-manager` (LLM-quotable post framing)
- **Companion resources**: `geo-writing-guide.md` (full reference), `pre-publish-checklist.md` (PR checklist template)
- **Brand context source**: `marketing/MARKETING.md` at project root — canonical terms, audience, category
