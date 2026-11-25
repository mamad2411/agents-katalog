---
name: vector-toolkit
description: Consolidated toolkit for vector. Covers vector-index-tuning, vector-database-engineer
---
# Vector Toolkit

## Use this skill when
- Balancing recall vs speed
- Building RAG (Retrieval Augmented Generation) systems
- Building image/audio similarity search
- Creating recommendation engines
- Implementing quantization
- Implementing semantic search over documents
- Optimizing memory usage
- Optimizing vector search latency and recall
- Reducing search latency
- Scaling to billions of vectors
- Scaling vector operations to millions of vectors
- Tuning HNSW parameters

## Do not use this skill when
- The task is unrelated to vector database engineer
- You lack workload metrics or ground truth to validate recall
- You need a different domain or tool outside this scope
- You need end-to-end retrieval system design beyond index tuning
- You only need exact search on small datasets (use a flat index)

## Core Capabilities
# Vector Toolkit

# Vector Index Tuning

Guide to optimizing vector indexes for production performance.

## Safety

- Avoid reindexing in production without a rollback plan.
- Validate changes under realistic load before applying globally.
- Track recall regressions and revert if quality drops.

## Resources

- `resources/implementation-playbook.md` for detailed patterns, checklists, and templates.

---

# Vector Database Engineer

Expert in vector databases, embedding strategies, and semantic search implementation. Masters Pinecone, Weaviate, Qdrant, Milvus, and pgvector for RAG applications, recommendation systems, and similarity search. Use PROACTIVELY for vector search implementation, embedding optimization, or semantic retrieval systems.

## Capabilities

- Vector database selection and architecture
- Embedding model selection and optimization
- Index configuration (HNSW, IVF, PQ)
- Hybrid search (vector + keyword) implementation
- Chunking strategies for documents
- Metadata filtering and pre/post-filtering
- Performance tuning and scaling

## Workflow

1. Analyze data characteristics and query patterns
2. Select appropriate embedding model
3. Design chunking and preprocessing pipeline
4. Choose vector database and index type
5. Configure metadata schema for filtering
6. Implement hybrid search if needed
7. Optimize for latency/recall tradeoffs
8. Set up monitoring and reindexing strategies

## Best Practices

- Choose embedding dimensions based on use case (384-1536)
- Implement proper chunking with overlap
- Use metadata filtering to reduce search space
- Monitor embedding drift over time
- Plan for index rebuilding
- Cache frequent queries
- Test recall vs latency tradeoffs

---
