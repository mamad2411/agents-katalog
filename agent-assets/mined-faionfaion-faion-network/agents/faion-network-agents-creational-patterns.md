# Creational Design Patterns

## Summary

**One-sentence:** Six GoF creational patterns (Factory Method, Abstract Factory, Builder, Prototype, Singleton, Object Pool) and DI for object creation that increases flexibility and reuse.

**One-paragraph:** Creational patterns control how objects are created so the rest of the system depends on abstractions instead of constructors. Output is a per-codebase creational-pattern selection record: which factories, which builder, which DI container, and the lint that prevents direct `new` of cross-context types.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Object construction is non-trivial (≥3 parameters, ≥1 invariant, async setup).
- Multiple variants of the same type need to be created at runtime.
- Tests need controlled fixtures of the same type.

## Skip If (ANY kills it)

- Trivial value objects with 1-2 fields.
- Singletons would be the only choice — usually a sign of static state, refactor instead.
- Throwaway prototype.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Construction hotspot list | list of types + call sites | tech lead |
| DI framework / convention | name or 'manual' | team consensus |
| Test fixture inventory | list | test lead |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/behavioral-patterns` | Creational patterns frequently pair with Strategy/State. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for selection record + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure: hotspot → pattern → DI → tests → lint | ~700 |
| `content/05-examples.xml` | medium | Worked example: Builder for a multi-field Order + Factory per payment provider | ~600 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-pattern` | sonnet | Per-hotspot pattern selection. |
| `draft-builder` | sonnet | Multi-step constructor scaffold. |
| `cross-codebase-audit` | opus | Spot direct `new` of cross-context types. |

## Templates

| File | Purpose |
|------|---------|
| `templates/creational-selection.md.j2` | Creational pattern selection record. |
| `templates/creational-selection.md` | Creational pattern selection record. Generated from `templates/creational-selection.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-creational-patterns.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[behavioral-patterns]]
- [[structural-patterns]]
- [[arch-pattern-clean]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
