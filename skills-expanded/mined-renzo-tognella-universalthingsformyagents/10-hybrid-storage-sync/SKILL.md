---
name: Hybrid Storage Sync
description: Persistência dual Neo4j+Qdrant, sincronização por memory_id, padrões de consistência, Saga Pattern, e recovery de falhas.
---

# Hybrid Storage Sync

## Quando Usar

- Ao persistir MemoryItems no armazenamento dual
- Ao debugar divergências entre grafo e vetor
- Ao implementar recovery de falhas de persistência

## Arquitetura de Armazenamento

```
┌─────────────┐         memory_id          ┌─────────────┐
│   Neo4j     │ ◄──── MESMO ID ────────►   │   Qdrant    │
│  (grafo)    │                             │  (vetor)    │
│             │                             │             │
│  Estrutura  │                             │  Embedding  │
│  Relações   │                             │  Payload    │
│  Navegação  │                             │  Busca sem. │
└─────────────┘                             └─────────────┘
```

## Regra de Ouro

> O `memory_id` PRECISA ser o MESMO nos dois lados.

```python
memory_id = MemoryItem.generate_id(project, category, title)
# Usado no Neo4j como propriedade do nó
# Usado no Qdrant como payload E para gerar o point_id (uuid5)
```

## Fluxo de Persistência

```python
async def persist(candidate, admission):
    # 1. Gerar embedding
    text = embeddings.build_text_for_embedding(title, summary, details)
    embedding = await embeddings.embed(text)
    
    # 2. Salvar no Qdrant (vetor + payload)
    qdrant.upsert(memory_id, embedding, item)
    
    # 3. Salvar no Neo4j (nó + relações)
    await neo4j.upsert_memory(memory_id, project, category, domains, ...)
```

## Problema: Atomicidade

Não há transação distribuída entre Neo4j e Qdrant. Se um falhar:

| Cenário | Estado |
|---------|--------|
| Qdrant OK + Neo4j OK | ✅ Consistente |
| Qdrant OK + Neo4j FALHA | ⚠️ Vetor sem grafo |
| Qdrant FALHA + Neo4j OK | ⚠️ Grafo sem vetor |
| Ambos FALHAM | ❌ Nada persistido (OK) |

## Estratégias de Consistência

### 1. Write-Ahead Log (MVP)

```python
async def persist_with_wal(candidate):
    # 1. Registrar intenção
    wal_entry = {"memory_id": mid, "status": "pending", "timestamp": now()}
    save_wal(wal_entry)
    
    # 2. Persistir sequencialmente
    try:
        qdrant.upsert(mid, embedding, item)
        await neo4j.upsert_memory(mid, ...)
        update_wal(mid, "committed")
    except Exception:
        update_wal(mid, "failed")
        raise
```

### 2. Saga Pattern (Produção)

```python
async def persist_saga(candidate):
    try:
        qdrant.upsert(mid, embedding, item)
    except:
        raise  # Nada para compensar
    
    try:
        await neo4j.upsert_memory(mid, ...)
    except:
        # Compensação: remover do Qdrant
        qdrant.delete(mid)
        raise
```

### 3. Reconciliação na Consolidação

A consolidação diferida (Task 17) deve incluir:

```python
async def reconcile_stores():
    # IDs no Qdrant
    qdrant_ids = set(qdrant.get_all_memory_ids())
    # IDs no Neo4j
    neo4j_ids = set(await neo4j.get_all_memory_ids())
    
    # Divergências
    only_qdrant = qdrant_ids - neo4j_ids
    only_neo4j = neo4j_ids - qdrant_ids
    
    # Resolver
    for mid in only_qdrant:
        # Recriar no Neo4j OU deletar do Qdrant
        ...
```

## Ações Suportadas

| Ação | Qdrant | Neo4j |
|------|--------|-------|
| create | Novo point | Novo nó + relações |
| update | Sobrescreve point | ON MATCH SET |
| refine | Novo point | Novo nó + `REFINES` |
| deprecate | Status→deprecated | Status→deprecated + `DEPRECATES` |

## Regras

- `memory_id` idêntico nos dois stores — inviolável
- Salvar Qdrant primeiro (mais fácil de compensar)
- Qdrant point_id = `uuid5(uuid.NAMESPACE_DNS, memory_id)` — determinístico
- Implementar reconciliação na consolidação diferida
- Logging de toda operação de persistência (auditoria)
