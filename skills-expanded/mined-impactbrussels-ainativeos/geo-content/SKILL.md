---
name: geo-content
description: Use when a founder asks why the AI engines never name them, when traffic holds but the buyer "already decided" before the call, when they say "we rank but ChatGPT cites a competitor", "how do I show up in Perplexity", "write the pillar page", "our content reads like everyone else's", or they are about to publish a vendor page nobody will quote. Produces a GEO content brief plus one piece structured to be lifted verbatim: standalone claim, named mechanism, quotable definition, data with provenance. Run after measure-ai-native-pmf baselines your Share of Model; feeds share-of-model-audit.
stage: grow
function: growth
license: CC-BY-4.0
attribution: AI-Native OS by Adam M. Adamek (Impact Brussels ASBL)
---

# GEO Content

The buyer reads four confident sentences in an AI engine before they ever reach your site, and those sentences name three companies as proof. Ranking puts a blue link on a page nobody scrolls anymore. It does not put your name in the paragraph the buyer actually read. The engine quotes rather than ranks, and quoting rewards different content: a claim that stands on its own, a number with a source, depth a keyword-stuffer cannot fake. Your job is not to climb a list. It is to become the source the machine reaches for.

## The method

Structure for extraction, then hit the citation factors. Full framework: [`references/geo-method.md`](references/geo-method.md), drawn from handbook [Chapter 10](../../handbook/10-narrative-positioning-geo.md).

### Step 1: Write the one-sentence extractable answer

Take your category's top buyer query, the exact question a high-intent buyer types into an engine. Write the one or two sentences you want quoted back, standing completely alone, naming you or your category claim. That sentence is the GEO north star; every page opens with a version of it.

### Step 2: Lead every section with its answer

A model scans for the chunk that answers and grabs the chunk that stands alone. Bury the claim in paragraph six and the engine reads past it. Pick the format that fits the query.

| Query shape | Format | Opening move |
| --- | --- | --- |
| "what is X" | Definitional | One-sentence standalone definition, then mechanism |
| "X vs Y" / "X alternatives" | Comparative | Named criteria table, verdict first |
| "how much / how long / how many" | Data-led | The number with its source in the same breath |
| "how do I [job]" | FAQ / steps | Direct answer, then the numbered method |

### Step 3: Hit the citation factors

An engine managing its own risk gravitates to sources it can defend. Score the draft against the checklist before publishing.

| Factor | Pass test |
| --- | --- |
| Clarity | Each section opens with a liftable, self-contained sentence |
| Structure | Headings match real buyer queries; answer before depth |
| Specificity | Exact numbers and named mechanisms, never "significant" |
| Authority | Every statistic carries its source; every claim a named expert |
| Freshness | Dated, with the most recent verified figure |

### Step 4: Close the gap under the claim

The extractable claim and the proof behind it have to be the same length. Write the bold, citable sentence, then make sure the dossier under it would survive the body that polices your sector. Never publish a number you cannot source; the engine repeats your overclaim to every buyer after the one you disappointed.

## Output

- A **GEO content brief**: the north-star sentence, the target buyer queries, the chosen format per query, the citation-factor checklist.
- **One piece** rewritten to be cited: standalone claim, named mechanism, quotable definition, data with provenance.
- Next: run `share-of-model-audit` to measure whether the engines start naming you.

## Constraints

- Name the failure mode: hype with no claim. A page of adjectives and no liftable sentence gets read past, not quoted. Forbid it.
- A demo is not evidence and an unsourced number is a liability. Apply the research-before-asserting principle: any figure that fails a web check does not ship.
- Stay theme-agnostic; the founder supplies the domain, you supply the rigour. Never invent a metric or a company.

## Dictionary

[GEO (Generative Engine Optimization)](../../dictionary/07-ai-native-business.md#geo-generative-engine-optimization) ·
[extractability](../../dictionary/07-ai-native-business.md#extractability) ·
[Share of Model](../../dictionary/07-ai-native-business.md#share-of-model)

## Copy-paste version

> For non-coders: paste into any chatbot (Claude.ai, ChatGPT, Perplexity). Tag: `chat`.

```
Act as my GEO content strategist. The goal: be cited inside AI-engine answers, not just ranked.
Product: [ONE_LINER]. For: [ICP]. Domain: [DOMAIN]. Top competitors: [2-4 NAMES].

1. Write the single highest-intent buyer query my [ICP] types into an AI engine, and the one
   standalone sentence I want quoted back, naming me or my category claim. That is my north star.
2. List 8 to 12 real buyer queries (category, comparison, problem-led). For each, tell me the
   format that wins it: definitional, comparative table, data-led, or FAQ.
3. Take ONE query and write the section to be lifted verbatim: open with a complete standalone
   answer, name the mechanism, give a quotable definition, attach a named source to every number.
4. Score my draft on five citation factors: clarity, structure, specificity, authority (sourced
   stats + named experts), freshness. Flag every section that cannot surrender a standalone sentence.
5. For my boldest claim, name the proof behind it and the proof I still owe. If I cannot source a
   number, tell me to cut it.

CONSTRAINTS: no hype without a liftable claim; no unsourced numbers; do not invent figures or
companies. OUTPUT: a GEO content brief plus one cited-ready piece, then ONE next action.
```
