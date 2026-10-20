---
name: llm-retrieval
description: "Evaluate chunking, ranking, filters, and retrieval recall separately. Use to diagnose candidate generation/ranking failures; llm-rag covers the whole answer pipeline."
---

# llm-retrieval

Evaluate chunking, ranking, filters, and retrieval recall separately.

## Choose this workflow

Use to diagnose candidate generation/ranking failures; llm-rag covers the whole answer pipeline.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [LLMs and retrieval methods](../../references/packs/llm.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; query set, relevance judgments, corpus/index versions, and retrieval configuration.

**Pack prerequisites:** Task definition, model/provider configuration, representative permitted data, versioned prompts/corpus where relevant, and explicit token/cost/latency limits for remote calls. Use current provider interfaces during implementation. Retrieved content and model-generated tool arguments remain untrusted.

- **Infer from evidence:** Read current prompt/tool schemas, retrieval boundaries, installed SDK/provider config and permitted examples without reading secret values.
- **Reasonable default:** Use mocked calls for local contract tests when remote access is absent; do not infer model quality from mocks.
- **Ask only when needed:** Ask for budget and permitted data/provider before a paid or external run if not already set; local prompt/tool implementation can proceed in apply mode.

Declared evidence requirements: `data.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Chunking, candidate recall, ranking, filters, and retrieval latency; generation quality is separate.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Trace a query through normalization, filters, candidates, ranking and final context using known relevance judgments and stable document IDs.
2. Inspect missed relevant passages, validate access filters independently, and compare bounded configurations under the same judgments.

## Technical method

- **Inspect:** Define a query set with relevant document IDs, access labels, corpus version and ranking budget.
- **Method:** Measure candidate recall before reranking; inspect normalization, chunk boundaries and filters at the first stage losing relevant evidence.
- **Avoid misdiagnosis:** Improving final prose cannot recover a passage never retrieved; aggregate recall can hide access-filter leaks.
- **Check the result:** Include an exact answer split across chunks and a highly relevant forbidden document; verify both relevance and isolation.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [LLMs and retrieval worked example](../../references/examples/llm.md).


## Decision branches

- **When a relevant passage never entered candidates:** Fix that stage before tuning the answer prompt or reranker.

## Deliver and verify

- Stage-level retrieval metrics and recall/error evidence, a failure taxonomy with examples, access-filter checks and matched configuration comparisons.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A missing exception passage is localized to candidate generation or ranking; unauthorized passages are excluded regardless of relevance.

## Stop and recover

- New embedding/index/reranking jobs require cost scope. Weak relevance labels limit metric confidence.

## Example requests

- **Normal (inspect):** Evaluate missed exception passages separately from generation quality.
- **Edge (inspect):** Diagnose a missing exception passage hidden by a metadata filter.
- **Blocked (inspect):** Inspect retrieval traces without starting new embeddings or paid reranking jobs.
