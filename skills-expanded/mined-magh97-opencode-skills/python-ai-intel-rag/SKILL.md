---
name: python-ai-intel-rag
description: "RAG (Retrieval-Augmented Generation) optimizado para hardware Intel. Cubre embeddings via OpenVINO, pgvector en PostgreSQL, LangChain/LlamaIndex con backend Intel, re-ranking con cross-encoders OpenVINO, y RAG on-device en Core Ultra. Actívala al implementar RAG, búsqueda vectorial, o chatbots con documentos."
disable-model-invocation: true
---

# RAG on Intel Hardware

Retrieval-Augmented Generation optimizado para CPUs y GPUs Intel: embeddings via OpenVINO, pgvector para búsqueda vectorial, y LangChain con backend Intel.

---

## Arquitectura RAG en Intel

```
Documentos → Chunking → Embeddings (OpenVINO) → pgvector
                                                      ↓
Query → Embedding (OpenVINO) → Búsqueda (pgvector HNSW)
                                      ↓
Contexto + Query → LLM (OpenVINO GenAI) → Respuesta
```

---

## Stack RAG Intel

| Componente | Herramienta | Instalación |
|-----------|-------------|-------------|
| Embeddings | OpenVINO + optimum-intel | `uv add optimum-intel` |
| Vector DB | pgvector en PostgreSQL | PostgreSQL 18 + `CREATE EXTENSION vector` |
| RAG framework | LangChain / LlamaIndex | `uv add langchain langchain-community` |
| Re-ranker | Cross-encoder via OpenVINO | `uv add optimum-intel` |
| LLM | OpenVINO GenAI | `uv add openvino-genai` |

---

## Embeddings con OpenVINO

```python
from optimum.intel import OVModelForFeatureExtraction
from transformers import AutoTokenizer
import numpy as np

model_id = "BAAI/bge-small-en-v1.5"  # 384-dim, rápido, buena calidad

# ─── Cargar y convertir a OpenVINO ───
model = OVModelForFeatureExtraction.from_pretrained(
    model_id,
    export=True,
    device="CPU",
    ov_config={
        "PERFORMANCE_HINT": "THROUGHPUT",
        "NUM_STREAMS": "AUTO",
    },
)
tokenizer = AutoTokenizer.from_pretrained(model_id)

# ─── Embedding de un texto ───
def embed(texts: list[str]) -> np.ndarray:
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    outputs = model(**inputs)
    # Mean pooling
    attention_mask = inputs["attention_mask"]
    embeddings = outputs.last_hidden_state
    mask = attention_mask.unsqueeze(-1).expand(embeddings.size()).float()
    pooled = (embeddings * mask).sum(1) / mask.sum(1)
    return pooled.detach().cpu().numpy()

# ─── Embedding de documentos ───
docs = [
    "Intel Arc GPUs feature Xe HPG architecture with hardware ray tracing.",
    "OpenVINO optimizes inference across Intel CPUs, GPUs, and NPUs.",
    "pgvector provides HNSW indexing for fast approximate nearest neighbor search.",
]
doc_embeddings = embed(docs)
print(f"Shape: {doc_embeddings.shape}")  # → (3, 384)
```

---

## pgvector + PostgreSQL

### SQL setup

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    embedding VECTOR(384)  -- bge-small = 384 dims
);

-- Índice HNSW (más rápido que IVFFlat)
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 200);

-- Índice IVFFlat (alternativa, requiere más memoria)
-- CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```

### Python client

```python
import asyncpg
import numpy as np

