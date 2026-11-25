---
name: bio-literature-review
version: 1.0.0
description: Run a structured life-sciences literature search and synthesize findings into a cited, evidence-graded review.
author: matrixx0070
tags: [biology, literature, pubmed, biorxiv, review, evidence-grading]
capabilities: []
---

## When to use

Use this when the user needs a defensible summary of what is known about a gene, pathway, disease mechanism, modality, or method, with traceable citations rather than unsourced prose. Reach for it before target work, grant writing, or experiment design.

**Not for:** ranking drug targets (use bio-target-prioritization), choosing what to work on (use bio-problem-selection), or answering a single factual lookup where one authoritative reference already settles it.

## Method

1. Frame the question in PICO terms: population/system, intervention/perturbation, comparator, outcome. State species scope and time window.
2. Build a query set: MeSH terms, free-text synonyms, HGNC gene aliases, and preprint spellings. **Decision:** if aliases are ambiguous (e.g. a symbol reused across species), split into separate queries rather than OR-ing them.
3. Search PubMed/PMC for peer-reviewed work and bioRxiv/medRxiv for preprints. Tag preprints as unreviewed at capture time.
4. Screen by title/abstract, then full text. Record inclusion/exclusion counts so the search is reproducible.
5. Extract per paper into an evidence table: design, model system, sample size, effect direction/magnitude, key caveats.
6. Grade each claim. **Decision:** strong = multiple independent in vivo/clinical; moderate = single robust study or consistent in vitro; weak = preprint, correlational, or contested. If two strong papers disagree, log a contradiction — do not average them away.
7. Synthesize: consensus, open controversies, and gaps that motivate new work.

## Example

Question: "Does TREM2 loss-of-function increase Alzheimer's risk?" You query `TREM2 AND (Alzheimer OR "amyloid") AND (variant OR knockout)`, screen 60 hits to 14, and build the table. Human genetics (R47H GWAS/Mendelian, multiple cohorts) grades **strong**; mouse amyloid-clearance studies grade **moderate** and split on direction depending on disease stage. Output flags the stage-dependence as an open controversy rather than a settled effect.

## Pitfalls

- Citing an abstract you never opened — confabulated PMIDs are the top failure. Verify every identifier resolves.
- Treating a preprint as equivalent to peer-reviewed evidence.
- Missing papers because you searched the current gene symbol only and skipped historical aliases.
- Burying a contradiction inside "studies suggest" instead of naming both sides.

## Output format

```
# <Question> — Evidence Review
Executive summary: <one paragraph>

## Evidence table
| Claim | Grade (strong/mod/weak) | Key refs (PMID/DOI) | Caveat |

## Synthesis (by sub-question)
- <consensus / controversy per group>

## Contradictions & gaps
- <conflicting findings, missing studies>

## References
1. Author, Year. Title. PMID/DOI. [preprint if applicable]
```
Never invent a citation. If a claim is unsupported, say so and mark it UNVERIFIED.

## Reference

### Evidence hierarchy (adapted from GRADE and OCEBM)

GRADE grades a body of evidence, not a single paper, and rates *certainty* in four levels. Start high for RCT-type designs and low for observational, then move up or down.

| Certainty | Meaning | Typical basis |
|-----------|---------|---------------|
| High ⊕⊕⊕⊕ | Further research very unlikely to change the estimate | Consistent, low-bias RCTs or large Mendelian-randomization + replicated GWAS |
| Moderate ⊕⊕⊕ | Further research may change the estimate | Single good RCT, or downgraded observational with large effect |
| Low ⊕⊕ | Estimate is uncertain | Observational, small n, indirect model |
| Very low ⊕ | Any estimate is very uncertain | Case reports, mechanistic-only, contested preprints |

GRADE downgrades for: (1) **risk of bias**, (2) **inconsistency** (heterogeneity, I² high), (3) **indirectness** (surrogate endpoint, wrong population/species), (4) **imprecision** (wide CI crossing null), (5) **publication bias** (funnel asymmetry). GRADE upgrades observational data for: large effect (RR >2 or <0.5), dose-response gradient, and plausible confounding that would only strengthen the effect. For a preclinical mechanism review, map "human genetics + in-vivo replication" → high; "single in-vitro" → low.

Classic OCEBM levels for orientation: 1 = systematic review of RCTs; 2 = individual RCT; 3 = non-randomized cohort/case-control; 4 = case series; 5 = mechanism-based reasoning. Preprints inherit the design's level but carry a standing "risk of bias: not peer reviewed" flag until published.

### PubMed / PMC search syntax

Field tags (append in `[...]`):

| Tag | Field | Example |
|-----|-------|---------|
| `[mesh]` | MeSH term (exploded by default) | `alzheimer disease[mesh]` |
| `[majr]` | MeSH major topic | `neoplasms[majr]` |
| `[mesh:noexp]` | MeSH, no explosion | `dementia[mesh:noexp]` |
| `[tiab]` | Title/abstract free text | `TREM2[tiab]` |
| `[ti]` | Title only | `microglia[ti]` |
| `[tw]` | Text word (broad) | `amyloid[tw]` |
| `[au]` | Author | `Karran E[au]` |
| `[dp]` | Date of publication | `2018:2024[dp]` |
| `[pt]` | Publication type | `randomized controlled trial[pt]` |
| `[la]` | Language | `english[la]` |
| `[sb]` | Subset filter | `medline[sb]` |

Boolean operators are **uppercase** `AND` / `OR` / `NOT`; parentheses nest; double-quotes force phrase search; `*` truncates (min 4 leading chars, e.g. `inflamm*`). MeSH auto-explodes to narrower terms unless you use `:noexp`. "Automatic Term Mapping" silently expands untagged words — tag terms explicitly for reproducible queries. Use the `#1 AND #2` History syntax to combine numbered searches. PMC full-text adds `[body]` and `[fulltext]`. bioRxiv/medRxiv have no MeSH — rely on `[tiab]`/keyword and their category facets, and always resrecord the version (v1/v2) since preprints mutate.

### Reporting standards to cite by study type

PRISMA (systematic reviews, 27-item checklist + flow diagram of identified→screened→included), CONSORT (RCTs), STROBE (observational), ARRIVE 2.0 (in-vivo animal studies — the "essential 10" incl. sample size, randomization, blinding), MIAME/MINSEQE (array/seq data), STARD (diagnostic accuracy). Note which standard a paper claims to follow; deviation is a bias signal.

### Identifier hygiene

PMID = integer, resolves at `pubmed.ncbi.nlm.nih.gov/<id>`. PMCID = `PMC` + digits (full text). DOI = `10.xxxx/...`, resolves at `doi.org/<doi>`. Preprint DOIs from bioRxiv are `10.1101/<date>.<id>`. Verify every identifier resolves to the title you cite — a plausible-looking but wrong PMID is the single most common confabulation failure. Gene symbols: reconcile against HGNC (`genenames.org`) and record aliases/prior symbols so historical papers aren't missed.
