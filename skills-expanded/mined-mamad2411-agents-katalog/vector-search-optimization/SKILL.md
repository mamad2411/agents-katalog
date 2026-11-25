---
name: vector-search-optimization
description: Vector search optimization — HNSW, IVF, quantization, hybrid search
triggers: [vector search, similarity search, HNSW, embeddings, vector database, ANN]
---

# SKILL: Vector Search Optimization

## Index Types

### HNSW (Hierarchical Navigable Small World)
```python
import hnswlib

# Create HNSW index
index = hnswlib.Index(space='cosine', dim=1536)

# Initialize index
index.init_index(max_elements=100000, ef_construction=200, M=16)

# Add vectors
index.add_items(vectors, ids)

# Search (fast approximate)
labels, distances = index.knn_query(query_vector, k=5)
```

### IVF (Inverted File Index)
```python
import faiss

# Create IVF index
quantizer = faiss.IndexFlatL2(1536)
index = faiss.IndexIVFFlat(quantizer, 1536, 100)  # 100 clusters

# Train index
index.train(training_vectors)

# Add vectors
index.add(vectors)

# Search
index.nprobe = 10  # Search 10 clusters
distances, ids = index.search(query_vector, k=5)
```

## Quantization (Reduce Memory)

```python
# Product Quantization (compress 1536D → 64 bytes)
index = faiss.IndexPQ(1536, 64, 8)  # 64 subspaces, 8 bits each

index.train(vectors)
index.add(vectors)

# 24x memory reduction with ~5% accuracy loss
```

## Hybrid Search (Vector + Keyword)

```python
def hybrid_search(query, top_k=5):
    # 1. Vector search
    query_vec = embed([query])[0]
    vector_results = index.search(query_vec, top_k * 2)
    
    # 2. Keyword search (BM25)
    keyword_results = bm25_index.search(query, top_k * 2)
    
    # 3. Combine scores (RRF - Reciprocal Rank Fusion)
    combined_scores = {}
    for rank, doc_id in enumerate(vector_results):
        combined_scores[doc_id] = 1 / (60 + rank)
    
    for rank, doc_id in enumerate(keyword_results):
        combined_scores[doc_id] = combined_scores.get(doc_id, 0) + 1 / (60 + rank)
    
    # Return top k
    top_docs = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
    return [doc_id for doc_id, score in top_docs]
```

## Quality Checks
- [ ] Index type chosen (HNSW for speed, IVF for scale)
- [ ] Quantization if memory-constrained
- [ ] Hybrid search for better recall
- [ ] Index parameters tuned (ef_construction, M, nprobe)
- [ ] Recall measured (vs brute-force baseline)
- [ ] Latency tested (p50, p95, p99)
- [ ] Index rebuild strategy (how often)
- [ ] Incremental updates supported
