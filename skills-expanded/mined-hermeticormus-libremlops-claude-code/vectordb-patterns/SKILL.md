---
name: "vectordb-patterns"
description: "Vector database patterns with code: pgvector with an HNSW index, Pinecone namespaces for isolation, Qdrant named vectors and payload filters, FAISS for offline batch indexing, and embedding drift detection with reindexing. Use when storing and searching embeddings."
---

# VectorDB Patterns

Expert patterns for HNSW index tuning, pgvector setup, Pinecone/Qdrant upsert, metadata filtering, multi-tenancy, and embedding drift management.

## Pattern 1: pgvector Setup with HNSW Index

PostgreSQL vector search with proper index configuration.

```sql
-- Install extension (requires PostgreSQL 15+ with pgvector)
CREATE EXTENSION IF NOT EXISTS vector;

-- Table with embedding column
CREATE TABLE documents (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content     TEXT NOT NULL,
    embedding   vector(1536),            -- dimension matches your model
    source      TEXT,
    tenant_id   TEXT NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    metadata    JSONB DEFAULT '{}'
);

-- HNSW index: best recall, higher memory
-- m=16 (connections per node), ef_construction=64 (build quality)
CREATE INDEX idx_docs_embedding_hnsw
ON documents USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Index on tenant_id for filtered queries
CREATE INDEX idx_docs_tenant ON documents (tenant_id);

-- Verify index
SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'documents';
```

```python
import psycopg2
import numpy as np
from openai import OpenAI

client = OpenAI()

def embed(text: str, model: str = "text-embedding-3-large",
          dimensions: int = 1536) -> list[float]:
    response = client.embeddings.create(input=text, model=model,
                                         dimensions=dimensions)
    return response.data[0].embedding

def upsert_document(conn, content: str, tenant_id: str, source: str,
                    metadata: dict = None):
    embedding = embed(content)
    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO documents (content, embedding, source, tenant_id, metadata)
               VALUES (%s, %s, %s, %s, %s)""",
            (content, embedding, source, tenant_id, metadata or {})
        )
    conn.commit()

def search(conn, query: str, tenant_id: str, k: int = 10,
           ef_search: int = 100) -> list[dict]:
    query_embedding = embed(query)
    with conn.cursor() as cur:
        cur.execute(f"SET hnsw.ef_search = {ef_search}")
        cur.execute(
            """SELECT id, content, source,
                      1 - (embedding <=> %s::vector) AS similarity
               FROM documents
               WHERE tenant_id = %s
               ORDER BY embedding <=> %s::vector
               LIMIT %s""",
            (query_embedding, tenant_id, query_embedding, k)
        )
        rows = cur.fetchall()
    return [{"id": r[0], "content": r[1], "source": r[2],
             "similarity": r[3]} for r in rows]
```

## Pattern 2: Pinecone with Namespace Isolation

Production Pinecone with per-tenant namespaces.

```python
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
import uuid

pc = Pinecone(api_key="PINECONE_API_KEY")
oai = OpenAI()

# Create index
INDEX_NAME = "documents"
DIMENSION = 1536

if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

index = pc.Index(INDEX_NAME)

def embed_batch(texts: list[str]) -> list[list[float]]:
    response = oai.embeddings.create(
        input=texts,
        model="text-embedding-3-large",
        dimensions=DIMENSION,
    )
    return [item.embedding for item in response.data]

def upsert_documents(tenant_id: str, docs: list[dict], batch_size: int = 100):
    """Upsert to tenant-specific namespace."""
    vectors = []
    for i in range(0, len(docs), batch_size):
        batch = docs[i:i+batch_size]
        texts = [d["content"] for d in batch]
        embeddings = embed_batch(texts)

        for doc, emb in zip(batch, embeddings):
            vectors.append({
                "id": doc.get("id", str(uuid.uuid4())),
                "values": emb,
                "metadata": {
                    "content": doc["content"][:1000],  # Pinecone metadata size limit
                    "source": doc.get("source", ""),
                }
            })

        index.upsert(vectors=vectors, namespace=tenant_id)
        vectors = []
        print(f"Upserted {min(i+batch_size, len(docs))}/{len(docs)}")

def query_documents(tenant_id: str, query: str, k: int = 10,
                    filter: dict = None) -> list[dict]:
    query_emb = embed_batch([query])[0]
    response = index.query(
        vector=query_emb,
        top_k=k,
        namespace=tenant_id,
        filter=filter,
        include_metadata=True,
    )
    return [{"id": m.id, "score": m.score,
             "content": m.metadata.get("content", "")}
            for m in response.matches]
```

