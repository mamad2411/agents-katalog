# Use Case Mapping

## Summary

**One-sentence:** Document specific ways users interact with the product to achieve goals: enumerate use cases, name actor + goal + trigger + flow + alternate flows + edge cases, produce a use-case spec artefact downstream design and QA read.

**One-paragraph:** Products get built without a shared understanding of how users will actually use them; features ship disconnected from real workflows, critical paths are missed, edge cases surface only in production. This methodology pins the use-case format (actor, goal, trigger, preconditions, main flow, alternate flows, edge cases, success criteria), enumerates the top use cases per primary actor, and ranks them by frequency × business impact. Output: a use-case spec artefact downstream design, QA, and engineering all anchor on.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за JSON Schema — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Before scoping a new feature when the user flow is not yet shared between design and engineering.
- QA test plan generation — use cases become test cases.
- Onboarding a new engineer who needs the canonical actor / flow map.
- Pre-spec gate when the requirements doc reads as a feature list, not a usage map.

## Skip If (ANY kills it)

- The change is a UI polish / visual refresh — use cases do not change.
- An existing use-case spec < 6 months old already covers the actor set.
- The team is doing pure discovery and does not yet know who the actors are — run audience-segmentation first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Primary actor list | segment doc | audience-segmentation output |
| Product capability inventory | feature list | product spec |
| Named accountable owner | name + email | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/user-researcher/jobs-to-be-done` | jobs supply the actor + goal pairs use cases enumerate |
| `solo/ux/user-researcher/success-metrics-definition` | downstream consumer mapping success criteria to metrics |

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
| `templates/use-case-mapping.json` | JSON skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in fixture used by `validate-use-case-mapping.py --self-test` |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-use-case-mapping.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[jobs-to-be-done]]
- [[success-metrics-definition]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, segment scope) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/use-case-mapping.json`

```json
{
  "artefact_id": "use-case-mapping-2026-05-23",
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
  "artefact_id": "use-case-mapping-smoke-2026-05-23",
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
