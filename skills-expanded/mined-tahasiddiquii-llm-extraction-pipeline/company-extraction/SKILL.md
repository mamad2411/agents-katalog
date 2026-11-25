---
name: company-extraction
description: >
  Extract a structured B2B company record (name, website, industry, employee_count,
  founded_year, city, country, email, phone) from a web document — JSON-LD, labelled HTML,
  or messy prose. Decide rule-vs-LLM by structure, emit strict JSON, resolve vague
  quantities/dates, and never invent values. Use when turning company web pages into rows.
---

# Company extraction skill

A portable spec for turning one company web document into one validated record. The
implementation lives in `src/extractor/`, but the *contract* below is what makes the behaviour
reproducible whether a parser or a model does the work.

## Output schema (strict JSON)

| field | type | rule |
| --- | --- | --- |
| `name` | string (required) | the legal/operating company name, human-readable |
| `website` | string \| null | bare registrable host, lowercased (`acme.com`, not `https://www.Acme.com/about`) |
| `industry` | string \| null | short sector label, adjectives stripped (`robotics`, not `leading robotics`) |
| `employee_count` | int \| null | resolve vague quantities; null over a guess |
| `founded_year` | int \| null | 4-digit year in 1800–present; resolve decades |
| `city` | string \| null | headquarters city |
| `country` | string \| null | headquarters country |
| `email` | string \| null | contact email |
| `phone` | string \| null | E.164-ish digits |

## Route decision (rule vs LLM)

1. **JSON-LD** — `@type: Organization` (or `@context` + `name`) → parse deterministically. No model.
2. **Labelled HTML** — ≥ 3 `Field: value` lines → deterministic selectors. No model.
3. **Prose** — anything else → LLM, because fields must be *interpreted*.

Reach for a parser whenever the structure allows; only escalate to a model when interpretation
is genuinely required. The per-route eval numbers justify the split.

## Extraction rubric (the LLM prompt, `v2`)

- Resolve vague quantities: "a team of about two hundred" → `200`; "a few dozen" → `36`.
- Resolve vague years: "founded in the early 2000s" → `2001`; "mid-90s" → `1995`.
- Normalize `website` to a bare domain.
- **Do not invent values. Prefer `null` over a low-confidence guess.** (This is what keeps
  precision high; recall is allowed to be < 1.0.)

## Post-processing (always)

1. **Validate / repair** — coerce types (`"1,200"` → `1200`), null out impossible values
   (year `1300`, negative headcount), reject records with no name.
2. **Normalize** — canonicalize website + phone so downstream dedup works.
3. **Confidence + review** — below the confidence threshold → human review, not silent load.
4. **Trace** — record route, model, prompt version, tokens, cost, latency, validity.

## Invocation

```bash
extract extract --id d10     # one document → JSON + trace
extract run                  # full ETL: extract → resolve → load
extract eval                 # precision/recall + CI gate
extract drift                # catch a silently-regressed model
```

```python
from extractor import Extractor, RawDocument

result = Extractor().extract_one(RawDocument(id="d1", raw=html_or_prose))
result.company        # validated, normalized Company (or None → review)
result.trace          # route, model, prompt_version, tokens, cost_usd, confidence
```
