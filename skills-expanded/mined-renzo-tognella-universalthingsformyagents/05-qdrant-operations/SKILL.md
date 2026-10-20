---
name: Qdrant Operations
description: Operações com Qdrant — collections, upsert, busca vetorial com payload filtering, índices, e práticas de performance.
---

# Qdrant Operations

## Quando Usar

- Ao criar/gerenciar collections no Qdrant
- Ao fazer upsert ou busca de vetores
- Ao configurar payload filtering
- Ao debugar problemas de busca vetorial

## Conceitos Core

- **Collection** = tabela (conjunto de pontos vetoriais)
- **Point** = registro (id + vector + payload)
- **Payload** = metadados JSON associados ao vetor
- **Filterable HNSW** = índice que filtra DURANTE a busca (não depois)

## Criar Collection

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(host="localhost", port=6333)
client.create_collection(
    collection_name="memories",
    vectors_config=VectorParams(
        size=512,               # MUST match embedding dimensions
        distance=Distance.COSINE
    )
)
```

## Criar Payload Indexes

Indexes aceleram filtering dramaticamente:

```python
from qdrant_client.models import PayloadSchemaType

for field in ["project", "type", "status", "domain"]:
    client.create_payload_index(
        collection_name="memories",
        field_name=field,
        field_schema=PayloadSchemaType.KEYWORD
    )
```

## Upsert

```python
from qdrant_client.models import PointStruct
import uuid

point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, memory_id))
client.upsert(
    collection_name="memories",
    points=[PointStruct(
        id=point_id,
        vector=embedding,       # list[float] com 512 dims
        payload={
            "memory_id": memory_id,
            "project": "CORE",
            "type": "DesignPattern",
            "domain": ["Sazonalizacao"],
            "status": "active",
            "effective_weight": 0.75,
            "title": "Seasonal Distribution Pattern",
        }
    )]
)
```

Upsert é idempotente — mesmo `id` sobrescreve o ponto existente.

## Busca com Payload Filtering

```python
from qdrant_client.models import Filter, FieldCondition, MatchValue

results = client.search(
    collection_name="memories",
    query_vector=query_embedding,
    query_filter=Filter(
        must=[
            FieldCondition(key="project", match=MatchValue(value="CORE")),
            FieldCondition(key="status", match=MatchValue(value="active")),
        ]
    ),
    limit=10,
    score_threshold=0.0  # 0.0 = sem threshold
)
```

### Operadores de Filtro

| Operador | Função | Uso |
|----------|--------|-----|
| `must` | AND — todas devem ser verdade | `project=CORE AND status=active` |
| `should` | OR — pelo menos uma verdade | `type=DesignPattern OR type=DesignRule` |
| `must_not` | NOT — nenhuma pode ser verdade | `status != deprecated` |

### Tipos de FieldCondition

```python
# Keyword match (string exato)
FieldCondition(key="project", match=MatchValue(value="CORE"))

# Array contains
FieldCondition(key="domain", match=MatchValue(value="Sazonalizacao"))

# Range (numérico)
from qdrant_client.models import Range
FieldCondition(key="effective_weight", range=Range(gte=0.5))
```

## Detecção de Duplicatas

```python
def find_similar(embedding, project, type, threshold=0.92):
    return client.search(
        collection_name="memories",
        query_vector=embedding,
        query_filter=Filter(must=[
            FieldCondition(key="project", match=MatchValue(value=project)),
            FieldCondition(key="type", match=MatchValue(value=type)),
        ]),
        limit=5,
        score_threshold=threshold  # >= 0.92 = duplicata provável
    )
```

## Dashboard e Debug

```bash
# Dashboard web
open http://localhost:6333/dashboard

# Info da collection
curl http://localhost:6333/collections/memories

# Contar pontos
curl http://localhost:6333/collections/memories/points/count
```

## Regras

- SEMPRE criar payload indexes antes de inserir dados
- O `id` do ponto DEVE ser determinístico (uuid5 do memory_id)
- Filtros são aplicados DURANTE a busca HNSW (eficiente)
- `score_threshold` filtra resultados com score abaixo do limiar
- Nunca mudar `vector_size` de uma collection existente — recriar
- Usar `AsyncQdrantClient` para consistência com o código async
