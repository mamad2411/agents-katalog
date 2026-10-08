---
name: researching-telco-standards
description: Researches telecom standards questions against the 3GPP, O-RAN, GSMA and CAMARA corpora using the telco MCP search tools. Use when a question involves 3GPP specs (TS/TR numbers, 5G NR, LTE, 5GC, RRC, MAC, PHY), O-RAN Alliance specifications, GSMA documents (eSIM, SGP.xx, Open Gateway, NESAS), CAMARA network APIs, or when the user asks what a standard says, requires spec citations, or is writing research or deployment guidance that must be grounded in published specifications.
---

# Researching telco standards

Single-shot semantic search over these corpora drifts on telecom vocabulary.
Measured: 2 of 4 naive queries on a real research question returned
plausible-but-wrong results. This skill is the query discipline that fixes it.

**Answer confidently when the corpus supports it.** These corpora are good.
Most questions get a solid, citable answer. Hedging on a well-covered topic is
as much a failure as inventing one on a thin topic.

## What the 3GPP corpus is

`telco:search_in_3gpp` searches a **wiki built from 3GPP specs**, not the spec
PDFs. Chunks carry a `source_spec` pointer (e.g. `38321`) and mix three kinds
of content:

| `callout_kind` | What it is | Quotable? |
|---|---|---|
| `normative` | Extracted clause text, carrying its own `**Source:** TS ... §...` line | Yes, with that attribution |
| `table`, `config` | Reproduced tables and parameter values | Yes, as the corpus's reproduction |
| everything else | Summaries and paraphrase written for the wiki | No — treat as a pointer, not text |

So: **quote `normative` and `table` chunks and pass their attribution through.
Never quote a summary chunk as clause wording.** When it matters — a
conformance claim, a `shall`, a research citation — say the text came via the
wiki and should be checked against the published document.

Long tables come back **truncated**. Never present a truncated table as
complete. Two rules:

- **Recover what you can.** Continuation chunks carry no table header — only
  rows — so requerying the table *title* returns the same truncated head.
  Query the distinctive row *values* you expect past the cut, **combined with
  the table's context terms** (e.g. row names + `eLCID DL-SCH`): values alone
  often miss too. A continuation chunk is recognisable by opening mid-row.
  Expect several attempts before concluding failure; these recovery queries
  do not count against the Step 3 budget.
- **Name the gap and stop.** For rows that still did not come back, do not
  describe, hint at, or characterise what they contain — not even hedged as
  "in the published spec these carry...". A truncated table is a hole you
  report, not a hole you narrate. If you can name the missing content, you
  are answering from memory, which this skill forbids.

O-RAN, GSMA and CAMARA chunks come from the published documents directly.

## Workflow

```
Research Progress:
- [ ] Step 1: Anchor the question to spec numbers and corpora
- [ ] Step 2: Check the disambiguation list for trap terms
- [ ] Step 3: Run the query budget
- [ ] Step 4: Filter results on metadata, discard off-target hits
- [ ] Step 5: Report with citations, and name real gaps
```

### Step 1: Anchor to spec numbers and corpora

Decompose the question into *which specification family would contain the
answer*. Route with `reference/corpus-map.md`.

A question rarely maps to one spec. "MAC layer impact of DSS at the RU level"
is rate matching (38.214), control resources (38.213), MAC procedures
(38.321), RRC configuration (38.331), and O-RAN 7.2x split behaviour.

**If a deployment term is not a spec feature name, decompose it.** DSS, MRSS,
massive MIMO and RAN slicing are umbrella names for *sets* of specified
features. Searching the umbrella returns noise; search the constituents.

### Step 2: Check for trap terms

Read `reference/disambiguation.md` before querying. Telecom terms collapse two
senses under one embedding, and the wrong sense retrieves *confidently*. The
confirmed traps include "sharing", "scheduling restriction", and the LTE/NR
dialect split on MAC vocabulary.

Defeat them by naming the mechanism rather than the concept.

### Step 3: Run the query budget

**Minimum 3 queries. Stop at 8 for the topic search, or earlier when two
consecutive queries return nothing new.** Truncated-table recovery queries are
exempt — continuation chunks are cheap to find and expensive to miss. Vary
phrasing deliberately:

1. **Mechanism terms** — RRC/IE/parameter names (`lte-CRS-ToMatchAround`)
2. **Spec-anchored** — the spec number plus the clause topic
3. **Native vocabulary** — the exact wording that generation uses (see the
   LTE/NR dialect trap; "MAC subheader" is NR, "MAC PDU subheader" is LTE)
4. **Procedural** — how the feature behaves at run time
5. **Adjacent** — the neighbouring feature that constrains it

Priority when short on budget: mechanism terms first, native vocabulary
second. Those two find the most.

**Scope, corrected:** `narrow` returns **2** chunks; `focused` and `broad`
both return **5**. Because they tie, widen coverage by varying the query text,
not the scope value.

