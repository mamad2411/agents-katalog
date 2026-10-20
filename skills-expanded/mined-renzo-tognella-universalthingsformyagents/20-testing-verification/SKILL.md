---
name: Testing & Verification
description: Estratégia de testes para o TheSearch — pytest, testes unitários com mocks, testes de integração com testcontainers, E2E, fixtures, e property-based testing.
---

# Testing & Verification

## Quando Usar

- Ao criar testes para novos services ou módulos
- Ao configurar a infraestrutura de testes
- Ao validar o pipeline completo E2E

## Pirâmide de Testes

```
         /  E2E  \          ← Poucos, lentos, validam pipeline completo
        /─────────\
       / Integração \       ← Médios, testam services + infra (Docker)
      /──────────────\
     /   Unitários    \     ← Muitos, rápidos, testam lógica isolada
    /──────────────────\
```

## Estrutura de Diretórios

```
tests/
├── conftest.py           # Fixtures compartilhadas
├── unit/
│   ├── test_weight_service.py
│   ├── test_admission_service.py
│   ├── test_sanitization_service.py
│   ├── test_context_resolver.py
│   └── test_memory_item.py
├── integration/
│   ├── test_neo4j_service.py
│   ├── test_qdrant_service.py
│   ├── test_persistence_service.py
│   └── test_hybrid_search.py
└── e2e/
    └── test_full_pipeline.py
```

## Testes Unitários (com Mocks)

```python
import pytest
from unittest.mock import AsyncMock, MagicMock
from services.admission_service import AdmissionService
from models.memory_candidate import MemoryCandidate, EvidenceRef

class TestAdmissionService:
    @pytest.fixture
    def qdrant_mock(self):
        return MagicMock()
    
    @pytest.fixture
    def embeddings_mock(self):
        mock = AsyncMock()
        mock.embed.return_value = [0.1] * 512
        return mock
    
    @pytest.fixture
    def service(self, qdrant_mock, embeddings_mock):
        return AdmissionService(qdrant_mock, embeddings_mock)
    
    @pytest.mark.asyncio
    async def test_gate_a_rejects_without_project(self, service):
        candidate = MemoryCandidate(
            project="", type="DesignRule", title="Test", summary="Test"
        )
        result = await service.evaluate(candidate)
        assert result.status == "rejected"
        assert result.reason == "Sem projeto definido"
    
    @pytest.mark.asyncio
    async def test_gate_b_rejects_without_evidence(self, service):
        candidate = MemoryCandidate(
            project="CORE", type="DesignRule", title="Test",
            summary="Test", evidence=[]
        )
        result = await service.evaluate(candidate)
        assert result.status == "evidence_only"
    
    @pytest.mark.asyncio
    async def test_admits_valid_candidate(self, service, qdrant_mock):
        qdrant_mock.find_similar.return_value = []
        candidate = MemoryCandidate(
            project="CORE", type="DesignRule", title="Forms Pattern",
            summary="Use forms for all writes",
            proposed_weight=0.8,
            evidence=[EvidenceRef(type="commit", ref="abc123", snippet="...")]
        )
        result = await service.evaluate(candidate)
        assert result.status == "active"
        assert result.action == "create"
```

## Testes de Integração (com Docker)

```python
import pytest
from testcontainers.neo4j import Neo4jContainer
from testcontainers.core.container import DockerContainer

@pytest.fixture(scope="session")
def neo4j_container():
    with Neo4jContainer("neo4j:5.26-community") as container:
        yield container

@pytest.fixture(scope="session")
def qdrant_container():
    with DockerContainer("qdrant/qdrant:v1.13.2").with_exposed_ports(6333) as container:
        yield container

@pytest.fixture
async def neo4j_service(neo4j_container):
    service = Neo4jService(uri=neo4j_container.get_connection_url())
    yield service
    await service.close()
```

## Property-Based Testing (WeightService)

```python
from hypothesis import given, strategies as st

class TestWeightServiceProperties:
    @given(
        manual=st.floats(min_value=0, max_value=1),
        confidence=st.floats(min_value=0, max_value=1),
        usage=st.floats(min_value=0, max_value=1),
        feedback=st.floats(min_value=0, max_value=1),
    )
    def test_effective_weight_always_between_0_and_1(
        self, manual, confidence, usage, feedback
    ):
        svc = WeightService()
        result = svc.calculate_effective_weight(manual, confidence, usage, feedback)
        assert 0.0 <= result <= 1.0
    
    @given(significance=st.floats(min_value=0, max_value=1))
    def test_decay_always_between_0_and_1(self, significance):
        svc = WeightService()
        result = svc.calculate_decay(significance, datetime.utcnow() - timedelta(days=30))
        assert 0.0 <= result <= 1.0
```

## Comandos

```bash
# Rodar todos os testes
pytest

# Testes unitários apenas
pytest tests/unit -v

# Testes de integração (precisa de Docker)
pytest tests/integration -v

# Com cobertura
pytest --cov=services --cov-report=term-missing

# Fail-fast
pytest --fail-fast

# Teste específico
pytest tests/unit/test_admission_service.py::TestAdmissionService::test_gate_a -v
```

## Dependências de Teste

```toml
[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "pytest-cov>=5.0",
    "hypothesis>=6.0",
    "testcontainers[neo4j]>=4.0",
    "ruff>=0.3",
]
```

## Regras

- Cada service DEVE ter testes unitários com mocks
- Testes de integração usam testcontainers (Docker real)
- E2E valida o pipeline completo (bootstrap → query)
- Property-based testing para funções matemáticas (pesos, decay)
- `pytest-asyncio` para testes async
- Arrange → Act → Assert em todo teste
- `pytest.fixture` com `scope` adequado (function/session)
- NUNCA depender de estado externo em testes unitários