## Pattern 3: Qdrant with Named Vectors and Payload Filtering

Multi-embedding per document with Qdrant.

```python
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams, Distance, PointStruct, Filter, FieldCondition, MatchValue,
    HnswConfigDiff, OptimizersConfigDiff, ScalarQuantization, ScalarType
)
import uuid

client = QdrantClient(url="http://localhost:6333")
COLLECTION = "documents"

# Create collection with named vectors and scalar quantization
client.recreate_collection(
    collection_name=COLLECTION,
    vectors_config={
        "dense": VectorParams(size=1536, distance=Distance.COSINE),
        "sparse_placeholder": VectorParams(size=256, distance=Distance.COSINE),
    },
    hnsw_config=HnswConfigDiff(m=16, ef_construct=100, full_scan_threshold=10000),
    quantization_config=ScalarQuantization(
        scalar=ScalarType.INT8,
        quantile=0.99,
        always_ram=True,
    ),
    optimizers_config=OptimizersConfigDiff(indexing_threshold=20000),
)

def upsert_qdrant(docs: list[dict], batch_size: int = 64):
    for i in range(0, len(docs), batch_size):
        batch = docs[i:i+batch_size]
        points = [
            PointStruct(
                id=doc.get("id", str(uuid.uuid4())),
                vector={"dense": doc["embedding"]},
                payload={
                    "content": doc["content"],
                    "tenant_id": doc["tenant_id"],
                    "source": doc.get("source", ""),
                }
            )
            for doc in batch
        ]
        client.upsert(collection_name=COLLECTION, points=points)

def search_qdrant(query_embedding: list[float], tenant_id: str,
                  k: int = 10) -> list[dict]:
    results = client.search(
        collection_name=COLLECTION,
        query_vector=("dense", query_embedding),
        query_filter=Filter(
            must=[FieldCondition(key="tenant_id",
                                 match=MatchValue(value=tenant_id))]
        ),
        limit=k,
        with_payload=True,
    )
    return [{"id": r.id, "score": r.score,
             "content": r.payload.get("content", "")} for r in results]
```

## Pattern 4: FAISS for Offline Batch Indexing

High-performance offline indexing with FAISS.

```python
import faiss
import numpy as np
import pickle

def build_faiss_index(embeddings: np.ndarray,
                      index_type: str = "hnsw") -> faiss.Index:
    """
    Build FAISS index from embeddings array.
    index_type: 'flat' (exact), 'hnsw', 'ivfpq' (compressed)
    """
    d = embeddings.shape[1]
    embeddings = embeddings.astype(np.float32)

    if index_type == "flat":
        index = faiss.IndexFlatIP(d)     # Inner product (cosine after normalization)
        faiss.normalize_L2(embeddings)
        index.add(embeddings)

    elif index_type == "hnsw":
        index = faiss.IndexHNSWFlat(d, 32, faiss.METRIC_INNER_PRODUCT)
        index.hnsw.efConstruction = 200
        faiss.normalize_L2(embeddings)
        index.add(embeddings)

    elif index_type == "ivfpq":
        quantizer = faiss.IndexFlatL2(d)
        nlist = max(4 * int(np.sqrt(len(embeddings))), 100)
        m_subquantizers = 32          # PQ subquantizers (d must be divisible by m)
        bits_per_code = 8
        index = faiss.IndexIVFPQ(quantizer, d, nlist, m_subquantizers, bits_per_code)
        index.train(embeddings)
        index.add(embeddings)
        index.nprobe = 16

    return index

def search_faiss(index: faiss.Index, query: np.ndarray, k: int = 10,
                 ef_search: int = 100) -> tuple:
    query = query.astype(np.float32)
    faiss.normalize_L2(query.reshape(1, -1))
    if hasattr(index, "hnsw"):
        index.hnsw.efSearch = ef_search
    distances, indices = index.search(query.reshape(1, -1), k)
    return indices[0], distances[0]

# Benchmark recall vs brute force
def compute_recall_at_k(hnsw_index, flat_index, queries, k=10):
    recalls = []
    for q in queries:
        gt_ids, _ = search_faiss(flat_index, q, k=k)
        approx_ids, _ = search_faiss(hnsw_index, q, k=k)
        recall = len(set(gt_ids) & set(approx_ids)) / k
        recalls.append(recall)
    return np.mean(recalls)
```

