---
name: qdrant-vector-search
description: Mecanismo de busca de similaridade vetorial de alto desempenho para RAG e busca semântica. Use ao construir sistemas RAG em produção que exigem busca de vizinhos mais próximos rápida, busca híbrida com filtragem ou armazenamento vetorial escalável com desempenho impulsionado por Rust.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [RAG, Vector Search, Qdrant, Semantic Search, Embeddings, Similarity Search, HNSW, Production, Distributed]
dependencies: [qdrant-client>=1.12.0]
---

# Qdrant - Mecanismo de Busca de Similaridade Vetorial

Banco de dados vetorial de alto desempenho escrito em Rust para RAG em produção e busca semântica.

## Quando usar Qdrant

**Use Qdrant quando:**
- Construir sistemas RAG em produção que exigem baixa latência
- Precisar de busca híbrida (vetores + filtragem de metadados)
- Exigir dimensionamento horizontal com sharding/replicação
- Quiser deploy on-premise com controle total de dados
- Precisar armazenar múltiplos vetores por registro (denso + esparso)
- Construir sistemas de recomendação em tempo real

**Recursos principais:**
- **Impulsionado por Rust**: Segurança de memória, alto desempenho
- **Filtragem avançada**: Filtrar por qualquer campo de payload durante a busca
- **Múltiplos vetores**: Denso, esparso, multi-denso por ponto
- **Quantização**: Escalar, produto, binária para eficiência de memória
- **Distribuído**: Consenso Raft, sharding, replicação
- **REST + gRPC**: Ambas as APIs com paridade completa de recursos

**Use alternativas:**
- **Chroma**: Configuração mais simples, casos de uso incorporados
- **FAISS**: Velocidade máxima em bruto, pesquisa/processamento em lote
- **Pinecone**: Totalmente gerenciado, sem operações preferidas
- **Weaviate**: Preferência por GraphQL, vetorizadores integrados

## Início rápido

### Instalação

```bash
# Cliente Python
pip install qdrant-client

# Docker (recomendado para desenvolvimento)
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant

# Docker com armazenamento persistente
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage \
    qdrant/qdrant
```

### Uso básico

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Conectar ao Qdrant
client = QdrantClient(host="localhost", port=6333)

# Criar coleção
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# Inserir vetores com payload
client.upsert(
    collection_name="documents",
    points=[
        PointStruct(
            id=1,
            vector=[0.1, 0.2, ...],  # vetor de 384 dimensões
            payload={"title": "Doc 1", "category": "tech"}
        ),
        PointStruct(
            id=2,
            vector=[0.3, 0.4, ...],
            payload={"title": "Doc 2", "category": "science"}
        )
    ]
)

# Buscar com filtragem
results = client.search(
    collection_name="documents",
    query_vector=[0.15, 0.25, ...],
    query_filter={
        "must": [{"key": "category", "match": {"value": "tech"}}]
    },
    limit=10
)

for point in results:
    print(f"ID: {point.id}, Score: {point.score}, Payload: {point.payload}")
```

## Conceitos fundamentais

### Points - Unidade básica de dados

```python
from qdrant_client.models import PointStruct

# Point = ID + Vector(s) + Payload
point = PointStruct(
    id=123,                              # Integer ou string UUID
    vector=[0.1, 0.2, 0.3, ...],        # Vetor denso
    payload={                            # Metadados JSON arbitrários
        "title": "Document title",
        "category": "tech",
        "timestamp": 1699900000,
        "tags": ["python", "ml"]
    }
)

# Upsert em lote (recomendado)
client.upsert(
    collection_name="documents",
    points=[point1, point2, point3],
    wait=True  # Aguardar indexação
)
```

### Collections - Contêineres de vetores

```python
from qdrant_client.models import VectorParams, Distance, HnswConfigDiff

# Criar com configuração HNSW
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(
        size=384,                        # Dimensões do vetor
        distance=Distance.COSINE         # COSINE, EUCLID, DOT, MANHATTAN
    ),
    hnsw_config=HnswConfigDiff(
        m=16,                            # Conexões por nó (padrão 16)
        ef_construct=100,                # Precisão em tempo de construção (padrão 100)
        full_scan_threshold=10000        # Mudar para força bruta abaixo disso
    ),
    on_disk_payload=True                 # Armazenar payload em disco
)

