# Value Proposition Design

## Summary

**One-sentence:** Design a value proposition using the Strategyzer Canvas: map customer jobs / pains / gains against products & services / pain relievers / gain creators, score fit, and emit a positioning statement.

**One-paragraph:** Products fail because they do not clearly articulate why a customer should choose them over alternatives. This methodology applies the Strategyzer Value Proposition Canvas: on the customer side map jobs, pains, gains (anchored on JTBD evidence); on the offer side map products & services, pain relievers, gain creators; check fit by pairing each pain to a reliever and each gain to a creator; produce a single positioning statement (Geoffrey Moore format) that downstream marketing and onboarding copy reuse. Output: a canvas + positioning statement spec artefact.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за JSON Schema — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Pre-launch positioning when the team can describe features but not the value to a target segment.
- Quarterly refresh after major segment, feature, or competitor moves.
- Marketing handoff — supplying canonical canvas to copywriters / paid acquisition / sales decks.
- Pivot positioning — when the segment changes and old copy stops converting.

## Skip If (ANY kills it)

- A current canvas < 6 months old exists with the same primary segment.
- The team has no JTBD evidence yet — run JTBD first; a canvas without evidence is fiction.
- The change is an internal-only feature (no customer-facing positioning needed).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| JTBD artefact | customer jobs / pains / gains | jobs-to-be-done output |
| Feature inventory | list with descriptions | product spec |
| Competitor positioning samples | 3-5 examples | competitive-analysis output |
| Named accountable owner | name + email | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/user-researcher/jobs-to-be-done` | supplies the customer-side canvas inputs |
| `solo/ux/ux-researcher/competitive-analysis` | supplies competitor positioning context |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate per step | ~800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end (anonymised) | ~700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `draft-inputs-summary` | haiku | Mechanical template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-instance judgment against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/value-proposition-design.json` | JSON skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in fixture used by `validate-value-proposition-design.py --self-test` |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-value-proposition-design.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[jobs-to-be-done]]
- [[competitive-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, segment scope) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/value-proposition-design.json`

```json
{
  "artefact_id": "value-proposition-design-2026-05-23",
  "owner": "ruslan@faion.net",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "inputs_used": [
    {
      "name": "prerequisite-doc",
      "source": "docs/prereq.md"
    }
  ],
  "sections": [
    {
      "heading": "Context",
      "body": "bounded scope per Applies-If; named owner"
    },
    {
      "heading": "Decision",
      "body": "apply rules from 01-core-rules.xml end-to-end"
    }
  ],
  "decision": "Adopt the methodology as the engagement standard."
}
```

### `templates/_smoke-test.json`

```json
{
  "artefact_id": "value-proposition-design-smoke-2026-05-23",
  "owner": "ruslan@faion.net",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "inputs_used": [
    {
      "name": "smoke-fixture",
      "source": "templates/_smoke-test.json"
    }
  ],
  "sections": [
    {
      "heading": "Context",
      "body": "smoke-test"
    },
    {
      "heading": "Decision",
      "body": "smoke-test"
    }
  ],
  "decision": "smoke-test artefact"
}
```
