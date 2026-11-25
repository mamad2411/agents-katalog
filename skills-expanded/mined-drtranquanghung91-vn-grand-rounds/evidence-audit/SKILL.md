---
name: evidence-audit
description: Use when a medical slide deck (HTML or PPTX) is built or edited and before it is presented, shared or called finished; when numbers, hazard ratios, percentages, recommendations or references on slides need checking against their sources; or when a clinical-case deck may contain patient identifiers.
---

# Evidence audit

## Overview

You are checking someone else's work. The question is not "is the source real?" but "does
the source say exactly this, about this endpoint, in this population?". Read the source
passage for every claim; do not trust the ledger's quote.

## Procedure

1. **Run the scripts** (from this skill's folder):

   ```bash
   python scripts/verify_refs.py <talk>/evidence/references.json
   python scripts/check_claims.py <talk>/out/<deck> <talk>/evidence/claims.json --refs <talk>/evidence/references.json
   python scripts/phi_scan.py <talk>/out/<deck>
   ```

   - `verify_refs` confirms that each PMID/DOI exists and that its title, year and first
     author match the record.
   - `check_claims` lists every number on every slide that no claim covers, claims whose
     values are missing from their own quote, and claims citing unknown references.
   - `phi_scan` flags dates, record numbers, phone numbers, ID numbers and names.

2. **Read each claim against its source**: open the source at the locator. Check for each
   claim:
   - the value, unit, CI, P value and denominator;
   - the right endpoint, population (ITT, per-protocol, subgroup) and time point;
   - observed results versus protocol assumptions;
   - interim versus final data, and the data cut-off.

3. **Check the wording on the slide**:
   - "improved", "reduced", "superior" when the CI crosses 1 or P ≥ 0.05;
   - causal language from observational data;
   - a subgroup presented as a main result;
   - relative effects without absolute ones on the key slide;
   - a surrogate presented as a hard outcome;
   - a guideline recommendation paraphrased into a stronger one;
   - a title that asserts more than the evidence on that slide shows.

4. **Check figures** against `figures/manifest.json`. Each figure needs a source and
   locator. Reused figures need a licence or a stated educational-use basis. Rebuilt
   diagrams must use only numbers that appear in `claims.json`.

5. **Privacy** (all case decks, and any deck where `phi_scan` reports a hit). No names,
   initials with dates, record numbers, exact dates (use D0, D3), addresses, faces or
   identifiable images without documented consent. A clean `phi_scan` does not clear a deck:
   look at the images.

## Report: `<talk>/audit/evidence-report.md`

```markdown
# Evidence audit: <deck> (<date>)
Result: PASS | FAIL (<n> blocking, <n> advisory)

## Blocking
- E-NUM-01 · slide 7 · "HR 0.58" under DMFS; source (long2026, p. 6) gives DMFS HR 0.62
  (95% CI 0.45–0.85). 0.58 is RFS. → Fix: …

## Advisory
- …

## Not checked
- <claims whose sources could not be opened, and why>
```

Finding codes:

| Code | Meaning |
|------|---------|
| E-NUM | a value doesn't match its source |
| E-SRC | no source, or the source doesn't support the claim |
| E-REF | reference metadata is wrong or unverifiable |
| E-CLAIM | overclaim or misleading wording |
| E-FIG | figure provenance or licence problem |
| E-PHI | a patient could be identified |

Every E-NUM, E-SRC, E-REF and E-PHI finding is blocking. E-CLAIM and E-FIG findings are
blocking when they change the meaning.
