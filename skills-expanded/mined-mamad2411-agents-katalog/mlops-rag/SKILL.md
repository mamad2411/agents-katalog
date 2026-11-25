---
name: mlops-rag
description: MLOps for RAG systems — model versioning, A/B testing, embedding pipelines, vector DB comparison, evaluation, observability, and continuous delivery for retrieval-augmented generation.
origin: AI Dev Kit
---

# MLOps for RAG Systems

End-to-end MLOps practices tailored to retrieval-augmented generation (RAG) pipelines: model and artifact versioning, A/B testing, embedding management, evaluation frameworks, observability, and continuous evaluation.

## When to Use

- Building or operating a RAG system in production with SLAs on accuracy, latency, and cost
- Need to version, compare, and roll back embedding models, retrievers, or LLM prompts
- Running A/B tests or canary deployments on retrieval strategies, chunking, or prompt variants
- Setting up continuous evaluation gates to catch regressions before they reach users
- Instrumenting RAG pipelines for drift detection, latency monitoring, and hallucination tracking

## Core Concepts

### 1. Model & Artifact Versioning

**MLflow Models** — version retrievers, rerankers, and LLM wrappers as MLflow models with signatures.

```python
import mlflow
from mlflow.models.signature import ModelSignature, infer_signature

class RAGRetriever(mlflow.pyfunc.PythonModel):
    def __init__(self, embedding_model, vector_store):
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    def predict(self, context, model_input: pd.DataFrame) -> pd.DataFrame:
        queries = model_input["query"].tolist()
        embeddings = self.embedding_model.encode(queries)
        results = [self.vector_store.search(e, top_k=5) for e in embeddings]
        return pd.DataFrame({"contexts": results})

signature = ModelSignature(
    inputs=infer_signature(pd.DataFrame({"query": ["test"]})),
    outputs=infer_signature(pd.DataFrame({"contexts": [[]]}))
)

with mlflow.start_run(run_name="retriever-v3"):
    mlflow.pyfunc.log_model(
        artifact_path="retriever",
        python_model=RAGRetriever(embed_model, vector_store),
        signature=signature,
        conda_env={"pip": ["sentence-transformers", "faiss-cpu"]},
    )
    mlflow.log_params({"chunk_size": 512, "top_k": 5, "embedding_model": "all-MiniLM-L6-v2"})
```

**W&B Artifacts** — track embedding checkpoints and vector store snapshots.

```python
import wandb

run = wandb.init(project="rag-pipeline", job_type="embeddings")
artifact = wandb.Artifact("embedding-checkpoint", type="model")
artifact.add_file("models/chunk-embed-v2.pt")
artifact.metadata = {"model": "text-embedding-3-small", "dim": 1536}
run.log_artifact(artifact)
```

**DVC** — version raw documents, chunked data, and generated embeddings.

```bash
dvc init
dvc add data/raw_documents/
dvc add data/chunks/chunked.jsonl
dvc add data/embeddings/embeddings.npy
git add data/*.dvc .gitignore
git commit -m "Track RAG data artifacts"
```

### 2. A/B Testing Strategies

| Strategy | Use Case | Rollout |
|----------|----------|---------|
| **Traffic Splitting** | Compare two retrievers head-to-head | 50/50 → 80/20 |
| **Canary** | Deploy new chunking to 5% of traffic | 5% → 25% → 100% |
| **Shadow Mode** | Run new retriever in parallel, no user impact | Log results for comparison |

```python
# Shadow mode — run both retrievers, log comparison
def shadow_mode_evaluate(query, current_retriever, candidate_retriever):
    current_ctx = current_retriever.retrieve(query)
    candidate_ctx = candidate_retriever.retrieve(query)

    # Log to experiment tracking
    mlflow.log_metrics({
        "current_context_count": len(current_ctx),
        "candidate_context_count": len(candidate_ctx),
        "overlap_ratio": len(set(current_ctx) & set(candidate_ctx)) / max(len(current_ctx), 1),
    })
    # Always return current for users
    return current_ctx
```

### 3. Embedding Pipeline Patterns

**Model Selection Matrix**:

| Model | Dim | Max Tokens | Best For |
|-------|-----|-----------|----------|
| text-embedding-3-small | 1536 | 8191 | Cost-sensitive, general-purpose |
| text-embedding-3-large | 3072 | 8191 | High-accuracy, enterprise RAG |
| all-MiniLM-L6-v2 | 384 | 256 | On-prem, low-latency retrieval |
| e5-large-v2 | 1024 | 512 | Open-source, multilingual |
| bge-large-en-v1.5 | 1024 | 512 | Best open-source English retrieval |

**Chunking Strategy Selection**:

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter, SemanticChunker

# Token-aware chunking with overlap
token_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=128,
    separators=["\n\n", "\n", ". ", " ", ""],
)

