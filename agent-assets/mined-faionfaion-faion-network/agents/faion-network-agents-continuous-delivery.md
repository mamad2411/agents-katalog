# Continuous Delivery (Index)

## Summary

**One-sentence:** Router for the CD cluster: triages to cd-basics (principles + prereqs + expand-contract migrations) or cd-pipelines (YAML + strategies + health checks + rollback).

**One-paragraph:** Router for the CD cluster: triages to cd-basics (principles + prereqs + expand-contract migrations) or cd-pipelines (YAML + strategies + health checks + rollback). Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Need to decide which CD methodology to load first (principles vs concrete pipeline).
- Triaging a CD adoption project from cold start.
- Choosing between deepening principle knowledge or shipping pipeline YAML.
- Output produces `decision-record` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Need to decide which CD methodology to load first (principles vs concrete pipeline).
- Triaging a CD adoption project from cold start.
- Choosing between deepening principle knowledge or shipping pipeline YAML.

## Skip If (ANY kills it)

- Already know which child you need — load it directly.
- No CD ambition; classic manual release workflow is the chosen pattern.
- Stack is batch / one-shot — CD methodology doesn't apply.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| CD adoption stage | principles-needed / pipeline-needed | team |
| Existing pipeline (if any) | ci.yml or cd.yml | repository |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-stage` | haiku | Map team state to principles vs pipeline path. |
| `dispatch-child` | haiku | Emit pointer to cd-basics or cd-pipelines. |

## Templates

| File | Purpose |
|------|---------|
| `templates/triage_checklist.md` | Triage checklist routing to cd-basics or cd-pipelines |
| `templates/_smoke-test.md` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-continuous-delivery.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[cd-basics]]
- [[cd-pipelines]]
- [[feature-flags-types-lifecycle]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are all CD prerequisites in place (CI + tests + IaC + flags)?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
