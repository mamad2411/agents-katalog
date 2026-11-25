---
name: rag-architecture
description: Design Retrieval-Augmented Generation systems with vector databases, chunking strategies, and hybrid search. Outputs architecture, embedding pipelines, and retrieval optimizations.
argument-hint: [document corpus, query patterns, latency requirements]
allowed-tools: Read, Write, Bash
---

# RAG Architecture (Retrieval-Augmented Generation)

Design RAG systems that combine retrieval and generation. Not pure LLMs — vector search + embeddings + context injection for accurate, source-grounded answers.

## Process

1. **Define use case.** Q&A over docs, semantic search, chatbot with knowledge base.
2. **Choose components.** Vector DB (Pinecone, Weaviate, Qdrant), embedding model, LLM.
3. **Design chunking.** Document splitting strategy (size, overlap, semantic).
4. **Embed documents.** Convert chunks to vectors, store in vector DB.
5. **Build retrieval.** Semantic search, hybrid (dense + sparse), reranking.
6. **Inject context.** Retrieve relevant chunks, format into prompt.
7. **Generate answer.** LLM generates response grounded in retrieved context.

## Output Format

### RAG System: [Application Name]

**Use Case:** Customer support Q&A over docs  
**Vector DB:** Pinecone (1M vectors)  
**Embeddings:** OpenAI text-embedding-3-small  
**Chunking:** 512 tokens, 50 token overlap  
**Retrieval:** Hybrid search (semantic + keyword)  
**LLM:** GPT-4 Turbo

---

## Architecture

```
┌─────────────┐
│  Documents  │ (PDFs, HTML, Markdown)
└──────┬──────┘
       │ Ingestion
       ▼
┌─────────────┐
│  Chunking   │ (Split into 512-token chunks)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Embedding  │ (text-embedding-3-small)
│   Model     │
└──────┬──────┘
       │ Vectors
       ▼
┌─────────────┐
│  Vector DB  │ (Pinecone, indexed by metadata)
│  Pinecone   │
└─────────────┘
       │
       │ Query time
       ▼
┌─────────────┐
│    User     │ → "What is the refund policy?"
│   Query     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Embed      │ (Convert query to vector)
│   Query     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Semantic   │ (Search vector DB, top-k=5)
│   Search    │
└──────┬──────┘
       │ Retrieved chunks
       ▼
┌─────────────┐
│  Rerank     │ (Optional: reorder by relevance)
└──────┬──────┘
       │ Top 3 chunks
       ▼
┌─────────────┐
│   Format    │ (Inject chunks into prompt)
│   Prompt    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│     LLM     │ (Generate answer with context)
│   GPT-4     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Answer    │ → "Refunds are processed within 5-7 days..."
└─────────────┘
```

---

## Document Chunking

### Fixed-Size Chunking
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_documents(documents, chunk_size=512, chunk_overlap=50):
    """Split documents into fixed-size chunks"""
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]  # Try to split on natural boundaries
    )
    
    chunks = []
    for doc in documents:
        doc_chunks = splitter.split_text(doc['content'])
        
        for i, chunk in enumerate(doc_chunks):
            chunks.append({
                'text': chunk,
                'metadata': {
                    'source': doc['source'],
                    'chunk_index': i,
                    'total_chunks': len(doc_chunks)
                }
            })
    
    return chunks

# Usage
documents = [
    {'source': 'refund_policy.pdf', 'content': '...'},
    {'source': 'shipping_guide.pdf', 'content': '...'}
]

chunks = chunk_documents(documents, chunk_size=512, chunk_overlap=50)
print(f"Created {len(chunks)} chunks")
```

### Semantic Chunking
```python
from sentence_transformers import SentenceTransformer
import numpy as np

