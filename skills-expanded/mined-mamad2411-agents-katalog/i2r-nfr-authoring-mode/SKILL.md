---
name: i2r-nfr-authoring-mode
description: Walks ISO/IEC 25010:2023 systematically to produce measurable NFRs, each with a Volere fit_criterion; outputs 05-nfr.json.
when_to_use: Loaded by i2r-nfr-author when authoring or repairing stage 05-nfr.json.
user-invocable: false
---

# i2r-nfr-authoring-mode

**Purpose:** Walk all 9 ISO/IEC 25010:2023 quality characteristics, derive NFRs for this product's context, attach a Volere fit_criterion (threshold + environment + period) to every `required` NFR, and mark the rest `not_applicable` (with reason) or `deferred` (with missing info). Produces `05-nfr.json` that passes `i2r.py validate --stage 5`.

---

## Core discipline (read first)

1. **WHAT/WHY only — never HOW.** Apply the stack-swap test: if swapping the database, framework, or infrastructure provider forces an edit to the `description` or `fit_criterion`, rewrite. Naming Redis, S3, PostgreSQL, JWT, or any library inside an NFR = `IMPLEMENTATION_LEAK` (BLOCKER).
2. **No vague adjectives without a number.** "Fast", "secure", "scalable", "robust" in `description` or `fit_criterion` → `PLACEHOLDER` (BLOCKER). Every `required` NFR must have a real `fit_criterion` with a measurable `threshold`.
3. **No silent omission.** Every ISO 25010:2023 characteristic must be CONSIDERED and explicitly marked — `required` (with a real `fit_criterion`), `not_applicable` (with `na_reason`), or `deferred` (with `deferred_missing_info`). A characteristic SILENTLY omitted (neither addressed nor explicitly marked) = `MAJOR` gap, not BLOCKER. The intent is "no silently-empty category", not "all 9 must be `required`".
3b. **An NFR you cannot motivate is over-specification.** Before marking a characteristic `required`, climb the RML ladder (root skill `requirements-minimalism.md`): does this product actually need a quality target here, or is it an engineered default nobody asked for? A `required` NFR with `source: assumed` and no real driver is a candidate to mark `deferred` (with `deferred_missing_info`) instead — the gate surfaces it (`OVER_SPECIFICATION`, MINOR, advisory). Never re-state a platform/standard guarantee (TLS, hashing the stack mandates) as an NFR — that belongs in CONSTRAINTS. The safety floor (security / data / accessibility / compliance) is never minimized away — those stay `required`.
4. **Source every NFR.** `source_ref` → pointer into `raw/` or a decision reference. Never fabricate.

---

## Step-by-step authoring procedure

```
1. Read 04-functional.json → identify the system's actors, data, and delivery context.
2. For each of the 9 ISO 25010:2023 characteristics (see references/iso25010-coverage.md):
   a. Ask: does this product have a meaningful quality target for this characteristic?
   b. If YES (required):
      - Write a description of the quality goal in observable terms.
      - Write a fit_criterion: { threshold, environment, period } (all three required).
      - Assign id: NFR-<ISOCAT>-NN using the short category codes in iso25010-coverage.md.
      - Record source_ref and priority.
   c. If NOT APPLICABLE: set coverage_status = "not_applicable" + na_reason explaining why.
   d. If DEFERRED (info missing): set coverage_status = "deferred" + deferred_missing_info naming exactly what info is needed.
3. Add benign-failure lens items (reliability / cost-capacity / concurrency) — see iso25010-coverage.md §benign.
4. Validate via: Bash(python scripts/i2r.py validate --stage 5).
5. Fix all schema violations before writing the final file.
```

---

## Required output structure

The output `05-nfr.json` must carry `_meta` (§4 of CONTRACT.md) plus `nfrs[]`. Every item must satisfy all required fields in `schemas/05-nfr.schema.json`. Every `required` item must have `fit_criterion` with all three sub-fields present and non-empty.

---

## Key references (depth lives here)

| File | What it teaches |
|---|---|
| `references/iso25010-coverage.md` | All 9 ISO 25010:2023 characteristics; category ID codes; required/NA/deferred guidance; benign-failure lenses |
| `references/volere-fit-criterion-rules.md` | fit_criterion = threshold + environment + period; measurability rules; measurement_method guidance |
| `references/TEMPLATE.json` | Blank NFR item with all required keys — copy-paste start point |
| `references/GOOD_EXAMPLE.json` | Strong NFR anchored on NFR-PERF-01 (measurable threshold, full fit_criterion) |
| `references/BAD_EXAMPLE.md` | Bad NFRs ("must be fast", "secure") with diagnosis and corrected versions |

---

## Hard limits

- `placeholder_scan` rejects in NFR fields: `fast`, `secure`, `scalable`, `robust`, `performant`, `user-friendly`, `TBD`, `TODO`, `as needed` — outside `rationale`. A hit → `PLACEHOLDER` (BLOCKER).
- `fit_criterion` on a `required` NFR: all three of `threshold`, `environment`, `period` must be present and non-empty. Missing any one → gate blocks.
- Never name a specific technology (framework, database, cloud provider, library) in `description` or `fit_criterion`.
- Never emit phases, tasks, architecture, code, or UI.
- Set each NFR's `source` ∈ {stated, assumed, decision}. If a threshold/number is NOT stated in the raw idea (an engineered default you chose to make the NFR testable), set `source: assumed` — never label an invented number as if the user stated it. (out/ surfaces an assumed threshold as 'assumed default — pending confirmation'.)

Sources: ISO/IEC 25010:2023; Volere fit criterion (Robertson & Robertson); PM Skills constraints framework; product-on-purpose template + example anchoring; ponytail laziness ladder (→ RML).
