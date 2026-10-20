---
name: Hybrid Search & RRF
description: Busca híbrida combinando vetorial (Qdrant) + estrutural (Neo4j), fusão via Reciprocal Rank Fusion, diversificação, e explicabilidade de resultados.
---

# Hybrid Search & RRF

## Quando Usar

- Ao implementar ou modificar a consulta de memórias
- Ao ajustar parâmetros de fusão e diversificação
- Ao debugar ranqueamento de resultados

## Conceito

Busca híbrida = combinar dois tipos de busca em paralelo e fundir resultados:

```
Query
  ├─ Busca Vetorial (Qdrant) → ranking por similaridade semântica
  ├─ Busca Estrutural (Neo4j) → ranking por peso/relações no grafo
  └─ Fusão RRF → ranking unificado → diversificação → resposta
```

## Pipeline de 6 Passos

### Passo 1 — Filtro Estrutural

```python
filter = Filter(must=[
    FieldCondition(key="project", match=MatchValue(value="CORE")),
    FieldCondition(key="type", match=MatchValue(value="DesignPattern")),
    FieldCondition(key="status", match=MatchValue(value="active")),
])
```

### Passo 2 — Busca Vetorial (no subconjunto filtrado)

```python
vector_results = qdrant.search(embedding, project=project, type=category, top_k=top_k * 2)
```

### Passo 3 — Busca Estrutural (em paralelo)

```cypher
MATCH (m:MemoryItem)-[:IN_PROJECT]->(p:Project {name: 'CORE'})
WHERE m.status = 'active'
OPTIONAL MATCH (m)-[:RELATED_TO]-(related)
RETURN m, collect(related) AS related_items
ORDER BY m.effective_weight DESC
LIMIT 20
```

### Passo 4 — Fusão RRF

```python
def reciprocal_rank_fusion(ranked_lists: list[list[str]], k: int = 60) -> dict[str, float]:
    """RRF_Score(d) = Σ(1 / (k + rank_i(d)))"""
    scores = {}
    for ranked_list in ranked_lists:
        for rank, doc_id in enumerate(ranked_list, start=1):
            if doc_id:
                scores[doc_id] = scores.get(doc_id, 0.0) + (1.0 / (k + rank))
    return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
```

**Por que RRF funciona:** Usa posição (rank), não score bruto. Resolve normalização entre scores incompatíveis (cosine 0-1 vs weight 0-1).

**k=60** é o valor empírico recomendado por Cormack, Clarke & Buettcher (2009).

### Passo 5 — Diversificação

Evitar retornar 10 itens quase idênticos:

```python
def diversify(fused, results, max_similar=2):
    seen_titles = {}
    diversified = {}
    for memory_id, score in fused.items():
        item = find_item(results, memory_id)
        title_prefix = item.get("title", "")[:30]
        count = seen_titles.get(title_prefix, 0)
        if count < max_similar:
            diversified[memory_id] = score
            seen_titles[title_prefix] = count + 1
    return diversified
```

### Passo 6 — Explicabilidade

Cada resultado deve incluir:

```python
{
    "memory_id": "abc123",
    "title": "Forms Pattern",
    "rrf_score": 0.0327,
    "retrieval_source": "hybrid",  # vector | graph | hybrid
    "effective_weight": 0.85,
    "related_items": ["Pattern X", "Rule Y"]
}
```

## Reranking (Fase Futura)

Após RRF, aplicar cross-encoder para reranking semântico profundo:

- **Cohere Rerank v3** (API)
- **bge-reranker-v2-m3** (open-source)
- Analisa interações token-a-token entre query e documento

## Regras

- SEMPRE filtrar por projeto antes de buscar
- Buscar 2× o top_k de cada fonte para dar margem ao RRF
- Documentos consistentes em ambas as buscas ganham score mais alto
- Diversificação por prefixo de título (30 chars) = heurística simples mas eficaz
- Top-1 vetorial sozinho NÃO decide nada crítico (regra inviolável #6)