def semantic_chunking(text, max_chunk_size=512):
    """Split on semantic boundaries using embeddings"""
    
    # Split into sentences
    sentences = text.split('. ')
    
    # Embed sentences
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(sentences)
    
    # Find semantic breaks (low similarity between adjacent sentences)
    similarities = []
    for i in range(len(embeddings) - 1):
        sim = np.dot(embeddings[i], embeddings[i+1])
        similarities.append(sim)
    
    # Split at similarity dips
    threshold = np.percentile(similarities, 25)  # Bottom 25%
    chunks = []
    current_chunk = []
    
    for i, sentence in enumerate(sentences):
        current_chunk.append(sentence)
        
        # Split if similarity dip or chunk too large
        if (i < len(similarities) and similarities[i] < threshold) or len(' '.join(current_chunk)) > max_chunk_size:
            chunks.append('. '.join(current_chunk) + '.')
            current_chunk = []
    
    if current_chunk:
        chunks.append('. '.join(current_chunk) + '.')
    
    return chunks
```

---

## Embedding & Vector Storage

### Generate Embeddings
```python
from openai import OpenAI

client = OpenAI()

def embed_chunks(chunks):
    """Generate embeddings for chunks"""
    
    embedded_chunks = []
    
    for chunk in chunks:
        # Generate embedding
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk['text']
        )
        
        embedding = response.data[0].embedding
        
        embedded_chunks.append({
            'id': f"{chunk['metadata']['source']}_{chunk['metadata']['chunk_index']}",
            'text': chunk['text'],
            'embedding': embedding,
            'metadata': chunk['metadata']
        })
    
    return embedded_chunks
```

### Store in Pinecone
```python
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="your-api-key")

# Create index
index_name = "docs-index"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # text-embedding-3-small dimension
        metric='cosine',
        spec=ServerlessSpec(cloud='aws', region='us-east-1')
    )

index = pc.Index(index_name)

# Upsert vectors
def store_embeddings(embedded_chunks):
    """Store embeddings in Pinecone"""
    
    vectors = []
    for chunk in embedded_chunks:
        vectors.append({
            'id': chunk['id'],
            'values': chunk['embedding'],
            'metadata': {
                'text': chunk['text'],
                'source': chunk['metadata']['source']
            }
        })
    
    # Batch upsert (100 at a time)
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i+batch_size]
        index.upsert(vectors=batch)
    
    print(f"Stored {len(vectors)} vectors")
```

---

## Retrieval

### Semantic Search
```python
def retrieve_relevant_chunks(query, top_k=5):
    """Retrieve most relevant chunks for query"""
    
    # Embed query
    query_response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    query_embedding = query_response.data[0].embedding
    
    # Search vector DB
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    
    # Extract chunks
    chunks = []
    for match in results['matches']:
        chunks.append({
            'text': match['metadata']['text'],
            'source': match['metadata']['source'],
            'score': match['score']
        })
    
    return chunks

# Usage
query = "What is the refund policy?"
relevant_chunks = retrieve_relevant_chunks(query, top_k=5)

for i, chunk in enumerate(relevant_chunks):
    print(f"Chunk {i+1} (score: {chunk['score']:.3f})")
    print(f"Source: {chunk['source']}")
    print(f"Text: {chunk['text'][:200]}...")
```

### Hybrid Search (Dense + Sparse)
```python
from rank_bm25 import BM25Okapi

