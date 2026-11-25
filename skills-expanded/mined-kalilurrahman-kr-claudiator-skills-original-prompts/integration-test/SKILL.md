---
name: integration-test
description: Design integration tests for APIs, databases, and external services. Outputs test strategies, fixtures, mocking, and CI integration.
argument-hint: [system components, integration points, test environment]
allowed-tools: Read, Write, Bash
---

# Integration Testing Strategy

Design integration tests that verify component interactions work correctly. Not unit tests — real databases, message queues, APIs, with proper fixtures, teardown, and isolation.

## Process

1. **Identify integration points.** API → DB, Service → Queue, App → External API.
2. **Choose test scope.** Single service + dependencies vs multi-service.
3. **Setup test environment.** Docker Compose, test databases, mock services.
4. **Design fixtures.** Seed data, test users, realistic scenarios.
5. **Handle external deps.** Mock third-party APIs or use sandbox environments.
6. **Plan cleanup.** Transaction rollback, database reset, queue purge.
7. **Integrate with CI.** Run on every PR, parallel execution.

## Output Format

### Integration Tests: [System Name]

**Framework:** pytest + testcontainers  
**Scope:** API + PostgreSQL + Redis  
**Execution:** Docker Compose (local), GitHub Actions (CI)  
**Coverage:** 80% of critical paths  
**Duration:** 2 minutes (full suite)

---

## Test Pyramid

```
     /\
    /  \   E2E Tests (UI → API → DB)
   /____\  ← 10% (slow, brittle)
  /      \
 / Integration \ API → DB, Service → Queue
/___Tests______\ ← 30% (medium speed)
/              \
/  Unit Tests   \ Pure functions, business logic
/_________________\ ← 60% (fast, isolated)
```

**Integration tests verify:**
- Database queries return correct data
- API contracts honored
- Message queues process messages
- Cache invalidation works
- External API integration

---

## Test Structure (pytest)

```python
# tests/integration/test_order_api.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models import User, Product

# Test database
TEST_DB_URL = "postgresql://test:test@localhost:5433/test_db"
engine = create_engine(TEST_DB_URL)
TestSessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Create fresh DB for each test"""
    Base.metadata.create_all(bind=engine)
    session = TestSessionLocal()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session):
    """Test client with overridden DB dependency"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def test_user(db_session):
    """Create test user"""
    user = User(email="test@example.com", name="Test User")
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def test_products(db_session):
    """Create test products"""
    products = [
        Product(name="Product A", price=10.00, stock=100),
        Product(name="Product B", price=20.00, stock=50),
    ]
    db_session.add_all(products)
    db_session.commit()
    return products

def test_create_order(client, test_user, test_products):
    """Test complete order creation flow"""
    response = client.post("/api/orders", json={
        "user_id": test_user.id,
        "items": [
            {"product_id": test_products[0].id, "quantity": 2},
            {"product_id": test_products[1].id, "quantity": 1},
        ]
    })
    
    assert response.status_code == 201
    data = response.json()
    
    # Verify response structure
    assert "order_id" in data
    assert data["total_amount"] == 40.00  # 10*2 + 20*1
    
    # Verify database state
    order = db_session.query(Order).filter_by(id=data["order_id"]).one()
    assert len(order.items) == 2
    assert order.status == "pending"
    
    # Verify inventory reduced
    product_a = db_session.query(Product).get(test_products[0].id)
    assert product_a.stock == 98  # 100 - 2

def test_order_out_of_stock(client, test_user, test_products):
    """Test order fails when product out of stock"""
    # Set stock to 0
    test_products[0].stock = 0
    db_session.commit()
    
    response = client.post("/api/orders", json={
        "user_id": test_user.id,
        "items": [{"product_id": test_products[0].id, "quantity": 1}]
    })
    
    assert response.status_code == 400
    assert "out of stock" in response.json()["error"].lower()
```

---

## Docker Test Environment

```yaml
# docker-compose.test.yml
version: '3.8'

services:
  test-db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
      POSTGRES_DB: test_db
    ports:
      - "5433:5432"
    tmpfs:
      - /var/lib/postgresql/data  # In-memory for speed
  
  test-redis:
    image: redis:7-alpine
    ports:
      - "6380:6379"
  
  test-app:
    build:
      context: .
      dockerfile: Dockerfile.test
    environment:
      DATABASE_URL: postgresql://test:test@test-db:5432/test_db
      REDIS_URL: redis://test-redis:6379
      TESTING: "true"
    depends_on:
      - test-db
      - test-redis
    command: pytest tests/integration -v
```

**Run tests:**
```bash
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

---

## Testcontainers (Dynamic Docker)

```python
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

@pytest.fixture(scope="session")
def postgres_container():
    """Start PostgreSQL in Docker"""
    with PostgresContainer("postgres:15") as postgres:
        yield postgres

@pytest.fixture(scope="session")
def redis_container():
    """Start Redis in Docker"""
    with RedisContainer("redis:7") as redis:
        yield redis

@pytest.fixture
def db_engine(postgres_container):
    """Create DB engine from container"""
    from sqlalchemy import create_engine
    engine = create_engine(postgres_container.get_connection_url())
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

def test_with_real_postgres(db_engine):
    """Test runs against real PostgreSQL in Docker"""
    session = Session(db_engine)
    user = User(email="test@example.com")
    session.add(user)
    session.commit()
    
    assert session.query(User).count() == 1
```

---

## Mocking External APIs

### Option 1: HTTP Mocking (responses library)
```python
import responses

