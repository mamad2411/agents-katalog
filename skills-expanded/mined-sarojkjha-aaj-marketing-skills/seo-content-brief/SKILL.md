---
name: seo-content-brief
description: >-
  Use when the user wants to plan or spec a piece of content before writing it —
  a content brief, an outline for a target keyword, or a blog post that needs to
  rank and get cited. Also use when the user mentions content brief, keyword
  targeting, search intent, SERP analysis, outlining an article, or "what should
  this post cover". Produces a writer-ready brief: intent classification, the
  answer block, heading structure, entities to cover, citation and internal-link
  targets, and the cannibalisation check.
license: MIT
metadata:
  search_description: "Plan a piece of content before writing it: search intent, an answer block, headings, entities, sources to cite, internal links and a cannibalisation check."
  publisher: AAJ
  slug: seo-content-brief
  category: SEO, GEO & AEO
  phase: Design
  difficulty: Starter
  card: >-
    Produces a writer-ready brief: intent, answer block, entities, internal links.
  version: 1.1.1
  sprint: ai-visibility
  topic: content-seo
  secondary_topics: [ai-search]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: Target query, the audience and their awareness state, what currently ranks for it, existing pages on the topic, and the business outcome the page should drive
  outputs: A writer-ready brief — intent classification, the 40-60 word answer block, H2/H3 structure, entities and subtopics to cover, citation and statistic targets, internal links, schema type, and success criteria
  related_aaj:
    - https://aajconsult.com/tools/seo-geo-readiness-scorer
    - https://aajconsult.com/resources/content-calendar-repurposing-tracker
    - https://aajconsult.com/playbooks/content-creation-playbook
  tags: [seo, content-brief, search-intent, keyword-targeting, aeo, content-planning]
---

# SEO Content Brief

Spec a piece of content **before anyone writes it**, so it can rank on search *and* be cited by AI engines. A brief is not an outline — an outline says what sections exist; a brief says what job the page does, what question it answers in the first hundred words, which entities it must cover to be considered complete, and what would make it citable rather than merely readable.

The single most expensive content mistake is writing to a keyword instead of to an intent. A page that targets "marketing budget" without deciding whether the searcher wants a benchmark, a calculator, or a consultant will satisfy none of them.

## When to use

The user is planning content that hasn't been written yet — a blog post, a guide, a landing page, a comparison page. If the content already exists, use `seo-geo-aeo-audit` to find the gaps or `geo-content-optimization` to fix them.

## Before you start

1. **Read the brand/product context first** (`.agents/product-marketing.md` / `.agents/aaj-brand.md`) for audience, voice, and the offer this content should route toward.
2. **Get the target query and the business outcome.** A brief without a defined next action produces content that ranks and converts nothing.
3. **Look at what actually ranks.** Ask the user to paste the current top results, or fetch them. The SERP is the clearest available statement of what the engine believes the intent is — arguing with it rarely works.
4. **Inventory existing pages on the topic.** Cannibalisation is easier to prevent than to unwind.

## Method

Four decisions drive the brief, in order:

**1. Intent.** Classify it — informational, commercial-investigation, transactional, or navigational — from the SERP, not from the words in the query. If the top ten are all listicles, that intent is settled regardless of what you'd prefer to publish.

**2. The answer block.** Decide the single question this page answers and write the 40–60 word answer that goes near the top. This is what answer engines extract and what AI engines cite. Content that buries its answer in paragraph six is invisible to both.

**3. Coverage.** List the entities and subtopics the page must address to read as complete. Completeness against the topic beats word count — "aim for 2,000 words" is a proxy that produces padding.

**4. Citability.** Specify what makes the page worth citing rather than summarising: original data, a named source per claim, precise statistics, a real example. The GEO study (Aggarwal et al., KDD 2024) found quotations, statistics and cited sources raised a page's share of an AI answer by roughly 27–41% — but inside a fixed five-source context, and end-to-end studies since found the gains don't transfer reliably. Brief for them because they make the page checkable and worth citing, not for a predicted lift. That is a structural property you brief for, not a style you edit in later.

See `resources/brief-template.md` for the full template, the intent-to-format map, the entity checklist, the cannibalisation test, and a worked example.

## Workflow

