---
name: rag-architecture
description: "RAG reference across all seven layers: chunking decision tree, hybrid retrieval with reciprocal rank fusion, reranking, grounded generation prompts, retrieval and generation metrics, a vector DB performance table, a catalog of production failure modes, and runnable LangChain, pgvector, cross-encoder, and RAGAS patterns. Use when building, tuning, or debugging retrieval-augmented generation."
---

# RAG architecture pattern library

## The 7 layers

1. **Ingestion** — source → parsed text
2. **Chunking** — text → retrievable units
3. **Embedding** — chunks → vectors
4. **Storage** — vectors + metadata
5. **Retrieval** — query → relevant chunks
6. **Generation** — chunks + query → answer
7. **Evaluation** — measure continuously

## Chunking decision tree

```
Content type:
  Code → AST-based chunking (function/class boundaries)
  Markdown → header-based (## sections)
  PDF (layout-rich) → Unstructured/Marker; layout-aware splits
  Plain text → semantic (sentence-aware, ~512 tokens, 10% overlap)
  Conversation logs → message-pair boundaries
  Tabular → row or row-group based
```

Long documents (> 10k tokens): hierarchical chunking. Retrieve child chunks; generate from parent context.

## Hybrid retrieval

```python
def hybrid_retrieve(query, k=20):
    dense = vector_db.search(embed(query), k=k)
    sparse = bm25_index.search(query, k=k)
    return reciprocal_rank_fusion([dense, sparse])
```

RRF formula: score(doc) = sum(1 / (rank_i + 60)) across retrieval methods.

## Reranking

Top-K → reranker → final K':
- Cross-encoder (ms-marco-MiniLM-L-6-v2 or similar): ~50ms for 50 candidates, self-hostable
- Cohere rerank-3: API call, fast, high quality
- ColBERT: late-interaction; high quality, complex deployment
- LLM-as-reranker: highest quality, highest cost; reserve for top 10-20

## Generation prompting

```
Documents:
[doc_1] {chunk_1.text}
[doc_2] {chunk_2.text}
[doc_3] {chunk_3.text}

Question: {query}

Rules:
- Cite each fact with [doc_id]
- If insufficient information: respond "I don't have enough information to answer that."
- Don't add information not in documents.
- Note ambiguity if multiple interpretations.

Answer:
```

## Evaluation metrics

### Retrieval

| Metric | Formula | Target |
|---|---|---|
| Recall@k | (relevant docs in top-k) / (total relevant) | > 0.8 @ k=5 |
| Precision@k | relevant in top-k / k | > 0.6 @ k=5 |
| MRR | mean(1 / rank of first relevant) | > 0.7 |
| NDCG@k | rank-weighted, accounts for partial relevance | > 0.8 |

### Generation

| Metric | What it measures |
|---|---|
| Faithfulness | % claims supported by retrieved chunks (LLM-judge) |
| Answer relevance | Does answer address the query (LLM-judge) |
| Citation accuracy | Do cited doc IDs match the chunks actually used |
| Latency p95 | End-to-end response time |

## Common mistakes catalog

### Hallucinations in production

Causes:
- No refusal instruction → model fills gap with plausible text
- Retrieval returns irrelevant chunks → model uses them anyway
- Chunks span context limit → some context dropped silently
- Generation model too weak to follow citation rule

Fix: stricter prompt, better retrieval, citation enforcement at parse-time.

### "Demo works, production fails"

Often: corpus changed between demo and prod. Re-embed. Check eval on prod corpus, not demo corpus.

### Pure dense retrieval misses exact terms

Hybrid (dense + BM25) catches both. Pure dense fails on rare technical terms, names, codes.

### Retrieval is too slow

- Vector DB index needs tuning (HNSW parameters)
- Query embedding latency adds up (cache common queries)
- Reranking too many candidates (cap at 50-100)

### Reranker is too slow

Switch from cross-encoder to bi-encoder for first-pass, cross-encoder only for top 20.

### Hallucinations when out-of-corpus

The model needs the refusal prompt explicitly. Without it, models almost always answer rather than say "I don't know."

## Vector DB performance reference

