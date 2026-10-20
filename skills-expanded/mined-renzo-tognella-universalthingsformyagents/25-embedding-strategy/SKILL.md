---
name: Embedding Strategy
description: Use when choosing embedding models, configuring Qdrant vector collections, implementing multi-stage search, switching between dense/sparse/multi-vector embeddings, or optimizing embedding costs and memory in TheSearch.
---

# Embedding Strategy

## Overview

TheSearch usa embeddings para busca semântica e deduplicação. A escolha do modelo e da estratégia (dense, sparse, multi-vector) afeta diretamente qualidade de busca, custo, e latência. O design atual (OpenAI `text-embedding-3-small` 512d) é um MVP — existem estratégias superiores para cada caso de uso.

**Princípio:** Não existe um único tipo de embedding ideal. Use o tipo certo para cada estágio do pipeline.

## Quando Usar

- Ao criar ou reconfigurar collections no Qdrant
- Ao escolher entre OpenAI, local, ou modelos especializados
- Ao implementar busca híbrida (dense + sparse)
- Ao otimizar uso de memória RAM do Qdrant
- Ao avaliar se ColBERT/Matryoshka melhoram retrieval

## Quando NÃO Usar

- Se a collection atual funciona bem (recall > 90%) — não troque sem medir
- Se o projeto está em fase inicial — MVP com modelo simples primeiro

## Tipos de Embedding

| Tipo | Como Funciona | Melhor Para | Custo |
|------|--------------|-------------|:-----:|
| **Dense** | Vetor único denso (512-3072d) | Busca semântica geral | Baixo |
| **Sparse** (SPLADE) | Vetor esparsos com peso por token | Keyword matching, termos técnicos | Baixo |
| **Multi-vector** (ColBERT) | Vetor por token → late interaction | Precision-critical retrieval | Alto |
| **Matryoshka** (MRL) | Dense com granularidades truncáveis | Multi-stage search (coarse→fine) | Médio |

## Estado Atual do TheSearch

```python
# Configuração atual (MVP)
model = "text-embedding-3-small"
dimensions = 512  # truncado de 1536 via MRL
collection = "thesearch_memories"
```

- OpenAI API, 512 dimensões, dense apenas
- Funciona para busca semântica geral
- Limitações: sem keyword matching, sem multi-stage, sem sparse

## Estratégia 1: Matryoshka para Multi-Stage Search

MRL permite truncar o mesmo embedding em múltiplas resoluções sem retreinar.

```
Stage 1: Coarse filter (64d)  → Top 100 candidatos (rápido, barato)
Stage 2: Medium filter (256d) → Top 20 (balanceado)
Stage 3: Fine rank (512d)     → Top 5 final (preciso)
```

```python
async def matryoshka_search(
    query: str,
    project: str,
    top_k: int = 5
) -> list[SearchResult]:
    full_embedding = await embed(query, dimensions=512)

    coarse = full_embedding[:64]
    candidates = await qdrant.search(coarse, limit=100, project=project)

    medium = full_embedding[:256]
    reranked = await qdrant.rerank(medium, candidates, limit=20)

    fine = full_embedding[:512]
    final = await qdrant.rerank(fine, reranked, limit=top_k)

    return final
```

**Configuração Qdrant para MRL:**

```python
from qdrant_client.models import VectorParams

collection_config = VectorParams(
    size=512,
    distance="Cosine",
    multivector_config=None,
    quantization_config=ScalarQuantization(
        scalar=ScalarQuantizationConfig(
            type="int8",
            quantile=0.99,
            always_ram=True
        )
    )
)
```

**Ganho estimado:** 3-5x speedup na busca com ~2% perda de recall.

## Estratégia 2: SPLADE para Hybrid Search

SPLADE gera embeddings esparsos que mapeiam termos com peso — ideal para matching de keywords técnicos, nomes de padrões, identificadores.

```python
from fastembed import SparseEmbedding

sparse_model = SparseEmbedding("Qdrant/bm25")

async def hybrid_search(query: str, project: str) -> list[SearchResult]:
    dense_embedding = await openai_embed(query, dimensions=512)
    sparse_embedding = await sparse_model.embed(query)

    results = await qdrant.hybrid_search(
        dense=dense_embedding,
        sparse=sparse_embedding,
        fusion="rrf",  # Reciprocal Rank Fusion
        limit=10,
        filter={"project": project}
    )
    return results
```

**Configuração Qdrant para sparse:**

```python
from qdrant_client.models import SparseVectorParams, SparseIndexParams

qdrant.create_collection(
    collection_name="thesearch_memories",
    vectors_config={"dense": VectorParams(size=512, distance="Cosine")},
    sparse_vectors_config={
        "sparse": SparseVectorParams(
            index=SparseIndexParams(on_disk=False)
        )
    }
)
```

**Quando SPLADE vale a pena:**
- Busca por nomes exatos (DesignPattern, ArchitecturalDecision)
- Matching de termos técnicos em inglês/português misturados
- Queries que combinam semântica + keywords

## Estratégia 3: ColBERT para Precision-Critical Retrieval

ColBERT gera um vetor por token e faz late interaction (max-sim) — muito mais preciso mas mais caro em storage e compute.

