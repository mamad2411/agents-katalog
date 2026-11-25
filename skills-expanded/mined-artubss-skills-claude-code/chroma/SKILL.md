---
name: chroma
description: Banco de dados de embeddings de código aberto para aplicações de IA. Armazene embeddings e metadados, realize buscas vetoriais e full-text, filtre por metadados. API simples com 4 funções. Escala de notebooks para clusters de produção. Use para busca semântica, aplicações RAG ou recuperação de documentos. Melhor para desenvolvimento local e projetos de código aberto.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [RAG, Chroma, Vector Database, Embeddings, Semantic Search, Open Source, Self-Hosted, Document Retrieval, Metadata Filtering]
dependencies: [chromadb, sentence-transformers]
---

# Chroma - Banco de Dados de Embeddings de Código Aberto

O banco de dados nativo de IA para construir aplicações LLM com memória.

## Quando usar Chroma

**Use Chroma quando:**
- Construir aplicações RAG (retrieval-augmented generation)
- Precisar de banco de dados vetorial local/auto-hospedado
- Quiser solução de código aberto (Apache 2.0)
- Prototipar em notebooks
- Fazer busca semântica sobre documentos
- Armazenar embeddings com metadados

**Métricas**:
- **24.300+ estrelas no GitHub**
- **1.900+ forks**
- **v1.3.3** (estável, lançamentos semanais)
- **Licença Apache 2.0**

**Use alternativas:**
- **Pinecone**: Cloud gerenciado, auto-scaling
- **FAISS**: Busca de similaridade pura, sem metadados
- **Weaviate**: Banco de dados nativo de ML para produção
- **Qdrant**: Alto desempenho, baseado em Rust

## Início rápido

### Instalação

```bash
# Python
pip install chromadb

# JavaScript/TypeScript
npm install chromadb @chroma-core/default-embed
```

### Uso básico (Python)

```python
import chromadb

# Criar cliente
client = chromadb.Client()

# Criar coleção
collection = client.create_collection(name="my_collection")

# Adicionar documentos
collection.add(
    documents=["This is document 1", "This is document 2"],
    metadatas=[{"source": "doc1"}, {"source": "doc2"}],
    ids=["id1", "id2"]
)

# Consultar
results = collection.query(
    query_texts=["document about topic"],
    n_results=2
)

print(results)
```

## Operações principais

### 1. Criar coleção

```python
# Coleção simples
collection = client.create_collection("my_docs")

# Com função de embedding customizada
from chromadb.utils import embedding_functions

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key="your-key",
    model_name="text-embedding-3-small"
)

collection = client.create_collection(
    name="my_docs",
    embedding_function=openai_ef
)

# Obter coleção existente
collection = client.get_collection("my_docs")

# Deletar coleção
client.delete_collection("my_docs")
```

### 2. Adicionar documentos

```python
# Adicionar com IDs auto-gerados
collection.add(
    documents=["Doc 1", "Doc 2", "Doc 3"],
    metadatas=[
        {"source": "web", "category": "tutorial"},
        {"source": "pdf", "page": 5},
        {"source": "api", "timestamp": "2025-01-01"}
    ],
    ids=["id1", "id2", "id3"]
)

# Adicionar com embeddings customizados
collection.add(
    embeddings=[[0.1, 0.2, ...], [0.3, 0.4, ...]],
    documents=["Doc 1", "Doc 2"],
    ids=["id1", "id2"]
)
```

### 3. Consultar (busca de similaridade)

```python
# Consulta básica
results = collection.query(
    query_texts=["machine learning tutorial"],
    n_results=5
)

# Consulta com filtros
results = collection.query(
    query_texts=["Python programming"],
    n_results=3,
    where={"source": "web"}
)

# Consulta com filtros de metadados
results = collection.query(
    query_texts=["advanced topics"],
    where={
        "$and": [
            {"category": "tutorial"},
            {"difficulty": {"$gte": 3}}
        ]
    }
)

# Acessar resultados
print(results["documents"])      # Lista de documentos correspondentes
print(results["metadatas"])      # Metadados de cada documento
print(results["distances"])      # Pontuações de similaridade
print(results["ids"])            # IDs dos documentos
```

### 4. Obter documentos

```python
# Obter por IDs
docs = collection.get(
    ids=["id1", "id2"]
)

# Obter com filtros
docs = collection.get(
    where={"category": "tutorial"},
    limit=10
)

# Obter todos os documentos
docs = collection.get()
```

### 5. Atualizar documentos

```python
# Atualizar conteúdo do documento
collection.update(
    ids=["id1"],
    documents=["Updated content"],
    metadatas=[{"source": "updated"}]
)
```

