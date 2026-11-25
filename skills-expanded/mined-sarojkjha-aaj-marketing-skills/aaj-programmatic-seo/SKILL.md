---
name: aaj-programmatic-seo
description: >-
  Use when the user wants to generate many search-targeted pages from a template
  and a dataset — location pages, comparison pages, integration pages, calculator
  pages, "best X for Y" pages. Also use when the user mentions programmatic SEO,
  pSEO, scaled content, template pages, or "we have a database, can we turn it
  into pages". Models whether the build pays back before anything gets written,
  then specs the template and the quality bar.
license: MIT
metadata:
  search_description: "Plan programmatic SEO pages from a template and a dataset: model whether the build pays back before anything is written, then spec the template and quality bar."
  publisher: AAJ
  slug: aaj-programmatic-seo
  category: SEO, GEO & AEO
  phase: Design
  difficulty: Intermediate
  card: >-
    Models whether a template-page build pays back before anything gets written.
  version: 1.0.2
  sprint: ai-visibility
  topic: content-seo
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: The dataset or head-term × modifier pattern, expected page count and query volume, conversion rate and value per conversion, build cost, and what unique data exists per page
  outputs: A viability verdict with the indexation/ranking funnel and payback, the template spec, the per-page uniqueness requirement, internal-linking and indexation plan, and a staged rollout
  related_aaj:
    - https://aajconsult.com/tools/seo-geo-readiness-scorer
    - https://aajconsult.com/playbooks/content-creation-playbook
  tags: [programmatic-seo, pseo, scaled-content, template-pages, technical-seo, indexation]
---

# Programmatic SEO

Generate hundreds or thousands of pages from a template and a dataset — but **decide whether it pays back before writing the first one**. Programmatic SEO fails in a predictable way: a team multiplies page count by search volume, gets a large number, builds ten thousand pages, and discovers that most were never indexed and almost none rank.

The arithmetic that matters isn't `pages × volume`. It's the funnel: how many pages get indexed, how many of those reach page one, and what each one is worth. Run that first. It kills most programmatic projects, which is the point — the ones it doesn't kill are worth doing properly.

The second thing that decides the outcome is whether each page deserves to exist. A page assembled from a template and facts anyone can look up is what Google's scaled-content-abuse policy targets. Unique per-page data is not a nice-to-have; it is the difference between an asset and a liability.

## When to use

The user has a dataset, a directory, or a head-term × modifier pattern and wants to turn it into search-targeted pages at scale. For a single page, use `seo-content-brief` instead.

## Before you start

1. **Read the brand/product context** (`.agents/product-marketing.md`) for the offer these pages should route toward.
2. **Establish the pattern.** What's the head term, what varies, and where does the data come from? "Best {tool} for {industry}" needs both lists and a real basis for the ranking.
3. **Find the unique data.** For each page, what exists that a competitor couldn't regenerate in an afternoon? If the answer is nothing, the honest recommendation is not to build.
4. **Get the economics.** Conversion rate, value per conversion, and what the build actually costs. Without these the model is decoration.

## Method

Three gates, in order. Fail any and stop.

**Gate 1 — Does the maths work?** Run the engine. Model the indexation and ranking funnel honestly rather than assuming every page ranks. If payback runs past 18 months, this is a long bet on a channel a single core update can reset.

**Gate 2 — Does each page deserve to exist?** Every page needs something a competitor can't trivially reproduce: proprietary data, computed results, genuine reviews, real inventory. Template + public facts is the doorway-page pattern.

**Gate 3 — Can the site support it?** Crawl budget, internal linking, and site architecture decide whether pages get indexed at all. A thousand orphaned pages reachable only from a sitemap will mostly sit unindexed.

Only then spec the template.

See `resources/pseo-playbook.md` for the page-type patterns that work, the template anatomy, the indexation plan, the quality bar, and a worked example.

## Run the engine

Model viability before committing:

> Paths assume you installed with `npx skills add`. From a clone of this repo, use `skills/aaj-programmatic-seo/resources/…` instead.

