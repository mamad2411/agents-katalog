---
name: Design Patterns
description: Design Patterns aplicados ao TheSearch — Strategy, Chain of Responsibility, Repository, Observer, Factory, Saga, e Circuit Breaker.
---

# Design Patterns

## Quando Usar

- Ao implementar novos services ou módulos
- Ao refatorar código existente para melhor extensibilidade
- Como referência para decisões de design

## Patterns Aplicados ao TheSearch

### 1. Strategy Pattern — Embedding Providers

Permite trocar o provider de embedding sem alterar código cliente:

```python
from abc import ABC, abstractmethod

class EmbeddingProvider(ABC):
    @abstractmethod
    async def embed(self, text: str) -> list[float]: ...
    @abstractmethod
    async def embed_batch(self, texts: list[str]) -> list[list[float]]: ...

class OpenAIProvider(EmbeddingProvider):
    async def embed(self, text: str) -> list[float]:
        response = await self.client.embeddings.create(input=text, ...)
        return response.data[0].embedding

class SentenceTransformerProvider(EmbeddingProvider):
    async def embed(self, text: str) -> list[float]:
        return self.model.encode(text).tolist()

# Uso
service = EmbeddingService(provider=OpenAIProvider())
service = EmbeddingService(provider=SentenceTransformerProvider())
```

**Aplica-se a:** Embedding, LLM extraction, Reranking.

### 2. Chain of Responsibility — Admission Gates

Cada gate é uma classe independente, composível:

```python
class AdmissionGate(ABC):
    def __init__(self, next_gate: "AdmissionGate | None" = None):
        self.next = next_gate
    
    @abstractmethod
    async def evaluate(self, candidate) -> AdmissionResult | None: ...
    
    async def handle(self, candidate) -> AdmissionResult:
        result = await self.evaluate(candidate)
        if result:
            return result
        if self.next:
            return await self.next.handle(candidate)
        return AdmissionResult("active", "create")

class ProjectGate(AdmissionGate): ...
class EvidenceGate(AdmissionGate): ...
class DuplicateGate(AdmissionGate): ...
class WeightGate(AdmissionGate): ...

# Composição
chain = ProjectGate(EvidenceGate(DuplicateGate(WeightGate())))
result = await chain.handle(candidate)
```

**Vantagem:** Adicionar novo gate = criar classe + inserir na chain.

### 3. Repository Pattern — Abstração de Storage

```python
class MemoryRepository(ABC):
    @abstractmethod
    async def save(self, item: MemoryItem): ...
    @abstractmethod
    async def find_by_id(self, memory_id: str) -> MemoryItem | None: ...
    @abstractmethod
    async def find_by_project(self, project: str) -> list[MemoryItem]: ...

class HybridMemoryRepository(MemoryRepository):
    def __init__(self, neo4j: Neo4jService, qdrant: QdrantService):
        self.neo4j = neo4j
        self.qdrant = qdrant
    
    async def save(self, item: MemoryItem):
        self.qdrant.upsert(item.memory_id, item.embedding, item)
        await self.neo4j.upsert_memory(item.memory_id, ...)
```

**Vantagem:** Isola lógica de persistência. Testes usam `InMemoryRepository`.

### 4. Observer Pattern — Telemetria

```python
class MemoryEventBus:
    def __init__(self):
        self.listeners: dict[str, list[Callable]] = defaultdict(list)
    
    def subscribe(self, event_type: str, callback: Callable):
        self.listeners[event_type].append(callback)
    
    async def emit(self, event_type: str, data: dict):
        for callback in self.listeners[event_type]:
            await callback(data)

# Registrar listeners
bus = MemoryEventBus()
bus.subscribe("retrieval", telemetry.record_retrieval)
bus.subscribe("memory_created", audit.log_memory_change)
```

**Vantagem:** Desacopla telemetria/auditoria da lógica de negócio.

### 5. Factory Method — Criação de MemoryItem

```python
class MemoryItemFactory:
    @staticmethod
    def from_candidate(candidate: MemoryCandidate, admission: AdmissionResult) -> MemoryItem:
        memory_id = admission.memory_id or MemoryItem.generate_id(...)
        return MemoryItem(
            memory_id=memory_id,
            project=candidate.project,
            category=candidate.type,
            weight_confidence=min(len(candidate.evidence) * 0.25, 1.0),
            ...
        )
```

### 6. Saga Pattern — Persistência Dual

```python
class PersistenceSaga:
    async def execute(self, item: MemoryItem, embedding: list[float]):
        try:
            self.qdrant.upsert(item.memory_id, embedding, item)
        except Exception:
            raise  # Nada para compensar
        
        try:
            await self.neo4j.upsert_memory(item.memory_id, ...)
        except Exception:
            self.qdrant.delete(item.memory_id)  # Compensação
            raise
```

### 7. Circuit Breaker — APIs Externas

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failures = 0
        self.threshold = failure_threshold
        self.state = "closed"  # closed | open | half-open
    
    async def call(self, func, *args):
        if self.state == "open":
            raise ServiceUnavailableError("Circuit breaker open")
        try:
            result = await func(*args)
            self.failures = 0
            return result
        except Exception:
            self.failures += 1
            if self.failures >= self.threshold:
                self.state = "open"
            raise
```

## Mapa de Patterns no TheSearch

| Pattern | Módulo | Status |
|---------|--------|:------:|
| Strategy | EmbeddingService | 📋 Recomendado |
| Chain of Responsibility | AdmissionService | 📋 Recomendado |
| Repository | PersistenceService | 📋 Recomendado |
| Observer | TelemetryService | 📋 Recomendado |
| Factory Method | MemoryItem | ⚠️ Parcial |
| Saga | Persistência dual | 📋 Recomendado |
| Circuit Breaker | OpenAI API | 📋 Recomendado |
