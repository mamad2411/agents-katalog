# LLM Hallucination Test Patterns

## Summary

**One-sentence:** Catalogs 6 hallucination test patterns (fact_probes / grounding_required / refusal_correctness / citation_verification / contradiction_tests / off_topic_rejection) and packages each as a CI-gated test class with anchored gold labels.

**One-paragraph:** Catalogs 6 hallucination test patterns (fact_probes / grounding_required / refusal_correctness / citation_verification / contradiction_tests / off_topic_rejection) and packages each as a CI-gated test class with anchored gold labels. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- RAG / agent / extraction feature shipping до production.
- Hallucination — top-3 failure mode на customer-visible AI flows.
- Test-pattern reuse: 6 universal patterns → applicable до 80% AI features.
- CI gate: hallucination-rate >X% blocks merge.

## Applies If (ALL must hold)

- AI feature ships LLM output to end users (RAG / agent / extraction / summary).
- Hallucination is in top-3 known failure modes for the feature.
- Human SMEs available to author gold labels.
- CI can run the test suite on PR.

## Skip If (ANY kills it)

- Non-LLM features (deterministic NLP, search ranking with no generation).
- Creative-content output without consensus correctness.
- Existing eval framework already enforces hallucination coverage.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Per-pattern rubric document | Markdown | QA lead |
| Human SME availability for gold labels | calendar / roster | Team |
| Feature input + grounding sources | JSONL | Eng team |
| CI gate config | YAML | Infra team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/ai/qa-engineer/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-llm-hallucination-test-patterns` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/test-case.py` | Python test-case scaffold (pytest-style) wired to the output contract |
| `templates/suite-config.yaml` | Suite-level config: per-attack-class or per-pattern coverage thresholds |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-llm-hallucination-test-patterns.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- Parent: `pro/ai/qa-engineer/AGENTS.md`
- [[golden-set-curation-and-maintenance]]
- [[prompt-injection-test-suite]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
