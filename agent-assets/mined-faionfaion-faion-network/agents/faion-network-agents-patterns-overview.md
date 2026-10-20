# Design Patterns Overview

## Summary

**One-sentence:** Routes a design problem to a GoF (creational / structural / behavioural) or cloud-native pattern (CQRS, Saga, Circuit Breaker) using problem-signal triggers; emits a pattern-selection ADR.

**One-paragraph:** Routes a design problem to a GoF (creational / structural / behavioural) or cloud-native pattern (CQRS, Saga, Circuit Breaker) using problem-signal triggers; emits a pattern-selection ADR. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Designing a new module / service where the problem matches a known catalog pattern.
- Refactoring code that hits a pain point with a documented pattern fix (Strategy, State, Circuit Breaker).
- Reviewing an ADR whose stated pattern needs catalog-grounded justification.
- Output produces `decision-record` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Designing a new module / service where the problem matches a known catalog pattern.
- Refactoring code that hits a pain point with a documented pattern fix (Strategy, State, Circuit Breaker).
- Reviewing an ADR whose stated pattern needs catalog-grounded justification.

## Skip If (ANY kills it)

- Pattern is being applied speculatively — wait for a real pain signal before introducing the indirection.
- Problem is a trivial CRUD operation — patterns add cost not value.
- Pattern catalog is already mandated by org policy and matches the problem exactly.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Problem statement (one paragraph) | Markdown | team |
| Symptom evidence (logs, latency, code smell) | data | team |
| Existing code or design draft | code / diagram | team |
| Pattern catalog reference (GoF / cloud-native) | doc / link | architect |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[structural-patterns]] | Catalog of structural patterns and selection cues. |
| [[system-design-process]] | Patterns plug into the design process. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure with input/action/output per step | 900 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-symptom` | haiku | Lookup signal → pattern bucket. |
| `pick-pattern` | sonnet | Bounded judgement: pattern fit + cost. |
| `draft-adr` | sonnet | Compose ADR with rejected alternatives + cost. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pattern-selection-adr.md.j2` | ADR skeleton recording the chosen pattern + rejected alternatives. |
| `templates/pattern-selection-adr.md` | ADR skeleton recording the chosen pattern + rejected alternatives. Generated from `templates/pattern-selection-adr.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/pattern-signal-table.md.j2` | Lookup table mapping symptom → candidate patterns. |
| `templates/pattern-signal-table.md` | Lookup table mapping symptom → candidate patterns. Generated from `templates/pattern-signal-table.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in artefact for sanity-checking the schema. |
| `templates/_smoke-test.md` | Minimum viable filled-in artefact for sanity-checking the schema. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-patterns-overview.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[structural-patterns]]
- [[system-design-process]]
- [[modular-monolith]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is a concrete symptom documented with measurable signals?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
