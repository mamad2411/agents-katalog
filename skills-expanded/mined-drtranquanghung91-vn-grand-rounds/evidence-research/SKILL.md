---
name: evidence-research
description: Use when a medical presentation needs facts, numbers, trial results, guideline recommendations or references, whether from papers the user supplied or from a literature search (PubMed, Europe PMC, ClinicalTrials.gov, OpenEvidence), and before any number is written on a slide.
---

# Evidence research

## Overview

Every claim a slide makes becomes a record: what is claimed, which source says it, where in
the source, the exact words, and how well you could check it. A paper existing does not make
a number from it correct. Numbers are copied from the source passage, never recalled.

**Identifiers (PMID, DOI, NCT) come only from a lookup you ran in this session.** An
identifier you remember, even one marked "(verify)", does not go into any file.

## Sources, in order

1. Files the user supplied (`<talk>/sources/`). Read the full text: results, tables,
   figure legends, supplement if given.
2. The database tools the user allowed in the brief. If the user named one (for example
   "OpenEvidence only"), use only that one and record what it could not give you as a gap.
3. Otherwise:
   - **PubMed** through a PubMed MCP server if one is connected, else
     `python scripts/pubmed.py` (see `--help`; needs no API key).
   - **Europe PMC** for full text of open-access papers (`pubmed.py fulltext`).
   - **ClinicalTrials.gov** for the registered design and endpoints (`pubmed.py trial NCT…`).
   - Guidelines from the issuing society's own site.

Record every search string and its date in `evidence/notes.md`.

## Extracting a claim

For each claim the plan lists:

- Copy the number exactly as printed, with its unit, CI and P value. Keep the
  denominator.
- Record the **locator** (page, table, figure panel, section) and a **verbatim quote** of
  20–60 words that contains the number.
- Classify it with `kind`:

| kind | Use for | Watch for |
|------|---------|-----------|
| `observed` | results actually measured | primary vs secondary endpoint; ITT vs per-protocol; interim vs final |
| `planned` | protocol assumptions, sample-size targets | never present as a result |
| `derived` | numbers you computed (1 − HR, absolute difference, NNT) | store the formula in `derivation` |
| `recommendation` | guideline statements | keep class and level, and the exact wording |
| `background` | epidemiology, mechanism | prefer reviews or guidelines from the last 5 years |

- Set `status`: `verified-fulltext`, `verified-abstract` (you saw only the abstract), or
  `unverified` (could not open any version). Unverified claims may stay in the plan but are
  flagged to the user.

## Files

`evidence/references.json`:

```json
{"references": [{"id": "long2026", "title": "…", "authors": ["Long GV", "…"],
  "journal": "N Engl J Med", "year": 2026, "volume": "", "pages": "",
  "doi": "10.1056/…", "pmid": "…", "nct": "",
  "retrieved_with": "pubmed.py esummary", "access": "full-text"}]}
```

`evidence/claims.json`:

```json
{"claims": [{"id": "c07", "slide": 7, "text": "RFS at 24 months, intervention vs control",
  "values": ["82.2%", "70.0%", "HR 0.58", "0.45–0.75"], "source": "long2026",
  "locator": "p. 6, Results; Fig. 1A", "quote": "…exact words…",
  "kind": "observed", "status": "verified-fulltext"}]}
```

`pubmed.py refs PMID…` prints reference records in this shape from a real lookup.

## Common mistakes

- Swapping endpoints: an HR from RFS written under DMFS. Each value's quote must name its
  endpoint.
- Reporting "improved" for a result whose CI crosses 1. Store the CI and P value so the
  audit can catch it.
- Taking a conference abstract's interim number when the paper reports a later one. Note
  the data cut-off date.
- Citing a review for a trial result. Cite the trial.
