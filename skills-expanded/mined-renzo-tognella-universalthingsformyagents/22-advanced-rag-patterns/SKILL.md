---
name: Advanced RAG Patterns
description: Use when improving retrieval quality, implementing self-reflective retrieval, query transformation, reranking, semantic caching, or choosing between RAG strategies for TheSearch's hybrid search.
---

# Advanced RAG Patterns

## Quando Usar

- Ao melhorar qualidade de retrieval (reranking, query transformation)
- Ao implementar validação/reflexão sobre resultados recuperados
- Ao decidir estratégia de RAG para um tipo de query
- Ao adicionar cache semântico para queries repetidas

## Estado Atual: RRF Básico

TheSearch usa busca híbrida (Qdrant + Neo4j) com Reciprocal Rank Fusion:

```
Query → Filtro → Busca Vetorial + Busca Estrutural → RRF → Diversificação → Resultado
```

Funciona, mas não tem reflexão, transformação de query, ou reranking profundo.

## Padrões Avançados

### 1. Self-RAG: Retrieval com Reflexão

Após recuperar, o LLM avalia se o resultado é útil antes de usar.

```python
REFLECTION_PROMPT = """
Given the query: {query}
And this retrieved memory: {memory_title}: {memory_summary}

Evaluate:
1. is_relevant: Does this memory address the query? (yes/no)
2. is_supported: Is the memory well-evidenced? (yes/no)
3. is_faithful: Can we trust using this memory for answering? (yes/no)

Respond as JSON: {{"is_relevant": bool, "is_supported": bool, "is_faithful": bool}}
"""

async def self_rag_filter(query: str, results: list[dict]) -> list[dict]:
    filtered = []
    for result in results:
        reflection = await llm.extract(
            REFLECTION_PROMPT.format(query=query, **result),
            response_model=ReflectionResult,
        )
        if reflection.is_relevant and reflection.is_faithful:
            result["reflection"] = reflection
            filtered.append(result)
    return filtered
```

**Quando usar:** Queries críticas onde resposta errada é pior que sem resposta.

### 2. Corrective RAG (CRAG): Fallback Inteligente

Se confiança nos resultados é baixa, tentar estratégia alternativa.

```python
async def corrective_rag(query: str, project: str) -> list[dict]:
    results = await hybrid_search.search(query, project, top_k=5)

    confidence = calculate_confidence(results)
    # confidence = média dos scores RRF dos top-3

    if confidence > 0.5:
        return results

    if confidence > 0.2:
        enhanced_query = await transform_query(query)
        return await hybrid_search.search(enhanced_query, project, top_k=8)

    return await broad_search(project, category_filter=None, top_k=10)
```

**Quando usar:** Queries ambíguas ou em domínios com poucas memórias.

### 3. Query Transformation: HyDE

Gerar documento hipotético para melhorar embedding da query.

```python
HYDE_PROMPT = """
Given this question, write a brief answer as if you had the knowledge.
This hypothetical answer will be used to find similar content.

Question: {query}
"""

async def hyde_search(query: str, project: str) -> list[dict]:
    hypothetical = await llm.generate(HYDE_PROMPT.format(query=query))
    return await hybrid_search.search(hypothetical, project, top_k=5)
```

**Quando usar:** Queries curtas ou vagas onde o embedding direto é fraco.

### 4. Query Transformation: Step-Back Prompting

Abstrair a query para um nível conceitual mais alto.

```python
STEPBACK_PROMPT = """
You are given a specific question. Generate a more general, higher-level question
that captures the underlying concept.

Specific: {query}
General:
"""

async def stepback_search(query: str, project: str) -> list[dict]:
    general = await llm.generate(STEPBACK_PROMPT.format(query=query))
    specific_results = await hybrid_search.search(query, project, top_k=3)
    general_results = await hybrid_search.search(general, project, top_k=3)
    return reciprocal_rank_fusion([specific_results, general_results])
```

**Quando usar:** Queries muito específicas que podem não ter match direto.

### 5. Multi-Query Retrieval

Gerar múltiplas variantes da query e fundir resultados.

```python
MULTIQUERY_PROMPT = """
Generate 3 different phrasings of this question, capturing different angles:
Original: {query}
"""

async def multi_query_search(query: str, project: str) -> list[dict]:
    variants = await llm.extract(
        MULTIQUERY_PROMPT.format(query=query),
        response_model=QueryVariants,
    )
    all_results = []
    for variant in [query] + variants.queries:
        results = await hybrid_search.search(variant, project, top_k=5)
        all_results.append(results)
    return reciprocal_rank_fusion(all_results)
```

**Quando usar:** Queries complexas com múltiplas facetas.

