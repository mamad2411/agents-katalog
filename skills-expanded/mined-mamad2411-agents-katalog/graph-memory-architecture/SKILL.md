---
name: Graph Memory Architecture
description: Use when modifying the Neo4j graph model, adding node/relationship types, implementing Personalized PageRank retrieval, hierarchical context trees, spreading activation, or community detection for memory.
---

# Graph Memory Architecture

## Quando Usar

- Ao estender o modelo do grafo com novos tipos de nó ou relação
- Ao implementar algoritmos de retrieval sobre o grafo (PageRank, spreading activation)
- Ao projetar estruturas hierárquicas (context trees, comunidades)
- Ao avaliar qual técnica de graph memory aplicar a um problema

## Modelo Atual (Fase 2)

```
(:Project)-[:HAS_CATEGORY]->(:Category)
(:MemoryItem)-[:IN_PROJECT]->(:Project)
(:MemoryItem)-[:IN_CATEGORY]->(:Category)
(:MemoryItem)-[:ABOUT_DOMAIN]->(:Domain)
(:MemoryItem)-[:SUPPORTED_BY]->(:Evidence)

# Inter-memória
(:MemoryItem)-[:RELATED_TO]->(:MemoryItem)
(:MemoryItem)-[:DEPENDS_ON]->(:MemoryItem)
(:MemoryItem)-[:REFINES]->(:MemoryItem)
(:MemoryItem)-[:DEPRECATES]->(:MemoryItem)
(:MemoryItem)-[:CONFLICTS_WITH]->(:MemoryItem)
(:MemoryItem)-[:EVOLVES_FROM]->(:MemoryItem)
```

## Técnicas de Graph Memory por Pesquisa

### 1. Personalized PageRank (HippoRAG, GAAMA)

Inspirado no hipocampo: query vira nó-semente, PageRank propaga relevância pelo grafo.

```cypher
// Neo4j GDS — Personalized PageRank a partir de um nó-semente
CALL gds.pageRank.stream('memory-graph', {
  sourceNodes: [seed_node],
  relationshipTypes: ['RELATED_TO', 'REFINES', 'DEPENDS_ON'],
  maxIterations: 20,
  dampingFactor: 0.85
})
YIELD nodeId, score
WITH gds.util.asNode(nodeId) AS node, score
WHERE node.status = 'active'
RETURN node.memory_id AS memory_id, node.title AS title, score
ORDER BY score DESC
LIMIT 10
```

**Quando usar:** Query exploratória onde vizinhos de vizinhos importam. Ex: "quais decisões arquiteturais afetam esse padrão?"

### 2. Hierarchical Context Tree (ByteRover)

Memória organizada em árvore de arquivos/conceitos — cada nó herda contexto do pai.

```cypher
// Modelo proposto
(:ContextNode)-[:PARENT_OF]->(:ContextNode)
(:MemoryItem)-[:LOCATED_IN]->(:ContextNode)

// Query: buscar com herança de contexto
MATCH (root:ContextNode {path: 'src/api'})
MATCH (root)-[:PARENT_OF*0..]->(descendant)
MATCH (m:MemoryItem)-[:LOCATED_IN]->(descendant)
WHERE m.status = 'active'
RETURN DISTINCT m
ORDER BY m.effective_weight DESC
```

**Quando usar:** Projetos com estrutura hierárquica natural (módulos, pacotes, domínios).

### 3. Spreading Activation (SuperLocalMemory, SCM)

Ativação se propaga pelo grafo a partir de nós relevantes, decaindo com distância.

```python
async def spreading_activation(
    seed_ids: list[str],
    decay: float = 0.7,
    max_hops: int = 3,
    threshold: float = 0.1,
) -> list[tuple[str, float]]:
    activated = {sid: 1.0 for sid in seed_ids}
    frontier = set(seed_ids)

    for hop in range(max_hops):
        next_frontier = set()
        query = """
        UNWIND $seeds AS sid
        MATCH (m:MemoryItem {memory_id: sid})-[r]-(neighbor:MemoryItem)
        WHERE neighbor.status = 'active'
        RETURN DISTINCT neighbor.memory_id AS nid, type(r) AS rel_type
        """
        results = await neo4j_session.run(query, seeds=list(frontier))
        async for record in results:
            nid = record["nid"]
            activation = activated.get(nid, 0.0) + decay ** (hop + 1)
            if activation >= threshold:
                activated[nid] = activation
                next_frontier.add(nid)
        frontier = next_frontier
        if not frontier:
            break

    return sorted(activated.items(), key=lambda x: -x[1])
```

**Quando usar:** Encontrar memórias conectadas indiretamente. Complementa busca vetorial.

### 4. Community Detection (Microsoft GraphRAG)

Detectar comunidades (Louvain/Label Propagation) e gerar resumos por comunidade.