async def setup_db():
    conn = await asyncpg.connect(
        "postgresql://user:pass@localhost:5432/ragdb"
    )
    # Crear tabla (si no existe)
    await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            content TEXT NOT NULL,
            metadata JSONB DEFAULT '{}',
            embedding VECTOR(384)
        )
    """)
    return conn

async def insert_document(conn, content: str, embedding: np.ndarray, metadata: dict = None):
    embedding_str = f"[{','.join(map(str, embedding))}]"
    await conn.execute(
        "INSERT INTO documents (content, embedding, metadata) VALUES ($1, $2::vector, $3)",
        content, embedding_str, json.dumps(metadata or {}),
    )

async def search(conn, query_embedding: np.ndarray, top_k: int = 5) -> list:
    embedding_str = f"[{','.join(map(str, query_embedding))}]"
    rows = await conn.fetch("""
        SELECT id, content, metadata,
               1 - (embedding <=> $1::vector) AS similarity
        FROM documents
        ORDER BY embedding <=> $1::vector
        LIMIT $2
    """, embedding_str, top_k)
    return [dict(row) for row in rows]
```

---

## RAG completo con LangChain + OpenVINO

```python
from langchain_community.vectorstores import PGVector
from langchain_openai import ChatOpenAI  # o langchain_community para OpenVINO
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import numpy as np

# ─── Embeddings con OpenVINO ───
class OpenVINOEmbeddings:
    def __init__(self, model_id="BAAI/bge-small-en-v1.5", device="CPU"):
        from optimum.intel import OVModelForFeatureExtraction
        from transformers import AutoTokenizer

        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = OVModelForFeatureExtraction.from_pretrained(
            model_id, export=True, device=device,
        )

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return embed(texts).tolist()

    def embed_query(self, text: str) -> list[float]:
        return embed([text])[0].tolist()

embeddings = OpenVINOEmbeddings()

# ─── Vector store (pgvector) ───
vectorstore = PGVector(
    connection_string="postgresql://user:pass@localhost:5432/ragdb",
    embedding_function=embeddings,
    collection_name="intel_docs",
)

# ─── Indexar documentos ───
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
with open("docs/intel_arc.txt") as f:
    chunks = splitter.split_text(f.read())

vectorstore.add_texts(chunks)

# ─── Retrieval ───
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# ─── RAG chain ───
template = """Answer based on the provided context.

Context:
{context}

Question: {question}
Answer:"""

prompt = ChatPromptTemplate.from_template(template)

# LLM (puede ser OpenVINO o API)
# Si usás OpenVINO GenAI, necesitás un wrapper.
# Acá usamos OpenAI como ejemplo (reemplazable por OpenVINO GenAI wrapper)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

answer = chain.invoke("What is Intel Arc's architecture?")
print(answer)
```

---

## Re-ranking con cross-encoder OpenVINO

```python
from optimum.intel import OVModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np

# ─── Cargar cross-encoder (re-ranker) ───
reranker = OVModelForSequenceClassification.from_pretrained(
    "BAAI/bge-reranker-base",
    export=True,
    device="CPU",
)
reranker_tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-reranker-base")

def rerank(query: str, documents: list[str], top_k: int = 3) -> list[dict]:
    """Re-ordena documentos por relevancia usando cross-encoder."""
    pairs = [[query, doc] for doc in documents]
    inputs = reranker_tokenizer(
        pairs, padding=True, truncation=True, return_tensors="pt", max_length=512,
    )
    scores = reranker(**inputs).logits.squeeze(-1).detach().numpy()
    ranked = sorted(
        [{"doc": doc, "score": float(score)} for doc, score in zip(documents, scores)],
        key=lambda x: x["score"],
        reverse=True,
    )
    return ranked[:top_k]

# ─── Pipeline: retrieve → rerank → generate ───
query = "Explain OpenVINO's advantages"
candidates = [r["content"] for r in await search(conn, query_embedding, top_k=10)]
top_docs = rerank(query, candidates, top_k=3)
context = "\n".join(d["doc"] for d in top_docs)
# ... feed context to LLM ...
```

---

## RAG on-device (Core Ultra)

```python
# RAG completo en Core Ultra: embeddings en CPU, búsqueda en pgvector local, LLM en GPU

import openvino_genai as ov_genai
from optimum.intel import OVModelForFeatureExtraction

# ─── Embedding model en CPU (rápido, 384-dim) ───
embed_model = OVModelForFeatureExtraction.from_pretrained(
    "BAAI/bge-small-en-v1.5", export=True, device="CPU",
)

# ─── LLM cuantizado en GPU integrada ───
# Usar modelo pequeño (1-3B params) cuantizado a INT4
llm = ov_genai.LLMPipeline("phi-3-mini-int4/", device="GPU")

def on_device_rag(query: str, context: str) -> str:
    prompt = f"""<|system|>
