---
name: aeo-diagnostic-metrics
description: Scores a page or site on Gartner's four content-optimization diagnostic metrics for Answer Engine Optimization (AEO) — answer extractability, entity attribute coverage, citation rate and citation quality — with a repeatable prompt-set method for citation rate. Use when someone asks whether content is ready to be cited by AI answer engines, wants an AEO baseline, or needs to report AEO progress. Run via /aeo-score.
---

# AEO diagnostic metrics (Gartner)

Source: Gartner table "Content optimization (diagnostic) metrics for AEO" (© Gartner, Inc.). These are DIAGNOSTIC metrics, not outcome metrics: they say whether content is built to be reused by answer engines, not whether the business grew. Do not present them as revenue evidence.

| Metric | What it is | How to measure here |
|--------|-----------|---------------------|
| Answer extractability score | How easily a page can be extracted and reused in generative answers (clear structure and machine-readable context) | Score 0–5 per page: question-style headings, answer in first 1–2 sentences, lists/tables, schema.org markup, no answer hidden behind tabs or scripts |
| Entity attribute coverage | Completeness of entity attributes for a topic or entity (for products: price, features, competitive comparison) | Build the attribute list for the entity first, then % present on the page. Missing price or comparison are the usual gaps |
| Citation rate | How often URLs/assets are cited by answer engines for a defined prompt set | Fixed prompt set (20–50 buyer questions) × engines × same date; citation rate = prompts where your URL is cited ÷ prompts run |
| Citation quality (qualitative) | Quality of the sources and contexts LLMs use when citing the brand | Read each citation: good = accurate, current, on-message; bad = outdated, wrong, competitor-framed |

## Procedure
1. Fix the scope: one entity (product, service or brand) and 1–5 URLs. Ask for them if missing.
2. Extractability: score each URL, quote the evidence (heading text, first sentence).
3. Coverage: list the expected attributes, mark present/absent per URL, give the %.
4. Citation rate: only if the user supplies or approves a prompt set and a way to run it. If answer engines cannot be queried here, output the prompt-set template and mark the metric NOT MEASURED — never estimate it.
5. Citation quality: only from real citations the user pastes. Otherwise NOT MEASURED.
6. Output: scorecard, top 5 fixes by effort/impact, and what was not measured.

Related skills: `old-seo-vs-new-aeo`, `aeo-geo-resources`, `ai-search-visibility`, `gartner-brand-health-framework`.
