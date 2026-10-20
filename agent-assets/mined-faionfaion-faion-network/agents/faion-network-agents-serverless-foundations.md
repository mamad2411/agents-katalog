# Serverless Architecture Foundations

## Summary

**One-sentence:** Foundational checklist for adopting serverless: execution model, statelessness, event sources, observability, vendor lock-in awareness, and IaC discipline. Output: yes/no checklist with rationale.

**One-paragraph:** Foundational checklist for adopting serverless: execution model, statelessness, event sources, observability, vendor lock-in awareness, and IaC discipline. Output: yes/no checklist with rationale. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Team is evaluating serverless for the first time on a real workload.
- Reviewing an existing serverless service for hygiene.
- Setting org-wide serverless guardrails before a new platform.
- Output produces `checklist` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Team is evaluating serverless for the first time on a real workload.
- Reviewing an existing serverless service for hygiene.
- Setting org-wide serverless guardrails before a new platform.

## Skip If (ANY kills it)

- Workload already mapped to a non-serverless runtime and not under reconsideration.
- Team has shipped 10+ serverless services already; this checklist is below their bar.
- One-off throwaway script with no operational expectations.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Workload description (purpose, RPS, latency) | doc | team |
| Cloud provider + region | field | ops |
| Identity provider | field | ops |
| Observability stack | field | SRE |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `run-checklist` | haiku | Walk the items and mark yes/no/na with rationale. |
| `summarise` | sonnet | Produce summary + recommended next step (pattern selection, opt-out). |

## Templates

| File | Purpose |
|------|---------|
| `templates/serverless-foundations-checklist.md.j2` | Markdown checklist mirroring the rule set. |
| `templates/serverless-foundations-checklist.md` | Markdown checklist mirroring the rule set. Generated from `templates/serverless-foundations-checklist.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in artefact for sanity-checking the schema. |
| `templates/_smoke-test.md` | Minimum viable filled-in artefact for sanity-checking the schema. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-serverless-foundations.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[serverless-architecture-patterns]]
- [[serverless-cold-start-optimization]]
- [[serverless-cost-optimization]]
- [[serverless-iac-and-templates]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are all four prerequisites populated (workload, provider, IAM, observability)?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
