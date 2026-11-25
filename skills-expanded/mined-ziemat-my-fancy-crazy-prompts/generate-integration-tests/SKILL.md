name: generate-integration-tests
description: Creates meaningful Python integration tests for module, service, database, API, filesystem, or queue boundaries. Use this when you need to test how components work together with real or realistic dependencies.

---

# Generate Integration Tests

## Purpose

Create meaningful Python integration tests for module, service, database, API, filesystem, or queue boundaries. This skill generates integration tests that verify components work together correctly with real or realistic dependencies.

## Use when

- Testing interactions between multiple modules
- Verifying database operations and queries
- Testing API endpoints with a test client
- Validating filesystem operations
- Testing async service interactions
- Verifying third-party library integrations

## Do not use when

- You need pure unit tests (use `generate-unit-tests`)
- You're testing user-facing workflows (use e2e tests)
- You need to test isolated logic without dependencies

## Inputs

- Python code with dependencies (modules, services, APIs)
- Dependency configuration (database URLs, API keys, etc.)
- Test environment setup (fixtures, mocks, test containers)
- Expected integration behavior

## Outputs

- Complete integration test file
- Test fixtures for dependencies
- Setup/teardown logic for test isolation
- Assertions that verify integration points

## Method

1. **Identify integration boundaries**
   - Database queries and ORM operations
   - API calls (internal or external)
   - Filesystem operations
   - Message queue interactions
   - Network calls

2. **Choose integration approach**
   - **Real dependencies**: Use test DB, test containers, mock servers
   - **Partial mocks**: Mock some deps, use real others
   - **Test doubles**: Use in-memory implementations where possible

3. **Set up test fixtures**
   - Use `pytest.fixture` for shared setup
   - Use `scope="function"` for isolation
   - Use `tmp_path` for filesystem tests
   - Use `testcontainers` for external services

4. **Write integration tests**
   - Test complete workflows, not individual steps
   - Verify end-to-end data flow
   - Check error handling at boundaries
   - Validate performance where relevant

5. **Handle test isolation**
   - Rollback database transactions
   - Clean up filesystem after tests
   - Reset mocks and state
   - Use unique test data per test

## Integration Test Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| **Test client** | Web API testing | Flask/FastAPI test client |
| **Test DB** | Database operations | In-memory SQLite, testcontainers |
| **Mock server** | External API testing | responses, httpretty |
| **Test fixtures** | Shared setup | pytest fixtures with cleanup |
| **Async integration** | Async services | asyncio + test client |

## Guardrails

- Don't make integration tests slower than necessary
- Don't rely on external services that might be unavailable
- Don't skip cleanup; tests must be isolated
- Don't test the same thing in unit and integration tests

## Example prompts

```
Generate integration tests for this service:

```python
class UserService:
    def __init__(self, db: Session, email_service: EmailService):
        self.db = db
        self.email = email_service
    
    def create_user(self, data: dict) -> User:
        user = User(**data)
        self.db.add(user)
        self.db.commit()
        self.email.send_welcome(user.email)
        return user
```

---

Write integration tests for this API endpoint:

```python
@app.post("/api/orders")
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # Create order, update inventory, send notification
    pass
```

---

Generate integration tests for this database repository:

```python
class OrderRepository:
    def find_by_user(self, user_id: int) -> list[Order]:
        return db.query(Order).filter(Order.user_id == user_id).all()
    
    def total_by_status(self, status: str) -> dict[str, int]:
        return db.query(Order.status, func.count()).group_by(Order.status).all()
```
