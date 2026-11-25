---
name: web-keyword
description: "Use when the question is which keywords a site should target, in which language, and whether existing titles and H1s target real demand: \"keyword research\", \"are we using the right keywords\", \"keyword contract\", \"search volume\", \"our non-English pages aren't ranking\", \"did we translate the keywords correctly\", or a list of guessed keywords to check. Builds a keyword contract for new pages or audits a live site against one with measured data, and owns the locale decision. NOT technical site health (`/founder-pipeline:seo-audit`) or competitor gap work."
---

# Web Keyword

Keywords get chosen twice: once when someone picks words that sound right, and once when the
market decides which words it actually types. This skill closes the gap between those two, with
measured data, before copy gets written around a guess.

The failure this exists to prevent is specific and expensive: a page titled with the brand's
favourite word instead of the buyer's word. In one measured case, two near-synonyms for the same
professional service — one the brand's preferred word, one the buyer's — differed 88× in monthly
volume, 880 against 10. The two phrases were a single noun apart and read as interchangeable to
everyone who hadn't measured both. The non-English version of the same failure is worse, because a
literal translation *looks* correct while measuring zero.

## Two modes

Read the request and pick one. They share the same core (localization table, SERP gate) but differ
in where they start.

**Mode A — Contract.** Pages don't exist yet, or a new page set is planned. Build the keyword
contract that copy and meta will be written around. This is the classic direction: keywords first,
copy second, never the reverse.

**Mode B — Audit.** The site is live. Score what exists against measured demand: which pages target
terms with real volume, which target phantoms, which demand has no page at all. Read
`references/audit-mode.md` — it owns the no-orphans check, the translation-quality layer, and the
fix-table format.

Most real requests are Mode B wearing Mode A's clothes. "Should we target X?" on a site that
already has dozens of pages is an audit; answer the keyword question, then tell them what their
current pages are actually targeting, because it's usually not what they think.

## The locale decision — declared once, never retrofitted

**Before any measuring, name the territories.** A territory is a market-plus-language pair —
somewhere the business sells, in the language its buyers there search in. The default shape is two:

- **your home market**, in its own language
- **your primary export market**, in the language that market searches in — for most businesses
  that is English, and for many it is English *even inside the home market*, which is a finding
  step 2 exists to catch

Add a third only when there is a real commercial reason for it, and never add one because a
translation was cheap.

This decision is upstream of everything else in the skill and it does not get revisited per page.
Retrofitting a language later is the expensive path: every page already built has a title, an H1,
a URL and a set of internal links chosen against a different keyword set, and the retrofit either
rewrites all of them or leaves a permanently inconsistent site. Two territories chosen deliberately
beat four chosen by drift.

Record the decision — the territories, the language code for each, and the one-line reason — at the
top of the contract, and carry it into the site config so later work doesn't have to re-derive it.
Every downstream step in this skill runs **once per territory**, separately.

## The workflow

### 1. Seed the concept list

