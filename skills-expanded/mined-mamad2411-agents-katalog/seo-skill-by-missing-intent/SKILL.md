---
name: seo-skill-by-missing-intent
description: >
  SEO analysis grounded in primary sources rather than industry folklore. Use for any
  question about how Google ranks, why a page does or does not rank, what the 2024
  Google API leak actually says, or which patent describes a mechanism. Also use for
  concrete site decisions: update or delete old content, prune thin pages, structure
  internal links, choose subfolder or subdomain, plan a migration, diagnose a ranking
  drop, handle UGC or product pages or local or YMYL content, judge whether AI content
  is risky, evaluate an agency, vet a site before buying it, or set an author, date, or
  anchor text policy. Triggers on "audit this page", "why did my rankings drop",
  "should I delete this post", "does X matter for SEO", "what does the leak say about
  X", "explain NavBoost", "is this agency any good", and similar. Bundles the Content
  Warehouse leak (14,022 attributes) cross-referenced against 5,456 Google search
  patents, as a 12-stage pipeline with 26 decision playbooks.
license: All rights reserved
metadata:
  version: 2.0.0
  source: Missing Intent (https://missingintent.com)
---

# SEO Skill by Missing Intent

Two primary sources, joined. The 2024 Google Content Warehouse API leak tells you **what
Google stores**. 5,456 Google search patents tell you **how the stored value is computed
and used**. Neither half is enough alone. Together they are evidence you can cite.

Every answer this skill produces should be checkable by the person reading it.

---

## Start here: routing

Do not dump reference material. Work out what the person actually needs first.

### Step 0: is this a lookup or a decision?

**Lookup** ("what does the leak say about X", "which patent covers Y", "explain
NavBoost"). Run the tools, answer, stop. Do not run the router and do not open reference
files unless the answer needs the narrative.

```bash
python3 scripts/explain.py siteAuthority        # the one-shot answer: field plus patents
python3 scripts/search_signals.py click --tier core
python3 scripts/search_patents.py "dwell time" --claims
```

**Decision or vague ask** ("help with my site", "why did traffic drop", "should I
delete these posts", "is this agency good"). Continue to step 1.

### Step 1: ask two questions

Use AskUserQuestion if available, otherwise ask in plain text. Two questions, not five.

**Question A. What are you trying to do?**

- Fix something that broke or dropped
- Decide something (what to publish, what to cut, how to structure it)
- Evaluate someone else's work or a site you might buy
- Understand how something works
- Improve a specific page or set of pages

**Question B. Depends on A.** Ask only the one that changes the route.

| If A was | Ask B |
|---|---|
| Fix something | When did it start, is it site-wide or one section, and what shipped in the two weeks before? |
| Decide something | Which decision: content, site structure, or a content type like ecommerce, local, UGC, YMYL? |
| Evaluate | Evaluating an agency's work, a recovery offer, or a site you might buy? |
| Understand | Which part: the pipeline overall, one subsystem, or one field? |
| Improve a page | Not indexed, no impressions, impressions but no clicks, or ranked then slipped? |

### Step 2: route to exactly one playbook or workflow

Open one file. Not the whole directory. The playbooks are short and self-contained, and
each one names the exact commands to run.

### Step 3: surface what they did not know to ask

This step is what makes the skill useful rather than merely available. After answering,
name **two or three** adjacent decisions from the index below that apply to their
situation, in one line each. Do not list all 26. Do not pad.

Example: someone asking about deleting old posts almost always also needs the dates
policy and the internal linking question. Someone asking about a ranking drop after a
redesign needs the CMS extraction check.

---

## Decision index

Twenty-six decisions with a real answer in these sources. Route to one.

**Content**

| Decision | Playbook |
|---|---|
| Update, rewrite, or delete an old page | `playbooks/update-or-delete.md` |
| Is AI-assisted content a risk here | `playbooks/ai-content-risk.md` |
| Publish pages at scale, or not | `playbooks/programmatic-pages.md` |
| Show dates on pages, or hide them | `playbooks/dates-on-pages.md` |
| Author and byline policy | `playbooks/author-strategy.md` |
| How often to publish | `playbooks/publishing-cadence.md` |

**Site structure**

| Decision | Playbook |
|---|---|
| What to prune from an existing site | `playbooks/content-pruning.md` |
| How to structure internal links | `playbooks/internal-linking.md` |
| Anchor text policy, internal and external | `playbooks/anchor-text-policy.md` |
| Subfolder or subdomain | `playbooks/subfolder-vs-subdomain.md` |
| How to migrate without losing what you have | `playbooks/site-migration.md` |
| What broke after the redesign | `playbooks/redesign-recovery.md` |
| Which CMS, theme, or framework | `playbooks/cms-and-theme.md` |

**Content types**

| Decision | Playbook |
|---|---|
| Product and review pages | `playbooks/ecommerce-product-pages.md` |
| Local business sites | `playbooks/local-business.md` |
| Health, money, legal, safety content | `playbooks/ymyl-sites.md` |
| Comments, forums, user content | `playbooks/ugc-and-comments.md` |
| Multiple countries and languages | `playbooks/international-and-locale.md` |
| Original images and video, worth it or not | `playbooks/images-and-video.md` |
| Chase featured snippets, or not | `playbooks/featured-snippets.md` |

**Diagnosis and commercial**

| Decision | Playbook |
|---|---|
| Rankings dropped, what now | `playbooks/ranking-drop-triage.md` |
| Is this site worth buying | `playbooks/vet-a-site-to-buy.md` |
| Is this agency doing real work | `playbooks/evaluate-agency-work.md` |
| Is this penalty recovery offer real | `playbooks/penalty-recovery-claims.md` |
| Justify the budget or timeline | `playbooks/justify-budget.md` |
| Get someone up to speed fast | `playbooks/train-a-junior.md` |

**Worked example.** `examples/worked-example.md` shows the whole method end to end: routing, the
projection trace, the demotions checked and cleared, and what was left undetermined. Read it once to
calibrate what a good answer looks like.

**Deep workflows** for work that takes longer than one answer.

| Task | File |
|---|---|
| Full page or site audit | `workflows/page-audit.md` |
| Find the signals a page produces nothing for | `workflows/signal-gap-analysis.md` |
| Build a content brief from the mechanisms | `workflows/content-brief.md` |
| Write a piece that survives fact checking | `workflows/research-writeup.md` |

---

## The evidence rule

Follow this in every answer. It is the whole point of the skill.

1. **Never assert a ranking behavior without a source.** Cite the leak attribute
   (`Module.attributeName`), the patent number, or both. With neither, say you are
   reasoning by analogy and label it.
2. **An undocumented attribute proves existence, not function.** 4,547 of the 14,022
   attributes ship with no description. You may say the field exists. You may not say
   what it does. `--described` filters these out, and the tools mark them explicitly.
3. **No weights leaked.** Nothing says how much any signal counts. Any impact percentage
   is invented. Never produce one, and flag it when someone else does.
4. **A patent proves Google described a method, not that it ships.** Check the filing
   date, which every tool prints.
5. **Say when you do not know.** Naming what you ruled out and what you could not
   determine is a deliverable, not a failure.

---

## Signal Projection

The reasoning method, not a section to skip.

Every stored signal is a lossy, compressed projection of an upstream computation.

    stored signal = quantize( upstream quality model( real behavior ) )

`siteAuthority` is an integer in a serving bundle, not authority. `contentEffort` is a
score, not effort. `goodClicks` is a float, not satisfaction. You cannot write to a
projection. You can only change the behavior upstream of it.

So every recommendation gets traced through three columns before it ships:

| Stored signal | Upstream computation (from the patents) | Behavior to produce |
|---|---|---|

If you cannot fill the third column, you have a metric, not a recommendation. Do not
ship it. Full treatment in `references/signal-projection.md`.

---

## Tools

Three scripts, no dependencies beyond Python 3. Run them before answering from memory,
because memory is where SEO folklore lives.

```bash
# One-shot: a field or patent explained with both evidence layers
python3 scripts/explain.py goodClicks
python3 scripts/explain.py US8661029B1
python3 scripts/explain.py QualityNsrNsrData

# The leak
python3 scripts/search_signals.py siteauthority
python3 scripts/search_signals.py --tier core --limit 60
python3 scripts/search_signals.py click --tier signals --described
python3 scripts/search_signals.py --stage 5
python3 scripts/search_signals.py --stages
python3 scripts/search_signals.py --tiers

# The patents
python3 scripts/search_patents.py "dwell time" --claims
python3 scripts/search_patents.py --mechanism click_engagement --limit 20
python3 scripts/search_patents.py --key
python3 scripts/search_patents.py "site quality" --after 2015
```

Matching is whole-word by default and field names are split on camelCase, so `author`
matches `authorObfuscatedGaiaStr` and not `siteAuthority`. Use `--loose` for substrings.

Tiers come from a classification pass over all 9,475 documented attributes: `core` is
used directly in scoring (58 of them), `supporting` feeds a core signal (790),
`contextual` is search-related but not ranking (1,047), `not_a_signal` is infrastructure
(7,580). **848 core plus supporting is the defensible signal count.** Use that number, not
the inflated ones circulating elsewhere, and cite `data/classification_report.md` for how
it was produced and where an independent second pass disagreed.

---

## The 12 stages

Load the file for the stage the question is about, not all of them.

| Stage | File | What it decides |
|---|---|---|
| Overview | `references/00-architecture.md` | How the stages connect, pre-query versus query-time |
| 1 Crawling | `references/01-crawling-discovery.md` | Whether you get fetched, and how often |
| 2 Processing | `references/02-document-processing.md` | What Google extracts from your HTML |
| 3 Content quality | `references/03-content-quality.md` | NSR, Panda, contentEffort, site-level scoring |
| 4 Links | `references/04-links-authority.md` | PageRank, anchors, Penguin, devaluation |
| 5 NavBoost | `references/05-navboost-clicks.md` | goodClicks, badClicks, lastLongestClicks, CRAPS |
| 6 Entities | `references/06-entities-knowledge-graph.md` | Entity resolution, topicality, author identity |
| 7 Freshness | `references/07-freshness-temporal.md` | Dates, decay, what counts as a real update |
| 8 Spam and trust | `references/08-spam-trust.md` | SpamBrain, demotions, penalties, scamness |
| 9 Query intent | `references/09-query-intent.md` | Intent classification, rewriting, salient terms |
| 10 Snippets | `references/10-snippets-answers.md` | Passage selection, featured snippets |
| 11 Re-ranking | `references/11-reranking-twiddlers.md` | Boosts and demotions applied after scoring |
| 12 Personalization | `references/12-personalization-local.md` | Location, history, device context |

Stage files are long, 40KB to 120KB each. When you need one specific mechanism from one, grep it
rather than reading the whole file:
`grep -n -A 12 "onsiteProminence" references/04-links-authority.md`

Two more references sit alongside the stages:

| File | Use |
|---|---|
| `references/signal-projection.md` | The reasoning method. Read once, apply always |
| `references/signal-catalog.md` | Every core and supporting signal in one readable file. Use this when scripts cannot run in the current environment |

---

## What this cannot tell you

Say these out loud when they apply. The caveats are what make the rest credible.

- **No weights.** Nothing in the leak says how much any signal counts.
- **No confirmation of deployment.** The leak documents an internal API surface. Fields
  may be experimental, deprecated, or dark-launched. Some say so in their own text.
- **It is a 2024 snapshot.** Google has shipped changes since.
- **Patents describe methods, not products.** Google patents far more than it deploys.
- **Claim summaries are paraphrases.** The 77,663 claims were extracted from patent full
  text by a model. Patent numbers, titles, inventors and dates are exact. Before
  publishing a direct quote, pull the original from Google Patents.
- **No site data.** No crawler, no backlink index, no traffic, no SERP data. This skill
  explains mechanisms. It does not measure a site.
- **The map pack is out of scope.** Local pack ranking runs on a different pipeline.

---

## Data

| File | Contents |
|---|---|
| `data/leak_attributes.jsonl` | All 14,022 attributes: module, name, type, Google's description, pipeline stage, classified tier and plain meaning |
| `data/patents.jsonl.gz` | 5,456 patents: dates, inventor, core concept, extracted claims, connected leak modules |
| `data/key_patents.csv` | 27 curated patents with theme, note, and the action each implies |
| `data/pipeline_map.json` | 12 stages and 20 topics mapped to modules and patents |
| `data/classification_report.md` | How the tiers were produced, the counts, and the measured agreement rate |

`gunzip -k data/patents.jsonl.gz` if you want to grep the patent corpus raw.

Built by Missing Intent. Sources: the May 2024 Google Content Warehouse API leak and
5,451 Google search patents from Google Patents. Cross-referencing, claim extraction, the
12-stage pipeline, the attribute classification, and the Signal Projection framework are
original work. All rights reserved.
