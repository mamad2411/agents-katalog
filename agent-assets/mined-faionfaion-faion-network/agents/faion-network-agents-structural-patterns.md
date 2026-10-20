# Structural Design Patterns

## Summary

**One-sentence:** Selects a GoF structural pattern (Adapter, Bridge, Composite, Decorator, Facade, Proxy, Flyweight) from concrete symptom signals; emits ADR with cost + alternative + ban on stacking >2 decorators.

**One-paragraph:** Selects a GoF structural pattern (Adapter, Bridge, Composite, Decorator, Facade, Proxy, Flyweight) from concrete symptom signals; emits ADR with cost + alternative + ban on stacking >2 decorators. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Concrete symptom matches one of: incompatible interfaces, growing class hierarchy, tree-of-tree behaviour, behaviour stacking, broad subsystem entry-point, access control on object, memory pressure from many similar instances.
- Code review identifies a coupling smell a structural pattern would dissolve.
- ADR proposes a structural pattern and needs catalog-grounded justification.
- Output produces `decision-record` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Concrete symptom matches one of: incompatible interfaces, growing class hierarchy, tree-of-tree behaviour, behaviour stacking, broad subsystem entry-point, access control on object, memory pressure from many similar instances.
- Code review identifies a coupling smell a structural pattern would dissolve.
- ADR proposes a structural pattern and needs catalog-grounded justification.

## Skip If (ANY kills it)

- Speculative application — no symptom yet, just 'we might need it'.
- Trivial CRUD layer where the pattern would be the only complexity.
- Behavioural / creational concern in disguise — wrong pattern family.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Code or design exhibiting the symptom | code / diagram | team |
| Catalog reference (GoF + cloud-native) | doc / link | architect |
| Test coverage of affected area | data | QA |
| Change-impact estimate (files touched) | data | team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[patterns-overview]] | Selection between pattern families starts here. |

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
| `match-symptom-to-pattern` | haiku | Lookup signal → candidate structural patterns. |
| `score-cost-and-fit` | sonnet | Bounded scoring (indirection cost vs symptom severity). |
| `draft-adr` | sonnet | Compose ADR with rejected alternatives + cost + review trigger. |

## Templates

| File | Purpose |
|------|---------|
| `templates/structural-pattern-adr.md.j2` | ADR skeleton for structural pattern selection. |
| `templates/structural-pattern-adr.md` | ADR skeleton for structural pattern selection. Generated from `templates/structural-pattern-adr.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/decorator-cap-rule.md.j2` | Lint / convention enforcing decorator stack depth ≤ 2. |
| `templates/decorator-cap-rule.md` | Lint / convention enforcing decorator stack depth ≤ 2. Generated from `templates/decorator-cap-rule.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.md.j2` | Minimum viable filled-in artefact for sanity-checking the schema. |
| `templates/_smoke-test.md` | Minimum viable filled-in artefact for sanity-checking the schema. Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-structural-patterns.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[patterns-overview]]
- [[system-design-process]]
- [[quality-attributes]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is there a concrete structural symptom (interface mismatch, class explosion, behaviour stacking, broad entry point, access control, memory pressure)?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
