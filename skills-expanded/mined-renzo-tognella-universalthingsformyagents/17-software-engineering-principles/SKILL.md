---
name: Software Engineering Principles
description: SOLID, DRY, KISS, YAGNI, ACID, Clean Code — princípios aplicados ao contexto do TheSearch para garantir qualidade e manutenibilidade.
---

# Software Engineering Principles

## Quando Usar

- Como referência constante durante toda implementação
- Ao revisar código para compliance com princípios
- Ao tomar decisões de design e refatoração

## SOLID

### S — Single Responsibility Principle

Cada classe/módulo tem UMA única razão para mudar:

| Módulo | Responsabilidade ÚNICA |
|--------|----------------------|
| `EmbeddingService` | Gerar embeddings |
| `QdrantService` | Operações no Qdrant |
| `Neo4jService` | Operações no Neo4j |
| `AdmissionService` | Avaliar candidatos |
| `PersistenceService` | Persistir nos dois stores |
| `WeightService` | Calcular pesos |
| Tools MCP | Orquestração (thin controller) |

**Violação comum no projeto:** Tools instanciando e usando services diretamente em vez de delegar para um orquestrador.

### O — Open/Closed Principle

Aberto para extensão, fechado para modificação:

```python
# ❌ Modificar código existente para nova categoria
CATEGORIES = ["BusinessRule", "DesignPattern", "DesignRule"]  # hardcoded

# ✅ Extensível via configuração
categories = load_categories_from_config()
```

### L — Liskov Substitution Principle

Subtipos devem ser substituíveis por seus tipos base:

```python
class EmbeddingProvider(ABC):
    @abstractmethod
    async def embed(self, text: str) -> list[float]: ...

class OpenAIProvider(EmbeddingProvider): ...
class LocalProvider(EmbeddingProvider): ...
# Ambos substituíveis sem quebrar código cliente
```

### I — Interface Segregation Principle

Interfaces específicas em vez de uma genérica:

```python
# ❌ Interface gorda
class MemoryStore:
    def upsert(self): ...
    def search(self): ...
    def link(self): ...
    def consolidate(self): ...

# ✅ Interfaces segregadas
class Writable(ABC):
    def upsert(self): ...

class Searchable(ABC):
    def search(self): ...
```

### D — Dependency Inversion Principle

Dependa de abstrações, não de implementações concretas:

```python
# ❌ Acoplamento direto
class PersistenceService:
    def __init__(self):
        self.qdrant = QdrantService()  # concreto

# ✅ DI via injeção
class PersistenceService:
    def __init__(self, vector_store: VectorStore, graph_store: GraphStore):
        self.vector_store = vector_store
        self.graph_store = graph_store
```

## DRY — Don't Repeat Yourself

Uma única fonte de verdade (single source of truth):

- Lógica de upsert: APENAS no `PersistenceService`, nunca em tools
- Categorias: APENAS no config/bootstrap, nunca hardcoded
- ID generation: APENAS no `MemoryItem.generate_id()`

## KISS — Keep It Simple

- Prefira composição sobre herança
- Métodos curtos (<10 linhas) e focados
- Guard clauses para early return
- Nomes descritivos que eliminam necessidade de comentários

## YAGNI — You Aren't Gonna Need It

- Não implementar features de Fase 4 na Fase 1
- Não criar abstrações prematuras
- Implementar o mínimo viável, refatorar quando necessário

## ACID (para Persistência Dual)

| Propriedade | Status no TheSearch | Mitigação |
|------------|:---:|-----------|
| **Atomicity** | ⚠️ Parcial | Saga Pattern + WAL |
| **Consistency** | ⚠️ Eventual | Reconciliação na consolidação |
| **Isolation** | ✅ | Cada operação é independente |
| **Durability** | ✅ | Neo4j (WAL nativo) + Qdrant (snapshots) |

## Clean Code Checklist

- [ ] Nomes autoexplicativos (sem comentários necessários)
- [ ] Métodos curtos e focados (SRP)
- [ ] Guard clauses em vez de ifs aninhados
- [ ] Exceções custom em vez de strings de erro genéricas
- [ ] Constantes nomeadas em vez de magic numbers
- [ ] Imports organizados (stdlib → third-party → local)
