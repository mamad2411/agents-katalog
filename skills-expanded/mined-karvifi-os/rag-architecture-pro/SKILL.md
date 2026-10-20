---
name: rag-architecture-pro
description: Production RAG systems — chunking, embeddings, retrieval, reranking, evaluation
triggers: [RAG, retrieval augmented generation, vector search, embeddings, semantic search, document retrieval]
---

# SKILL: RAG Architecture Pro

## RAG Pipeline (5 Core Stages)

```
1. Ingestion → Load & chunk documents
2. Embedding → Convert chunks to vectors
3. Indexing → Store in vector database
4. Retrieval → Find relevant chunks
5. Generation → LLM generates answer using retrieved context
```

## Stage 1: Document Chunking Strategy

```python
from llama_index.core.node_parser import SentenceSplitter

# ❌ BAD: Fixed character chunks (breaks sentences)
chunks = [text[i:i+500] for i in range(0, len(text), 500)]

# ✅ GOOD: Semantic chunking (preserves meaning)
splitter = SentenceSplitter(
    chunk_size=512,  # Target size in tokens
    chunk_overlap=50,  # Overlap to preserve context
    separator=" "
)

chunks = splitter.split_text(document)
```

**Chunking strategies by document type:**
```
Code documentation: Split by function/class
Legal documents: Split by section/clause
Articles: Split by paragraph + heading
Chat transcripts: Split by speaker turn
CSV/Tables: Keep full row context
```

## Stage 2: Embedding Models

```python
from openai import OpenAI

client = OpenAI()

# Generate embeddings
def embed(texts: List[str]) -> List[List[float]]:
    response = client.embeddings.create(
        model="text-embedding-3-small",  # 1536 dimensions
        input=texts
    )
    return [item.embedding for item in response.data]

# Embedding model comparison
models = {
    "text-embedding-3-small": {
        "dimensions": 1536,
        "cost": "$0.02/1M tokens",
        "use": "Most tasks"
    },
    "text-embedding-3-large": {
        "dimensions": 3072,
        "cost": "$0.13/1M tokens",
        "use": "High accuracy needed"
    }
}
```

## Stage 3: Vector Database (pgvector example)

```python
import psycopg2
from pgvector.psycopg2 import register_vector

# Enable pgvector extension
conn = psycopg2.connect("dbname=mydb")
conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
register_vector(conn)

# Create table with vector column
conn.execute("""
    CREATE TABLE documents (
        id SERIAL PRIMARY KEY,
        content TEXT,
        embedding vector(1536),  -- Dimension matches embedding model
        metadata JSONB
    )
""")

# Create index for fast similarity search
conn.execute("""
    CREATE INDEX ON documents 
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100)
""")

# Insert documents
def insert_doc(content: str, embedding: List[float], metadata: dict):
    conn.execute(
        "INSERT INTO documents (content, embedding, metadata) VALUES (%s, %s, %s)",
        (content, embedding, json.dumps(metadata))
    )
```

## Stage 4: Retrieval Strategies

### Basic Similarity Search
```python
def retrieve(query: str, top_k: int = 5) -> List[dict]:
    """Cosine similarity search"""
    query_embedding = embed([query])[0]
    
    results = conn.execute("""
        SELECT content, metadata, 
               1 - (embedding <=> %s) AS similarity
        FROM documents
        ORDER BY embedding <=> %s
        LIMIT %s
    """, (query_embedding, query_embedding, top_k))
    
    return results.fetchall()
```

### Hybrid Search (Keyword + Semantic)
```python
def hybrid_search(query: str, top_k: int = 5) -> List[dict]:
    """Combine full-text search + vector similarity"""
    query_embedding = embed([query])[0]
    
    results = conn.execute("""
        SELECT content, metadata,
               ts_rank(to_tsvector('english', content), plainto_tsquery('english', %s)) AS keyword_score,
               1 - (embedding <=> %s) AS semantic_score,
               (ts_rank(...) * 0.3 + (1 - (embedding <=> %s)) * 0.7) AS combined_score
        FROM documents
        WHERE to_tsvector('english', content) @@ plainto_tsquery('english', %s)
           OR (embedding <=> %s) < 0.5
        ORDER BY combined_score DESC
        LIMIT %s
    """, (query, query_embedding, query_embedding, query, query_embedding, top_k))
    
    return results.fetchall()
```

### Metadata Filtering
```python
def filtered_search(query: str, filters: dict, top_k: int = 5):
    """Filter by metadata before vector search"""
    query_embedding = embed([query])[0]
    
    # Example: Only search documents from last 30 days
    results = conn.execute("""
        SELECT content, metadata
        FROM documents
        WHERE metadata->>'date' > NOW() - INTERVAL '30 days'
          AND metadata->>'category' = %s
        ORDER BY embedding <=> %s
        LIMIT %s
    """, (filters["category"], query_embedding, top_k))
    
    return results.fetchall()
```

## Stage 5: Generation with Retrieved Context

```python
def rag_query(question: str) -> str:
    """Complete RAG pipeline"""
    
    # 1. Retrieve relevant documents
    docs = retrieve(question, top_k=3)
    
    # 2. Build context
    context = "\n\n".join([doc["content"] for doc in docs])
    
    # 3. Generate answer
    prompt = f"""Answer the question using only the provided context.
    
Context:
{context}

Question: {question}

Answer:"""
    
    response = llm.invoke(prompt)
    return response
```

## Advanced: Reranking

```python
from sentence_transformers import CrossEncoder

# After initial retrieval, rerank for better precision
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank(query: str, docs: List[str], top_k: int = 3) -> List[str]:
    """Rerank retrieved documents"""
    # Score each doc against query
    scores = reranker.predict([(query, doc) for doc in docs])
    
    # Sort by score
    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    
    return [doc for doc, score in ranked[:top_k]]

# Usage in RAG
docs = retrieve(question, top_k=10)  # Get more candidates
docs = rerank(question, docs, top_k=3)  # Rerank to top 3
```

## RAG Evaluation

```python
from deepeval.metrics import AnswerRelevancy, Faithfulness

# Metrics
answer_relevancy = AnswerRelevancy()
faithfulness = Faithfulness()

# Test case
test_case = {
    "input": "What is the capital of France?",
    "actual_output": "The capital of France is Paris.",
    "retrieval_context": ["Paris is the capital and largest city of France."]
}

# Evaluate
relevancy_score = answer_relevancy.measure(test_case)
faithfulness_score = faithfulness.measure(test_case)

print(f"Relevancy: {relevancy_score}")  # How relevant is answer to question?
print(f"Faithfulness: {faithfulness_score}")  # Is answer grounded in context?
```

## Quality Checks
- [ ] Chunking strategy matches document type
- [ ] Embedding model selected (small vs large)
- [ ] Vector database indexed (HNSW or IVFFlat)
- [ ] Retrieval tested (precision/recall measured)
- [ ] Hybrid search if keyword matching needed
- [ ] Reranking for better precision
- [ ] Metadata filtering implemented
- [ ] RAG evaluation metrics (faithfulness, relevancy)
