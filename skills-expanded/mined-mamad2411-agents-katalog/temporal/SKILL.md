---
name: Temporal & Episodic Memory
description: Use when implementing time-aware retrieval, memory stream architecture, episodic memory layer, spreading activation scoring, or hierarchical memory trees for TheSearch.
---

# Temporal & Episodic Memory

## Quando Usar

- Ao implementar scoring temporal (relevance × recency × importance)
- Ao criar camada de memória episódica (experiências vs conhecimento)
- Ao modelar decadência temporal com forgetting curves
- Ao construir árvores de memória hierárquicas
- Ao implementar spreading activation sobre memórias conectadas

## Estado Atual: Timestamps + Decay

TheSearch usa timestamps e decadência exponencial simples:

```python
# Skill 11 — Weight System & Decay
decay_factor = 0.5 ** (days_since / half_life)
effective_weight = composite_weight × decay_factor
```

Funciona mas não diferencia tipos de memória, não tem memória episódica, e scoring temporal é binário (decay ou não).

## Tipos de Memória (CoALA Framework)

```
┌────────────────────────────────────────────┐
│           Long-Term Memory (LTM)           │
│                                             │
│  Semantic    Episodic      Procedural       │
│  (fatos,     (experiên-    (skills,         │
│   regras,    cias, even-   rotinas,         │
│   padrões)   tos, decisões) código)         │
│                                             │
│  ← TheSearch faz isso    ← Futuro          │
│    bem                      (skill library) │
└────────────────────────────────────────────┘
```

TheSearch atualmente só modela **memória semântica**. Episódica e procedural são futuras.

## Melhoria 1: Scoring Composto (Generative Agents)

Stanford Generative Agents: `score = relevance × recency × importance`

```python
import math
from datetime import datetime, timedelta

def relevance_score(query_embedding: list[float], memory_embedding: list[float]) -> float:
    dot = sum(a * b for a, b in zip(query_embedding, memory_embedding))
    norm_q = math.sqrt(sum(a * a for a in query_embedding))
    norm_m = math.sqrt(sum(b * b for b in memory_embedding))
    return dot / (norm_q * norm_m + 1e-8)

def recency_score(last_accessed: datetime, now: datetime, decay_rate: float = 0.995) -> float:
    hours_since = (now - last_accessed).total_seconds() / 3600
    return decay_rate ** hours_since

def importance_score(memory: dict) -> float:
    base = memory.get("weight_manual", 0.5)
    evidence_bonus = min(memory.get("evidence_count", 0) * 0.1, 0.3)
    usage_bonus = min(memory.get("access_count", 0) * 0.02, 0.2)
    return min(base + evidence_bonus + usage_bonus, 1.0)

def composite_score(
    query_embedding: list[float],
    memory: dict,
    now: datetime,
    alpha: float = 0.5,
    beta: float = 0.3,
    gamma: float = 0.2,
) -> float:
    rel = relevance_score(query_embedding, memory["embedding"])
    rec = recency_score(memory["last_accessed_at"], now)
    imp = importance_score(memory)
    return alpha * rel + beta * rec + gamma * imp
```

**Pesos padrão:** α=0.5 (relevance), β=0.3 (recency), γ=0.2 (importance).

## Melhoria 2: Ebbinghaus com Reforço (MemoryBank)

Esquecimento com reforço — acessar uma memória fortalece retenção.

```python
class EbbinghausForgetting:
    def __init__(self, base_half_life_days: float = 30.0):
        self.base_half_life = base_half_life_days

    def half_life(self, memory: dict) -> float:
        significance = memory.get("significance", 0.5)
        reinforcement_count = memory.get("reinforcement_count", 0)
        reinforcement_bonus = 1.0 + (reinforcement_count * 0.5)
        return self.base_half_life * (0.5 + significance * 0.5) * reinforcement_bonus

    def retrieval_strength(self, memory: dict, now: datetime) -> float:
        days = (now - memory["last_accessed_at"]).days
        hl = self.half_life(memory)
        return 0.5 ** (days / hl)

    def reinforce(self, memory: dict) -> dict:
        memory["reinforcement_count"] = memory.get("reinforcement_count", 0) + 1
        memory["last_accessed_at"] = datetime.utcnow()
        return memory
```

