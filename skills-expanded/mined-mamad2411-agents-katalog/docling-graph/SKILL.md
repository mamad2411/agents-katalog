---
name: docling-graph
description: "Use when designing/reviewing Docling Graph knowledge-graph workflows: templates, contracts, CLI/API configs, inspect reports, exports, traces. NOT for generic Docling parsing, vector-only RAG, graph DB admin, or ontology-only work."
argument-hint: "[mode] [source-or-template-or-question] [options]"
model: opus
license: MIT
compatibility: "Docling Graph 1.5.x; Python 3.10+; optional provider credentials for LLM-backed extraction"
metadata:
  author: wyattowalsh
  version: "1.1.0"
---

# Docling Graph

Use this skill when the task is specifically about **Docling Graph**: converting documents into typed Pydantic knowledge graphs, reviewing templates, choosing extraction contracts, tuning pipeline configuration, inspecting/debugging extraction runs, and exporting graph outputs.

Do **not** use it for generic Docling document parsing, vector-only RAG, graph database administration, ontology-only modeling with no Docling Graph run, or unrelated PDF tooling.

## Dispatch

Interpret `$ARGUMENTS` as `[mode] [source-or-template-or-question] [options]`. If `$ARGUMENTS` is empty, ask for the minimum missing context instead of assuming a document, provider, or extraction contract.

| $ARGUMENTS pattern | Mode | What to produce |
| --- | --- | --- |
| `plan [documents/domain]` | Plan | End-to-end workflow plan, template strategy, provider/config choices, validation path |
| `template [domain]` | Template | Pydantic graph template or review notes with stable IDs and relationship hints |
| `contract [direct|staged|delta] [domain]` | Contract | Extraction-contract recommendation with schema and pipeline implications |
| `convert [source] [template]` | Convert | CLI/API run recipe with inputs, provider/model overrides, output paths, and validation |
| `api [source] [template]` | API | Python integration using `PipelineConfig` and explicit override fields |
| `inspect [output-path]` | Inspect | HTML/debug inspection workflow for an existing or planned output directory |
| `export [output]` | Export | JSON/CSV/Cypher/NetworkX export and post-export checks |
| `debug [error-or-output]` | Debug | Root-cause path using logs, `debug/trace_data.json`, stage artifacts, and schema checks |
| `batch [folder]` | Batch | Scaling plan for many documents, manifests, retries, idempotency, and QA sampling |
| Natural language | Auto-detect | Classify first, then run the matching mode |
| Empty/unclear | Clarify | Ask for the document type, target graph, run surface, and provider constraints |

### Auto-Detection

1. Mentions `direct`, `staged`, `delta`, extraction contract, structured output, schema enforcement, sparse checks, gleaning, or streaming -> **Contract**.
2. Mentions `inspect`, HTML report, `trace_data.json`, debug artifacts, output directory review, or failed graph mapping -> **Inspect** or **Debug**.
3. Mentions Pydantic models, `BaseModel`, `Field`, relationships, entities, or `edge()` -> **Template**.
4. Mentions command line, `docling-graph convert`, provider/model flags, source file paths, or output directories -> **Convert**.
5. Mentions `PipelineConfig`, `run_pipeline`, Python integration, `provider_override`, `model_override`, or programmatic runs -> **API**.
6. Mentions graph exports, Cypher, Neo4j, NetworkX, CSV, or graph JSON -> **Export**.
7. Mentions folders, many PDFs, retries, throughput, manifests, or QA sampling -> **Batch**.
8. Otherwise ask one concise clarification question before prescribing a workflow.

## Gallery