# Semantic chunking (sentence embeddings + breakpoint detection)
semantic_splitter = SemanticChunker(
    embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=65,
)
```

**Hybrid Search** (dense + sparse):

```python
from rank_bm25 import BM25Okapi
import numpy as np

class HybridRetriever:
    def __init__(self, dense_store, bm25_index, dense_weight=0.7):
        self.dense_store = dense_store
        self.bm25 = bm25_index
        self.dense_weight = dense_weight

    def retrieve(self, query: str, top_k: int = 5):
        dense_results = self.dense_store.search(query, top_k=top_k * 2)
        sparse_scores = self.bm25.get_scores(query.split())
        # Normalize and combine scores
        combined = self._reciprocal_rank_fusion(dense_results, sparse_scores)
        return combined[:top_k]
```

**Semantic Caching** — avoid redundant LLM calls for semantically identical queries:

```python
import faiss
import hashlib

class SemanticCache:
    def __init__(self, dim=1536, threshold=0.95):
        self.index = faiss.IndexFlatIP(dim)
        self.threshold = threshold
        self.cache = {}  # faiss_id -> (response, metadata)
        self.embedder = OpenAIEmbeddings(model="text-embedding-3-small")

    def lookup(self, query: str) -> str | None:
        q_emb = self.embedder.embed_query(query)
        scores, ids = self.index.search(np.array([q_emb]), k=1)
        if scores[0][0] >= self.threshold:
            return self.cache[ids[0][0]][0]
        return None

    def put(self, query: str, response: str):
        q_emb = self.embedder.embed_query(query)
        self.index.add(np.array([q_emb]))
        idx = self.index.ntotal - 1
        self.cache[idx] = (response, {"query": query})
```

### 4. Vector DB Comparison Matrix

| Database | Open Source | Managed | Hybrid Search | Metadata Filtering | Multi-Tenancy | Scale |
|----------|:-----------:|:-------:|:-------------:|:------------------:|:-------------:|:-----:|
| **Pinecone** | No | Yes | Yes | Yes | Namespaces | 1B+ |
| **Weaviate** | Yes | Yes | Yes | Yes | Multi-tenant | 100M+ |
| **Milvus** | Yes | Yes | Yes | Yes | Collections | 1B+ |
| **Qdrant** | Yes | Yes | Yes | Payload filters | Collections | 100M+ |
| **Chroma** | Yes | No | Limited | Yes | N/A | 10M |
| **FAISS** | Yes | No | No | No | N/A | 1B+ |
| **pgvector** | Yes | Yes (Supabase) | Via tsvector | Yes | Schemas | 10M |
| **Elasticsearch** | Yes | Yes (Elastic) | Yes (kNN + BM25) | Yes | Indices | 1B+ |

### 5. RAG Evaluation Metrics

| Metric | What It Measures | Formula / Method |
|--------|-----------------|-------------------|
| **Faithfulness** | Does the answer follow the retrieved context? | LLM-as-judge: answer entailed by contexts? |
| **Answer Relevance** | Does the answer address the question? | LLM rates answer-to-question alignment |
| **Context Precision** | Are retrieved contexts relevant to the question? | Relevant docs / Total docs retrieved |
| **Context Recall** | Did we retrieve the documents containing the answer? | Relevant retrieved / Total relevant |
| **Hallucination Rate** | Answer claims not grounded in context | Claim-level fact-checking against contexts |
| **Latency P95** | End-to-end response time | P95 of (retrieval + LLM generation) |

### 6. RAG Evaluation Frameworks

**RAGAS** — comprehensive offline evaluation:

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevance, context_precision
from datasets import Dataset

# Prepare evaluation dataset
data = {
    "question": ["What is the refund policy?", "How do I reset my password?"],
    "answer": ["Refunds are processed within 30 days...", "Go to Settings > Security > Reset..."],
    "contexts": [["Policy doc v3, section 4.2"], ["User guide, section 8.1"]],
    "ground_truth": ["30-day refund window", "Settings > Security > Reset Password"],
}
dataset = Dataset.from_dict(data)

result = evaluate(dataset, metrics=[faithfulness, answer_relevance, context_precision])
print(result)
```

**DeepEval** — pytest-integrated RAG evaluation:

```python
from deeval import assert_test
from deeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric
from deeval.test_case import LLMTestCase

def test_rag_output():
    test_case = LLMTestCase(
        input="What is the refund policy?",
        actual_output="Refunds are processed within 30 days of purchase.",
        retrieval_context=["All purchases are eligible for refund within 30 days."],
        expected_output="30-day refund window from date of purchase.",
    )
    faithfulness = FaithfulnessMetric(threshold=0.7)
    relevancy = AnswerRelevancyMetric(threshold=0.7)
    assert_test(test_case, [faithfulness, relevancy])
```

### 7. Observability Stack