## Pattern 5: Embedding Drift Detection and Reindexing

Monitor embedding model version and manage reindexing.

```python
import numpy as np
from scipy.stats import ks_2samp
import json
from datetime import datetime

def check_embedding_drift(reference_embeddings: np.ndarray,
                           current_embeddings: np.ndarray,
                           sample_size: int = 1000) -> dict:
    """Detect distribution shift between embedding batches."""
    rng = np.random.default_rng(42)
    ref_sample = reference_embeddings[rng.choice(len(reference_embeddings),
                                                   min(sample_size, len(reference_embeddings)),
                                                   replace=False)]
    cur_sample = current_embeddings[rng.choice(len(current_embeddings),
                                                min(sample_size, len(current_embeddings)),
                                                replace=False)]

    # KS test on mean norm (proxy for distribution shift)
    ref_norms = np.linalg.norm(ref_sample, axis=1)
    cur_norms = np.linalg.norm(cur_sample, axis=1)
    ks_stat, p_value = ks_2samp(ref_norms, cur_norms)

    # Cosine similarity between centroid embeddings
    ref_centroid = ref_sample.mean(axis=0)
    cur_centroid = cur_sample.mean(axis=0)
    centroid_sim = float(np.dot(ref_centroid, cur_centroid) /
                         (np.linalg.norm(ref_centroid) * np.linalg.norm(cur_centroid)))

    return {
        "ks_statistic": round(ks_stat, 4),
        "p_value": round(p_value, 4),
        "centroid_similarity": round(centroid_sim, 4),
        "drift_detected": p_value < 0.05 or centroid_sim < 0.95,
        "checked_at": datetime.utcnow().isoformat(),
    }

def plan_reindex(vector_count: int, embed_rate_per_sec: int = 500,
                 model_name: str = "text-embedding-3-large") -> dict:
    """Estimate reindexing cost."""
    embed_hours = vector_count / embed_rate_per_sec / 3600
    return {
        "vector_count": vector_count,
        "embedding_model": model_name,
        "estimated_embed_hours": round(embed_hours, 2),
        "strategy": "shadow_index",
        "note": "Build new index in parallel; validate recall parity before cutover",
    }
```

## Anti-Patterns

### Anti-Pattern 1: Using Chroma in Production
Chroma is an in-process library with no production SLA, no horizontal scaling, and single-file storage. It is appropriate for local development and prototyping. Any production workload (multi-user, persistent, > 100K vectors) belongs in Pinecone, Qdrant, Weaviate, or pgvector.

### Anti-Pattern 2: Default HNSW Parameters for All Scales
HNSW with M=16, ef_construction=64 at 100K vectors is fine. At 10M vectors, the same parameters produce poor recall because the index is too sparse relative to dataset density. Benchmark recall@10 against exact search before going to production. Tune M and ef_construction to achieve target recall.

### Anti-Pattern 3: No Metadata on Vectors
Storing vectors without source document reference, embedding model version, or ingestion timestamp makes reindexing impossible without re-fetching all source data. Always store: `source_id`, `embedding_model`, `model_version`, `ingested_at`. These are small metadata fields that save days of work during reindexing.

### Anti-Pattern 4: Tenant Isolation via Metadata Filter Only
`WHERE tenant_id = 'X'` is a soft isolation — a bug in query construction leaks all tenants' data. Use namespace-level isolation (Pinecone namespaces, Weaviate multi-tenancy) for hard isolation. Reserve metadata-only filtering for non-sensitive segmentation.
