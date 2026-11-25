---
name: geo-content
description: "E-E-A-T and content quality assessment for AI citability: scores experience, expertise, authoritativeness, and trustworthiness, plus word count, readability, structure, freshness, topical authority, and low-quality AI content signals, and writes GEO-CONTENT-ANALYSIS.md. Use when the user wants a content quality review of a page or blog, or asks whether their content is credible enough to be cited."
version: 1.0.0
author: geo-seo-claude
tags: [geo, content-quality, eeat, citability, ai-content, topical-authority]
---

# GEO content quality and E-E-A-T assessment

## Purpose

AI search platforms do not just find content — they evaluate whether content deserves to be cited. The primary framework for this evaluation is **E-E-A-T** (Experience, Expertise, Authoritativeness, Trustworthiness), which per Google's December 2025 Quality Rater Guidelines update now applies to **ALL competitive queries**, not just YMYL topics. Content that scores high on E-E-A-T is dramatically more likely to be cited by AI platforms.

Two lenses:
1. **E-E-A-T signals** — does the content demonstrate real expertise and trust?
2. **AI citability** — is the content structured so AI platforms can extract and cite specific claims?

## Operational protocol

1. Fetch the target page(s) — homepage, key blog posts, service/product pages
2. Evaluate E-E-A-T across the 4 dimensions (25 points each) using rubrics in `signals.md`
3. Assess content quality metrics (word count, readability, paragraph/heading structure, internal linking) using `scoring.md`
4. Check for low-quality AI content signals (see `signals.md`)
5. Evaluate content freshness and topical authority modifier (`scoring.md`)
6. Score and generate `GEO-CONTENT-ANALYSIS.md` using the template in `templates.md`

## References

- `signals.md` — per-signal scoring rubrics for all 4 E-E-A-T dimensions, plus AI content quality signals (low/high)
- `scoring.md` — word count benchmarks, readability, paragraph/heading/linking rules, freshness scoring, topical authority modifier
- `templates.md` — `GEO-CONTENT-ANALYSIS.md` output template

---

## Final scoring (0-100)

| Component | Weight | Max points |
|---|---|---|
| Experience | 25% | 25 |
| Expertise | 25% | 25 |
| Authoritativeness | 25% | 25 |
| Trustworthiness | 25% | 25 |
| **Subtotal** | | **100** |
| Topical Authority Modifier | | +10 to -5 |
| **Final Score** | | **Capped at 100** |

### Interpretation

- **85-100**: Exceptional — strong AI citation candidate across platforms
- **70-84**: Good — solid foundation, specific improvements will increase citability
- **55-69**: Average — multiple E-E-A-T gaps reducing AI visibility
- **40-54**: Below Average — significant content quality and trust issues
- **0-39**: Poor — fundamental content strategy overhaul needed
