---
name: Hybrid AI Systems (Neurosymbolic)
description: Use when combining symbolic reasoning (Neo4j graph) with neural reasoning (embeddings + LLM) in TheSearch, designing constraint-based retrieval, deciding between deterministic vs fuzzy operations, or validating neural outputs with symbolic checks.
---

# Hybrid AI Systems (Neurosymbolic)

## Quando Usar

- Ao decidir se uma operação deve ser determinística ou usar LLM
- Ao projetar retrieval que combina estrutura de grafo + busca vetorial
- Ao validar outputs de LLM com checks simbólicos
- Ao arquitetar pipelines que misturam graph + vector + LLM
- Ao avaliar confiança entre raciocínio simbólico vs neural

## Conceito Fundamental

TheSearch é um **sistema híbrido neurosymbolic**: combina raciocínio simbólico (Neo4j knowledge graph — determinístico, audível, estruturado) com raciocínio neural (embeddings + LLM — probabilístico, flexível, fuzzy). O poder do sistema vem de saber **quando confiar em cada paradigma**.

```
┌─────────────────────────────────────────────┐
│           TheSearch Hybrid Architecture      │
│                                              │
│  SYMBOLIC (Neo4j)    NEURAL (LLM/Qdrant)    │
│  ─────────────────   ────────────────────── │
│  Deduplication       Extraction              │
│  Weight calc         Summarization           │
│  Relation traversal  Semantic search         │
│  Constraint check    Classification          │
│  Audit trail         Similarity scoring      │
└─────────────────────────────────────────────┘
```

## 1. Quando Usar Symbolic vs Neural

| Operação | Paradigma | Porquê |
|----------|-----------|--------|
| Deduplicação por memory_id | Symbolic | ID comparison é determinística |
| Cálculo de peso composto | Symbolic | Fórmula matemática exata |
| Validação de categoria | Symbolic | Enum finito, não precisa de LLM |
| Validação de relação | Symbolic | Whitelist de relações válidas |
| Extração de candidatos | Neural | Texto livre → structured knowledge |
| Classificação semântica | Neural | Ambiguidade requer understanding |
| Busca por similaridade | Neural | "O que é parecido com X?" |
| Sumarização | Neural | Texto → texto condensado |
| Racial de decisão | Neural | Interpretar contexto e trade-offs |
| Merge de duplicatas | Hybrid | Neural detecta similaridade, symbolic decide merge |

**Regra de ouro:** Se a operação pode ser expressa como uma fórmula ou lookup, use symbolic. Se requer interpretação de texto ou julgamento subjetivo, use neural.

## 2. Constraint-Based Retrieval: Grafo Guiando Busca Vetorial

```python
async def constrained_search(query: str, project: str, top_k: int = 10) -> list[dict]:
    graph_constraints = await neo4j_session.run(
        """
        MATCH (m:Memory {project: $project, status: 'active'})
        WHERE m.weight >= 0.5
        MATCH (m)-[r:RELATED_TO|DEPENDS_ON]->(related:Memory)
        WHERE related.status = 'active'
        RETURN m.memory_id AS memory_id,
               m.category AS category,
               m.weight AS weight,
               collect(related.memory_id) AS related_ids
        ORDER BY m.weight DESC
        LIMIT $limit
        """,
        project=project,
        limit=top_k * 3
    )
    
    candidate_ids = {r["memory_id"] for r in graph_constraints}
    
    vector_results = await qdrant_client.search(
        collection_name=f"memories_{project}",
        query_vector=await embed(query),
        query_filter={
            "must": [
                {"key": "memory_id", "match": {"any": list(candidate_ids)}},
                {"key": "status", "match": {"value": "active"}},
            ]
        },
        limit=top_k
    )
    
    return enrich_with_graph_metadata(vector_results, graph_constraints)
```

