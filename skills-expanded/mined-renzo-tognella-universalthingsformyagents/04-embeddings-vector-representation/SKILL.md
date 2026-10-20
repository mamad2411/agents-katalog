---
name: Embeddings & Vector Representation
description: Geração de embeddings vetoriais, modelos disponíveis, dimensão reduction via Matryoshka RL, construção de texto para embedding, e batch processing.
---

# Embeddings & Vector Representation

## Quando Usar

- Ao gerar embeddings para novos MemoryItems
- Ao escolher ou trocar o modelo de embedding
- Ao otimizar performance/custo de embeddings

## Conceitos Fundamentais

**Embedding** = representação numérica densa de texto em um espaço vetorial de alta dimensão. Textos semanticamente similares têm vetores próximos (alta similaridade de cosseno).

**Similaridade de Cosseno:**
```
cos(A, B) = (A · B) / (||A|| × ||B||)
```
- `1.0` = idênticos semanticamente
- `0.0` = não relacionados
- Threshold para duplicata: `>= 0.92`
- Threshold para refinamento: `>= 0.80`

## Modelos Disponíveis

| Modelo | Dimensões | Custo | Qualidade | Uso |
|--------|:---------:|:-----:|:---------:|-----|
| `text-embedding-3-small` | 1536→512 | API paga | Boa | **MVP (recomendado)** |
| `text-embedding-3-large` | 3072→1024 | API paga | Alta | Produção |
| `all-MiniLM-L6-v2` | 384 | Gratuito | OK | Self-hosted |
| `all-mpnet-base-v2` | 768 | Gratuito | Boa | Self-hosted premium |
| `voyage-3-large` | 1536 | API paga | Alta | Domain-specific |

## Matryoshka Representation Learning (MRL)

OpenAI `text-embedding-3-*` suporta **redução de dimensão sem retreino**:

```python
response = client.embeddings.create(
    input=text,
    model="text-embedding-3-small",
    dimensions=512  # Reduz de 1536 para 512
)
```

- 512 dims mantém ~90% da qualidade vs 1536
- Economiza ~66% de storage e memória
- Trade-off aceito para MVP

## Construção do Texto para Embedding

A qualidade do embedding depende diretamente do texto de entrada:

```python
def build_text_for_embedding(title: str, summary: str, details: str = "") -> str:
    parts = [title, summary]
    if details:
        parts.append(details[:500])  # Truncar para evitar ruído
    return " | ".join(parts)
```

O separador ` | ` ajuda o modelo a distinguir campos. Ordem importa: título primeiro (mais peso semântico).

## Batch Processing

```python
async def embed_batch(texts: list[str]) -> list[list[float]]:
    response = await client.embeddings.create(
        input=texts,
        model="text-embedding-3-small",
        dimensions=512
    )
    return [item.embedding for item in response.data]
```

Limites da OpenAI API:
- Max 8192 tokens por texto individual
- Max 2048 textos por batch request
- Rate limit varia por tier

## Strategy Pattern (Recomendado)

Para suportar múltiplos providers, usar interface base:

```python
from abc import ABC, abstractmethod

class EmbeddingProvider(ABC):
    @abstractmethod
    async def embed(self, text: str) -> list[float]: ...
    
    @abstractmethod
    async def embed_batch(self, texts: list[str]) -> list[list[float]]: ...

class OpenAIEmbeddingProvider(EmbeddingProvider):
    async def embed(self, text: str) -> list[float]:
        # implementação OpenAI
        ...

class SentenceTransformerProvider(EmbeddingProvider):
    async def embed(self, text: str) -> list[float]:
        # implementação local
        ...
```

## Regras

- Nunca mudar o modelo de embedding sem reindexar toda a collection
- Sempre usar a mesma dimensão no embedding e na collection Qdrant
- Truncar textos longos (>500 chars details) para evitar ruído semântico
- Batch quando possível para reduzir latência e custo
- Guardar o nome do modelo e dimensão no `.env` para rastreabilidade