# Informações de coleção
info = client.get_collection("documents")
print(f"Points: {info.points_count}, Vectors: {info.vectors_count}")
```

### Métricas de distância

| Métrica | Caso de Uso | Intervalo |
|---------|----------|-----------|
| `COSINE` | Embeddings de texto, vetores normalizados | 0 a 2 |
| `EUCLID` | Dados espaciais, recursos de imagem | 0 a ∞ |
| `DOT` | Recomendações, não normalizadas | -∞ a ∞ |
| `MANHATTAN` | Recursos esparsos, dados discretos | 0 a ∞ |

## Operações de busca

### Busca básica

```python
# Busca simples do vizinho mais próximo
results = client.search(
    collection_name="documents",
    query_vector=[0.1, 0.2, ...],
    limit=10,
    with_payload=True,
    with_vectors=False  # Não retornar vetores (mais rápido)
)
```

### Busca com filtragem

```python
from qdrant_client.models import Filter, FieldCondition, MatchValue, Range

# Filtragem complexa
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    query_filter=Filter(
        must=[
            FieldCondition(key="category", match=MatchValue(value="tech")),
            FieldCondition(key="timestamp", range=Range(gte=1699000000))
        ],
        must_not=[
            FieldCondition(key="status", match=MatchValue(value="archived"))
        ]
    ),
    limit=10
)

# Sintaxe abreviada de filtro
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    query_filter={
        "must": [
            {"key": "category", "match": {"value": "tech"}},
            {"key": "price", "range": {"gte": 10, "lte": 100}}
        ]
    },
    limit=10
)
```

### Busca em lote

```python
from qdrant_client.models import SearchRequest

# Múltiplas consultas em uma única requisição
results = client.search_batch(
    collection_name="documents",
    requests=[
        SearchRequest(vector=[0.1, ...], limit=5),
        SearchRequest(vector=[0.2, ...], limit=5, filter={"must": [...]}),
        SearchRequest(vector=[0.3, ...], limit=10)
    ]
)
```

## Integração com RAG

### Com sentence-transformers

```python
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

# Inicializar
encoder = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient(host="localhost", port=6333)

