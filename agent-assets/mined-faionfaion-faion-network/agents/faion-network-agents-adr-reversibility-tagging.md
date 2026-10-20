# ADR Reversibility Tagging

## Summary

**One-sentence:** Tags every ADR with one-way-door vs two-way-door reversibility so review depth and approval gates match the cost of being wrong.

**One-paragraph:** Adds a reversibility frontmatter field to every ADR (two_way_door / partial_two_way / one_way_door_costly / one_way_door_irrevocable) plus a rollback_estimate and a pre-mortem for one-way decisions. Reversibility drives approval depth: two-way = solo, one-way = founder/architect sign-off with cool-off. Output is a tagged ADR plus a review-gate routing record.

**Ефективно для:**

- паст-готова основа для повторюваної задачі 'ADR reversibility tagging' — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- you use ADRs (MADR, Nygard, or similar lightweight format).
- multiple people contribute architecture decisions, OR you author ≥5 ADRs per quarter.
- decisions vary in cost-of-reversal (some easy, some hard).
- you have a code review process where ADRs can carry tags.

## Skip If (ANY kills it)

- no ADRs in use yet — start with `architecture-decision-records` first.
- single-developer pet project with no audit trail need — overkill.
- regulatory environment requires all decisions to go through full board review — tagging adds no signal.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| ADR format with frontmatter | yaml/markdown | repo ADR directory |
| Reversibility-to-approval mapping | config | engagement charter |
| Rollback-cost definition | doc | team operations playbook |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/architecture-decision-records` | Provides the base ADR format this tag extends. |
| `pro/dev/software-architect/adr-staleness-audit` | Counterpart: staleness audit uses reversibility to prioritize re-review. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology fallback | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the tagged ADR + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure: pre-check → estimate rollback → tag → pre-mortem → route gate | ~700 |
| `content/05-examples.xml` | medium | Worked example: tagging a payment-processor ADR as one_way_door_costly | ~600 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `tag-reversibility-per-adr` | sonnet | Bounded classification, 4-way enum. |
| `pre-mortem-synthesis` | sonnet | Generate 'what would cause us to reverse' list. |
| `cross-adr-reversibility-audit` | opus | Spot patterns (e.g., 10 vendor-lock decisions tagged two-way). |

## Templates

| File | Purpose |
|------|---------|
| `templates/adr-with-reversibility.md.j2` | ADR template with reversibility frontmatter populated. |
| `templates/adr-with-reversibility.md` | ADR template with reversibility frontmatter populated. Generated from `templates/adr-with-reversibility.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-adr-reversibility-tagging.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[architecture-decision-records]]
- [[decision-tree-architecture-style]]
- [[decision-tree-build-vs-buy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
