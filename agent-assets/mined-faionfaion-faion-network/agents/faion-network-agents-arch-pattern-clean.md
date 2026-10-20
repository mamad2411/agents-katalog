# Clean Architecture

## Summary

**One-sentence:** Dependencies point inward through concentric circles: Domain (Entities) at the center, then Application (Use Cases), then Interface Adapters, then Frameworks and Drivers at the outside.

**One-paragraph:** Clean Architecture (Uncle Bob, 2012) places the domain at the centre and arranges everything else in concentric circles, with the dependency rule: source-code dependencies can only point inward. Frameworks, UI, databases, and external services live at the outer ring as adapters. Output is a module layout plus an enforced import-direction lint, blocking the common drift of domain code importing infra.

**Ефективно для:**

- паст-готова основа для повторюваної задачі 'clean architecture layout' — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф імпорт-напрямку до того, як він потрапить у CI.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Codebase has clear business logic separate from infrastructure (DB, HTTP, queues).
- You expect the project to live > 12 months with ≥2 engineers.
- You want to swap frameworks or persistence layer without rewriting the domain.

## Skip If (ANY kills it)

- Throwaway prototype or CRUD-only app with no domain logic.
- Tiny script (< 500 LOC) with no test pyramid.
- Team unfamiliar with DI; cost of indirection > benefit.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Bounded context list | list | domain expert |
| Use case list | list | PM/architect |
| Lint tool that can enforce import direction | config | tooling team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/arch-pattern-hexagonal` | Ports-and-adapters is the implementation surface of Clean. |
| `solo/dev/software-architect/arch-pattern-ddd` | Domain modelling for the centre ring. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the layout spec + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure: identify entities → use cases → adapters → frameworks → enforce direction | ~700 |
| `content/05-examples.xml` | medium | Worked example: e-commerce ordering with Clean Architecture layout | ~600 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-layout` | sonnet | Per-ring module assignment. |
| `draft-import-lint` | sonnet | Tool-specific lint config (Python/Java/Go). |
| `audit-existing-codebase` | opus | Detect violations in current import graph. |

## Templates

| File | Purpose |
|------|---------|
| `templates/clean-layout.md.j2` | Clean Architecture module layout spec. |
| `templates/clean-layout.md` | Clean Architecture module layout spec. Generated from `templates/clean-layout.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-arch-pattern-clean.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[arch-pattern-hexagonal]]
- [[arch-pattern-onion]]
- [[arch-pattern-ddd]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
