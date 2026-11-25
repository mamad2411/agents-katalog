---
name: evidence-review
description: Answer a biomedical or life-sciences research question with a cited evidence summary, using the BioLit MCP tools (PubMed, Europe PMC, NCBI Gene, UniProt). Use when a scientist asks what is known about a drug, target, gene, disease mechanism or clinical result and needs claims traced to PMIDs.
---

# Evidence Review

Produce a short, citation-grounded answer a scientist can check. Every factual claim must trace to a paper you actually read in this session.

## Workflow

1. **Scope the question.** Identify the entities (drug, gene, disease, population) and what kind of evidence would answer it (RCT, meta-analysis, mechanistic study, review).
2. **Resolve entities when relevant.** For genes or proteins, call `lookup_gene` and/or `lookup_protein` to get official symbols, aliases and function. Use aliases to widen searches.
3. **Search.** Call `search_pubmed` with 2–3 focused queries (e.g. entity + outcome, entity + "randomized", entity + "meta-analysis"). Use `min_year` when recency matters. Prefer trials, meta-analyses and systematic reviews for clinical questions.
4. **Read before citing.** Call `get_abstracts` on the most relevant 5–15 PMIDs. Only abstracts returned here count as evidence.
5. **Write claims.** Each claim is one sentence supported by the abstracts you cite for it. Include effect sizes, populations and study type when the abstract states them.
6. **Check yourself.** Before answering, confirm that every cited PMID came back from `get_abstracts` (not `not_found`) and that its abstract actually supports the claim. Remove or rewrite any claim that fails.

## Rules

- Never cite a PMID from memory. If you can't find support, say the evidence was not found.
- Don't overstate: distinguish RCT evidence from observational, preclinical or review findings.
- Surface disagreement between studies instead of averaging it away.
- Note important gaps (e.g. only abstracts read, no head-to-head trials, small samples).

## Output format

```
**Answer:** 2–4 sentence bottom line.

**Evidence**
- Claim … [PMID: 12345678]
- Claim … [PMID: 23456789, 34567890]

**Strength & gaps:** study types, conflicts, what's missing.

**References**
- PMID 12345678 — First author et al., Journal (Year). Title.
```