@responses.activate
def test_payment_integration():
    # Mock Stripe API
    responses.add(
        responses.POST,
        "https://api.stripe.com/v1/charges",
        json={"id": "ch_123", "status": "succeeded"},
        status=200
    )
    
    # Test code that calls Stripe
    result = payment_service.charge(amount=100, token="tok_visa")
    
    assert result["status"] == "succeeded"
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "https://api.stripe.com/v1/charges"
```

### Option 2: Fake Server (WireMock, mock-server)
```python
from wiremock import WireMock

@pytest.fixture(scope="module")
def wiremock():
    wm = WireMock(host="localhost", port=8080)
    yield wm
    wm.reset()

def test_external_api(wiremock):
    # Stub external API
    wiremock.stub_for(
        wiremock.get("/api/users/123")
        .will_return(
            status=200,
            headers={"Content-Type": "application/json"},
            body='{"id": "123", "name": "Test User"}'
        )
    )
    
    # Test code calls localhost:8080 instead of real API
    user = external_api.get_user("123")
    assert user["name"] == "Test User"
```

### Option 3: Sandbox Environment
```python
# Use Stripe test mode
STRIPE_TEST_KEY = "sk_test_..."

def test_real_stripe_sandbox():
    """Test against Stripe's test environment"""
    stripe.api_key = STRIPE_TEST_KEY
    
    # Use test card
    charge = stripe.Charge.create(
        amount=1000,
        currency="usd",
        source="tok_visa"  # Stripe test token
    )
    
    assert charge.status == "succeeded"
```

---

## Database Fixtures

### Fixture Factory Pattern
```python
# conftest.py
import pytest
from faker import Faker

fake = Faker()

class UserFactory:
    @staticmethod
    def create(db, **kwargs):
        defaults = {
            "email": fake.email(),
            "name": fake.name(),
            "created_at": fake.date_time_this_year()
        }
        defaults.update(kwargs)
        
        user = User(**defaults)
        db.add(user)
        db.commit()
        return user

@pytest.fixture
def user_factory(db_session):
    return UserFactory()

# Usage in tests
def test_user_operations(user_factory):
    user1 = user_factory.create(email="user1@test.com")
    user2 = user_factory.create(email="user2@test.com")
    
    assert user1.id != user2.id
```

### SQL Fixtures
```python
@pytest.fixture
def seed_database(db_session):
    """Load SQL fixtures"""
    with open("tests/fixtures/sample_data.sql") as f:
        db_session.execute(f.read())
    db_session.commit()

# sample_data.sql
INSERT INTO users (email, name) VALUES
    ('user1@test.com', 'User One'),
    ('user2@test.com', 'User Two');

INSERT INTO products (name, price, stock) VALUES
    ('Product A', 10.00, 100),
    ('Product B', 20.00, 50);
```

---

## Transaction Rollback Pattern

```python
@pytest.fixture(scope="function")
def db_session():
    """Each test runs in a transaction that's rolled back"""
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

# Tests leave no data in DB
def test_create_user(db_session):
    user = User(email="test@example.com")
    db_session.add(user)
    db_session.commit()
    
    assert db_session.query(User).count() == 1
    # After test: rollback, count = 0
```

---

## Message Queue Testing

```python
import pytest
from kombu import Queue, Exchange
from celery import Celery

@pytest.fixture
def celery_app():
    """Celery app with test broker"""
    app = Celery(broker='redis://localhost:6380/0')
    app.conf.update(task_always_eager=True)  # Execute tasks synchronously
    return app

def test_order_created_task(celery_app, test_order):
    """Test async task execution"""
    from app.tasks import send_order_confirmation
    
    # Task executes immediately in tests
    result = send_order_confirmation.delay(test_order.id)
    
    assert result.successful()
    
    # Verify email sent (check mock or DB)
    emails = db.query(SentEmail).filter_by(order_id=test_order.id).all()
    assert len(emails) == 1
```

---

## Parallel Test Execution

```python
# pytest.ini
[pytest]
addopts = -n auto --dist loadgroup

# tests/integration/test_orders.py
@pytest.mark.order_tests  # Group marker
class TestOrders:
    def test_create_order(self): ...
    def test_update_order(self): ...

# Run with parallelism
pytest tests/integration -n 4  # 4 workers
```

---

## CI/CD Integration

```yaml
# .github/workflows/integration-tests.yml
name: Integration Tests

on: [pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      
      redis:
        image: redis:7
        ports:
          - 6379:6379
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements-test.txt
      
      - name: Run integration tests
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379
        run: |
          pytest tests/integration -v --cov --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## Test Data Management

```python
# Separate test data from production
class TestConfig:
    TESTING = True
    DATABASE_URL = "postgresql://test:test@localhost:5433/test_db"
    REDIS_URL = "redis://localhost:6380"
    STRIPE_API_KEY = "sk_test_..."
    SEND_EMAILS = False  # Don't send real emails

# app/config.py
import os

if os.getenv("TESTING"):
    config = TestConfig
else:
    config = ProductionConfig
```

## Rules

- Integration tests require real dependencies (DB, queue, cache), not mocks — verifies actual behavior.
- Each test must be isolated — use transactions or database reset to prevent test pollution.
- Test databases must be separate from development/production databases.
- External API calls mocked or use sandbox environments — avoid production API usage in tests.
- Fixtures create minimal required data — avoid large seed files that slow tests.
- Tests run in CI on every PR — integration tests catch issues before production.
- Parallel execution recommended for large suites — reduce feedback time from 10min to 2min.
- Docker Compose or testcontainers for consistent test environment across developers.
- Cleanup after tests (rollback transactions, purge queues) — leave no trace.
- Integration test coverage 70-80% of critical paths, not 100% — focus on important flows.