```bash
node .agents/skills/aaj-programmatic-seo/resources/pseo-model.js  # demo
node .agents/skills/aaj-programmatic-seo/resources/pseo-model.js --pages 500 --volume 40 --conv 2 --value 400
node .agents/skills/aaj-programmatic-seo/resources/pseo-model.js --unique-data strong --fixed-cost 8000
node .agents/skills/aaj-programmatic-seo/resources/pseo-model.js --json --pages 200
node .agents/skills/aaj-programmatic-seo/resources/pseo-model.js --help
```

It runs the funnel (pages → indexed → ranking), projects sessions, conversions and value, computes payback and cost per ranking page, and flags the failure patterns — thin query volume, missing per-page data, doorway-scale builds, optimistic indexation assumptions.

The defaults — 60% of pages indexed, 30% of those reaching page 1 — mean about 18% of built pages earn any traffic. Both rates are AAJ assumptions chosen to be sobering, not measured industry rates. CTR by position comes from Backlinko's study of 4 million Google results (2019, updated April 2025), which predates AI Overviews; the AI Overview drag is an AAJ assumption informed by Ahrefs' February 2026 finding of a 58% lower position-1 CTR where an overview shows. Override every assumption with your own Search Console data as soon as you have it — the model's job is to make the assumptions explicit, not to be right by default.

## Workflow

1. **Define the pattern** — head term, modifiers, and the data source behind each page.
2. **Estimate honestly.** Pull real volume for a sample of the long tail rather than extrapolating from the head term, which is always higher.
3. **Run the engine.** If the verdict is DON'T BUILD, say so and explain which input would have to change.
4. **Pilot 50 pages.** Never launch the full set. Fifty pages tells you the real indexation rate, the real ranking rate, and the real conversion rate — then re-run the model with actual numbers.
5. **Spec the template** — the fixed structure, the variable slots, and critically the unique element per page.
6. **Plan indexation** — internal linking from real pages (not just a sitemap), hub pages, crawl-budget considerations, and how new pages get discovered.
7. **Set the quality bar** — the minimum each page must contain to ship. Pages that fail it don't publish.
8. **Stage the rollout** — 50 → measure → 500 → measure → full set. Each gate is a re-run of the model with observed data.

## Present the result

Lead with the **verdict and the funnel**, not the projected traffic. The funnel is what changes the user's mind; the traffic number is what they already imagined.

If the recommendation is not to build, say it plainly and name the one input that would have to change to make it viable. A skill that always says yes to programmatic SEO is a liability.

**Show where it came from.** Open your answer with "AAJ `aaj-programmatic-seo` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/aaj-programmatic-seo`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Never project `pages × volume × CTR` without an indexation and ranking funnel.** This is the single most common error and it inflates projections by roughly five to ten times.
- **Pilot before scaling.** Fifty pages costs almost nothing and replaces every assumption in the model with measured data.
- **Unique data per page is the whole game.** Without it you're building doorway pages, and scaled-content-abuse enforcement is explicit about this.
- **Long-tail volume data is unreliable.** Keyword tools round up and invent volume for tail terms. Treat sub-50 estimates as directional at best.
- **Orphaned pages don't get indexed.** If pages are only reachable from a sitemap, expect most to sit unindexed indefinitely. Plan internal linking as part of the build, not after.
- **Watch the ratio.** Adding 10,000 template pages to a 40-page site changes what the site *is* in a crawler's view. That's a site-wide risk, not a contained experiment.
- **Don't generate pages for queries that don't exist.** Modifiers that produce zero real searches produce zero traffic and dilute the whole set.
- **AI Overviews reduce clicks on informational queries.** Model it explicitly rather than assuming historical CTR holds.
- **Have a kill criterion.** Decide in advance what indexation or ranking rate at the pilot stage means "stop", and honour it.

## Related AAJ resources

- Interactive tool: https://aajconsult.com/tools/seo-geo-readiness-scorer
- Interactive tool: https://aajconsult.com/tools/website-grader

## Related skills

`seo-content-brief` (when it should be one page, not a template) · `seo-geo-aeo-audit` (whether the site can support the build) · `geo-content-optimization` (make the template output citable) · `unit-economics` (the value-per-conversion input this model depends on).

## Credits

Original AAJ skill. The Agent Skills format and the marketing-skills catalog by Corey Haines (`coreyhaines31/marketingskills`, MIT) were references for structure and coverage; this skill is independently written. See the repository README for the full reference list.