| User asks | Response pattern |
| --- | --- |
| "Create a template for SEC filings" | Produce Pydantic models with graph ID fields, relationship fields, extraction notes, and a validation checklist. |
| "Should this use staged extraction?" | Compare direct, staged, and delta contracts against schema size, nesting, cardinality, provider limits, and debug cost. |
| "Run this PDF with OpenAI" | Provide a `docling-graph convert` command and API equivalent with provider/model overrides and output checks. |
| "Review this output folder" | Walk `inspect`, graph JSON, `debug/trace_data.json`, stage artifacts, and schema/sparse-check results. |
| "The graph is missing relationships" | Diagnose template relationship modeling, extraction contract, structured-output fallback, gleaning, and graph mapping artifacts. |
| "Export to Neo4j" | Generate export steps plus uniqueness constraints, ID normalization, and relationship-count checks. |

## Workflow

### 1. Classify Scope

Start every response by deciding whether the task is Docling Graph-specific.

- In scope: document-to-typed-knowledge-graph extraction, Pydantic graph templates, `docling-graph` CLI/API runs, extraction contracts, inspect/debug artifacts, and graph exports.
- Out of scope: plain Docling conversion, embeddings-only pipelines, generic LLM extraction, graph database tuning, ontology design without Docling Graph execution.

If out of scope, state the boundary and suggest the closest appropriate skill or workflow.

### 2. Gather Minimal Inputs

Only ask for missing inputs that change the answer:

- Document type and examples: PDF/HTML/DOCX/image, expected length, scanned vs digital, table density.
- Graph target: entities, relationships, IDs, required fields, downstream consumer.
- Template state: none, draft Pydantic model, existing package/module, or failing template.
- Run surface: CLI, Python API, batch job, CI, or notebook.
- Provider constraints: OpenAI, Mistral, Gemini, Watsonx, local Ollama/vLLM/LM Studio, privacy/cost/latency limits.
- Extraction contract: direct, staged, delta, or undecided.
- Debug context: command/API config, output directory, logs, `debug/trace_data.json`, and exact error.

### 3. Choose the Extraction Contract

Docling Graph supports three contract styles. Make the choice explicit for non-trivial workflows.

| Contract | Use when | Main risks | Required checks |
| --- | --- | --- | --- |
| `direct` | Small, stable schemas; limited nesting; provider handles full schema in one pass | Context overflow, weak relationship coverage | Schema fit, sparse-check results, field coverage |
| `staged` | Large templates with clear sections or nested entity groups | Stage boundaries can drop cross-stage links | Stage outputs, root merge rules, relationship counts |
| `delta` | Complex/high-cardinality graphs, weak source ordering, or incremental enrichment | Resolver quality and stable IDs dominate correctness | ID strategy, resolver config, duplicate entity checks |

Structured output and schema enforcement should be preferred when the provider supports it. If unavailable or brittle, document the fallback parser, sparse-check setting, and extra validation pass. Use gleaning for recall-sensitive extraction, and enable LLM streaming when long runs need live progress or cancellation visibility.

### 4. Apply Mode Protocol

#### Plan

Return:

1. Document and graph assumptions.
2. Template outline and stable-ID strategy.
3. Contract choice with direct/staged/delta rationale.
4. CLI/API run surface, provider/model overrides, and structured-output policy.
5. Validation path: template lint, dry run, inspect report, graph invariants, export checks.
6. Operational path: batch manifest, retries, idempotent outputs, traces, and sampled review.

#### Template

Use Pydantic `BaseModel` classes. Prefer:

- Descriptive `Field(..., description=...)` metadata for all extracted fields.
- Stable graph IDs through `model_config = ConfigDict(json_schema_extra={"graph_id_fields": [...]})` or the project-supported equivalent.
- Relationship fields typed as entity models or lists of entity models.
- Explicit relationship semantics with Docling Graph helpers such as `edge()` when available.
- Root models that describe the document-level graph and expose top-level relationship collections.

Avoid:

- Untyped `dict`/`Any` blobs for graph-critical entities.
- Relationship fields with no source evidence or no stable IDs.
- Overly deep list-of-model nesting without a staged/delta contract.
- IDs based only on extraction order, page number, or model-generated labels.

#### Contract

Return a recommendation table with:

- Selected contract and fallback contract.
- Schema changes needed for the contract.
- Pipeline flags/config fields to set.
- Expected debug artifacts and how to inspect them.
- Failure modes that should trigger switching contracts.

Use direct for simple extractions, staged for templates that naturally decompose, and delta when correctness depends on resolving entities/relationships across many observations.

#### Convert

Give both a CLI command and validation follow-up. Keep CLI flag names distinct from API field names.

```bash
docling-graph convert SOURCE_PATH \
  --template TEMPLATE_MODULE:RootModel \
  --output-dir OUTPUT_DIR \
  --provider PROVIDER \
  --model MODEL \
  --extraction-contract direct \
  --schema-enforced-llm \
  --structured-sparse-check \
  --llm-streaming \
  --show-llm-config
```

Then instruct the user to inspect:

- `OUTPUT_DIR/graph.json` or the configured graph artifact.
- `OUTPUT_DIR/debug/trace_data.json` when debug dumping is enabled.
- `docling-graph inspect OUTPUT_DIR` for an HTML review report.
- Relationship counts, orphan entities, duplicate IDs, and required-field coverage.

#### API

Prefer explicit configuration and typed paths:

```python
from pathlib import Path

from docling_graph import run_pipeline
from docling_graph.pipeline import PipelineConfig

from templates.sec import FilingGraph

config = PipelineConfig(
    source=Path("filing.pdf"),
    output_dir=Path("out/filing"),
    template=FilingGraph,
    provider_override="openai",
    model_override="gpt-4.1-mini",
    extraction_contract="staged",
    structured_output=True,
    structured_sparse_check=True,
    llm_streaming=True,
    gleaning_enabled=True,
    gleaning_max_passes=2,
    dump_to_disk=True,
    debug=True,
)

context = run_pipeline(config)
```

When exact upstream API names differ by installed version, inspect the installed docs/help and adapt. Preserve the concept split: provider/model overrides, contract selection, structured-output policy, gleaning, streaming, and debug dumping.

#### Inspect

Use inspect when reviewing an output folder or preparing a debug handoff:

```bash
docling-graph inspect OUTPUT_DIR
```

Review:

- HTML summary for extraction stages, errors, model calls, and graph mapping.
- `debug/trace_data.json` for stage inputs/outputs, fallback paths, structured-output failures, and sparse-check findings.
- Graph artifact for root entity count, relationship count, orphan nodes, duplicate IDs, and missing required fields.
- Provider/model config actually used, not only the intended config.

#### Export

Tie export format to downstream needs:

- JSON: canonical artifact, regression fixtures, API handoff.
- CSV: analyst review, relationship tables, import staging.
- Cypher/Neo4j: graph database load with uniqueness constraints.
- NetworkX: algorithmic checks, connected components, centrality, reachability.

Before export handoff, verify stable IDs, relationship direction, duplicate nodes, and counts against the inspect report.

#### Debug

Debug in this order:

1. Confirm installed `docling-graph` version, Python version, provider credentials, and CLI/API command.
2. Lint the template for root model, stable IDs, field descriptions, relationship types, and contract fit.
3. Reproduce with debug dumping and a small source sample.
4. Inspect `debug/trace_data.json` for structured-output fallback, sparse-check failures, stage/delta resolver misses, and graph mapping errors.
5. Compare source evidence -> extracted JSON -> graph artifact -> export artifact.
6. Propose the smallest fix: template field description, contract switch, provider/model override, gleaning pass, resolver config, or export mapping.

#### Batch

For many documents, specify:

- Manifest format with source path, template, contract, provider/model, output directory, and retry state.
- Idempotent output directories and resumable runs.
- Per-document traces retained for failures only unless compliance requires all traces.
- QA sampling by document class and failure class.
- Aggregate checks: required-field coverage, relationship density, duplicate IDs, provider cost, latency, and fallback rate.

## Helper Scripts

This skill includes optional local helpers:

