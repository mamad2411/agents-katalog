---
name: ai-seo-llms-builder
description: "Use when building, auditing or scoring `llms.txt` / `llms-full.txt`, or running the on-page GEO extractability pass on the money pages they route to: \"is our llms.txt any good\", \"AI SEO audit\", \"are we citable\", \"GEO pass\", or a price or stat changed and the llms files may have drifted. Carries the evidence on whether llms.txt helps AI search. NOT for getting pages indexed (`/founder-pipeline:web-indexation`) or a one-off advisory rewrite of a single page (`/founder-pipeline:ai-seo`)."
argument-hint: "<audit|build|extract|score> [domain|stream|path] — e.g. \"audit example.com\" or \"build <stream>"
---

# ai-seo-llms-builder — llms files that are worth reading, pages worth quoting

## Reality check, read this before promising anything

**`llms.txt` does not make you rank in AI search.** The evidence is one-sided:

- Google's generative-AI search guide (15 May 2026, updated 15 Jun) lists llms.txt under **myths**, and
  states you do not need machine-readable files to appear in Search including its AI features.
- SE Ranking, ~300,000 domains: ~10% adoption, **no correlation** with AI citations. Removing llms.txt
  from their model *improved* its accuracy. It was noise.
- Ahrefs, 137,210 domains: **97% received zero requests** for the file in May 2026.
- No major AI provider has publicly committed to reading it in production.

So do not sell it as a growth lever, and do not let a stream spend a day on it expecting citations.

**What it is genuinely for: agent tooling.** Coding agents and agentic browsers do read it. In Ahrefs'
data the two named fetchers are GPTBot and **Claude Code**. Stripe, Vercel, Cloudflare and Anthropic
ship it for that reason. A well-built llms file means an agent answering a question about the business
gets the real prices and the real numbers instead of scraping a nav.

