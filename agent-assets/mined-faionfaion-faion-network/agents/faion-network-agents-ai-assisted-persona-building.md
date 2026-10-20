# AI-Assisted Persona Building

## Summary

**One-sentence:** Builds research-grounded personas from interview transcripts + behavioral data using staged LLM passes with explicit segment criteria and human verification.

**One-paragraph:** Builds research-grounded personas from interview transcripts + behavioral data using staged LLM passes with explicit segment criteria and human verification. The methodology is testable end-to-end: each artefact it produces conforms to the JSON Schema in `content/02-output-contract.xml`, every claim in the body resolves to a rule in `content/01-core-rules.xml`, and the decision-tree in `content/06-decision-tree.xml` routes observable inputs to the right rule.

**Ефективно для:**

- Швидкий перший draft персон з 8-20 інтерв'ю замість 5-day workshop.
- Behavioral-data fusion: інтерв'ю + survey + product signals в одну особу.
- Explicit segment criteria — кожна персона має сегмент-membership rules.
- Verification gate: researcher підписує перед використанням у roadmap.

## Applies If (ALL must hold)

- ≥8 інтерв'ю + behavioral data на ту ж cohort.
- Існує сегментація гіпотеза, яку треба підтвердити/спростувати.
- Researcher доступний для верифікації результату.

## Skip If (ANY kills it)

- < 8 інтерв'ю — недостатньо для статистично значущих сегментів.
- Marketing fluff personas без data backing — це не цей workflow.
- Бренди без segmentation — single-persona shortcut кращий.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| interview transcripts | JSONL | interview platform |
| behavioral signals | CSV/JSON exports | analytics |
| segment hypothesis | YAML candidate segments | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ai-interview-analysis]] | single-interview analysis available |
| [[interview-note-synthesis-ai]] | cross-interview themes available |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure (input/action/output/decision-gate) | 900 |
| `content/05-examples.xml` | essential | One worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule in 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| classify-input | sonnet | Light judgment; identifies branch in decision tree. |
| draft-output | sonnet | Drafting the output artefact per schema. |
| validate-output | haiku | Mechanical schema validation via script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/persona-spec.md` | Persona spec skeleton |
| `templates/personas.json` | Machine-readable personas matching schema |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-assisted-persona-building.py` | Validate output artefact against schema in 02-output-contract.xml | CI on each artefact change; pre-commit |

## Related

- [[ai-interview-analysis]]
- [[interview-note-synthesis-ai]]
- [[ai-coding-of-qualitative-data-protocol]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from the question "Do we have N >= 8 interviews and behavioral data?" and routes observable input signals to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Apply it whenever the input shape changes or before scaling a pilot run.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/personas.json`

```json
{
  "personas": [
    {
      "id": "solo-builder",
      "label": "Solo builder",
      "goals": [
        "ship alone",
        "stay under $200/mo"
      ],
      "pains": [
        "context-loss",
        "auth boilerplate"
      ],
      "segment_rules": [
        "plan_tier in [free, solo]",
        "team_size == 1"
      ],
      "evidence": [
        {
          "source_id": "i01",
          "type": "interview",
          "snippet": "I gave up after auth boilerplate"
        },
        {
          "source_id": "i03",
          "type": "interview",
          "snippet": "I lose context every restart"
        },
        {
          "source_id": "s12",
          "type": "survey",
          "snippet": "Top pain: time on plumbing"
        }
      ]
    }
  ],
  "verified_by": "ruslan@faion.net",
  "interview_count": 14
}
```