Work in **concepts**, not keywords. A concept is a thing the buyer wants ("someone to coach an
engineering manager"). A keyword is one of several ways to type it. Getting this level right is
what makes the rest work — you compare candidates *within* a concept, and you assign *concepts* to
pages.

Seeds come from how the buyer describes the problem, not how the brand describes the offer: their
own words from calls and support threads, the category language competitors use, and any prior
research on disk. Check for prior runs before spending a call — re-measuring a term someone already
priced last month is waste, and the older number is worth having as a comparison anyway.

### 2. Draft candidates per concept — the step that decides everything

For every concept, in every target language, draft **at least two** candidate phrasings before
measuring anything:

- the literal translation (a hypothesis, never the default answer)
- the industry or job-title term locals actually use, which is often not the literal one
- the buyer-language synonym — the word a buyer would use where the brand uses its own
- the kept-English option, where the market borrows the English term wholesale

That last one matters more than people expect. In technical fields many markets type the English
job title even when a perfectly good native word exists, because the English one is what appears on
their contract and their LinkedIn.

Read `references/localization.md` before drafting for any non-English territory. It covers spelling
traps that silently measure the wrong word (in closely related languages a one-letter difference is
a different term in a different market, not a typo), and the rules for territories where everything
measures near zero.

### 3. Measure

You need a keyword-data provider — anything that returns search volume, CPC, difficulty, intent,
trend and live SERP results for a named location and language. `references/dataforseo-recipes.md`
works the whole method through against DataForSEO, which is the recommended default and the source
of every endpoint name in that file. Any provider with equivalent coverage substitutes cleanly:
what the skill depends on is the *capability*, not the vendor. If yours can't do one of the layers
— live SERP, related queries, a non-Google engine — that layer is unmeasured and is reported as
unmeasured, not as zero.

The short version: volume and CPC per candidate, batched; difficulty and intent on survivors only;
Trends for direction; and expansion endpoints to catch phrasings nobody guessed.

Run **rising and top related queries** from Trends for the two or three head terms. This is the
closest thing to hearing the market speak — it surfaces the phrasing people actually use, as
opposed to the phrasing we thought to ask about. Findings here frequently reshape the concept list,
so do it before locking anything.

Every territory is a separate call. Volumes and SERPs differ completely between languages, and a
combined call silently averages two markets into a number describing neither.

### 4. Lock the term, record the losers

Per concept, per territory: the candidate with the best real volume and trend wins.

**Record the losing candidates with their volumes next to the winner.** This is not bookkeeping —
it is the entire evidence trail. It is what lets someone sanity-check the call six months later,
and when a literal translation turns out to be wrong, the rejected-candidates column *is* the
deliverable. "We chose X" persuades nobody; "we chose X at 140/mo over Y at 10/mo" ends the
argument.

When every candidate for a concept measures near zero — common for B2B service terms in smaller
language markets — still lock one, tagged `[low-volume — brand/AI-search play]`. Never leave an
untested literal translation in place by default. A near-zero market is a real finding with real
consequences (it means that language is a brand and AI-search play, not a traffic play), and it
should be stated rather than discovered again next quarter.

### 5. Validate on the live SERP — the gate

Database volume is a snapshot; the live SERP is the truth. For every primary keyword, pull the
actual SERP and record four things:

1. **Intent confirmed?** A keyword you called transactional whose top 10 is all blog guides means
   you misread the intent, and the page you were about to build will lose.
2. **Who ranks** — known competitors, or someone you hadn't considered?
3. **SERP features** — AI Overview, featured snippet, People-also-ask, local pack. These change
   what position one is worth and what content format wins.
4. **Beatable?** A top 10 of DR-80 giants means the keyword is mispriced for this site no matter
   what its difficulty score says.

A primary keyword with no recorded SERP check is an unvalidated guess. It doesn't lock.

### 6. Map keywords to pages — no orphans in either direction

Every page gets at least one primary keyword. Every primary keyword gets a target page. Both
directions matter: a page with no keyword is a page nobody will find, and a keyword with no page is
demand you measured and then abandoned.

Money pages — the offer, pricing, booking, homepage — each need at least one commercial or
transactional primary, or an explicitly recorded exception. A pricing page targeting an
informational query is a common and quiet failure.

### 7. Write the AI-search question set

Search is splitting into keywords typed at engines and questions asked of models. Both need
answering, and they need different phrasings.

Per locked language, write three to five questions the way a buyer would actually ask a model —
full sentences, first person, with the awkwardness real people include. Then check who currently
wins those answers. These questions feed FAQ blocks, llms.txt, and the probe set.

Volume data barely applies here, which cuts both ways: a phrasing with zero Google volume can still
be worth owning if it's how people ask models. That is often the *only* live play in a small
language market, and it's why the low-volume tag exists rather than a kill decision.

**Fan-out queries are the third research artifact here, and they are not PAA.** A *fan-out query* is
a sub-question an engine generates and answers **internally** before synthesising the response it
shows — ask "which CRM for a 5-person agency" and it may resolve "what CRMs exist", "which are
priced for small teams", "which integrate with X" first. PAA is **observed SERP data**: questions
Google actually displays, pulled in step 5. Fan-out is **inferred** — a model of a model, 🟡 at best,
and never recorded as if it were measured. Record them in a separate column, tagged, so a later
session can tell which is which. **Tooling limit: fan-out data is US and English only.** None exists
for most other markets — it did not exist for either Czech or Slovak when this was last checked, and
smaller language markets should be assumed uncovered until proven otherwise. Where it is missing,
derive sub-questions from PAA and from real customer questions, and never pass an English fan-out
list off as research into another market. Definition and downstream use:
`${CLAUDE_PLUGIN_ROOT}/skills/ai-seo/references/aeo-patterns.md` §6 and §9.

### 8. Hand off to standing measurement

A one-off measurement decays into a stale opinion. The terms worth watching become standing probes
on a cadence — AI-citation probes on the question set, rank checks on the locked commercial terms,
Trends on the positioning roots.

Keep the probe set small and stable, or the trend line means nothing. A term earns a permanent probe
row only if it's a locked commercial term with demand and a target page, or a natural-language
buying question. The definitional long tail gets tracked in Search Console instead of probed.

### 9. Persist the locked terms where translation happens

Write the locked terms and their rejected candidates into the project's `TRANSLATION-GLOSSARY.md`
(create it seeded with these rows if absent). Whatever translates pages next — a skill, a
translator, a vendor — reads that file first and treats the locked column as non-negotiable. That
is what stops the next page from being freshly re-translated straight back into the term you just
measured and rejected. Without this step the localization work decays with every page added.

## Output

Localization table first, because it carries the reasoning:

`Concept | EN term [vol, source] | <Territory> term — locked [vol, source] | rejected <Territory> candidates + volumes [source]`

— one locked-term column pair per territory. Then the keyword table:

`Keyword | Language | Volume | Difficulty | Trend (12m/5y) | Intent | SERP check | Target page | Verdict | Source`

Verdict is one of **target** / **AI-only** / **ignore**. Every row gets one. A keyword table without
verdicts pushes the decision back onto the reader, which is the job this skill was asked to do.

Then the AI-search question set per language, the intent-to-page map, and the rankings baseline.

## What makes this trustworthy

- Every number carries `[source: <endpoint>, YYYY-MM-DD]`. A volume figure with no source is a
  guess wearing a number's clothes.
- Raw API responses save to disk so re-runs read from the file instead of re-paying.
- **Unmeasured is never reported as zero.** If an engine or market couldn't be measured, say it
  couldn't be measured. A zero is a finding about the world; an unmeasured layer is a finding about
  the instrument, and conflating them manufactures conclusions that survive for quarters.
- When a term was measured previously, compare and call out any large swing rather than silently
  replacing the old number.
- If the data contradicts the reason the project exists — the head term is declining, the market is
  empty — say so plainly. That contradiction is the most valuable thing a keyword run produces, and
  burying it to keep a plan alive wastes far more than the research cost.

## Before sign-off

Run `/founder-pipeline:critical` on the draft contract, aimed at volume wishful-thinking, intent
mismatches, and any keyword that got picked because it flatters the offer rather than matching how
buyers search. Revise, note what changed, and present the contract with the findings. Don't
auto-advance to writing copy — the whole point of a contract is that someone agreed to it.

## Routing

Ships with this plugin:

- Technical site health, meta hygiene, crawl issues → `/founder-pipeline:seo-audit`
- Optimising a page for citation in AI answers → `/founder-pipeline:ai-seo` (this skill supplies
  its question set)
- Getting pages discovered after they ship → `/founder-pipeline:web-indexation`
- Building the pages the contract describes → `/founder-pipeline:web-site-creator`
- Fetching a competitor or SERP page for inspection → `/founder-pipeline:firecrawl-scrape`

Not shipped — do these inline rather than routing to a skill that won't be installed:

- **Competitor rankings and keyword gap.** Run ranked-keywords on your domain and on each named
  competitor, intersect the two, and report the terms they rank for and you don't, sized by volume.
  The recipes are in `references/dataforseo-recipes.md` under *Rankings and gap*. Keep it to the
  gap question — a full competitive teardown is a different job.
- **Ongoing AI-visibility measurement.** Step 8 hands off a probe set. If you have no standing
  measurement loop, the minimum viable version is: the locked commercial terms and the
  natural-language question set, re-run on a fixed cadence against the same engines, results
  appended to a dated file so the trend line is real. Changing the probe set breaks the trend, so
  freeze it.
- **Translating pages.** Whatever does the translating reads `TRANSLATION-GLOSSARY.md` first and
  treats the locked terms as fixed. A translation that is idiomatic and targets a rejected term is
  a regression, not a style choice.

Note that discovery and ranking are different problems. If pages are unindexed, keyword choice
explains nothing about their absence — check indexation first, or you'll rewrite titles to fix a
problem that was never about titles.
