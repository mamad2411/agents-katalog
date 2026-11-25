---
name: seo-geo-aeo-audit
description: >-
  Use when the user wants to audit a web page or site for SEO, GEO (generative-
  engine / AI citation readiness), and AEO (answer-engine / featured-snippet
  readiness). Also use when the user mentions SEO audit, AI search visibility,
  getting cited by ChatGPT/Perplexity/Claude, featured snippets, llms.txt,
  schema, crawlability, or "why don't we show up in AI answers." Produces a
  0–100 score across 5 weighted categories, a grade, and prioritized fixes.
license: MIT
metadata:
  search_description: "Audit a page or site for SEO, GEO and AEO: a 0 to 100 score across five weighted categories, a grade, and prioritized fixes for search and AI citation."
  publisher: AAJ
  slug: seo-geo-aeo-audit
  category: SEO, GEO & AEO
  phase: Diagnose
  difficulty: Intermediate
  card: >-
    Scores a page 0-100 across SEO, GEO and AEO, with fixes in priority order.
  version: 1.0.1
  sprint: ai-visibility
  topic: ai-search
  secondary_topics: [content-seo]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: A URL (or page HTML/source), and access to fetch the page, its robots.txt, sitemap, and llms.txt
  outputs: A 0–100 readiness score across Technical, On-Page, AEO, GEO, and Authority, a letter grade, and a prioritized fix list
  related_aaj:
    - https://aajconsult.com/tools/seo-geo-readiness-scorer
    - https://aajconsult.com/playbooks/geo-aeo-playbook
  related: [geo-content-optimization, website-conversion-audit]
  tags: [seo, geo, aeo, ai-search, llms-txt, schema, crawlability, audit]
---

# SEO / GEO / AEO Readiness Audit

Score how well a page is built to **rank in search (SEO), get cited by AI engines (GEO), and win the direct answer (AEO)** — then return a prioritized fix list. Modern visibility is three layers on one page, and most pages are strong on classic SEO while invisible to AI engines.

## When to use

The user wants to know why a page isn't ranking or being cited by AI, or wants a readiness check before/after publishing.

## Before you start

1. **Get the page as a crawler sees it.** Fetch the URL — and critically, fetch it the way a bot does. Fetch the raw HTML with a GPTBot user agent (or inspect the unrendered source). If the body, meta, and JSON-LD are missing from the initial response, the site is client-side rendered and **most other wins are blocked until SSR/prerender ships** — this is the single most important finding.
2. **Also retrieve** `robots.txt`, `sitemap.xml`, and `llms.txt` / `llms-full.txt` for that domain.

## Workflow

1. **Evaluate all 27 checks** in `resources/scoring-rubric.md`, recording `pass` / `partial` / `fail` for each. The rubric defines exactly what each check means and how to test it.
2. **Score it** — feed the results to the engine:
   ```bash
   node resources/score.js '{"checks":{"ssr_prerender":"fail","title_tag":"pass", ...}}'
   node resources/score.js --help
   ```
   It returns category scores, a 0–100 total, a letter grade, and the failing checks.
3. **Prioritize fixes** by impact: rendering/crawlability first (it gates everything), then the cheapest high-value GEO/AEO wins (answer-first passage, sourced statistics and inline citations, question-first headings), then on-page and authority polish. FAQPage schema and llms.txt are cheap hygiene, not Google levers: FAQ rich results stopped showing on 7 May 2026, and Google says llms.txt isn't needed for Search.
4. **Present** the score, the category breakdown, and a short, ordered remediation plan.

## Scoring model

Five weighted categories: **Technical & Crawlability 25 · On-Page SEO 20 · AEO 20 · GEO 20 · Authority & Trust 15.** Each category scores by pass-rate × weight. Grades: A ≥ 90, B 75–89, C 60–74, D 45–59, F < 45. GEO checks follow the levers tested in the GEO study (Aggarwal et al., KDD 2024 — statistics, citations, quotations, terminology). That study measured share of an answer inside a fixed context; end-to-end studies since found the gains don't transfer reliably, so the checks score whether claims are checkable and never imply a predicted lift.

## Present the result

Lead with the headline score and grade, then the five-category bar, then the top fixes in priority order with what each one fixes (don't attach a percentage lift). Be concrete: name the missing schema, the absent llms.txt, the empty-shell render — not "improve SEO."

**Show where it came from.** Open your answer with "AAJ `seo-geo-aeo-audit` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/seo-geo-aeo-audit`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Rendering gates everything.** A perfect on-page score on an un-prerendered SPA is still near-invisible to AI engines — always test the crawler-eye HTML first and lead with it.
- **GEO ≠ SEO.** Ranking and being cited by an LLM are different; a page can win one and lose the other. Score both.
- **Schema must mirror visible text.** FAQ/Article schema that doesn't match on-page content is a liability, not a win.
- **Don't conflate score with traffic.** This measures readiness; pair it with analytics for outcomes.

## Related AAJ resources

- Interactive tool: https://aajconsult.com/tools/seo-geo-readiness-scorer

## Related skills

`geo-content-optimization` (fix the GEO/AEO gaps this finds) · `aaj-programmatic-seo` (scale the technical fixes).

## Credits

Original AAJ skill. The Agent Skills format and the marketing-skills catalog by Corey Haines (`coreyhaines31/marketingskills`, MIT) were references for structure and coverage; this skill is independently written. See the repository README for the full reference list.