**Efeito:** Cada acesso DOBRA a half-life (até saturar). Memórias frequentemente usadas decaem muito mais devagar.

## Melhoria 3: Memória Episódica

Registrar não só "o quê" mas "como, quando, por quê".

```python
from pydantic import BaseModel
from datetime import datetime

class EpisodicMemory(BaseModel):
    memory_id: str
    title: str
    occurred_at: datetime
    task_description: str
    outcome: str  # "success" | "partial" | "failure"
    lessons: list[str]
    decisions_made: list[str]
    context_snapshot: dict
    involved_semantic_ids: list[str]
    agent_id: str | None = None
```

```cypher
// Criar memória episódica
MERGE (e:EpisodicMemory {memory_id: $id})
SET e.title = $title,
    e.occurred_at = datetime($occurred_at),
    e.outcome = $outcome,
    e.lessons = $lessons,
    e.task_description = $task_description

// Conectar com memórias semânticas
UNWIND $semantic_ids AS sid
MATCH (s:MemoryItem {memory_id: sid})
MERGE (e)-[:INVOLVES]->(s)

// Recuperar episódios por similaridade de contexto
MATCH (e:EpisodicMemory)-[:INVOLVES]->(s:MemoryItem)
WHERE s.memory_id IN $current_semantic_ids
RETURN e, count(s) AS overlap
ORDER BY overlap DESC, e.occurred_at DESC
LIMIT 5
```

**Quando usar:** Pós-tarefa, registrar a experiência completa da execução.

## Melhoria 4: Spreading Activation (SCM)

Ativação se propaga pelo grafo de memórias, simulando associação cognitiva.

```python
from collections import defaultdict

async def spreading_activation_search(
    seed_memory_ids: list[str],
    project: str,
    initial_activation: float = 1.0,
    decay_factor: float = 0.6,
    max_depth: int = 3,
    threshold: float = 0.05,
) -> list[tuple[str, float]]:
    activation: dict[str, float] = defaultdict(float)

    for sid in seed_memory_ids:
        activation[sid] += initial_activation

    current_seeds = set(seed_memory_ids)

    for depth in range(max_depth):
        if not current_seeds:
            break

        query = """
        UNWIND $seeds AS sid
        MATCH (m:MemoryItem {memory_id: sid})-[r]-(neighbor:MemoryItem)
        WHERE neighbor.status = 'active'
          AND neighbor:MemoryItem-[:IN_PROJECT]->(:Project {name: $project})
        RETURN DISTINCT neighbor.memory_id AS nid, labels(neighbor) AS labels
        """
        result = await neo4j_session.run(query, seeds=list(current_seeds), project=project)

        next_seeds = set()
        async for record in result:
            nid = record["nid"]
            propagated = initial_activation * (decay_factor ** (depth + 1))
            activation[nid] += propagated
            if propagated >= threshold:
                next_seeds.add(nid)

        current_seeds = next_seeds

    ranked = sorted(activation.items(), key=lambda x: -x[1])
    return [(mid, act) for mid, act in ranked if act >= threshold]
```

**Integração com RRF:** Spreading activation scores como terceira fonte no RRF:

```python
def enhanced_rrf(
    vector_results: list[str],
    graph_results: list[str],
    activation_results: list[tuple[str, float]],
    k: int = 60,
) -> dict[str, float]:
    scores: dict[str, float] = defaultdict(float)

    for rank, doc_id in enumerate(vector_results, 1):
        scores[doc_id] += 1.0 / (k + rank)

    for rank, doc_id in enumerate(graph_results, 1):
        scores[doc_id] += 1.0 / (k + rank)

    for rank, (doc_id, act_score) in enumerate(activation_results, 1):
        scores[doc_id] += 1.0 / (k + rank) + act_score * 0.1

    return dict(sorted(scores.items(), key=lambda x: -x[1]))
```

