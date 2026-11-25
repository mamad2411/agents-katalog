---
name: Consolidation & Background Jobs
description: Consolidação diferida em background — merge de duplicates, recálculo de pesos, promoção/deprecação, scheduling, e Jaro-Winkler similarity.
---

# Consolidation & Background Jobs

## Quando Usar

- Ao implementar ou modificar jobs de consolidação
- Ao configurar scheduling de consolidação
- Ao debugar problemas de qualidade de memória

## Conceito

Consolidação = melhorar qualidade da memória sem bloquear o agente:

```
Consolidação Imediata: salva rápido no calor da tarefa (crítico)
Consolidação Diferida: refina em background (qualidade)
```

## 5 Operações da Consolidação Diferida

### 1. Merge de Near-Duplicates

```cypher
MATCH (a:MemoryItem)-[:IN_PROJECT]->(p:Project)
MATCH (b:MemoryItem)-[:IN_PROJECT]->(p)
WHERE a.memory_id < b.memory_id
  AND a.status = 'active' AND b.status = 'active'
  AND apoc.text.jaroWinklerDistance(a.title, b.title) > 0.9
RETURN a.memory_id, b.memory_id, a.effective_weight, b.effective_weight
```

- O de maior peso VENCE e DEPRECATES o perdedor
- Jaro-Winkler > 0.9 = títulos muito similares

### 2. Recálculo de Pesos

```python
async def recalculate_weights():
    items = await neo4j.get_all_active_items()
    for item in items:
        new_weight = weight_svc.calculate_effective_weight(
            item.weight_manual, item.weight_confidence,
            item.weight_usage, item.weight_feedback
        )
        await neo4j.update_weight(item.memory_id, new_weight)
```

### 3. Aplicar Decay

```python
async def apply_decay():
    items = await neo4j.get_items_with_access_dates()
    for item in items:
        decay = weight_svc.calculate_decay(item.weight_manual, item.last_accessed_at)
        new_weight = item.effective_weight * decay
        await neo4j.update_weight(item.memory_id, new_weight)
```

### 4. Promover Proposed → Active

```cypher
MATCH (m:MemoryItem)
WHERE m.status = 'proposed' AND m.evidence_count >= 2
SET m.status = 'active'
RETURN count(m) AS promoted
```

### 5. Deprecar Stale (peso < 0.1)

```cypher
MATCH (m:MemoryItem)
WHERE m.status = 'active' AND m.effective_weight < 0.1
SET m.status = 'deprecated', m.invalid_at = timestamp()
RETURN count(m) AS deprecated
```

## Scheduling

```python
# Opção 1: APScheduler (simples)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
scheduler.add_job(consolidation.run_now, 'interval', hours=6)
scheduler.start()

# Opção 2: Celery (distribuído)
@app.task
def consolidation_task(scope="all"):
    asyncio.run(consolidation.run_now(scope))

# Opção 3: Cron (externo)
# 0 */6 * * * cd /app && python -m scripts.consolidate
```

## Reconciliação de Stores

```python
async def reconcile():
    qdrant_ids = set(qdrant.get_all_ids())
    neo4j_ids = set(await neo4j.get_all_ids())
    
    only_qdrant = qdrant_ids - neo4j_ids  # Orphans no Qdrant
    only_neo4j = neo4j_ids - qdrant_ids   # Orphans no Neo4j
    
    for mid in only_qdrant:
        qdrant.delete(mid)  # ou recriar no Neo4j
    for mid in only_neo4j:
        # Reindexar no Qdrant
        ...
```

## Regras

- Consolidação NUNCA bloqueia o fluxo do agente
- Batch processing: paginar resultados, não carregar tudo
- Logging detalhado de cada operação (auditoria)
- Idempotência: rodar 2x deve gerar o mesmo resultado
- APOC deve estar habilitado para `jaroWinklerDistance`
- Frequência recomendada: a cada 6h ou após N inserções
