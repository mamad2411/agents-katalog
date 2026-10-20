---
name: rz-content-optimize
description: >
  Use when an article on richezamor.com needs SEO or AIO (answer-engine optimization) recommendations. Trigger when optimizing a draft, when rz-draft-content invokes it as a sub-step, or when asked for keyword research, SERP analysis, internal linking, schema markup, or AI-citation optimization. Skip for site-level SEO strategy (that's rz-growth-marketing).
---

# Content Optimize, Riché Zamor

You produce heavy SEO and AIO recommendations for long-form articles. Output is prescriptive and actionable. Every recommendation ties to a measurable SEO outcome (ranking, CTR, crawlability) or a measurable AIO outcome (citation likelihood in LLM answers, featured snippet capture, entity association).

## Before beginning work

The corpus has migrated to Notion. Notion is the source of truth — the local `corpus/*` paths cited below are historical and may drift. Always load these references via the Notion MCP (`mcp__bc2cd475-c3cd-49fa-a4ab-02ee9f795171__notion-fetch`) before executing this skill:

1. **Strategy Stack README** — Notion page `357ac0ea-4f65-81b8-98b4-ffd0f376198c` (`Brand > README — Strategy Stack`). Doc ownership, canonical constants (thesis label, channels, cadence, North Star), and the Decision-of-Record log. Honor it; flag drift.
2. **Your section of the Corpus** at `Projects > RZ Claude Skills > Corpus`:
   - `growth` → page `357ac0ea-4f65-812a-a480-d3b7ab463bc2` (especially the `seo/` sub-page)

Each Corpus directory page lists its child entries. Fetch only the specific entries you need.

## Quick Reference

| Situation | Load | Notes |
|---|---|---|
| Optimizing a draft article | Article body, target topic, slug (or recommend one) | Produce the 12-section block under "SEO & AIO Optimization" |
| Keyword research and SERP analysis | `references/keyword-research.md` plus `corpus/growth/seo/` | SEO methodology owned by `rz-growth-marketing` |
| Title, meta, slug variants | `references/title-meta-slug.md` | 3 title options, 1 primary plus 1 alt meta, slug under 60 chars |
| H2 structure and entity coverage | `references/content-structure.md` | Current vs. recommended; name entities for LLM citation |
| Quotables, schema, AIO hooks | `references/aio-optimization.md` | 3-5 pull-quote sentences, JSON-LD, question-based H2s |
| Internal and external linking | `references/internal-and-external-linking.md` | Link to other Content Topics, cite 3-5 high-authority sources |

## When This Skill Runs

Two entry points:

1. **Invoked by `rz-draft-content`** after step 6 (Content Topic page created). The draft article body is passed in context.
2. **Invoked directly by Riché** to optimize an existing article or new draft.

Inputs required before producing recommendations: the article body (or Notion page link), the target topic (one-sentence summary), and the intended URL slug if decided. If the slug isn't decided, recommend one as part of the output.

## The Output Contract

Every optimization pass produces a structured block added to the Content Topic's Notion page under a section titled **"SEO & AIO Optimization"**. The block contains:

1. **Target keyword analysis** (primary + 3-5 secondary)
2. **Title variants** (3 options with rationale)
3. **Meta description** (1 primary + 1 alternate, both under 160 chars)
4. **URL slug recommendation**
5. **H2 structure review** (current vs. recommended)
6. **Entity coverage** (named entities, concepts, people the piece should mention for LLM citation)
7. **Quotable sentences** (3-5 sentences optimized for LLM pull-quotes)
8. **Internal linking** (specific links to other Content Topics)
9. **External authority links** (3-5 high-authority sources to cite)
10. **Schema markup** (JSON-LD recommendation)
11. **AIO hooks** (question-based H2 additions, FAQ section if warranted)
12. **Competitor piece review** (top 3 SERP competitors and where Riché's piece differentiates)

If any section doesn't apply, say so explicitly rather than skipping it.

## The 13 Steps (load the relevant reference for procedure)

For canonical SEO methodology (free-stack approach, topic clusters, Target Keywords DB), load `corpus/growth/seo/`. SEO is owned by `rz-growth-marketing`; this skill applies it per-article.

- **Steps 1-2: Keyword research and SERP analysis.** See `references/keyword-research.md`.
- **Steps 3-5: Title variants, meta description, URL slug.** See `references/title-meta-slug.md`.
- **Steps 6-7: H2 structure review and entity coverage.** See `references/content-structure.md`.
- **Steps 8, 11, 12: Quotable sentences, schema markup, AIO hooks.** See `references/aio-optimization.md`.
- **Steps 9-10: Internal and external linking.** See `references/internal-and-external-linking.md`.
- **Step 13: Competitor differentiation.** See `references/competitor-differentiation.md`.
- **Output format.** See `references/output-format.md`.

## Voice & Scope Constraints

This skill produces optimization recommendations. It does NOT rewrite Riché's prose. If a recommendation requires a prose change (rewriting an H2, adding a definition sentence, sharpening a quotable), present it as a suggested edit with original and proposed versions side by side. Let Riché make the call.

Do NOT stuff keywords. Do NOT recommend changes that compromise the piece's voice. If an SEO best practice conflicts with the Content Style Guide, prioritize voice and say so explicitly.

## Common Mistakes

| Mistake | What goes wrong | Fix |
|---|---|---|
| Rewriting Riché's prose to fit a keyword | Voice match breaks, recommendation overrides source of truth | Present a side-by-side suggested edit; let Riché decide |
| Stuffing the primary keyword into every H2 | Reads as SEO content, kills AIO citation odds | One primary keyword per H2 maximum, secondaries used naturally |
| Skipping competitor SERP review | Differentiation claims become guesses, output loses credibility | Run step 13 from `references/competitor-differentiation.md` on every pass |
| Skipping a section because "it doesn't apply" | Output is incomplete, downstream readers cannot tell if it was considered | State explicitly that the section does not apply and why |
| Recommending external links without authority check | Sends ranking signal to weak sources | Verify domain authority before listing the 3-5 external citations |

## Cross-skill connections

**Upstream (reads from these for canonical knowledge):**
- `rz-copywriting`. Source of truth for voice and style. This skill never overrides it. When a recommendation conflicts with voice, this skill flags it and lets Riché decide.
- `rz-growth-marketing`. Owns the canonical SEO methodology (free-stack approach, topic clusters, Target Keywords DB) loaded from `corpus/growth/seo/`. This skill applies that methodology per-article.

**Downstream (hands off to these for execution):**
- `rz-draft-content`. This skill is invoked by step 7 of the draft pipeline. Output is the structured "SEO & AIO Optimization" block written into the Content Topic's Notion page.
