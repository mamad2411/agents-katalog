---
name: rag-evaluation
description: "Evaluate retrieval-augmented generation honestly: golden sets, retrieval metrics, groundedness and citation checks, and regression gates that survive model changes."
type: procedural
category: ai
domain: ai
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - evaluate rag pipeline
  - rag retrieval metrics
  - hallucination evaluation rag
  - golden dataset for rag
  - rag regression test
aliases:
  - rag-eval
keywords:
  - rag
  - evaluation
  - retrieval
  - groundedness
  - faithfulness
  - golden-set
  - recall
mcp_servers:
  - filesystem
  - github
source: custom
enabled: true
---

# RAG Evaluation

## Purpose

Evaluate retrieval-augmented generation honestly: golden sets, retrieval metrics, groundedness and citation checks, and regression gates that survive model changes.

## When to Use

- A RAG system changes and nobody can say whether quality improved.
- Retrieval returns plausible text but answers are ungrounded.
- A model or embedding upgrade needs a before/after comparison.

## When NOT to Use

- There is no labelled data and no budget to create any.
- The system has no retrieval step.
- The question is latency or cost only.

## Capabilities

- Build a golden set with graded relevance and realistic questions.
- Measure retrieval separately from generation.
- Score groundedness against retrieved context, not against a reference answer alone.
- Gate changes on metric deltas with confidence, not single runs.
- Track cost and latency alongside quality.

## Inputs

- A corpus and a set of questions with known good sources.
- The retrieval configuration: chunking, embedding model, top-k, reranking.
- The quality bar the product actually needs.

## Workflow

1. Collect 50–200 real questions and label the passages that answer them.
2. Compute retrieval recall@k and MRR before touching generation.
3. Score answers for groundedness, completeness and citation correctness on a rubric.
4. Run each configuration three times; report variance, not one number.
5. Gate merging on a minimum delta with a confidence interval.
6. Store the run artifacts so a regression can be bisected later.

## Tools

- ragas
- pytest
- numpy
- langsmith

## Examples

- `Recall@10 of 0.62 with perfect groundedness means the model is fine and the retriever is not.`
- `A single-run 3% win is noise; with n=3 runs you need the interval to exclude zero.`

## Safety

- Never evaluate on the same questions used for prompt tuning; hold out a split.
- Judge models inherit their own biases — calibrate against human labels.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `filesystem` | stdio | core | low | — |
| `github` | http | standard | medium | `GITHUB_PERSONAL_ACCESS_TOKEN` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/ai/rag-evaluation`). First-party skill, maintained in this repository.

## Notes

- Retrieval metrics are cheap and stable; generation metrics are expensive and noisy.
- Report per-question failures, not just aggregates, or nobody acts on them.
- Pairs with: `mlops`, `model-drift-monitoring`.
