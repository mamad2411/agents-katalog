---
name: Neo4j & Cypher
description: Operações com Neo4j — Cypher queries, MERGE/MATCH, property graphs, indices, driver async Python, e modelagem de grafo de conhecimento.
---

# Neo4j & Cypher

## Quando Usar

- Ao criar/modificar o grafo de conhecimento
- Ao escrever queries Cypher
- Ao modelar relações entre entidades
- Ao debugar o grafo no Neo4j Browser

## Modelo do Grafo

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

## MERGE vs CREATE

**SEMPRE use MERGE** — garantia de idempotência:

```cypher
MERGE (m:MemoryItem {memory_id: $id})
ON CREATE SET m.title = $title, m.created_at = timestamp()
ON MATCH SET m.updated_at = timestamp(), m.access_count = m.access_count + 1
```

- `ON CREATE SET` → executa só se NÃO existia
- `ON MATCH SET` → executa só se JÁ existia

## Queries Essenciais

### Bootstrap

```cypher
MERGE (p:Project {name: $project})
MERGE (c:Category {name: $category})
MERGE (p)-[:HAS_CATEGORY]->(c)
```

### Upsert com Relações

```cypher
MERGE (m:MemoryItem {memory_id: $mid})
ON CREATE SET m.title=$title, m.summary=$summary, m.status=$status,
              m.effective_weight=$weight, m.created_at=timestamp()
ON MATCH SET  m.summary=$summary, m.status=$status,
              m.effective_weight=$weight, m.updated_at=timestamp()
WITH m
MATCH (p:Project {name: $project}) MERGE (m)-[:IN_PROJECT]->(p)
WITH m
MATCH (c:Category {name: $category}) MERGE (m)-[:IN_CATEGORY]->(c)
```

### Consulta por Projeto

```cypher
MATCH (m:MemoryItem)-[:IN_PROJECT]->(p:Project {name: 'CORE'})
WHERE m.status = 'active'
OPTIONAL MATCH (m)-[:RELATED_TO]-(related)
RETURN m, collect(DISTINCT related.title) AS related_titles
ORDER BY m.effective_weight DESC
LIMIT 20
```

### Near-Duplicates (APOC)

```cypher
MATCH (a:MemoryItem)-[:IN_PROJECT]->(p:Project)
MATCH (b:MemoryItem)-[:IN_PROJECT]->(p)
WHERE a.memory_id < b.memory_id
  AND a.status = 'active' AND b.status = 'active'
  AND apoc.text.jaroWinklerDistance(a.title, b.title) > 0.9
RETURN a.memory_id, b.memory_id, a.effective_weight, b.effective_weight
```

## Driver Async Python

```python
from neo4j import AsyncGraphDatabase

driver = AsyncGraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "password")
)

async with driver.session() as session:
    result = await session.run("MATCH (n) RETURN count(n)")
    record = await result.single()
    print(record[0])

await driver.close()
```

## Atenção: Cypher Injection

NUNCA usar f-strings para construir Cypher com input do usuário:

```python
# ❌ PERIGOSO
await session.run(f"MATCH (m:MemoryItem {{title: '{user_input}'}}) RETURN m")

# ✅ SEGURO — parametrizado
await session.run("MATCH (m:MemoryItem {title: $title}) RETURN m", title=user_input)
```

Para nomes de relação dinâmicos, usar whitelist:

```python
VALID_RELS = {"RELATED_TO", "DEPENDS_ON", "REFINES", "DEPRECATES", "CONFLICTS_WITH", "EVOLVES_FROM"}
if rel_type not in VALID_RELS:
    raise ValueError(f"Relação inválida: {rel_type}")
```

## Neo4j Browser

```bash
open http://localhost:7474
# Login: neo4j / password

# Ver todo o grafo
MATCH (n)-[r]->(m) RETURN n, r, m

# Contar nós por tipo
MATCH (n) RETURN labels(n)[0] AS type, count(n) AS count
```

## Regras

- MERGE para upserts, CREATE apenas quando tem certeza que não existe
- Parametrizar TUDO — zero f-strings em queries
- Fechar o driver no shutdown (`await driver.close()`)
- Sessions são leves e reutilizáveis via connection pool
- APOC deve estar habilitado para funções de texto
