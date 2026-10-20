# Problem Validation 2026

## Summary

**One-sentence:** 2026 variant of problem validation: 5-step interview opener (Vision → Framing → Weakness → Pedestal → Ask), commitment signal taxonomy (Time / Reputation / Money), Mom Test replacement question table, validation as a recurring weekly loop during discovery.

**One-paragraph:** The 2026 variant supplements the canonical problem-validation methodology with three updates: (1) a 5-step interview opener (Vision-state → Framing-honesty → Weakness-admit → Pedestal-knock → Ask for help) that lowers interviewee performance pressure; (2) a commitment-signal taxonomy tying each evidence tier to observable signal type (Time signals = engagement; Reputation = referrals; Money = pre-orders / contracts); (3) the principle that problem validation is a weekly recurring loop during discovery, not a one-time gate. Output: a validation artefact carrying signals per tier, opener-applied flag, and next-iteration plan.

**Ефективно для:**

- паст-готова основа для повторюваної задачі — без винаходу велосипеда.
- контракт виходу пинить за JSON Schema — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- Discovery sprints that need a weekly cadence rather than a single validation gate.
- Founders whose interview style triggers performance answers from interviewees.
- Replacing legacy lean-startup style validation with current commitment-signal practice (2026 update).

## Skip If (ANY kills it)

- Engagement is post-MVP and the question is feature-prioritisation, not problem-existence.
- Team already runs the canonical problem-validation methodology effectively; the 2026 update adds friction.
- No live discovery loop exists (team can only run interviews once a quarter).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Problem statement draft | one paragraph | founder / PM notes |
| Interview list | recruited segment | audience-segmentation output |
| Cadence commitment | weekly schedule | team calendar |
| Named accountable owner | name + email | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/user-researcher/problem-validation` | canonical methodology this variant extends |
| `solo/ux/user-researcher/pain-point-research` | companion lens for pain evidence |

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
| `templates/problem-validation-2026.json` | JSON skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in fixture used by `validate-problem-validation-2026.py --self-test` |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-problem-validation-2026.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[problem-validation]]
- [[pain-point-research]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, segment scope) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/problem-validation-2026.json`

```json
{
  "artefact_id": "problem-validation-2026-2026-05-23",
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
  "artefact_id": "problem-validation-2026-smoke-2026-05-23",
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