**Never use `narrow` for a coverage or absence question.** Two chunks is not
evidence about what a corpus contains. Use `focused` or `broad` by default and
reserve `narrow` for confirming a single fact you have already located.

**Watch for single-document clustering.** If every result shares one `slug`,
the search found one page, not a topic. Requery before concluding.

### Step 4: Filter on metadata

Results cannot be filtered inside the query, but every chunk returns metadata
you must read and act on:

| Field | Corpus | Use it to |
|---|---|---|
| `source_spec` | 3GPP | Confirm the hit is from the spec family you wanted |
| `releases` / `release_latest` | 3GPP | Check the release matches the question |
| `normative_levels`, `has_shall` | 3GPP | Separate requirements from description |
| `aliases` | 3GPP | Harvest better search terms for the next query |
| `callout_kind` | 3GPP | Decide whether a chunk is quotable (see above) |
| `wg`, `doc_type`, `version` | O-RAN | Identify working group and TS vs TR |
| `similarity` | all | See the two rules below |

Two different similarity failures, and the dangerous one is not the low-score
case:

- **Low similarity, off-target `source_spec`** — ordinary weak retrieval.
  Discard.
- **High similarity, off-target `source_spec`** — this is what the
  disambiguation traps produce. Topically coherent, confidently retrieved,
  answering a different question. Judge by whether `source_spec` matches the
  spec family Step 1 predicted, **never by the score alone.**

**Discard off-target hits explicitly rather than summarising them.**

**CAMARA sibling documents duplicate schemas.** Component schemas (`Port`,
`Rate`, `Duration`), field descriptions and generic error blocks are copied
verbatim across the APIs in one repo family. Finding a definition in one
sibling does not mean it is absent from another. Before attributing shared
text to a specific document, requery naming that document's own wrapper schema
(e.g. `BaseSessionInfo`) to confirm which one you are actually quoting.

`aliases` is the highest-value field: it is the corpus telling you its own
vocabulary. Feed those terms back into Step 3.

### The absence rule

Vector search never reports "absent" — it always returns its nearest chunks.
So absence is a conclusion you must earn:

**Do not claim the corpus lacks something unless you have run at least 3
queries at `focused` or `broad`, including one in that generation's native
vocabulary, and none returned a chunk with a matching `source_spec`.**

Even then the finding is *"not retrieved"*, not *"not specified"*. Three
statements, in increasing order of strength — say the weakest one that is true:

- "**I** did not retrieve X" — a statement about your search, not the corpus.
  Use this whenever you stopped before exhausting the Step 3 phrasings.
- "The corpus did not return X" — a retrieval outcome, earned only after the
  full absence-rule bar above (and, for table rows, a contents-phrased
  recovery query).
- "The specification does not define X" — a claim about the standard, and only
  assertable when the corpus positively shows it (e.g. the spec states
  something is implementation-dependent).

Collapsing these two is how a retrieval gap turns into a false claim about the
standard. It has happened in this skill's own history — an earlier version
asserted TS 38.321 was missing from the corpus on the strength of two
LTE-dialect queries. It is not missing.

### Step 5: Report

State how many queries you ran. It is the only auditable evidence of coverage.

Cite so the reader can tell what is verified from what is pointed at:

- Text from a `normative` or `table` chunk:
  `TS 38.321 §6.2.1 Table 6.2.1-1 (Rel-19, quoted via wiki)`
- A clause number the wiki cross-references but whose text you did not
  retrieve: `TS 38.214 §5.1.4.2 (clause referenced from TS 38.331 §6.3.2; text
  not retrieved)`

Never emit a bare `§` you did not see in a returned chunk.

Separate: what the corpus **directly supports**, what is **inference** across
chunks, and what is a **real gap** under the absence rule above.

## Tools

Fully qualified names, all read-only:

- `telco:search_in_3gpp` — 3GPP wiki (5G NR, LTE, 5GC, EPC, IMS, RRC/MAC/PHY)
- `telco:search_in_oran` — O-RAN Alliance TS/TR (RIC, 7.2x fronthaul, O-RU/O-DU)
- `telco:search_in_gsma` — GSMA documents (eSIM/RSP, IPX, RCS, Open Gateway)
- `telco:search_in_camara` — CAMARA network API definitions
- `telco:catalog_list` / `catalog_read` — open-source telecom software

Vector search tools appear only when their corpus is downloaded and
`OPENROUTER_API_KEY` is set. The catalog tools always work.

**If a tool you need is missing, say so and stop.** Do not substitute a
different corpus, and do not fall back on your own knowledge of the specs —
answering an ungrounded question from memory is the failure this skill exists
to prevent.

## Reference

- `reference/corpus-map.md` — which corpus and spec series holds what
- `reference/disambiguation.md` — terms that collide, and the queries that work
