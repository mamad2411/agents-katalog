# AI Governance and Compliance

## Summary

**One-sentence:** EU AI Act + NIST AI RMF aligned governance bundle: risk tier, model card, datasheet, fairness/explainability audit, audit trail, human-oversight plan, retention policy.

**One-paragraph:** Operationalises AI governance into seven concrete artefacts an agent must produce before shipping a production model: (1) risk tier per EU AI Act, (2) model card, (3) datasheet, (4) fairness + explainability audit, (5) immutable audit trail, (6) human-oversight plan, (7) data-retention policy with right-to-deletion path. Each artefact has a template, a verifier, and a named approver.

**Ефективно для:** ML eng + legal-counterpart, що шиплять модель з EU-експозицією і не хочуть платити 35M EUR штрафу, бо «не задокументували».

## Applies If (ALL must hold)

- model lands in production with real users
- any user is in the EU OR model decides about people (credit, hiring, healthcare)
- PII is processed by training or inference
- regulatory exposure (EU AI Act, NIST AI RMF, ISO 42001) is in scope
- a Designated Responsible Individual (DRI) exists

## Skip If (ANY kills it)

- proof-of-concept with no production traffic
- minimal-risk model (spam filter, recommender without legal impact)
- pre-revenue startup with no EU exposure (yet)
- no DRI assigned — governance without ownership is theatre

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Use-case brief | text | Author / owner |
| Tier-manifest entry | JSON | `skills/tier-manifest.json` |
| Eval / fixture data (when applicable) | jsonl | Repo `tests/fixtures/` |
| Named approver | role:person | Org RACI |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/semantic-xml-content` | Authoring shape for `content/*.xml`. |
| `geek/ai/ml-engineer/ai-agent-patterns` | Pattern catalogue for agent loops referenced from this methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with statement + rationale + source | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for produces=spec + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure with input / action / output / decision-gate | ~700 |
| `content/05-examples.xml` | medium | End-to-end worked example | ~500 |
| `content/06-decision-tree.xml` | essential | Root question + branches with `when` observables → conclusion(ref=rule-id) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan-step` | sonnet | Standard reasoning over the procedure / scoring axes. |
| `author-output` | sonnet | Produces the artefact in the shape `produces=spec`. |
| `audit-validate` | haiku | Mechanical schema check via `scripts/validate-ai-governance-compliance.py`. |
| `senior-review` | opus | Cross-artefact judgement on rejection / approval. |

## Templates

| File | Purpose |
|------|---------|
| `templates/model-card.md` | Model card template per Google guidelines |
| `templates/datasheet.md` | Datasheet template per Gebru et al. |
| `templates/fairness-audit.md` | Fairlearn / AIF360 audit report skeleton |
| `templates/audit-trail.sql` | Hash-chained append-only audit table DDL |
| `templates/oversight-plan.md` | Human-oversight plan template |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-governance-compliance.py` | Validate an output artefact against the JSON schema from `content/02-output-contract.xml`. | Pre-merge on the artefact PR + `--self-test` in CI. |

## Related

- [[ai-agent-patterns]] — pattern catalogue this methodology routes through.
- [[agents-production-deployment]] — production gates this methodology feeds into.
- external: rule rationales cite the sources in `content/01-core-rules.xml`.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks the right rule branch for the current task. Branches use observable inputs (numeric / boolean / categorical) and every leaf cites one of `r1-risk-tier-first`, `r2-named-dri`, `r3-audit-trail-immutable`, `r4-fairness-explainability`, `r5-human-oversight` from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/audit-trail.sql`

```sql
-- Minimal append-only audit table for ai-governance-compliance artefacts.
CREATE TABLE IF NOT EXISTS ai_governance_compliance_audit (
    id BIGSERIAL PRIMARY KEY,
    produced_at TIMESTAMPTZ NOT NULL,
    owner TEXT NOT NULL,
    approver TEXT NOT NULL,
    payload JSONB NOT NULL,
    hash TEXT NOT NULL
);

-- Forbid UPDATE / DELETE — append-only.
CREATE OR REPLACE RULE no_update AS ON UPDATE TO ai_governance_compliance_audit DO INSTEAD NOTHING;
CREATE OR REPLACE RULE no_delete AS ON DELETE TO ai_governance_compliance_audit DO INSTEAD NOTHING;
```
