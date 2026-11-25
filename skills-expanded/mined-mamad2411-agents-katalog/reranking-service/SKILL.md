---
name: Reranking Service
description: Reranking semântico pós-fusão — Cross-Encoder local, Cohere API, Jina API. Configuração, trade-offs e quando usar cada provider.
---

# Reranking Service

## Quando Usar

- Ao configurar ou trocar o provider de reranking
- Ao debugar qualidade de resultados de busca
- Ao avaliar impacto do reranking na precisão

## O que é Reranking

Após a busca híbrida (RRF), o reranker reordena documentos analisando a interação token-a-token entre query e documento. É mais preciso que similaridade de cosseno porque entende relações semânticas profundas.

```
Query: "how to handle auth errors"
  → RRF retorna top-20 por rank
  → Reranker analisa query vs cada documento
  → Reordena por relevância real
  → Retorna top-10 final
```

## Providers

### 1. Cross-Encoder Local (padrão recomendado)

```
RERANKER_PROVIDER=local
```

- **Modelo:** `cross-encoder/ms-marco-MiniLM-L-6-v2` (12MB)
- **Custo:** Grátis, roda offline
- **Qualidade:** Boa (MS MARCO treinado)
- **Latência:** ~50ms por query com 20 docs
- **Setup:** Nenhum — `sentence-transformers` já é dependência

Modelo alternativo (mais preciso, maior):
```
RERANKER_MODEL=cross-encoder/ms-marco-MiniLM-L-12-v2
```

### 2. Cohere (melhor qualidade)

```
RERANKER_PROVIDER=cohere
COHERE_API_KEY=sua-chave
```

- **Modelo:** `rerank-v3.5`
- **Custo:** Pago por request
- **Qualidade:** Estado da arte
- **Latência:** ~200ms (rede)

### 3. Jina AI (grátis até 1000/mês)

```
RERANKER_PROVIDER=jina
JINA_API_KEY=sua-chave
```

- **Modelo:** `jina-reranker-v2-base-multilingual`
- **Custo:** 1000 requests/mês grátis
- **Qualidade:** Muito boa, suporta multilíngue
- **Latência:** ~150ms (rede)

### 4. NoOp (sem reranking)

```
RERANKER_PROVIDER=none
```

- Retorna documentos na ordem do RRF
- Use para comparação A/B ou debug

## Como Funciona

```python
# HybridSearchService chama automaticamente:
if self.reranker and query_text:
    pre_rerank = await self.reranker.rerank(
        query=query_text,
        documents=pre_rerank,
        top_k=top_k,
    )
```

Cada documento recebe `rerank_score` (0.0-1.0) indicando relevância.

## Decisão de Provider

| Cenário | Recomendação |
|---------|-------------|
| Desenvolvimento local | `local` |
| Produção com orçamento | `jina` (free tier) |
| Produção máxima qualidade | `cohere` |
| Debugando busca | `none` (comparar com/sem) |

## Arquitetura

```
services/reranking_service.py
├── NoOpReranker          → fallback, retorna inalterado
├── CrossEncoderReranker   → sentence-transformers local
├── CohereReranker         → API Cohere
├── JinaReranker           → API Jina
└── create_reranker()      → factory com fallback seguro
```

Todos implementam `Reranker` ABC de `services/abstractions.py`.

## Regras

- Se API key falta, `create_reranker()` faz fallback para `NoOpReranker`
- Se API falha durante request, retorna documentos na ordem original
- Cross-encoder carrega modelo lazy (primeira chamada)
- Texto extraído de `title | summary | details[:300]`