### 6. Deletar documentos

```python
# Deletar por IDs
collection.delete(ids=["id1", "id2"])

# Deletar com filtro
collection.delete(
    where={"source": "outdated"}
)
```

## Armazenamento persistente

```python
# Persistir em disco
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.create_collection("my_docs")
collection.add(documents=["Doc 1"], ids=["id1"])

# Dados persistidos automaticamente
# Recarregar mais tarde com o mesmo caminho
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("my_docs")
```

## Funções de embedding

### Padrão (Sentence Transformers)

```python
# Usa sentence-transformers por padrão
collection = client.create_collection("my_docs")
# Modelo padrão: all-MiniLM-L6-v2
```

### OpenAI

```python
from chromadb.utils import embedding_functions

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key="your-key",
    model_name="text-embedding-3-small"
)

collection = client.create_collection(
    name="openai_docs",
    embedding_function=openai_ef
)
```

### HuggingFace

```python
huggingface_ef = embedding_functions.HuggingFaceEmbeddingFunction(
    api_key="your-key",
    model_name="sentence-transformers/all-mpnet-base-v2"
)

collection = client.create_collection(
    name="hf_docs",
    embedding_function=huggingface_ef
)
```

### Função de embedding customizada

```python
from chromadb import Documents, EmbeddingFunction, Embeddings

class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        # Sua lógica de embedding
        return embeddings

my_ef = MyEmbeddingFunction()
collection = client.create_collection(
    name="custom_docs",
    embedding_function=my_ef
)
```

## Filtragem de metadados

```python
# Correspondência exata
results = collection.query(
    query_texts=["query"],
    where={"category": "tutorial"}
)

# Operadores de comparação
results = collection.query(
    query_texts=["query"],
    where={"page": {"$gt": 10}}  # $gt, $gte, $lt, $lte, $ne
)

# Operadores lógicos
results = collection.query(
    query_texts=["query"],
    where={
        "$and": [
            {"category": "tutorial"},
            {"difficulty": {"$lte": 3}}
        ]
    }  # Também: $or
)

# Contém
results = collection.query(
    query_texts=["query"],
    where={"tags": {"$in": ["python", "ml"]}}
)
```

## Integração com LangChain

```python
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Dividir documentos
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
docs = text_splitter.split_documents(documents)

# Criar vector store Chroma
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings(),
    persist_directory="./chroma_db"
)

# Consultar
results = vectorstore.similarity_search("machine learning", k=3)

# Como retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
```

## Integração com LlamaIndex

```python
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
import chromadb

# Inicializar Chroma
db = chromadb.PersistentClient(path="./chroma_db")
collection = db.get_or_create_collection("my_collection")

# Criar vector store
vector_store = ChromaVectorStore(chroma_collection=collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Criar índice
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context
)

# Consultar
query_engine = index.as_query_engine()
response = query_engine.query("What is machine learning?")
```

## Modo servidor

```python
# Executar servidor Chroma
# Terminal: chroma run --path ./chroma_db --port 8000

# Conectar ao servidor
import chromadb
from chromadb.config import Settings

client = chromadb.HttpClient(
    host="localhost",
    port=8000,
    settings=Settings(anonymized_telemetry=False)
)

# Usar normalmente
collection = client.get_or_create_collection("my_docs")
```

## Melhores práticas

1. **Use cliente persistente** - Não perca dados ao reiniciar
2. **Adicione metadados** - Habilita filtragem e rastreamento
3. **Operações em lote** - Adicione múltiplos documentos de uma vez
4. **Escolha o modelo de embedding certo** - Equilibre velocidade/qualidade
5. **Use filtros** - Reduza o espaço de busca
6. **IDs únicos** - Evite colisões
7. **Backups regulares** - Copie o diretório chroma_db
8. **Monitore tamanho da coleção** - Escale se necessário
9. **Teste funções de embedding** - Garanta qualidade
10. **Use modo servidor para produção** - Melhor para multi-usuário

## Desempenho

| Operação | Latência | Notas |
|-----------|---------|-------|
| Adicionar 100 documentos | ~1-3s | Com embedding |
| Consulta (top 10) | ~50-200ms | Depende do tamanho da coleção |
| Filtro de metadados | ~10-50ms | Rápido com indexação apropriada |

## Recursos

- **GitHub**: https://github.com/chroma-core/chroma ⭐ 24.300+
- **Docs**: https://docs.trychroma.com
- **Discord**: https://discord.gg/MMeYNTmh3x
- **Versão**: 1.3.3+
- **Licença**: Apache 2.0