```cypher
// Criar projeção in-memory e detectar comunidades
CALL gds.louvain.stream('memory-graph', {
  relationshipTypes: ['RELATED_TO', 'REFINES', 'DEPENDS_ON'],
  includeIntermediateCommunities: true
})
YIELD nodeId, communityId
WITH gds.util.asNode(nodeId) AS node, communityId
SET node.community_id = communityId
```

```cypher
// Buscar por comunidade (visão global)
MATCH (m:MemoryItem)
WHERE m.community_id = $community_id AND m.status = 'active'
RETURN m.category AS category, collect(m.title) AS memories
```

**Quando usar:** Queries globais tipo "quais são os temas principais deste projeto?"

### 5. Graph Chain-of-Thought (Graph-CoT)

Raciocínio passo-a-passo sobre o grafo: explorar relações antes de responder.

```python
async def graph_cot_reasoning(question: str, project: str) -> dict:
    relevant = await hybrid_search.search(question, project, top_k=3)

    relations = await neo4j_session.run("""
    UNWIND $ids AS mid
    MATCH (m:MemoryItem {memory_id: mid})-[r]-(neighbor:MemoryItem)
    WHERE neighbor.status = 'active'
    RETURN m.memory_id AS source, type(r) AS rel, neighbor.memory_id AS target,
           neighbor.title AS target_title
    """, ids=[r["memory_id"] for r in relevant])

    reasoning_chain = []
    async for rec in relations:
        reasoning_chain.append(
            f"{rec['source']} --[{rec['rel']}]--> {rec['target_title']}"
        )

    return {"reasoning_chain": reasoning_chain, "memories": relevant}
```

**Quando usar:** Queries que exigem raciocínio multi-hop (ex: "por que essa decisão foi tomada?").

### 6. Episodic + Semantic Memory (AriGraph)

Separação entre conhecimento factual (semântico) e experiências (episódico).

```cypher
// Modelo proposto
(:EpisodicMemory)-[:INVOLVES]->(:MemoryItem)
(:EpisodicMemory)-[:OCCURRED_IN]->(:Context {session_id, task_type})

// Propriedades de EpisodicMemory:
// - occurred_at, outcome, agents_involved, lesson_learned
```

**Quando usar:** Registrar não só "o quê" mas "como e por quê" — decisões em contexto.

## Modelo Proposto (Fase 4+)

```
# Nós existentes
(:Project), (:Category), (:Domain), (:MemoryItem), (:Evidence)

# Nós novos
(:ContextNode {path, summary})          # Hierarchical Context Tree
(:EpisodicMemory {occurred_at, outcome}) # Episodic layer
(:Community {id, summary})              # Community summaries

# Relações novas
(:ContextNode)-[:PARENT_OF]->(:ContextNode)
(:MemoryItem)-[:LOCATED_IN]->(:ContextNode)
(:EpisodicMemory)-[:INVOLVES]->(:MemoryItem)
(:EpisodicMemory)-[:OCCURRED_IN]->(:Context)
(:MemoryItem)-[:BELONGS_TO_COMMUNITY]->(:Community)
```

## Quando Usar Qual Técnica

| Cenário | Técnica | Custo |
|---------|---------|:-----:|
| Query local, vizinhos diretos | Spreading Activation | Baixo |
| Query exploratória, vizinhos distantes | Personalized PageRank | Médio |
| Visão global do projeto | Community Detection | Alto (batch) |
| Raciocínio sobre relações | Graph Chain-of-Thought | Médio |
| Contexto hierárquico (código, domínios) | Hierarchical Context Tree | Baixo |
| Registro de experiências | Episodic Memory | Baixo |

## Migração (Path Seguro)

1. **Fase 2 atual:** Modelo flat com RELATED_TO — funciona, não mexer até estabilizar
2. **Fase 3:** Adicionar ContextNodes para projetos com estrutura natural
3. **Fase 4:** Personalized PageRank como retrieval complementar (atrás do RRF)
4. **Fase 4+:** Community detection em batch (consolidação diferida)

## Erros Comuns

- Usar PageRank para queries simples — overkill, usar busca direta
- Criar ContextNodes automaticamente sem curadoria — gera ruído
- Community detection em grafo pequeno (<50 nós) — resultados instáveis
- Ignorar pesos existentes ao implementar spreading activation — combinar scores
- Migração sem manter retrocompatibilidade — quebrar queries existentes

## Referências

- `knogdement/01_graphs_llm_memory.md` — fonte completa de pesquisas
- HippoRAG (NeurIPS'24) — hippocampal indexing
- GAAMA — Graph Augmented Associative Memory
- ByteRover — Hierarchical Context Tree
- SuperLocalMemory V3.3 — spreading activation + Ebbinghaus
- Microsoft GraphRAG — community detection + summarization
- Graph Chain-of-Thought (ACL'24) — reasoning over graphs
