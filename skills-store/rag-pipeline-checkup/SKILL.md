---
name: rag-pipeline-checkup
description: "Verify a RAG pipeline end-to-end, chunking, embeddings, retrieval quality, reranking, grounded answers with citations. Use when building or debugging retrieval-augmented generation."
version: 1.0.0
author: Zorost Intelligence
license: MIT
metadata:
  zorost:
    tags: [rag, retrieval, embeddings, citations, build]
    related_skills: [eval-first-development, error-analysis-50]
    program_weeks: [7]
---

# RAG Pipeline Checkup

## 1 · Purpose

Debug a RAG system as five separable stages, so "the answer was wrong" becomes
"retrieval missed the policy section" or "the model ignored the citation", each with
its own fix.

## 2 · When to use

- Building any RAG feature, or when a RAG feature's answers are wrong, ungrounded,
  or stale.
- Before adding complexity (HyDE, hybrid search, graphs) to a pipeline whose basics
  are unmeasured.

## 3 · Inputs

- The document corpus and the chunking code/config.
- A question set: ≥ 20 real questions with the passage that *should* answer each
  (the retrieval golden set, build it with `eval-first-development`).
- The ability to log intermediate stage outputs.

## 4 · Procedure

1. **Chunking.** Print 10 random chunks. Check: each chunk is one topic, carries its
   source and section, and respects the size budget (~300 to 500 tokens with 10 to 15%
   overlap is the default start). Fix splits that cut tables or definitions in half.
2. **Embedding.** Embed three paraphrases of one question. Confirm they retrieve
   each other's chunks, if paraphrases diverge wildly, the embedding model does not
   match the domain. Try a domain-appropriate model before tuning anything else.
3. **Retrieval.** Score the golden set: for each question, is the right passage in
   the top-k? Record recall@5. Below 0.8, fix retrieval before touching generation,
   a model cannot cite what it never saw.
4. **Reranking.** Add a reranker over the top-20 and re-measure recall@5 of the
   reranked top-5. Keep it only if recall rises; record the latency cost either way.
5. **Generation.** Require citations: every factual sentence must reference a
   retrieved chunk ID, and the answer must say "not in the documents" when retrieval
   came back empty. A schema constrains shape, never truth, spot-check that cited
   chunks actually contain the claim.
6. **End-to-end eval.** Score the full pipeline on the question set with the answer
   grader. Record: retrieval recall, answer score, citation precision (sampled).
7. Attribute every failure to exactly one stage. Fix the stage with the most
   failures first. Re-run the full eval after each fix.

## 5 · Anti-rationalization

| Excuse | Answer |
|---|---|
| "The model is bad; let's upgrade the LLM." | Most RAG failures are retrieval failures wearing a generation costume. Measure recall first. |
| "Chunk size doesn't matter much." | It is the highest-leverage knob you own. Measure at two sizes before dismissing it. |
| "Citations slow the model down." | Ungrounded answers cost more than tokens, they cost trust. |
| "It worked in the demo." | Demos use the questions the builder remembers. The golden set uses the ones users ask. |

## 6 · Red flags

- No recall number exists for retrieval alone.
- Chunks lack source metadata, so citations are impossible by construction.
- The answer never says "not in the documents", the model always finds *something*.
- A fix was applied to generation while retrieval recall sat below 0.5.

## 7 · Verify

- recall@5 on the retrieval golden set is recorded, before and after each change.
- The end-to-end answer score is recorded against the same question set.
- A sample of 10 answers has citation precision checked by hand (cited chunk
  actually supports the claim).
- Every known failure is attributed to one stage in the log.

## 8 · ZoroLogistics example

Week 7's policy bot: 20 ops questions ("who approves a refund over $500?") with the
handbook section that answers each. Baseline: recall@5 = 0.65, the chunker split
the approval table across two chunks. Fix: table-aware chunking → recall 0.90,
answer score 0.61 → 0.88 without touching the model. The lesson the pipeline teaches:
retrieval was the ceiling all along.

---
© 2026 Zorost Intelligence LLC · zorost.com