class HybridRetriever:
    """Combine semantic (dense) and keyword (sparse) search"""
    
    def __init__(self, chunks):
        self.chunks = chunks
        
        # Build BM25 index (keyword search)
        tokenized_chunks = [chunk['text'].split() for chunk in chunks]
        self.bm25 = BM25Okapi(tokenized_chunks)
    
    def retrieve(self, query, top_k=5, alpha=0.5):
        """
        alpha: weight for semantic vs keyword (0.5 = equal)
        """
        
        # Semantic search
        semantic_results = retrieve_relevant_chunks(query, top_k=top_k*2)
        
        # Keyword search
        tokenized_query = query.split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        
        # Combine scores
        combined = {}
        
        # Add semantic scores
        for result in semantic_results:
            chunk_id = result['source'] + '_' + result['text'][:50]
            combined[chunk_id] = {
                'chunk': result,
                'semantic_score': result['score'],
                'bm25_score': 0
            }
        
        # Add BM25 scores
        for i, score in enumerate(bm25_scores):
            chunk = self.chunks[i]
            chunk_id = chunk['metadata']['source'] + '_' + chunk['text'][:50]
            
            if chunk_id in combined:
                combined[chunk_id]['bm25_score'] = score
            else:
                combined[chunk_id] = {
                    'chunk': chunk,
                    'semantic_score': 0,
                    'bm25_score': score
                }
        
        # Calculate final scores
        for chunk_id in combined:
            combined[chunk_id]['final_score'] = (
                alpha * combined[chunk_id]['semantic_score'] +
                (1 - alpha) * combined[chunk_id]['bm25_score']
            )
        
        # Sort by final score
        sorted_chunks = sorted(
            combined.values(),
            key=lambda x: x['final_score'],
            reverse=True
        )
        
        return [c['chunk'] for c in sorted_chunks[:top_k]]
```

---

## Reranking

```python
from sentence_transformers import CrossEncoder

def rerank_chunks(query, chunks, top_k=3):
    """Rerank retrieved chunks using cross-encoder"""
    
    reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    
    # Create query-chunk pairs
    pairs = [[query, chunk['text']] for chunk in chunks]
    
    # Score pairs
    scores = reranker.predict(pairs)
    
    # Sort by score
    ranked = sorted(
        zip(chunks, scores),
        key=lambda x: x[1],
        reverse=True
    )
    
    return [chunk for chunk, score in ranked[:top_k]]
```

---

## Prompt Construction

```python
def build_rag_prompt(query, chunks):
    """Construct prompt with retrieved context"""
    
    context = "\n\n".join([
        f"Source: {chunk['source']}\n{chunk['text']}"
        for chunk in chunks
    ])
    
    prompt = f"""Use the following context to answer the question. If the answer is not in the context, say "I don't have enough information to answer this question."

Context:
{context}

Question: {query}

Answer:"""
    
    return prompt

# Usage
chunks = retrieve_relevant_chunks(query, top_k=3)
prompt = build_rag_prompt(query, chunks)

response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
        {"role": "user", "content": prompt}
    ]
)

answer = response.choices[0].message.content
print(answer)
```

---

## Complete RAG Pipeline

```python
class RAGSystem:
    def __init__(self, index_name, embedding_model="text-embedding-3-small"):
        self.client = OpenAI()
        self.index = pc.Index(index_name)
        self.embedding_model = embedding_model
    
    def ingest_documents(self, documents):
        """Ingest and index documents"""
        
        # Chunk
        chunks = chunk_documents(documents)
        
        # Embed
        embedded_chunks = embed_chunks(chunks)
        
        # Store
        store_embeddings(embedded_chunks)
    
    def query(self, query, top_k=5, use_rerank=True):
        """Answer query using RAG"""
        
        # Retrieve
        chunks = retrieve_relevant_chunks(query, top_k=top_k*2)
        
        # Rerank (optional)
        if use_rerank:
            chunks = rerank_chunks(query, chunks, top_k=top_k)
        
        # Build prompt
        prompt = build_rag_prompt(query, chunks[:3])  # Use top 3
        
        # Generate
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Answer questions using only the provided context."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return {
            'answer': response.choices[0].message.content,
            'sources': [chunk['source'] for chunk in chunks[:3]]
        }

# Usage
rag = RAGSystem("docs-index")

# Ingest documents (one-time)
# rag.ingest_documents(documents)

