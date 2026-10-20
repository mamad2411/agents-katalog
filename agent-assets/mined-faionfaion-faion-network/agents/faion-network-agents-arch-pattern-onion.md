# Onion Architecture

## Summary

**One-sentence:** All coupling points toward the center: Domain Model -> Domain Services -> Application Services -> Infrastructure / UI / Tests at the outermost layer.

**One-paragraph:** Onion Architecture (Jeffrey Palermo, 2008) formalises a four-layer onion with the dependency rule: all coupling points inward. Domain Model + Domain Services live in the inner core; Application Services depend on the core; Infrastructure / UI / Tests are at the outermost. Output is a module layout spec + import-direction lint, blocking infra leaking inward.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- .NET-shaped or DDD-leaning codebase where Palermo's terminology is familiar.
- Codebase has clear domain logic separate from infrastructure.
- You expect the project to live > 12 months with ≥2 engineers.

## Skip If (ANY kills it)

- Throwaway prototype or CRUD-only app.
- Team prefers Clean or Hexagonal naming — pick one to avoid double terminology.
- Pure library with no UI/infra concerns.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain model draft | doc/UML | domain expert |
| Service inventory | list | tech lead |
| Import-direction lint tool | config | tooling team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/arch-pattern-clean` | Clean rings are equivalent layers under different names. |
| `solo/dev/software-architect/arch-pattern-ddd` | Domain model + domain services come from DDD. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the layout spec + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure: model → domain services → app services → infra/ui → lint | ~700 |
| `content/05-examples.xml` | medium | Worked example: .NET-style onion for an Ordering bounded context | ~600 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `design-layout` | sonnet | Layer assignment per module. |
| `draft-import-lint` | sonnet | Tool-specific lint config. |
| `audit-existing-codebase` | opus | Detect violations in current import graph. |

## Templates

| File | Purpose |
|------|---------|
| `templates/onion-layout.md.j2` | Onion Architecture layout spec with four layers and lint contract. |
| `templates/onion-layout.md` | Onion Architecture layout spec with four layers and lint contract. Generated from `templates/onion-layout.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-arch-pattern-onion.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[arch-pattern-clean]]
- [[arch-pattern-hexagonal]]
- [[arch-pattern-ddd]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