**Padrão:** Graph define o espaço de busca (quem é válido), vector ordena por relevância (quem é mais similar). Combina precisão estrutural com flexibilidade semântica.

### Path-Constrained Retrieval (PCR)

```python
async def path_constrained_search(
    query: str, project: str,
    path_pattern: str = "(m:Memory)-[:RELATED_TO*1..3]->(target:Memory)",
    min_weight: float = 0.5
) -> list[dict]:
    path_results = await neo4j_session.run(
        f"""
        MATCH {path_pattern}
        WHERE m.project = $project AND m.weight >= $min_weight
        WITH DISTINCT m, length(p) as path_distance
        ORDER BY path_distance ASC, m.weight DESC
        LIMIT 50
        RETURN m.memory_id AS id, m.title AS title, path_distance
        """,
        project=project, min_weight=min_weight
    )
    
    constrained_ids = [r["id"] for r in path_results]
    
    return await qdrant_client.search(
        collection_name=f"memories_{project}",
        query_vector=await embed(query),
        query_filter={"must": [{"key": "memory_id", "match": {"any": constrained_ids}}]},
        limit=10
    )
```

## 3. Operações Determinísticas para Caminhos Críticos

### Deduplicação Symbolic + Neural

```python
async def deduplicate(candidate: MemoryCandidate, project: str) -> DeduplicationResult:
    exact_match = await neo4j_session.run(
        "MATCH (m:Memory {title: $title, project: $project}) RETURN m",
        title=candidate.title, project=project
    )
    if exact_match:
        return DeduplicationResult(action="exact_duplicate", existing_id=exact_match[0]["m"]["memory_id"])
    
    similar = await qdrant_client.search(
        collection_name=f"memories_{project}",
        query_vector=candidate.embedding,
        query_filter={"must": [{"key": "category", "match": {"value": candidate.category}}]},
        score_threshold=0.92,
        limit=5
    )
    
    if similar:
        return DeduplicationResult(action="potential_duplicate", candidates=similar)
    
    return DeduplicationResult(action="unique")
```

### Cálculo de Peso Composto (Symbolic puro)

```python
def calculate_composite_weight(memory: Memory) -> float:
    w_decay = math.exp(-DECAY_RATE * days_since(memory.last_accessed))
    w_usage = min(memory.access_count / USAGE_NORMALIZATION, 1.0)
    w_feedback = memory.feedback_score
    w_category = CATEGORY_WEIGHTS.get(memory.category, 0.5)
    w_recency = recency_factor(memory.created_at)
    
    return (
        DECAY_LAMBDA * w_decay +
        USAGE_LAMBDA * w_usage +
        FEEDBACK_LAMBDA * w_feedback +
        CATEGORY_LAMBDA * w_category +
        RECENCY_LAMBDA * w_recency
    )
```

**Nunca** usar LLM para calcular pesos — é determinístico por design.

## 4. Operações Neural para Tarefas Fuzzy

### Extração com Validação Symbolic

```python
async def extract_and_validate(text: str, project: str) -> list[MemoryCandidate]:
    candidates = await llm_extract(text, project)
    
    valid = []
    for c in candidates:
        if c.category not in VALID_CATEGORIES:
            c.category = await llm_classify(c.content, VALID_CATEGORIES)
        
        if not c.evidence:
            continue
        
        if c.proposed_weight < 0.3 or c.proposed_weight > 1.0:
            c.proposed_weight = CATEGORY_DEFAULT_WEIGHTS.get(c.category, 0.5)
        
        valid.append(c)
    
    return valid
```

**Padrão:** Neural gera, symbolic valida. LLM propõe categorias, código verifica contra enum. LLM propõe weights, código clamp ao range válido.

## 5. Validação: Checks Symbolics para Outputs Neurais