| Tool | Strength | Key Features |
|------|----------|-------------|
| **LangSmith** | OpenAI/LangChain native | Trace LLM calls, evaluate datasets, debug chains |
| **Phoenix (Arize)** | Open-source, embeddings | Embedding drift detection, UMAP visualization |
| **WhyLabs** | Production monitoring | Data quality profiles, drift alerts, dashboard |
| **LangFuse** | Open-source, multi-LLM | Session tracking, prompt versioning, cost tracking |

```python
# LangSmith instrumentation
from langsmith import traceable
from langsmith.wrappers import wrap_openai

client = wrap_openai(openai.Client())

@traceable(run_type="retriever")
def retrieve(query: str, top_k: int = 5) -> list[str]:
    """Retrieve context documents for a query."""
    embeddings = embedder.encode(query)
    results = vector_store.search(embeddings, top_k=top_k)
    return [doc.text for doc in results]

@traceable(run_type="chain")
def rag_chain(query: str) -> str:
    contexts = retrieve(query)
    prompt = f"Context:\n{contexts}\n\nQuestion: {query}"
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

### 8. Continuous Evaluation

**Offline Regression Tests** — run on every PR to the RAG pipeline:

```python
# tests/test_rag_regression.py
import pytest
from deeval import evaluate
from deeval.metrics import FaithfulnessMetric

GOLDEN_DATASET = "tests/data/rag_golden.jsonl"

@pytest.fixture(scope="module")
def golden_tests():
    return load_test_cases(GOLDEN_DATASET)

def test_faithfulness_regression(golden_tests):
    metric = FaithfulnessMetric(threshold=0.8)
    results = evaluate(golden_tests, [metric])
    assert results["faithfulness"].score >= 0.8, "Faithfulness dropped below threshold"

def test_pass_at_k(golden_tests):
    """At least K% of queries should have the ground truth in top-N results."""
    pass_count = 0
    for tc in golden_tests:
        results = retriever.retrieve(tc.input, top_k=5)
        if any(gt in results for gt in tc.expected_contexts):
            pass_count += 1
    pass_rate = pass_count / len(golden_tests)
    assert pass_rate >= 0.85, f"pass@5 rate {pass_rate:.2f} < 0.85"
```

**Online Evaluation** — production feedback loop:

```python
# Capture user feedback for online eval
@traceable(run_type="evaluator")
def log_feedback(query: str, response: str, thumbs_up: bool):
    """Log user feedback to evaluation store."""
    mlflow.log_metrics({
        "user_satisfaction": 1.0 if thumbs_up else 0.0,
        "feedback_count": 1,
    })
    # Store for periodic RAGAS evaluation
    feedback_store.append({
        "question": query, "answer": response, "rating": thumbs_up,
    })
```

## Anti-Patterns

- **No baseline retriever** — deploying a RAG system without comparing against BM25-only or keyword search
- **Chunk size not tuned** — using default 512-token chunks without evaluating retrieval quality at different sizes
- **No embedding drift monitoring** — not detecting when source documents change but embeddings are stale
- **Single-metric evaluation** — optimizing only for answer relevance while ignoring faithfulness and hallucination
- **Evaluating with LLM-as-judge on production traffic** — running expensive LLM evaluations synchronously on every request
- **No semantic caching** — paying for identical or near-identical queries repeatedly
- **Hard-coded prompts** — not versioning prompts as artifacts alongside models
- **Skipping shadow mode** — deploying new retriever versions directly to production traffic without validation
- **No golden dataset** — lacking a curated set of QA pairs for regression testing
- **Ignoring latency** — optimizing only for accuracy while P95 latency exceeds SLA

## Best Practices

1. **Version everything**: embedding models, chunking configs, prompts, vector store snapshots, and evaluation datasets
2. **Establish a golden dataset early**: 50-200 QA pairs with ground-truth contexts, updated quarterly
3. **Run offline evals on every PR**: block merges that drop faithfulness or context recall below thresholds
4. **Use shadow mode for new retrievers**: compare candidate vs. current on live traffic before any cutover
5. **Implement semantic caching**: reduce LLM costs 10-30% with a similarity threshold of 0.92-0.97
6. **Monitor embedding drift**: use Phoenix or WhyLabs to track embedding distribution shifts over time
7. **Set SLOs for RAG latency**: e.g., P95 < 3s for retrieval + generation combined
8. **Use hybrid search by default**: dense + sparse retrieval outperforms either alone on most benchmarks
9. **Automate evaluation dataset curation**: mine production queries with low user satisfaction for new test cases
10. **Separate offline and online eval**: offline for PR gates, online for continuous monitoring with user feedback

## Related Skills

- **data-pipelines-ai** — building the ingestion and embedding pipelines that feed RAG
- **openai-api** — LLM API patterns for the generation step of RAG
- **observability-telemetry** — instrumenting RAG spans, metrics, and tracing end-to-end
- **multi-agent-git-workflow** — coordinating parallel development on RAG features
