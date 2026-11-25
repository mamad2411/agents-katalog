---
name: empirical-research
description: "Appraise whether an empirical claim actually holds, against primary sources, with a mandatory refutation pass and tiered sources. Use for \"does X actually work\", benchmark and vendor claims. Not for API docs (find-docs)."
---

# Empirical Research

Fires when **there is something here that could be false**. Documentation describes what a system does and there is no fact of the matter to be mistaken about. An empirical claim asserts the world behaves a certain way, so it can be wrong, overstated, contested, measured under conditions that are not the user's, or funded by whoever benefits.

## Tier

**Light** (default): steps 1-6.
**Deep** (the answer moves money, health, a public claim, or an irreversible decision): steps 1-6 plus every **Deep** addition marked below.

The refutation pass is mandatory in **both** tiers. It is one query and it is the highest-yield step here. A run that skips it is web search wearing a lab coat.

## Protocol

**1. Decompose.** Split the question into atomic claims that could individually be false. Not "should I take creatine" but "creatine increases strength in trained adults", "creatine causes kidney harm", "loading phases outperform steady dosing". Vague questions cannot be refuted, so they cannot be researched.

**2. Retrieve primary sources.** See [Retrieval](#retrieval). Web search **orients only**. It never sources a claim. Pull the actual abstract before asserting what a paper found.

**3. Tier every source** before leaning on it. See [Source tiers](#source-tiers).

**4. Refutation pass (mandatory).** Run at least one query built to *break* your current conclusion, not support it. If you believe X works, search for X failing, X null results, X criticism, X overstated. Record what you ran and what came back, including "nothing found."
> **Deep:** traverse the citation graph of your top source. Who cited it, and did they challenge it? This mechanically surfaces post-publication challenges, superseding work, and non-English literature that keyword search misses.

**5. Parameter transfer.** Write out the study's population, dose, duration and conditions, *then* compare to the user's. **The study's parameters are almost never the user's.** A study dosed 5 g and the user takes 3. A benchmark ran at 100 QPS and the user runs 10. A return series assumes 30 years and the user has 12. Trained subjects, untrained user.
Where the primary parameters allow it, **recompute at the user's numbers and show the working**. Where they do not, say the number may not transfer. Faithfully citing a figure measured under conditions that are not the user's is a correct-looking wrong answer, and it is more dangerous than an obvious error because every citation checks out.
> **Deep:** flag funding source and author affiliation per source. Vendor-funded trials of the vendor's own product are admissible but must be labelled.

**6. Report.** Claims table first, prose synthesis after. See [Output](#output).

> **Deep also:** search the user's other working languages when local practice, regulation or availability matters (Norwegian sources for Norwegian healthcare, consumer rights, or product availability). Check whether the top source has been superseded or retracted.

## Source tiers

**Name what ground truth is for this domain before tiering anything**, then rank by proximity to it. There is no universal hierarchy.

| Domain | T1, ground truth | Descending | Bottom |
|---|---|---|---|
| Medicine, nutrition, psychology | Systematic review or meta-analysis of RCTs | Single RCT → cohort → questionnaire → mechanism | Vendor material |
| Classical physics, algorithms, numerics | Derivation from conserved quantities, or a proof | Simulation → measurement → practitioner report | Vendor material |
| Software performance | Reproducible benchmark on the user's own config | Third-party benchmark → vendor benchmark → anecdote | Marketing |
| Engineering and design practice | Postmortem with data, or a talk by the implementer | Practitioner consensus → single dev report | Marketing |

Two invariants:

**Bottom tier may never support an efficacy claim.** It is admissible only for uncontested specification facts (a material's refractive index, a published API limit, a stated dimension). Naming the tier in the output is what stops a marketing blog hiding behind confident phrasing.

**Mechanism is not automatically weak.** In biomedicine a mechanism is a hypothesis awaiting outcome evidence. In classical mechanics a derivation *is* the ground truth and playtesting is the noisy proxy. Importing the biomedical ranking into a derivable domain misranks every claim, putting the strongest evidence at the bottom.

## Verdicts

Use exactly these. Split a claim into two rows rather than straddling two verdicts.

| Verdict | Means |
|---|---|
| **Demonstrated** | Outcome evidence, decent tier, at parameters near the user's |
| **Refuted** | Outcome evidence against |
| **Mechanism-plausible, outcome-untested** | The physics or biology checks out; nobody has shown it changes what the user cares about |
| **Contested** | Real evidence both directions; state which is higher tier |
| **No evidence found** | Searched and found nothing. Not the same as refuted |

**Never upgrade a verdict because the mechanism is satisfying.** A clean causal story is a reason to go looking for outcome evidence, not a substitute for finding it. Most product marketing lives in *mechanism-plausible, outcome-untested*, and collapsing that into *demonstrated* is this skill's central failure mode.

## Output

Mandatory table, then prose. The columns exist so that a skipped step leaves a visible hole.

| Claim | Verdict | Best source (tier) | Refutation attempt | Confidence + why |
|---|---|---|---|---|

- **Verdict** is stated at the user's parameters, never the study's. "Supported, but small at the user's dose" beats "Supported".
- **Refutation attempt** records the query run and the result, including "nothing found".
- **Confidence** states its reasoning, never a bare word. "High: T1 meta-analysis, effect direction consistent across 17 trials" or "Low: single T3 questionnaire, vendor-funded, parameters far from the user's".

Fabricating these cells is a bigger lie than vague prose, and each is checkable with one command.

**Destination:** report inline. Offer to persist afterwards. When already working in a notes vault or a repo with a research convention, follow that convention rather than dumping a raw report, and let the offer default toward yes.

## Retrieval

`curl` and `jq` only. Keys are **optional and free**; use one when the env var is set, carry on without it when not. Prefer these over web search for anything with a DOI.

```bash
# Abstract, open-access status, retraction flag, citation count
curl -s "https://api.openalex.org/works/doi:$DOI${OPENALEX_API_KEY:+&api_key=$OPENALEX_API_KEY}" \
  | jq '{title,oa:.open_access.oa_url,retracted:.is_retracted,cited:.cited_by_count}'

# Full abstract (works when the publisher blocks direct fetch)
curl -s "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:%22$DOI%22&format=json&resultType=core" \
  | jq -r '.resultList.result[0].abstractText'

# Known title → use filter=title.search. Plain search= fuzzy-matches the whole corpus and returns noise
curl -s "https://api.openalex.org/works?filter=title.search:$TITLE&per-page=5" \
  | jq -r '.results[] | "\(.publication_year) [\(.cited_by_count)] \(.title)"'

# Who cited this, i.e. who challenged it  (step 4, Deep)
curl -s "https://api.semanticscholar.org/graph/v1/paper/DOI:$DOI/citations?fields=title,year,venue&limit=20" \
  | jq -r '.data[] | "\(.citingPaper.year)  \(.citingPaper.title)"'
```

**Quotas, verified not assumed.** OpenAlex serves unauthenticated at $0.10/day, roughly 1000 calls; a free key gives 10×. Live budget is in the response headers (`x-ratelimit-remaining`, `x-ratelimit-remaining-usd`), so check there rather than guessing. Semantic Scholar's anonymous pool is shared across all users and **throttles unpredictably: a 429 is transient, not a block.** Back off and retry once before routing around it; a free key trades burst for a guaranteed 1 RPS.

**Fallback chain, in order:** the APIs above → `WebSearch` (orientation only) → `WebFetch` → the **playwriter** skill for anything returning 403 or sitting behind Cloudflare.

**A paywall never ends the attempt.** Walk the chain. If full text stays unreachable, use the abstract and say the full text was not read, rather than quietly citing a paper you only saw summarised.

### Domains with no literature

Many questions have no papers at all. Game feel, engineering practice, tooling, product behaviour. The academic APIs return nothing useful and their absence is **not** evidence of absence.

Go to that domain's primary sources instead: conference talks by the people who shipped it (GDC, SIGGRAPH, Strange Loop), engine or library **source code**, specifications and RFCs, postmortems with data, and issue trackers. An implementer describing their own system outranks a third-party blog summarising it.

Watch for jargon collisions when searching. A domain term that also names a physical object will return patents and retail listings; add domain words to the query rather than assuming the topic is unstudied.

## Worked example

For an end-to-end run showing decomposition, a refutation pass that overturned a confident claim, and a recomputation that changed the recommendation, see [references/worked-example.md](references/worked-example.md).
