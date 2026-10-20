---
description: >
  Queries a specific U.S. public database for a name. Available databases:
  fec, lda, fara, fl (Florida Sunbiz), de (Delaware), tx (Texas),
  oc (OpenCorporates), news-br (Brazilian press), news-us (U.S. press).
argument-hint: "<database> \"Full Name\""
---

You will query the database specified as the first argument, searching for
the name in quotes from $ARGUMENTS.

All output must be in **English**.

## Expected argument format

```
fec "Carlos Ferreira"
lda "Carlos Eduardo Ferreira"
oc "Ferreira Global LLC"
news-us "Carlos Ferreira"
```

## Database-to-skill mapping

| Database        | Skill / Script                                             |
|-----------------|------------------------------------------------------------|
| `fec`           | `skills/search-fec/SKILL.md` + MCP fec-finance             |
| `lda`           | `skills/search-lobby-fara/scripts/lda_search.py`           |
| `fara`          | `skills/search-lobby-fara/scripts/fara_search.py`          |
| `fl`            | `skills/search-state-corps/scripts/florida_sunbiz.py`      |
| `de`            | `skills/search-state-corps/scripts/delaware_corp.py`       |
| `tx`            | `skills/search-state-corps/scripts/texas_comptroller.py`   |
| `oc`            | `skills/search-opencorporates/scripts/opencorporates_search.py` |
| `news-br`       | `skills/search-news-archive/SKILL.md` (BR outlets)         |
| `news-us`       | `skills/search-news-archive/SKILL.md` (US outlets)         |

## Rules

1. Before searching, generate name variations using `expand-brazilian-identity`.
2. Cite the source of each result in the project's standard format.
3. If the database returns no results, list the variations tested and explain
   any applicable legal context (e.g., 52 U.S.C. § 30121 for FEC).
4. Output as JSON following `schemas/findings.schema.json`.