# Query
result = rag.query("What is the refund policy?")
print(f"Answer: {result['answer']}")
print(f"Sources: {result['sources']}")
```

---

## Metadata Filtering

```python
# Filter by source during retrieval
results = index.query(
    vector=query_embedding,
    top_k=5,
    filter={
        "source": {"$eq": "refund_policy.pdf"}
    },
    include_metadata=True
)

# Filter by date range
results = index.query(
    vector=query_embedding,
    top_k=5,
    filter={
        "date": {"$gte": "2024-01-01"}
    }
)
```

---

## Evaluation

### Retrieval Metrics
```python
def evaluate_retrieval(queries_with_ground_truth):
    """Evaluate retrieval quality"""
    
    precision_at_k = []
    recall_at_k = []
    
    for query_data in queries_with_ground_truth:
        query = query_data['query']
        relevant_docs = set(query_data['relevant_docs'])
        
        # Retrieve
        retrieved = retrieve_relevant_chunks(query, top_k=5)
        retrieved_docs = set([chunk['source'] for chunk in retrieved])
        
        # Calculate metrics
        true_positives = len(relevant_docs & retrieved_docs)
        precision = true_positives / len(retrieved_docs) if retrieved_docs else 0
        recall = true_positives / len(relevant_docs) if relevant_docs else 0
        
        precision_at_k.append(precision)
        recall_at_k.append(recall)
    
    return {
        'precision@5': np.mean(precision_at_k),
        'recall@5': np.mean(recall_at_k)
    }
```

### Answer Quality
```python
def evaluate_answer_quality(test_cases):
    """Evaluate generated answers"""
    
    scores = []
    
    for case in test_cases:
        query = case['query']
        expected_answer = case['expected_answer']
        
        # Generate answer
        result = rag.query(query)
        generated_answer = result['answer']
        
        # Calculate similarity (using embeddings)
        expected_emb = client.embeddings.create(
            model="text-embedding-3-small",
            input=expected_answer
        ).data[0].embedding
        
        generated_emb = client.embeddings.create(
            model="text-embedding-3-small",
            input=generated_answer
        ).data[0].embedding
        
        similarity = np.dot(expected_emb, generated_emb)
        scores.append(similarity)
    
    return {'average_similarity': np.mean(scores)}
```

---

## Optimization Strategies

### Caching
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def retrieve_cached(query):
    """Cache retrieval results"""
    return retrieve_relevant_chunks(query)
```

### Async Processing
```python
import asyncio

async def async_retrieve(queries):
    """Retrieve for multiple queries in parallel"""
    
    tasks = [retrieve_relevant_chunks(q) for q in queries]
    results = await asyncio.gather(*tasks)
    
    return results
```

### Quantization (Reduce vector size)
```python
# Use smaller embedding model
# text-embedding-3-small (1536 dims) vs text-embedding-3-large (3072 dims)

# Or quantize embeddings
import numpy as np

def quantize_embedding(embedding, num_bits=8):
    """Reduce precision to save storage"""
    
    min_val = np.min(embedding)
    max_val = np.max(embedding)
    
    scale = (2**num_bits - 1) / (max_val - min_val)
    quantized = np.round((embedding - min_val) * scale).astype(np.uint8)
    
    return quantized
```

## Rules

- Chunk size 200-1000 tokens — too small loses context, too large dilutes relevance.
- 10-20% overlap between chunks — prevents splitting mid-sentence or concept.
- Retrieve 2-3x top_k, then rerank — improves precision without latency penalty.
- Use metadata filters for scoped search — filter by date, source, or category before semantic search.
- Hybrid search for keyword-heavy queries — "what is form 1099" needs exact keyword match.
- Rerank with cross-encoder for accuracy — semantic search recall, reranker precision.
- Include source attribution in answers — enables fact-checking, builds trust.
- Cache frequent queries — 80% queries repeat, cache saves embedding + search cost.
- Monitor retrieval metrics (precision@k, recall@k) — poor retrieval = poor answers.
- Set LLM to refuse when context insufficient — "I don't know" better than hallucination.