1. **Classify intent from the SERP** and name the format it demands (guide, comparison, tool, listicle, definition).
2. **Run the cannibalisation check.** If an existing page already targets this intent, the answer is usually to improve that page rather than publish a second one. Two pages competing for one intent split authority and often both drop.
3. **Write the answer block** — 40–60 words, direct, no preamble. If you can't write it, the topic isn't clear enough to brief.
4. **Build the heading structure.** Phrase H2s as the questions people actually ask; answer each in the first two sentences beneath it. This is what makes a page extractable.
5. **List entities and subtopics** the page must cover, drawn from what ranks and from the questions in People Also Ask.
6. **Specify citations, statistics and sources** — the named sources the writer must cite, and where original data or a real example goes.
7. **Assign internal links** — which existing pages link in, and which page or offer this one routes to.
8. **Name the schema type** (Article, FAQPage, HowTo, Product) and any required fields.
9. **Set success criteria** — the ranking, citation, or conversion outcome that would make this page worth having written.

## Run the tool

```bash
node resources/brief-check.js --demo
node resources/brief-check.js '{"query":"...","action":"...","serp":["title that ranks today","..."],"intent":"commercial","format":"comparison","answer":"...","existing":["/blog/page - commercial"],"entities":["..."],"headings":["...?"],"sources":["named source - URL"],"linksIn":["/page"],"schema":"Article","success":"..."}'
node resources/brief-check.js --help
```

`build(input)` reads the intent from the pasted titles (each title votes once, for its strongest format signal), lists the issues as blockers and smaller gaps, and gives the verdict: *Not ready for a writer*, *Ready, with gaps* or *Ready for a writer*. `briefText(input)` writes the brief in the same Markdown as the page. Add `--json` for both as one object.

This is the code of the AAJ Content Brief Builder (https://aajconsult.com/tools/content-brief-builder), byte for byte; the site's guard fails if the two drift. Run it once the ranking titles, existing pages and draft answer block are in hand (workflow steps 1-3), and again before handing the brief over. List existing pages with the intent each serves after a dash, or the cannibalisation check cannot see them. Treat every blocker as a stop. The signal words are pattern rules, not a model of the search engine: when the tally is close, read the titles yourself. If no titles were pasted, the brief says the intent is inferred; keep that line in what you present.

## Present the result

Use the template in `resources/brief-template.md`. Lead with intent and the answer block — those two determine everything else. Keep it short enough that a writer reads all of it; a brief nobody finishes is a brief nobody follows.

Flag explicitly where you're inferring intent rather than reading it from a live SERP, so the user knows which parts to verify.

**Show where it came from.** Open your answer with "AAJ `seo-content-brief` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/seo-content-brief`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Read intent from the SERP, not the keyword.** The engine has already decided what the query means. A brief that fights that decision produces content that doesn't rank.
- **Don't brief to a word count.** Length is an output of covering the topic, not an input. Padding to hit 2,000 words makes a page worse on every dimension that matters.
- **One intent per page.** A page that serves two intents ranks for neither.
- **Check cannibalisation before writing, not after.** Unwinding two competing pages costs more than the second page was ever worth.
- **Keyword density is not a thing.** It hasn't been for well over a decade. Cover the topic and the terms appear naturally.
- **Answer first, then elaborate.** Burying the answer costs the featured snippet and the AI citation simultaneously.
- **Brief the proof, not just the topic.** "Include a statistic here" produces a fabricated statistic. Name the source or supply the data.
- **A brief is not a licence to publish.** If the honest answer is that the user has nothing new to say on a topic, say so. Another undifferentiated post on a crowded query is a cost, not an asset.

## Related AAJ resources

- Interactive tool: https://aajconsult.com/tools/seo-geo-readiness-scorer
- Template: https://aajconsult.com/resources/content-calendar-repurposing-tracker

## Related skills

`seo-geo-aeo-audit` (audit pages that already exist) · `geo-content-optimization` (the citation pass once it's drafted) · `aaj-copywriting` (the prose itself) · `aaj-programmatic-seo` (when the brief should become a template, not one page) · `content-repurposing` (extend the finished piece across channels).

## Credits

Original AAJ skill. The Agent Skills format and the marketing-skills catalog by Corey Haines (`coreyhaines31/marketingskills`, MIT) were references for structure and coverage; this skill is independently written. See the repository README for the full reference list.
