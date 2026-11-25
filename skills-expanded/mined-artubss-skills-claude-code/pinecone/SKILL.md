---
name: pinecone
description: Banco de dados vetorial gerenciado para aplicações de IA em produção. Totalmente gerenciado, com auto-scaling, busca híbrida (vetores densos + esparsos), filtragem de metadados e namespaces. Latência baixa (<100ms p95). Use para RAG em produção, sistemas de recomendação ou busca semântica em escala. Ideal para infraestrutura serverless e gerenciada.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [RAG, Pinecone, Vector Database, Managed Service, Serverless, Hybrid Search, Production, Auto-Scaling, Low Latency, Recommendations]
dependencies: [pinecone-client]
---

# Pinecone - Banco de Dados Vetorial Gerenciado

O banco de dados vetorial para aplicações de IA em produção.

## Quando usar Pinecone

**Use quando:**
- Precisar de banco de dados vetorial gerenciado e serverless
- Aplicações RAG em produção
- Auto-scaling necessário
- Latência baixa crítica (<100ms)
- Não quiser gerenciar infraestrutura
- Precisar de busca híbrida (vetores densos + esparsos)

**Métricas**:
- SaaS totalmente gerenciado
- Auto-scales para bilhões de vetores
- **p95 latência <100ms**
- SLA de 99,9% uptime

**Use alternativas em vez disso**:
- **Chroma**: Auto-hospedado, open-source
- **FAISS**: Offline, busca de similaridade pura
- **Weaviate**: Auto-hospedado com mais recursos

## Quick start

### Instalação

```bash
pip install pinecone-client
```

### Uso básico

```python
from pinecone import Pinecone, ServerlessSpec

# Inicializar
pc = Pinecone(api_key="your-api-key")

# Criar índice
pc.create_index(
    name="my-index",
    dimension=1536,  # Deve corresponder à dimensão de embedding
    metric="cosine",  # ou "euclidean", "dotproduct"
    spec=ServerlessSpec(cloud="aws", region="us-east-1")
)

# Conectar ao índice
index = pc.Index("my-index")

# Fazer upsert de vetores
index.upsert(vectors=[
    {"id": "vec1", "values": [0.1, 0.2, ...], "metadata": {"category": "A"}},
    {"id": "vec2", "values": [0.3, 0.4, ...], "metadata": {"category": "B"}}
])

# Consultar
results = index.query(
    vector=[0.1, 0.2, ...],
    top_k=5,
    include_metadata=True
)

print(results["matches"])
```

## Operações principais

### Criar índice

```python
# Serverless (recomendado)
pc.create_index(
    name="my-index",
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",         # ou "gcp", "azure"
        region="us-east-1"
    )
)

# Baseado em pod (para performance consistente)
from pinecone import PodSpec

pc.create_index(
    name="my-index",
    dimension=1536,
    metric="cosine",
    spec=PodSpec(
        environment="us-east1-gcp",
        pod_type="p1.x1"
    )
)
```

### Fazer upsert de vetores

```python
# Upsert único
index.upsert(vectors=[
    {
        "id": "doc1",
        "values": [0.1, 0.2, ...],  # 1536 dimensões
        "metadata": {
            "text": "Conteúdo do documento",
            "category": "tutorial",
            "timestamp": "2025-01-01"
        }
    }
])

# Upsert em lote (recomendado)
vectors = [
    {"id": f"vec{i}", "values": embedding, "metadata": metadata}
    for i, (embedding, metadata) in enumerate(zip(embeddings, metadatas))
]

index.upsert(vectors=vectors, batch_size=100)
```

### Consultar vetores

```python
# Consulta básica
results = index.query(
    vector=[0.1, 0.2, ...],
    top_k=10,
    include_metadata=True,
    include_values=False
)

# Com filtragem de metadados
results = index.query(
    vector=[0.1, 0.2, ...],
    top_k=5,
    filter={"category": {"$eq": "tutorial"}}
)

# Consulta de namespace
results = index.query(
    vector=[0.1, 0.2, ...],
    top_k=5,
    namespace="production"
)

# Acessar resultados
for match in results["matches"]:
    print(f"ID: {match['id']}")
    print(f"Score: {match['score']}")
    print(f"Metadata: {match['metadata']}")
```

### Filtragem de metadados