```python
from fastembed import LateInteractionTextEmbedding

colbert_model = LateInteractionTextEmbedding("colbert-ir/colbertv2.0")

async def precision_search(query: str) -> list[SearchResult]:
    query_embeddings = await colbert_model.embed(query)

    results = await qdrant.search(
        collection_name="thesearch_colbert",
        query_vector=query_embeddings,
        limit=5
    )
    return results
```

**Quando usar ColBERT:**
- Deduplicação onde falso positivo é caro (merge incorreto)
- Queries ambíguas que dense embeddings confundem
- **NÃO para search geral** — custo de storage 10-50x maior

## Modelo: BGE-M3 (All-in-One)

BGE-M3 gera dense + sparse + ColBERT em uma única passada:

```python
from fastembed import TextEmbedding

model = TextEmbedding("BAAI/bge-m3")

async def embed_multi(text: str) -> MultiEmbedding:
    result = await model.embed(text, embed_type="all")
    return MultiEmbedding(
        dense=result.dense,
        sparse=result.sparse,
        colbert=result.colbert
    )
```

**Vantagem:** Um modelo, três representações. Ideal se TheSearch quiser suportar os três tipos sem inferência separada.

## Guia de Seleção de Modelo

| Cenário | Modelo | Tipo | Razão |
|---------|--------|:----:|-------|
| MVP / Busca geral | text-embedding-3-small 512d | Dense | Custo baixo, boa qualidade |
| Hybrid search | text-embedding-3-small + SPLADE | Dense+Sparse | Keyword + semântica |
| Multi-stage filter | text-embedding-3-small (MRL) | Dense | 3-5x speedup |
| Precision dedup | ColBERT v2 | Multi-vector | Falso positivo caro |
| Local/self-hosted | all-MiniLM-L6-v2 + FastEmbed | Dense+Sparse | Sem API, gratuito |
| All-in-one | BGE-M3 via FastEmbed | Dense+Sparse+ColBERT | Máxima flexibilidade |

**Matriz de decisão:**

```
Budget API? ──── SIM ──── Precisa de keyword? ──── SIM → Dense + SPLADE
                  │                                    │
                  │                                    └── NÃO → Dense (text-embedding-3-small)
                  │
                  └── NÃO ──── FastEmbed local ──── Precisa de precision?
                                                      │
                                                      ├─ SIM → BGE-M3 (all-in-one)
                                                      └─ NÃO → all-MiniLM-L6-v2
```

## Quantização no Qdrant

Para reduzir memória RAM sem perder muita qualidade:

| Tipo | Redução RAM | Perda Recall | Quando Usar |
|------|:-----------:|:------------:|-------------|
| Scalar (int8) | 4x | ~1-2% | Default — sempre habilitar |
| Product (uint8) | 4-8x | ~2-5% | Coleções grandes (>100K) |
| Binary (1-bit) | 32x | ~10-20% | Pre-filtering stage |

```python
from qdrant_client.models import ScalarQuantization, ScalarQuantizationConfig

quantization = ScalarQuantization(
    scalar=ScalarQuantizationConfig(
        type="int8",
        quantile=0.99,
        always_ram=True
    )
)
```

**Recomendação TheSearch:** Scalar quantization (int8) por default. Para >100K memórias, considerar product quantization com oversampling.

## Regras

- Nunca trocar modelo sem reindexar toda a collection
- Sempre medir recall antes/depois de qualquer mudança de embedding
- Matryoshka truncation funciona APENAS com modelos MRL (text-embedding-3-*, bge-m3)
- Sparse vectors no Qdrant requerem `sparse_vectors_config` na criação da collection
- FastEmbed é CPU-local (ONNX) — sem custo API mas sem GPU acceleration
- ColBERT storage é 10-50x maior que dense — usar apenas para collections específicas

## Common Mistakes

1. **Usar 1536d sem necessidade** — 512d com MRL mantém ~90% da qualidade com 3x menos storage.
2. **Sparse sem dense** — SPLADE sozinho perde semântica. Sempre combinar com dense via RRF.
3. **Quantizar sem oversampling** — int8 + rescore com full vectors para manter recall.
4. **Trocar modelo sem baseline** — sempre medir recall@k antes de mudar. Sem números, é achismo.
5. **ColBERT para tudo** — storage explosion. Usar apenas para dedup precision ou queries específicas.

## Referências

- `knogdement/10_thesearch_related.md` — seção Embeddings (MRL, ColBERT, SPLADE, FastEmbed)
- `knogdement/04_advanced_rag.md` — técnicas avançadas de retrieval
- MRL: https://arxiv.org/abs/2205.13147
- ColBERT: https://arxiv.org/abs/2112.01488
- FastEmbed SPLADE: https://qdrant.tech/documentation/fastembed/fastembed-splade/
- FastEmbed ColBERT: https://qdrant.tech/documentation/fastembed/fastembed-colbert/
- Qdrant Static Embeddings: https://qdrant.tech/documentation/tutorials-search-engineering/static-embeddings/
- Qdrant Quantization: https://qdrant.tech/documentation/manage-data/quantization/