## Melhoria 5: Memory Tree Hierárquica

Organizar memórias em árvore por granularidade — abstrato no topo, específico nas folhas.

```cypher
// Modelo
(:MemoryCluster {
  cluster_id: String,
  level: Integer,        // 0 = mais abstrato
  summary: String,
  embedding: List(Float)
})

(:MemoryCluster)-[:PARENT_CLUSTER]->(:MemoryCluster)
(:MemoryItem)-[:MEMBER_OF]->(:MemoryCluster)

// Busca top-down: começar no nível mais alto, descer onde relevante
MATCH (root:MemoryCluster {level: 0})
WHERE root.project = $project
WITH root
CALL db.index.vector.queryNodes('cluster_embeddings', 3, $query_embedding)
YIELD node, score
WHERE node.level = 0
MATCH (node)-[:PARENT_CLUSTER*0..2]->(leaf)
MATCH (m:MemoryItem)-[:MEMBER_OF]->(leaf)
WHERE m.status = 'active'
RETURN m
ORDER BY score DESC
LIMIT 10
```

**Quando usar:** Projetos com 100+ memórias onde busca flat fica ineficiente.

## Memória Temporal na Prática

### Pós-Tarefa (Integração com Agent Loop)

```python
async def post_task_episodic(
    task: str, changes: str, project: str, outcome: str
) -> dict:
    semantic_candidates = await extraction.extract_candidates(
        f"TASK: {task}\nCHANGES: {changes}", project
    )

    episode = EpisodicMemory(
        memory_id=generate_id(),
        title=f"Episode: {task[:80]}",
        occurred_at=datetime.utcnow(),
        task_description=task,
        outcome=outcome,
        lessons=await extract_lessons(task, changes, outcome),
        decisions_made=await extract_decisions(changes),
        context_snapshot={"project": project},
        involved_semantic_ids=[],
    )

    admitted_ids = []
    for candidate in semantic_candidates:
        result = await admission.evaluate(candidate)
        if result.status in ("active", "proposed"):
            item = await persistence.persist(candidate, result)
            admitted_ids.append(item.memory_id)

    episode.involved_semantic_ids = admitted_ids
    await persistence.persist_episode(episode)

    return {"episode_id": episode.memory_id, "semantic_ids": admitted_ids}
```

## Path de Adoção

| Fase | Melhoria | Impacto |
|------|----------|---------|
| 3.1 | Scoring composto (relevance × recency × importance) | Substitui decay simples |
| 3.2 | Ebbinghaus com reforço | Memórias usadas duram mais |
| 4.1 | Spreading activation como 3ª fonte RRF | Recupera conectados indiretos |
| 4.2 | Episodic memory layer | Registra experiências |
| 5.0 | Memory tree hierárquica | Escala para 100+ memórias |

## Erros Comuns

- Scoring composto sem calibrar α, β, γ — seguir default e medir
- Spreading activation sem threshold — explode para o grafo inteiro
- Episodic memory sem limite — cresce sem controle, consolidar periodicamente
- Memory tree com auto-clusterização precoce — clusters ruins pioram retrieval
- Ignorar last_accessed_at no reforço — da mesma forma que weight_usage precisa atualização
- Misturar scoring temporal com weight_decay — usar um OU outro, não ambos

## Referências

- `knogdement/02_temporal_memory_trees.md` — fonte completa de pesquisas
- Generative Agents (Park et al., Stanford) — relevance × recency × importance
- MemoryBank — Ebbinghaus Forgetting Curve com reinforcement
- CoALA (Sumers et al.) — episodic, semantic, procedural memory taxonomy
- SCM — Spreading Activation over Conversational Memory Graph
- TiM — Temporal-aware Memory for LLM agents
- Memory Mosaics (LeCun/Meta) — associative memory networks
- LoCoMo benchmark — long-term conversational memory evaluation