```python
# Correspondência exata
filter = {"category": "tutorial"}

# Comparação
filter = {"price": {"$gte": 100}}  # $gt, $gte, $lt, $lte, $ne

# Operadores lógicos
filter = {
    "$and": [
        {"category": "tutorial"},
        {"difficulty": {"$lte": 3}}
    ]
}  # Também: $or

# Operador in
filter = {"tags": {"$in": ["python", "ml"]}}
```

## Namespaces

```python
# Particionar dados por namespace
index.upsert(
    vectors=[{"id": "vec1", "values": [...]}],
    namespace="user-123"
)

# Consultar namespace específico
results = index.query(
    vector=[...],
    namespace="user-123",
    top_k=5
)

# Listar namespaces
stats = index.describe_index_stats()
print(stats['namespaces'])
```

## Busca híbrida (denso + esparso)

```python
# Fazer upsert com vetores esparsos
index.upsert(vectors=[
    {
        "id": "doc1",
        "values": [0.1, 0.2, ...],  # Vetor denso
        "sparse_values": {
            "indices": [10, 45, 123],  # IDs de token
            "values": [0.5, 0.3, 0.8]   # Pontuações TF-IDF
        },
        "metadata": {"text": "..."}
    }
])

# Consulta híbrida
results = index.query(
    vector=[0.1, 0.2, ...],
    sparse_vector={
        "indices": [10, 45],
        "values": [0.5, 0.3]
    },
    top_k=5,
    alpha=0.5  # 0=esparso, 1=denso, 0.5=híbrido
)
```

## Integração com LangChain

```python
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings

# Criar vector store
vectorstore = PineconeVectorStore.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings(),
    index_name="my-index"
)

# Consultar
results = vectorstore.similarity_search("query", k=5)

# Com filtro de metadados
results = vectorstore.similarity_search(
    "query",
    k=5,
    filter={"category": "tutorial"}
)

# Como retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
```

## Integração com LlamaIndex

```python
from llama_index.vector_stores.pinecone import PineconeVectorStore

# Conectar ao Pinecone
pc = Pinecone(api_key="your-key")
pinecone_index = pc.Index("my-index")

# Criar vector store
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

# Usar no LlamaIndex
from llama_index.core import StorageContext, VectorStoreIndex

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
```

## Gerenciamento de índices

```python
# Listar índices
indexes = pc.list_indexes()

# Descrever índice
index_info = pc.describe_index("my-index")
print(index_info)

# Obter estatísticas do índice
stats = index.describe_index_stats()
print(f"Total de vetores: {stats['total_vector_count']}")
print(f"Namespaces: {stats['namespaces']}")

# Deletar índice
pc.delete_index("my-index")
```

## Deletar vetores

```python
# Deletar por ID
index.delete(ids=["vec1", "vec2"])

# Deletar por filtro
index.delete(filter={"category": "old"})

# Deletar tudo em um namespace
index.delete(delete_all=True, namespace="test")

# Deletar índice inteiro
index.delete(delete_all=True)
```

## Melhores práticas

1. **Use serverless** - Auto-scaling, custo-efetivo
2. **Faça batch upserts** - Mais eficiente (100-200 por lote)
3. **Adicione metadados** - Habilite filtragem
4. **Use namespaces** - Isole dados por usuário/tenant
5. **Monitore o uso** - Verifique o dashboard do Pinecone
6. **Otimize filtros** - Indexe campos frequentemente filtrados
7. **Teste com tier gratuito** - 1 índice, 100K vetores grátis
8. **Use busca híbrida** - Melhor qualidade
9. **Defina dimensões apropriadas** - Corresponda ao modelo de embedding
10. **Faça backups regulares** - Exporte dados importantes

## Performance

| Operação | Latência | Notas |
|-----------|---------|-------|
| Upsert | ~50-100ms | Por lote |
| Query (p50) | ~50ms | Depende do tamanho do índice |
| Query (p95) | ~100ms | Meta de SLA |
| Filtro de metadados | ~+10-20ms | Overhead adicional |

## Preços (a partir de 2025)

**Serverless**:
- R$ 0,096 por milhão de unidades de leitura
- R$ 0,06 por milhão de unidades de escrita
- R$ 0,06 por GB armazenamento/mês

**Tier gratuito**:
- 1 índice serverless
- 100K vetores (1536 dimensões)
- Ótimo para prototipagem

## Recursos

- **Website**: https://www.pinecone.io
- **Docs**: https://docs.pinecone.io
- **Console**: https://app.pinecone.io
- **Pricing**: https://www.pinecone.io/pricing