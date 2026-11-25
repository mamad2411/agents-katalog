---
name: Intelligence Pipeline
description: Pipeline de inteligência da busca — Spreading Activation (3a fonte RRF), HyDE (expansão de queries vagas), Composite Scoring (relevância × recência × importância), Context Compaction e Ebbinghaus reinforcement.
---

# Intelligence Pipeline

## Quando Usar

- Ao entender como a busca encontra e rankeia resultados
- Ao ajustar parâmetros de qualidade da busca
- Ao debugar porque um resultado apareceu (ou não)

## Pipeline Completo de Busca

```
Query: "authentication"
  │
  ├─ 1. HyDE (se query < 15 chars)
  │     "authentication" → "authentication refers to verifying user identity..."
  │
  ├─ 2. Embedding + Busca paralela
  │     ├─ Qdrant (vetorial) → top-20 por cosseno
  │     ├─ Neo4j (estrutural) → top-20 por peso
  │     └─ Spreading Activation → top-20 por vizinhança no grafo
  │
  ├─ 3. RRF Fusion (3 fontes)
  │     RRF_Score(d) = Σ(1 / (60 + rank_i(d)))
  │
  ├─ 4. Diversificação (prefix 30 chars, max 2 similares)
  │
  ├─ 5. Composite Scoring
  │     score = 0.50×relevance + 0.25×recency + 0.25×importance
  │
  ├─ 6. Reranking (se configurado)
  │     Cross-encoder ou API reranker
  │
  └─ 7. Top-K final
```

## Componentes

### Spreading Activation (3a fonte RRF)

Propaga scores de sementes (top-5 vetoriais) através de relações no grafo.

```
Semente: memory_id="auth-1" (score 1.0)
  → RELATED_TO → "jwt-2" (score 0.5)
  → DEPENDS_ON → "middleware-3" (score 0.25)
```

**Parâmetros:**
- `decay=0.5` — fator de decaimento por hop
- `max_depth=2` — máximo de hops
- Score mínimo: `0.05` (ignora abaixo)

**Configuração:** Automático — `HybridSearchService` usa se `spreading_activation` estiver injetado.

**Arquivo:** `services/spreading_activation_service.py`

### HyDE (Hypothetical Document Embeddings)

Queries curtas são ruins para busca semântica. HyDE gera uma resposta hipotética e usa como query.

```
Input:  "design"          (8 chars)
Output: "design refers to architectural patterns and conventions..." (150 chars)
```

**Parâmetros:**
- `min_query_length=15` — só expande queries menores que isso
- Usa o LLM provider configurado (`LLM_PROVIDER`)

**Configuração:** Automático via `HyDEService()` no container.

**Arquivo:** `services/hyde_service.py`

### Composite Scoring

Depois do RRF, cada resultado recebe um score composto:

```
composite = 0.50 × relevance + 0.25 × recency + 0.25 × importance
```

- **relevance** = RRF score normalizado (×60, capped 1.0)
- **recency** = 0.5^(dias/90) — decai com meia-vida de 90 dias
- **importance** = média(effective_weight, significance)

**Arquivo:** `services/composite_scorer.py`

### Context Compaction

`memory.context` retorna resultados compactados:
- Top-3 por categoria (ordenado por peso)
- Summaries truncados em 200 chars
- Apenas campos essenciais (memory_id, title, summary, effective_weight)

**Configuração:** `MAX_CONTEXT_ITEMS=3`, `MAX_SUMMARY_CHARS=200`

**Arquivo:** `services/agent_loop_service.py`

### Ebbinghaus Reinforcement

Quando uma memória é recuperada e aceita (feedback positivo):
- `weight_manual` += 0.1 (reforço)
- `weight_usage` += 0.05
- Decay reseta (spacing effect)

**Método:** `WeightService.reinforce_on_retrieval(weight_manual, weight_usage, was_accepted=True)`

**Arquivo:** `services/weight_service.py`

## Ajuste Fino

| Parâmetro | Onde | Default | Efeito |
|-----------|------|---------|--------|
| HyDE threshold | `HYDE_MIN_QUERY_LENGTH` | 15 | Queries menores são expandidas |
| Spreading decay | construtor | 0.5 | Decay por hop (menor = mais agressivo) |
| Spreading depth | construtor | 2 | Max hops no grafo |
| Relevance weight | `CompositeScorer` | 0.50 | Peso da relevância no score |
| Recency weight | `CompositeScorer` | 0.25 | Peso da recência |
| Importance weight | `CompositeScorer` | 0.25 | Peso da importância |
| Recency half-life | `CompositeScorer` | 90 dias | Meia-vida do decaimento temporal |
| Reinforcement factor | `reinforce_on_retrieval` | 0.1 | Quanto sobe no acerto |

## Regras

- Spreading Activation só roda se a busca vetorial retornar resultados
- HyDE desliga automaticamente se não houver LLM client
- Composite Scoring roda sempre que injetado (não tem fallback)
- Context Compaction roda dentro de `memory.context` automaticamente
