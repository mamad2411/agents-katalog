---
name: rag-pipeline-architecture
description: Reference architecture for building a Retrieval-Augmented Generation (RAG) system — the indexing pipeline (raw docs → chunk → embed → vector DB) and the query pipeline (question → embed → similarity search → top-K → prompt → LLM → grounded answer), plus the build-order discipline and quality model behind it. Use whenever the user is designing, building, or debugging a RAG system, a "chat with your docs" feature, a retrieval-based AI assistant, or asks why their RAG answers are wrong/ungrounded/missing context. Pairs with the rag-build-order procedure for the sequencing discipline.
---

# RAG Pipeline Architecture

Source: "End-to-End RAG — Write index first → then read evidence" (@hackproduct). A standard two-pipeline architecture for building a retrieval-augmented generation system, plus the discipline and quality model behind it.

## The two pipelines

### 1. Indexing pipeline (offline — build this first)

| Stage | What happens |
|---|---|
| **Raw docs** (e.g. PDF) | Source documents enter the system |
| **Chunk** | Split into text chunks — chunk size/overlap strategy directly determines what a later query can retrieve |
| **Embedding** | Each chunk is embedded into a vector representing its meaning |
| **Vector DB** | Chunk vectors are stored and indexed — index ready for querying |

### 2. Query pipeline (online — runs per user question)

| Stage | What happens |
|---|---|
| **Question** | User's actual intent, as typed |
| **Embedding** | The question is embedded with the *same* embedding model/approach used for the chunks — a mismatch here silently breaks retrieval quality |
| **Search** | Similarity search against the vector DB (retrieve step) |
| **Top K** | The K most similar chunks are selected as retrieved context |

### 3. Augment + Generate

- The **Top-K context** flows into a **Prompt** (context + the original ask).
- The **Prompt** goes to the **LLM** for reasoning.
- The LLM produces an **Answer** — and the answer should **cite the retrieved evidence**, not just narrate from the model's own training knowledge. An ungrounded answer that ignores the retrieved context has defeated the point of building retrieval at all.

## The build-order discipline: write index first, then read evidence

Build and validate the indexing pipeline completely *before* building the query pipeline. The query pipeline is only as good as the index it searches — debugging retrieval quality against an unfinished or unvalidated index wastes effort chasing symptoms in the wrong half of the system. See the `rag-build-order` procedure for the concrete sequence.

## The quality model: RAG quality = chunk quality × retrieval quality

This is multiplicative, not additive — a weak factor on either side caps the whole system regardless of how good the other one is:

- **Chunk quality** (indexing-side): chunks that are too large dilute relevance; too small lose context; wrong split boundaries (mid-sentence, mid-table) produce chunks that don't make sense in isolation.
- **Retrieval quality** (query-side): the embedding model, similarity metric, and K value all affect whether the *right* chunks actually surface for a given question.

When a RAG system produces bad answers, diagnose which factor is failing before changing anything — a poorly-tuned prompt or LLM is rarely the actual problem if either chunk quality or retrieval quality is broken upstream. Improving the LLM prompt cannot fix bad chunks or bad retrieval; it can only make a good retrieval result read better.

## Common failure modes to check first

- **Chunking**: chunks split mid-thought, no overlap between adjacent chunks losing boundary context, or chunk size mismatched to the kind of question being asked (a summary question needs bigger context than a fact-lookup question).
- **Embedding mismatch**: query embedded with a different model/version than the chunks were indexed with.
- **K too small or too large**: too small misses relevant chunks; too large drowns the LLM in irrelevant context and increases the chance the model ignores the right chunk.
- **No citation/grounding check**: the answer doesn't actually reference what was retrieved — a sign the LLM is answering from its own training knowledge instead of the provided context, which defeats the purpose of retrieval.

## Related skills in this repo

- **rag-build-order** (procedure): The concrete step sequence for building/validating the indexing pipeline before the query pipeline, per this skill's core discipline.
- **the-productize-yourself-blueprint** / **saas-idea-validator**: If a RAG feature is part of a new product idea, this skill is the technical-architecture reference once that idea moves toward actual implementation.
- **night-shift-workflow**: If a RAG-based feature runs as part of a scheduled/autonomous workflow (e.g. an overnight document-ingestion job), apply that skill's autonomy-boundary discipline to what the pipeline may do unattended.

## Notes

Source: "End-to-End RAG" diagram video (@hackproduct / TikTok @hackproduct9). Standard RAG architecture terminology (chunking, embeddings, vector DB, top-K retrieval, augment-and-generate) — not vendor- or tool-specific; applies regardless of which vector DB, embedding model, or LLM is actually used.
