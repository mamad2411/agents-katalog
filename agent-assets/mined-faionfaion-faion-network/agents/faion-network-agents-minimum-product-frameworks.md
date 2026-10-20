# Minimum Product Frameworks

## Summary

**One-sentence:** Pick one of four minimum-product frames (MVP / MLP / MMP / MMR) for the current goal, document the trade-off, and run the matching planning methodology.

**One-paragraph:** Different goals demand different 'minimum' framings: MVP for learning, MLP for love, MMP for marketable, MMR for revenue. The decision matrix maps goal → frame → downstream methodology. Picking wrong = building a Minimum Lovable Product when you needed an MVP (or vice versa).

**Ефективно для:**

- Solo founder who keeps hearing different acronyms (MVP/MLP/MMP) and isn't sure which fits — needs a decision matrix that maps current goal to the right framework.

## Applies If (ALL must hold)

- Goal is set for the next ship (learn / love / market / monetise).
- Multiple frames plausible — needs disambiguation.
- Downstream methodology will be picked from the frame.

## Skip If (ANY kills it)

- Goal is genuinely ambiguous — fix that first.
- Frame is locked by external constraint (e.g. investor mandate).
- Single-day patch — no framework needed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Stated goal for the ship | string | PM doc |
| Decision matrix reference | table | Team doc |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning/mvp-scoping` | MVP downstream methodology. |
| `solo/product/product-planning/mlp-planning` | MLP downstream methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-minimum-product-frameworks` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-minimum-product-frameworks` | haiku | Schema check + threshold checks; deterministic. |
| `review-minimum-product-frameworks` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/minimum-product-frameworks.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-minimum-product-frameworks.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[mvp-scoping]]
- [[mlp-planning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
