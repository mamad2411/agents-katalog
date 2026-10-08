---
name: python-clean-arch
description: Python Clean Architecture patterns - project structure, layers, DI, FastAPI/Flask integration, testing
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: python
---

# Purpose

Strict Clean Architecture for Python apps. Layered design, dependency inversion, testability.

## Project Structure

```text
src/
├── domain/              # Entities, value objects, exceptions
├── use_cases/           # Business rules, port definitions
├── adapters/            # API routers, persistence, DTOs
├── infrastructure/      # DI container, config, entry point
└── tests/               # unit/ (no I/O), integration/ (real infra)
```

## Dependency Rule

```text
Domain ← Use Cases ← Adapters ← Infrastructure
Dependencies flow INWARD ONLY
```

- Domain: zero imports from outer layers, no framework deps
- Use Cases: import only domain, define ports as ABCs
- Adapters: implement ports, framework code here
- Infrastructure: wiring, DI, startup

## Dependency Injection

```python
class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: str) -> User | None: ...
    @abstractmethod
    async def save(self, user: User) -> None: ...

class CreateUserUseCase:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo  # Port injected, not concrete
```

Constructor injection. Wire in composition root.

## FastAPI Integration

- Routers in `adapters/api/` — thin, delegate to use cases
- Pydantic in `adapters/dto/` (NOT domain entities)
- Map DTO ↔ Domain at adapter boundary

## Testing Strategy

| Layer       | Mocks?                    | I/O? |
| ----------- | ------------------------- | ---- |
| Domain      | None                      | No   |
| Use Cases   | Mock ports (ABC)          | No   |
| Adapters    | Test doubles / real infra | Yes  |
| Integration | Minimal                   | Yes  |

## Anti-patterns

- Domain importing SQLAlchemy/Pydantic/FastAPI
- Use cases calling HTTP/DB directly (bypass ports)
- Business logic in routers
- Domain entities used as Pydantic models
- God use cases — split by feature

## When to Use

- New apps with complex business logic
- Refactoring monoliths
- Code review for violations
