---
name: programmatic-seo-content-quality
description: >-
  Use when designing the content layer for programmatic SEO pages: avoiding thin
  content, deduplication, AI generation guardrails, E-E-A-T signals, and
  quality thresholds. Not for one-off blog editing or full template design (use
  programmatic-seo-pages).
---

# Programmatic SEO — content quality

Programmatic pages succeed or fail on whether each page **deserves to exist** on its own. Google's Helpful Content System actively penalizes thin, near-duplicate, doorway pages — and the penalty often hits the whole domain, not just the bad URLs.

Companion: [`programmatic-seo-pages`](../programmatic-seo-pages/), [`seo-meta-tags-spa`](../seo-meta-tags-spa/), [`seo-structured-data`](../seo-structured-data/).

## The single rule

> If a user landed on this URL and 9 nearly identical ones, would they find each useful?

If not, do not publish that row.

## Per-page minimum bar

A programmatic page should have:

- **≥ 300 words** of substantive, page-unique content.
- **At least 3** unique data points (price, stat, testimonial, list item) that vary per row.
- **At least 1** UGC or hand-curated element (review, FAQ answered by a human, local note).
- A reason a user would click your result over the existing top 3.

If you can't hit this for a row, leave it unpublished.

## Data inputs — where uniqueness comes from

| Source | Example |
|--------|---------|
| Public datasets | Census stats, NOAA weather, Wikipedia openings |
| Your own data | Anonymized usage, top searches, customer outcomes |
| User-generated | Reviews, Q&A, before/after photos |
| Computed | "Compare X and Y on price, plan limits, ratings" |
| AI-augmented (with guardrails) | Summaries of UGC, opening paragraphs |

**Mix at least three**. A page built only from AI prose will read like every other AI page.

## AI generation guardrails

If you use an LLM to draft prose:

1. Feed it **structured per-row facts** in the prompt — never let it invent facts.
2. Force a **specific structure** (intro, comparison table, 3 bullet pros/cons, 1 anecdote).
3. **Human review** before `published = true`. Even a 30-second skim catches hallucinations.
4. **Disclose AI** if your audience or regulation requires it.
5. Re-generate on a schedule with refreshed data — don't ship 2024 prices in 2026.

## Deduplication

Run a similarity check across pages before launch:

```sql
-- find suspiciously similar pages
select a.slug, b.slug, similarity(a.body, b.body) as sim
from public.location_pages a
cross join public.location_pages b
where a.slug < b.slug and similarity(a.body, b.body) > 0.80
order by sim desc;
```

(Use `pg_trgm`'s `similarity()`; or compute embeddings + cosine if you need semantic dedup.)

Threshold: kill or merge any pair with **> 0.85** prose similarity.

## E-E-A-T signals

Show **Experience, Expertise, Authoritativeness, Trustworthiness**:

- **Author byline** with photo, role, link to bio.
- **`datePublished` + `dateModified`** visible and accurate (see [`seo-structured-data`](../seo-structured-data/)).
- **Citations** for facts: link to the source.
- **Reviews / testimonials with names**, dates, optional verification.
- **Contact / legal pages** linked from footer (not orphaned).

## Quality gates before publishing

Block `published = true` until each row passes:

- [ ] ≥ 300 words page-unique text
- [ ] No near-duplicate (`similarity < 0.80`) of another page
- [ ] Title and meta unique
- [ ] Hero image exists (real or generated for this row)
- [ ] At least one human-reviewed paragraph
- [ ] No invented facts (LLM output reviewed)

Enforce with a server check, not "the team will remember".

## Pruning

After 90 days in production:

- Identify pages with **zero clicks + zero impressions** (Search Console).
- Set `noindex = true` and remove from sitemap.
- After 180 days with no recovery, set `published = false` and `301` redirect to the parent hub.

This is the most important habit in programmatic SEO: cut what doesn't work.

## Avoid

- Shipping 5,000 rows on launch day. Start with 100 best; expand by 100/week.
- Identical headline structure ("Best X in Y") with nothing else unique.
- Auto-translated content without native review.
- Stuffing locations into a single page (`Atlanta, Boston, Chicago, …`) hoping one ranks.
- Using AI to invent reviews or testimonials (illegal in many jurisdictions; always against Google guidelines).

## Checklist

- [ ] Quality gate enforced at the `published` flag.
- [ ] Deduplication script run before each batch publish.
- [ ] Human review per row, recorded with reviewer + timestamp.
- [ ] Monthly pruning of zero-traffic pages.
- [ ] Author / source / date signals visible on every page.
