# Database Selection

## Summary

**One-sentence:** Framework for choosing among 100+ databases by access pattern, consistency need, scale envelope, and operational fit; output is a documented selection ADR.

**One-paragraph:** Database choice is one of the highest-rollback-cost architectural decisions. The framework forces the picker to score candidates against access patterns (read/write ratio, query shape), consistency needs (strong / RYW / eventual), scale envelope (rows × QPS), and operational fit (team familiarity, managed vs self-hosted). Output is an ADR with ≥2 rejected alternatives + a rollback path estimate.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Choosing the primary DB for a new bounded context, OR replacing an existing DB.
- Workload has ≥1 dimension that stresses defaults (rows > 100M, QPS > 1k, multi-region read).
- Decision is consequential (>2 weeks rollback cost).

## Skip If (ANY kills it)

- Tiny app with < 100K rows and < 100 QPS — Postgres default.
- Org-wide DB lock-in already documented and not under review.
- Prototype where DB is throwaway.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Access-pattern profile (read/write ratio, query shape) | table | tech lead |
| Consistency need (strong/RYW/eventual) | doc | domain expert |
| Scale envelope (rows × QPS × growth rate) | estimate | PM |
| Operational constraints (managed/self/hetzner/AWS) | doc | ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/architecture-decision-records` | Selection lands as an ADR. |
| `solo/dev/software-architect/adr-reversibility-tagging` | DB selection is almost always partial_two_way or one_way_door_costly. |
| `solo/dev/software-architect/data-modeling` | Drives schema design after selection. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology fallback | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the selection ADR + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | deep | 6-step procedure: profile → candidates → score → spike → ADR → rollback path | ~900 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-candidates` | sonnet | Per-criterion scoring matrix. |
| `design-spike` | sonnet | Short benchmark plan for top 2 candidates. |
| `audit-existing-fleet` | opus | Spot polyglot-persistence sprawl across the org. |

## Templates

| File | Purpose |
|------|---------|
| `templates/db-selection-adr.md.j2` | Database selection ADR with scoring + rollback path. |
| `templates/db-selection-adr.md` | Database selection ADR with scoring + rollback path. Generated from `templates/db-selection-adr.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-database-selection.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[data-modeling]]
- [[architecture-decision-records]]
- [[adr-reversibility-tagging]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