You are an assistant. Answer based on the provided context.
<|user|>
Context: {context}

Question: {query}
<|assistant|>
"""
    return llm.generate(prompt, max_new_tokens=256, temperature=0.3)

# ─── ChromaDB como alternativa ligera a pgvector ───
# En edge, ChromaDB (sqlite-backed) evita dependencia de PostgreSQL
import chromadb

chroma_client = chromadb.PersistentClient(path="./chroma_data")
collection = chroma_client.get_or_create_collection("intel_docs")

collection.add(
    ids=[str(i) for i in range(len(chunks))],
    documents=chunks,
    embeddings=embed(chunks).tolist(),
)

results = collection.query(query_embeddings=embed([query]).tolist(), n_results=4)
```

---

## Optimización de embeddings en batch

```python
import numpy as np

def embed_batch(texts: list[str], batch_size: int = 32) -> np.ndarray:
    """Embeddings en batch para aprovechar paralelismo de CPU."""
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        inputs = tokenizer(batch, padding=True, truncation=True, return_tensors="pt")
        outputs = model(**inputs)
        attention_mask = inputs["attention_mask"]
        embeddings = outputs.last_hidden_state
        mask = attention_mask.unsqueeze(-1).expand(embeddings.size()).float()
        pooled = (embeddings * mask).sum(1) / mask.sum(1)
        all_embeddings.append(pooled.detach().cpu().numpy())
    return np.concatenate(all_embeddings, axis=0)

# Indexar 10K documentos
chunks = load_chunks("corpus.txt")
embeddings = embed_batch(chunks, batch_size=64)  # Batch grandes = más throughput
```

---

## Hybrid search (vector + keyword)

```sql
-- Combinar búsqueda vectorial con texto completo
SELECT id, content, metadata,
       (1 - (embedding <=> $1::vector)) * 0.7 +        -- 70% peso vectorial
       ts_rank(to_tsvector('english', content), plainto_tsquery('english', $2)) * 0.3  -- 30% keyword
       AS score
FROM documents
WHERE to_tsvector('english', content) @@ plainto_tsquery('english', $2)
   OR embedding <=> $1::vector < 0.5
ORDER BY score DESC
LIMIT 10;
```

```python
async def hybrid_search(conn, query_text: str, query_embedding: np.ndarray, top_k=10):
    emb_str = f"[{','.join(map(str, query_embedding))}]"
    rows = await conn.fetch("""
        SELECT id, content, metadata,
               (1 - (embedding <=> $1::vector)) * 0.7 +
               ts_rank(to_tsvector('english', content), plainto_tsquery('english', $2)) * 0.3
               AS score
        FROM documents
        WHERE embedding <=> $1::vector < 0.5
        ORDER BY score DESC
        LIMIT $3
    """, emb_str, query_text, top_k)
    return [dict(row) for row in rows]
```

---

## Checklist RAG en Intel

- [ ] Embeddings con OpenVINO (optimum-intel) para throughput máximo
- [ ] Modelo de embeddings alineado con la dimensionalidad de pgvector (384, 768, 1024)
- [ ] Índice HNSW en pgvector (`m=16, ef_construction=200`) para búsqueda rápida
- [ ] Batch embedding para indexar documentos grandes
- [ ] Re-ranking con cross-encoder OpenVINO para calidad extra
- [ ] LLM cuantizado (INT4) para generación en GPU Intel
- [ ] Context window ajustada a la VRAM disponible
- [ ] ChromaDB (sqlite) para edge/dev, pgvector para producción
- [ ] Hybrid search (vector + keyword) si los documentos tienen terminología específica
- [ ] On-device RAG: embedding en CPU + LLM en GPU integrada de Core Ultra
