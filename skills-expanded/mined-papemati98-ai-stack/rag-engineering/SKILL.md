---
name: rag-engineering
description: Design, audit and evaluate provider-neutral retrieval-augmented generation pipelines from ingest through answer quality, latency and drift. Use for planning and local evaluation; do not upload, deploy or publish automatically.
---

# RAG Engineering

Use this skill for a grounded retrieval system or evaluation covering documents,
chunking, embeddings, retrieval, reranking, generation and monitoring.

## Workflow

1. Define corpus authority, user questions, answer contract and access boundary.
2. Inventory formats, provenance, revisions, permissions, PII and freshness.
3. Specify ingest, normalization, chunking, indexing, retrieval, reranking,
   context assembly, citation and abstention behavior.
4. Build a versioned eval set with gold evidence, adversarial cases and leakage checks.
5. Compare a simple baseline before tuning; report quality, grounding, latency,
   cost and failure modes.
6. Define drift, reindex, rollback and human-review gates. Keep upload, provider
   jobs, deployment and production writes explicitly approved.

## Local evaluation harness

The skill ships a deterministic, **stdlib-only** evaluator that runs against
declared predictions and never executes the system under test.

```powershell
python "<skill-dir>\scripts\evaluate_retrieval.py" validate-corpus --corpus "<corpus.json>"
python "<skill-dir>\scripts\evaluate_retrieval.py" evaluate --corpus "<corpus.json>" --predictions "<predictions.json>" --output "<report.json>"
python "<skill-dir>\scripts\evaluate_retrieval.py" compare --corpus "<corpus.json>" --baseline "<baseline.json>" --candidate "<candidate.json>" --output-dir "<out>"
python "<skill-dir>\scripts\evaluate_retrieval.py" selftest --output-dir "<out>"
python "<skill-dir>\scripts\test_evaluate_retrieval.py" --artifact-root "<fixtures-dir>"
```

The bundled synthetic corpus and stub predictions live under
[`fixtures/`](fixtures/README.md); they cover current-vs-historical,
superseded source, alias collision, unknown answer, conflicting evidence,
forbidden project citation and duplicate advisory proposals.

See:

- [references/contract.md](references/contract.md) — design / evaluation contract.
- [references/json-schema.md](references/json-schema.md) — JSON schema for the
  corpus, predictions and comparison report.
- [references/sample-report.md](references/sample-report.md) — preserved sample
  of an evaluator run on the bundled corpus.
- [references/trigger-cases.json](references/trigger-cases.json) — activation
  triggers and anti-triggers.
- [scripts/evaluate_retrieval.py](scripts/evaluate_retrieval.py) — the evaluator.
- [scripts/test_evaluate_retrieval.py](scripts/test_evaluate_retrieval.py) — the
  deterministic test suite.
- For a Hub pilot preparation or repair task explicitly assigned in scope, see
  [references/hub-quality.md](references/hub-quality.md). This conditional
  pointer does not create a general retrieval-evaluation trigger.