# Criar coleção
client.create_collection(
    collection_name="knowledge_base",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# Indexar documentos
documents = [
    {"id": 1, "text": "Python is a programming language", "source": "wiki"},
    {"id": 2, "text": "Machine learning uses algorithms", "source": "textbook"},
]

points = [
    PointStruct(
        id=doc["id"],
        vector=encoder.encode(doc["text"]).tolist(),
        payload={"text": doc["text"], "source": doc["source"]}
    )
    for doc in documents
]
client.upsert(collection_name="knowledge_base", points=points)

# Recuperação para RAG
def retrieve(query: str, top_k: int = 5) -> list[dict]:
    query_vector = encoder.encode(query).tolist()
    results = client.search(
        collection_name="knowledge_base",
        query_vector=query_vector,
        limit=top_k
    )
    return [{"text": r.payload["text"], "score": r.score} for r in results]

# Usar em pipeline RAG
context = retrieve("What is Python?")
prompt = f"Context: {context}\n\nQuestion: What is Python?"
```

### Com LangChain

```python
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Qdrant.from_documents(documents, embeddings, url="http://localhost:6333", collection_name="docs")
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
```

### Com LlamaIndex

```python
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex, StorageContext

vector_store = QdrantVectorStore(client=client, collection_name="llama_docs")
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
query_engine = index.as_query_engine()
```

## Suporte multi-vetor

### Vetores nomeados (modelos de embedding diferentes)

```python
from qdrant_client.models import VectorParams, Distance

# Coleção com múltiplos tipos de vetores
client.create_collection(
    collection_name="hybrid_search",
    vectors_config={
        "dense": VectorParams(size=384, distance=Distance.COSINE),
        "sparse": VectorParams(size=30000, distance=Distance.DOT)
    }
)

# Inserir com vetores nomeados
client.upsert(
    collection_name="hybrid_search",
    points=[
        PointStruct(
            id=1,
            vector={
                "dense": dense_embedding,
                "sparse": sparse_embedding
            },
            payload={"text": "document text"}
        )
    ]
)

# Buscar vetor específico
results = client.search(
    collection_name="hybrid_search",
    query_vector=("dense", query_dense),  # Especificar qual vetor
    limit=10
)
```

### Vetores esparsos (BM25, SPLADE)

```python
from qdrant_client.models import SparseVectorParams, SparseIndexParams, SparseVector

# Coleção com vetores esparsos
client.create_collection(
    collection_name="sparse_search",
    vectors_config={},
    sparse_vectors_config={"text": SparseVectorParams(index=SparseIndexParams(on_disk=False))}
)

# Inserir vetor esparso
client.upsert(
    collection_name="sparse_search",
    points=[PointStruct(id=1, vector={"text": SparseVector(indices=[1, 5, 100], values=[0.5, 0.8, 0.2])}, payload={"text": "document"})]
)
```

## Quantização (otimização de memória)

```python
from qdrant_client.models import ScalarQuantization, ScalarQuantizationConfig, ScalarType

# Quantização escalar (redução de 4x de memória)
client.create_collection(
    collection_name="quantized",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    quantization_config=ScalarQuantization(
        scalar=ScalarQuantizationConfig(
            type=ScalarType.INT8,
            quantile=0.99,        # Recortar outliers
            always_ram=True      # Manter quantizado em RAM
        )
    )
)

# Buscar com rescore
results = client.search(
    collection_name="quantized",
    query_vector=query,
    search_params={"quantization": {"rescore": True}},  # Rescore dos top resultados
    limit=10
)
```

## Indexação de payload

```python
from qdrant_client.models import PayloadSchemaType

# Criar índice de payload para filtragem mais rápida
client.create_payload_index(
    collection_name="documents",
    field_name="category",
    field_schema=PayloadSchemaType.KEYWORD
)

client.create_payload_index(
    collection_name="documents",
    field_name="timestamp",
    field_schema=PayloadSchemaType.INTEGER
)

# Tipos de índice: KEYWORD, INTEGER, FLOAT, GEO, TEXT (full-text), BOOL
```

## Deploy em produção

### Qdrant Cloud

```python
from qdrant_client import QdrantClient

# Conectar ao Qdrant Cloud
client = QdrantClient(
    url="https://your-cluster.cloud.qdrant.io",
    api_key="your-api-key"
)
```

### Otimização de desempenho

```python
# Otimizar para velocidade de busca (maior recall)
client.update_collection(
    collection_name="documents",
    hnsw_config=HnswConfigDiff(ef_construct=200, m=32)
)

# Otimizar para velocidade de indexação (cargas em massa)
client.update_collection(
    collection_name="documents",
    optimizer_config={"indexing_threshold": 20000}
)
```

## Boas práticas

1. **Operações em lote** - Use upsert/search em lote para eficiência
2. **Indexação de payload** - Indexar campos usados em filtros
3. **Quantização** - Habilitar para coleções grandes (>1M vetores)
4. **Sharding** - Usar para coleções >10M vetores
5. **Armazenamento em disco** - Habilitar `on_disk_payload` para payloads grandes
6. **Pool de conexões** - Reutilizar instâncias de cliente

## Problemas comuns

**Busca lenta com filtros:**
```python
# Criar índice de payload para campos filtrados
client.create_payload_index(
    collection_name="docs",
    field_name="category",
    field_schema=PayloadSchemaType.KEYWORD
)
```

**Falta de memória:**
```python
# Habilitar quantização e armazenamento em disco
client.create_collection(
    collection_name="large_collection",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    quantization_config=ScalarQuantization(...),
    on_disk_payload=True
)
```

**Problemas de conexão:**
```python
# Usar timeout e retry
client = QdrantClient(
    host="localhost",
    port=6333,
    timeout=30,
    prefer_grpc=True  # gRPC para melhor desempenho
)
```

## Referências

- **[Uso Avançado](references/advanced-usage.md)** - Modo distribuído, busca híbrida, recomendações
- **[Solução de Problemas](references/troubleshooting.md)** - Problemas comuns, debugging, otimização de desempenho

## Recursos

- **GitHub**: https://github.com/qdrant/qdrant (22k+ stars)
- **Documentação**: https://qdrant.tech/documentation/
- **Cliente Python**: https://github.com/qdrant/qdrant-client
- **Cloud**: https://cloud.qdrant.io
- **Versão**: 1.12.0+
- **Licença**: Apache 2.0