### 6. Reranking com Cross-Encoder

Após RRF, aplicar modelo mais profundo para reranking final.

```python
async def rerank_results(query: str, results: list[dict], top_n: int = 5) -> list[dict]:
    pairs = [(query, f"{r['title']}: {r['summary']}") for r in results]
    scores = cross_encoder.predict(pairs)

    for result, score in zip(results, scores):
        result["rerank_score"] = float(score)

    return sorted(results, key=lambda x: -x["rerank_score"])[:top_n]
```

**Modelos:** `bge-reranker-v2-m3` (local) ou `Cohere Rerank v3` (API).

**Quando usar:** Sempre que possível — melhora precisão em ~10-20%.

### 7. Agentic RAG: Retrieval Iterativo

O agente decide quando e como buscar, iterativamente.

```python
async def agentic_rag(question: str, project: str, max_iterations: int = 3) -> dict:
    context = []
    for i in range(max_iterations):
        results = await hybrid_search.search(question, project, top_k=5)
        context.extend(results)

        decision = await llm.extract(
            f"Question: {question}\nContext: {context}\n"
            "Is the context sufficient to answer? (sufficient/insufficient/refine)",
            response_model=RAGDecision,
        )

        if decision.status == "sufficient":
            break
        question = decision.refined_query or question

    return {"context": context, "iterations": i + 1}
```

**Quando usar:** Queries complexas que exigem múltiplas buscas encadeadas.

### 8. Semantic Cache

Cache de queries semanticamente similares.

```python
async def cached_search(query: str, project: str, similarity_threshold: float = 0.95) -> list[dict]:
    query_embedding = await embed(query)

    cache_hit = await qdrant.search(
        collection="query_cache",
        query_vector=query_embedding,
        query_filter=Filter(must=[
            FieldCondition(key="project", match=MatchValue(value=project)),
        ]),
        limit=1,
        score_threshold=similarity_threshold,
    )

    if cache_hit:
        return json.loads(cache_hit[0].payload["results"])

    results = await hybrid_search.search(query, project, top_k=5)

    await qdrant.upsert(
        collection="query_cache",
        points=[{
            "id": str(uuid4()),
            "vector": query_embedding,
            "payload": {
                "project": project,
                "query": query,
                "results": json.dumps(results),
                "cached_at": datetime.utcnow().isoformat(),
            },
        }],
    )

    return results
```

**Quando usar:** Queries repetidas do agente em loops (ex: pre-task loading).

### 9. Adaptive RAG: Seleção por Complexidade

```python
async def adaptive_search(query: str, project: str) -> list[dict]:
    complexity = await classify_complexity(query)

    if complexity == "simple":
        return await hybrid_search.search(query, project, top_k=3)
    elif complexity == "moderate":
        results = await hybrid_search.search(query, project, top_k=5)
        return await rerank_results(query, results)
    else:
        return await agentic_rag(query, project, max_iterations=3)
```

## Decisão: Qual Padrão Usar

```
Query simples, direta → RRF básico (estado atual)
Query vaga/curta       → HyDE + RRF
Query complexa         → Multi-Query + Reranking
Query crítica          → Self-RAG (reflexão)
Poucas memórias        → CRAG (fallback)
Query repetida         → Semantic Cache
Query exploratória     → Agentic RAG (iterativo)
```

## Path de Adoção

| Fase | Padrão | Prioridade |
|------|--------|:----------:|
| Atual | RRF básico | ✅ |
| 3.1 | Reranking (cross-encoder) | Alta |
| 3.2 | Semantic Cache | Alta |
| 3.3 | HyDE para queries curtas | Média |
| 4.1 | Self-RAG para queries críticas | Média |
| 4.2 | Multi-Query para queries complexas | Baixa |
| 5.0 | Agentic RAG iterativo | Baixa |

## Erros Comuns

- Aplicar todos os padrões de uma vez — implementar incrementalmente com medição
- HyDE sem benchmark — pode piorar queries que já funcionam bem
- Cross-encoder em todo resultado — custoso, aplicar só no top-10 do RRF
- Semantic cache com threshold baixo — retorna resultados errados
- Self-RAG em queries simples — adiciona latência sem ganho

## Referências

- `knogdement/04_advanced_rag.md` — fonte completa de pesquisas
- Self-RAG (Asai et al.) — reflection tokens: is_relevant, is_supported, is_faithful
- CRAG (Yan et al.) — confidence-triggered retrieval
- HyDE (Gao et al.) — Hypothetical Document Embeddings
- ColBERT — late interaction reranking
- Adaptive-RAG (Jeong et al.) — query complexity classification
- DSPy — systematic RAG pipeline optimization