```python
def validate_extraction(result: ExtractionResult, original_text: str) -> list[str]:
    errors = []
    
    for candidate in result.candidates:
        for evidence in candidate.evidence:
            if not fuzzy_contains(original_text, evidence, threshold=0.85):
                errors.append(f"Evidence '{evidence}' not found in source text")
        
        if candidate.category not in VALID_CATEGORIES:
            errors.append(f"Invalid category: {candidate.category}")
        
        if not (0.0 <= candidate.proposed_weight <= 1.0):
            errors.append(f"Weight out of range: {candidate.proposed_weight}")
        
        if len(candidate.title) < 10:
            errors.append(f"Title too short: '{candidate.title}'")
    
    return errors
```

### Verification Pipeline

```
LLM Output → Schema Validation (Pydantic) → Business Rules (symbolic) → Evidence Check (fuzzy string match) → Persist
```

Cada etapa é um gate. Se qualquer gate falha, o candidato é rejeitado ou corrigido.

## 6. Padrões Arquiteturais

### GraphRAG no TheSearch

```python
async def graphrag_query(question: str, project: str) -> dict:
    seed_memories = await vector_search(question, project, top_k=5)
    
    graph_context = await neo4j_session.run(
        """
        UNWIND $ids AS id
        MATCH path = (m:Memory {memory_id: id})-[:RELATED_TO*1..2]-(related:Memory)
        WHERE related.project = $project AND related.status = 'active'
        RETURN path
        """,
        ids=[m.memory_id for m in seed_memories], project=project
    )
    
    enriched_context = merge_vector_graph(seed_memories, graph_context)
    
    answer = await llm_generate(
        system="Responda baseado apenas no contexto fornecido.",
        context=enriched_context,
        question=question
    )
    
    return {"answer": answer, "sources": enriched_context.source_ids}
```

### Saga Pattern para Consistência Dual (Neo4j + Qdrant)

```python
async def persist_memory(candidate: MemoryCandidate, project: str) -> Memory:
    memory_id = generate_id()
    
    try:
        await neo4j_session.run(
            """MERGE (m:Memory {memory_id: $id})
            SET m += $props""",
            id=memory_id, props=candidate.to_dict()
        )
    except Exception as e:
        raise StorageError(f"Neo4j write failed: {e}")
    
    try:
        await qdrant_client.upsert(
            collection_name=f"memories_{project}",
            points=[PointStruct(id=memory_id, vector=candidate.embedding, payload=candidate.to_dict())]
        )
    except Exception as e:
        await neo4j_session.run("MATCH (m:Memory {memory_id: $id}) DELETE m", id=memory_id)
        raise StorageError(f"Qdrant write failed, Neo4j rolled back: {e}")
    
    return Memory(memory_id=memory_id, **candidate.to_dict())
```

## Erros Comuns

| Erro | Correção |
|------|----------|
| Usar LLM para validação determinística | Schema validation, enum check, range check são mais rápidos e confiáveis |
| Ignorar graph structure na busca | Sempre combinar graph constraints com vector search |
| Não ter fallback quando LLM falha | Graceful degradation para busca puramente simbólica |
| Mixar responsabilidades neural/symbolic | Pipeline clara: neural gera, symbolic valida |
| Não compensar erros duais (Neo4j + Qdrant) | Saga pattern com rollback compensatório |
| Trust 100% em LLM output | Sempre validar com checks simbólicos |

## Referências

- **knogdement/01_graphs_llm_memory.md** — GraphRAG, Graph Neural Networks, graph memory systems
- **knogdement/10_thesearch_related.md** — Path-Constrained Retrieval, Deterministic Legal Agents, RAGdb
- **GraphRAG Survey (arXiv 2501.00309)** — Componentes de sistema GraphRAG
- **Path-Constrained Retrieval (arXiv 2511.18313)** — Structural constraints + semantic search
- **Deterministic Legal Agents (arXiv 2510.06002)** — Auditable reasoning over temporal KGs
- **RAGdb (arXiv 2602.22217)** — Embeddable vector search + structured metadata
