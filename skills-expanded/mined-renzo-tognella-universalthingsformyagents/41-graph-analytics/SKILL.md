---
name: Graph Analytics
description: Análise de grafo — Cross-Memory Synthesis (clustering por similaridade), Graph Clustering (comunidades via Cypher), Weight Propagation (PageRank alternativo), e Matryoshka multi-resolution search.
---

# Graph Analytics

## Quando Usar

- Ao descobrir memórias relacionadas que deveriam ser merged
- Ao analisar a estrutura do grafo de conhecimento
- Ao propagar importância através de relações
- Ao otimizar busca em collections grandes

## Serviços

### Cross-Memory Synthesis

Encontra clusters de memórias com títulos similares e sugere merge.

```python
from services.cross_memory_synthesis_service import CrossMemorySynthesisService

svc = CrossMemorySynthesisService(neo4j=neo4j)
clusters = await svc.find_clusters(project="CORE", min_cluster_size=2)
# [
#   {
#     "cluster_id": "a1b2c3",
#     "size": 3,
#     "titles": ["use guard clauses", "use guard clause", "using guard clauses"],
#     "memory_ids": ["m1", "m2", "m3"],
#     "avg_weight": 0.72
#   }
# ]
```

**Algoritmo:** Jaro-Winkler ≥ 0.75 no título → grupo. O(n) com prefix filtering.

**Saída:** `synthesize_cluster()` retorna análise textual do cluster.

**Arquivo:** `services/cross_memory_synthesis_service.py`

### Graph Clustering

Encontra comunidades de memórias conectadas via relações no grafo.

```python
from services.graph_clustering_service import GraphClusteringService

svc = GraphClusteringService(neo4j=neo4j)
communities = await svc.find_communities(project="CORE", min_size=2)
# [
#   {
#     "community_id": "comm-1",
#     "members": [{"memory_id": "m1", "title": "...", "weight": 0.9}],
#     "total_weight": 2.3
#   }
# ]
```

**Algoritmo:** Cypher puro — traversa relações `RELATED_TO|DEPENDS_ON|REFINES|EVOLVES_FROM` até 3 hops.

**Limitação:** Não é Leiden/Louvain — é connected components simplificado. Bom o suficiente para MVP.

**Arquivo:** `services/graph_clustering_service.py`

### Weight Propagation (PageRank alternativo)

Propaga pesos através de relações do grafo — sem plugin GDS.

```python
from services.weight_propagation_service import WeightPropagationService

svc = WeightPropagationService(neo4j=neo4j)
result = await svc.propagate_weights(project="CORE")
# {"project": "CORE", "iterations": 3, "total_updates": 47}

top = await svc.get_top_propagated(project="CORE", limit=10)
# [
#   {"memory_id": "m1", "title": "...", "original_weight": 0.5, "propagated_weight": 0.82}
# ]
```

**Algoritmo:** 3 iterações de:
```
propagated = 0.85 × avg(neighbor_weights) + 0.15 × current_weight
```

**Parâmetros:**
- `ITERATIONS=3` — convergence em 3 rounds
- `DAMPING=0.85` — fator de amortecimento (mesmo do PageRank)
- Delta mínimo: `0.001` (só atualiza se mudou significativamente)

**Resultado:** Campo `propagated_weight` no nó Neo4j.

**Arquivo:** `services/weight_propagation_service.py`

### Matryoshka Multi-Resolution Search

Busca em múltiplas resoluções — coarse search rápido, fine search preciso.

```python
from services.matryoshka_search_service import MatryoshkaSearchService

svc = MatryoshkaSearchService()
embedding = [0.1] * 768

# Stage 1: 64 dimensions, top-100 (coarse)
truncated_64 = svc.truncate_embedding(embedding, 64)

# Stage 2: 128 dimensions, top-50 (medium)
truncated_128 = svc.truncate_embedding(embedding, 128)

# Stage 3: 256 dimensions, top-20 (fine)
truncated_256 = svc.truncate_embedding(embedding, 256)

# Stage 4: full dimensions, top-10 (final)
```

**Stages configuráveis:**
```python
STAGES = [
    {"dimensions": 64,  "top_k_multiplier": 10},
    {"dimensions": 128, "top_k_multiplier": 5},
    {"dimensions": 256, "top_k_multiplier": 2},
]
```

**Quando usar:** `should_use_multi_stage()` retorna True se embedding ≥ 256d e top_k ≥ 5.

**Arquivo:** `services/matryoshka_search_service.py`

## Como Integrar no Workflow

### Consolidação semanal:
```
1. svc.propagate_weights(project="CORE")     → recalcula pesos propagados
2. svc.find_clusters(project="CORE")          → encontra candidatos a merge
3. Para cada cluster → consolidation.merge()  → merge automático
4. memory.reconcile(project="CORE")            → limpa órfãos
```

### Análise do grafo:
```
1. svc.find_communities(project="CORE")        → comunidades de conhecimento
2. top = svc.get_top_propagated(project="CORE") → memórias mais "influentes"
```

## Regras

- Cross-Memory Synthesis e Graph Clustering NÃO são MCP tools — são services internos
- Weight Propagation é idempotente — pode rodar múltiplas vezes
- Matryoshka requer embeddings ≥ 256 dimensões para ativar
- Todos usam Cypher puro (sem plugin GDS do Neo4j)
- Propagation weight é gravado em `propagated_weight` (não substitui `effective_weight`)
