---
name: am-literature-rag
description: Answer additive-manufacturing questions from the user's own library of papers and textbooks with page-cited evidence — ingest PDFs, chunk and index them, retrieve the most relevant passages (BM25 or the all-mpnet-base-v2 dense model, fused), and write grounded answers that say when the library does not cover the question. Based on AMGPT (Barati Farimani Lab). Use for literature questions on L-PBF, DED, melt pools, defects or alloys, building a lab knowledge base, or checking what a set of papers actually says.
---

# AM literature RAG (AMGPT)

AMGPT (Chandrasekhar et al., *Additive Manufacturing Letters* 11 (2024) 100232) showed that a
mid-size model reading a curated library gives specific, citable answers to metal-AM questions
that general chatbots answer vaguely. Its stack:
- PDFs converted to TeX with Mathpix
- LlamaIndex chunking
- `all-mpnet-base-v2` embeddings
- cosine top-k retrieval
- Llama2-7B generation

Here **you** are the generator and `scripts/amrag.py` is the retriever. Every passage it returns
carries a `[short title, p.N]` citation.

## Workflow
1. **Build the library.**
   ```bash
   python scripts/amrag.py ingest ~/papers/*.pdf --index lib/      # incremental; dedups by file hash
   python scripts/amrag.py list --index lib/
   ```
   - Text comes from `pdftotext` (poppler) when it is installed, otherwise from `pypdf`.
   - Chunks are about 220 words with 40 words of overlap, and never cross a page boundary, so
     page citations are exact.
   - Reference lists are dropped.
   - For scanned PDFs, OCR them first (e.g. `ocrmypdf`).

   No papers yet? `python scripts/amrag.py reading-list --topic "melt pool"` prints the AMGPT
   corpus (55 titles with DOIs and topics, MIT-licensed metadata from the authors' repo). The user
   downloads what their library has access to.
2. **Retrieve, then answer.** For each question:
   ```bash
   python scripts/amrag.py query "how does hatch spacing affect lack-of-fusion porosity?" --index lib/ --k 5 [--per-doc 2]
   ```
   Read the passages and write the answer **only from them**:
   - Cite each claim with the `cite` string, for example `[ThermoPore: Predicting part porosity…, p.4]`.
   - If the passages don't answer the question, say "the library doesn't cover this". Then answer
     from general knowledge, **clearly labelled as such**, or ask for the paper.
   - When sources disagree, give both views with their citations.
   - Quote numbers exactly as written (units included). Don't round or convert silently.
3. **Tune.** AMGPT found that a **small top-k and low sampling temperature** gave the most faithful
   answers. Start at `--k 5`. Raise it only for survey-style questions, and then use `--per-doc 2`
   so a single paper can't dominate the results.

## Retrievers
- `--backend hybrid` (default): reciprocal-rank fusion of BM25 and dense, when
  `sentence-transformers` and the Hugging Face model are reachable. Otherwise it falls back to BM25
  and reports `bm25 (dense unavailable)`.
- `--backend dense`: AMGPT's `all-mpnet-base-v2` (768-d, cosine). Embeddings are cached in
  `lib/dense.npy`.
- `--backend bm25`: no model download. Strong on exact terms (alloy names, units, symbols), weaker
  on paraphrases.

## Check the retriever on your own library
Write questions with the file they should come from and a phrase the right passage must contain
(see `examples/questions_lab.json`), then run:
```bash
python scripts/amrag.py eval my_questions.json --index lib/ --k 3
```
- On the 13 lab papers in this repo's tutorials, BM25 alone found the right passage for 11 of 12
  questions at k = 3.
- The one miss was a paraphrase: "unsafe commands" against the paper's "unintended shutdowns".
  That kind of miss is what the dense model fixes.

## Paper facts worth repeating
- AMGPT's RAG system answered **80%** of its expert-graded prompts factually without
  hallucination, against **86.7%** for GPT-4. Its answers were more specific, from a model with
  under 0.5% of GPT-4's parameters.
- The system can also pull 10 full-text papers per query from the ScienceDirect Search API. This
  skill doesn't call that API (it needs a key and an institutional entitlement), but the user can
  download those papers and `ingest` them.

Cite: Chandrasekhar et al., AMGPT, *Addit. Manuf. Lett.* 11 (2024) 100232; code and corpus list
github.com/BaratiLab/LLM_RAG (MIT).
