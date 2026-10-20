# EU AI Act Compliance (2026)

## Summary

**One-sentence:** Implements an end-to-end EU AI Act compliance workflow — risk classification, model cards, bias detection, explainability, human-oversight gates, and regulatory documentation — to meet the high-risk-system and Article 50 obligations enforceable on 2 August 2026.

**One-paragraph:** 2 August 2026 is the next major EU AI Act enforcement milestone: high-risk obligations under Annex III, transparency obligations under Article 50, the public registration database under Article 49, and enforcement powers all become applicable. This methodology drives a compliance pipeline that classifies risk tier, generates model cards / data sheets / conformity assessments, runs Fairlearn/AIF360 bias checks, produces SHAP/LIME explanations where applicable, and enforces a hard human-legal-review gate before any document leaves the system.

**Ефективно для:** будь-яких AI-систем, що обслуговують користувачів у ЄС — від чат-ботів і recommender-движків до агентських систем, що торкаються біометрії, працевлаштування, кредиту чи критичної інфраструктури.

## Applies If (ALL must hold)

- Any AI system operates in or serves users in the EU (regardless of provider's country of incorporation).
- Chatbots, recommendation engines, or automated-decision systems are marketed in the EU.
- Agent systems touch biometrics, employment, credit, education, or critical infrastructure.
- A GPAI integration is subject to copyright and transparency obligations.
- An audit pipeline must be ready before the 2 August 2026 deadline.

## Skip If (ANY kills it)

- Purely internal R&D tools with no user-facing deployment.
- AI systems deployed exclusively outside EU jurisdictions with no EU data subjects.
- Spam filters, games, or scientific research tools in the "minimal risk" category.
- Prototypes under active development not yet in production.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| System description | Markdown / structured fact sheet | Product team |
| Deployment context | Country list, user types, domain | Legal / GTM team |
| Eval dataset for bias checks | CSV with sensitive-attribute columns | Data engineering |
| Training-data lineage | Lineage record with copyright opt-out flags | Data engineering |
| Reviewer roster | Identity of the human with legal competence who signs off | Compliance lead |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `field-descriptions-as-prompts` | Compliance prompts must precisely instruct the model on field meanings. |
| `handoff-id-payload` | The multi-agent compliance pipeline hands off classifier → docgen → reviewer with task IDs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Six testable rules: classify-first, human-gate, version-artefacts, no-hallucinated-articles, re-classify-on-change, GDPR-parallel-track | ~1100 |
| `content/02-output-contract.xml` | essential | Schemas for risk-classification, model-card, conformity-assessment, bias-report | ~1100 |
| `content/03-failure-modes.xml` | essential | Hallucinated articles, classification drift, missing human gate, surrogate explanations | ~900 |
| `content/04-procedure.xml` | recommended | Six-step pipeline: classify → docgen → bias-check → explainability → human review → register | ~1000 |
| `content/05-examples.xml` | recommended | Worked example: high-risk credit-scoring agent compliance | ~800 |
| `content/06-decision-tree.xml` | essential | Risk-tier routing from a system description | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Risk classification | sonnet | Pattern matching on the Annex III enumeration |
| Model card / data sheet draft | sonnet | Structured generation from facts |
| Conformity-assessment review | opus | Long-tail edge cases against Act text |
| Bias-check execution | haiku | Pure Python / library invocation |

## Templates

| File | Purpose |
|------|---------|
| `templates/model_card_skeleton.md` | Markdown skeleton matching the Article 11 technical documentation outline |
| `templates/_smoke-test.json` | Minimum valid risk-classification report for the validator |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-eu-ai-act-compliance.py` | Validates a risk-classification report against the schema | After every classifier run, before passing to docgen |

## Related

- [[handoff-id-payload]]
- [[idempotent-write-tools]]
- [[discriminated-union-output]]

## Decision tree

See `content/06-decision-tree.xml`. The root question asks whether the system or any of its features falls under Annex III enumeration of high-risk uses. Branches then route to "prohibited" (unacceptable risk, must halt), "high-risk" (full Annex III obligations), "limited" (Article 50 transparency only), or "minimal" (no obligation beyond ordinary engineering practice). Each leaf maps to a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/_smoke-test.json`

```json
{
  "_purpose": "smallest valid risk-classification report",
  "_consumes": "nothing",
  "_produces": "example output matching content/02-output-contract.xml",
  "_depends_on": "content/01-core-rules.xml",
  "_token_budget_impact": "~120 tokens",
  "risk_tier": "high",
  "applicable_articles": [
    "Article 6",
    "Article 11"
  ],
  "rationale": "Smoke fixture: employment-screening agent falls under Annex III point 4.",
  "requires_conformity_assessment": true,
  "reviewer_signoff": {
    "reviewer_id": "legal-lead-smoke",
    "signed_at": "2026-05-22T10:00:00Z"
  }
}
```
