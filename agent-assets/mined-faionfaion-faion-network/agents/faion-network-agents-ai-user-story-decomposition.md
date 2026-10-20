# AI User Story Decomposition

## Summary

**One-sentence:** Decomposes vague AI-product asks ('add chatbot', 'make it smart') into INVEST-compliant user stories with explicit AI-vs-deterministic boundary, eval criteria (precision/recall/cost/latency), fallback behavior, and golden-set seed.

**One-paragraph:** Decomposes vague AI-product asks ('add chatbot', 'make it smart') into INVEST-compliant user stories with explicit AI-vs-deterministic boundary, eval criteria (precision/recall/cost/latency), fallback behavior, and golden-set seed. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Stakeholder ask is vague ('add AI', 'make it smart') — needs decomposition.
- AI-vs-deterministic boundary не ясний — стейкхолдери думають LLM зробить все.
- Eval criteria для AI-feature: precision/recall/accuracy/cost — потрібно AC.
- Fallback behavior: коли AI fails (low confidence, refusal) — який UX?

## Applies If (ALL must hold)

- Stakeholder ask is vague ('add AI', 'make it smart').
- Production-deploy intent (not research spike).
- BA owns the story and has access to JTBD / stakeholder records.
- Eng team can act on numeric AC and golden seeds.

## Skip If (ANY kills it)

- Deterministic-only story (CRUD, lookup, integration with no LLM in the loop).
- Research spike with no production-deploy plan.
- Story already has measurable spec attached.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Stakeholder ask (raw) | email / transcript / JTBD record | PM / sponsor |
| Existing story template | Markdown / Jira | BA repo |
| Eval AC catalogue (precision / recall / cost / latency) | YAML | ML eng team |
| Golden-set seed template | JSONL | ml-engineering methodology |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/ba/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/05-examples.xml` | essential | Worked example end-to-end (input → output) | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-ai-user-story-decomposition` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec.md.j2` | Markdown spec skeleton — sections + acceptance criteria slots |
| `templates/spec.md` | Markdown spec skeleton — sections + acceptance criteria slots Generated from `templates/spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/spec-instance.json` | Instance of a filled spec (machine-readable mirror) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-user-story-decomposition.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Parent: `pro/ba/AGENTS.md`
- [[ambiguity-contradiction-detector]]
- [[ba-governance]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
