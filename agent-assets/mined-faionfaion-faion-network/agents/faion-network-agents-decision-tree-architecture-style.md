# Architecture Style Decision Tree

## Summary

**One-sentence:** Choose between Monolith, Modular Monolith, and Microservices based on team size, DevOps maturity, and deployment-frequency requirements.

**One-paragraph:** A standardised decision tree for the most-mis-decided architectural choice. Inputs: team size, deploy frequency, DevOps maturity, domain coupling, regulatory regime. Output is a recommendation + ADR template + rollback path estimate. Defaults to Modular Monolith for teams under 12; Microservices only when ≥3 of 4 supporting conditions hold.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- New system OR major rewrite is on the table.
- Choosing between Monolith, Modular Monolith, or Microservices is genuine (not predetermined).
- Team has data on size, deploy frequency, and DevOps maturity.

## Skip If (ANY kills it)

- Choice is org-mandated and not under review.
- Stack is fixed (e.g., a specific framework's microservices template).
- Throwaway prototype.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Team size + growth trajectory | headcount + 12mo plan | PM/architect |
| Deploy frequency target | deploys/day or week | PM |
| DevOps maturity score | DORA / SPACE / similar | ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/architecture-decision-records` | Result lands as an ADR. |
| `solo/dev/software-architect/adr-reversibility-tagging` | Architecture-style choice is one_way_door_costly or higher. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the decision record + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure: inputs → score → walk tree → ADR → reversibility tag | ~700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `walk-tree` | sonnet | Per-input branch evaluation. |
| `draft-adr` | sonnet | Template-driven ADR composition. |
| `audit-team-readiness` | opus | DORA + DevOps maturity synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/architecture-style-adr.md.j2` | Architecture style decision ADR template. |
| `templates/architecture-style-adr.md` | Architecture style decision ADR template. Generated from `templates/architecture-style-adr.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-decision-tree-architecture-style.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[architecture-decision-records]]
- [[adr-reversibility-tagging]]
- [[decision-tree-build-vs-buy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