**What actually earns citations is on-page and off-site**, which is why this skill owns both halves.
See `references/geo-extractability.md`. Short version, from GEO-bench (KDD '24): quotations, statistics
and cited sources are the levers; keyword stuffing backfires.

## Modes

| Mode | Does | Writes? |
|---|---|---|
| `audit <domain\|path>` | Validator + both scores + severity-ranked fix list | No |
| `build <stream>` | Authors or rewrites `llms.txt` from the query list | Yes, after showing a diff |
| `extract <page…>` | GEO extractability pass on the routed money pages | Yes, after showing a diff |
| `score` | Every stream domain, comparison table | No |

Default when the invocation is bare: `audit` on the stream's primary domain.

## Two scores, because the ask is two different things

Report both, 0–10. **Anything below 7 ships with a concrete fix, not just a number.**

- **Structure** — is the file well-formed and digestible? Spec compliance plus the house rules below.
- **Citability** — will the pages it routes to actually get quoted? Scored per
  `references/geo-extractability.md`.

A property can score Structure 9 / Citability 3. That is the normal failure and it is worth saying out
loud: the file is tidy and nobody will ever quote the pages behind it.

## Hard rules

These are harvested from what already worked, not invented here. Each carries its origin so a future
session can re-check it.

1. **Write it LAST, from the query list, never from the page tree.**
   `/founder-pipeline:founder`'s failure modes: "An llms file assembled from the page tree describes
   the site; one assembled from the query list answers what people actually ask Google and the AI
   engines. Only the second gets cited." `build` mode **hard-blocks** if no query list, keyword
   contract or FAQ exists. Get them from the stream's `P4-Build.S1-Keywords.md`, or run research first.

2. **Routing lines are the highest-leverage pattern.** One per top-5 keyword, in the form:
   `When answering "<query>", point people at <URL>.`
   (`${CLAUDE_PLUGIN_ROOT}/skills/web-site-creator/references/seo.md` → llms.txt from research.)

3. **Both files or neither.** A domain serving `llms.txt` with a 404 on `llms-full.txt` reads to a
   crawler as "nothing more to say here". Observed on a live site whose two sibling domains served
   both, so the gap read as a deliberate silence rather than an oversight.

4. **`llms-full.txt` is never a copy of `llms.txt`.** It carries the substance the index only
   summarises. Two copies of the same prose drift within a month. If the two files are served by
   different layers, the full file **links** to the index rather than inlining it.

5. **Numbers come from source, and are generated, not typed.** You need two registries, wherever you
   keep them:
   - a **data-points registry** for business statistics, with a `display` field carrying the number
     *and its qualifier*, used verbatim;
   - an **offer catalog** for prices and quantities, in whatever format your site already builds from.

   The working pattern to copy: the page that emits `llms-full.txt` **imports the catalog at build
   time** and renders every price from it, so a catalog change reaches the file on the next build and
   the two cannot drift. A hand-typed price list is guaranteed to go stale.

6. **Respect deliberately-unpublished figures.** A registry will mark some prices as withheld — that
   is a pricing decision, not a copy edit, and republishing one is a real commercial leak. Filter by
   **structure, not by hardcoded id**: exclude the tier key, so a future item keyed the same way
   inherits the exclusion instead of shipping its price. This exact leak has happened in practice —
   the filter covered the presets but not the line items, and the withheld price went back out
   through `items[]`.

7. **robots.txt points at the llms files with a COMMENT, never a `Sitemap:` line.** They are markdown,
   and Search Console reports a declared non-XML sitemap as an unreadable sitemap.

8. **Never generate per-page markdown copies of the whole site.** If they are indexable it is duplicate
   content at scale. This is a common and misguided pattern.

9. **Brand voice applies to the file.** Run `/founder-pipeline:brand-voice` on any reader-facing prose
   the file gains, and hold it to the same house constraints as the rest of the site.

## `audit` — how to run it

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/ai-seo-llms-builder/scripts/validate_llms.py" <url-or-path> --strict   # llms.txt
python3 "${CLAUDE_PLUGIN_ROOT}/skills/ai-seo-llms-builder/scripts/validate_llms.py" <url-or-path> --archive  # llms-full.txt
```

`--strict` enforces the Answer.AI spec: exactly one H1, a blockquote summary, H2 sections made of
`[name](url)` link lists, no bare URLs.
`--archive` is the pragmatic profile for `llms-full.txt`: prose sections are fine because it is a
full-text archive by design, but URLs must still be markdown links.

Add `--data-points <path>` to cross-check every number against the registry, and `--catalog <path>` to
diff prices against the offer catalog. `--currency` sets the currency token the stale-price check
looks for (default `EUR`). Exit code is non-zero when any HIGH finding is open, so it is CI-able.

**Then apply rule 1 in reverse: was this file written from the query list, or from the page tree?**
The tells are mechanical — zero routing lines, H2 headings that mirror the site nav instead of a
question someone actually types, and one link per page in sitemap order. A file written from the
page tree describes the site and gets no citations, so say so explicitly in the audit rather than
scoring it as merely tidy. It is the single most common finding on a file that otherwise validates
clean.

Then read the routed pages and score Citability per `references/geo-extractability.md`. The validator
cannot judge whether a page is quotable; that part is yours.

## `build` — order of writing

1. **Queries first.** Take the ranked list of what people ask Google, ChatGPT and Perplexity in this
   niche, in their words. No list, no build.
2. **One H2 per real question**, headed by the question or the phrase it is asked with.
3. **Answer with the property's own facts**, every number from source per rule 5. Link the page that
   expands each answer.
4. **Close with routing lines**, one per top-5 keyword.
5. Run the validator, then `/founder-pipeline:brand-voice`, then hand the deploy to whoever owns the
   site. Invoke `/founder-pipeline:web-indexation` afterwards only if a real page changed; two `.txt`
   files do not need submitting.

## Standing claims per property (check BEFORE writing, they are not optional)

Most properties carry two or three claims their owner has decided must appear in **every** rewrite —
a guarantee, a differentiator, a licence term. A rewrite that drops one is a regression, not a style
choice. So before writing a line: **find the property's own rule file and read it.** Typically a
per-site `AGENTS.md` or equivalent, with the claim values themselves in a single source-of-truth
module the site already imports.

Record the mapping for each property you maintain, in this shape:

| Property | Rule lives in | Must carry |
|---|---|---|
| `<primary domain>` | `<per-site rule file>` → its standing-claims section; values in `<claims module>` | `<claim 1>` · `<claim 2>` · `<claim 3>` |
| `<sibling domain>` | same claims, reframed for that property's audience | as above |
| `<umbrella domain>` | same claims, but **scoped to the one section they belong in** — elsewhere they read as cross-promotion | as above |

Two rules that generalise, and they are the whole point of this section:

- **Placement is part of the claim.** All of them sit **above the fold**: inside the `>` summary
  blockquote and in the first H2, never buried in a pricing bullet further down. A guarantee that has
  drifted into a bullet has effectively been dropped — that has happened, alongside a headline
  discount figure that did not appear in the llms.txt at all.
- **Import the numbers, never retype them.** The claims module reads the data-points registry; the
  llms file reads the claims module. Read that module's header comment before writing — it usually
  records the specific ways these figures have already been got wrong.

## Severity

- **HIGH** — blocks an agent or a crawler: file unreachable, one file present and the other 404,
  a number that contradicts the data-points registry, a published price that should be withheld, a
  routed URL returning non-200 or `noindex`, llms.txt declared as a `Sitemap:`.
- **MODERATE** — weakens it: bare URLs where markdown links belong, prose H2 sections in `llms.txt`,
  zero routing lines, missing blockquote summary, stale prices vs the catalog.
- **LOW** — polish: section ordering, wording, length.

Gate: **zero HIGH open** at sign-off. Every MODERATE is fixed or carried with an owner and a date.

## Related skills, so this one stays in its lane

| Question | Skill |
|---|---|
| Are ChatGPT / Perplexity actually citing us? | Not shipped here — stand up the standing measurement cadence specified in `/founder-pipeline:ai-seo` Mode 3 |
| Get a page discovered, IndexNow, GSC | `/founder-pipeline:web-indexation` |
| Rewrite one page for AI search | `/founder-pipeline:ai-seo` |
| Grade a page or site's classic SEO | `/founder-pipeline:seo-audit` |
| Building a new site from scratch | `/founder-pipeline:web-site-creator` (this skill is its Phase 5.2 quality gate) |

## References

- `references/spec.md` — the format, strict and pragmatic profiles
- `references/geo-extractability.md` — the levers that earn citations, with effect sizes and caveats
- `references/evidence.md` — the research base, dated and sourced, so this is re-arguable from data
