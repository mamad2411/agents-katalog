# Domain-Driven Design (DDD)

## Summary

**One-sentence:** Tackles complexity in the heart of software by building a shared model between developers and domain experts using bounded contexts, aggregates, and ubiquitous language.

**One-paragraph:** DDD (Eric Evans, 2003) anchors architecture in domain language, bounded contexts, and aggregates with explicit invariants. Aggregates own consistency boundaries; communication across contexts uses domain events. Output is a context map + per-context model with named aggregates, events, and ubiquitous-language glossary.

**Ефективно для:**

- паст-готова основа для повторюваної задачі 'DDD context modelling' — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф моделі до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Domain has nontrivial business rules (≥3 invariants per aggregate).
- Multiple sub-domains with distinct language exist (e.g., catalog vs ordering vs fulfilment).
- You expect long-lived investment (≥18 months) in the codebase.
- Domain experts available for collaborative modelling.

## Skip If (ANY kills it)

- CRUD app with no real domain rules.
- Greenfield with no domain expert access.
- Throwaway prototype.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain expert availability | calendar slots | PM |
| Glossary draft | spreadsheet/markdown | domain expert |
| Event-storming session output | sticky notes / Miro export | facilitator |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/arch-pattern-clean` | Clean rings are the implementation skeleton for each bounded context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology fallback | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for context map + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | deep | 6-step procedure: storming → contexts → aggregates → events → context map → glossary | ~900 |
| `content/05-examples.xml` | medium | Worked example: ordering bounded context with Order aggregate | ~700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-context-map` | sonnet | Synthesize context relationships from event storm. |
| `design-aggregate` | sonnet | Aggregate boundary + invariants. |
| `audit-language-drift` | opus | Cross-team glossary consistency. |

## Templates

| File | Purpose |
|------|---------|
| `templates/context-map.md.j2` | Bounded context map + per-context aggregate + events. |
| `templates/context-map.md` | Bounded context map + per-context aggregate + events. Generated from `templates/context-map.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-arch-pattern-ddd.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[arch-pattern-clean]]
- [[arch-pattern-hexagonal]]
- [[arch-pattern-onion]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
