---
name: faiss
description: Biblioteca do Facebook para busca eficiente de similaridade e clustering de vetores densos. Suporta bilhões de vetores, aceleração GPU e vários tipos de índice (Flat, IVF, HNSW). Use para busca k-NN rápida, recuperação de vetores em larga escala ou quando você precisa de busca pura de similaridade sem metadados. Melhor para aplicações de alto desempenho.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [RAG, FAISS, Similarity Search, Vector Search, Facebook AI, GPU Acceleration, Billion-Scale, K-NN, HNSW, High Performance, Large Scale]
dependencies: [faiss-cpu, faiss-gpu, numpy]
---

# FAISS - Busca Eficiente de Similaridade

Biblioteca do Facebook AI para busca de similaridade de vetores em escala de bilhões.

## Quando usar FAISS

**Use FAISS quando:**
- Precisa de busca rápida de similaridade em grandes conjuntos de dados vetoriais (milhões/bilhões)
- Aceleração GPU é necessária
- Similaridade pura de vetores (sem filtragem de metadados necessária)
- Throughput alto e baixa latência são críticos
- Processamento offline/batch de embeddings

**Métricas**:
- **31.700+ stars no GitHub**
- Meta/Facebook AI Research
- **Processa bilhões de vetores**
- **C++** com bindings Python

**Use alternativas em vez disso**:
- **Chroma/Pinecone**: Precisa de filtragem por metadados
- **Weaviate**: Precisa de recursos completos de banco de dados
- **Annoy**: Mais simples, menos recursos

## Início rápido

### Instalação

```bash
# Apenas CPU
pip install faiss-cpu

# Com suporte a GPU
pip install faiss-gpu
```

### Uso básico

```python
import faiss
import numpy as np

# Criar dados de exemplo (1000 vetores, 128 dimensões)
d = 128
nb = 1000
vectors = np.random.random((nb, d)).astype('float32')

# Criar índice
index = faiss.IndexFlatL2(d)  # Distância L2
index.add(vectors)             # Adicionar vetores

# Buscar
k = 5  # Encontrar 5 vizinhos mais próximos
query = np.random.random((1, d)).astype('float32')
distances, indices = index.search(query, k)

print(f"Nearest neighbors: {indices}")
print(f"Distances: {distances}")
```

## Tipos de índice

### 1. Flat (busca exata)

```python
# Distância L2 (Euclidiana)
index = faiss.IndexFlatL2(d)

# Produto interno (similaridade de cosseno se normalizado)
index = faiss.IndexFlatIP(d)

# Mais lento, mais preciso
```

### 2. IVF (inverted file) - Aproximação rápida

```python
# Criar quantizador
quantizer = faiss.IndexFlatL2(d)

# Índice IVF com 100 clusters
nlist = 100
index = faiss.IndexIVFFlat(quantizer, d, nlist)

# Treinar nos dados
index.train(vectors)

# Adicionar vetores
index.add(vectors)

# Buscar (nprobe = clusters a buscar)
index.nprobe = 10
distances, indices = index.search(query, k)
```

### 3. HNSW (Hierarchical NSW) - Melhor qualidade/velocidade

```python
# Índice HNSW
M = 32  # Número de conexões por camada
index = faiss.IndexHNSWFlat(d, M)

# Sem necessidade de treinamento
index.add(vectors)

# Buscar
distances, indices = index.search(query, k)
```

### 4. Product Quantization - Eficiente em memória

```python
# PQ reduz memória em 16-32×
m = 8   # Número de subquantizadores
nbits = 8
index = faiss.IndexPQ(d, m, nbits)

# Treinar e adicionar
index.train(vectors)
index.add(vectors)
```

## Salvar e carregar

```python
# Salvar índice
faiss.write_index(index, "large.index")

# Carregar índice
index = faiss.read_index("large.index")

# Continuar usando
distances, indices = index.search(query, k)
```

## Aceleração GPU

```python
# GPU única
res = faiss.StandardGpuResources()
index_cpu = faiss.IndexFlatL2(d)
index_gpu = faiss.index_cpu_to_gpu(res, 0, index_cpu)  # GPU 0

# Multi-GPU
index_gpu = faiss.index_cpu_to_all_gpus(index_cpu)

# 10-100× mais rápido que CPU
```

## Integração com LangChain

```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Criar vector store FAISS
vectorstore = FAISS.from_documents(docs, OpenAIEmbeddings())

# Salvar
vectorstore.save_local("faiss_index")

# Carregar
vectorstore = FAISS.load_local(
    "faiss_index",
    OpenAIEmbeddings(),
    allow_dangerous_deserialization=True
)

# Buscar
results = vectorstore.similarity_search("query", k=5)
```

## Integração com LlamaIndex

```python
from llama_index.vector_stores.faiss import FaissVectorStore
import faiss

# Criar índice FAISS
d = 1536
faiss_index = faiss.IndexFlatL2(d)

vector_store = FaissVectorStore(faiss_index=faiss_index)
```

## Melhores práticas

1. **Escolha o tipo de índice certo** - Flat para <10K, IVF para 10K-1M, HNSW para qualidade
2. **Normalize para cosseno** - Use IndexFlatIP com vetores normalizados
3. **Use GPU para grandes conjuntos de dados** - 10-100× mais rápido
4. **Salve índices treinados** - Treinamento é custoso
5. **Ajuste nprobe/ef_search** - Equilibre velocidade/precisão
6. **Monitore memória** - PQ para grandes conjuntos de dados
7. **Agrupe queries em lote** - Melhor utilização de GPU

## Desempenho

| Tipo de Índice | Tempo de Build | Tempo de Busca | Memória | Precisão |
|------------|------------|-------------|--------|----------|
| Flat | Rápido | Lento | Alto | 100% |
| IVF | Médio | Rápido | Médio | 95-99% |
| HNSW | Lento | Mais rápido | Alto | 99% |
| PQ | Médio | Rápido | Baixo | 90-95% |

## Recursos

- **GitHub**: https://github.com/facebookresearch/faiss ⭐ 31.700+
- **Wiki**: https://github.com/facebookresearch/faiss/wiki
- **License**: MIT