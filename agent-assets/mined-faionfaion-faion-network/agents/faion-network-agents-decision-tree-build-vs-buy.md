# Build vs Buy Decision Tree

## Summary

**One-sentence:** Decide whether to build custom software or buy/adopt a commercial solution by scoring strategic differentiation, TCO, time-to-value, and vendor lock-in.

**One-paragraph:** Build-vs-buy is decided across four axes: strategic differentiation (is this our moat?), TCO over 3 years, time-to-value, and vendor lock-in. The tree forces a scoring across all four; result is a recommendation + rejected alternatives + rollback path. Default: buy non-differentiating capability; build only what carries the moat.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Choice between building a capability or adopting a vendor/OSS is genuine.
- Capability spans ≥1 quarter of engineering time if built.
- ≥1 viable vendor or OSS alternative exists.

## Skip If (ANY kills it)

- No viable vendor/OSS option in the market.
- Capability is core moat with no comparable substitute.
- Throwaway prototype.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Capability charter (what it does, who uses it) | doc | PM |
| 3-year TCO estimate per option | spreadsheet | finance/PM |
| Strategic differentiation assessment | 1-paragraph | founder/architect |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/software-architect/architecture-decision-records` | Result lands as an ADR. |
| `solo/dev/software-architect/adr-reversibility-tagging` | Build-vs-buy choices are often one_way_door_costly. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the decision record + valid/invalid examples | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~800 |
| `content/04-procedure.xml` | medium | 5-step procedure: charter → score → tree → ADR → reversibility tag | ~700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-axes` | sonnet | Per-axis scoring of build vs buy options. |
| `audit-vendor-options` | sonnet | Market scan + viable alternatives. |
| `cross-portfolio-audit` | opus | Spot 'build everything' or 'buy everything' org patterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/build-vs-buy-adr.md.j2` | Build vs Buy ADR template. |
| `templates/build-vs-buy-adr.md` | Build vs Buy ADR template. Generated from `templates/build-vs-buy-adr.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-decision-tree-build-vs-buy.py` | Validate the output artefact against the schema in `content/02-output-contract.xml`. | After subagent returns, before downstream consumer reads. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[architecture-decision-records]]
- [[adr-reversibility-tagging]]
- [[decision-tree-architecture-style]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