| Operation | pgvector | Pinecone | Qdrant |
|---|---|---|---|
| Insert 1M vectors | ~10 min | ~5 min | ~3 min |
| Query (k=10) on 1M | ~50ms | ~30ms | ~25ms |
| Query (k=10) on 100M | ~500ms | ~100ms | ~80ms |
| Update vector | atomic | atomic | atomic |
| Hybrid filter + search | yes (SQL) | yes (filter) | yes (payload filter) |

Numbers approximate; depend on dimensionality + hardware.

## Implementation patterns

Expert patterns for document chunking, embedding pipelines, hybrid search, cross-encoder re-ranking, and RAGAS evaluation.

### Pattern 1: Document Ingestion with Recursive Chunking

Parse and chunk documents with metadata preservation.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.schema import Document
import hashlib
from pathlib import Path

def ingest_documents(file_paths: list[str],
                     chunk_size: int = 512,
                     chunk_overlap: int = 64) -> list[Document]:
    """Load, parse, and chunk documents with source metadata."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )

    all_chunks = []
    for path in file_paths:
        ext = Path(path).suffix.lower()
        if ext == ".pdf":
            loader = PyPDFLoader(path)
        else:
            loader = TextLoader(path, encoding="utf-8")

        docs = loader.load()
        chunks = splitter.split_documents(docs)

        # Enrich metadata
        for i, chunk in enumerate(chunks):
            chunk.metadata.update({
                "source": Path(path).name,
                "chunk_id": i,
                "chunk_hash": hashlib.sha256(chunk.page_content.encode()).hexdigest()[:16],
                "char_count": len(chunk.page_content),
            })
        all_chunks.extend(chunks)

    print(f"Ingested {len(file_paths)} files → {len(all_chunks)} chunks")
    return all_chunks

# Usage
chunks = ingest_documents(["contracts/msa.pdf", "docs/policy.txt"],
                           chunk_size=512, chunk_overlap=64)
```

### Pattern 2: Embedding and Indexing with pgvector

Store document embeddings in PostgreSQL with pgvector.

```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import PGVector
from langchain.schema import Document
import os

CONNECTION_STRING = os.getenv("POSTGRES_CONNECTION_STRING")
COLLECTION_NAME = "legal_documents"

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    dimensions=1536,          # Matryoshka: can reduce from 3072
)

# Create vector store and index documents
vectorstore = PGVector.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name=COLLECTION_NAME,
    connection_string=CONNECTION_STRING,
    pre_delete_collection=False,   # set True to reindex
)

# For retrieval
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 20, "filter": {"source": "msa.pdf"}}
)

# Similarity score threshold
retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"score_threshold": 0.75, "k": 10}
)
```

### Pattern 3: Hybrid Search with BM25 + Dense Vectors

Combine keyword and semantic retrieval with Reciprocal Rank Fusion.

```python
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# Build dense retriever
texts = [doc.page_content for doc in chunks]
metadatas = [doc.metadata for doc in chunks]

vectorstore = Chroma.from_texts(
    texts=texts,
    embedding=OpenAIEmbeddings(model="text-embedding-3-large"),
    metadatas=metadatas,
)
dense_retriever = vectorstore.as_retriever(search_kwargs={"k": 20})

# Build sparse (BM25) retriever
bm25_retriever = BM25Retriever.from_texts(texts, metadatas=metadatas)
bm25_retriever.k = 20

# Hybrid: RRF fusion
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, dense_retriever],
    weights=[0.4, 0.6],   # BM25: 40%, dense: 60%
)

def hybrid_search(query: str, top_k: int = 5) -> list:
    results = ensemble_retriever.get_relevant_documents(query)
    return results[:top_k]

docs = hybrid_search("indemnification clause maximum liability cap")
for doc in docs:
    print(f"[{doc.metadata['source']}] {doc.page_content[:150]}...")
```

### Pattern 4: Cross-Encoder Re-ranking

Re-rank top candidates with a cross-encoder for precision.

```python
from sentence_transformers import CrossEncoder
from langchain.schema import Document

# Load cross-encoder (runs locally, no API cost)
cross_encoder = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2",
    max_length=512,
)

def rerank_documents(query: str, candidate_docs: list[Document],
                     top_n: int = 5) -> list[Document]:
    """Score each (query, doc) pair with cross-encoder; return top_n."""
    pairs = [(query, doc.page_content) for doc in candidate_docs]
    scores = cross_encoder.predict(pairs)

    # Sort by score descending
    ranked = sorted(zip(scores, candidate_docs),
                    key=lambda x: x[0], reverse=True)

    for score, doc in ranked[:top_n]:
        doc.metadata["rerank_score"] = round(float(score), 4)

    return [doc for _, doc in ranked[:top_n]]

# Two-stage retrieval
candidates = hybrid_search(query, top_k=20)   # stage 1: fast, broad
reranked = rerank_documents(query, candidates, top_n=5)   # stage 2: precise

# Or use Cohere Rerank API
import cohere
co = cohere.Client(os.getenv("COHERE_API_KEY"))

def cohere_rerank(query: str, docs: list[Document], top_n: int = 5):
    response = co.rerank(
        model="rerank-english-v3.0",
        query=query,
        documents=[doc.page_content for doc in docs],
        top_n=top_n,
    )
    return [docs[r.index] for r in response.results]
```

### Pattern 5: RAGAS Pipeline Evaluation

Measure retrieval and generation quality with RAGAS metrics.

```python
from ragas import evaluate as ragas_evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_recall, context_precision
from datasets import Dataset
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatAnthropic

# Build RAG chain
llm = ChatAnthropic(model="claude-opus-4-6")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=ensemble_retriever,
    return_source_documents=True,
)

# Prepare evaluation dataset
eval_questions = [
    "What is the maximum liability cap in the MSA?",
    "Under what conditions can the agreement be terminated?",
    # ... 50+ questions for meaningful evaluation
]
eval_ground_truths = [
    "The maximum liability cap is limited to fees paid in the 12 months preceding the claim.",
    "Either party may terminate with 30 days written notice.",
    # ...
]

# Collect RAG outputs
rows = []
for question, ground_truth in zip(eval_questions, eval_ground_truths):
    result = qa_chain({"query": question})
    rows.append({
        "question": question,
        "answer": result["result"],
        "contexts": [doc.page_content for doc in result["source_documents"]],
        "ground_truth": ground_truth,
    })

ragas_dataset = Dataset.from_list(rows)
scores = ragas_evaluate(
    ragas_dataset,
    metrics=[faithfulness, answer_relevancy, context_recall, context_precision]
)
print(scores.to_pandas().mean())
# Target: faithfulness > 0.85, context_recall > 0.80
```

## More anti-patterns

### Anti-Pattern 1: Fixed 512-Token Chunks for All Document Types
Code files split differently than legal contracts. PDFs with tables need table-aware parsing. Markdown should split at headers. Using the same RecursiveCharacterTextSplitter for all document types is lazy and hurts retrieval. Match chunking to document structure.

### Anti-Pattern 2: Vector-Only Retrieval (No Hybrid Search)
Dense vectors miss exact matches: "Section 12.3(b)", "ISO 27001", "RFC 2119". BM25 misses paraphrases and synonyms. Both alone underperform hybrid. Always combine with RRF — it costs nothing extra and consistently improves retrieval by 10-20%.

### Anti-Pattern 3: Evaluating RAG by Reading Outputs
Reading 10 answers and saying "looks good" is not evaluation. Hallucinations are polished and plausible-sounding. Run RAGAS on 50+ labeled questions. Faithfulness < 0.75 means the model is fabricating — regardless of how good the answers read.

### Anti-Pattern 4: Same Embedding Model for Query and Document (When Domain Differs)
Asymmetric retrieval: user queries are short, informal, interrogative. Documents are long, formal, declarative. `e5-mistral-7b-instruct` and `bge-large` are designed for asymmetric retrieval and handle this mismatch. Generic embeddings trained for symmetric tasks underperform.

## Cross-references

- `model-evaluation` plugin — broader eval methodology
- `prompt-engineering` plugin — generation prompt design
- `vector-databases` plugin — DB selection + ops
- `data-pipelines` plugin — ingestion + re-indexing automation
