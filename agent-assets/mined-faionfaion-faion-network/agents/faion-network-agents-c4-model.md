# C4 Model for Architecture Visualization

## Summary

**One-sentence:** Hierarchical diagrams at four levels: System Context, Containers, Components, Code. Locked toolchain (Structurizr / Mermaid / PlantUML) and per-level audience.

**One-paragraph:** C4 (Simon Brown) gives architecture diagrams a hierarchy: Level 1 Context (system + users + external systems), Level 2 Containers (deployable units + tech), Level 3 Components (internals of one container), Level 4 Code (class diagrams, usually auto-generated). Output is a diagram pack at Levels 1-3 + a chosen toolchain + a sync-with-code policy.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Stakeholders ask 'how does this system fit together?' more than once a quarter.
- Onboarding a new engineer takes > 1 day on architecture alone.
- You have ≥1 external integration or ≥3 deployable containers.

## Skip If (ANY kills it)

- Single binary, single DB, no external integrations.
- No stakeholders beyond the implementing engineer.
- Architecture changes weekly — diagrams will stale before they ship.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| System inventory | list of containers + tech | tech lead |
| External integrations | list | tech lead |
| Toolchain decision | Structurizr / Mermaid / PlantUML | team consensus |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/architecture-decision-records` | Toolchain choice is recorded as an ADR. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the diagram pack + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure: tool choice → L1 context → L2 containers → L3 components → sync policy | ~700 |
| `content/05-examples.xml` | medium | Worked example: Context + Containers diagrams for a SaaS shop | ~600 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-l1-context` | sonnet | Synthesize external systems + actors. |
| `draft-l2-containers` | sonnet | Per-container tech + relationships. |
| `audit-staleness` | opus | Compare diagrams against current repo + manifests. |

## Templates

| File | Purpose |
|------|---------|
| `templates/c4-diagram-pack.md.j2` | C4 diagram-pack spec listing levels + toolchain + sync policy. |
| `templates/c4-diagram-pack.md` | C4 diagram-pack spec listing levels + toolchain + sync policy. Generated from `templates/c4-diagram-pack.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/structurizr-workspace.dsl` | Structurizr DSL workspace skeleton: system + actors + container view scaffolding. |
| `templates/plantuml-context.puml` | PlantUML C4 Context-diagram template using `C4-PlantUML` includes. |
| `templates/mermaid-container.md.j2` | Mermaid Container-diagram template inside a Markdown fence for repo docs. |
| `templates/mermaid-container.md` | Mermaid Container-diagram template inside a Markdown fence for repo docs. Generated from `templates/mermaid-container.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-c4-model.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[architecture-decision-records]]
- [[arch-pattern-clean]]
- [[decision-tree-architecture-style]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
