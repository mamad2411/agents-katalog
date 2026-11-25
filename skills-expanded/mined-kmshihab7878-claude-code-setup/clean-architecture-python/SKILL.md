---
name: clean-architecture-python
description: Hexagonal/Clean Architecture patterns for Python with ports-and-adapters, DDD, repository pattern, and dependency injection
triggers:
  - clean architecture
  - hexagonal
  - ports and adapters
  - domain driven design
  - DDD
  - repository pattern
  - dependency injection
  - SOLID
---

# Clean Architecture for Python

Hexagonal architecture (ports-and-adapters) for Python services. Domain-driven design with clear layer boundaries.

## Layer Structure

```
src/coremind/
  domain/           # Entities, value objects, domain services (NO external deps)
    entities/
    value_objects/
    services/
    exceptions.py
  application/      # Use cases, ports (interfaces), DTOs
    use_cases/
    ports/           # Abstract interfaces (inbound + outbound)
    dtos/
  infrastructure/   # Adapters (implementations of ports)
    persistence/     # Database repos, ORM models
    external/        # API clients, message queues
    config/          # Settings, DI container
  api/              # HTTP/WebSocket adapters (FastAPI routes)
    routes/
    middleware/
```

## Dependency Rule

Dependencies point INWARD only:
- `api` -> `application` -> `domain`
- `infrastructure` -> `application` -> `domain`
- `domain` has ZERO external imports

## Port (Interface)

```python
# application/ports/agent_repository.py
from abc import ABC, abstractmethod
from domain.entities.agent import Agent

class AgentRepository(ABC):
    @abstractmethod
    async def get_by_id(self, agent_id: str) -> Agent | None: ...

    @abstractmethod
    async def save(self, agent: Agent) -> Agent: ...

    @abstractmethod
    async def list_active(self) -> list[Agent]: ...
```

## Adapter (Implementation)

```python
# infrastructure/persistence/postgres_agent_repo.py
from application.ports.agent_repository import AgentRepository
from domain.entities.agent import Agent

class PostgresAgentRepository(AgentRepository):
    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def get_by_id(self, agent_id: str) -> Agent | None:
        async with self._session_factory() as session:
            row = await session.get(AgentModel, agent_id)
            return row.to_domain() if row else None
```

## Use Case

```python
# application/use_cases/create_agent.py
from dataclasses import dataclass
from application.ports.agent_repository import AgentRepository
from domain.entities.agent import Agent

@dataclass
class CreateAgentUseCase:
    repo: AgentRepository  # Injected port, not concrete impl

    async def execute(self, name: str, agent_type: str) -> Agent:
        agent = Agent.create(name=name, agent_type=agent_type)
        return await self.repo.save(agent)
```

## Dependency Injection

```python
# infrastructure/config/container.py
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    db_session = providers.Singleton(create_session_factory, config.database_url)
    agent_repo = providers.Factory(PostgresAgentRepository, session_factory=db_session)
    create_agent = providers.Factory(CreateAgentUseCase, repo=agent_repo)
```

## Testing Each Layer

- **Domain**: Pure unit tests, no mocks needed (no external deps)
- **Application**: Mock the ports, test use case logic
- **Infrastructure**: Integration tests with real DB (Testcontainers)
- **API**: HTTP tests with TestClient, mock use cases