```bash
uv run python skills/docling-graph/scripts/check-env.py --provider openai --format json
uv run python skills/docling-graph/scripts/lint-template.py path/to/template.py --root FilingGraph --format json
```

The helpers are advisory. They should never replace running the installed `docling-graph` CLI/API and inspecting real outputs.

## References

| Reference file | Load when |
| --- | --- |
| `references/template-design.md` | Creating or reviewing Pydantic graph templates, stable IDs, relationship fields, staged/delta modeling |
| `references/pipeline-configuration.md` | Choosing contracts, provider/model overrides, structured output, gleaning, streaming, debug dumping |
| `references/cli-api-recipes.md` | Writing CLI/API run patterns, inspect workflows, or batch manifests |
| `references/export-graph-management.md` | Planning JSON/CSV/Cypher/NetworkX exports and graph integrity checks |
| `references/debugging.md` | Debugging traces, inspect reports, failed graph mapping, or artifact handoffs |

## Canonical Vocabulary

Canonical terms. Use these exactly:

| Canonical term | Meaning |
| --- | --- |
| `direct contract` | One-pass extraction from source evidence into the root graph schema |
| `staged contract` | Decomposed extraction into stage outputs that are merged into the root graph |
| `delta contract` | Observation-first extraction plus entity/relationship resolution into the graph |
| `structured output` | Provider-supported schema enforcement or equivalent constrained generation |
| `sparse check` | Validation pass that identifies missing or underfilled schema fields |
| `gleaning` | Bounded follow-up passes that improve recall for entities and relationships |
| `inspect report` | Human-readable review surface created from an output directory |
| `trace data` | Debug artifacts such as `debug/trace_data.json` that connect source, extraction, mapping, and graph output |

## Progressive Disclosure

Load references only when the request needs them:

1. Start with this skill body for dispatch, scope, and mode protocol.
2. Open one reference file for the active mode.
3. Open helper scripts only when asked to run local checks or when maintaining the skill.
4. Avoid loading all references for simple scope redirects or one-command answers.

## Scaling Strategy

Scale Docling Graph work by increasing operational controls before increasing model complexity:

| Scope | Strategy |
| --- | --- |
| Small | Validate one representative document with debug dumping and inspect output |
| Medium | Add a manifest, idempotent outputs, retries, and sampled QA |
| Large | Use batch execution with aggregate metrics, trace retention policy, and staged promotion |
| 100+ files | Parallelize by manifest shard only after the single-document invariant suite passes |

1. Validate one representative document with debug dumping and inspect output.
2. Add a manifest for batches with source, template, contract, provider/model, output path, and status.
3. Make outputs idempotent and resumable.
4. Retain traces for failures and sampled successes.
5. Aggregate required-field coverage, relationship density, duplicate IDs, orphan relationships, fallback rate, cost, and latency.
6. Promote to larger batches only after graph invariants pass on the sampled set.

## Validation Contract

Run from this skill directory before declaring changes complete:

```bash
python scripts/check.py
python -m py_compile scripts/check-env.py scripts/lint-template.py
pytest -q tests/test_docling_graph_skill.py
git diff --check
```

Completion criteria:

1. `scripts/check.py` exits 0.
2. Helper scripts compile and focused tests pass.
3. `git diff --check` exits 0.
4. No portable-CLI violations remain under this skill directory.

After changing skill definitions, public descriptions, reference files, or eval behavior, invoke `docs-steward` if available.

## Critical Rules

1. Keep Docling Graph scope narrow; redirect generic parsing or graph database questions.
2. Distinguish CLI flags from Python API fields.
3. Verify IDs, required fields, relationships, and debug/inspect artifacts before claiming graph quality.
4. Prefer structured output/schema enforcement when available, and specify fallback behavior.
5. Choose direct, staged, or delta explicitly for complex templates.
6. Preserve source evidence paths in debug handoffs.
7. Redact secrets from commands, logs, examples, traces, and generated configs.
