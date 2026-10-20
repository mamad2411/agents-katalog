# Behavioral Design Patterns

## Summary

**One-sentence:** Nine GoF behavioral patterns (Strategy, Observer, Command, State, Chain of Responsibility, Template Method, Mediator, Iterator, Visitor) for controlling object communication at runtime.

**One-paragraph:** Behavioral patterns address how objects communicate and distribute responsibility. Output is a per-codebase pattern selection record naming which patterns are intentionally used, the rule for picking among confusable patterns (Strategy vs State vs Chain of Responsibility), and the lint / review check that prevents accidental misuse.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Codebase has runtime variance in behaviour (e.g., 'choose one of N algorithms', 'react to events').
- You see if/else or switch on type that grows weekly.
- ≥2 engineers will touch the variance-bearing code.

## Skip If (ANY kills it)

- Codebase is small (<5K LOC) and behaviour is stable.
- Solo founder with throwaway prototype.
- Pattern would add ≥2 layers of indirection over a 1-line if/else.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Variance hotspot list | list of files/methods | tech lead |
| Refactoring budget | story points / hours | PM |
| Language idiom catalogue | doc | tech lead |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/creational-patterns` | Object creation patterns complement behavioural ones. |
| `solo/dev/software-architect/arch-pattern-clean` | Behavioural patterns live in the inner rings. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the pattern selection record + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure: locate variance → diagnose → pick pattern → refactor → review | ~700 |
| `content/05-examples.xml` | medium | Worked example: refactoring an if/elif/else into Strategy | ~600 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-variance` | sonnet | Decide which pattern (Strategy/State/Chain) fits the variance. |
| `draft-refactor` | sonnet | Per-pattern refactor scaffold. |
| `cross-codebase-audit` | opus | Spot misuse patterns across modules. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pattern-selection.md.j2` | Behavioural pattern selection record. |
| `templates/pattern-selection.md` | Behavioural pattern selection record. Generated from `templates/pattern-selection.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/chain-py.py` | Chain of Responsibility Python skeleton with fluent `set_next` chaining. |
| `templates/command-py.py` | Command pattern Python skeleton with invoker + undo/redo stack. |
| `templates/observer-py.py` | Observer pattern Python skeleton: subject + subscribe/unsubscribe + notify. |
| `templates/state-py.py` | State pattern Python skeleton: context delegates behaviour to current state. |
| `templates/strategy-py.py` | Strategy pattern Python skeleton: interchangeable algorithm objects. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-behavioral-patterns.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[creational-patterns]]
- [[arch-pattern-clean]]
- [[arch-pattern-hexagonal]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
